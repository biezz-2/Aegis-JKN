# Skema Data Klaim Sintetis Aegis-JKN

## Status dan sumber kebenaran

Dokumen ini mendeskripsikan file kanonik `docs/datasets/klaim-aegis-jkn-dataset.json`, bukan klaim tentang skema yang direncanakan pada dokumen lain. File tersebut adalah array JSON dengan **300** record (`KLM001` sampai `KLM300`) dan SHA-256:

```text
2b8c4113da2dd742075282865b9075eb14061a8eea81a2f3da0035cbbae79d9a
```

Dataset adalah **simulasi sintetis dan pseudonymized**. Ia bukan data peserta JKN riil, bukan evidence klinis, dan tidak dapat digunakan untuk menyatakan validitas model produksi. Dashboard menampilkan label/skor yang telah tersedia dalam file sebagai bukti demonstrasi, tanpa melakukan retraining atau inferensi.

## Invarian file

| Invarian | Nilai |
|---|---|
| Struktur root | Array JSON |
| Jumlah record | 300 |
| Jumlah field tiap record | 28 |
| Rentang tanggal | `2026-01-01`–`2026-06-27` |
| Skor fraud | `0.04`–`0.95` |
| Nilai klaim total | Rp3.526.650.000 |
| File dashboard copy | `dashboard/src/data/klaim-aegis-jkn-dataset.json` |

## Field aktual

| Field sumber | Tipe | Contoh | Makna / tujuan UI |
|---|---|---|---|
| `Name` | string | `KLM001` | ID klaim; menjadi `Claim.id`. |
| `Tanggal` | string ISO date | `2026-02-16` | Tanggal layanan. |
| `Status` | enum string | `escalate` | Rekomendasi sistem sintetis, bukan tindakan yang telah dieksekusi. |
| `Risiko` | enum string | `fraud` | Tingkat risiko dataset. |
| `Skor Fraud` | number | `0.94` | Skor yang telah diprakomputasi. |
| `Modus` | string, dapat kosong | `upcoding` | Modus indikatif; kosong menjadi `undefined` di view model. |
| `Sindikat` | string, dapat kosong | `SYND-01` | Label sindikat sintetis; kosong menjadi `undefined`. |
| `Faskes` | string | `RS_A` | Fasilitas kesehatan sintetis. |
| `Layanan` | enum string | `rawat inap` | Jenis layanan. |
| `Pasien` | string | `P01 (Agus Raharjo)` | Display pseudonym; prefiks ID boleh diekstrak untuk UI. |
| `Dokter` | string | `D01 (dr. Adnan Prakoso, Sp.BTKV)` | Display pseudonym; prefiks ID boleh diekstrak untuk UI. |
| `Diagnosis ICD-10` | string | `K29.7 - Gastritis, tanpa perdarahan` | Diagnosis / chip ICD-10. |
| `Prosedur ICD-9-CM` | string | `00.66 - Angioplasti koroner + stent (PCI)` | Prosedur / chip ICD-9-CM; `—` berarti tidak tersedia. |
| `Biaya Rp` | integer | `52300000` | Nilai klaim. Dataset tidak memuat tarif INA-CBG pembanding. |
| `LOS hari` | integer | `2` | Lama rawat. |
| `Obat` | string | `M04 x 3 vial; M08 x 10 tablet` | Bukti obat tekstual. |
| `Rujukan` | string | `Puskesmas … · RJ-2026-300 · 2026-02-15` | Bukti rujukan tekstual. |
| `Alasan Berobat` | string | `Nyeri ulu hati…` | Keluhan/alasan kunjungan. |
| `Narasi Rekam Medis` | string | `Pasien nyeri epigastrium…` | Resume klinis naratif. |
| `Kontradiksi Narasi` | boolean | `true` | Flag bukti kontradiksi. |
| `Umpan Balik Pasien` | string | `Saya hanya periksa lambung…` | Umpan balik sintetis. |
| `Sentimen` | enum string | `negatif` | Sentimen umpan balik. |
| `Skor Sentimen` | number | `-0.75` | Skor sentimen yang tersedia. |
| `Sinyal SHAP` | string | `inkonsistensi …; biaya …` | Evidence naratif, **bukan** atribuisi SHAP numerik per fitur. |
| `Kontribusi Saluran` | string | `T 0.31 · F 0.32 · S 0.31` | Kontribusi tiga saluran; diparse defensif menjadi topology/feature/semantic. |
| `Alasan` | string | `FRAUD (Upcoding): …` | Penjelasan sintetis. `KLM031` kosong. |
| `Catatan` | string | `Dx primer gastritis…` | Catatan tambahan; boleh kosong. |
| `Notion ID` | string | UUID Notion | Provenance; tidak ditampilkan sebagai identitas utama. |

## Domain enum dan distribusi teramati

| Field | Nilai teramati | Distribusi |
|---|---|---|
| `Risiko` | `low`, `medium`, `high`, `fraud` | 240 / 10 / 14 / 36 |
| `Status` | `auto_clear`, `review`, `escalate` | 240 / 24 / 36 |
| `Layanan` | `rawat inap`, `rawat jalan` | 189 / 111 |
| `Sentimen` | `positif`, `netral`, `negatif` | 170 / 58 / 72 |
| `Kontradiksi Narasi` | `true`, `false` | 12 / 288 |
| `Sindikat` | kosong, `SYND-01`–`SYND-09` | kosong 264; sisanya 36 |

`Faskes` memiliki sepuluh nilai `RS_A`–`RS_J`. `Modus` dapat kosong; nilai non-kosong mencakup `upcoding`, `phantom_billing`, `unbundling`, `repeat_billing`, `cloning`, dan modus investigatif lain.

## Aturan parsing dashboard

1. `Pasien` serta `Dokter` disimpan apa adanya untuk display; ekspresi `ID (nama)` dapat memberi `pseudonymId`, tanpa mengklaim sebagai ID produksi.
2. Diagnosis/prosedur dipecah hanya pada delimiter ` - `. Bila prosedur bernilai `—`, view model bernilai absent.
3. `Kontribusi Saluran` valid bila cocok dengan `T <angka> · F <angka> · S <angka>`. Ketiga nilai tidak diasumsikan berjumlah 1; total teramati berada pada 0,04–0,94.
4. `Sinyal SHAP` bernilai `tidak ada sinyal dominan` pada 240 record. Pada 60 record lainnya, UI hanya membagi klausa berdasarkan titik koma untuk keterbacaan. UI tidak membuat bar SHAP signed/numerik dari prosa ini.
5. Node dan edge tampilan sindikat boleh diturunkan dari klaim yang memiliki label `Sindikat` sama. Tampilan tersebut harus dilabeli sebagai representasi kelompok dataset sintetis, bukan graph discovery.
6. Badge UI diturunkan dengan urutan: `Syndicate` jika ada sindikat, lalu `Escalate`, `Review`, atau `Safe` menurut `Status`.

## Deviasi terhadap dokumen lama dan brief

Data aktual menang atas deskripsi yang tidak sinkron. File ini tidak memiliki `pasien_id`, `faskes_id`, `dokter_id`, `seed`, `version`, `timestamp`, daftar edge, `HeteroData`, artefak leakage blocklist, atau SHAP numerik terstruktur. Karena itu, dashboard tidak boleh mengarang perbandingan tarif INA-CBG, delta biaya, graph edge produksi, atau feature SHAP numeric.

Dokumentasi lama juga menyebut 100 klaim/v2.1 pada beberapa bagian, sedangkan file kanonik berisi 300 record. `KLM115` berisiko `fraud` pada skor 0,80; ini berbeda dari aturan naratif lama yang menyatakan fraud harus lebih besar dari 0,80. Dataset memuat 12, bukan 8, flag kontradiksi narasi.

## Perubahan dataset yang disengaja

Jika file sumber diganti dengan persetujuan pemilik data, jalankan audit ulang pada seluruh file, perbarui checksum/invarian/dokumentasi ini, jalankan test integritas, lalu perbarui salinan dashboard secara byte-identik. Jangan memperbarui hash untuk menutupi perubahan yang tidak diaudit.
