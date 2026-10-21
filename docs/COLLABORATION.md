# Aegis-JKN Controlled Collaboration & Workspace Isolation Guide

## 1. Arsitektur Kolaborasi

Sistem kolaborasi Aegis-JKN menggunakan model **Authoritative Owner Source + Controlled Shared Realtime Workspace**:

* **Source Owner (Authoritative)**: `/home/biezz/Documents/Project/coding/Aegis-JKN`

* **Shared Workspace**: `/srv/aegis-jkn/workspace` (fallback `~/.collab/aegis-jkn`)

* **State & Conflict Store**: `/home/biezz/.collab-state/aegis-jkn/`

* **Sync Daemon**: `aegis-owner-sync.py` (stat-based signature + SHA-256 conflict detector)

### Alur Perubahan

1. **Owner → Shared (Otomatis Satu Arah)**: Setiap perubahan file yang dibuat oleh owner di direktori aslinya disinkronkan otomatis dalam 1–2 detik ke shared workspace.

2. **Shared Workspace**: Anggota tim (KPT & Malik) membuka shared workspace sebagai `/workspace` di editor masing-masing. Perubahan file langsung terlihat antar-anggota melalui filesystem watcher.

3. **Shared → Owner (Manual Review / Non-Overwrite)**: Perubahan anggota di shared workspace tidak menimpa file owner secara otomatis untuk mencegah kerusakan atau penimpaan tidak sengaja.

4. **Deteksi Konflik**: Jika owner dan anggota mengedit file yang sama secara bersamaan, sistem tidak menimpa versi manapun. Kedua versi disimpan di: `/home/biezz/.collab-state/aegis-jkn/conflicts/<YYYYMMDD-HHMMSS>/`

## 2. Batas Realtime

* **Realtime Berbasis Filesystem**: Anggota tim mengedit berkas di shared storage yang sama. Simpan file akan memicu file-watcher di editor anggota lain.

* **Bukan CRDT / Google Docs Presence**: Tidak ada fitur multi-kursor bersamaan atau auto-merge per karakter. Hindari mengedit baris kode yang persis sama pada saat yang sama tanpa koordinasi.

## 3. Model Keamanan & Isolasi OS

* **Akun OS Mandiri**: User `kpt` dan `malik` berjalan di bawah akun sistem Linux terpisah tanpa shell login (`/usr/sbin/nologin`).

* **File System Sandboxing**:

  * `ProtectHome=tmpfs`: Direktori `/home/biezz` sepenuhnya tidak terlihat dan tidak dapat diakses oleh KPT dan Malik.

  * `ProtectSystem=strict`: Direktori sistem `/usr`, `/boot`, `/etc` berstatus read-only.

  * `/workspace`: Hanya direktori kolaborasi yang di-bind rw ke dalam sandbox.

* **Autentikasi Gateway**: Akses browser dikontrol penuh oleh `ide-gateway.js` dengan token autentikasi. KPT dan Malik tidak dapat mengakses socket IPC atau sandbox satu sama lain.
