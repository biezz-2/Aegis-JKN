import os
import logging
from typing import Dict, Any, Optional
from hvac import Client
from hvac.exceptions import VaultError

logger = logging.getLogger(__name__)

class VaultClient:
    """
    HashiCorp Vault Client for Aegis-JKN.
    Handles authentication and secret retrieval.
    """
    def __init__(self):
        self._client: Optional[Client] = None
        self._secrets_cache: Dict[str, Any] = {}

        # Configuration from environment
        self.vault_url = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
        self.vault_token = os.getenv("VAULT_TOKEN") # Simplified for dev, use AppRole/K8s in prod
        self.vault_role_id = os.getenv("VAULT_ROLE_ID")
        self.vault_secret_id = os.getenv("VAULT_SECRET_ID")

    def authenticate(self) -> bool:
        """
        Authenticates with Vault.
        Tries AppRole first, then falls back to token.
        """
        try:
            self._client = Client(url=self.vault_url)

            if self.vault_role_id and self.vault_secret_id:
                # AppRole Authentication
                auth_res = self._client.auth.approle.login(
                    role_id=self.vault_role_id,
                    secret_id=self.vault_secret_id
                )
                self._client.token = auth_res['auth']['client_token']
                logger.info("Authenticated with Vault via AppRole")
            elif self.vault_token:
                # Token Authentication
                self._client.token = self.vault_token
                logger.info("Authenticated with Vault via Token")
            else:
                logger.warning("No Vault credentials found in environment")
                return False

            return self._client.is_authenticated()
        except VaultError as e:
            logger.error(f"Vault authentication failed: {str(e)}")
            return False

    def get_secret(self, path: str, key: str) -> Optional[str]:
        """
        Retrieves a secret from Vault KV store.
        """
        if not self._client or not self._client.is_authenticated():
            if not self.authenticate():
                return None

        # Check cache first
        cache_key = f"{path}:{key}"
        if cache_key in self._secrets_cache:
            return self._secrets_cache[cache_key]

        try:
            # Read KV v2 secret
            response = self._client.secrets.kv.v2.read_secret_version(path=path)
            secret_data = response['data']['data']
            val = secret_data.get(key)

            if val:
                self._secrets_cache[cache_key] = val
            return val
        except VaultError as e:
            logger.error(f"Failed to fetch secret {path}/{key} from Vault: {str(e)}")
            return None

    def clear_cache(self):
        self._secrets_cache.clear()

# Singleton instance
_vault_instance = None

def get_vault_client() -> VaultClient:
    global _vault_instance
    if _vault_instance is None:
        _vault_instance = VaultClient()
    return _vault_instance

def load_secrets_from_vault(path: str) -> Dict[str, Any]:
    """
    Utility to load all secrets from a specific Vault path.
    """
    client = get_vault_client()
    if not client._client or not client._client.is_authenticated():
        client.authenticate()

    try:
        response = client._client.secrets.kv.v2.read_secret_version(path=path)
        return response['data']['data']
    except Exception as e:
        logger.error(f"Error loading secrets from {path}: {str(e)}")
        return {}
