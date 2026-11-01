# Panduan Penggunaan & Arsitektur Sistem Aegis-JKN

Platform Kecurangan Klaim JKN Terpadu berbasis **Multi-Channel Heterogeneous Graph Structure Learning (MHGSL)**, **Late Fusion Multimodal**, dan **Audit Kriptografis SHA-256 / Ed25519**.

---

## 1. Arsitektur & Cara Kerja Sistem

Aegis-JKN mendeteksi anomali dan indikasi sindikat kecurangan (fraud) pada klaim BPJS Kesehatan melalui 4 lapisan inti:

### A. Tiga Kanal Graf MHGSL (Multi-Channel Graph)
1. **Kanal Topologi (Topology Channel)**:
   - Merepresentasikan relasi entitas klaim: `Pasien (P) <-> Dokter DPJP (D) <-> Faskes/RS (H)`.
   - Menghitung koefisien *clustering* dan deteksi siklus rujukan sirkular/kolusif (syndicate rings) menggunakan Graph Attention Network (GAT).
2. **Kanal Fitur (Feature Similarity Channel)**:
   - Menghitung kemiripan vektor fitur (*cosine similarity*) antar klaim: LOS (Length of Stay), biaya klaim, rasio tindakan sekunder, dan keparahan diagnosis.
   - Mengelompokkan klaim dengan pola tagihan serupa meski diajukan oleh dokter atau rumah sakit berbeda.
3. **Kanal Semantik Rekam Medis (Semantic Channel)**:
   - Mengekstraksi embedding klinis dari narasi rekam medis dokter (resume medis) dan pengakuan anamnesis pasien via representasi BioBERT.
   - Menghitung diskrepansi semantik: jika narasi dokter menuliskan tindakan operasi besar (misal PCI / Bedah Femur) namun anamnesis keluhan mencatat rawat jalan ringan tanpa tindakan invasif, kanal ini menghasilkan skor deviasi tinggi.

### B. Late Fusion Multimodal
Skor akhir klaim dihitung menggabungkan kanal graf struktur ($p_{\text{graph}}$) dengan penalti kontradiksi teks ($f_{\text{text}}$):
$$p_{\text{fused}} = p_{\text{graph}} + 0.10 \times f_{\text{text}} \times (1 - p_{\text{graph}})$$
- Memprioritaskan klaim yang memiliki kontradiksi narasi langsung ke antrean teratas verifikator.

### C. Human-in-the-Loop (HITL) Workstation
- Verifikator menerima rekomendasi terstruktur dari AI Dossier.
- Pilihan putusan verifikator:
  - **SETUJUI KLAIM**: Klaim lolos verifikasi klinis dan administratif.
  - **KLARIFIKASI RS**: Meminta dokumen rekam medis tambahan ke Faskes.
  - **ESKALASI P2PK**: Mengirim berkas ke Tim Pencegahan & Penanganan Kecurangan (P2PK) BPJS Kesehatan untuk audit investigatif lapangan.

### D. Audit Kriptografis & Integritas Data (UU PDP No. 27/2022)
Setiap putusan verifikator disegel dalam buku besar rantai hash SHA-256 (*Hash Chain*):
$$\text{Hash}_n = \text{SHA-256}(\text{Index} \parallel \text{Timestamp} \parallel \text{ClaimID} \parallel \text{Verifikator} \parallel \text{Aksi} \parallel \text{PrevHash})$$
- Genesis block dimulai dengan `0` sebanyak 64 karakter.
- Perubahan apa pun pada catatan lampau otomatis memutus rantai integritas (terdeteksi seketika oleh modul verifikasi).

---

## 2. Struktur Direktori Proyek

```
HEALTHKATHON/
├── Aegis-JKN app/
│   ├── frontend/             # SvelteKit + Svelte 5 + Tailwind CSS v4 UI Workstation
│   │   ├── src/
│   │   │   ├── lib/
│   │   │   │   ├── components/  # Komponen UI (Graf 3D, Queue, EMR, AI Dossier, Topbar)
│   │   │   │   ├── stores/      # Svelte runes store (dashboard, i18n, theme)
│   │   │   │   └── claims.ts    # Model data, normalizer, & filter engine
│   │   │   └── routes/
│   │   │       ├── +page.svelte # Landing page & showcase MHGSL
│   │   │       ├── app/         # Workstation Verifikator Klaim (HITL)
│   │   │       └── it/          # IT Dashboard & SATUSEHAT Observability Hub
│   ├── src/
│   │   ├── backend/          # REST API FastAPI + MCP Router
│   │   └── ml/               # Pipa MHGSL GNN, Late Fusion, & Evaluasi
│   ├── deploy/               # Helm charts & Argo workflows
│   └── docker-compose.observability.yml # Prometheus, OTEL Collector, Grafana
├── colab/                    # Jupyter Notebook & payload simulasi 300 data
├── Notion-docs/              # Skrip ekstraksi dataset riset & katalog klaim
└── dokumen/                  # Proposal resmi & generator naskah Healthkathon
```

---

## 3. Prasyarat Sistem

- **Node.js**: v20.x atau v22.x
- **Python**: v3.10 atau v3.11
- **Docker & Docker Compose** (opsional untuk observabilitas)
- **Git**

---

## 4. Cara Menjalankan Aplikasi

### A. Frontend Workstation (SvelteKit)
```bash
# Masuk ke direktori frontend
cd "Aegis-JKN app/frontend"

# Pasang dependensi
npm install

# Jalankan server pengembangan
npm run dev
```
Akses di peramban:
- **Landing Page**: `http://localhost:5173/`
- **Workstation Verifikator**: `http://localhost:5173/app`
- **IT Dashboard & SATUSEHAT**: `http://localhost:5173/it`

Untuk menjalankan pengujian unit frontend:
```bash
npm run test:unit
```

Untuk memvalidasi type safety dan build produksi:
```bash
npm run check
npm run build
```

---

### B. Backend REST API (FastAPI)
```bash
# Masuk ke direktori backend
cd "Aegis-JKN app/src/backend"

# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows (Git Bash):
source venv/Scripts/activate
# Windows (PowerShell/CMD):
venv\Scripts\activate

# Pasang dependensi backend
pip install -r requirements.txt

# Salin konfigurasi environment
cp .env.example .env

# Jalankan server API
uvicorn app.main:create_app --reload --port 8000
```
Dokumentasi interaktif Swagger API tersedia di `http://localhost:8000/docs`.

---

### C. Menjalankan Observability Stack (Prometheus & OpenTelemetry)
```bash
cd "Aegis-JKN app"
docker compose -f docker-compose.observability.yml up -d
```
- **Prometheus UI**: `http://localhost:9090`
- **OpenTelemetry Collector gRPC**: `localhost:4317`
- **OpenTelemetry Collector HTTP**: `localhost:4318`

---

## 5. Alur Penggunaan Workstation (/app)

1. **Antrean Klaim (Claim Queue)**:
   - Pilih berkas klaim dari daftar antrean kiri.
   - Gunakan filter risiko (*Fraud, High, Medium, Low*), filter kontradiksi, atau pencarian berdasarkan ID Klaim, Diagnosis ICD-10, maupun Nama Dokter/Faskes.
2. **Panel Bukti EMR & Narasi Pasien**:
   - Tinjau perbandingan klaim dokter vs wawancara pasien. Tag merah menandai kontradiksi klinis.
3. **Analisis AI MHGSL**:
   - Periksa pembagian bobot 3 kanal (Topologi, Fitur, Semantik).
   - Klik tab **Graf Relasi** untuk melihat visualisasi jaringan kolusi sindikat.
4. **Eksekusi Putusan Verifikator (HITL Action Bar)**:
   - Masukkan catatan verifikator pada kolom telaah.
   - Klik **Setujui Klaim**, **Klarifikasi RS**, atau **Eskalasi ke P2PK**.
   - Sistem otomatis menghitung ulang KPI nominal yang diamankan (*Prevented Fraud Cost*) dan mencatat entri ke rantai audit kriptografis.
