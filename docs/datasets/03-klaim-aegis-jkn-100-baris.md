# Klaim Aegis-JKN — Dataset Lengkap (300 Baris Klaim Sintetis)

> **Sumber Notion Database:** [Klaim Aegis-JKN](https://app.notion.com/p/c783afb3d0d4458295456180b7b7756b)  
> **Database ID:** `c783afb3-d0d4-4582-9545-6180b7b7756b`  
> **Total Klaim:** 300 baris klaim sintetis tervalidasi klinis  
> **Format Data Mentah:** [JSON (300 Baris)](./klaim-aegis-jkn-dataset.json) | [CSV (300 Baris)](./klaim-aegis-jkn-dataset.csv)  
> **Total Akumulasi Biaya Klaim:** Rp3,526,650,000

*Catatan: Pada tampilan awal Notion tertera label "Klaim Aegis-JKN (100 Baris)", namun melalui pagination API Notion lengkap, seluruh dataset berjumlah **300 baris klaim** (portofolio komprehensif yang digunakan untuk pengujian empiris proposal Aegis-JKN).*

---

## 1. Analisis Ringkasan Dataset

### Distribusi Risiko
| Tingkat Risiko | Jumlah Klaim | Persentase | Interpretasi Tindakan |
|---|---|---|---|
| 🟢 Low | 240 | 80.0% | Auto-clear (Lolos otomatis) |
| 🟡 Medium | 10 | 3.3% | Human-in-the-Loop Review |
| 🟠 High | 14 | 4.7% | Prioritas Investigasi Verifikator |
| 🔴 Fraud | 36 | 12.0% | Flagging Kritis & Eskalasi Tim PK-JKN |

### Distribusi Status Klaim
| Status Tindakan | Jumlah Klaim |
|---|---|
| `auto_clear` | 240 |
| `escalate` | 36 |
| `review` | 24 |

### Distribusi Modus Kecurangan Terdeteksi
| Modus Indikasi | Jumlah Klaim | Estimasi Potensi Overcharge |
|---|---|---|
| Normal / Non-fraud | 240 | Rp2,685,550,000 |
| anomali_frekuensi | 12 | Rp15,800,000 |
| unbundling | 6 | Rp52,800,000 |
| readmission_berulang | 6 | Rp25,290,000 |
| excessive_usage | 6 | Rp12,900,000 |
| upcoding | 5 | Rp212,800,000 |
| prolonged_stay | 4 | Rp127,400,000 |
| overbilling | 4 | Rp65,950,000 |
| repeat_billing | 4 | Rp61,600,000 |
| iur_biaya | 4 | Rp63,880,000 |
| phantom_billing | 3 | Rp134,250,000 |
| drug_diversion | 3 | Rp26,030,000 |
| cloning | 2 | Rp14,900,000 |
| biaya_markup | 1 | Rp27,500,000 |

---

## 2. Tabel Rekapitulasi 300 Baris Klaim

| ID | Tgl | Faskes | Layanan | Pasien | Dokter | Dx ICD-10 | Prosedur | Biaya (Rp) | Skor | Risiko | Status | Modus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **KLM001** | 2026-02-16 | RS_A | rawat inap | P01 (Agus Raharjo) | D01 (dr. Adnan Prakoso, Sp.BTKV) | K29.7 | 00.66 | 52,300,000 | 0.94 | fraud | `escalate` | upcoding |
| **KLM002** | 2026-02-17 | RS_A | rawat inap | P02 (Bunga Lestari) | D02 (dr. Barli Soemarno, Sp.B) | K29.7 | 00.66 | 52,300,000 | 0.95 | fraud | `escalate` | upcoding |
| **KLM003** | 2026-02-18 | RS_A | rawat inap | P03 (Candra Wijaya) | D01 (dr. Adnan Prakoso, Sp.BTKV) | K29.7 | 00.66 | 52,300,000 | 0.93 | fraud | `escalate` | upcoding |
| **KLM004** | 2026-03-12 | RS_C | rawat inap | P08 (Maryam Yusuf) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 44,750,000 | 0.92 | fraud | `escalate` | phantom_billing |
| **KLM005** | 2026-03-12 | RS_C | rawat inap | P09 (Idrus Hakim) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 44,750,000 | 0.94 | fraud | `escalate` | phantom_billing |
| **KLM006** | 2026-03-12 | RS_C | rawat inap | P10 (Kartini Ibrahim) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 44,750,000 | 0.93 | fraud | `escalate` | phantom_billing |
| **KLM007** | 2026-04-18 | RS_B | rawat inap | P12 (Maya Sari) | D07 (dr. Gunawan Halim, Sp.B) | K80.2 | 51.23 | 15,500,000 | 0.85 | fraud | `escalate` | unbundling |
| **KLM008** | 2026-04-18 | RS_B | rawat inap | P12 (Maya Sari) | D07 (dr. Gunawan Halim, Sp.B) | K80.2 | 96.04 | 2,100,000 | 0.85 | fraud | `escalate` | unbundling |
| **KLM009** | 2026-04-19 | RS_B | rawat inap | P13 (Nadia Rahmawati) | D07 (dr. Gunawan Halim, Sp.B) | K80.2 | 51.23 | 15,500,000 | 0.86 | fraud | `escalate` | unbundling |
| **KLM010** | 2026-04-19 | RS_B | rawat inap | P13 (Nadia Rahmawati) | D07 (dr. Gunawan Halim, Sp.B) | K80.2 | 96.04 | 2,100,000 | 0.86 | fraud | `escalate` | unbundling |
| **KLM011** | 2026-04-20 | RS_B | rawat inap | P14 (Odi Setiawan) | D07 (dr. Gunawan Halim, Sp.B) | K80.2 | 51.23 | 15,500,000 | 0.87 | fraud | `escalate` | unbundling |
| **KLM012** | 2026-04-20 | RS_B | rawat inap | P14 (Odi Setiawan) | D07 (dr. Gunawan Halim, Sp.B) | K80.2 | 96.04 | 2,100,000 | 0.87 | fraud | `escalate` | unbundling |
| **KLM013** | 2026-05-04 | RS_E | rawat jalan | P16 (Ratna Dewi) | D09 (dr. Indah Pratiwi, Sp.PD) | E11.9 | — | 9,450,000 | 0.88 | fraud | `escalate` | drug_diversion |
| **KLM014** | 2026-05-11 | RS_E | rawat jalan | P17 (Slamet Riyadi) | D09 (dr. Indah Pratiwi, Sp.PD) | E11.9 | — | 7,680,000 | 0.86 | fraud | `escalate` | drug_diversion |
| **KLM015** | 2026-01-22 | RS_A | rawat inap | P18 (Tarmizi Karim) | D03 (dr. Citra Ayuningtyas, Sp.PD) | J18.9 | — | 8,900,000 | 0.74 | high | `review` | prolonged_stay |
| **KLM016** | 2026-05-06 | RS_F | rawat inap | P19 (Umi Kalsum) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 7,450,000 | 0.78 | high | `review` | cloning |
| **KLM017** | 2026-05-06 | RS_F | rawat inap | P20 (Wahyu Nugraha) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 7,450,000 | 0.79 | high | `review` | cloning |
| **KLM018** | 2026-03-27 | RS_D | rawat inap | P11 (Lukman Sutrisno) | D04 (dr. Danur Wibisono, Sp.JP) | E11.9 | 00.66 | 49,700,000 | 0.68 | high | `review` | upcoding |
| **KLM019** | 2026-02-08 | RS_D | rawat inap | P07 (Gilang Saputra) | D11 (dr. Kartika Sari, Sp.B) | K35.8 | 47.09 | 38,000,000 | 0.62 | high | `review` | overbilling |
| **KLM020** | 2026-01-05 | RS_E | rawat jalan | P15 (Purnama Sidik) | D09 (dr. Indah Pratiwi, Sp.PD) | E11.9 | — | 1,150,000 | 0.45 | medium | `review` | anomali_frekuensi |
| **KLM021** | 2026-01-12 | RS_E | rawat jalan | P15 (Purnama Sidik) | D09 (dr. Indah Pratiwi, Sp.PD) | E11.9 | — | 1,150,000 | 0.48 | medium | `review` | anomali_frekuensi |
| **KLM022** | 2026-01-19 | RS_E | rawat jalan | P15 (Purnama Sidik) | D09 (dr. Indah Pratiwi, Sp.PD) | E11.9 | — | 1,150,000 | 0.51 | medium | `review` | anomali_frekuensi |
| **KLM023** | 2026-01-26 | RS_E | rawat jalan | P15 (Purnama Sidik) | D09 (dr. Indah Pratiwi, Sp.PD) | E11.9 | — | 1,150,000 | 0.53 | medium | `review` | anomali_frekuensi |
| **KLM024** | 2026-04-11 | RS_F | rawat inap | P05 (Eka Putri) | D12 (dr. Lina Marlina, Sp.OG) | O80 | 74.1 | 6,200,000 | 0.66 | high | `review` | upcoding |
| **KLM025** | 2026-01-01 | RS_F | rawat inap | P01 (Agus Raharjo) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 6,100,000 | 0.04 | low | `auto_clear` | - |
| **KLM026** | 2026-02-12 | RS_F | rawat inap | P04 (Dewi Anggraeni) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 8,250,000 | 0.11 | low | `auto_clear` | - |
| **KLM027** | 2026-03-23 | RS_D | rawat inap | P07 (Gilang Saputra) | D04 (dr. Danur Wibisono, Sp.JP) | I21.9 | 00.66 | 53,100,000 | 0.09 | low | `auto_clear` | - |
| **KLM028** | 2026-04-07 | RS_E | rawat inap | P10 (Kartini Ibrahim) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 4,300,000 | 0.06 | low | `auto_clear` | - |
| **KLM029** | 2026-05-18 | RS_A | rawat jalan | P13 (Nadia Rahmawati) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,050,000 | 0.14 | low | `auto_clear` | - |
| **KLM030** | 2026-06-02 | RS_E | rawat inap | P16 (Ratna Dewi) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 5,800,000 | 0.11 | low | `auto_clear` | - |
| **KLM031** | 2026-01-13 | RS_C | rawat inap | P19 (Umi Kalsum) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 44,000,000 | 0.08 | low | `auto_clear` | - |
| **KLM032** | 2026-02-24 | RS_F | rawat inap | P02 (Bunga Lestari) | D12 (dr. Lina Marlina, Sp.OG) | O80 | — | 4,100,000 | 0.06 | low | `auto_clear` | - |
| **KLM033** | 2026-03-08 | RS_A | rawat inap | P05 (Eka Putri) | D02 (dr. Barli Soemarno, Sp.B) | K80.2 | 51.23 | 13,950,000 | 0.13 | low | `auto_clear` | - |
| **KLM034** | 2026-04-19 | RS_B | rawat jalan | P08 (Maryam Yusuf) | D07 (dr. Gunawan Halim, Sp.B) | K29.7 | — | 800,000 | 0.11 | low | `auto_clear` | - |
| **KLM035** | 2026-05-03 | RS_F | rawat inap | P11 (Lukman Sutrisno) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 6,650,000 | 0.08 | low | `auto_clear` | - |
| **KLM036** | 2026-06-14 | RS_F | rawat inap | P14 (Odi Setiawan) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 8,900,000 | 0.05 | low | `auto_clear` | - |
| **KLM037** | 2026-01-25 | RS_D | rawat inap | P17 (Slamet Riyadi) | D04 (dr. Danur Wibisono, Sp.JP) | I21.9 | 00.66 | 57,550,000 | 0.13 | low | `auto_clear` | - |
| **KLM038** | 2026-02-09 | RS_E | rawat inap | P20 (Wahyu Nugraha) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 3,800,000 | 0.10 | low | `auto_clear` | - |
| **KLM039** | 2026-03-20 | RS_A | rawat jalan | P03 (Candra Wijaya) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,150,000 | 0.07 | low | `auto_clear` | - |
| **KLM040** | 2026-04-04 | RS_E | rawat inap | P06 (Fajar Nugroho) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 5,150,000 | 0.05 | low | `auto_clear` | - |
| **KLM041** | 2026-05-15 | RS_C | rawat inap | P09 (Idrus Hakim) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 47,550,000 | 0.12 | low | `auto_clear` | - |
| **KLM042** | 2026-06-26 | RS_F | rawat inap | P12 (Maya Sari) | D12 (dr. Lina Marlina, Sp.OG) | O80 | — | 3,650,000 | 0.10 | low | `auto_clear` | - |
| **KLM043** | 2026-01-10 | RS_A | rawat inap | P15 (Purnama Sidik) | D02 (dr. Barli Soemarno, Sp.B) | K80.2 | 51.23 | 15,050,000 | 0.07 | low | `auto_clear` | - |
| **KLM044** | 2026-02-21 | RS_B | rawat jalan | P18 (Tarmizi Karim) | D07 (dr. Gunawan Halim, Sp.B) | K29.7 | — | 700,000 | 0.04 | low | `auto_clear` | - |
| **KLM045** | 2026-03-05 | RS_F | rawat inap | P01 (Agus Raharjo) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 7,150,000 | 0.12 | low | `auto_clear` | - |
| **KLM046** | 2026-04-16 | RS_F | rawat inap | P04 (Dewi Anggraeni) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 7,900,000 | 0.09 | low | `auto_clear` | - |
| **KLM047** | 2026-05-27 | RS_D | rawat inap | P07 (Gilang Saputra) | D04 (dr. Danur Wibisono, Sp.JP) | I21.9 | 00.66 | 62,000,000 | 0.07 | low | `auto_clear` | - |
| **KLM048** | 2026-06-11 | RS_E | rawat inap | P10 (Kartini Ibrahim) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 4,100,000 | 0.04 | low | `auto_clear` | - |
| **KLM049** | 2026-01-22 | RS_A | rawat jalan | P13 (Nadia Rahmawati) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,250,000 | 0.11 | low | `auto_clear` | - |
| **KLM050** | 2026-02-06 | RS_E | rawat inap | P16 (Ratna Dewi) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 5,550,000 | 0.09 | low | `auto_clear` | - |
| **KLM051** | 2026-03-17 | RS_C | rawat inap | P19 (Umi Kalsum) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 41,850,000 | 0.06 | low | `auto_clear` | - |
| **KLM052** | 2026-04-01 | RS_F | rawat inap | P02 (Bunga Lestari) | D12 (dr. Lina Marlina, Sp.OG) | O80 | — | 3,950,000 | 0.14 | low | `auto_clear` | - |
| **KLM053** | 2026-05-12 | RS_A | rawat inap | P05 (Eka Putri) | D02 (dr. Barli Soemarno, Sp.B) | K80.2 | 51.23 | 13,250,000 | 0.11 | low | `auto_clear` | - |
| **KLM054** | 2026-06-23 | RS_B | rawat jalan | P08 (Maryam Yusuf) | D07 (dr. Gunawan Halim, Sp.B) | K29.7 | — | 750,000 | 0.08 | low | `auto_clear` | - |
| **KLM055** | 2026-01-07 | RS_F | rawat inap | P11 (Lukman Sutrisno) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 6,350,000 | 0.06 | low | `auto_clear` | - |
| **KLM056** | 2026-02-18 | RS_F | rawat inap | P14 (Odi Setiawan) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 8,500,000 | 0.13 | low | `auto_clear` | - |
| **KLM057** | 2026-03-02 | RS_D | rawat inap | P17 (Slamet Riyadi) | D04 (dr. Danur Wibisono, Sp.JP) | I21.9 | 00.66 | 54,900,000 | 0.11 | low | `auto_clear` | - |
| **KLM058** | 2026-04-13 | RS_E | rawat inap | P20 (Wahyu Nugraha) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 4,450,000 | 0.08 | low | `auto_clear` | - |
| **KLM059** | 2026-05-24 | RS_A | rawat jalan | P03 (Candra Wijaya) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,100,000 | 0.05 | low | `auto_clear` | - |
| **KLM060** | 2026-06-08 | RS_E | rawat inap | P06 (Fajar Nugroho) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 6,000,000 | 0.13 | low | `auto_clear` | - |
| **KLM061** | 2026-01-19 | RS_C | rawat inap | P09 (Idrus Hakim) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 45,450,000 | 0.10 | low | `auto_clear` | - |
| **KLM062** | 2026-02-03 | RS_F | rawat inap | P12 (Maya Sari) | D12 (dr. Lina Marlina, Sp.OG) | O80 | — | 4,250,000 | 0.07 | low | `auto_clear` | - |
| **KLM063** | 2026-03-14 | RS_A | rawat inap | P15 (Purnama Sidik) | D02 (dr. Barli Soemarno, Sp.B) | K80.2 | 51.23 | 14,400,000 | 0.05 | low | `auto_clear` | - |
| **KLM064** | 2026-04-25 | RS_B | rawat jalan | P18 (Tarmizi Karim) | D07 (dr. Gunawan Halim, Sp.B) | K29.7 | — | 700,000 | 0.12 | low | `auto_clear` | - |
| **KLM065** | 2026-05-09 | RS_F | rawat inap | P01 (Agus Raharjo) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 6,850,000 | 0.10 | low | `auto_clear` | - |
| **KLM066** | 2026-06-20 | RS_F | rawat inap | P04 (Dewi Anggraeni) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 7,500,000 | 0.07 | low | `auto_clear` | - |
| **KLM067** | 2026-01-04 | RS_D | rawat inap | P07 (Gilang Saputra) | D04 (dr. Danur Wibisono, Sp.JP) | I21.9 | 00.66 | 59,350,000 | 0.04 | low | `auto_clear` | - |
| **KLM068** | 2026-02-15 | RS_E | rawat inap | P10 (Kartini Ibrahim) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 3,900,000 | 0.12 | low | `auto_clear` | - |
| **KLM069** | 2026-03-26 | RS_A | rawat jalan | P13 (Nadia Rahmawati) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,200,000 | 0.09 | low | `auto_clear` | - |
| **KLM070** | 2026-04-10 | RS_E | rawat inap | P16 (Ratna Dewi) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 5,300,000 | 0.07 | low | `auto_clear` | - |
| **KLM071** | 2026-05-21 | RS_C | rawat inap | P19 (Umi Kalsum) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 49,000,000 | 0.04 | low | `auto_clear` | - |
| **KLM072** | 2026-06-05 | RS_F | rawat inap | P02 (Bunga Lestari) | D12 (dr. Lina Marlina, Sp.OG) | O80 | — | 3,750,000 | 0.11 | low | `auto_clear` | - |
| **KLM073** | 2026-01-16 | RS_A | rawat inap | P05 (Eka Putri) | D02 (dr. Barli Soemarno, Sp.B) | K80.2 | 51.23 | 15,500,000 | 0.09 | low | `auto_clear` | - |
| **KLM074** | 2026-02-27 | RS_B | rawat jalan | P08 (Maryam Yusuf) | D07 (dr. Gunawan Halim, Sp.B) | K29.7 | — | 750,000 | 0.06 | low | `auto_clear` | - |
| **KLM075** | 2026-03-11 | RS_F | rawat inap | P11 (Lukman Sutrisno) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 7,400,000 | 0.14 | low | `auto_clear` | - |
| **KLM076** | 2026-04-22 | RS_F | rawat inap | P14 (Odi Setiawan) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 8,150,000 | 0.11 | low | `auto_clear` | - |
| **KLM077** | 2026-05-06 | RS_D | rawat inap | P17 (Slamet Riyadi) | D04 (dr. Danur Wibisono, Sp.JP) | I21.9 | 00.66 | 52,200,000 | 0.08 | low | `auto_clear` | - |
| **KLM078** | 2026-06-17 | RS_E | rawat inap | P20 (Wahyu Nugraha) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 4,250,000 | 0.06 | low | `auto_clear` | - |
| **KLM079** | 2026-01-01 | RS_A | rawat jalan | P03 (Candra Wijaya) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,050,000 | 0.13 | low | `auto_clear` | - |
| **KLM080** | 2026-02-12 | RS_E | rawat inap | P06 (Fajar Nugroho) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 5,750,000 | 0.11 | low | `auto_clear` | - |
| **KLM081** | 2026-03-23 | RS_C | rawat inap | P09 (Idrus Hakim) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 43,300,000 | 0.08 | low | `auto_clear` | - |
| **KLM082** | 2026-04-07 | RS_F | rawat inap | P12 (Maya Sari) | D12 (dr. Lina Marlina, Sp.OG) | O80 | — | 4,050,000 | 0.05 | low | `auto_clear` | - |
| **KLM083** | 2026-05-18 | RS_A | rawat inap | P15 (Purnama Sidik) | D02 (dr. Barli Soemarno, Sp.B) | K80.2 | 51.23 | 13,700,000 | 0.13 | low | `auto_clear` | - |
| **KLM084** | 2026-06-02 | RS_B | rawat jalan | P18 (Tarmizi Karim) | D07 (dr. Gunawan Halim, Sp.B) | K29.7 | — | 800,000 | 0.10 | low | `auto_clear` | - |
| **KLM085** | 2026-01-13 | RS_F | rawat inap | P01 (Agus Raharjo) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 6,550,000 | 0.07 | low | `auto_clear` | - |
| **KLM086** | 2026-02-24 | RS_F | rawat inap | P04 (Dewi Anggraeni) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 8,750,000 | 0.05 | low | `auto_clear` | - |
| **KLM087** | 2026-03-08 | RS_D | rawat inap | P07 (Gilang Saputra) | D04 (dr. Danur Wibisono, Sp.JP) | I21.9 | 00.66 | 56,650,000 | 0.12 | low | `auto_clear` | - |
| **KLM088** | 2026-04-19 | RS_E | rawat inap | P10 (Kartini Ibrahim) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 4,550,000 | 0.10 | low | `auto_clear` | - |
| **KLM089** | 2026-05-03 | RS_A | rawat jalan | P13 (Nadia Rahmawati) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,150,000 | 0.07 | low | `auto_clear` | - |
| **KLM090** | 2026-06-14 | RS_E | rawat inap | P16 (Ratna Dewi) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 5,050,000 | 0.04 | low | `auto_clear` | - |
| **KLM091** | 2026-01-25 | RS_C | rawat inap | P19 (Umi Kalsum) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 46,850,000 | 0.12 | low | `auto_clear` | - |
| **KLM092** | 2026-02-09 | RS_F | rawat inap | P02 (Bunga Lestari) | D12 (dr. Lina Marlina, Sp.OG) | O80 | — | 3,550,000 | 0.09 | low | `auto_clear` | - |
| **KLM093** | 2026-03-20 | RS_A | rawat inap | P05 (Eka Putri) | D02 (dr. Barli Soemarno, Sp.B) | K80.2 | 51.23 | 14,850,000 | 0.07 | low | `auto_clear` | - |
| **KLM094** | 2026-04-04 | RS_B | rawat jalan | P08 (Maryam Yusuf) | D07 (dr. Gunawan Halim, Sp.B) | K29.7 | — | 700,000 | 0.04 | low | `auto_clear` | - |
| **KLM095** | 2026-05-15 | RS_F | rawat inap | P11 (Lukman Sutrisno) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 7,050,000 | 0.11 | low | `auto_clear` | - |
| **KLM096** | 2026-06-26 | RS_F | rawat inap | P14 (Odi Setiawan) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 7,750,000 | 0.09 | low | `auto_clear` | - |
| **KLM097** | 2026-01-10 | RS_D | rawat inap | P17 (Slamet Riyadi) | D04 (dr. Danur Wibisono, Sp.JP) | I21.9 | 00.66 | 61,100,000 | 0.06 | low | `auto_clear` | - |
| **KLM098** | 2026-02-21 | RS_E | rawat inap | P20 (Wahyu Nugraha) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 4,050,000 | 0.14 | low | `auto_clear` | - |
| **KLM099** | 2026-03-05 | RS_A | rawat jalan | P03 (Candra Wijaya) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,250,000 | 0.11 | low | `auto_clear` | - |
| **KLM100** | 2026-04-16 | RS_E | rawat inap | P06 (Fajar Nugroho) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 5,450,000 | 0.08 | low | `auto_clear` | - |
| **KLM101** | 2026-03-09 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 15,400,000 | 0.92 | fraud | `escalate` | repeat_billing |
| **KLM102** | 2026-03-09 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 15,400,000 | 0.91 | fraud | `escalate` | repeat_billing |
| **KLM103** | 2026-03-10 | RS_G | rawat inap | P22 (Sri Wahyuni) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 15,400,000 | 0.90 | fraud | `escalate` | repeat_billing |
| **KLM104** | 2026-03-10 | RS_G | rawat inap | P22 (Sri Wahyuni) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 15,400,000 | 0.89 | fraud | `escalate` | repeat_billing |
| **KLM105** | 2026-02-20 | RS_H | rawat inap | P23 (Tono Sugiarto) | D14 (dr. Nurul Aini, Sp.PD) | I21.9 | 00.66 | 57,400,000 | 0.84 | fraud | `escalate` | iur_biaya |
| **KLM106** | 2026-03-20 | RS_H | rawat jalan | P23 (Tono Sugiarto) | D14 (dr. Nurul Aini, Sp.PD) | E11.9 | — | 1,150,000 | 0.82 | fraud | `escalate` | iur_biaya |
| **KLM107** | 2026-04-02 | RS_H | rawat inap | P24 (Umi Rahayu) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 4,350,000 | 0.85 | fraud | `escalate` | iur_biaya |
| **KLM108** | 2026-05-07 | RS_H | rawat jalan | P24 (Umi Rahayu) | D14 (dr. Nurul Aini, Sp.PD) | I10 | — | 980,000 | 0.83 | fraud | `escalate` | iur_biaya |
| **KLM109** | 2026-01-08 | RS_I | rawat inap | P25 (Wawan Setiawan) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,150,000 | 0.86 | fraud | `escalate` | readmission_berulang |
| **KLM110** | 2026-01-16 | RS_I | rawat inap | P25 (Wawan Setiawan) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,150,000 | 0.87 | fraud | `escalate` | readmission_berulang |
| **KLM111** | 2026-01-23 | RS_I | rawat inap | P25 (Wawan Setiawan) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,150,000 | 0.89 | fraud | `escalate` | readmission_berulang |
| **KLM112** | 2026-03-04 | RS_I | rawat inap | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,280,000 | 0.86 | fraud | `escalate` | readmission_berulang |
| **KLM113** | 2026-03-12 | RS_I | rawat inap | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,280,000 | 0.88 | fraud | `escalate` | readmission_berulang |
| **KLM114** | 2026-03-19 | RS_I | rawat inap | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,280,000 | 0.88 | fraud | `escalate` | readmission_berulang |
| **KLM115** | 2026-02-02 | RS_J | rawat jalan | P27 (Zainal Abidin) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 2,150,000 | 0.80 | fraud | `escalate` | excessive_usage |
| **KLM116** | 2026-02-09 | RS_J | rawat jalan | P27 (Zainal Abidin) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 2,150,000 | 0.81 | fraud | `escalate` | excessive_usage |
| **KLM117** | 2026-02-16 | RS_J | rawat jalan | P27 (Zainal Abidin) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 2,150,000 | 0.82 | fraud | `escalate` | excessive_usage |
| **KLM118** | 2026-02-23 | RS_J | rawat jalan | P27 (Zainal Abidin) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 2,150,000 | 0.83 | fraud | `escalate` | excessive_usage |
| **KLM119** | 2026-03-02 | RS_J | rawat jalan | P27 (Zainal Abidin) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 2,150,000 | 0.84 | fraud | `escalate` | excessive_usage |
| **KLM120** | 2026-03-09 | RS_J | rawat jalan | P27 (Zainal Abidin) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 2,150,000 | 0.84 | fraud | `escalate` | excessive_usage |
| **KLM121** | 2026-05-18 | RS_G | rawat inap | P29 (Bambang Riyanto) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 27,500,000 | 0.81 | fraud | `escalate` | biaya_markup |
| **KLM122** | 2026-06-06 | RS_H | rawat jalan | P30 (Citra Ayu Lestari) | D14 (dr. Nurul Aini, Sp.PD) | E11.9 | — | 8,900,000 | 0.82 | fraud | `escalate` | drug_diversion |
| **KLM123** | 2026-02-14 | RS_I | rawat inap | P31 (Dedi Kurniawan) | D18 (dr. Rizky Ramadhan, Sp.OT) | K40.9 | 53.1 | 21,000,000 | 0.64 | high | `review` | overbilling |
| **KLM124** | 2026-01-29 | RS_J | rawat inap | P32 (Endang Sulastri) | D19 (dr. Sinta Bella, Sp.P) | J18.9 | — | 8,200,000 | 0.71 | high | `review` | prolonged_stay |
| **KLM125** | 2026-03-27 | RS_G | rawat jalan | P33 (Fauzi Rahman) | D16 (dr. Prasetyo Utomo, Sp.JP) | E11.9 | — | 4,200,000 | 0.67 | high | `review` | anomali_frekuensi |
| **KLM126** | 2026-04-22 | RS_H | rawat jalan | P34 (Gita Puspita) | D14 (dr. Nurul Aini, Sp.PD) | K29.7 | — | 750,000 | 0.62 | high | `review` | anomali_frekuensi |
| **KLM127** | 2026-05-24 | RS_G | rawat inap | P35 (Hasan Basri) | D16 (dr. Prasetyo Utomo, Sp.JP) | I21.9 | 00.66 | 63,500,000 | 0.68 | high | `review` | prolonged_stay |
| **KLM128** | 2026-06-13 | RS_J | rawat jalan | P36 (Ifa Hidayati) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 3,100,000 | 0.63 | high | `review` | overbilling |
| **KLM129** | 2026-02-26 | RS_G | rawat inap | P37 (Jefri Nainggolan) | D13 (dr. Mulyadi Santoso, Sp.B) | S72.0 | 81.52 | 46,800,000 | 0.72 | high | `review` | prolonged_stay |
| **KLM130** | 2026-06-20 | RS_H | rawat jalan | P38 (Kirana Maheswari) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 3,850,000 | 0.62 | high | `review` | overbilling |
| **KLM131** | 2026-02-05 | RS_I | rawat jalan | P39 (Lukman Hakim) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,050,000 | 0.46 | medium | `review` | anomali_frekuensi |
| **KLM132** | 2026-03-14 | RS_J | rawat jalan | P40 (Maya Anggraini) | D19 (dr. Sinta Bella, Sp.P) | I10 | — | 950,000 | 0.42 | medium | `review` | anomali_frekuensi |
| **KLM133** | 2026-04-16 | RS_I | rawat jalan | P39 (Lukman Hakim) | D15 (dr. Oskar Lingga, Sp.PD) | J45.9 | — | 1,200,000 | 0.44 | medium | `review` | anomali_frekuensi |
| **KLM134** | 2026-05-09 | RS_J | rawat jalan | P40 (Maya Anggraini) | D19 (dr. Sinta Bella, Sp.P) | N39.0 | — | 1,100,000 | 0.48 | medium | `review` | anomali_frekuensi |
| **KLM135** | 2026-01-31 | RS_J | rawat jalan | P28 (Anisa Fitriani) | D19 (dr. Sinta Bella, Sp.P) | E11.9 | — | 1,250,000 | 0.40 | medium | `review` | anomali_frekuensi |
| **KLM136** | 2026-06-27 | RS_I | rawat jalan | P31 (Dedi Kurniawan) | D15 (dr. Oskar Lingga, Sp.PD) | K29.7 | — | 700,000 | 0.45 | medium | `review` | anomali_frekuensi |
| **KLM137** | 2026-01-03 | RS_J | rawat inap | P27 (Zainal Abidin) | D20 (dr. Teguh Wijaya, Sp.B) | K80.2 | 51.23 | 14,150,000 | 0.13 | low | `auto_clear` | - |
| **KLM138** | 2026-01-03 | RS_H | rawat jalan | P30 (Citra Ayu Lestari) | D14 (dr. Nurul Aini, Sp.PD) | I10 | — | 1,000,000 | 0.10 | low | `auto_clear` | - |
| **KLM139** | 2026-01-04 | RS_G | rawat jalan | P37 (Jefri Nainggolan) | D16 (dr. Prasetyo Utomo, Sp.JP) | I10 | — | 1,000,000 | 0.08 | low | `auto_clear` | - |
| **KLM140** | 2026-01-05 | RS_G | rawat jalan | P29 (Bambang Riyanto) | D16 (dr. Prasetyo Utomo, Sp.JP) | E11.9 | — | 1,100,000 | 0.07 | low | `auto_clear` | - |
| **KLM141** | 2026-01-06 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D16 (dr. Prasetyo Utomo, Sp.JP) | I21.9 | 00.66 | 61,150,000 | 0.06 | low | `auto_clear` | - |
| **KLM142** | 2026-01-06 | RS_I | rawat inap | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,450,000 | 0.09 | low | `auto_clear` | - |
| **KLM143** | 2026-01-07 | RS_H | rawat jalan | P23 (Tono Sugiarto) | D17 (dr. Qori Rahmawati, Sp.A) | J45.9 | — | 950,000 | 0.12 | low | `auto_clear` | - |
| **KLM144** | 2026-01-07 | RS_J | rawat jalan | P36 (Ifa Hidayati) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,150,000 | 0.08 | low | `auto_clear` | - |
| **KLM145** | 2026-01-08 | RS_J | rawat jalan | P36 (Ifa Hidayati) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,000,000 | 0.07 | low | `auto_clear` | - |
| **KLM146** | 2026-01-09 | RS_C | rawat inap | P08 (Maryam Yusuf) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 45,100,000 | 0.11 | low | `auto_clear` | - |
| **KLM147** | 2026-01-09 | RS_B | rawat inap | P14 (Odi Setiawan) | D07 (dr. Gunawan Halim, Sp.B) | K80.2 | 51.23 | 14,100,000 | 0.07 | low | `auto_clear` | - |
| **KLM148** | 2026-01-09 | RS_E | rawat jalan | P15 (Purnama Sidik) | D09 (dr. Indah Pratiwi, Sp.PD) | N39.0 | — | 1,150,000 | 0.08 | low | `auto_clear` | - |
| **KLM149** | 2026-01-09 | RS_I | rawat jalan | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | I10 | — | 1,000,000 | 0.09 | low | `auto_clear` | - |
| **KLM150** | 2026-01-10 | RS_H | rawat jalan | P24 (Umi Rahayu) | D14 (dr. Nurul Aini, Sp.PD) | I10 | — | 950,000 | 0.11 | low | `auto_clear` | - |
| **KLM151** | 2026-01-11 | RS_J | rawat inap | P40 (Maya Anggraini) | D20 (dr. Teguh Wijaya, Sp.B) | K35.8 | 47.09 | 6,900,000 | 0.12 | low | `auto_clear` | - |
| **KLM152** | 2026-01-13 | RS_B | rawat jalan | P06 (Fajar Nugroho) | D07 (dr. Gunawan Halim, Sp.B) | K29.7 | — | 700,000 | 0.07 | low | `auto_clear` | - |
| **KLM153** | 2026-01-13 | RS_I | rawat jalan | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,150,000 | 0.09 | low | `auto_clear` | - |
| **KLM154** | 2026-01-15 | RS_A | rawat inap | P02 (Bunga Lestari) | D01 (dr. Adnan Prakoso, Sp.BTKV) | I21.9 | 00.66 | 52,250,000 | 0.12 | low | `auto_clear` | - |
| **KLM155** | 2026-01-15 | RS_B | rawat inap | P06 (Fajar Nugroho) | D07 (dr. Gunawan Halim, Sp.B) | K35.8 | 47.09 | 6,600,000 | 0.08 | low | `auto_clear` | - |
| **KLM156** | 2026-01-15 | RS_E | rawat inap | P15 (Purnama Sidik) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 3,800,000 | 0.07 | low | `auto_clear` | - |
| **KLM157** | 2026-01-17 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D16 (dr. Prasetyo Utomo, Sp.JP) | I21.9 | 00.66 | 61,300,000 | 0.07 | low | `auto_clear` | - |
| **KLM158** | 2026-01-19 | RS_E | rawat inap | P17 (Slamet Riyadi) | D10 (dr. Joko Purnomo, Sp.S) | N20.0 | 98.51 | 5,650,000 | 0.07 | low | `auto_clear` | - |
| **KLM159** | 2026-01-19 | RS_J | rawat inap | P27 (Zainal Abidin) | D20 (dr. Teguh Wijaya, Sp.B) | K40.9 | 53.1 | 9,000,000 | 0.08 | low | `auto_clear` | - |
| **KLM160** | 2026-01-20 | RS_H | rawat jalan | P34 (Gita Puspita) | D14 (dr. Nurul Aini, Sp.PD) | I10 | — | 1,000,000 | 0.05 | low | `auto_clear` | - |
| **KLM161** | 2026-01-21 | RS_G | rawat inap | P35 (Hasan Basri) | D16 (dr. Prasetyo Utomo, Sp.JP) | I21.9 | 00.66 | 52,900,000 | 0.08 | low | `auto_clear` | - |
| **KLM162** | 2026-01-22 | RS_G | rawat inap | P22 (Sri Wahyuni) | D16 (dr. Prasetyo Utomo, Sp.JP) | I21.9 | 00.66 | 52,750,000 | 0.08 | low | `auto_clear` | - |
| **KLM163** | 2026-01-22 | RS_I | rawat jalan | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,100,000 | 0.10 | low | `auto_clear` | - |
| **KLM164** | 2026-01-22 | RS_G | rawat jalan | P33 (Fauzi Rahman) | D16 (dr. Prasetyo Utomo, Sp.JP) | E11.9 | — | 1,100,000 | 0.10 | low | `auto_clear` | - |
| **KLM165** | 2026-01-23 | RS_G | rawat inap | P33 (Fauzi Rahman) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 6,900,000 | 0.08 | low | `auto_clear` | - |
| **KLM166** | 2026-01-23 | RS_J | rawat inap | P36 (Ifa Hidayati) | D20 (dr. Teguh Wijaya, Sp.B) | K80.2 | 51.23 | 14,750,000 | 0.07 | low | `auto_clear` | - |
| **KLM167** | 2026-01-24 | RS_G | rawat inap | P22 (Sri Wahyuni) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 13,850,000 | 0.13 | low | `auto_clear` | - |
| **KLM168** | 2026-01-26 | RS_H | rawat inap | P30 (Citra Ayu Lestari) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 4,450,000 | 0.08 | low | `auto_clear` | - |
| **KLM169** | 2026-01-27 | RS_G | rawat jalan | P37 (Jefri Nainggolan) | D16 (dr. Prasetyo Utomo, Sp.JP) | I10 | — | 900,000 | 0.08 | low | `auto_clear` | - |
| **KLM170** | 2026-02-02 | RS_F | rawat inap | P19 (Umi Kalsum) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 7,550,000 | 0.06 | low | `auto_clear` | - |
| **KLM171** | 2026-02-02 | RS_H | rawat inap | P30 (Citra Ayu Lestari) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 4,250,000 | 0.09 | low | `auto_clear` | - |
| **KLM172** | 2026-02-02 | RS_G | rawat inap | P33 (Fauzi Rahman) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 6,800,000 | 0.09 | low | `auto_clear` | - |
| **KLM173** | 2026-02-05 | RS_A | rawat inap | P03 (Candra Wijaya) | D01 (dr. Adnan Prakoso, Sp.BTKV) | I21.9 | 00.66 | 58,850,000 | 0.07 | low | `auto_clear` | - |
| **KLM174** | 2026-02-05 | RS_G | rawat jalan | P29 (Bambang Riyanto) | D16 (dr. Prasetyo Utomo, Sp.JP) | I10 | — | 950,000 | 0.06 | low | `auto_clear` | - |
| **KLM175** | 2026-02-05 | RS_I | rawat inap | P31 (Dedi Kurniawan) | D18 (dr. Rizky Ramadhan, Sp.OT) | K40.9 | 53.1 | 8,150,000 | 0.11 | low | `auto_clear` | - |
| **KLM176** | 2026-02-06 | RS_F | rawat inap | P05 (Eka Putri) | D12 (dr. Lina Marlina, Sp.OG) | O80 | — | 3,900,000 | 0.10 | low | `auto_clear` | - |
| **KLM177** | 2026-02-08 | RS_A | rawat jalan | P01 (Agus Raharjo) | D03 (dr. Citra Ayuningtyas, Sp.PD) | N39.0 | — | 950,000 | 0.07 | low | `auto_clear` | - |
| **KLM178** | 2026-02-09 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D13 (dr. Mulyadi Santoso, Sp.B) | K40.9 | 53.1 | 8,800,000 | 0.09 | low | `auto_clear` | - |
| **KLM179** | 2026-02-11 | RS_I | rawat jalan | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,250,000 | 0.13 | low | `auto_clear` | - |
| **KLM180** | 2026-02-12 | RS_I | rawat jalan | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,250,000 | 0.07 | low | `auto_clear` | - |
| **KLM181** | 2026-02-13 | RS_E | rawat jalan | P17 (Slamet Riyadi) | D09 (dr. Indah Pratiwi, Sp.PD) | N39.0 | — | 1,050,000 | 0.09 | low | `auto_clear` | - |
| **KLM182** | 2026-02-13 | RS_G | rawat jalan | P29 (Bambang Riyanto) | D16 (dr. Prasetyo Utomo, Sp.JP) | E11.9 | — | 1,200,000 | 0.06 | low | `auto_clear` | - |
| **KLM183** | 2026-02-13 | RS_H | rawat inap | P38 (Kirana Maheswari) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 4,400,000 | 0.05 | low | `auto_clear` | - |
| **KLM184** | 2026-02-14 | RS_I | rawat jalan | P31 (Dedi Kurniawan) | D15 (dr. Oskar Lingga, Sp.PD) | I10 | — | 950,000 | 0.10 | low | `auto_clear` | - |
| **KLM185** | 2026-02-17 | RS_I | rawat jalan | P25 (Wawan Setiawan) | D15 (dr. Oskar Lingga, Sp.PD) | N39.0 | — | 1,100,000 | 0.07 | low | `auto_clear` | - |
| **KLM186** | 2026-02-19 | RS_J | rawat inap | P28 (Anisa Fitriani) | D20 (dr. Teguh Wijaya, Sp.B) | K40.9 | 53.1 | 8,350,000 | 0.08 | low | `auto_clear` | - |
| **KLM187** | 2026-02-19 | RS_J | rawat inap | P32 (Endang Sulastri) | D20 (dr. Teguh Wijaya, Sp.B) | K80.2 | 51.23 | 15,800,000 | 0.07 | low | `auto_clear` | - |
| **KLM188** | 2026-02-20 | RS_A | rawat inap | P01 (Agus Raharjo) | D03 (dr. Citra Ayuningtyas, Sp.PD) | J18.9 | — | 4,050,000 | 0.11 | low | `auto_clear` | - |
| **KLM189** | 2026-02-20 | RS_G | rawat jalan | P29 (Bambang Riyanto) | D16 (dr. Prasetyo Utomo, Sp.JP) | E11.9 | — | 1,050,000 | 0.11 | low | `auto_clear` | - |
| **KLM190** | 2026-02-20 | RS_I | rawat inap | P39 (Lukman Hakim) | D18 (dr. Rizky Ramadhan, Sp.OT) | S72.0 | 81.52 | 47,550,000 | 0.08 | low | `auto_clear` | - |
| **KLM191** | 2026-02-21 | RS_J | rawat inap | P27 (Zainal Abidin) | D20 (dr. Teguh Wijaya, Sp.B) | K80.2 | 51.23 | 13,650,000 | 0.07 | low | `auto_clear` | - |
| **KLM192** | 2026-02-21 | RS_J | rawat inap | P40 (Maya Anggraini) | D20 (dr. Teguh Wijaya, Sp.B) | K80.2 | 51.23 | 13,500,000 | 0.06 | low | `auto_clear` | - |
| **KLM193** | 2026-02-23 | RS_H | rawat jalan | P23 (Tono Sugiarto) | D17 (dr. Qori Rahmawati, Sp.A) | J45.9 | — | 950,000 | 0.08 | low | `auto_clear` | - |
| **KLM194** | 2026-02-24 | RS_H | rawat jalan | P24 (Umi Rahayu) | D17 (dr. Qori Rahmawati, Sp.A) | J45.9 | — | 1,050,000 | 0.08 | low | `auto_clear` | - |
| **KLM195** | 2026-02-25 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D16 (dr. Prasetyo Utomo, Sp.JP) | I21.9 | 00.66 | 61,400,000 | 0.10 | low | `auto_clear` | - |
| **KLM196** | 2026-02-25 | RS_J | rawat inap | P28 (Anisa Fitriani) | D20 (dr. Teguh Wijaya, Sp.B) | K40.9 | 53.1 | 8,750,000 | 0.07 | low | `auto_clear` | - |
| **KLM197** | 2026-02-26 | RS_H | rawat inap | P34 (Gita Puspita) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 3,900,000 | 0.09 | low | `auto_clear` | - |
| **KLM198** | 2026-02-26 | RS_J | rawat inap | P40 (Maya Anggraini) | D20 (dr. Teguh Wijaya, Sp.B) | K35.8 | 47.09 | 6,650,000 | 0.08 | low | `auto_clear` | - |
| **KLM199** | 2026-02-27 | RS_E | rawat inap | P16 (Ratna Dewi) | D09 (dr. Indah Pratiwi, Sp.PD) | J18.9 | — | 3,850,000 | 0.09 | low | `auto_clear` | - |
| **KLM200** | 2026-03-02 | RS_H | rawat jalan | P30 (Citra Ayu Lestari) | D14 (dr. Nurul Aini, Sp.PD) | I10 | — | 1,050,000 | 0.10 | low | `auto_clear` | - |
| **KLM201** | 2026-03-03 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 14,350,000 | 0.10 | low | `auto_clear` | - |
| **KLM202** | 2026-03-03 | RS_I | rawat jalan | P39 (Lukman Hakim) | D15 (dr. Oskar Lingga, Sp.PD) | N39.0 | — | 1,050,000 | 0.07 | low | `auto_clear` | - |
| **KLM203** | 2026-03-04 | RS_H | rawat inap | P38 (Kirana Maheswari) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 3,900,000 | 0.11 | low | `auto_clear` | - |
| **KLM204** | 2026-03-06 | RS_I | rawat inap | P31 (Dedi Kurniawan) | D18 (dr. Rizky Ramadhan, Sp.OT) | K40.9 | 53.1 | 8,750,000 | 0.07 | low | `auto_clear` | - |
| **KLM205** | 2026-03-07 | RS_G | rawat inap | P33 (Fauzi Rahman) | D13 (dr. Mulyadi Santoso, Sp.B) | K40.9 | 53.1 | 8,600,000 | 0.08 | low | `auto_clear` | - |
| **KLM206** | 2026-03-08 | RS_J | rawat inap | P32 (Endang Sulastri) | D20 (dr. Teguh Wijaya, Sp.B) | K40.9 | 53.1 | 8,600,000 | 0.07 | low | `auto_clear` | - |
| **KLM207** | 2026-03-10 | RS_A | rawat inap | P03 (Candra Wijaya) | D03 (dr. Citra Ayuningtyas, Sp.PD) | J18.9 | — | 4,500,000 | 0.11 | low | `auto_clear` | - |
| **KLM208** | 2026-03-10 | RS_I | rawat inap | P25 (Wawan Setiawan) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,100,000 | 0.11 | low | `auto_clear` | - |
| **KLM209** | 2026-03-11 | RS_G | rawat inap | P22 (Sri Wahyuni) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 7,150,000 | 0.07 | low | `auto_clear` | - |
| **KLM210** | 2026-03-11 | RS_I | rawat inap | P25 (Wawan Setiawan) | D18 (dr. Rizky Ramadhan, Sp.OT) | K40.9 | 53.1 | 8,450,000 | 0.10 | low | `auto_clear` | - |
| **KLM211** | 2026-03-13 | RS_D | rawat jalan | P07 (Gilang Saputra) | D04 (dr. Danur Wibisono, Sp.JP) | I10 | — | 900,000 | 0.07 | low | `auto_clear` | - |
| **KLM212** | 2026-03-13 | RS_F | rawat inap | P19 (Umi Kalsum) | D08 (dr. Hendra Maulana, Sp.B) | K35.8 | 47.09 | 6,400,000 | 0.08 | low | `auto_clear` | - |
| **KLM213** | 2026-03-17 | RS_C | rawat inap | P10 (Kartini Ibrahim) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 45,450,000 | 0.08 | low | `auto_clear` | - |
| **KLM214** | 2026-03-19 | RS_I | rawat inap | P31 (Dedi Kurniawan) | D15 (dr. Oskar Lingga, Sp.PD) | J18.9 | — | 4,150,000 | 0.10 | low | `auto_clear` | - |
| **KLM215** | 2026-03-20 | RS_G | rawat inap | P35 (Hasan Basri) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 13,900,000 | 0.06 | low | `auto_clear` | - |
| **KLM216** | 2026-03-21 | RS_H | rawat jalan | P34 (Gita Puspita) | D14 (dr. Nurul Aini, Sp.PD) | K29.7 | — | 800,000 | 0.07 | low | `auto_clear` | - |
| **KLM217** | 2026-03-22 | RS_G | rawat inap | P33 (Fauzi Rahman) | D16 (dr. Prasetyo Utomo, Sp.JP) | I21.9 | 00.66 | 59,900,000 | 0.11 | low | `auto_clear` | - |
| **KLM218** | 2026-03-22 | RS_J | rawat inap | P36 (Ifa Hidayati) | D20 (dr. Teguh Wijaya, Sp.B) | K35.8 | 47.09 | 6,250,000 | 0.08 | low | `auto_clear` | - |
| **KLM219** | 2026-03-23 | RS_G | rawat inap | P37 (Jefri Nainggolan) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 15,550,000 | 0.09 | low | `auto_clear` | - |
| **KLM220** | 2026-03-24 | RS_H | rawat jalan | P23 (Tono Sugiarto) | D14 (dr. Nurul Aini, Sp.PD) | N39.0 | — | 1,050,000 | 0.10 | low | `auto_clear` | - |
| **KLM221** | 2026-03-25 | RS_I | rawat inap | P39 (Lukman Hakim) | D18 (dr. Rizky Ramadhan, Sp.OT) | K40.9 | 53.1 | 7,650,000 | 0.11 | low | `auto_clear` | - |
| **KLM222** | 2026-03-27 | RS_G | rawat inap | P35 (Hasan Basri) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 14,350,000 | 0.08 | low | `auto_clear` | - |
| **KLM223** | 2026-04-03 | RS_G | rawat inap | P22 (Sri Wahyuni) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 6,150,000 | 0.10 | low | `auto_clear` | - |
| **KLM224** | 2026-04-04 | RS_G | rawat inap | P37 (Jefri Nainggolan) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 7,100,000 | 0.12 | low | `auto_clear` | - |
| **KLM225** | 2026-04-08 | RS_A | rawat inap | P18 (Tarmizi Karim) | D02 (dr. Barli Soemarno, Sp.B) | K35.8 | 47.09 | 7,350,000 | 0.09 | low | `auto_clear` | - |
| **KLM226** | 2026-04-12 | RS_J | rawat inap | P28 (Anisa Fitriani) | D19 (dr. Sinta Bella, Sp.P) | J18.9 | — | 4,200,000 | 0.09 | low | `auto_clear` | - |
| **KLM227** | 2026-04-12 | RS_G | rawat jalan | P37 (Jefri Nainggolan) | D16 (dr. Prasetyo Utomo, Sp.JP) | I10 | — | 1,000,000 | 0.07 | low | `auto_clear` | - |
| **KLM228** | 2026-04-12 | RS_I | rawat inap | P39 (Lukman Hakim) | D18 (dr. Rizky Ramadhan, Sp.OT) | S72.0 | 81.52 | 49,300,000 | 0.07 | low | `auto_clear` | - |
| **KLM229** | 2026-04-13 | RS_H | rawat jalan | P38 (Kirana Maheswari) | D14 (dr. Nurul Aini, Sp.PD) | I10 | — | 1,050,000 | 0.06 | low | `auto_clear` | - |
| **KLM230** | 2026-04-14 | RS_H | rawat jalan | P34 (Gita Puspita) | D14 (dr. Nurul Aini, Sp.PD) | E11.9 | — | 1,100,000 | 0.05 | low | `auto_clear` | - |
| **KLM231** | 2026-04-16 | RS_J | rawat jalan | P36 (Ifa Hidayati) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,100,000 | 0.12 | low | `auto_clear` | - |
| **KLM232** | 2026-04-18 | RS_G | rawat jalan | P33 (Fauzi Rahman) | D16 (dr. Prasetyo Utomo, Sp.JP) | E11.9 | — | 1,250,000 | 0.11 | low | `auto_clear` | - |
| **KLM233** | 2026-04-23 | RS_I | rawat jalan | P25 (Wawan Setiawan) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,150,000 | 0.10 | low | `auto_clear` | - |
| **KLM234** | 2026-04-23 | RS_J | rawat jalan | P32 (Endang Sulastri) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,150,000 | 0.06 | low | `auto_clear` | - |
| **KLM235** | 2026-04-26 | RS_F | rawat inap | P05 (Eka Putri) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 8,750,000 | 0.12 | low | `auto_clear` | - |
| **KLM236** | 2026-04-27 | RS_H | rawat jalan | P24 (Umi Rahayu) | D14 (dr. Nurul Aini, Sp.PD) | E11.9 | — | 1,100,000 | 0.07 | low | `auto_clear` | - |
| **KLM237** | 2026-04-27 | RS_J | rawat jalan | P32 (Endang Sulastri) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,050,000 | 0.10 | low | `auto_clear` | - |
| **KLM238** | 2026-04-28 | RS_H | rawat jalan | P24 (Umi Rahayu) | D14 (dr. Nurul Aini, Sp.PD) | E11.9 | — | 1,150,000 | 0.11 | low | `auto_clear` | - |
| **KLM239** | 2026-05-01 | RS_J | rawat jalan | P27 (Zainal Abidin) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,000,000 | 0.08 | low | `auto_clear` | - |
| **KLM240** | 2026-05-02 | RS_J | rawat inap | P28 (Anisa Fitriani) | D19 (dr. Sinta Bella, Sp.P) | J18.9 | — | 4,350,000 | 0.05 | low | `auto_clear` | - |
| **KLM241** | 2026-05-03 | RS_E | rawat jalan | P16 (Ratna Dewi) | D09 (dr. Indah Pratiwi, Sp.PD) | K29.7 | — | 700,000 | 0.08 | low | `auto_clear` | - |
| **KLM242** | 2026-05-04 | RS_H | rawat jalan | P34 (Gita Puspita) | D14 (dr. Nurul Aini, Sp.PD) | E11.9 | — | 1,100,000 | 0.06 | low | `auto_clear` | - |
| **KLM243** | 2026-05-05 | RS_J | rawat inap | P32 (Endang Sulastri) | D20 (dr. Teguh Wijaya, Sp.B) | K80.2 | 51.23 | 13,250,000 | 0.11 | low | `auto_clear` | - |
| **KLM244** | 2026-05-05 | RS_G | rawat inap | P35 (Hasan Basri) | D16 (dr. Prasetyo Utomo, Sp.JP) | I21.9 | 00.66 | 52,300,000 | 0.06 | low | `auto_clear` | - |
| **KLM245** | 2026-05-05 | RS_J | rawat inap | P36 (Ifa Hidayati) | D19 (dr. Sinta Bella, Sp.P) | J18.9 | — | 4,100,000 | 0.06 | low | `auto_clear` | - |
| **KLM246** | 2026-05-05 | RS_I | rawat inap | P39 (Lukman Hakim) | D18 (dr. Rizky Ramadhan, Sp.OT) | S72.0 | 81.52 | 48,850,000 | 0.07 | low | `auto_clear` | - |
| **KLM247** | 2026-05-06 | RS_I | rawat jalan | P25 (Wawan Setiawan) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,100,000 | 0.04 | low | `auto_clear` | - |
| **KLM248** | 2026-05-07 | RS_J | rawat inap | P27 (Zainal Abidin) | D20 (dr. Teguh Wijaya, Sp.B) | K35.8 | 47.09 | 6,450,000 | 0.05 | low | `auto_clear` | - |
| **KLM249** | 2026-05-08 | RS_G | rawat jalan | P29 (Bambang Riyanto) | D16 (dr. Prasetyo Utomo, Sp.JP) | I10 | — | 1,000,000 | 0.10 | low | `auto_clear` | - |
| **KLM250** | 2026-05-09 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 6,600,000 | 0.09 | low | `auto_clear` | - |
| **KLM251** | 2026-05-11 | RS_C | rawat inap | P09 (Idrus Hakim) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 42,500,000 | 0.09 | low | `auto_clear` | - |
| **KLM252** | 2026-05-13 | RS_G | rawat inap | P22 (Sri Wahyuni) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 6,150,000 | 0.11 | low | `auto_clear` | - |
| **KLM253** | 2026-05-13 | RS_H | rawat jalan | P23 (Tono Sugiarto) | D14 (dr. Nurul Aini, Sp.PD) | N39.0 | — | 1,050,000 | 0.07 | low | `auto_clear` | - |
| **KLM254** | 2026-05-13 | RS_I | rawat jalan | P31 (Dedi Kurniawan) | D15 (dr. Oskar Lingga, Sp.PD) | I10 | — | 950,000 | 0.06 | low | `auto_clear` | - |
| **KLM255** | 2026-05-14 | RS_A | rawat inap | P04 (Dewi Anggraeni) | D02 (dr. Barli Soemarno, Sp.B) | K35.8 | 47.09 | 6,850,000 | 0.12 | low | `auto_clear` | - |
| **KLM256** | 2026-05-14 | RS_F | rawat inap | P20 (Wahyu Nugraha) | D08 (dr. Hendra Maulana, Sp.B) | K40.9 | 53.1 | 7,450,000 | 0.10 | low | `auto_clear` | - |
| **KLM257** | 2026-05-15 | RS_I | rawat jalan | P31 (Dedi Kurniawan) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,200,000 | 0.08 | low | `auto_clear` | - |
| **KLM258** | 2026-05-17 | RS_G | rawat inap | P35 (Hasan Basri) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 15,500,000 | 0.11 | low | `auto_clear` | - |
| **KLM259** | 2026-05-17 | RS_H | rawat jalan | P38 (Kirana Maheswari) | D17 (dr. Qori Rahmawati, Sp.A) | J45.9 | — | 1,050,000 | 0.10 | low | `auto_clear` | - |
| **KLM260** | 2026-05-18 | RS_H | rawat jalan | P23 (Tono Sugiarto) | D14 (dr. Nurul Aini, Sp.PD) | N39.0 | — | 1,000,000 | 0.07 | low | `auto_clear` | - |
| **KLM261** | 2026-05-18 | RS_H | rawat jalan | P23 (Tono Sugiarto) | D14 (dr. Nurul Aini, Sp.PD) | N39.0 | — | 1,050,000 | 0.08 | low | `auto_clear` | - |
| **KLM262** | 2026-05-19 | RS_A | rawat inap | P18 (Tarmizi Karim) | D01 (dr. Adnan Prakoso, Sp.BTKV) | I21.9 | 00.66 | 58,000,000 | 0.06 | low | `auto_clear` | - |
| **KLM263** | 2026-05-21 | RS_J | rawat jalan | P28 (Anisa Fitriani) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,000,000 | 0.05 | low | `auto_clear` | - |
| **KLM264** | 2026-05-21 | RS_G | rawat inap | P29 (Bambang Riyanto) | D13 (dr. Mulyadi Santoso, Sp.B) | K40.9 | 53.1 | 7,650,000 | 0.05 | low | `auto_clear` | - |
| **KLM265** | 2026-05-21 | RS_J | rawat inap | P40 (Maya Anggraini) | D19 (dr. Sinta Bella, Sp.P) | J18.9 | — | 4,600,000 | 0.08 | low | `auto_clear` | - |
| **KLM266** | 2026-05-21 | RS_J | rawat jalan | P40 (Maya Anggraini) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,000,000 | 0.10 | low | `auto_clear` | - |
| **KLM267** | 2026-05-22 | RS_J | rawat inap | P32 (Endang Sulastri) | D20 (dr. Teguh Wijaya, Sp.B) | K35.8 | 47.09 | 6,550,000 | 0.09 | low | `auto_clear` | - |
| **KLM268** | 2026-05-23 | RS_C | rawat inap | P10 (Kartini Ibrahim) | D05 (dr. Endra Kusuma, Sp.OT) | K40.9 | 53.1 | 8,100,000 | 0.06 | low | `auto_clear` | - |
| **KLM269** | 2026-05-23 | RS_B | rawat jalan | P13 (Nadia Rahmawati) | D06 (dr. Fitri Handayani, Sp.A) | N39.0 | — | 1,150,000 | 0.06 | low | `auto_clear` | - |
| **KLM270** | 2026-05-23 | RS_J | rawat inap | P27 (Zainal Abidin) | D20 (dr. Teguh Wijaya, Sp.B) | K80.2 | 51.23 | 15,800,000 | 0.10 | low | `auto_clear` | - |
| **KLM271** | 2026-05-24 | RS_J | rawat inap | P40 (Maya Anggraini) | D20 (dr. Teguh Wijaya, Sp.B) | K35.8 | 47.09 | 6,850,000 | 0.09 | low | `auto_clear` | - |
| **KLM272** | 2026-05-25 | RS_H | rawat jalan | P34 (Gita Puspita) | D14 (dr. Nurul Aini, Sp.PD) | I10 | — | 950,000 | 0.06 | low | `auto_clear` | - |
| **KLM273** | 2026-05-25 | RS_G | rawat jalan | P35 (Hasan Basri) | D16 (dr. Prasetyo Utomo, Sp.JP) | I10 | — | 1,000,000 | 0.11 | low | `auto_clear` | - |
| **KLM274** | 2026-06-01 | RS_D | rawat jalan | P11 (Lukman Sutrisno) | D04 (dr. Danur Wibisono, Sp.JP) | I10 | — | 950,000 | 0.09 | low | `auto_clear` | - |
| **KLM275** | 2026-06-01 | RS_F | rawat jalan | P20 (Wahyu Nugraha) | D08 (dr. Hendra Maulana, Sp.B) | K29.7 | — | 800,000 | 0.08 | low | `auto_clear` | - |
| **KLM276** | 2026-06-02 | RS_C | rawat inap | P08 (Maryam Yusuf) | D05 (dr. Endra Kusuma, Sp.OT) | S72.0 | 81.52 | 43,950,000 | 0.10 | low | `auto_clear` | - |
| **KLM277** | 2026-06-02 | RS_H | rawat jalan | P30 (Citra Ayu Lestari) | D14 (dr. Nurul Aini, Sp.PD) | K29.7 | — | 750,000 | 0.11 | low | `auto_clear` | - |
| **KLM278** | 2026-06-04 | RS_B | rawat inap | P12 (Maya Sari) | D07 (dr. Gunawan Halim, Sp.B) | K40.9 | 53.1 | 7,500,000 | 0.09 | low | `auto_clear` | - |
| **KLM279** | 2026-06-05 | RS_H | rawat inap | P38 (Kirana Maheswari) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 4,300,000 | 0.08 | low | `auto_clear` | - |
| **KLM280** | 2026-06-06 | RS_J | rawat inap | P28 (Anisa Fitriani) | D19 (dr. Sinta Bella, Sp.P) | J18.9 | — | 4,100,000 | 0.06 | low | `auto_clear` | - |
| **KLM281** | 2026-06-07 | RS_H | rawat inap | P24 (Umi Rahayu) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 4,100,000 | 0.13 | low | `auto_clear` | - |
| **KLM282** | 2026-06-10 | RS_D | rawat inap | P07 (Gilang Saputra) | D11 (dr. Kartika Sari, Sp.B) | K40.9 | 53.1 | 8,800,000 | 0.09 | low | `auto_clear` | - |
| **KLM283** | 2026-06-10 | RS_B | rawat inap | P14 (Odi Setiawan) | D07 (dr. Gunawan Halim, Sp.B) | K40.9 | 53.1 | 7,900,000 | 0.09 | low | `auto_clear` | - |
| **KLM284** | 2026-06-11 | RS_G | rawat jalan | P22 (Sri Wahyuni) | D16 (dr. Prasetyo Utomo, Sp.JP) | E11.9 | — | 1,250,000 | 0.07 | low | `auto_clear` | - |
| **KLM285** | 2026-06-12 | RS_G | rawat inap | P21 (Rahmat Fauzi) | D13 (dr. Mulyadi Santoso, Sp.B) | K80.2 | 51.23 | 15,000,000 | 0.10 | low | `auto_clear` | - |
| **KLM286** | 2026-06-13 | RS_G | rawat inap | P37 (Jefri Nainggolan) | D13 (dr. Mulyadi Santoso, Sp.B) | K35.8 | 47.09 | 6,850,000 | 0.06 | low | `auto_clear` | - |
| **KLM287** | 2026-06-15 | RS_H | rawat jalan | P24 (Umi Rahayu) | D14 (dr. Nurul Aini, Sp.PD) | N39.0 | — | 950,000 | 0.10 | low | `auto_clear` | - |
| **KLM288** | 2026-06-18 | RS_I | rawat jalan | P31 (Dedi Kurniawan) | D15 (dr. Oskar Lingga, Sp.PD) | N39.0 | — | 1,050,000 | 0.09 | low | `auto_clear` | - |
| **KLM289** | 2026-06-19 | RS_A | rawat jalan | P02 (Bunga Lestari) | D03 (dr. Citra Ayuningtyas, Sp.PD) | I10 | — | 1,000,000 | 0.10 | low | `auto_clear` | - |
| **KLM290** | 2026-06-20 | RS_I | rawat jalan | P26 (Yulia Ningsih) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,200,000 | 0.10 | low | `auto_clear` | - |
| **KLM291** | 2026-06-20 | RS_H | rawat jalan | P38 (Kirana Maheswari) | D14 (dr. Nurul Aini, Sp.PD) | I10 | — | 900,000 | 0.12 | low | `auto_clear` | - |
| **KLM292** | 2026-06-21 | RS_I | rawat jalan | P25 (Wawan Setiawan) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,050,000 | 0.08 | low | `auto_clear` | - |
| **KLM293** | 2026-06-23 | RS_I | rawat jalan | P39 (Lukman Hakim) | D15 (dr. Oskar Lingga, Sp.PD) | E11.9 | — | 1,050,000 | 0.10 | low | `auto_clear` | - |
| **KLM294** | 2026-06-24 | RS_A | rawat jalan | P04 (Dewi Anggraeni) | D03 (dr. Citra Ayuningtyas, Sp.PD) | E11.9 | — | 1,100,000 | 0.08 | low | `auto_clear` | - |
| **KLM295** | 2026-06-24 | RS_B | rawat inap | P13 (Nadia Rahmawati) | D07 (dr. Gunawan Halim, Sp.B) | K40.9 | 53.1 | 8,200,000 | 0.09 | low | `auto_clear` | - |
| **KLM296** | 2026-06-25 | RS_H | rawat inap | P30 (Citra Ayu Lestari) | D14 (dr. Nurul Aini, Sp.PD) | J18.9 | — | 4,550,000 | 0.10 | low | `auto_clear` | - |
| **KLM297** | 2026-06-26 | RS_C | rawat inap | P09 (Idrus Hakim) | D05 (dr. Endra Kusuma, Sp.OT) | K40.9 | 53.1 | 8,800,000 | 0.08 | low | `auto_clear` | - |
| **KLM298** | 2026-06-26 | RS_D | rawat inap | P11 (Lukman Sutrisno) | D11 (dr. Kartika Sari, Sp.B) | K35.8 | 47.09 | 6,500,000 | 0.08 | low | `auto_clear` | - |
| **KLM299** | 2026-06-27 | RS_B | rawat jalan | P12 (Maya Sari) | D06 (dr. Fitri Handayani, Sp.A) | N39.0 | — | 1,100,000 | 0.08 | low | `auto_clear` | - |
| **KLM300** | 2026-06-27 | RS_J | rawat jalan | P36 (Ifa Hidayati) | D19 (dr. Sinta Bella, Sp.P) | J45.9 | — | 1,150,000 | 0.07 | low | `auto_clear` | - |

---

## 3. Investigasi Kasus Fraud & Sinyal SHAP Terverifikasi

Berikut adalah studi kasus klaim terflagging fraud paling kritis dari dataset:

### 1. Klaim KLM001 — upcoding (Skor Fraud: 0.94, Risiko: `fraud`)
- **Faskes / Dokter:** RS_A / D01 (dr. Adnan Prakoso, Sp.BTKV)
- **Pasien:** P01 (Agus Raharjo) (rawat inap, Tgl: 2026-02-16, LOS: 2 hari)
- **Diagnosis ICD-10:** K29.7 - Gastritis, tanpa perdarahan
- **Prosedur ICD-9-CM:** 00.66 - Angioplasti koroner + stent (PCI)
- **Biaya Klaim:** Rp52,300,000 | **Obat:** M04 x 3 vial; M08 x 10 tablet
- **Narasi EMR:** "Pasien nyeri epigastrium; hasil endoskopi gastritis superfisialis. Selama rawat dicatat tindakan kateterisasi jantung dan pemasangan stent koroner."
- **Kontradiksi Narasi EMR:** `True`
- **Umpan Balik Pasien:** "Saya hanya periksa lambung, kenapa ada tagihan tindakan jantung?" (Sentimen: negatif, Skor: -0.75)
- **Sinyal SHAP Dominan:** inkonsistensi diagnosis-prosedur (K29.7 gastritis -> 00.66 PCI); biaya & LOS identik antar-pasien; subgraf padat P-D-RS_A
- **Kontribusi Saluran Deteksi:** `T 0.31 · F 0.32 · S 0.31`
- **Alasan Deteksi Sistem:** FRAUD (Upcoding): diagnosis primer gastritis ringan (K29.7) ditagih sebagai tindakan PCI dengan stent (00.66, Rp58 jt) — tidak mungkin secara klinis tanpa indikasi kardiologis, dan tidak ada satu pun obat kardiovaskular pada dispensing. Biaya & LOS identik pada 3 pasien berbeda menandakan pola terorganisir (sindikat), bukan kesalahan input.
- **Sindikat / Catatan:** SYND-01

### 2. Klaim KLM002 — upcoding (Skor Fraud: 0.95, Risiko: `fraud`)
- **Faskes / Dokter:** RS_A / D02 (dr. Barli Soemarno, Sp.B)
- **Pasien:** P02 (Bunga Lestari) (rawat inap, Tgl: 2026-02-17, LOS: 2 hari)
- **Diagnosis ICD-10:** K29.7 - Gastritis, tanpa perdarahan
- **Prosedur ICD-9-CM:** 00.66 - Angioplasti koroner + stent (PCI)
- **Biaya Klaim:** Rp52,300,000 | **Obat:** M04 x 3 vial; M08 x 10 tablet
- **Narasi EMR:** "Pasien nyeri epigastrium; hasil endoskopi gastritis superfisialis. Selama rawat dicatat tindakan kateterisasi jantung dan pemasangan stent koroner."
- **Kontradiksi Narasi EMR:** `True`
- **Umpan Balik Pasien:** "Katanya hanya endoskopi, tapi muncul tindakan kateter jantung di tagihan." (Sentimen: negatif, Skor: -0.8)
- **Sinyal SHAP Dominan:** inkonsistensi diagnosis-prosedur (K29.7 gastritis -> 00.66 PCI); biaya & LOS identik antar-pasien; subgraf padat P-D-RS_A
- **Kontribusi Saluran Deteksi:** `T 0.31 · F 0.32 · S 0.31`
- **Alasan Deteksi Sistem:** FRAUD (Upcoding): diagnosis primer gastritis ringan (K29.7) ditagih sebagai tindakan PCI dengan stent (00.66, Rp58 jt) — tidak mungkin secara klinis tanpa indikasi kardiologis, dan tidak ada satu pun obat kardiovaskular pada dispensing. Biaya & LOS identik pada 3 pasien berbeda menandakan pola terorganisir (sindikat), bukan kesalahan input.
- **Sindikat / Catatan:** SYND-01

### 3. Klaim KLM003 — upcoding (Skor Fraud: 0.93, Risiko: `fraud`)
- **Faskes / Dokter:** RS_A / D01 (dr. Adnan Prakoso, Sp.BTKV)
- **Pasien:** P03 (Candra Wijaya) (rawat inap, Tgl: 2026-02-18, LOS: 2 hari)
- **Diagnosis ICD-10:** K29.7 - Gastritis, tanpa perdarahan
- **Prosedur ICD-9-CM:** 00.66 - Angioplasti koroner + stent (PCI)
- **Biaya Klaim:** Rp52,300,000 | **Obat:** M04 x 3 vial; M08 x 10 tablet
- **Narasi EMR:** "Pasien nyeri epigastrium; hasil endoskopi gastritis superfisialis. Selama rawat dicatat tindakan kateterisasi jantung dan pemasangan stent koroner."
- **Kontradiksi Narasi EMR:** `True`
- **Umpan Balik Pasien:** "Saya tidak pernah sakit dada, kok dibilang dipasang stent?" (Sentimen: negatif, Skor: -0.78)
- **Sinyal SHAP Dominan:** inkonsistensi diagnosis-prosedur (K29.7 gastritis -> 00.66 PCI); biaya & LOS identik antar-pasien; subgraf padat P-D-RS_A
- **Kontribusi Saluran Deteksi:** `T 0.31 · F 0.32 · S 0.31`
- **Alasan Deteksi Sistem:** FRAUD (Upcoding): diagnosis primer gastritis ringan (K29.7) ditagih sebagai tindakan PCI dengan stent (00.66, Rp58 jt) — tidak mungkin secara klinis tanpa indikasi kardiologis, dan tidak ada satu pun obat kardiovaskular pada dispensing. Biaya & LOS identik pada 3 pasien berbeda menandakan pola terorganisir (sindikat), bukan kesalahan input.
- **Sindikat / Catatan:** SYND-01

### 4. Klaim KLM004 — phantom_billing (Skor Fraud: 0.92, Risiko: `fraud`)
- **Faskes / Dokter:** RS_C / D05 (dr. Endra Kusuma, Sp.OT)
- **Pasien:** P08 (Maryam Yusuf) (rawat inap, Tgl: 2026-03-12, LOS: 1 hari)
- **Diagnosis ICD-10:** S72.0 - Fraktur kolum femur, tertutup
- **Prosedur ICD-9-CM:** 81.52 - Hemiarthroplasty panggul
- **Biaya Klaim:** Rp44,750,000 | **Obat:** —
- **Narasi EMR:** "Fraktur kolum femur; dilakukan hemiarthroplasty. Toleransi oral baik, pasien pulang dalam kondisi stabil."
- **Kontradiksi Narasi EMR:** `True`
- **Umpan Balik Pasien:** "Saya tidak pernah menjalani operasi apa pun di rumah sakit ini." (Sentimen: negatif, Skor: -0.9)
- **Sinyal SHAP Dominan:** 3 klaim tanggal & biaya identik; LOS 1 hari untuk hemiarthroplasty mayor; tanpa MedicationDispense (layanan tak terverifikasi)
- **Kontribusi Saluran Deteksi:** `T 0.32 · F 0.35 · S 0.26`
- **Alasan Deteksi Sistem:** FRAUD (Phantom Billing): klaim hemiarthroplasty dengan tanggal & biaya identik untuk 3 pasien pada hari yang sama, LOS hanya 1 hari untuk bedah mayor, tanpa MedicationDispense maupun resume medis di SATUSEHAT — indikasi kuat layanan tidak pernah diberikan (klaim fiktif).
- **Sindikat / Catatan:** SYND-02

### 5. Klaim KLM005 — phantom_billing (Skor Fraud: 0.94, Risiko: `fraud`)
- **Faskes / Dokter:** RS_C / D05 (dr. Endra Kusuma, Sp.OT)
- **Pasien:** P09 (Idrus Hakim) (rawat inap, Tgl: 2026-03-12, LOS: 1 hari)
- **Diagnosis ICD-10:** S72.0 - Fraktur kolum femur, tertutup
- **Prosedur ICD-9-CM:** 81.52 - Hemiarthroplasty panggul
- **Biaya Klaim:** Rp44,750,000 | **Obat:** —
- **Narasi EMR:** "Fraktur kolum femur; dilakukan hemiarthroplasty. Toleransi oral baik, pasien pulang dalam kondisi stabil."
- **Kontradiksi Narasi EMR:** `True`
- **Umpan Balik Pasien:** "Tidak ada operasi yang pernah saya jalani bulan Maret ini." (Sentimen: negatif, Skor: -0.85)
- **Sinyal SHAP Dominan:** 3 klaim tanggal & biaya identik; LOS 1 hari untuk hemiarthroplasty mayor; tanpa MedicationDispense (layanan tak terverifikasi)
- **Kontribusi Saluran Deteksi:** `T 0.32 · F 0.35 · S 0.26`
- **Alasan Deteksi Sistem:** FRAUD (Phantom Billing): klaim hemiarthroplasty dengan tanggal & biaya identik untuk 3 pasien pada hari yang sama, LOS hanya 1 hari untuk bedah mayor, tanpa MedicationDispense maupun resume medis di SATUSEHAT — indikasi kuat layanan tidak pernah diberikan (klaim fiktif).
- **Sindikat / Catatan:** SYND-02

### 6. Klaim KLM006 — phantom_billing (Skor Fraud: 0.93, Risiko: `fraud`)
- **Faskes / Dokter:** RS_C / D05 (dr. Endra Kusuma, Sp.OT)
- **Pasien:** P10 (Kartini Ibrahim) (rawat inap, Tgl: 2026-03-12, LOS: 1 hari)
- **Diagnosis ICD-10:** S72.0 - Fraktur kolum femur, tertutup
- **Prosedur ICD-9-CM:** 81.52 - Hemiarthroplasty panggul
- **Biaya Klaim:** Rp44,750,000 | **Obat:** —
- **Narasi EMR:** "Fraktur kolum femur; dilakukan hemiarthroplasty. Toleransi oral baik, pasien pulang dalam kondisi stabil."
- **Kontradiksi Narasi EMR:** `True`
- **Umpan Balik Pasien:** "Saya hanya kontrol nyeri pinggang, tidak pernah dioperasi." (Sentimen: negatif, Skor: -0.88)
- **Sinyal SHAP Dominan:** 3 klaim tanggal & biaya identik; LOS 1 hari untuk hemiarthroplasty mayor; tanpa MedicationDispense (layanan tak terverifikasi)
- **Kontribusi Saluran Deteksi:** `T 0.32 · F 0.35 · S 0.26`
- **Alasan Deteksi Sistem:** FRAUD (Phantom Billing): klaim hemiarthroplasty dengan tanggal & biaya identik untuk 3 pasien pada hari yang sama, LOS hanya 1 hari untuk bedah mayor, tanpa MedicationDispense maupun resume medis di SATUSEHAT — indikasi kuat layanan tidak pernah diberikan (klaim fiktif).
- **Sindikat / Catatan:** SYND-02

### 7. Klaim KLM007 — unbundling (Skor Fraud: 0.85, Risiko: `fraud`)
- **Faskes / Dokter:** RS_B / D07 (dr. Gunawan Halim, Sp.B)
- **Pasien:** P12 (Maya Sari) (rawat inap, Tgl: 2026-04-18, LOS: 4 hari)
- **Diagnosis ICD-10:** K80.2 - Kolelitiasis, tanpa kolesistitis
- **Prosedur ICD-9-CM:** 51.23 - Kolesistektomi laparoskopik
- **Biaya Klaim:** Rp15,500,000 | **Obat:** M03 x 6 vial; M04 x 7 vial
- **Narasi EMR:** "Kolelitiasis; dilakukan kolesistektomi laparoskopik. Toleransi oral baik, pasien pulang dengan kontrol poliklinik."
- **Kontradiksi Narasi EMR:** `False`
- **Umpan Balik Pasien:** "Kenapa ada dua tagihan untuk satu operasi yang sama?" (Sentimen: negatif, Skor: -0.5)
- **Sinyal SHAP Dominan:** paket kolesistektomi dipecah menjadi 2 klaim tanggal sama; total biaya > paket INA-CBG; pola identik pada 3 pasien berbeda
- **Kontribusi Saluran Deteksi:** `T 0.29 · F 0.3 · S 0.26`
- **Alasan Deteksi Sistem:** FRAUD (Unbundling): paket kolesistektomi (51.23) dipecah dengan menagih intubasi (96.04) secara terpisah pada tanggal yang sama, sehingga total tagihan melampaui nilai paket INA-CBG; pola identik pada 3 pasien menandakan fragmentasi sistematis, bukan kesalahan coding.
- **Sindikat / Catatan:** SYND-03

### 8. Klaim KLM008 — unbundling (Skor Fraud: 0.85, Risiko: `fraud`)
- **Faskes / Dokter:** RS_B / D07 (dr. Gunawan Halim, Sp.B)
- **Pasien:** P12 (Maya Sari) (rawat inap, Tgl: 2026-04-18, LOS: 0 hari)
- **Diagnosis ICD-10:** K80.2 - Kolelitiasis, tanpa kolesistitis
- **Prosedur ICD-9-CM:** 96.04 - Pemasangan pipa endotrakeal (intubasi)
- **Biaya Klaim:** Rp2,100,000 | **Obat:** M08 x 6 tablet
- **Narasi EMR:** "Kolelitiasis; dilakukan kolesistektomi laparoskopik. Toleransi oral baik, pasien pulang dengan kontrol poliklinik."
- **Kontradiksi Narasi EMR:** `False`
- **Umpan Balik Pasien:** "Muncul tagihan kedua untuk tindakan yang tidak saya ketahui." (Sentimen: negatif, Skor: -0.55)
- **Sinyal SHAP Dominan:** klaim pecahan dari paket operasi (unbundling); LOS 0 padat kunjungan bedah mayor
- **Kontribusi Saluran Deteksi:** `T 0.29 · F 0.3 · S 0.26`
- **Alasan Deteksi Sistem:** FRAUD (Unbundling — klaim pecahan): baris intubasi (96.04) seharusnya tergabung dalam paket bedah kolesistektomi pada tanggal yang sama; menagihnya terpisah menghasilkan pembayaran ganda untuk komponen yang sudah termasuk paket.
- **Sindikat / Catatan:** SYND-03
