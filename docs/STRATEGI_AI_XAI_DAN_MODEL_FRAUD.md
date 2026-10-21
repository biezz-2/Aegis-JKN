# Strategi AI: XAI/Grok dan Model Deteksi Fraud Aegis-JKN

## Keputusan

**XAI/Grok cukup kuat sebagai copilot bahasa untuk verifikator, tetapi tidak digunakan sebagai mesin utama deteksi fraud klaim.**

Aegis-JKN tidak melatih LLM dari nol. Untuk skor fraud, sistem memakai model khusus yang dapat diukur dan diaudit. XAI/Grok dipakai secara terbatas untuk membantu pembacaan serta penjelasan bukti.

> AI memberikan rekomendasi, bukan keputusan. Keputusan akhir ada pada verifikator.

## Pembagian peran teknologi

| Fungsi | Teknologi yang disarankan | Peran |
|---|---|---|
| Prioritisasi fraud | Rule engine + XGBoost/LightGBM | Menghasilkan skor risiko dari fitur klaim terstruktur secara cepat dan terukur. |
| Pola kolusi/sindikat | Graf heterogen / MHGSL | Tahap lanjutan untuk pola relasional, setelah tersedia data graph berizin dengan provenance. |
| Narasi medis dan komunikasi | XAI/Grok API dengan kontrol ketat | Menyusun ringkasan, mengekstrak fakta, serta menulis draf pertanyaan klarifikasi. |
| Keputusan klaim | Verifikator manusia | Menyetujui, meminta konfirmasi, atau menolak klaim berdasarkan bukti dan kebijakan. |

## Mengapa XAI/Grok tidak menjadi mesin fraud utama

1. **Tidak deterministik.** Jawaban LLM dapat berbeda untuk input atau prompt yang serupa.
2. **Sulit dikalibrasi.** Fraud detection memerlukan metrik terukur, seperti precision, recall, AUPRC, false-positive rate, dan pemantauan drift.
3. **Auditabilitas terbatas.** Alasan keputusan harus dapat ditelusuri pada sumber klaim, bukan pada narasi generatif yang dapat terhalusinasi.
4. **Biaya dan latensi.** Pemrosesan seluruh volume klaim dengan LLM lebih mahal serta lebih lambat dibanding model tabular.
5. **Privasi dan kepatuhan.** Data kesehatan merupakan data pribadi spesifik menurut UU PDP. Data nyata tidak boleh dikirim ke API eksternal tanpa dasar pemrosesan yang sah, kontrak pemrosesan data, kontrol retensi, penilaian keamanan, dan otorisasi institusi.

## Penggunaan XAI/Grok yang diperbolehkan

XAI/Grok dapat digunakan untuk:

- membuat ringkasan narasi rekam medis;
- mengekstrak fakta yang sudah tertulis, misalnya tanggal, diagnosis, prosedur, obat, dan LOS;
- menunjukkan ketidaksesuaian yang **harus diperiksa** verifikator;
- menyusun draf permintaan klarifikasi kepada rumah sakit;
- menerjemahkan bukti model tabular/graf ke bahasa Indonesia yang mudah dibaca;
- membantu klasifikasi kelengkapan dokumen, dengan keputusan tetap pada manusia.

Implementasi harus memakai output terstruktur, misalnya JSON schema, serta validasi terhadap sumber. Jika data tidak cukup atau output tidak valid, sistem harus menampilkan status tidak tersedia atau meminta telaah manusia.

## Penggunaan yang dilarang

XAI/Grok tidak boleh:

- menyetujui, menolak, menghentikan, atau mengeskalasi klaim secara otomatis;
- menyatakan suatu klaim "pasti fraud";
- mengubah status, tarif, nilai bayar, atau data sumber klaim;
- membuat fakta medis yang tidak tertulis dalam dokumen sumber;
- menerima data kesehatan nyata pada layanan eksternal sebelum seluruh kontrol kepatuhan disetujui.

## Strategi pengembangan bertahap

### 1. Prototype saat ini

- Gunakan dataset sintetis.
- Terapkan rule engine dan baseline tabular pada tahap konsep.
- Tampilkan bukti yang telah diprakomputasi pada dashboard.
- Gunakan XAI hanya dengan data sintetis atau data yang telah dipseudonimkan sesuai persetujuan.

### 2. Pilot berizin

- Kumpulkan label audit historis yang terdefinisi dengan jelas.
- Terapkan pemisahan data berdasarkan waktu, pasien, dokter, dan faskes untuk mencegah leakage.
- Latih serta kalibrasi model fraud tabular khusus.
- Ukur AUPRC, precision pada kapasitas antrean, false positive, override rate, dan kualitas dokumentasi verifikator.

### 3. MHGSL dan graph analytics

- Bentuk graph dari relasi claim–patient–doctor–faskes–diagnosis–procedure yang berizin.
- Simpan timestamp, tipe relasi, dan provenance untuk setiap edge.
- Bandingkan model MHGSL dengan baseline XGBoost/LightGBM melalui split temporal dan group-aware.
- Jangan mempromosikan GNN ke produksi jika manfaatnya tidak melebihi tambahan kompleksitas, biaya, dan risiko tata kelola.

### 4. Integrasi LLM terbatas

- Terapkan *retrieval-grounded summarization* terhadap bukti yang diizinkan.
- Kirim data minimum yang telah dipseudonimkan.
- Gunakan JSON schema, validasi input/output, audit prompt dan output, serta fallback tanpa LLM.
- Pisahkan sepenuhnya fungsi LLM dari mesin skor dan keputusan klaim.

## Kesimpulan

Pilihan paling tepat untuk Aegis-JKN adalah:

1. tidak menggunakan XAI/Grok sebagai fraud engine utama;
2. tidak melatih LLM dari nol;
3. melatih model fraud tabular khusus ketika tersedia data dan label audit berizin;
4. menambahkan MHGSL hanya setelah graph nyata dan evaluasi yang sah tersedia;
5. menggunakan XAI/Grok sebagai copilot bahasa yang dibatasi, dapat divalidasi, dan tidak memiliki hak veto.

## Referensi awal

- xAI API: <https://x.ai/api> — verifikasi langsung persyaratan enterprise, retensi, lokasi pemrosesan, dan perjanjian pemrosesan data sebelum penggunaan data kesehatan nyata.
- Republik Indonesia, Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi.
- `docs/makalah/Makalah_Aegis-JKN.md` — rancangan MHGSL, HITL, kepatuhan, dan batasan data sintetis.
