# Aegis-JKN · Unified Fraud Intelligence Platform

Platform deteksi kecurangan (*fraud*) klaim BPJS Kesehatan berbasis **Multi-Channel Heterogeneous Graph Structure Learning (MHGSL)**, integrasi simulasi multi-agen **Oasis (mistral-oasis:24b)**, serta audit kriptografis **Merkle Tree**.

---

## 📁 Struktur Direktori Platform

```
Aegis-JKN app/
├── frontend/                     # Frontend Modern Svelte 5 + SvelteKit + Tailwind CSS v4
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/       # Komponen visual (Graf SVG 3 Kanal, Simulasi, Formulasi, dll.)
│   │   │   ├── data/             # Dataset 300 klaim, 33 riset Notion, hasil simulasi Oasis
│   │   │   ├── stores/           # Svelte 5 runes store (i18n bilingual ID/EN, Dark/Light Theme)
│   │   │   └── types.ts          # Kontrak tipe data TypeScript
│   │   └── routes/
│   │       ├── +page.svelte      # Beranda & Showcase MHGSL
│   │       ├── simulasi/         # Dashboard Simulasi Interaksi Agen Teks Oasis (300 Langkah)
│   │       ├── dataset/          # Katalog & Filter 300 Berkas Klaim Notion (Rp 3,53 Miliar)
│   │       └── audit/            # Visualisasi Pohon Kriptografis Merkle Tree & Audit Log
│   ├── package.json
│   └── vite.config.ts
│
├── src/
│   ├── backend/                  # Backend REST API berbasis FastAPI
│   │   ├── app/
│   │   │   ├── api/              # Routers (graph, simulation, report, metrics, auth)
│   │   │   ├── core/             # Konfigurasi, database, mTLS, RBAC, dan audit
│   │   │   └── services/         # Integrasi ML service, graph schema, Qdrant vector DB
│   │   └── requirements.txt
│   │
│   └── ml/                       # Pipa Model MHGSL & Algoritma Machine Learning
│       ├── mhgsl/                # Kanal Topologi, Fitur (Cosine Sim), dan Semantik (BioBERT)
│       ├── synth/                # Generator data sintetis berbasis privasi diferensial
│       ├── evaluation/           # Benchmark metrik AUPRC, Recall, Precision, Robustness
│       └── xai/                  # Atribusi Explainable AI berbasis SHAP Waterfall
│
├── Dataset/                      # Berkas data referensi & pemetaan FHIR R4
├── deploy/                       # Konfigurasi orkestrasi Docker & OpenTelemetry
├── migrations/                   # Skema database & migrasi Alembic
└── tests/                        # Pengujian E2E & unit testing
```

---

## 🚀 Panduan Memulai Cepat (Quickstart)

### 1. Menjalankan Frontend SvelteKit
```bash
cd frontend
npm install
npm run dev
```
Buka peramban di `http://localhost:5173`.

### 2. Memeriksa Type Safety Frontend
```bash
cd frontend
npm run check
```

### 3. Membangun Versi Produksi Frontend
```bash
cd frontend
npm run build
```

### 4. Menjalankan Backend FastAPI
```bash
cd src/backend
uvicorn app.main:create_app --reload --port 8000
```
Dokumentasi Swagger API interaktif tersedia di `http://localhost:8000/docs`.
