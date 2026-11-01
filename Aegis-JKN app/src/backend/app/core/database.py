"""Database engine and session management for Aegis-JKN.

Design notes
------------
* ``Base`` is re-exported from :mod:`src.backend.app.models.base`.  Declaring a
  second ``DeclarativeBase`` in this module would register models against a
  different metadata registry, so ``create_all`` would silently create nothing.
* No engine is built at import time, and ``sqlalchemy.ext.asyncio`` is never
  imported at module scope.  On SQLAlchemy >= 2.1 that package raises
  ``ImportError`` during import when the ``greenlet`` package is absent, which
  used to break every import of this module.  The engine is now created lazily
  by :func:`get_engine`, which retries against a local SQLite (aiosqlite) URL
  and finally degrades to ``None`` instead of exploding.
* Model modules are imported inside :func:`init_db` only, which keeps this
  module free of ``models -> database -> models`` import cycles.
"""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, AsyncGenerator, Dict, List, Optional

from fastapi import HTTPException

from ..models.base import Base
from .config import get_settings

if TYPE_CHECKING:  # typing only; sqlalchemy.ext.asyncio is imported lazily below
    from sqlalchemy.ext.asyncio import (
        AsyncEngine,
        AsyncSession,
        async_sessionmaker,
    )

__all__ = [
    "Base",
    "DRIVER_UNAVAILABLE_MESSAGE",
    "AsyncSessionLocal",
    "engine",
    "get_engine",
    "get_sessionmaker",
    "get_db",
    "init_db",
    "close_db",
]

logger = logging.getLogger(__name__)

settings = get_settings()

#: Last-resort local database used when the configured driver is not usable.
SQLITE_FALLBACK_URL = "sqlite+aiosqlite:///./aegis_jkn.db"

#: Message surfaced to API clients when no async database driver can be loaded.
DRIVER_UNAVAILABLE_MESSAGE = (
    "database driver unavailable: install sqlalchemy[asyncio] + greenlet"
)

# Module-level handles. They stay ``None`` until get_engine() succeeds; this is
# the supported way to detect a driver-less runtime before using the ORM.
engine: Optional[AsyncEngine] = None
AsyncSessionLocal: Optional[async_sessionmaker] = None

_engine_attempted: bool = False
_last_engine_error: Optional[str] = None


def _driver_label(url: str) -> str:
    """Return just the dialect+driver part of a URL (never logs credentials)."""
    return url.split("://", 1)[0] if "://" in url else url


def _engine_options(url: str) -> Dict[str, Any]:
    """Build ``create_async_engine`` kwargs.

    Pool sizing is only valid for pooled dialects; SQLite's aiosqlite dialect
    rejects ``pool_size``/``max_overflow``, so those keys are skipped for it.
    """
    options: Dict[str, Any] = {
        "echo": bool(settings.debug),
        "pool_pre_ping": True,
    }
    if not url.startswith("sqlite"):
        options["pool_size"] = settings.database_pool_size
        options["max_overflow"] = settings.database_max_overflow
        options["pool_recycle"] = 3600
    return options


def _candidate_urls() -> List[str]:
    """Configured database URL first, then the local SQLite fallback."""
    configured = (settings.database_url or "").strip() or SQLITE_FALLBACK_URL
    urls = [configured]
    if configured != SQLITE_FALLBACK_URL:
        urls.append(SQLITE_FALLBACK_URL)
    return urls


def get_engine() -> Optional[AsyncEngine]:
    """Return the cached async engine, creating it on first call.

    Safe to call at import time by accident: it never raises.  Returns ``None``
    when neither the configured driver nor the SQLite fallback can be created
    (for example when ``greenlet`` is not installed), and the reason is logged
    once so operators can see it instead of a bare traceback.
    """
    global engine, AsyncSessionLocal, _engine_attempted, _last_engine_error

    if _engine_attempted:
        return engine

    _engine_attempted = True

    for url in _candidate_urls():
        try:
            # Imported lazily on purpose: on SQLAlchemy >= 2.1 merely importing
            # sqlalchemy.ext.asyncio raises ImportError when greenlet is absent.
            from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

            candidate = create_async_engine(url, **_engine_options(url))
        except (ImportError, ModuleNotFoundError) as exc:
            # Missing greenlet or missing DBAPI driver: try the next candidate.
            _last_engine_error = "{}: {}".format(type(exc).__name__, exc)
            logger.warning(
                "Async database driver unavailable for %s: %s",
                _driver_label(url),
                exc,
            )
            continue
        except Exception as exc:  # malformed URL, invalid pool options, ...
            _last_engine_error = "{}: {}".format(type(exc).__name__, exc)
            logger.warning(
                "Could not create async engine for %s: %s",
                _driver_label(url),
                exc,
            )
            continue

        engine = candidate
        AsyncSessionLocal = async_sessionmaker(
            bind=candidate,
            class_=AsyncSession,
            expire_on_commit=False,
            autoflush=False,
        )
        logger.info("Async database engine ready (%s)", _driver_label(url))
        return engine

    engine = None
    AsyncSessionLocal = None
    logger.warning(
        "%s (last error: %s)", DRIVER_UNAVAILABLE_MESSAGE, _last_engine_error
    )
    return None


def get_sessionmaker() -> async_sessionmaker:
    """Return the session factory, raising HTTP 503 when the DB is unusable."""
    if AsyncSessionLocal is None:
        get_engine()
    if AsyncSessionLocal is None:
        raise HTTPException(
            status_code=503,
            detail=DRIVER_UNAVAILABLE_MESSAGE,
        )
    return AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency yielding a session, or HTTP 503 with no driver."""
    session_factory = get_sessionmaker()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Create tables for every registered model.

    Model modules are imported here (not at module scope) so that they can
    import this module without a circular import.  When no async driver is
    available the call logs a warning and returns instead of aborting startup.
    """
    engine_obj = get_engine()
    if engine_obj is None:
        logger.warning(
            "Skipping database initialisation: %s", DRIVER_UNAVAILABLE_MESSAGE
        )
        return

    # Import side effect registers every table on Base.metadata.
    from .. import models  # noqa: F401  (imported for model registration)

    async with engine_obj.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database initialised (%d tables)", len(Base.metadata.tables))


async def close_db() -> None:
    """Dispose the engine and reset the lazy cache (safe to call twice)."""
    global engine, AsyncSessionLocal, _engine_attempted

    if engine is not None:
        await engine.dispose()
    engine = None
    AsyncSessionLocal = None
    _engine_attempted = False