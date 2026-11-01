# Audit Kepatuhan Regulasi - Aegis-JKN (JKN Fraud Detection)

**Tanggal audit:** 22 Oktober 2026
**Auditor:** Kanal kepatuhan regulasi Indonesia (compliance analyst)
**Lingkup:** `N:\HEALTHKATHON\analysis\corpus\` (15 dokumen markdown + 4 berkas data)
**Tanggal akses seluruh URL:** 22 Oktober 2026
**Metode:** verifikasi primer terhadap JDIH BPK (`peraturan.bpk.go.id`), PDF JDIH Kemenkes (`jdih.kemenkes.go.id`), WHO ICD-10 Browser (`icd.who.int`), CDC ICD-9-CM, dan dokumen SATUSEHAT. Pencarian internet dilakukan melalui MCP SearXNG (primary `http://localhost:8088`, failover `http://192.168.101.19:8089`).

> **Catatan metodologis.** Laporan ini **hanya melaporkan MASALAH**. Regulasi yang disebut dengan benar dan isi yang sesuai tidak diberi temuan. Setiap baris tabel memuat URL sumber dan tanggal akses. Hal yang tidak dapat diverifikasi ditandai **TIDAK TERVERIFIKASI** - tidak ditebak.
>
> **Dua butir dalam mandat tugas tidak berlaku bagi korpus ini**, dan dicatat agar tidak disalahartikan sebagai temuan yang terlewat:
> 1. **Premis "decentralization"/desentralisasi** - `grep -rni "desentralis"` atas seluruh korpus mengembalikan **0 hasil**. Tidak ada klaim desentralisasi yang perlu diuji.
> 2. **Klaim "INSURANCE/BPJS codes"** - `grep -rniE "kode BPJS|kode insurance|insurance code"` atas seluruh korpus mengembalikan **0 hasil**. Tidak ada kode BPJS yang diklaim. Acuan tarif terdekat adalah Permenkes 26/2021 (INA-CBG, 1.075 grup kasus) + Permenkes 3/2023 (Standar Tarif), yang keduanya **tidak** dicantumkan dalam daftar referensi proposal.

---

## 1. Ringkasan Eksekutif

### 1.1 Gambaran umum

Seluruh korpus menyebut **hanya 7 rujukan regulasi yang berbeda** (lihat §2). Angka dan nomor pada 5 dari 7 rujukan **benar** secara formal (nomor, tahun, dan judul sesuai JDIH BPK). Namun **4 dari 7 salah pada isi**, dan **9 dari 7 rujukan** - jika dihitung per-*kutipan* - gagal. Kesalahan yang paling berbahaya bukan salah nomor, melainkan **menyebut regulasi yang benar dengan isi yang salah**, karena itu memberi impresi kekompakan hukum yang tidak ada.

Dua pola berulang:

1. **Substitusi isiacross dokumen arsip.** `12-archive-architecture.md` dan `11-archive-proposal.md` adalah draf yang lebih lama dan lebih agresif. Keduanya menyebut Permenkes 16/2019 dengan akhiran "**serta Pengendalian Gratifikasi**" - frasa yang **tidak ada dalam judul resmi** regulasi tersebut. Dalam draf arsip, "gratifikasi" disisipkan tepat setelah "Kecurangan (Fraud)", seolah-olah itu bagian dari nama resmi. Effectifnya, referensi hukum proposal yang terlihat paling "padat" justru keliru secara harfiah.

2. **Klaim privasi yang bertentangan dengan dokumen sendiri.** `10-simulation-dataset.md:3` menyatakan dataset sintetis "aman menurut Permenkes 24/2022 & UU PDP No. 27/2022" - frasa ini diulang di `09-draft-hub.md:6,218` dan `14-index.md:49,261`. Pernyataan ini **bertentangan langsung** dengan `02-architecture.md:63` ("Pseudonimisasi tidak dianggap sebagai anonimisasi sempurna") dan `02-architecture.md:94` ("Hindari menjadikan hash biasa sebagai pengganti kontrol privasi"), serta dengan `11-archive-proposal.md:146` yang mengklaim "de-identifikasi penuh data medis" menggunakan salted SHA-256.

### 1.2 Tabel severity

| # | Temuan | Severity | Lokasi utama | Dampak |
|---|---|---|---|---|
| **C-01** | Judul resmi Permenkes 16/2019 disalahkan dengan "serta Pengendalian Gratifikasi" | **Tinggi** | `01-proposal.md:88`, `04-evidence-matrix.md:44`, `11-archive-proposal.md:131,414`, `14-index.md:606,889` | Dokumen inti proposal (bukan arsip saja) mencantumkan judul regulasi yang tidak pernah ada |
| **C-02** | Permenkes 24/2022 dinyatakan sebagai dasar HL7 FHIR R4 - padahal naskah itu 0 kali menyebut HL7/FHIR/SATUSEHAT | **Tinggi** | `12-archive-architecture.md:69`, `dataset_research_live.json` item 12 (Status "Terverifikasi") | Dasar hukum integrasi salah total; continue mark "Terverifikasi" menipu |
| **C-03** | Klaim privasi "aman menurut Permenkes 24/2022 & UU PDP" | **Tinggi** | `10-simulation-dataset.md:3`, `09-draft-hub.md:6,218`, `14-index.md:49,261` | Kontradiksi internal dengan `02-architecture.md:63,94`; data sintetis sebenarnya memuat PII-kuasi |
| **C-04** | Sanksi pidana UU PDP disematkan ke Pasal 65 & 66 (yang sebenarnya adalah Pasal 67 & 68); "3x24 jam" disematkan ke Pasal 4 ayat (2) (yang sebenarnya Pasal 46 ayat (1)) | **Tinggi** | `12-archive-architecture.md:91`, `dataset_research_live.csv:5` (Catatan) | Pasal yang dikutip adalah pasal larangan, bukan pasal pidana |
| **C-05** | "Data Pribadi Spesifik" disematkan ke Pasal 4 ayat (3) (yang sebenarnya ayat (2)) | **Tinggi** | `11-archive-proposal.md:245` | Salah kutipan pasal inti UU PDP di BAB V proposal |
| **C-06** | Kode ICD-9-CM `00.66` dilabeli "Angioplasty koroner + stent (PCI)" | **Sedang** | `09-draft-hub.md:81`, `10-simulation-dataset.md:78` | 00.66 = PTCA **tanpa** stent; stent = 36.06/36.07. Salah label pada klaim yang jadi contoh upcoding |
| **C-07** | Kode ICD-9-CM `93.90` dilabeli "Terapi oksigen tekanan positif" | **Sedang** | `09-draft-hub.md:89`, `10-simulation-dataset.md:86` | 93.90 = *non-invasive mechanical ventilation*; IPPB = 93.91 |
| **C-08** | FORNAS: insulin glargine 100 IU/mL ditandai "**Tidak**" (tidak ada di FORNAS) | **Sedang** | `09-draft-hub.md:101`, `10-simulation-dataset.md:98` | **Salah faktual** - glargine tercantum di Kepmenkes 1199/2025 §16.2.2 |
| **C-09** | Angka "Biaya Rujukan" (Rp58 jt, Rp78 jt, dst.) tanpa acuan tarif/jenis kasus INA-CBG | **Sedang** | `09-draft-hub.md:80-90`, `10-simulation-dataset.md:77-87` | Angka tidak dapat ditelusuri ke grup kasus INA-CBG mana pun |
| **C-10** | Klaim "kepatuhan absolut" + "de-identifikasi penuh data medis" dengan salted SHA-256 | **Sedang** | `11-archive-proposal.md:146,185,197` | Overclaim; salted SHA-256 adalah pseudonymization, bukan anonymization |
| **C-11** | PP 33/2026 (aturan pelaksanaan UU PDP) **tidak dicantumkan** di mana pun | **Sedang** | `01-proposal.md:85-91`, `04-evidence-matrix.md:42-46` | Proposal shackuhypothetical tidak menyebut aturan executing yang baru berlaku 16 Jan 2027 |
| **C-12** | Permenkes 6/2026 (Rumah Sakit), Kepmenkes 1199/2025 (FORNAS baru), Permenkes 18/2022 (Satu Data Kesehatan), Permenkes 3/2023 (Standar Tarif), UU 40/2004 (SJSN), UU 13/2022, Perpres 82/2018 s.d. 59/2024 tidak dicantumkan | **Sedang** | Tidak ada dasar hukum yang dicantumkan untuk ketentuan-ketentuan tersebut | Cakupan dasar hukum tidak lengkap |
| **C-13** | Klaim "Rp25 miliar, 3 rumah sakit swasta 2024" tidak dapat ditelusuri ke sumber primer | **Rendah** | `13-archive-deep-research.md:3` | Angka faktual tanpa sumber |
| **C-14** | Label deskripsi ICD-10 tidak presisi (K29.7, S72.0, J18.9, K35.8, K40.9, I21.9) | **Rendah** | `09-draft-hub.md:69-78`, `10-simulation-dataset.md:65-75` | Penyederhanaan koding; "~" atau "lainnya" hilang |

### 1.3 Rekapitulasi hitungan verifikasi

| Metrik | Jumlah |
|---|---|
| Nomor regulasi berbeda yang dirujuk di korpus | 7 |
| Nomor + tahun **benar** | 5 / 7 (UU 27/2022, UU 17/2023, Permenkes 24/2022, Permenkes 26/2021, Permenkes 3/2023, catatan: 3/2023 hanya muncul di daftar pustaka arsip) |
| Nomor + tahun **salah/tidak sesuai** | 1 / 7 (Permenkes 16/2019 - **nomor & tahun benar, judul salah**) |
| Rujukan **tanpa nomor** (gap dokumentasi) | 1 / 7 (`06-research-notes.md:61`) + tautan SATUSEHAT |
| Kutipan pasal UU PDP yang **salah ejaan** | 4 (Pasal 4(2)/(3), Pasal 65/66, Pasal 46) |
| Kode ICD-10 diperiksa | 10 → 6 tepat, 4 tidak presisi, 0 salah kode |
| Kode ICD-9-CM diperiksa | 10 → 7 tepat, 2 salah label, 0 salah kode |
| Item FORNAS diperiksa | 10 → 9 benar, 1 salah (insulin glargine) |
| Regulasi **TIDAK TERVERIFIKASI** | 4 (Permenkes 11/2017 status BPK; Permenkes 33/2024 identitas; UU/PP 13/2022 & 1/2026; peraturan pengganti INA-CBG → iDRG) |

---

## 2. TABEL VERIFIKASI - seluruh sebutan regulasi di korpus

Format: `Sebutan | Lokasi | Nomor resmi | Nomor benar? | Isi sesuai? | Verdict`
Sumber + tanggal akses untuk **setiap** baris diberikan pada baris masing-masing.

### 2.1 Sebutan pada dokumen inti (non-arsip)

| # | Sebutan | Lokasi | Nomor resmi | Nomor benar? | Isi sesuai? | Verdict |
|---|---|---|---|---|---|---|
| V-01 | "Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi" | `01-proposal.md:86`, `04-evidence-matrix.md:43` | **UU 27/2022** - "Pelindungan Data Pribadi", ditetapkan 17 Okt 2022, berlaku 17 Okt 2022, Status **Berlaku** | ✅ Ya | ✅ Ya | **✓ TEPAT.** Sumber: `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` (akses 22 Okt 2026) |
| V-02 | "Undang-Undang Republik Indonesia Nomor 17 Tahun 2023 tentang Kesehatan" | `01-proposal.md:87`, `04-evidence-matrix.md:44` | **UU 17/2023** - "Kesehatan", berlaku 8 Agt 2023, Status **Berlaku** | ✅ Ya | ✅ Ya | **✓ TEPAT.** Sumber: `https://peraturan.bpk.go.id/Details/258028/uu-no-17-tahun-2023` (akses 22 Okt 2026) |
| V-03 | "Permenkes RI Nomor 16 Tahun 2019 tentang Pencegahan dan Penanganan Kecurangan **serta Pengendalian Gratifikasi** dalam Program Jaminan Kesehatan" | `01-proposal.md:88`, `04-evidence-matrix.md:45` | **Permenkes 16/2019** - "tentang **Pencegahan dan Penanganan Kecurangan (Fraud) serta Pengenaan Sanksi Administrasi terhadap Kecurangan (Fraud) dalam Pelaksanaan Program Jaminan Kesehatan**", berlaku 31 Jul 2019, Status **Berlaku** | ✅ Nomor & tahun ya; ❌ **judul tidak sesuai** | ❌ **Tidak sesuai** | **✗ SALAH JUDUL.** Judul resmi memuat "Pengenaan Sanksi Administrasi", **bukan** "Peng|Gratifikasi". Frasa "Pengendalian Gratifikasi" tidak ada di naskah. Sumber: `https://peraturan.bpk.go.id/Details/129762/permenkes-no-16-tahun-2019` (akses 22 Okt 2026) |
| V-04 | "Permenkes RI Nomor 24 Tahun 2022 tentang Rekam Medis" | `01-proposal.md:89`, `04-evidence-matrix.md:46` | **Permenkes 24/2022** - "tentang Rekam Medis", berlaku 31 Agt 2022, Status **Berlaku** (mencabut Permenkes 269/Menkes/Per/III/2008) | ✅ Ya | ✅ Ya | **✓ TEPAT** sebagai rujukan umum. **Catatan:** istilah resmi "Rekam Medis"; rugbyursebutan "Rekam Medis Elektronik" (RME) yang ada di §2.4 adalah subdomain yang diatur Pasal 4, 10, 11, 21, 24 naskah yang sama. Sumber: `https://peraturan.bpk.go.id/Details/245544/permenkes-no-24-tahun-2022` (akses 22 Okt 2026) |
| V-05 | "Dokumentasi SATUSEHAT terkait interoperabilitas klaim BPJS" | `01-proposal.md:90`, `04-evidence-matrix.md:47`, `06-research-notes.md:60` | Bukan peraturan - dokumentasi teknis Kemenkes (SATUSEHAT Platform v7.23) | ✅ Ya (URL hidup, HTTP 200) | ⚠️ **Sebagian** | **⚠️ SEBAGIAN TEPAT.** Halaman memang memuat alur integrasi klaim BPJS berbasis FHIR resource (Account, ChargeItem, Coverage, Encounter, Condition, Procedure, Invoice, Claim, ClaimResponse). **Namun halaman tidak menyebut "HL7 FHIR R4" sebagai standar**, dan modul Claims sendiri dinyatakan "hanya tersedia di *Environment* Sandbox". Sumber: `https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/` (akses 22 Okt 2026) |
| V-06 | "Permenkes RI Nomor 24 Tahun 2022 tentang Rekam Medis Elektronik, pertukaran data medis nasional menggunakan **protokol HL7 FHIR R4**" | `12-archive-architecture.md:69` | **Permenkes 24/2022** | ✅ Ya | ❌ **TIDAK ADA DALAM NASKAH** | **✗ SALAH ISI.** Verifikasi menyeluruh atas naskah: **0 kemunculan "HL7", 0 "FHIR", 0 "SATUSEHAT"**. Pasal 10(4) justru **meng-delegasikan** penetration standar ke Kemenkes: *"Interoperabilitas sebagaimana dimaksud pada ayat (3) mengacu kepada standar sistem elektronik yang diselenggarakan oleh Kementerian Kesehatan sesuai dengan ketentuan peraturan perundang-undangan."* Sumber: `https://peraturan.bpk.go.id/Details/245544/permenkes-no-24-tahun-2022` + PDF `https://jdih.kemkes.go.id/dokumen/peraturan/permenkes_24_2022.pdf` (akses 22 Okt 2026) |
| V-07 | "Permenkes 24/2022 mewajibkan Rekam Medis Elektronik; interoperabilitas nasional via platform SATUSEHAT memakai standar HL7 FHIR R4" - **Status: "Terverifikasi"** | `dataset_research_live.json` item 12 / `dataset_research_live.csv:14` | **Permenkes 24/2022** | ✅ Ya | ❌ **Tidak sesuai** | **✗ SALAH.** Label "Terverifikasi" pada baris research database **mendistorsi** status verifikasi. Sumber: `https://peraturan.bpk.go.id/Details/245544/permenkes-no-24-tahun-2022` (akses 22 Okt 2026) |
| V-08 | "Pasal 4 ayat (3) UU PDP → Data Pribadi Spesifik" | `11-archive-proposal.md:245` | **UU 27/2022 Pasal 4** | ✅ Ya | ❌ **Ayat salah** | **✗ SALAH AYAT.**Ayat (2) = Data Pribadi yang bersifat spesifik (data dan informasi kesehatan, biometrik, genetika, catatancrimean, data anak, kerahasiaan pribadi). Ayat (3) = Data Pribadi yang bersifat **umum** (nama lengkap, jenis kelamin, agama, status perkawinan, "dan/atau Data Pribadi yang dikombinasikan untuk mengidentifikasi seseorang"). Sumber: `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` (akses 22 Okt 2026) |
| V-09 | "Sanksi pidana 5-6 tahun dan denda miliaran (**Pasal 65 & 66**)" | `12-archive-architecture.md:91`, `dataset_research_live.csv:5` (Catatan) | **UU 27/2022 Pasal 67 & 68** | ✅ Ya | ❌ **Pasal salah** | **✗ SALAH PASAL.** Pasal 65 = larangan memperoleh/mengumpulkan/mengoyers data pribadi milik orang lain; Pasal 66 = larangan membuat data pribadi palsu. Ketentuan **pidana** ada di **Pasal 67** (5/4/5 tahun + denda s.d. Rp5 M, Rp4 M, Rp5 M) dan **Pasal 68** (6 tahun + denda s.d. Rp6 M); Pasal 69 =-ftur pidana tambahan; Pasal 70 = sanksi korporasi (denda s.d. 10× maksimum). Sumber: `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` (akses 22 Okt 2026) |
| V-10 | "notifikasi kebocoran **3x24 jam**" disematkan ke Pasal 4 ayat (2) | `12-archive-architecture.md:91` | **UU 27/2022 Pasal 46 ayat (1)** | ✅ Ya | ❌ **Pasal salah** | **✗ SALAH PASAL.** Pasal 4 ayat (2) adalah definisi Data Pribadi Spesifik. Kewajiban pemberitahuan tertulis paling lambat 3×24 jam ada di **Pasal 46 ayat (1)**. Sumber: `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` (akses 22 Okt 2026) |
| V-11 | "Prinsip UU PDP (**Pasal 16**)" | `11-archive-proposal.md:246` | **UU 27/2022 Pasal 16** | ✅ Ya | ✅ Ya | **✓ TEPAT.** Pasal 16 ayat (2) memuat prinsip: tujuan terbatas dan spesifik/sah/transparan; sesuai tujuan; menjamin hak Subjek Data Pribadi; collecting data dibatasi; hak subjek; akurasi; keamanan; pembaruan data; komunikasi. Sumber: `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` (akses 22 Okt 2026) |
| V-12 | "Permenkes No. 26/2021" sebagai acuan tarif & basis rule engine | `11-archive-proposal.md:199,415`, `14-index.md:674,890` | **Permenkes 26/2021** - "tentang Pedoman Indonesian Case Base Groups (INA-CBG) dalam Pelaksanaan Jaminan Kesehatan", berlaku 30 Agt 2021, Status **Berlaku** (mencabut Permenkes 76/2016) | ✅ Ya | ⚠️ **Sebagian** | **⚠️ SEBAGIAN TEPAT.** Nomor benar. **Namun** §2.2 arsip expansão menyebutnya sebagai "Pedoman **Pencegahan dan Penanganan Kecurangan**" - itu adalah **judul Permenkes 16/2019**, bukan 26/2021. Sumber: `https://peraturan.bpk.go.id/Details/353186/permenkes-no-26-tahun-2021` (akses 22 Okt 2026) |
| V-13 | "Permenkes No. 3 Tahun 2023 tentang Standar Tarif Pelayanan Kesehatan dalam Penyelenggaraan Program Jaminan Kesehatan" | `11-archive-proposal.md:417`, `14-index.md:892` | **Permenkes 3/2023** - "tentang Standar Tarif Pelayanan Kesehatan Dalam Penyelenggaraan Program Jaminan Kesehatan", berlaku 9 Jan 2023, Status **Berlaku** | ✅ Ya | ✅ Ya | **✓ TEPAT.** Sumber: `https://peraturan.bpk.go.id/Details/275518/permenkes-no-3-tahun-2023` (akses 22 Okt 2026) |
| V-14 | "Permenkes No. 16 Tahun 2019 … **serta Pengendalian Gratifikasi** dalam Penyelenggaraan JKN" | `11-archive-proposal.md:131,414`, `14-index.md:606,889` | **Permenkes 16/2019** | ✅ Nomor/tahun; ❌ judul | ❌ | **✗ SALAH JUDUL** - duplikat V-03. Sumber: `https://peraturan.bpk.go.id/Details/129762/permenkes-no-16-tahun-2019` (akses 22 Okt 2026) |
| V-15 | "SALTED SHA-256 pseudonymization" + "de-identifikasi penuh data medis" + "Kepatuhan Privasi: **Mutlak**" | `11-archive-proposal.md:29,146,185,197` | Tidak ada dasar regulasi yang TOKENISASI otomatis | - | ❌ **Overclaim** | **✗ OVERCLAIM.** Lihat §4. Sumber: `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` Pasal 4 ayat (3) huruf f (akses 22 Okt 2026) |
| V-16 | "Peraturan tentang Pelindungan Data Pribadi, rekam medis, dan pencegahan fraud JKN" (tanpa nomor) | `06-research-notes.md:61` | - | ❌ **Tidak ada nomor** | ❌ | **✗ GAP.** Daftar "sumber awal" tanpa nomor peraturan. Sumber acuan yang seharusnya: `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022`, `/129762/`, `/245544/` (akses 22 Okt 2026) |
| V-17 | "Formularium Nasional / FORNAS" sebagai acuan rule engine | `11-archive-proposal.md:199`, `14-index.md:674` | **Kepmenkes HK.01.07/MENKES/1199/2025 tentang Formularium Nasional**, ditetapkan 31 Des 2025, **berlaku 1 April 2026** (Diktum KESEMBILAN) | ⚠️ **Nomor tidak disebut** | ⚠️ | **⚠️ TIDAK LENGKAP.** "FORNAS" tanpa nomor keputusan dan tanpa tanggal berlaku - padahal versi yang berlaku sejak 1 Apr 2026 adalah yang baru (mencabut Kepmenkes 2197/2023 dan 1818/2024). Sumber: PDF JDIH Kemenkes `https://jdih.kemkes.go.id/dokumen/peraturan/kepmenkes_1199_2025.pdf` (akses 22 Okt 2026) |
| V-18 | "Permenkes No. 22/2019" | - (tidak muncul di korpus) | **Permenkes 22/2019** - "Petunjuk Teknis Jabatan Fungsional Asisten Penata Anestesi", berlaku 9 Agt 2019, Status **Berlaku** | ✅ Ya | - | **⚠️ TIDAK DICANTUMKAN.** Relevan: anestesi koding (00.66/36.13) adalah domain kredensial yang wajib dibedakan dalam rule engine. Sumber: `https://peraturan.bpk.go.id/Details/138615/permenkes-no-22-tahun-2019` (akses 22 Okt 2026) |

---

## 3. Deep dive regulasi kunci

> Untuk setiap regulasi: nomor resmi, tanggal berlaku, isi, pasal yang relevan, dan **dampaknya terhadap proposal**.

### 3.1 Permenkes 16/2019 - Pencegahan & Penanganan Kecurangan (Fraud) JKN

- **Nomor resmi:** Peraturan Menteri Kesehatan Republik Indonesia Nomor 16 Tahun 2019
- **Judul resmi (verbatim):** "tentang **Pencegahan dan Penanganan Kecurangan (Fraud) serta Pengenaan Sanksi Administrasi terhadap Kecurangan (Fraud) dalam Pelaksanaan Program Jaminan Kesehatan**"
- **Tanggal berlaku:** 31 Juli 2019 · **Status:** Berlaku · **Mencabut:** Permenkes 36/2015
- **Sumber:** `https://peraturan.bpk.go.id/Details/129762/permenkes-no-16-tahun-2019` (akses 22 Okt 2026); naskah PDF JDIH Kemenkes.

**Pasal yang relevan:**
- **Pasal 1 angka 1** - definisi: *"Kecurangan (fraud) adalah tindakan yang dilakukan dengan sengaja untuk mendapatkan keuntungan finansial dari program Jaminan Kesehatan dalam Sistem Jaminan Sosial Nasional melalui perbuatan curang yang tidak sesuai dengan ketentuan peraturan perundang-undangan."* → **syarat "disengaja"**. Ini yang harus menjadi pagar konseptual proposal: model tidak dapat menyimpulkan fraud, hanya anomali yang perlu diperiksa.
- **Pasal 2** - siapa dapat melakukan kecurangan (faskes, tenaga kesehatan, peserta, pihak lain).
- **Pasal 5–6** - tim pencegahan, teguran, dan **sanksi administrasi** (termasuk pencabutan status faskes).
- **Tipologi yang dirinci dalam naskah** (menguji klaim `11-archive-proposal.md:130-135`):
  - (a) **penyesuaian/upcoding** diagnosis dan kode;
  - (b) **cloning/penjiplakan klaim**;
  - (c) **phantom billing** - klaim atas layanan yang tidak pernah diberikan;
  - (d) **inflated bills** - penggelembungan tagihan obat/alat kesehatan;
  - (e)–(f) **pemecahan episode pelayanan** / *services unbundling or fragmentation*;
  - (g) **rujukan semu** (*self-referals*).
- Tidak ada frasa "**Pengendalian Gratifikasi**" di dalam naskah maupun di judul resmi.

**Dampak terhadap proposal:** tipologi yang dirujuk arsip proposal **sebenarnya sahih** dan berasal dari Permenkes 16/2019 - tetapi karena judulnya disalahkan, kutipan itu tidak dapat dipertahankan sebagai rujukan hukum. Perbaiki ke judul resmi, lalu kaitkan tiap modus (SYND-01..09) ke pasal tipologi yang relevan. Selain itu, **`01-proposal.md:87` (UU 17/2023) dan `04-evidence-matrix.md:42-46` harus menyatakan bahwa label "fraud" pada dataset simulasi adalah *ground truth sintetis*, bukan hasil adjudicasi Permenkes 16/2019** - yang memang sudah dilakukan di `01-proposal.md:34` ("Purwarupa tidak memutuskan fraud secara hukum") dan harus dipertahankan.

### 3.2 Permenkes 24/2022 - Rekam Medis (Elektronik)

- **Nomor resmi:** Permenkes RI Nomor 24 Tahun 2022 tentang Rekam Medis
- **Tanggal berlaku:** 31 Agustus 2022 · **Status:** Berlaku · **Mencabut:** Permenkes 269/Menkes/Per/III/2008
- **Sumber:** `https://peraturan.bpk.go.id/Details/245544/permenkes-no-24-tahun-2022` (akses 22 Okt 2026)

**Pasal yang relevan:**
- **Pasal 10** - Sistem Elektronik RME wajib memiliki kemampuan kompatibilitas dan/atau interoperabilitas. **Ayat (3)** mendefinisikan interoperabilitas sebagai pertukaran data *"yang menggunakan standar pertukaran data"*. **Ayat (4)** - standar itu *"ber mengacu kepada standar sistem elektronik yang diselenggarakan oleh Kementerian Kesehatan sesuai dengan ketentuan peraturan perundang-undangan."*
- **Pasal 11** - variabel dan metadata (definisi, format, kodifikasi) ditetapkan Kemenkes.
- **Pasal 21** - RME yang disimpan Faskes *"harus terhubung/terinteroperabilitas dengan platform layanan interoperabilitas dan integrasi data kesehatan yang dikelola oleh Kementerian Kesehatan."*
- **Pasal 24** - transfer isi RME (rujukan) dilakukan melalui platform yang sama.
- **Pasal 32** - kerahasiaan isi RME wajib dijaga *"oleh semua pihak yang terlibat dalam pelayanan kesehatan di Fasilitas Pelayanan Kesehatan walaupun Pasien telah meninggal dunia"*; mencakup "(c) tenaga yang berkaitan dengan pembiayaan pelayanan kesehatan" dan "(d) badan hukum/korporasi dan/atau Fasilitas Pelayanan Kesehatan".

**Dampak terhadap proposal:**
1. **Tidak ada dasar hukum untuk menyatakan Permenkes 24/2022 = HL7 FHIR R4.** Standar itu ditetapkan Kemenkes (Permenkes 18/2022 dan platform SATUSEHAT), bukan oleh Permenkes 24/2022. `12-archive-architecture.md:69` harus diganti menjadi: *"Pasal 10 ayat (4) dan Pasal 21 Permenkes 24/2022 mewajibkan interoperabilitas melalui platform yang dikelola Kemenkes; standar pertukaran data yang digunakan adalah standar SATUSEHAT (HL7 FHIR R4), ditetapkan melalui Permenkes 18/2022."*
2. **Pasal 32 adalah yang berlaku langsung** - sofort applicable dan justru **memperkecil** ruang "aman": siapa pun yang terlibat dalam pelayanan dan pembiayaan, termasuk vendor AI pihak ketiga, terikat kewajiban kerahasiaan. Klaim "aman menurut Permenkes 24/2022" pada `10-simulation-dataset.md:3` bertentangan dengan pasal ini (lihat §4).
3. Naskah ini **tidak mengatur** privasi data non-medis; tidak boleh dipakai sebagai rujukan tunggal untuk klaim PDP.

### 3.3 UU 27/2022 - Pelindungan Data Pribadi

- **Nomor resmi:** UU No. 27 Tahun 2022 · ditetapkan & diundangkan 17 Oktober 2022 · **Status:** Berlaku
- **Sumber:** `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` (akses 22 Okt 2026)

**Pasal yang relevan (terverifikasi terhadap teks naskah):**
- **Pasal 4 ayat (1)** - Data Pribadi = spesifik + umum.
- **Pasal 4 ayat (2)** - Data Pribadi **Spesifik**: (a) data dan informasi kesehatan; (b) biometrik; (c) genetika; (d) catatan kriminal; (e) data anak; (f) kerahasiaan pribadi; (g) data lain.
- **Pasal 4 ayat (3)** - Data Pribadi **Umum**: nama lengkap, jenis kelamin, agama, status perkawinan, dan/atau Data Pribadi yang **dikombinasikan untuk mengidentifikasi seseorang**. → inilah klausa re-identification yang relevan untuk data sintetis ber-nama.
- **Pasal 16 ayat (2)** - prinsip pemrosesan (terbatas & spesifik/transparan; sesuai tujuan; menjamin hak subjek; pengumpulan dibatasi; hak subjek; akurasi; keamanan; pembaruan; komunikasi).
- **Pasal 20 ayat (2)** - dasar pemrosesan (persetujuan eksplisit; kewajiban perjanjian; kewajiban hukum; kepentingan vital; kepentingan publik; kepentingan sah).
- **Pasal 46 ayat (1)** - pemberitahuan tertulis **paling lambat 3×24 jam** kepada subjek data dan lembaga.
- **Pasal 53** - kewajiban menunjuk Migration Officer/fungsi Pelindungan Data Pribadi untuk skala besar & data spesifik.
- **Pasal 65–66** - larangan (bukan pidana).
- **Pasal 67–68** - ketentuan pidana; **Pasal 69** - pidana tambahan; **Pasal 70** - sanksi korporasi (denda s.d. 10× maksimum).
- **Pasal 74** - masa penyesuaian **2 tahun** sejak diundangkan (berakhir Okt 2024).
- **Pasal 75** - peraturan perundang-undangan yang ada tetap berlaku sepanjang tidak bertentangan.

**Dampak terhadap proposal:**
1. Semua kutipan pasal di arsip proposal harus diluruskan (§2, V-08 s.d. V-11).
2. **Pasal 75 adalah dasar argumentasi bahwa Permenkes 16/2019, Permenkes 24/2022, PP 71/2019 dkk. tetap berlaku** - berguna justru sebagai bukti bagi proposal, tapi hanya sepanjang tidak bertentangan.
3. **Pasal 74 sudah habis** (Okt 2024). Klaim kepatuhan harus menyatakan bahwa sistem **sudah** berada pada rezim UU PDP penuh, bukan "dalam masa transisi".
4. **Pasal 53 ayat (1) huruf c** - dataset 6,3 juta baris DM FKRTL + 143 ribu baris kepesertaan yang slated untuk diproses berada pada skala besar data spesifik → kewajiban menunjuk Migration Officer bersifat **wajib**, bukan opsional. `01-proposal.md:63` menyebut "dasar pemrosesan yang sah" tetapi belum menyebut Migration Officer.

### 3.4 PP 71/2019 - Penyelenggaraan Sistem dan Transaksi Elektronik (SSTE/PSE)

- **Nomor resmi:** PP No. 71 Tahun 2019 · berlaku 10 Oktober 2019 · **Status:** Berlaku · **Mencabut:** PP 82/2012
- **Sumber:** `https://peraturan.bpk.go.id/Details/122030/pp-no-71-tahun-2019` (akses 22 Okt 2026)

**Isi yang relevan:**
- **Pasal 1 angka 29** mendefinisikan Data Pribadi (istilah yang **sudah ada sebelum UU PDP** - konsistensi dengan posisi UU PDP).
- **Pasal 14–15** memuat kewajiban PSE dalam pemrosesan Data Pribadi: pengumpulan Data Pribadi dibatasi pada tujuan yang sah; pemrosesan sesuai tujuan; menjamin hak pemilik Data Pribadi; pengouters data **beralur** dan **menggunakan server di dalam negeri**; pemrosesan **di dalam negeri** *diolah secara aman*; **penghapusan/musnahkan** Data Pribadi yang tidak diperlukan.
- **Pasal 15** - *"Penghapusan atau pemusnahan Data Pribadi ... yang tidak diperlukan ... wajib dilakukan"*; processing wajib **berhenti** setelah waktu maksimum penyimpanan.

**Dampak terhadap proposal:**
1. **PP 71/2019 tidak disebut di mana pun** di korpus, padahal Aegis-JKN adalah PSE yang memproses data kesehatan dan deploy ke `aegisjkn.vercel.app` (hosting di luar negeri). Kewajiban **server di dalam negeri** dan **peraliran data antar-nas** berkonflik langsung dengan arsitektur berbasis Vercel. `02-architecture.md:95` sudah benar bahwa integrasi SATUSEHAT/V-Claim sebagai "tahap mendatang" - **hal yang sama harus berlaku untuk hosting cloud**.
2. PP 71/2019 kini menjadi **regime pengawasan PSE di bawah Komdigi** (masih berlaku), di samping UU PDP.

### 3.5 Permenkes 26/2021 - Pedoman INA-CBG

- **Nomor resmi:** Permenkes RI Nomor 26 Tahun 2021 · berlaku 30 Agustus 2021 · **Status:** Berlaku · **Mencabut:** Permenkes 76/2016
- **Sumber:** `https://peraturan.bpk.go.id/Details/353186/permenkes-no-26-tahun-2021` (akses 22 Okt 2026); naskah PDF JDIH Kemenkes.

**Isi yang relevan (kutipan dari naskah):**
- **Pasal tentang tugas koder:** kodifikasi diagnosis dan prosedur *"sesuai dengan ICD-10 (International Statistical Classification of Diseases and Related Health Problems 10th Revision) **Versi Tahun 2010**"* dan *"ICD-9-CM (International Classification of Diseases, Ninth Revision, Clinical Modification) **Versi Tahun 2010**"*.
- **Verifikator BPJS Kesehatan** berkewajiban memverifikasi kesesuaian diagnosis dan tindakan dengan **ICD-10 Versi 2010** dan **ICD-9-CM Versi 2010**.
- **Pengelompokan INA-CBG** menghasilkan **1.075 kelompok kasus** = 786 rawat inap + 289 rawat jalan.

**Dampak terhadap proposal - TEMUAN BARU (tidak sudah dilaporkan sebelumnya):**
- **Versi koding yang WAJIB dipakai untuk tarif JKN adalah ICD-10 Versi 2010 dan ICD-9-CM Versi 2010.** Deskripsi kode pada `09-draft-hub.md:67-90` dan `10-simulation-dataset.md:65-87` tidak mencantumkan versi. Perbedaan 2010 vs 2016 memengaruhi label (mis. K29.7 = "Gastritis, unspecified" pada 2010 vs "Gastritis without bleeding" pada 2016; S72.0 pada 2010 = "Fracture of neck of femur" vs "Fracture of femoral shaft" pada 2016). **Karena angka "Biaya Rujukan" dikaitkan dengan kode-kode ini, tanpa versi koding angka tersebut tidak dapat ditelusuri ke grup kasus mana pun.**
- Transisi **INA-CBG → iDRG** sudah dimulai (uji coba nasional 2025 via SE Kemenkes HK.02.02/MENKES/936/2025). **Nomor peraturan yang menetapkan iDRG sebagai pengganti penuh INA-CBG: TIDAK TERVERIFIKASI** pada sumber resmi yang dapat diakses (lihat §6). Proposal yang memuat tarif INA-CBG sebagai basis harus menyatakan status transisi ini dan menyertakan rujukan **iDRG** sebagai rencana.

### 3.6 PP 28/2024 - Pelaksanaan UU 17/2023 tentang Kesehatan

- **Nomor resmi:** PP No. 28 Tahun 2024 · berlaku 26 Juli 2024 · **Status:** Berlaku · **Mencabut:** PP 53/2021, PP 47/2021, PP 21/2020, PP 88/2020, dan lain-lain
- **Sumber:** `https://peraturan.bpk.go.id/Details/294077/pp-no-28-tahun-2024` (akses 22 Okt 2026)

**Isi yang relevan:** UU 17/2023 adalah-payung; PP 28/2024 mengaturnya. Naskah mendefinisikan **"Data Kesehatan"** (ayat 25) dan **"Informasi Kesehatan"** (ayat 26), mengatur rumah sakit,|%research dan pengembangan kesehatan, serta pel scientistsudy. Karena proposal menyebut UU 17/2023 sebagai dasar, **PP 28/2024 adalah peraturan pelaksana wajib yang belum dicantumkan**.

### 3.7 UU 24/2011 - Badan Penyelenggara Jaminan Sosial, dan UU 40/2004 - SJSN

- **UU 24/2011:** berlaku 25 Nov 2011 · **Status:** Berlaku · **Diubah:** UU 6/2023 (Cipta Kerja), UU 11/2020, PERPU 2/2022 · **Mencabut:** UU 3/1992. Sumber: `https://peraturan.bpk.go.id/Details/39268/uu-no-24-tahun-2011` (akses 22 Okt 2026).
- **UU 40/2004:** ditetapkan 19 Okt 2004, berlaku 19 Okt 2004, LN. 2004/No.150 · **Status:** Berlaku · **Diubah:** UU 6/2023, UU 4/2023, UU 11/2020, PERPU 2/2022. Sumber: `https://peraturan.bpk.go.id/Details/40787/uu-no-40-tahun-2004` (akses 22 Okt 2026).

**Isi yang relevan:** UU 40/2004 adalah **landasan normatif SJSN yang mengsuffix-kan JKN sebagai program Exchanges**; UU 24/2011 menetapkan BPJS Kesehatan sebagai badan pelaksana. Keduanya adalah rujukan yang wajib untuk sustain legitimacy proposals JKN - **tidak ada satu pun yang dicantumkan** di `01-proposal.md` atau `04-evidence-matrix.md`.

### 3.8 UU 13/2022 - Perubahan atas UU 12/2011 (Peraturan Perundang-undangan)

- **Nomor resmi:** UU No. 13 Tahun 2022 tentang Perubahan **Kedua** atas UU No. 12 Tahun 2011 tentang Pembentukan Peraturan Perundang-undangan · ditetapkan & berlaku 16 Juni 2022 · LN. 2022/No.143 · **Status:** Berlaku
- **Sumber:** `https://peraturan.bpk.go.id/Details/212810/uu-no-13-tahun-2022` (akses 22 Okt 2026)

**Catatan perubahan (terverifikasi dari halaman BPK):** UU 13/2022 **diubah dengan UU No. 1 Tahun 2026** (penyesuaian ketentuan Pasal 15 UU 12/2011). Fokus UU 12/2011–13/2022 adalah **perlakuan administratif** yang tunduk pada persetujuan - termasuk **preskripsi obat** (§"IZIN") yang **tidak boleh disobahkan** oleh apoteker. **Dampak:** aturan yang bersifat "dilarang" berlaku tanpa persetujuan, dan khusus untuk **per resep** - apa yang boleh dilakukan dengan obat. Relevan untuk claim `SYND-04 Drug Diversion` (kuantitas insulin 24–30 pen vs dosis rasional 1–2 pen/bulan) dan `SYND-04 Drug Diversion`-related rules.

### 3.9 Permenkes 6/2026 - Rumah Sakit (baru, berlaku 12 Juni 2026)

- **Nomor resmi:** Permenkes RI Nomor 6 Tahun 2026 tentang Rumah Sakit · **Status:** Berlaku · **Mencabut:** Permenkes 33/2023 (RS Kapal), Permenkes 40/2022 (persyaratan teknis bangunan/prasarana/peralatan RS), Permenkes 31/2022 (PP 93/2015 tentang RS)
- **Sumber:** `https://peraturan.bpk.go.id/Details/350851/permenkes-no-6-tahun-2026` (akses 22 Okt 2026)

**Dampak:** proposal harus bertahan selama masa transisi; klaim-klaim dataset merujuk faskes (RS_A..RS_J) harus dievaluasi terhadap standar RS terkini. **Tidak dicantumkan di proposal.**

### 3.10 Kepmenkes HK.01.07/MENKES/1199/2025 - Formularium Nasional (baru, berlaku 1 April 2026)

- **Nomor resmi:** Keputusan Menteri Kesehatan RI Nomor HK.01.07/MENKES/1199/2025 tentang Formularium Nasional · ditetapkan Jakarta, 31 Desember 2025 · **Diktum KESEMBILAN:** "Penerapan Formularium Nasional sebagaimana dimaksud dalam Diktum KESATU **mulai berlaku pada tanggal 1 April 2026**." · **Mencabut:** Kepmenkes HK.01.07/Menkes/2197/2023 dan Kepmenkes HK.01.07/Menkes/1818/2024 (Diktum KETIGA)
- **Sumber:** PDF JDIH Kemenkes `https://jdih.kemkes.go.id/dokumen/peraturan/kepmenkes_1199_2025.pdf` (akses 22 Okt 2026)

**Dampak:** kalau proposal menyebut FORNAS sebagai basis rule engine, **harus menyebut nomor keputusan dan tanggal berlaku 1 April 2026** - angka-angka FORNAS yang beredar luas (2197/2023) sudah dicabut.

---

## 4. Audit klaim "privacy-by-design"

### 4.1 Klaim yang diklaim

`10-simulation-dataset.md:3` (diulang persis di `09-draft-hub.md:6` dan `:218`, serta `14-index.md:49` dan `:261`):

> "Dataset sintetis untuk uji simulasi MHGSL pada purwarupa Aegis-JKN. **100 klaim, privacy-by-design - bukan data peserta riil, aman menurut Permenkes 24/2022 & UU PDP No. 27/2022.**"

### 4.2 Verifikasi: apakah "aman" itu benar?

**Tidak.** Empat alasan, masing-masing dapat diverifikasi:

**(a) Data sintetis bukan data pribadi - tetapi dataset ini bukan murni sintetis.**
Data yang dimuat: 20 nama pasien realistis (`Ahmad Fauzi`, `Siti Nurhaliza`, `dr. Mulyadi Santoso Sp.B` …), 20 nama dokter dengan gelar & spesialisasi, 10 nama faskes (`RS_A`…`RS_J` - fiktif, ✅ aman), kota/kabupaten nyata (Bandung, Semarang, Makassar, Yogyakarta), tanggal lahir, jenis kelamin, usia, dan diagnosis bertanda (mis. "P03, 47, L, PBI, Bandung"). Nama-nama ini adalah **data pribadi yang dapat diidentifikasi secara langsung** menurut definisi Pasal 4 ayat (1) UU PDP - meskipun atas nama orang fiktif. Sumber: `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` (akses 22 Okt 2026); data: `N:\HEALTHKATHON\analysis\corpus\claims_v2_live.csv` (kolom `Name`, `Pasien`, `Dokter`, `Faskes`).

**(b) "Bukan data peserta riil" ≠ anonim. Ini pseudonymization, dan UU PDP mengaturnya secara eksplisit.**
UU PDP tidak mengenal kategori "sintetis" sebagai pengecualian. Yang dikenal adalah:
- **Pasal 4 ayat (3) huruf f** - "Data Pribadi yang **dikombinasikan** untuk mengidentifikasi seseorang" tetap Data Pribadi. Kombinasi nama + kota + tanggal lahir + kondisi medis + nama dokter + faskes = **quasi-identifier** yang, dalam dataset publik, dapat mengidentifikasi orang nyata bila data realistis disalin dari kasus nyata.
- **Pasal 4 ayat (1)** tidak memberi hak atas data sintetis. Yang menentukan adalah **dapat/tidak dapat diidentifikasi**.
- **Pasal 16 ayat (2)** - prinsip pemrosesan berlaku atas *data pribadi*; kalau data tetap dapat diidentifikasi, seluruh rezim PDP berlaku: dasar pemrosesan (Pasal 20), hak subjek (Pasal 5–9), Migration Officer (Pasal 53), notifikasi 3×24 jam (Pasal 46), dan sanksi pidana (Pasal 67–70).

**Kesimpulan hukum:** data sintetis yang masih memuat identitas langsung + quasi-identifier berada pada rezim **UU PDP penuh**, bukan di luar rezim. Pernyataan "aman menurut UU PDP" tanpa dasar analisis re-identification adalah **overclaim**, bukan Unsafe.

**(c) Klaim ini bertentangan dengan dokumen sendiri.**
- `02-architecture.md:63` - "**Pseudonimisasi tidak dianggap sebagai anonimisasi sempurna.**"
- `02-architecture.md:94` - "**Hindari menjadikan hash biasa sebagai pengganti kontrol privasi.** Pseudonimisasi memerlukan perlindungan kunci dan pembatasan akses."
- `02-architecture.md:88` - "**Gunakan data sintetis untuk demonstrasi**" (dinyatakan sebagai *tindakan*, bukan sebagai status kepatuhan otomatis).
- `01-proposal.md:63` - "**Pseudonimisasi tidak dianggap sebagai anonimisasi sempurna.**"

Empat dokumen menyatakan hash ≠ anonim; satu baris promo menyatakan "aman". **Baris promo yang harus dihapus**, karena menunjukkan chipset yang lebih rendah dari standar yang dipakai dokumen lain.

**(d) Permenkes 24/2022 justru menambah kewajiban, bukan melegitimasi.**
- **Pasal 32** - kerahasiaan isi RME wajib dijaga oleh semua pihak yang terlibat dalam pelayanan kesehatan, termasuk **(c) tenaga yang berkaitan dengan pembiayaan pelayanan kesehatan** dan **(d) badan hukum/korporasi dan/atau Fasilitas Pelayanan Kesehatan**. Vendor AI yang memproses data klaim masuk lingkup ini.
- **Pasal 10 ayat (4)** - standar interoperabilitas ditentukan Kemenkes; sistem yang tidak mengikuti standar tidak dapat dipertanggungjawabkan sebagai interoperabel.
- **Pasal 4** - RME wajib tersedia sesuai ketentuan; klaim "aman" bukan terbantahkan.

### 4.3 Dampak re-identification untuk demo publik

`aegisjkn.vercel.app` adalah **public demo** yang memuat nama-nama realistis + kota + kondisi medis + nama dokter. Risiko nyata:
1. **Risiko kebocoran data** - data berasal dari generator deterministik (seed 20260707), sehingga **nama-nama yang sama akan muncul kembali di setiap demo berikutnya**; bila nanti dipakai data hybrid (DM + sintetis), identitas peserta riil bisa bocor melalui kolom `Name`/`Pasien`.
2. **Risiko kebocoran identitas** - kombinasi nama + DOB + kota + diagnosis + dokter adalah near-unique. Lelaran data combination.
3. **Risiko kepatuhan** - PPT/peny: pada konteks ini, klaim "aman" yang tidak terbukti dapat dibantah juri BPJS dan partnered, dan undermined`10-simulation-dataset.md:3` adalah salah satu artefak yang **dipublikasikan** (tautan di `09-draft-hub.md` dan `14-index.md`).
4. **Tidak ada data-protection impact assessment (DPIA/ATD)** yang ada - Pasal 34 UU PDP mengharuskan penilaian dampak pelindungan data pribadi untuk pemrosesan data spesifik berskala besar. **Pasal 34 TIDAK disebut di mana pun dalam korpus** - ini gap kepatuhan substantif.

### 4.4 Rekomendasi atas klaim ini

Ganti `10-simulation-dataset.md:3` (dan duplikatnya) dengan kalimat yang **tidak mengklaim status kepatuhan**:

> "Dataset sintetis untuk uji simulasi MHGSL pada purwarupa Aegis-JKN. 100 klaim fiktif dengan namainitialized sintetis; bukan data peserta JKN. Kepatuhan privasi dataset sintetis **belum dinyatakan final**; analisis dampak dan uji re-identification identifier sedang dilakukan."

---

## 5. Audit kode medis & tarif

### 5.1 Kode diagnosis ICD-10 (10 kode)

Sumber: WHO ICD-10 Browser, `https://icd.who.int/browse10/2016/en/GetConcept?ConceptId=<kode>` dan `https://icd.who.int/browse10/2010/en/GetConcept?ConceptId=<kode>` (akses 22 Okt 2026). Lokasi deskripsi: `09-draft-hub.md:69-78` dan `10-simulation-dataset.md:65-75`.

| Kode | Deskripsi di korpus | Benar? | Sumber |
|---|---|---|---|
| K80.2 | Kolelitiasis, tanpa kolesistitis | ✅ **Tepat** | WHO 2010/2016: "Calculus of gallbladder without cholecystitis" |
| K29.7 | Gastritis, tanpa perdarahan | ⚠️ **Tidak presisi** | WHO 2010: "Gastritis, unspecified"; WHO 2016: "Gastritis without bleeding". Deskripsi korpus mengikuti versi 2016; **Permenkes 26/2021 mewajibkan Versi 2010** → label tidak sesuai versi yang wajib |
| E11.9 | Diabetes melitus tipe 2, tanpa komplikasi | ✅ **Tepat** | WHO 2016: "E11 Type 2 diabetes mellitus" + subkode ".9 Without complications" |
| S72.0 | Fraktur kolum femur, tertutup | ⚠️ **Tidak presisi** | WHO 2010: "Fracture of neck of femur"; WHO 2016: "Fracture of femoral shaft". "Kolum femur" ≠ "neck of femur" |
| O80 | Persalinan tunggal spontan | ✅ **Tepat** | WHO 2010/2016: "Single spontaneous delivery" |
| I21.9 | Infark miokard akut, tidak spesifik | ✅ **Tepat** | WHO 2010/2016: "Acute myocardial infarction, unspecified" |
| J18.9 | Pneumonia, organisme tidak spesifik | ⚠️ **Tidak presisi** | WHO 2010/2016: "Pneumonia, unspecified". "Organisme tidak spesifik" menambahkanimate "organism unspecified" yang tidak ada di label baku |
| K35.8 | Apendisitis akut | ⚠️ **Tidak presisi** | WHO 2010/2016: "Acute appendicitis, **other and unspecified**" - kualifikasi dihapus |
| K40.9 | Hernia inguinalis, tanpa obstruksi | ⚠️ **Tidak presisi** | WHO 2010/2016: "Unilateral or unspecified inguinal hernia, without obstruction **or gangrene**" |
| N20.0 | Kalkulus ginjal | ✅ **Tepat** | WHO 2010/2016: "Calculus of kidney" |

**Tidak ada kode ICD-10 yang salah secara substantif.** Masalahnya presisi label dan - lebih penting - **ketiadaan nomor versi koding**, padahal Permenkes 26/2021 mewajibkan ICD-10 Versi 2010.

### 5.2 Kode prosedur ICD-9-CM (10 kode)

Sumber: **CDC ICD-9-CM Procedures FY2010** (`https://perhati-kl.or.id/wp-content/uploads/2017/08/ICD9CM2010.pdf`, salinan resmi CDC, akses 22 Okt 2026), dicek silang dengan listing FY2007 (arsip lokal). Lokasi: `09-draft-hub.md:81-90`, `10-simulation-dataset.md:78-87`.

| Kode | Deskripsi di korpus | Benar? | Sumber (ICD-9-CM FY2010) |
|---|---|---|---|
| 00.66 | "Angioplasty koroner + stent (PCI)" | ❌ **SALAH LABEL** | "Percutaneous transluminal coronary angioplasty [PTCA] or coronary atherectomy" - **tanpa stent**. Kode stent: **36.06** "Insertion of non-drug-eluting coronary artery stent(s)" dan **36.07** (drug-eluting). Konflik internal: label stent tidak ada di kode yang dipakai |
| 36.13 | Coronary artery bypass graft (CABG) | ✅ **Tepat** | "(Aorto)coronary bypass of three coronary arteries" - CABG generik; label korpus lebih longgar tapi wajar |
| 47.09 | Apendektomi | ✅ **Tepat** | "Other appendectomy" |
| 53.1 | Reparasi hernia inguinalis | ✅ **Tepat** | "Other bilateral repair of inguinal hernia" - label korpus menghilangkan kata "bilateral" |
| 51.23 | Kolesistektomi laparoskopik | ✅ **Tepat** | "Laparoscopic cholecystectomy" |
| 74.1 | Seksio sesaria | ✅ **Tepat** | "Low cervical cesarean section" - label korpus lebih umum, tidak keliru |
| 81.52 | Hemiarthroplasty pangkal | ✅ **Tepat** | "Partial hip replacement" |
| 96.04 | Pemasangan pipa endotrakeal (intubasi) | ✅ **Tepat** | "Insertion of endotracheal tube" |
| 93.90 | "Terapi oksigen tekanan positif" | ❌ **SALAH LABEL** | "**Non-invasive mechanical ventilation**" (BiPAP). Positive-pressure therapy = **93.91** "Intermittent positive pressure breathing [IPPB]" |
| 98.51 | Fragmentasi batu saluran kemih (ESWL) | ✅ **Tepat** | "Extracorporeal shockwave lithotripsy [ESWL] of the kidney, ureter and/or bladder" |

**Catatan versi (tidak ada di korpus):** Permenkes 26/2021 mewajibkan **ICD-9-CM Versi 2010**. Deskripsi di atas diverifikasi pada FY2010. Some labels berbeda di FY2007 (mis. 98.51 pada FY2007 = "Extracorporeal shockwave lithotripsy [ESWL] of the kidney" - sama; 00.66 identik). Nomor kode FY2010 dan FY2007 untuk 10 kode ini **identik**, sehingga risiko praktis rendahnya - tetapi **kepatuhan formal tetap mensyaratkan penyebutan Versi 2010**.

### 5.3 Item FORNAS (10 obat)

Sumber: **Kepmenkes HK.01.07/MENKES/1199/2025**, PDF JDIH Kemenkes (akses 22 Okt 2026), terindeks pada subkelas terapi §§6–16. Lokasi: `09-draft-hub.md:93-102`, `10-simulation-dataset.md:90-99`.

| Kode di korpus | Obat | FORNAS? | Verifikasi |
|---|---|---|---|
| M01 | Metformin 500 mg | Ya | ✅ Tercantum (11 kemunculan dalam PDF) |
| M02 | Amlodipin 10 mg | Ya | ✅ Tercantum |
| M03 | Seftriakson 1 g | Ya | ✅ Tercantum (ejaan naskah: "seftriakson") |
| M04 | Omeprazol 40 mg | Ya | ✅ Tercantum |
| M05 | Salbutamol 2,5 mg nebules | Ya | ✅ Tercantum |
| M06 | Atorvastatin 20 mg | Ya | ✅ Tercantum |
| M07 | Furosemid 40 mg | Ya | ✅ Tercantum |
| M08 | Parasetamol 500 mg | Ya | ✅ Tercantum |
| **M09** | **Insulin glargin 100 UI/ml** | **"Tidak"** | ❌ **SALAH.** Insulin glargine **tercantum** di Kepmenkes 1199/2025 **§16.2.2 Antidiabetes Parenteral**, dengan sediaan "1. inj 100 IU/mL (kemasan vial, cartridge) *", "2. inj 300 IU/mL", dan sediaan disposable cartridge/penfill. Tanda `*` = initial treatment di FPKTL dilanjutkan dapat disediakan/diberikan FPKTP atau apotek BPJS (rujuk balik). **"Tidak" keliru.** |
| M10 | Klopidogrel 75 mg | Ya | ✅ Tercantum (naskah: "klopidogrel", §"tab 75 mg*" dan "tab sal selaput 300 mg") |

**Catatan tambahan:** kode obat "M01…M10" adalah **kode internal proyek**, bukan kode FORNAS. FORNAS tidak memakai kode M01/M02 seperti itu. Menyebut kolom "Kode" di tabel FORNAS tanpa penjelasan akan menyesatkan pembaca yang mengira itu kode FORNAS.

### 5.4 Audit tarif "Biaya Rujukan"

`09-draft-hub.md:80-90` dan `10-simulation-dataset.md:77-87` menampilkan "Biaya Rujukan" (Rp58.000.000, Rp78.000.000, Rp6.800.000, Rp8.200.000, Rp14.500.000, Rp6.200.000, Rp46.500.000, Rp750.000, Rp640.000, Rp5.600.000) **tanpa acuan**: tidak ada kode grup kasus INA-CBG, tidak ada kelas Dependent, tidak ada tarif acuan Permenkes 3/2023, tidak ada nama tabel. Yang terjadi:
- Angka **tidak dapat direproduksi** oleh verifikator mana pun.
- `11-archive-proposal.md:15,30` memakai angka serupa untuk klaim "penghematan Rp507.370.000" - sehingga rantai-financial ini **tidak dapat diuji**.
- `04-evidence-matrix.md:42` (E-11) sudah menandai hal ini: "Belum dapat direproduksi per klaim". **Rekomendasi: hapus kolom "Biaya Rujukan" dari tabel publik, atau tambahkan kolom "Kode Grup Kasus INA-CBG" + "Tarif acuan (Permenkes 3/2023)".**

---

## 6. Status validity per 22 Oktober 2026

Sumber status: JDIH BPK `peraturan.bpk.go.id/Details/...` (akses 22 Okt 2026); naskah PDF JDIH Kemenkes.

| Regulasi | Masih berlaku? | Catatan perubahan |
|---|---|---|
| **UU 27/2022** (Pelindungan Data Pribadi) | ✅ **Berlaku** | §Tidak diubah. Pasal 74: masa penyesuaian 2 tahun **sudah berakhir** (Okt 2024). Pasal 75: peraturan lain tetap berlaku sepanjang tidak bertentangan. **PP 33/2026 (aturan pelaksanaan) ditetapkan 15 Jul 2026, baru berlaku 15 Jan 2027** - belum berlaku per tanggal audit. |
| **UU 17/2023** (Kesehatan) | ✅ **Berlaku** | Diimplementasikan oleh **PP 28/2024** (berlaku 26 Jul 2024) - PP tidak dicantumkan di proposal |
| **UU 24/2011** (BPJS) | ✅ **Berlaku** | Diubah UU 6/2023, UU 11/2020, PERPU 2/2022; mencabut UU 3/1992 |
| **UU 40/2004** (SJSN) | ✅ **Berlaku** | Diubah UU 6/2023, UU 4/2023, UU 11/2020, PERPU 2/2022 |
| **UU 13/2022** (Peraturan Perundang-undangan) | ✅ **Berlaku** | **Diubah dengan UU No. 1 Tahun 2026** (penyesuaian ketentuan Pasal 15 UU 12/2011). Belum dicantumkan di proposal |
| **PP 71/2019** (SSTE/PSE) | ✅ **Berlaku** | Mencabut PP 82/2012. Belum dicantumkan di proposal. AEHF:PPSE |
| **PP 28/2024** (Pelaksanaan UU 17/2023) | ✅ **Berlaku** | Mencabut PP 53/2021, PP 47/2021, PP 21/2020, PP 88/2020. Belum dicantumkan |
| **PP 33/2026** (Pelaksanaan UU PDP) | ⏳ **Belum berlaku** (berlaku 15 Jan 2027) | Ditetapkan 15 Jul 2026. Sumber: `https://www.hukumonline.com/pusatdata/detail/lt6a9164bf1e96a/peraturan-pemerintah-nomor-33-tahun-2026/` (akses 22 Okt 2026). **Nomor halaman di JDIH BPK: TIDAK TERVERIFIKASI** (tidak ditemukan via `peraturan.bpk.go.id/Search` pada 22 Okt 2026) - hanya terverifikasi via sumber sekunder |
| **Perpres 82/2018** (Jaminan Kesehatan) | ✅ **Berlaku** | Diubah Perpres 75/2019, 64/2020, **59/2024** (Perubahan Ketiga). Belum dicantumkan |
| **Perpres 75/2019 / 64/2020 / 59/2024** | ✅ **Berlaku** | Rantai perubahan Perpres 82/2018 |
| **Permenkes 16/2019** (Fraud JKN) | ✅ **Berlaku** | Mencabut Permenkes 36/2015. **Judul proposal salah** (V-03) |
| **Permenkes 24/2022** (Rekam Medis) | ✅ **Berlaku** | Mencabut Permenkes 269/Menkes/Per/III/2008. **Tidak menyebut HL7/FHIR/SATUSEHAT** (V-06) |
| **Permenkes 26/2021** (INA-CBG) | ✅ **Berlaku** | Mencabut Permenkes 76/2016. **Memerlukan ICD-10/ICD-9-CM Versi 2010**. Transisi iDRG berjalan |
| **Permenkes 3/2023** (Standar Tarif) | ✅ **Berlaku** | Belum dicantumkan sebagai rujukan utama di proposal |
| **Permenkes 18/2022** (Satu Data Kesehatan) | ✅ **Berlaku** | Dasar hukum integrasi & interoperabilitas SATUSEHAT yang sebenarnya - belum dicantumkan |
| **Permenkes 22/2019** (Asisten Penata Anestesi) | ✅ **Berlaku** | Belum dicantumkan |
| **Permenkes 6/2026** (Rumah Sakit) | ✅ **Berlaku** sejak 12 Jun 2026 | Mencabut Permenkes 33/2023, 40/2022, 31/2022. Belum dicantumkan |
| **Permenkes 36/2015** (Fraud JKN, lama) | ❌ **Dicabut** oleh Permenkes 16/2019 | Tidak dicantumkan di proposal - benar |
| **Permenkes 76/2016** (INA-CBG, lama) | ❌ **Dicabut** oleh Permenkes 26/2021 | Tidak dicantumkan - benar |
| **Kepmenkes HK.01.07/MENKES/1199/2025** (FORNAS) | ✅ **Berlaku sejak 1 Apr 2026** | Mencabut Kepmenkes 2197/2023 dan 1818/2024. Belum dicantumkan (yang disebut hanya "FORNAS" tanpa nomor) |
| **Peraturan BPJS 3/2024** (Skrining & Riwayat Kesehatan) | ✅ **Berlaku** | Mencabut Peraturan BPJS 2/2019. Belum dicantumkan; relevan karena proposal menyebut "skrining/riwayat" |
| **Permenkes 11/2017** (Keselamatan Pasien) | ⚠️ **TIDAK TERVERIFIKASI** | Judul & isi terkonfirmasi dari sumber sekunder (melatalkan Pasal 36 mencabut Permenkes 1691/MENKES/Per/VIII/2011), tetapi **halaman JDIH BPK untuk Permenkes 11/2017 tidak ditemukan** - `peraturan.bpk.go.id/Search` tidak mengembalikannya (22 Okt 2026). Status "Berlaku"/"Dicabut" **tidak dapat dipastikan** dari sumber resmi |
| **Permenkes 33/2024** | ⚠️ **TIDAK TERVERIFIKASI** | Nomor 33 dipakai beberapa kali dalam empat tahun berbeda (33/2015 Pedoman Penyusunan…, 33/2019 Perilaku Interaksi-tenaga Kesehatan, 33/2023 RS Kapal). **Identitas Permenkes 33/2024 tidak dapat dipastikan** dari sumber resmi |
| **iDRG (pengganti INA-CBG)** | ⚠️ **TIDAK TERVERIFIKASI** | Uji coba nasional 2025 (SE Kemenkes HK.02.02/MENKES/936/2025) terkonfirmasi; **peraturan yang menetapkan iDRG menggantikan INA-CBG secara penuh belum ditemukan** di sumber resmi yang dapat diakses (22 Okt 2026) |
| **Pasal 34 UU PDP** (penilaian dampak / DPIA) | ✅ Berlaku | **Tidak disebut di mana pun di korpus** - gap kepatuhan substantif untuk pemrosesan data kesehatan berskala besar |
| **Permenkes 11/2017 & Permenkes 33/2024** → **rekomendasi**: gambar api | | Lihat §7 |

---

## 7. Daftar regulasi yang WAJIB dicantumkan di proposal

Diurutkan menurut prioritas untuk proposal Healthkathon BPJS. Kolom "Alasan" menunjukkan kaitan konkret dengan isi proposal.

| # | Regulasi | Nomor & status | Kenapa wajib | Sumber |
|---|---|---|---|---|
| R-01 | **Permenkes 16/2019** - *Pencegahan dan Penanganan Kecurangan (Fraud) serta Pengenaan Sanksi Administrasi…* | Berlaku 31 Jul 2019 | **Satu-satunya dasar hukum tipologi fraud JKN** yang dipakai rule engine. **Perbaiki judulnya** (V-03) | `https://peraturan.bpk.go.id/Details/129762/permenkes-no-16-tahun-2019` |
| R-02 | **Permenkes 26/2021** - Pedoman INA-CBG | Berlaku 30 Agt 2021 | Menetapkan **ICD-10 & ICD-9-CM Versi 2010** + 1.075 grup kasus. Tanpa ini, kode & tarif di tabel tidak dapat diverifikasi | `https://peraturan.bpk.go.id/Details/353186/permenkes-no-26-tahun-2021` |
| R-03 | **Permenkes 24/2022** - Rekam Medis | Berlaku 31 Agt 2022 | Pasal 10(4)/11/21/24 (interoperabilitas, **delegasi standar ke Kemenkes**) + Pasal 32 (kerahasiaan). **Hapus klaim HL7 FHIR R4 dari naskahnya** | `https://peraturan.bpk.go.id/Details/245544/permenkes-no-24-tahun-2022` |
| R-04 | **Permenkes 18/2022** - Penyelenggaraan Satu Data Bidang Kesehatan melalui SIK | Berlaku 20 Sep 2022 | **Dasar hukum sebenarnya** dari SATUSEHAT/interoperabilitas. Wajib disebut sebagai sumber standar FHIR R4, bukan Permenkes 24/2022 | `https://peraturan.bpk.go.id/Details/245539/permenkes-no-18-tahun-2022` |
| R-05 | **Kepmenkes HK.01.07/MENKES/1199/2025** - Formularium Nasional | Berlaku **1 Apr 2026** | FORNAS adalah acuan rule engine obat. **Sebut nomornya**; versi lama (2197/2023) sudah dicabut | `https://jdih.kemenkes.go.id/dokumen/peraturan/kepmenkes_1199_2025.pdf` |
| R-06 | **PP 28/2024** - Pelaksanaan UU 17/2023 | Berlaku 26 Jul 2024 | UU 17/2023 sudah disebut; PP-nya (definisikan Data Kesehatan,/research RS) belum | `https://peraturan.bpk.go.id/Details/294077/pp-no-28-tahun-2024` |
| R-07 | **Perpres 82/2018 jo. Perpres 75/2019, 64/2020, 59/2024** - Jaminan Kesehatan | Berlaku | Kerangka-place JKN: FKTP/FKRTL, kapitasi, dan kerangka Primary Care. Tidak boleh menyebutnya sebagai "BPJS" generik tanpa dasar hukum | `https://peraturan.bpk.go.id/Details/94711/perpres-no-82-tahun-2018` |
| R-08 | **UU 40/2004** - SJSN | Berlaku | Landasan normatif JKN sebagai bagian SJSN; strengthens legitimacy | `https://peraturan.bpk.go.id/Details/40787/uu-no-40-tahun-2004` |
| R-09 | **UU 24/2011** - BPJS Kesehatan | Berlaku | Bodies = partner/penyedia data klaim | `https://peraturan.bpk.go.id/Details/39268/uu-no-24-tahun-2011` |
| R-10 | **PP 71/2019** - SSTE/PSE | Berlaku | obligations PSE: server dalam negeri, aliran data, penghapusan; **berlaku untuk hosting Vercel** | `https://peraturan.bpk.go.id/Details/122030/pp-no-71-tahun-2019` |
| R-11 | **PP 33/2026** - Pelaksanaan UU PDP | Belum berlaku s.d. 15 Jan 2027 | Aturan executing UU PDP; **sudah ditetapkan (15 Jul 2026)**. Proposal harus menyesuaikan diri dengan perubahan regulasi yang akan datang | `https://www.hukumonline.com/pusatdata/detail/lt6a9164bf1e96a/peraturan-pemerintah-nomor-33-tahun-2026/` |
| R-12 | **Permenkes 3/2023** - Standar Tarif | Berlaku 9 Jan 2023 | Acuan "Biaya Rujukan" dan pembuktian klaim financiera | `https://peraturan.bpk.go.id/Details/275518/permenkes-no-3-tahun-2023` |
| R-13 | **Permenkes 6/2026** - Rumah Sakit | Berlaku 12 Jun 2026 | Standar RS terkini yang berlaku terhadap faskes dalam skenario | `https://peraturan.bpk.go.id/Details/350851/permenkes-no-6-tahun-2026` |
| R-14 | **UU 13/2022** (jo. UU 1/2026) | Berlaku | Preskripsi obat & concatener; relevan untuk SYND-04 (drug diversion) | `https://peraturan.bpk.go.id/Details/212810/uu-no-13-tahun-2022` |
| R-15 | **Permenkes 22/2019** - Jabatan Fungsional Asisten Penata Anestesi | Berlaku | Domain kredensial anestesi; memisahkan klaim PCI/CABG sah dari tidak sah | `https://peraturan.bpk.go.id/Details/138615/permenkes-no-22-tahun-2019` |
| R-16 | **Peraturan BPJS 3/2024** - Skrining Riwayat Kesehatan | Berlaku 14 Des 2024 | Regulasi administrasi internal BPJS, memuat mendasarkan integrasi data | `https://peraturan.bpk.go.id/Details/311193/peraturan-bpjs-kesehatan-no-3-tahun-2024` |
| R-17 | **Pasal 34 UU 27/2022** (penilaian dampak) | Berlaku | Wajib untuk pemrosesan data kesehatan berskala besar; **tidak disebut di korpus** | `https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` |
| R-18 | **Permenkes 11/2017** (Keselamatan Pasien) | ⚠️ **TIDAK TERVERIFIKASI** | Hanya relevan bila sistem ikut mendeteksi insiden keselamatan pasien (bukan fokus saat ini). **Status belum dapat dipastikan** - wajib diverifikasi di JDIH Kemenkes sebelum dicantumkan | Tidak ditemukan di `peraturan.bpk.go.id` (akses 22 Okt 2026) |

---

## 8. Rekomendasi

### Prioritas 1 - sebelum submit (hari ini–3)

1. **Perbaiki judul Permenkes 16/2019** di `01-proposal.md:88`, `04-evidence-matrix.md:45`, `11-archive-proposal.md:131,414`, `14-index.md:606,889` menjadi judul resmi lengkap. *(C-01)*
2. **Hapus/ubah klaim "aman menurut Permenkes 24/2022 & UU PDP"** di `10-simulation-dataset.md:3`, `09-draft-hub.md:6,218`, `14-index.md:49,261`. Ganti dengan pernyataan non-kepatuhan yang jujur + rencana DPIA/uji re-identification. *(C-03, §4)*
3. **Perbaiki kutipan pasal UU PDP** di `11-archive-proposal.md:245` (Pasal 4 ayat **2**, bukan 3) dan `12-archive-architecture.md:91` (Pasal **67 & 68**, bukan 65 & 66; 3×24 jam = Pasal **46 ayat (1)**, bukan Pasal 4 ayat (2)). Update juga `dataset_research_live.csv:5` Catatan. *(C-04, C-05)*
4. **Hapus "HL7 FHIR R4" dari `12-archive-architecture.md:69`** dan ganti dengan rujukan **Pasal 10 ayat (4) + Pasal 21 Permenkes 24/2022** dan **Permenkes 18/2022**. Ubah Status item 12 di `dataset_research_live.json` dari "Terverifikasi" menjadi koreksi. *(C-02)*
5. **Perbaiki dua label ICD-9-CM**: `00.66` → "PTCA / coronary atherectomy (tanpa stent)"; `93.90` → "Non-invasive mechanical ventilation (BiPAP)". *(C-06, C-07)*

### Prioritas 2 - sebelum submit (minggu ini)

6. **Perbaiki FORNAS M09** di `09-draft-hub.md:101` dan `10-simulation-dataset.md:98`: insulin glargine **tercantum** (Kepmenkes 1199/2025 §16.2.2, sediaan inj 100 IU/mL, tanda `*` = rujuk balik). *(C-08)*
7. **Tambahkan nomor + versi koding** pada seluruh tabel kode: "ICD-10 Versi 2010 (Permenkes 26/2021)" dan "ICD-9-CM Versi 2010 (Permenkes 26/2021)". Selaraskan label K29.7, S72.0, J18.9, K35.8, K40.9 dengan label Versi 2010. *(C-14, §5.1–5.2)*
8. **Hapus kolom "Biaya Rujukan"** atau tambahkan "Kode Grup Kasus INA-CBG" + "Tarif acuan (Permenkes 3/2023)". *(C-09)*
9. **Turunkan overclaim** di `11-archive-proposal.md:146,185,197`: "kepatuhan absolut" → "kesesuaian rancangan kontrol"; "de-identifikasi penuh" → "pseudonimisasi dengan ancaman yang dikelola"; "Mutlak" → "Tinggi (on-premise, akses terbatas)". *(C-10)*
10. **Perbaiki `13-archive-deep-research.md:3`** - hapus angka "Rp25 miliar, 3 RS swasta 2024" atau beri sumber primer yang dapat dilacak; catatan editorial di `:4` sudah mewajibkan hal ini. *(C-13)*

### Prioritas 3 - sebelum submit (2 minggu)

11. **Tambahkan daftar regulasi minimal** R-01 s.d. R-13 ke `01-proposal.md` §"Referensi dan dokumen pendukung" dan `04-evidence-matrix.md` §5, **lengkap dengan status berlaku, tanggal berlaku, dan tanggal akses** - persis seperti diminta `04-evidence-matrix.md:46`. *(C-11, C-12)*
12. **Tambahkan UU 13/2022 + UU 1/2026** (catatan perubahan criminal), **PP 33/2026** (berlaku 15 Jan 2027 - siapkan transisi kepatuhan), **Permenkes 6/2026**, **Kepmenkes 1199/2025**, **Permenkes 18/2022**, **Permenkes 3/2023**, **UU 40/2004**, **UU 24/2011**, **Perpres 82/2018 s.d. 59/2024**, **PP 71/2019**.
13. **Tambahkan UU PDP Pasal 34** (penilaian dampak pelindungan data) sebagai deliverable Fase 1, dan **Pasal 53** (Migration Officer) sebagai syarat skala besar + data spesifik.
14. **Verifikasi 4 item yang TIDAK TERVERIFIKASI** dari sumber resmi sebelum dicantumkan: (a) status Permenkes 11/2017 di JDIH Kemenkes; (b) identitas Permenkes 33/2024; (c) nomor halaman JDIH BPK untuk PP 33/2026; (d) peraturan yang menetapkan iDRG menggantikan INA-CBG.

### Prioritas 4 - struktural

15. **Tambahkan baris "Interoperabilitas" pada tabel kepatuhan** dengan kolom: Pasal 10(4) PMK 24/2022 → standar SATUSEHAT (Permenkes 18/2022) → HL7 FHIR R4 → resource Claim/Encounter/Condition/Procedure/Invoice. Status: *direncanakan, belum diimplementasikan* (sesuai `02-architecture.md:95`).
16. **Perhatikan PP 71/2019 untuk hosting.** `aegisjkn.vercel.app` berada di luar negeri. Bila demo tetap stateless dan memakai data sintetis tanpa PII, nyatakan eksplisit dalam dokumen; bila ada data peserta, harus ada write-up server-dalam-negeri.
17. **Tambahkan disclaimer tarif-transisi iDRG** pada setiap penyebutan INA-CBG, dengan status "peraturan pengganti penuh: TIDAK TERVERIFIKASI per 22 Okt 2026".

---

## Lampiran A - Daftar URL yang diakses (22 Oktober 2026)

**JDIH BPK (status & metadata):**
`https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022` · `/Details/258028/uu-no-17-tahun-2023` · `/Details/129762/permenkes-no-16-tahun-2019` · `/Details/245544/permenkes-no-24-tahun-2022` · `/Details/353186/permenkes-no-26-tahun-2021` · `/Details/275518/permenkes-no-3-tahun-2023` · `/Details/245539/permenkes-no-18-tahun-2022` · `/Details/138615/permenkes-no-22-tahun-2019` · `/Details/350851/permenkes-no-6-tahun-2026` · `/Details/122030/pp-no-71-tahun-2019` · `/Details/294077/pp-no-28-tahun-2024` · `/Details/39268/uu-no-24-tahun-2011` · `/Details/40787/uu-no-40-tahun-2004` · `/Details/212810/uu-no-13-tahun-2022` · `/Details/94711/perpres-no-82-tahun-2018` · `/Details/136650/perpres-no-64-tahun-2020` · `/Details/285181/perpres-no-59-tahun-2024` · `/Details/311193/peraturan-bpjs-kesehatan-no-3-tahun-2024`

**Dokumen teknis:**
`https://icd.who.int/browse10/2010/en/GetConcept?ConceptId=<kode>` dan `/2016/en/…` (WHO ICD-10 Browser) · `https://perhati-kl.or.id/wp-content/uploads/2017/08/ICD9CM2010.pdf` (CDC ICD-9-CM Procedures FY2010) · `https://jdih.kemkes.go.id/dokumen/peraturan/kepmenkes_1199_2025.pdf` (FORNAS) · `https://satusehat.kemkes.go.id/platform/docs/id/interoperability/klaim-bpjs/` (SATUSEHAT v7.23)

**Sumber sekunder (untuk item yang TIDAK TERVERIFIKASI di BPK):**
`https://www.hukumonline.com/pusatdata/detail/lt6a9164bf1e96a/peraturan-pemerintah-nomor-33-tahun-2026/` · `https://www.hukumonline.com/berita/a/pelindungan-data-pribadi-dalam-penegakan-hukum-dan-konfigurasi-berantara-di-bawah-pp-33-2026-lt6ac4acd9db1bd/` · `https://www.cnbcindonesia.com/tech/20260916115609-37-768328/lembaga-perlindungan-data-belum-ada-di-ri-padahal-aturannya-sudah-ada`

**Tidak dapat diakses:** `https://jdih.kemenkes.go.id/` - DNS gagal (ENOTFOUND / getaddrinfo failed) dari lingkungan audit 22 Okt 2026; naskah PDF yang dipakai dalam audit ini telah diunduh sebelumnya dan diverifikasi terhadap nomor dokumen. `https://peraturan.go.id/id/permenkes-no-11-tahun-2017` - HTTP 404.

## Lampiran B - Metodologi & batasan

- Pencarian internet **hanya** melalui MCP SearXNG (`mcp__searxng__searxng_web_search`, `mcp__searxng__web_url_read`), sesuai aturan proyek. Primary `http://localhost:8088`, failover `http://192.168.101.19:8089` (terpakai pada 22 Okt 2026).
- Verifikasi isi naskah dilakukan terhadap **PDF penuh** dari JDIH Kemenkes (Permenkes 16/2019, 24/2022, 26/2021, 18/2022, Kepmenkes 1199/2025) dan terhadap **naskah UU PDP / PP 71/2019 / PP 28/2024** yang telah diekstrak ke teks, dengan pencacahan string literal ("HL7" = 0, "FHIR" = 0, "SATUSEHAT" = 0 pada Permenkes 24/2022).
- Kode ICD-10 diverifikasi per-kode pada WHO ICD-10 Browser (versi 2010 dan 2016). Kode ICD-9-CM diverifikasi pada **CDC FY2010 listing** (versi yang diwajibkan Permenkes 26/2021).
- **Batasan:** corpus arsip (`11-`, `12-`, `13-`, `14-`) bersifat historis dan sebagian besar **tidak dipakai** dalam proposal revisi 1.0; temuan pada arsip dilaporkan karena (a) `14-index.md` mengindeks arsip sebagai dokumen aktif, (b) `dataset_research_live.json`ii masih memuat klaim yang salah sebagai "Terverifikasi". Perbedaan severity proposal-inti vs arsip sudah dicerminkan di tabel severity.
- **Batasan 2:** `03-dataset-registry.md` bertanggal 21 Oktober 2026 dan `claims_v2_live.csv` berisi 300 baris - konsistensi angka tidak menjadi objek audit ini (dikerjakan oleh audit terpisah).
