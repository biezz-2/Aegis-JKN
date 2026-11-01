# 20. Integritas Repositori, Artefak, dan Eksposur Secret

Status: Laporan audit internal
Tanggal audit: 22 Oktober 2026
Ruang lingkup: Integritas git, ketersediaan artefak yang disyaratkan spesifikasi Notion, dan paparan kredensial. Tidak mengulang analisis dokumen, definisi label, kualitas data, sitasi, regulatori, atau kualitas kode aplikasi yang ditangani auditor lain.

## 1. Ringkasan Eksekutif

Temuan utama: **struktur repo pada `N:\HEALTHKATHON` rusak secara organisatoris, tetapi tidak merusak apa pun yang sudah dipublikasikan.**

`N:\HEALTHKATHON` adalah working tree git yang tertinggal dan tidak sinkron dengan repo sebenarnya. Repo yang sesungguhnya adalah `N:\HEALTHKATHON\Aegis-JKN`, yang memiliki `.git` sendiri, remote yang sama, dan history lengkap. Empat commit setelah commit awal sudah dipush ke `origin/main`. Kerusakan yang terlihat pada `git status` root (122 file tracked ditandai terhapus) adalah artefak masalah direktori, bukan kehilangan kode.

Keputusan yang harus diambil: repo root `N:\HEALTHKATHON` seharusnya tidak lagi menjadi working tree git sama sekali. Direktori itu seharusnya menjadi workspace containing folder-folder proyek, bukan repo.

Peringatan kedua yang lebih serius untuk jadwal kompetisi: **hampir tidak ada artefak reproducibility yang ada di disk.** Tidak ada `data/`, tidak ada `configs/leakage.yaml`, tidak ada `tests/test_leakage.py`, tidak ada skrip generator, dan tidak ada manifest eksperimen. Yang tersedia hanyalah dump Notion yang diproses menjadi TypeScript. Padahal dashboard Notion §6 P0 mensyaratkan lampiran manifest eksperimen dan skrip untuk seluruh metrik yang dipublikasikan, dan §4 melarang metrik tersebut disebut tervalidasi.

Peringatan ketiga: ada **token Notion yang ter-hardcode di lima file skrip** pada `N:\HEALTHKATHON\Notion-docs\`. Token ini belum pernah masuk history git mana pun (sudah diverifikasi), jadi risikonya lokal, bukan publik. Namun token tersebut sudah terekspos dalam sesi ini dan harus dianggap bocor.

Peringatan keempat, dari konteks eksternal: **Healthkathon 2026 sedang berjalan.** Pendaftaran sudah ditutup, seleksi proposal sudah selesai, dan submit project akhir aktif 19 Oktober sampai 1 November 2026. Demo day atau Grand Final adalah 7 November 2026, 16 hari dari tanggal audit ini.

## 2. Struktur Git

### 2.1 Dua working tree, satu remote

| Aspek | `N:\HEALTHKATHON` (luar) | `N:\HEALTHKATHON\Aegis-JKN` (dalam) |
|---|---|---|
| `.git` ada | Ya | Ya |
| Remote `origin` | `github.com/biezz-2/Aegis-JKN.git` | `github.com/bpjs-.../Aegis-JKN.git` (identik) |
| Branch aktif | `main` | `main` |
| Jumlah file tracked | 122 | 133 |
| HEAD | `f62b86d` | `232ce79` |
| Selisih vs `origin/main` | 4 commit di belakang | 0, sinkron |
| `git status` | 122 terhapus, 10 untracked | 1 untracked (`AGENTS.md`) |

Keduanya menunjuk remote yang sama. `f62b86d` ("feat: initial production release") adalah ancestor dari HEAD repo dalam, sehingga **tidak ada history yang hilang**. Repo dalam bukan clone terpisah, melainkan kelanjutan yang benar.

### 2.2 Pemetaan path tracked ke lokasi nyata

Semua 122 path yang tercatat di HEAD repo luar ditemukan utuh di `Aegis-JKN/`. Verifikasi dilakukan per-path (`git ls-files` terhadap keberadaan disk) dengan hasil 122 dari 122 ada.

| Path tracked di HEAD | Lokasi nyata | Status |
|---|---|---|
| `package.json`, `next.config.ts`, `tsconfig.json`, `tailwind.config.ts`, `postcss.config.mjs`, `eslint.config.mjs`, `components.json`, `bun.lock` | `Aegis-JKN/` | Ada, tidak berubah |
| `src/**` (86 file: app, components/mhgsl, components/ui, hooks, lib, types) | `Aegis-JKN/src/` | Ada |
| `docs/**` (5 file) | `Aegis-JKN/docs/` | Ada |
| `prisma/schema.prisma` | `Aegis-JKN/prisma/` | Ada |
| `public/`, `download/`, `examples/`, `tests/`, `wiki/` | `Aegis-JKN/` | Ada |
| `.env.example`, `.gitignore`, `Caddyfile.txt`, `README.md`, `vercel.json`, `worklog.md` | `Aegis-JKN/` | Ada |

`.gitignore` **ada** di `Aegis-JKN/.gitignore` (509 byte) dan sudah mengecualikan `node_modules/`, `.next/`, `.env*.local`, `db/*.db`. Yang hilang di root adalah `.gitignore` dan `.env.example` root, karena keduanya pindah bersama isi repo.

### 2.3 Direktori yang tidak terkait

`N:\HEALTHKATHON\Aegis-JKN app\Dataset\` **tidak kosong** (9,1 GB). Isinya adalah data sampel resmi BPJS Kesehatan yang diunduh dari portal Data Sampel, bukan artefak proyek:

| Subdirektori | Ukuran | Isi |
|---|---|---|
| `Dataset/Data Sampel 2015-2020/` | 5,2 GB | Data Sampel Reguler dan Kontekstual DM 2015-2020, file `.dta` Stata, plus `Buku Data Sampel 2015-2020 (1).pdf` |
| `Dataset/Data sampel 2015-2024/2025/` | 4,0 GB | Edisi 2025: Reguler, Kontekstual COVID, DM, KIA (Ibu dan Anak), Kesehatan Mental, TB, dengan `.dta` dan `.xlsx` kode ICD-10 |

Ini satu-satunya sumber data **non-sintetis** di seluruh workspace, dan `analysis/corpus/07-dataset-v2-catalog.md` sudah mendokumentasikan skema `DM_kepesertaan.dta` (143.496 baris, 18 variabel) serta mencatat bahwa berkas itu memuat nomor peserta dan tanggal lahir. Jadi data sensitif ber-PII nyata ada di disk.

Status git: `Aegis-JKN app/` untracked di repo root, dan **tidak ada `.gitignore` di root `N:\HEALTHKATHON`** (semuanya dihapus dari worktree, lihat 2.2). Konsekuensinya `git add -A` di root akan mencoba menambahkan 9,1 GB data mentah Bernoulli patients. Lihat P0-5.

Sisanya, seluruhnya untracked di kedua repo dan tidak memengaruhi build:

| Direktori | Isi | Relevansi |
|---|---|---|
| `Aegis-JKN/` | Repo aplikasi aktif, 133 file tracked plus `node_modules` | **Ini repo aplikasi sebenarnya** |
| `mechine-learning-deep-learning/` | Repo git ketiga, 45 file tracked: dataset v2.1, pipeline Python, notebook eksperimen | **Ini repo eksperimen sebenarnya** |
| `Notion-docs/` | 7,2 MB: skrip fetch, dump JSON mentah, dump .md turunan | Alat dan arsip data, memuat token |
| `analysis/` | 12 MB: corpus dump (19 file) + reports (laporan audit) | Hasil kerja audit sesi ini |
| `colab/`, `dokumen/` | Output Colab (notebook 703,9 KB, PDF 17 halaman) dan proposal DOCX stored | Materi presentasi |
| `oasis/`, `REA CODING/`, `log/` | Proyek dan catatan lain | Tidak terkait |
| `commit_message.txt`, `COLAB_SSH_SETUP.md` | File lepas di root | Sampah repo |

### 2.4 Dampak praktis

- `git commit -a` di `N:\HEALTHKATHON` akan **menghapus 122 file dari history repo**. Ini destruktif dan harus dicegah.
- Build dan deploy dari root repo gagal: `package.json` root tidak ada, dan `vercel.json` yang ada di `Aegis-JKN/vercel.json` hanya berisi `{"$schema": ..., "framework": "nextjs"}`, tanpa path output custom, sehingga Vercel akan autodeteksi dari root project saat deploy diarahkan ke `Aegis-JKN/`.
- `prisma/schema.prisma` masih berupa template boilerplate Prisma (`User` dan `Post`, dua model generik), bukan skema domain JKN. Tidak ada model klaim, peserta, fasilitas, atau audit. Artinya **belum ada persistence domain di Prisma**, dan `.env.example` menunjuk `DATABASE_URL="file:./db/custom.db"` tanpa model yang memakainya.

## 3. Ketersediaan Artefak yang Disyaratkan Notion

Spesifikasi dataset simulasi v2.1 dan protokol training pada halaman Notion `10-simulation-dataset` dan `08-training-protocol` merujuk artefak berikut. Pemeriksaan di `Aegis-JKN/` (di luar `node_modules`) **dan** di repo eksperimen `mechine-learning-deep-learning/`:

| Artefak yang disyaratkan | Status | Lokasi aktual | Dampak |
|---|---|---|---|
| `claims_300_v2.1.csv` | **Ada** | `mechine-learning-deep-learning/datasets/claims_300_v2.1.csv` (242,3 KB, 300 baris, 31 kolom, tracked) | Protokol training v2.1 punya sumber data |
| `configs/leakage.yaml` | **Tidak ada** | Tidak ada di kedua repo | Blokir anti-leakage hanya naratif di dokumen; kode memakai konstanta Python, bukan YAML |
| `tests/test_leakage.py` | **Tidak ada** | `Aegis-JKN/tests/` hanya 3 skrip `.sh`; repo ML punya `backend/src/test_self_check.py` (65 baris) | Aturan anti-leakage tidak diuji |
| Skrip generator klaim | **Tidak ada** | Tidak ada di kedua repo | 300 baris ada sebagai CSV, tapi cara pembangkitan deterministiknya belum terdokumentasi |
| Manifest eksperimen / run metrics | **Tidak ada** | Repo ML tracked 45 file, tidak satu pun bernama manifest/checksum/metrics | Melanggar dashboard §6 P0 dan §7 aturan 6 |
| Pipeline Python (fetch + feature engineering) | **Ada** | `backend/src/data/pipeline.py` (352 baris), `notion_client.py` (93 baris) | Ada implementasi, dengan `LEAKAGE_COLUMNS` dan `seed 20260707` |
| Implementasi model MHGSL | **Ada** | `backend/src/models/mhgsl.py` (382 baris), checkpoint `backend/models/mhgsl_model.pth` (161 KB) | Arsitektur 3 kanal terimplementasi |
| Notebook eksperimen | **Ada** | `notebooks/Aegis-JKN.ipynb` (22 sel) berisi GroupKFold(5), LOGO, XGBoost, MLP, GCN, SHAP | Eksperimen ada, tapi **0 stored output**, jadi angkanya belum terekam |
| `src/data/notion-datasets.ts` | **Ada** | 451,6 KB | Dump Notion yang diproses menjadi modul TS |
| `src/types/dataset.ts` | **Ada** | `ClaimRecord` 26 field | Kontrak tipe data klaim |
| `docs/**` (5 file), `wiki/**` (19 file) | **Ada** | `Aegis-JKN/` | Sesuai klaim dashboard |

Tiga repo git, bukan satu:

| Repo | Remote | Tracked | Peran |
|---|---|---|---|
| `N:\HEALTHKATHON` | `biezz-2/Aegis-JKN.git` | 122 | Working tree usang, tertinggal 4 commit |
| `N:\HEALTHKATHON\Aegis-JKN` | `biezz-2/Aegis-JKN.git` | 133 | Repo aplikasi Next.js, sinkron dengan origin |
| `N:\HEALTHKATHON\mechine-learning-deep-learning` | `biezz-2/Aegis-JKN-mechine-learning-deep-learning.git` | 45 | Repo eksperimen ML, dataset v2.1, notebook, OASIS |

Pemisahan ini sendiri merupakan temuan: **tidak ada satu pun artefak eksperimen yang terhubung ke repo aplikasi**, sehingga aplikasi tidak dapat menyertakan bukti performa yang bisa direplikasi sesuai dashboard §7 aturan 6.

Bentuk data yang paling ephemeral ada di `src/data/notion-datasets.ts`: array TypeScript yang di-hardcode. Tidak ada pipeline yang menghasilkannya, tidak ada checksum, tidak ada seed, dan tidak ada jejak versi. Beberapa entri di dalamnya bahkan **membocorkan ID halaman Notion mentah** (misalnya `3f23e603-1ab7-8111-8173-e20f75996fcb`) yang tidak ada gunanya bagi pengguna akhir dan seharusnya tidak masuk bundle klien.

Catatan: `src/types/dataset.ts` mendefinisikan `ClaimRecord` dengan 26 field yang **tidak sama persis** dengan 24 properti pada kamus data Notion §5, dan menambah `layanan`, `rujukan`, `alasanBerobat` yang tidak ada di kamus, serta `kontradiksiNarasi` yang ada di kamus. Kontrak tipe dan kamus data perlu direkonsiliasi.

## 4. Eksposur Secret dan Kredensial

### 4.1 Temuan

| Path | Baris | Jenis | Nilai | Risiko |
|---|---|---|---|---|
| `Notion-docs/fetch_notion_page.py` | 4 | Token Notion | `ntn_1674...` [REDACTED] | Tinggi |
| `Notion-docs/fetch_notion_content.py` | 4 | Token Notion | `ntn_1674...` [REDACTED] | Tinggi |
| `Notion-docs/fetch_notion_databases.py` | 4 | Token Notion | `ntn_1674...` [REDACTED] | Tinggi |
| `Notion-docs/fetch_notion_blocks.py` | 4 | Token Notion | `ntn_1674...` [REDACTED] | Tinggi |
| `Notion-docs/test_notion.py` | 3 | Token Notion | `ntn_1674...` [REDACTED] | Tinggi |

Satu token yang sama, di-hardcode sebagai literal di lima file terpisah, di baris 3 atau 4 tiap file.

### 4.2 Mitigasi yang sudah ada

- `Notion-docs/` **tidak tracked** oleh repo luar maupun repo dalam (`git ls-files | grep notion-docs` = 0 di keduanya).
- Token **tidak pernah masuk history git**: `git log --all -S "ntn_1674"` mengembalikan kosong untuk kedua repo, termasuk `--all` yang mencakup seluruh branch dan ref.
- Semua repo remote sudah sinkron dengan HEAD (`rev-list --count origin/main..HEAD` = 0 di repo dalam), sehingga tidak ada draft commit lokal yang mengandung token.

Artinya kebocoran ini bersifat lokal dan belum masuk ke publik. Yang perlu dilakukan adalah rotasi, bukan membersihkan history.

### 4.3 Rekomendasi

1. **Rotasi token Notion sekarang** di Integrations Notion, lalu ganti literal di lima file itu dengan pembacaan `os.environ["NOTION_TOKEN"]`. Skrip `fetch_corpus.py` dan `fetch_dbs.py` di direktori yang sama sudah memakai pola environment variable, jadi pola yang benar sudah ada di repo.
2. Tambahkan `Notion-docs/` dan `analysis/` ke `.gitignore` repo dalam, atau pindahkan keduanya ke luar working tree, agar tidak ikut ter-commit saat commit berikutnya.
3. Pattern scan untuk `ntn_`, `sk-`, `ghp_`, `AKIA`, `AIza`, `xox?-` dijalankan pada `Aegis-JKN/src` dan `Aegis-JKN/docs`: **bersih, nol temuan**.

### 4.4 Catatan sensitivitas data

`Notion-docs/` (7,2 MB) dan `analysis/corpus/` (12 MB) berisi dump mentah klaim sintetis, termasuk entitas sintetis (pasien, dokter, faskes) dan metadata `_notion_page_id` serta `_last_edited` yang tidak ada gunanya di luar jejak audit. Karena statusnya "sintetis untuk demonstrasi", risiko privasi aktual rendah, tetapi jejak entitas sintetis yang tidak dianonimkan tetap sebaiknya tidak ikut ke arsip yang dibagikan luas.

## 5. Status Kompetisi Healthkathon 2026 per 22 Oktober 2026

Ditemukan di luar corpus Notion, dari API resmi situs kompetisi (`POST https://healthkathon.bpjs-kesehatan.go.id:8080/healthkathon/rest/referensi/siklus/list`):

| Kode | Tahap | Mulai | Selesai | Aktif |
|---|---|---|---|---|
| 1 | Pendaftaran | 14 Agu 2026 | 11 Okt 2026 | 0 |
| 2 | Submit Proposal | 14 Agu 2026 | 11 Okt 2026 | 0 |
| 3 | Seleksi Proposal | 12 Okt 2026 | 18 Okt 2026 | 0 |
| 4 | Submit project akhir | 19 Okt 2026 | 1 Nov 2026 | **1** |
| 5 | Seleksi project akhir | 2 Nov 2026 | 4 Nov 2026 | 0 |
| 6 | Coaching dan Development | 19 Okt 2026 | 30 Okt 2026 | **1** |
| 7 | Demo day / Grand Final | 7 Nov 2026 | - | 0 |
| 8 | Pengumuman Pemenang | - | - | 0 |

Pendaftaran diperpanjang sampai 11 Oktober (bukan 14 September seperti tertulis pada baris registrasi di database Notion). Jumlah peserta terdaftar: **872 tim**.

Implikasi terhadap audit ini: tenggat yang mengikat adalah **1 November 2026** untuk submit project akhir, bukan tanggal pendaftaran. Arti Bagian 3 di atas berpindah dari "catatan teknis" menjadi "penghalang deliverable". Dashboard Notion §4 menyatakan bahwa accuracy 93,0%, precision 94,12%, ROC-AUC 0,9825, AUPRC 0,9142, ketahanan masking 89,4%, FPR 10,6%, penurunan waktu telaah 45%, throughput 3,2 kali, SUS 82,5, serta penghematan finansial belum boleh disebut hasil tervalidasi. Tidak satu pun artefak manifest eksperimen dan skrip hitung yang ada di disk. **Angka-angka itu tidak boleh ditampilkan sebagai hasil di Grand Final 7 November** tanpa artefak replikasi, karena itu melanggar aturan sendiri proyek pada dashboard §7 aturan 6.

## 6. Peringkat Temuan

### P0 (menghambat kerja, build, atau reproduksi)

| ID | Temuan | Bukti |
|---|---|---|
| P0-1 | Repo root `N:\HEALTHKATHON` adalah working tree usang; `git commit -a` di sana akan menghapus 122 file dari history | `git status` = 122 ` D`; repo dalam sudah push 4 commit ke `origin/main` |
| P0-2 | Tidak ada satu pun artefak reproducibility: `data/`, `configs/leakage.yaml`, `tests/test_leakage.py`, skrip generator, manifest eksperimen | Pemeriksaan `Aegis-JKN/` (tanpa `node_modules`): 0 dari 6 artefak ada |
| P0-3 | Metrik yang dipublikasikan dashboard tidak memiliki artefak replikasi, sementara Grand Final 16 hari lagi | Dashboard §4 versus temuan P0-2 |
| P0-4 | `prisma/schema.prisma` masih template boilerplate (`User`, `Post`), tidak ada model domain JKN | `cat Aegis-JKN/prisma/schema.prisma` |
| P0-5 | Data sampel resmi BPJS dengan PII (9,1 GB) berada di workspace tanpa `.gitignore` root; satu `git add -A` di root akan menahannya | `du -sh Aegis-JKN app/Dataset` = 9,1 G; `git status` root tidak punya `.gitignore` |

### P1 (risiko keamanan, artefak hilang yang menghambat output)

| ID | Temuan | Bukti |
|---|---|---|
| P1-1 | Token Notion ter-hardcode di 5 file; sudah terekspos di luar repo, harus dirotasi | `Notion-docs/*.py` baris 3 atau 4 |
| P1-2 | 300 baris klaim sintetis tidak dapat direproduksi; sumber tunggal adalah dump Notion yang diproses | Tidak ada skrip generator |
| P1-3 | Baris research Notion mencantumkan tenggat pendaftaran yang salah (14 Sep vs 11 Okt) | `dataset_research_live.csv` versus API `referensi/siklus/list` |
| P1-4 | `src/data/notion-datasets.ts` membocorkan ID halaman Notion mentah ke bundle klien | Entri `"id": "3f23e603-1ab7-..."` |
| P1-5 | `src/types/dataset.ts` (26 field) tidak sama dengan kamus data Notion §5 (24 properti) | Perbandingan kedua berkas |
| P1-6 | Data sampel resmi BPJS 9,1 GB ada di `Aegis-JKN app/Dataset/` tanpa `.gitignore` root; `git add -A` akan mencicipkannya | `du -sh` 5,2 G + 4,0 G; tidak ada `.gitignore` di root |

### P2 (hygiene)

| ID | Temuan |
|---|---|
| P2-1 | 8 direktori dan 2 file lepas di root repo tidak terkait dan tidak ter-track |
| P2-2 | `Notion-docs/` (7,2 MB) dan `analysis/` (12 MB) tidak ada di `.gitignore` |
| P2-3 | Tidak ada `AGENTS.md` yang ter-commit (masih untracked di repo dalam) |
| P2-4 | `commit_message.txt` dan `COLAB_SSH_SETUP.md` di root repo |

## 7. Rekomendasi perbaikan

### 7.1 Memperbaiki struktur git (P0-1)

Jangan jalankan `git rm` pada 122 file. Yang benar adalah menjadikan `N:\HEALTHKATHON` bukan repo sama sekali, karena repo yang sudah benar ada di `Aegis-JKN/`:

```
cd N:\HEALTHKATHON
mv .git .git-stale-root-20261022
```

Setelah itu, `N:\HEALTHKATHON` menjadi workspace biasa yang berisi `Aegis-JKN/` (repo aplikasi), `Notion-docs/`, `analysis/`, dan material lain. `Aegis-JKN/.git` tetap menjadi satu-satunya repo dan tetap terhubung ke `origin`.

Alternatif yang lebih konservatif bila tetap ingin mempertahankan root sebagai repo: `git -C N:\HEALTHKATHON rm -r --cached .` lalu `git mv` tiap path. Ini menghasilkan diff rename 122 file dan mempertahankan history, tetapi tidak menambah manfaat karena repo dalam sudah punya history penuh.

Perlu dicatat: `.git-stale-root-20261022` masih menyimpan working tree lama dan sebaiknya dihapus setelah memastikan tidak ada yang dibutuhkan darinya.

### 7.2 Rotasi secret (P1-1)

1. Integrations Notion: buat token baru, revoke yang lama.
2. Kelima file di `Notion-docs/` ganti literal `token = "ntn_..."` menjadi `token = os.environ["NOTION_TOKEN"]` plus `import os`. `fetch_corpus.py` dan `fetch_dbs.py` sudah memakai pola ini.
3. Tambahkan `Notion-docs/`, `analysis/` ke `.gitignore` repo dalam.

### 7.3 Menutup celah reproducibility (P0-2, P0-3)

Prioritas dengan tenggat 1 November 2026:

1. `data/claims_300_v2.1.csv` beserta `data/CHECKSUMS.txt` (sha256) dan `data/seed.txt`.
2. `configs/leakage.yaml` yang mengimplementasikan blokir 8 kolom dashboard §7, plus `tests/test_leakage.py` yang memverifikasi tidak ada kolom terlarang pada matriks fitur.
3. `experiments/<id>/manifest.json` per metrik yang dipublikasikan, memuat seed, split ID, versi kode, dan skrip hitung. Ini yang diminta dashboard §6 P0.
4. Script yang bisa dijalankan ulang dari CSV ke angka metrik, sehingga klaim "replikasi" dapat dibuktikan onstage.

Tanpa butir 1 dan 3, dashboard §4 tetap benar: angka-angka tersebut bukan hasil tervalidasi, dan presentasi 7 November harus menyajikannya sebagai eksplorasi pada data sintetis, bukan performa terukur.

### 7.5 Melindungi data sampel resmi (P0-5)

Segera setelah root repo dinonaktifkan (7.1), pastikan `Aegis-JKN app/Dataset/` tidak pernah masuk git. Dua lapis pertahanan:

```
# N:\HEALTHKATHON\.gitignore  (buat baru di root workspace)
Aegis-JKN app/Dataset/
*.dta
*.sav
```

Bila data sampel ini akan dipakai untuk eksperimen, terapkan UU PDP 27/2022 lebih dulu: data `DM_kepesertaan.dta` memuat nomor peserta dan tanggal lahir, sehingga harus diproses di lingkungan terkendali, tidak disalin ke repo, tidak diunggah ke layanan pihak ketiga, dan keluarannya harus dianonimkan sebelum dipakai di demo. Jangan pernah menghubungkan data nyata yang membawa PII ke aplikasi demo yang saat ini tidak punya autentikasi maupun audit log.

### 7.4 Hygiene

- `src/types/dataset.ts` direkonsiliasi dengan kamus data Notion §5: samakan jumlah dan nama field, dan putuskan secara eksplisit apakah `layanan`, `rujukan`, `alasanBerobat` adalah tambahan yang sah.
- `notionId` pada `ClaimRecord` dan `id` pada `ResearchRecord` dihapus dari bundle klien, atau dipetakan ke ID stabil non-Notion.
- `prisma/schema.prisma` diisi model domain, atau dihapus bila persistence memang di luar lingkup MVP.

## 8. Metode dan Batasan

Perintah yang dijalankan: `git rev-parse`, `git log`, `git ls-files`, `git ls-tree`, `git status`, `git branch`, `git remote -v`, `git merge-base --is-ancestor`, `git rev-list --count`, `git log -S` (riwayat secret), `git log --all -S` untuk token; `ls`, `find`, `du` untuk inventaris direktori; `grep` untuk pattern secret; `cat` untuk `.gitignore`, `.env.example`, `vercel.json`, `prisma/schema.prisma`, `src/types/dataset.ts`.

Operasi git yang mengubah state tidak dijalankan. Build dan typecheck tidak dijalankan ulang karena auditor lain sudahploratory UoPadanya.

Batasan yang perlu dicatat: `node_modules` dikecualikan dari inventaris. Direktori `Aegis-JKN app/Dataset/` berisi data sampel resmi BPJS 9,1 GB (termasuk `DM_kepesertaan.dta` yang memuat nomor peserta dan tanggal lahir) dan tidak boleh masuk git; data ini di luar cakupan audit kode dan tidak dianalisis isinya. Token Notion yang tertera di sini sengaja dipotong empat karakter dan tidak pernah ditulis lengkap ke mana pun di repositori ini.
