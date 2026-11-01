# 03 - Audit Arsitektur: Desain vs Implementasi
## Aegis-JKN (Healthkathon BPJS Kesehatan 2026) - Spesifikasi Rekayasa Rev 1.0 vs Kode As-Built

| Aspek | Nilai |
|---|---|
| Spec utama | `analysis/corpus/02-architecture.md` (Spesifikasi Rekayasa Rev 1.0) |
| Spec pendukung | `analysis/corpus/00-dashboard.md`, `03-dataset-registry.md`, `05-decision-scope.md`, `08-training-protocol.md`, `10-simulation-dataset.md` |
| Pembanding arsip | `analysis/corpus/12-archive-architecture.md` (arsip v2.1) |
| Kode yang diaudit | `N:\HEALTHKATHON\Aegis-JKN\` (read-only, 86 file `src/`, 5 file `docs/`) |
| Tanggal audit | 22 Oktober 2026 |
| Metode | `grep`/`find`/`node` parsing nyata terhadap repo. Tidak ada estimasi manual. Semua baris di bawah sudah diverifikasi ulang per 22 Okt 2026. |

---

## 1. Ringkasan Eksekutif

Spesifikasi Rev 1.0 merancang sistem **berlapis**: rule engine (Tier 1) → model tabular (Tier 2) → heterogeneous graph (Tier 3) → fusi + SHAP, dengan API batch, basis data, dan protokol evaluasi yang dapat direproduksi. Yang ada di repo adalah **sebuah aplikasi Next.js satu halaman**: 12 komponen presentasi, satu stub `Hello, world!`, satu berkas dataset 300 klaim yang di-hardcode, dan angka benchmark yang ditulis langsung sebagai konstanta di dalam komponen.

Tiga kesimpulan utama:

1. **Tidak ada satu pun pipeline analitik yang diuji.** Tidak ada rule engine, tidak ada model, tidak ada split, tidak ada evaluator, tidak ada satu pun artefak eksperimen yang diwajibkan 02 §5.5.Repo berisi **nol file Python** (`find . -name "*.py"` → kosong), nol `configs/leakage.yaml`, nol `tests/test_leakage.py`, nol `edges.json`, nol `experiment_manifest.json`. `package.json:5-15` tidak punya script `test`.
2. **Angka "ilmu" yang ditampilkan adalah konstanta UI, bukan hasil pengukuran.** AUPRC 0,91, precision 0,92, ROC-AUC 0,95, Δ +0,20, kurva epoch E1→E5, akurasi 93%, deteksi 100%, antrean 20%, kapasitas 6.667 klaim, ROI 20→3 menit, penghematan "Rp 1,2 M/bulan" - semuanya konstanta hardcoded (`src/components/mhgsl/data.ts:253,264,289,300`; `comparison.tsx:134,373-377`; `src/data/oasis-data.ts:92,93,94,97,108`; `data.ts:391-392`; `fraud-ring.tsx:415`). Tidak ada satu pun yang berasal dari eksekusi model. 00-dashboard.md:46-49 justru menyatakan angka-angka yang serupa **"belum boleh disebut hasil tervalidasi"**, dan 02 §5.5 mewajibkan 10 artefak per eksperimen - nol tersedia.
3. **Mekanisme anti-leakage yang ada di arsip dihapus saat revisi, lalu kebocoran justru bocor lewat UI.** Arsip 12:47,66,140-141 Advocate `configs/leakage.yaml` + `tests/test_leakage.py` sebagai penutup. Rev 1.0 menghapus keduanya, dan 03 §7 (baris 84) tetap mewajibkan 8 kolom yang tidak boleh jadi fitur. Ekspor CSV di `dataset-explorer.tsx:425-453` justru **menyalin 8 kolom terlarang itu** (Skor Fraud, Risiko, Status, Modus, Sindikat, Sinyal SHAP, Kontribusi Saluran, Alasan Audit) plus checksum/seed/split-ID yang tidak ada (§8 butir 1-10).

Tumpukan masalah kedua yang berulang: **ambang skor ada di empat skala yang saling bertentangan** dan **nilai dataset aktif tidak cocok dengan ambang mana pun** - 11 dari 36 klaim fraud (31%) memiliki Skor Fraud 0,80–0,84, di bawah ambang 0,85 yang dipakai kode, dan 5 dari 14 klaim high (36%) di bawah 0,65. Ambang 0,80 yang dipakai 03 §4/10:9 mendefinisikan 36 klaim fraud; ambang 0,85 di kode hanya 25.

### Tabel severity

| Severity | Jumlah | Cakupan ringkas |
|---|---|---|
| KRITIS | 9 | Pipeline analitik nol; angka benchmark hardcode; 4 skala ambang bertentangan; 11/36 fraud di bawah ambang kode; 8 kolom anti-leakage diekspor; tidak ada API (stub hello-world); Prisma tanpa entitas domain; eksportir LOS "tidak berlaku" jadi 0; klaim DP-CTGAN tanpa bukti |
| TINGGI | 11 | Rule engine absen; 10 artefak eksperimen absen; leak konfigurasi `ignoreBuildErrors`; 0 file Python/0 test script; fusion 3 definisi berbeda; 3. ReLU vs LeakyReLU; φ₀ 0,20 vs b₀ 0,30; klaim kausal φ^(top) melanggar 02 §3.5; metric mismatch 0,9142 vs 0,91 vs 0,85; UI 7 field §3.6 tak lengkap; log audit/RBAC tak ada |
| SEDANG | 10 | θ_feat 0,75 vs 0,85; `camouflageDetected` dikontrak tapi tak diimplementasi; profil drilldown tak punya versi/threshold/override; hierarki frontend doc vs kode; `/dataset` & `/simulasi` tak terdokumentasi; Oasis KPI 100 klaim vs 300; KLM016-017 = high/review bukan fraud; narrative klaster campur; scoring tanpa versi/config |
| RINGAN | 6 | Penamaan target "fraud" vs "fraud-scenario"; "auto_clear" vs "auto-clear"; `next-auth` & `prisma` dependency mati; `reactStrictMode: false`; eksportir tanpa versi; 8 yang hilang saat revisi (DP-CTGAN, FL, AL/DPO, dst) |
| **Total** | **36** | |

---

## 2. Peta Arsitektur: As-Designed vs As-Built

```
AS-DESIGNED (02-architecture.md)                 AS-BUILT (N:\HEALTHKATHON\Aegis-JKN)
──────────────────────────────────────────         ─────────────────────────────────────────────────
[3.1 Ingest & validasi]  §17-23                  ❌ TIDAK ADA. Tidak ada worker ingest, tidak ada
  validasi tipe/rentang/kode                        validator skema, tidak ada log kesalahan.
  penanda missing / not_applicable / unknown       Persis satu jalur: data konstanta di
  identitas analitik sintetis untuk node            src/data/notion-datasets.ts:402
                                                   (300 record) → langsung dirender.

[3.2 Tier 1 - rule engine] §24-26               ❌ TIDAK ADA. Nol aturan. Nol ID/versi aturan,
  duplikasi tepat, kode tak kompatibel              nol condition, nol test case. "Rule"
  setiap aturan: ID+versi+sumber+input+             hanya ada sebagai narasi UI statis di
  kondisi+output+test case+tanggal tinjauan         src/components/mhgsl/data.ts:398-500
                                                   (FRAUD_PROFILES hardcoded).

[3.3 Tier 2 - model tabular] §27-28              ❌ TIDAK ADA. Tidak ada XGBoost/logreg, tidak ada
  fitur non-label, split+target di manifest          manifest eksperimen, tidak ada baseline yang
                                                   dapat dijalankan ulang. "XGBoost" hanya muncul
                                                   sebagai label seri benchmark (data.ts:253).

[3.4 Tier 3 - graph heterogen] §29-36           ⚠️ TIDAK DIREALISKAN - hanya ilustrasi SVG statis.
  node klaim/pasien/dokter/faskes/dx/proc/obat      12 node & 20 edge hardcoded di
  3 kanal: topologi/fitur/semantik                  src/components/mhgsl/data.ts:87-138,
  edge: arah, temporal, dasar, risiko leak          dirender ke SVG di multi-channel-graph.tsx:16-17.
  metapath terdokumentasi                          Tidak ada graph builder, tidak ada HeteroData,
  hiperparameter dipilih dari fold.train             tidak ada edge yang dihitung dari data.
                                                    20 edge statis ≠ pipeline 70+ edge (arsip 12:65).

[3.5 Fusion & penjelasan] §37-38                ⚠️ DEViasi. Tidak ada fusi 3-tier (rule+tabular+graph).
  formula fusion, threshold, kalibrasi dicatat      Hanya penjumlahan 3 heuristik di browser:
  SHAP bukan bukti kausal                             data-uploader.tsx:132
                                                    featureScore*0.38 + semanticScore*0.41
                                                      + topologyScore*(-0.12) + 0.3
                                                    SHAP = konstanta hardcode (data.ts:340 SHAP_ATTRS).

[3.6 UI verifier 7 field] §39-47                 ⚠️ DEViasi. Ada: ID (fraud-drilldown-modal.tsx:82),
  ID, triase, faktor, aturan, sumber+waktu,          faktor (evidence, :169), status/triase.
  versi+threshold, override+tindak lanjut          HILANG: aturan terpicu, sumber & waktu data,
                                                    versi model & threshold, alasan override,
                                                    status tindak lanjut. Grep "aturan|threshold|
                                                    versi|override|tindak lanjut" → 0 hit di 257 baris.

[§4 Kontrak data 8 entitas] §48-58              ❌ TIDAK ADA di skema DB. prisma/schema.prisma
  Claim/Patient/Practitioner/Org/                   hanya model User (:16) dan Post (:24).
  Condition/Procedure/Medication/Referral           src/lib/db.ts (12 baris) tidak diimpor siapa pun.

[§5 Protokol evaluasi] §59-86                   ❌ TIDAK ADA. Nol split, nol seed, nol CV,
  2 target, group split, LOFO, ablation,            nol metrik yang dihitung, nol artefak.
  8 metrik, 10 artefak wajib                        "Eksperimen" = satu array JSON konstanta.

[§6 Keamanan & operasi] §87-95                   ❌ TIDAK ADA. Nol RBAC (grep auth()/role → 0),
  RBAC, log akses, retensi, insiden, pemulihan        nol audit log (grep audit_log → 0), nol
  hash biasa bukan kontrol privasi                    environment split. next-auth ^4.24.11 terpasang
                                                    di package.json:62 tapi nol referensi di src/.

[REST API] (data-contracts.md §7)                ❌ STUB. src/app/api/route.ts (4 baris) →
  GET /api, POST /api batch                         GET {message:"Hello, world!"}. Hanya 1 file
                                                    di src/app/api/ - nol POST, nol route lain.

[Frontend] §4 system-design.md:163-200            ✅ ADA (8/12 komponen cocok) + 2 route tak
  12 komponen terender                               terpetakan di doc: /dataset (page.tsx:30
                                                    → DatasetExplorer), /simulasi (page.tsx:20
                                                    → OasisDashboard). src/app/page.tsx:4-15
                                                    mengimpor 12 komponen; DatasetExplorer,
                                                    OasisDashboard, Glossary, ShortcutsHint
                                                    tidak di-mount di sana.
```

**Stack as-built:** Next.js 16 App Router (`package.json:61`) + React 19 + TypeScript strict (`tsconfig.json:11`) + Tailwind v4 + shadcn/Radix + Recharts + framer-motion. Prisma 6 + SQLite (`prisma/schema.prisma:11-14`) terpasang tapi mati. Deploy Vercel. **Nol dependensi ML:** tidak ada `xgboost`, `torch`, `shap`, `torch-geometric` di `package.json`.

---

## 3. Tabel GAP: Komponen/Spesifikasi → Status di Kode

| # | Komponen/Spesifikasi | Lokasi di spec | Status di kode | Bukti path:line | Dampak |
|---|---|---|---|---|---|
| G-01 | Pipeline ingest + validasi skema + log kesalahan | 02-architecture.md:17-23 | **TIDAK ADA** | `src/data/notion-datasets.ts:402` (satu konstanta array); `src/app/api/route.ts:1-4` | Tidak ada jalur data masuk; ingest "berformat terdokumentasi" (03 §3.1, data-contracts §2.1) tidak dijalankan |
| G-02 | Tier 1 rule engine (duplikasi, kode inkompatibel, nilai tak masuk akal) | 02-architecture.md:24-26 | **TIDAK ADA** | grep `ruleId\|ruleVersion\|policySource` di `src/` → 0 hit; `src/components/mhgsl/data.ts:398-500` (profil hardcode) | Tidak ada `rule_flag` dengan alasan spesifik; 05 §5 in-scope "baseline rule engine" tidak terpenuhi |
| G-03 | Tier 2 model tabular + manifest eksperimen | 02-architecture.md:27-28 | **TIDAK ADA** | `package.json:5-15` (tanpa scikit/xgboost/torch); `package.json:5-15` tanpa script `test` | Baseline "dapat dijalankan ulang" (02 §7:100) mustahil - nol evaluator |
| G-04 | Graph heterogen 3 kanal, edge dihitung dari data | 02-architecture.md:29-36 | **DEVIASI** | `src/components/mhgsl/data.ts:87` (12 node), `:111` (20 edge, `kind` topologi 12/fitur 4/semantik 4); `multi-channel-graph.tsx:16-17` | Graf statis, bukan hasil perhitungan; bobot edge 0,92/0,88/0,85/0,79/0,81/0,83/0,94 (data.ts:127-130) angka konstanta, bukan cosinus pada data |
| G-05 | Hiperparameter kanal dipilih dari fold.train | 02-architecture.md:36 | **TIDAK ADA** | `src/data/oasis-data.ts:81` `theta_feat: 0.85`; `src/components/mhgsl/i18n.tsx:352,700` | θ_feat dipilih konstan di UI, tidak pernah di-validasi |
| G-06 | Fusion 3-tier (rule+tabular+graph), kalibrasi, SHAP bukan kausal | 02-architecture.md:37-38 | **DEVIASI** | `src/components/mhgsl/data-uploader.tsx:132`; `src/components/mhgsl/data.ts:340` (SHAP_ATTRS konstanta) | Tidak ada fusi rule/tabular; SHAP konstanta tanpa sumber |
| G-07 | UI verifier 7 field wajib | 02-architecture.md:39-47 | **DEVIASI** | `src/components/mhgsl/fraud-drilldown-modal.tsx` 257 baris - grep `aturan\|threshold\|versi\|override\|tindak lanjut` → 0 hit; ada `:136` metrik, `:169` evidence, `:207` timeline, `:243` rekomendasi | 5 dari 7 field wajib hilang; "alasan flag konsisten dengan input model" (02 §7:103) tak dapat diverifikasi |
| G-08 | Kontrak data 8 entitas domain | 02-architecture.md:48-58 | **TIDAK ADA** | `prisma/schema.prisma:16` (model User), `:24` (model Post) | Nol entitas Claim/Patient/Practitioner/Organization/Condition/Procedure/Medication/Referral |
| G-09 | Query/persistensi data | (implisit §4) | **TIDAK ADA** | `src/lib/db.ts:1-13`; grep `lib/db` di `src/` → 0 import; grep `fetch(` di `src/` → 0 | Lapisan data mati total; seluruh UI membaca konstanta |
| G-10 | Split group-aware, seed, LOFO, manifest split | 02-architecture.md:65-70 | **TIDAK ADA** | `find . -name "experiment_manifest.json"` → kosong; nol `.py` di repo | Tidak ada generalisasi terukur; D-02 (02:110) masih terbuka secara paksa |
| G-11 | Ablation per kanal | 02-architecture.md:71-72 | **TIDAK ADA** | `src/components/mhgsl/data.ts:253` (AUPRC 4 metode, konstanta) | Kontribusi kanal topologi/fitur/semantik tidak pernah diisolasi |
| G-12 | 8 metrik wajib (precision, recall, F1, FPR, ROC-AUC, AUPRC, kalibrasi, confusion matrix) | 02-architecture.md:73-74 | **DEVIASI** | `src/components/mhgsl/data.ts:289` (Precision/Recall/F1/AUPRC/Specificity - tanpa FPR, tanpa kalibrasi, tanpa confusion matrix), `:300` (ROC-AUC) | Metrik yang ditampilkan hanya5; kalibrasi & FPR absen padahal 00:48 menyebut FPR 10,6% |
| G-13 | 10 artefak wajib per eksperimen | 02-architecture.md:75-86 | **TIDAK ADA** | `find . \( -name "experiment_manifest.json" -o -name "train.py" -o -name "evaluate.py" -o -name "xai.py" -o -name "graph_builder.py" -o -name "edges.json" \) -not -path "./node_modules/*"` → kosong | D-03 (02:111) "reproduksi benchmark proposal" mustahil; tidak ada jejak audit |
| G-14 | REST GET /api + POST /api batch | data-contracts.md:222-264 | **DEVIASI** | `src/app/api/route.ts:3-4` → `NextResponse.json({message:"Hello, world!"})`; `find src/app/api -type f` → 1 file | Kontrak API terdokumentasi tidak ada; tidak ada inferensi server-side, seluruh MHGSL jalan di client |
| G-15 | `camouflageDetected` pada output skor | data-contracts.md:156, 260 | **TIDAK ADA** | `src/components/mhgsl/data-uploader.tsx:44-50` (ScoredRow: topologyScore/featureScore/semanticScore/fusionScore/riskLabel - tanpa `camouflageDetected`) | Sinyal "topological camouflage" (sisi inti MHGSL) tidak pernah dihitung, padahal `src/components/mhgsl/data.ts:252` menampilkan baris "Penembusan Kamuflase" |
| G-16 | Versi model & threshold di UI + 03 §4 "satu tempat, diberi versi" | 02:46, 03:46 | **DEVIASI** | `src/components/mhgsl/data-uploader.tsx:137` (0,40/0,65/0,85); `docs/api/data-contracts.md:207-213` (0,38/0,41/−0,12/0,30; θ 0,75; τ 0,65/0,85); `10-simulation-dataset.md:9,113` (0,35/0,6/0,8); `src/data/oasis-data.ts:81` (0,85) vs `docs/algorithms/mhgsl-theory.md:74` & `docs/architecture/system-design.md:106` (0,75) | 4 skala ambang berbeda hidup berdampingan; tidak ada satu pun konstanta bersama yang diimpor |
| G-17 | Penanda nilai hilang / tidak berlaku / tidak diketahui | 02-architecture.md:21, 02:99, 03:82 | **DEVIASI** | `src/types/dataset.ts:18` `losHari: number` (tanpa null/tri-state); `src/data/notion-datasets.ts` 109 baris `losHari: 0` (106 rawat jalan + 3 rawat inap, terverifikasi); `src/components/dataset/dataset-explorer.tsx:1130,2007` render "LOS 0 hr" | "Data tidak berlaku dibedakan dari data hilang" (02 §7:99) GAGAL; 3 rawat inap LOS 0 tak tertandai |
| G-18 | Anti-leakage: 8 kolom terlarang bukan fitur | 03-dataset-registry.md:84 | **DEVIASI** | `src/components/dataset/dataset-explorer.tsx:425-453` header ekspor memuat "Skor Fraud"(:441), "Risiko"(:442), "Status"(:443), "Modus"(:444), "Sindikat"(:445), "Sinyal SHAP"(:446), "Kontribusi Saluran"(:447), "Alasan Audit"(:451) | Ekspor CSV/JSON shipping 8 kolom terlarang sebagai data analisis; tidak ada daftar kolom dikecualikan |
| G-19 | Protokol ekspor 10 item (versi, checksum, seed, split ID, dll.) | 03-dataset-registry.md:86-98 | **TIDAK ADA** | `src/components/dataset/dataset-explorer.tsx:414` `handleExportClaimsCSV`, `:492` filename `aegis-jkn-claims-<tanggal>.csv`, `:505` `.json`; grep `checksum\|sha256\|seed\|split` di file itu → 0 hit | 8 dari 10 item hilang; hasil "berubah diam-diam" tidak bisa dilacak |
| G-20 | Log audit, RBAC, log akses, retensi, pemulihan | 02-architecture.md:89-93, 208-213 | **TIDAK ADA** | grep `audit_log\|review_log` di `src/` → 0; grep `auth()` → 0; `docs/architecture/system-design.md:211-213` menjanjikan "Audit Trail Immutability"; `package.json:62` `next-auth` 0 referensi | Janji di doc tidak ada padanannya; 02 §7:105 (kegagalan model tak menyebabkan penolakan otomatis) tak dapat dijamin tanpa log |
| G-21 | Hash ≠ kontrol privasi (perlindungan kunci, pembatasan akses) | 02-architecture.md:94 | **DEVIASI** | `docs/architecture/system-design.md:30` "Anonymized Hash (UU PDP No. 27/2022)", `:96` "salted SHA-256 tokenization" | Hash tanpa perlindungan kunci = persis yang dilarang 02:94; NPC tidak ada di repo |
| G-22 | Integrasi FHIR R4 / SATUSEHAT / V-Claim = tahap mendatang | 02-architecture.md:95, 05-decision-scope.md:65 | **SEBAGIAN (berlebihan)** | `docs/architecture/system-design.md:72-88` memetakan 5 FHIR Resource; `:209` "Kepatuhan Standar HL7 FHIR R4" | Dokumen sendiri menyatakan integrasi produksi adalah tahap mendatang ("out-of-scope"), namun memetakan resource seolah tersedia |
| G-23 | Confidentiality: 2 target terpisah (risk_triage vs review_action) | 02-architecture.md:60-64, 03:30 | **DEVIASI** | `src/types/dataset.ts:1-2` (`RiskLevel`, `ClaimStatus`) - dipisah di tipe; `src/data/notion-datasets.ts` memetakan risiko→status 1-1 (low→auto_clear 240, medium→review 10, high→review 14, fraud→escalate 36) | Property terpisah dijaga di tipe, tapi DIJEBRAKAN di data: 14 "high" semuanya "review", jadi 03:30 "medium dan high masih memerlukan telaah" tidak tampak |
| G-24 | Sumber & waktu data di UI | 02-architecture.md:45 | **TIDAK ADA** | `src/components/mhgsl/fraud-drilldown-modal.tsx:207` "Linimasa Anomali" (tanggal klaim, bukan timestamp ekstraksi); nol field `extractedAt`/`sourceSystem` | 7 field wajib tak lengkap |
| G-25 | Metrik benchmarkMHGSL | (02 §5.4, 00:47) | **DEVIASI** | `src/components/mhgsl/data.ts:264` AUPRC 0,91; `data.ts:289` precision 0,92; `data.ts:300` ROC-AUC 0,95; `data.ts:253` tabel 0,71/0,78/0,85/0,91; `comparison.tsx:134` Δ +0,20; `comparison.tsx:373-377` kurva epoch E1 0,71→E5 0,91; `00-dashboard.md:47` AUPRC 0,9142 & accuracy 93,0% | Angka tidak bisa direproduksi; berbeda dari angka yang tercatat di korpus sendiri (0,9142 vs 0,91) |
| G-26 | Dashboard KPI & "Status Bukti" | 00-dashboard.md:40-49 | **DEVIASI** | `src/data/oasis-data.ts:89` total_claims 100, `:90-92` fraud 14/14/100%, `:93-94` antrean 20/20%, `:95` status "SESUAI", `:97` accuracy 93, `:98` feat_edges 4563, `:108` capacity 6667, `:109` prevalensi 14 | Angka sesuai 00:47-49 (yang ditandai belum tervalidasi) tetapi disajikan sebagai KPI terverifikasi; total 100 ≠ 300 dataset aktif |
| G-27 | Klaim penghematan | 05-decision-scope.md:64, 03:37 | **DEVIASI** | `src/components/mhgsl/fraud-ring.tsx:415` "Total penghematan estimasi Rp 1,2 M / bulan (Rp 14,4 M / tahun)"; `src/components/mhgsl/data.ts:391-392` ROI 20 mnt→3 mnt, 1.000→~6.700 | 05:64 melarang klaim penghematan yang diekstrapolasi dari data sintetis; 03:37 menyatakan total nominal tidak membuktikan overcharge |
| G-28 | Provenance generator data | (03 §1, 02 §6) | **DEVIASI** | `src/components/mhgsl/i18n.tsx:524` (ID) & `:871` (EN) "dihasilkan via DP-CTGAN"; `src/components/dataset/dataset-explorer.tsx:1761` "Pelatihan model memakai generator sintetis DP-CTGAN dengan privasi diferensial"; `src/components/mhgsl/i18n.tsx:495` badge "Privacy-by-design"; `src/components/mhgsl/glossary.tsx:177-178` entri DP-CTGAN | Tidak ada generator DP-CTGAN di repo (nol `.py`, nol dependensi SDV). Klaim privasi diferensial tanpa bukti |
| G-29 | Struktur frontend sesuai doc | system-design.md:163-200 | **DEVIASI** | `src/app/page.tsx:4-15` (12 import) vs hierarki doc: tidak ada `Glossary`, `ShortcutsHint`, `DatasetExplorer`, `OasisDashboard`; `src/components/mhgsl/navbar.tsx:20-21` mengimpor ShortcutsHint+GlossaryButton, `:120,122` mount; `src/components/mhgsl/comparison.tsx:34,92` `DataUploader` ada di dalam Comparison, bukan anak langsung page | Doc §4 tidak mencerminkan app |
| G-30 | Panduan navigasi mencakup seluruh rute | docs/user-guide/navigation.md | **DEVIASI** | `docs/user-guide/navigation.md:60,73,89,106` - 4 bagian (§4.1-4.4), nol `/dataset` (`src/app/dataset/page.tsx:30`) dan nol `/simulasi` (`src/app/simulasi/page.tsx:20`) | Dua rute fungsional tak terdokumentasi |
| G-31 | Metadata rute simulasi | (truthfulness) | **DEVIASI** | `src/app/simulasi/page.tsx:7` "Hasil simulasi 300 langkah … mistral-oasis:24b"; `src/data/oasis-data.ts:86` steps 300; `:85` model "mistral-oasis:24b"; `:89` total_claims 100; feed sosial 48+48 item (`src/data/oasis-data.ts` twFeed/rdFeed) | 300 langkah padahal feed = 48+48; tidak ada pemanggilan model apa pun di repo |
| G-32 | Stigma "fraud" sebagai label triase | 02-architecture.md:42, 02:62 | **DEVIASI** | `src/components/mhgsl/data-uploader.tsx:201` "Verdict: skor ≥ 0.85 menandakan kemungkinan fraud → eskalasi ke verifikator"; `src/types/dataset.ts:1` `RiskLevel = "low" | "medium" | "high" | "fraud"` | 02 §5.1 menyebut target `fraud-scenario`; label UI "fraud" terbaca sebagai vonis (05:60 melarang vonis fraud otomatis) |
| G-33 | Build integrity | (reproduksibilitas, 02:11) | **DEVIASI** | `next.config.ts:6` `typescript.ignoreBuildErrors: true`; `tsconfig.json:11` strict true tapi `:13` `noImplicitAny: false`; `next.config.ts:8` `reactStrictMode: false` | Error TS ditolak saat build → hasil "tervalidasi" bisa saja gagal compile diam-diam |
| G-34 | Dependency management | (02:11) | **DEVIASI** | `package.json:62` `next-auth ^4.24.11` - grep `next-auth` di `src/` → 0; `package.json:65` `prisma ^6.11.1` - 1 file tak terpakai (`src/lib/db.ts`) | Beban &beban dependensi mati; menandakan auth/RBAC pernah direncanakan lalu tidak dikerjakan |
| G-35 | Eksportir claims: version & seed | 03:87-88, 08:83 | **DEVIASI** | `src/components/dataset/dataset-explorer.tsx:492,505` nama file hanya berisi tanggal; `src/data/oasis-data.ts:79-80` menyimpan `version:"v2.1"`, `seed:20260707` tetapi tidak pernah ditulis ke ekspor | Seed ada di konstanta tapi tidak menyertai artefak |
| G-36 | Klasifikasi risiko dataset v1 vs v2 | 10-simulation-dataset.md:9,113 | **DEVIASI** | `10-simulation-dataset.md:9` "<0.35 low; 0.35-0.6 medium; 0.6-0.8 high; >0.8 fraud"; `:113` "skor di bawah 0.35 low … di atas 0.8 fraud"; `src/components/mhgsl/data-uploader.tsx:137` 0,40/0,65/0,85 | Versi 100-klaim & versi 300-klaim memakai ambang berbeda tanpa versioning (03:46) |

**Ringkasan status:** 18 komponen **TIDAK ADA**, 13 **DEVIASI**, 5 **SEBAGIAN/berlebihan**, 0 **lengkap sesuai spec**. Tidak ada satu pun baris pipeline analitik (G-01 s.d. G-13) yang terimplementasi.

---

## 4. Temuan Internal Spec & Kontrak

### 4.1 Empat skala ambang yang hidup berdampingan

| Sumber | Lokasi | Ambang |
|---|---|---|
| Kode uploader | `src/components/mhgsl/data-uploader.tsx:137` | `>= 0.85 fraud : >= 0.65 high : >= 0.40 medium : low` |
| Kontrak API | `docs/api/data-contracts.md:211-213` | `θ_feat 0.75`, `τ_high 0.65`, `τ_fraud 0.85` |
| Teori MHGSL | `docs/algorithms/mhgsl-theory.md:74` | `θ_feat = 0.75` |
| Dokumen sistem | `docs/architecture/system-design.md:106` | `θ_feat = 0.75` |
| Data Oasis | `src/data/oasis-data.ts:81` | `theta_feat: 0.85` |
| i18n (ID/EN) | `src/components/mhgsl/i18n.tsx:352,700` | `θ_feat = 0.85` |
| Teks UI fraud | `src/components/mhgsl/data.ts:481` | `θ_feat = 0.85` |
| Dashboard Oasis | `src/components/oasis/oasis-dashboard.tsx:685` | `kosinus ≥ 0.85` |
| Katalog v1 | `10-simulation-dataset.md:9,113` | `<0.35 / 0.35-0.6 / 0.6-0.8 / >0.8` |
| Registry (final) | `03-dataset-registry.md:46` | skor 0,80 **sudah** fraud di DB aktif |

Dampak terukur pada dataset aktif (`src/data/notion-datasets.ts`, 300 record):
- 36 klaim `risiko:"fraud"`; skor Fraud **0,80–0,95**. **11 record bernilai 0,80–0,84** → di bawah ambang 0,85 kode. 1 record tepat 0,80 (batas kasus yang memisahkan definisi ">0.8" vs "≥0.80").
- 14 klaim `risiko:"high"`; skor 0,62–0,79. **5 record bernilai 0,62–0,64** → di bawah ambang 0,65 kode.
- 240 `low` 0,04–0,14; 10 `medium` 0,40–0,53 (semua ≥ 0,40, jadi konsisten).

Artinya: **hanya 25 dari 36 klaim fraud terbaca fraud** oleh ambang yang dipakai kode, dan 9 dari 14 "high" terbaca "medium". 03:46 sendiri menyatakan ambang harus "disimpan di satu tempat dan diberi versi" - belum terjadi.

### 4.2 Leakage: dua arah

- **Ke luar (ekspor):** `dataset-explorer.tsx:425-453` menyalin 8 kolom terlarang 03:84 tanpa daftar pengecualian. Tidak ada checksum/seed/split ID (03 §8 butir 1-10 → 8 hilang).
- **Ke dalam (fitur):** `data-uploader.tsx:100-137` menghitung skor dari konsentrasi dokter+faskes, kemiripan avg (LOS, biaya, obat), dan kombinasi dx/prosedur. Tidak ada kolom label yang bocor - **tetapi** `fraud-drilldown-modal.tsx:169` dan `data.ts:340` menampilkan bobot SHAP konstanta yang secara semantik identik dengan bobot fusi, jadi pembaca menyalahartikan bobot hardcode sebagai hasil hitung.
- **Konsumen dataset:** `src/data/notion-datasets.ts:402` exporting 300 record yang **sudah** memuat Skor Fraud, Risiko, Status, Modus, Sindikat, Sinyal SHAP, Kontribusi Saluran, Alasan. Produksi data aktif sama dengan data uji - tidak ada pemisahan.

### 4.3 Versioning & konfigurasi

Tidak ada file konfigurasi ambang tunggal. `src/data/oasis-data.ts:79-86` adalah satu-satunya tempat yangmemiliki punya metadata (`version "v2.1"`, `seed 20260707`, `theta_feat 0.85`, `gamma_text 0.1`, `steps 300`) - tetapi **tidak diimpor** oleh `data-uploader.tsx`, `simulation.tsx:73`, `oasis-dashboard.tsx:685`, `i18n.tsx:352,700`, atau `data.ts:481`. Enam salinan ambang decentralized.

### 4.4 Kontrak `docs/api/data-contracts.md` vs kode

| Kontrak | Baris | Kenyataan kode |
|---|---|---|
| `GraphNode.profileId` | `:113` | `src/components/mhgsl/data.ts:68-76` `GraphNode` **tanpa** `profileId` |
| `ScoredClaimOutput.camouflageDetected` | `:156`, `:260` | `data-uploader.tsx:44-50` `ScoredRow` **tanpa** field itu |
| `GET /api` health | `:224-236` | `src/app/api/route.ts:3-4` → `{message:"Hello, world!"}` |
| `POST /api` batch | `:238-264` | **tidak ada** handler POST di repo |
| Versi rilis `v0.2.1` | `:203` | `package.json:3` versi `1.1.0` |
| Bobot fusi | `:207-213`, `:217` | `data-uploader.tsx:132` cocok angkanya, tapi 3 definisi fusi berbeda antar dok (lihat §5) |

### 4.5 Klaim teknis tanpa benchmark

Semua angka berikut **konstanta literal** di komponen, tanpa eksekusi model, tanpa skrip, tanpa artefak:

| Klaim | Lokasi | Bukti bahwa bukan hasil ukur |
|---|---|---|
| AUPRC 0,91 | `data.ts:264` | konstanta dalam array `AUPRC_DATA` |
| AUPRC 0,71/0,78/0,85/0,91 (4 metode) | `data.ts:253` | string literal |
| Precision 0,92 / Recall 0,90 / F1 0,91 / Spec 0,96 | `data.ts:289` | literal |
| ROC-AUC 0,95 | `data.ts:300` | literal |
| Δ MHGSL vs XGBoost +0,20 | `comparison.tsx:134` | literal |
| Kurva epoch E1 0,71 → E5 0,91 | `comparison.tsx:373-377` | 5 titik literal, 5 epoch tanpa trainer |
| Akurasi 93%, deteksi 100%, antrean 20% | `oasis-data.ts:92,93,94,97` | literal |
| 4.563 edge feature | `data.ts:514`, `oasis-data.ts:98`, `oasis-dashboard.tsx:685` | literal; graf as-built hanya 4 edge fitur (`data.ts:127-130`) |
| syndicateHitRate 100% | `data.ts:518` | literal |
| Kapasitas 6.667 klaim | `oasis-data.ts:108` | literal |
| Telaah 20→3 mnt, 1.000→~6.700 | `data.ts:391-392` | literal |
| Penghematan Rp 1,2 M/bulan | `fraud-ring.tsx:415` | literal, tanpa tarif pembanding (03:37) |
| AUPRC +20%, false negatives −42% | `dataset-explorer.tsx:1800` | literal |
| 2.000.000 klaim/hari, ±1.000 verifikator, +20% AUPRC | `data.ts:20,21,23` | literal |
| "Privacy-by-design" badge | `i18n.tsx:495` | tanpa generator DP-CTGAN di repo |

Bandingkan 00-dashboard.md:46-49 - angka yang sama **dinyatakan belum boleh disebut hasil tervalidasi**; dan 02 §5.5 (baris 75-86) mewajibkan 10 artefak per eksperimen; **nol artefak ada**.

---

## 5. Inkonsistensi `docs/` vs Spec

### 5.1 `docs/algorithms/mhgsl-theory.md` vs `02-architecture.md` & `docs/api/data-contracts.md`

| Isu | theory | contracts | system-design | Masalah |
|---|---|---|---|---|
| θ_feat | 0,75 (`:74`) | 0,75 (`:211`) | 0,75 (`:106`) | kode/UI 0,85 →G-16 |
| Aktivasi | LeakyReLU slope 0,2 (`:159`) | - | ReLU (`:118`) | Dua fungsi aktivasi berbeda untuk model yang sama |
| Definisi fusi | Concat 4-dimensi + Sigmoid (`:180-186`) | weighted sum (`:217`) | "Attention-Based Fusion" (`:60`, `:142`) | **Tiga definisi fusi berbeda.** Kontrak tidak punya concat; system-design tidak punya Attention |
| SHAP dekomposisi | + `φ^(shared)` (`:206`) | - | tanpa `φ^(shared)` (`:156`) | Term differen → dekomposisi tidak reproducible |
| Base value | φ₀ = 0,20 (`:229`) | b₀ = +0,30 (`:210`) | - | 0,10 absolut pada skor akhir |
| τ_fraud | ≥ 0,85 (`:220`) | 0,85 (`:213`) | - | 03:46 → fraud mulai 0,80 |
| Klaim kausal | "Kehadiran φ^(top) = −0,12 **secara matematis membuktikan adanya upaya kamuflase aktif**" (`:236`) | - | "sistem memicu tanda bahaya Topological Camouflage Signature" (`:159`) | **Melanggar 02:38 "SHAP tidak boleh digambarkan sebagai bukti kausal."** Botserta "## 5.4" |
| Contoh hitung | ŷ = 0,20 −0,12 +0,38 +0,41 +0,07 = 0,94 (`:234`) | - | - | Angka 0,07 tanpa sumber; tidak cocokkan 0,30 + … |

### 5.2 `docs/architecture/system-design.md`

- `:30` + `:96` menjanjikan "Anonymized Hash" / "salted SHA-256" - 02:94 melarang hash biasa sebagai pengganti kontrol privasi; tidak ada proteksi kunci/NPC di repo (G-21).
- `:72-88` memetakan 5 FHIR Resource; `:209` "Kepatuhan Standar HL7 FHIR R4" - 02:95 & 05:65 menetapkan integrasi produksi sebagai tahap mendatang. (R4 memang benar di `:72` & `:209`; tidak ada klaim R5.)
- `:163-200` hierarki frontend tidak memuat `/dataset`, `/simulasi`, `Glossary`, `ShortcutsHint` (G-29).
- `:211-213` "Audit Trail Immutability" - nolimplementasi (G-20).
- `:106` θ_feat 0,75 vs `:94-112` Stage-2 naratif yang menyebut nilai berbeda; `:118` ReLU vs `:129-140` shared-GCN stage tanpa aktivasi konsisten.

### 5.3 `docs/api/data-contracts.md`

- `:203` "rilis `v0.2.1`" vs `package.json:3` versi `1.1.0` vs `src/data/oasis-data.ts:79` `"v2.1"` - tiga nomor versi hidup berdampingan tanpa peta.
- `:213` "τ_fraud = batas ambang **rekomendasi penolakan**" - 05:60-61 melarang penolakan/pemotongan otomatis; kata "penolakan" di kontrak/API bertentangan dengan batasan scope.
- `:156` `camouflageDetected` ada di kontrak tapi nol implementasi (G-15).

### 5.4 `docs/user-guide/navigation.md`

`:60,73,89,106` - 4 bagian; nol panduan `/dataset` dan `/simulasi` (G-30).

---

## 6. Yang Hilang Saat Revisi vs Arsip (12-archive-architecture.md)

Rev 1.0 menghapus komponen teknis berikut. Yang hilang = regresi potensial, karena mekanisme yang hilang justru **yang membuktikan klaim**.

| Konsep arsip | Bukti arsip | Status di Rev 1.0 / repo | Risiko regresi |
|---|---|---|---|
| **DP-CTGAN** sebagai generator data sintetis | `12-archive-architecture.md:57, 92-93, 111, 192` | Tidak ada generator; **tapi UI masih mengklaim data "dihasilkan via DP-CTGAN"** (`i18n.tsx:524,871`; `dataset-explorer.tsx:1761`) | Klaim privasi diferensial tanpa bukti - menyusunkerugian reputasi di seleksi |
| **Federated Learning** | `:94-95` | Dihapus total | Skala nasional perlu didiskusikan ulang |
| **Active Learning / DPO** (umpan balik reviewer) | `:97-99` | Dihapus total | Mekanisme `review_log`/umpan balik 02 §3.6 hilang bersamanya |
| **`configs/leakage.yaml`** | `:47, 66, 140, 157, 189` | **Hilang** - nol file | Tidak ada blocklist kolom terlarang; 8 kolom justru diekspor (G-18) |
| **`tests/test_leakage.py`** | `:47, 141, 174, 180` | **Hilang** - nol file `.py` | Anti-leakage tak teruji otomatis; 03:84 jadi Keynote saja |
| **Repeat CV ≥10 seed** | `:48` | Dihapus; nol split | Varian antar-fold tak terukur (n=300) |
| **Build graf `HeteroData` + `edges.json` (70+ edge)** | `:49, 65` | Dihapus; as-built 20 edge statis (`data.ts:111`) | Kanal fitur/semantik tak pernah dihitung dari data |
| **AUPRC pada prevalensi 3-7% (downsampling)** | `:50, 142` | Dihapus | AUPRC 0,91 pada prevalensi 12% bias; 03:100 menyatakan 12% bukan prevalensi aktual |
| **Kriteria penerimaan ≥90% fraud & antrean ≤20%** | `:112, 131, 181` | Dihapus; sebagai angka statis di `oasis-data.ts:92-94` | Kriteria tidak lagi terukur, hanya di-hardcode sebagai "SESUAI" |
| **Paired t-test AUPRC/AUROC ≥ baseline** | `:182` | Dihapus | Klaim "+0,20" (`comparison.tsx:134`) tanpa uji signifikansi |
| **Per-sindikat hit-rate > 0** | `:183` | Dihapus | `data.ts:518` `syndicateHitRate: 100` - angka global tanpa hit-rate per sindikat |
| **Konsistensi SHAP vs Alasan** | `:184` | Dihapus | `data.ts:340` SHAP konstanta; tidak ada `Alasan` yang bisa diuji konsisten |
| **8 klaim kontradiksi masuk prioritas** (`text_processor.py`) | `:185` | Dihapus | `data.ts` SHAP_ATTRS/`FRAUD_PROFILES` hardcode 4-5 profil |
| **Rencana 8-minggu bertahap** | `:187-193` | Diganti roadmap UI | Tidak ada gate artefacts per fase |
| **Skema ingestion FHIR R4 + baseline XGBoost+SMOTE** | `:120`, `notion-datasets.ts:71` | Tidak ada implementasi |urfaces di roadmap UI sebagai "terjadwal" |

**Catatan**: sebagian penghapusan memang benar (arsip `:108,111,112,116,131,133` memuat klaim berlebihan dan "terbukti" yang berlebihan; `:97-99` Active Learning terlalu dini untuk MVP). Yang bermasalah adalah penghapusan **mekanisme pembuktian** (leakage guard, repeat CV, builder edge, uji signifikansi, artefak) sementara **angkanya dipertahankan sebagai konstanta UI** - persis kebalikan dari 02:8 ("Dokumen tidak menyatakan bahwa seluruh komponen … telah diterapkan") dan 00:46.

---

## 7. Rekomendasi Terurut

**P0 - sebelum demo/seleksi (hari–minggu):**
1. **Turunkan semua angka benchmark dari UI ke mode "simulasi sintetis"** (`data.ts:253,264,289,300`; `comparison.tsx:134,373-377`; `oasis-data.ts:92-94,97,108`; `data.ts:391-392,514,518`; `fraud-ring.tsx:415`; `dataset-explorer.tsx:1800`). Ganti label "AUPRC 0,91"/"Fraud Terkonfirmasi" menjadi "nilai contoh ilustrasi". Tanpa ini, satu klaim "hasil tervalidasi" saja sudahimaging bohong. → 02:8, 00:46, 05:64
2. **Kunci satu berkas ambang** `src/config/thresholds.ts` (versi, seed, τ, θ, γ) lalu impor di `data-uploader.tsx:137`, `simulation.tsx:73`, `oasis-data.ts:81`, `i18n.tsx:352,700`, `data.ts:481`, `oasis-dashboard.tsx:685`; samakan dengan `03:46` (fraud ≥ 0,80). Verifikasi ulang: 11/36 fraud dan 5/14 high akan bergeser kelas. → 03:46
3. **Hapus atau turunkan klaim DP-CTGAN** di `i18n.tsx:524,871`, `dataset-explorer.tsx:1761`, `glossary.tsx:177-178`, badge `i18n.tsx:495`, sampai ada generator sungguhan. → 03:1, 02:6
4. **Hapus 8 kolom terlarang dari ekspor** `dataset-explorer.tsx:425-453` (Skor Fraud/Risiko/Status/Modus/Sindikat/Sinyal SHAP/Kontribusi Saluran/Alasan Audit) atau beri header eksplisit "KOLOM_LABEL_TIDAK_BOLEH_DIPAKAI_SEBAIAGI_FITUR"; tambahkan blokir(kernel) di `data-uploader.tsx:60-77`. → 03:84, 08:22
5. **Perbaiki 7 field UI §3.6** di `fraud-drilldown-modal.tsx`: `ruleTriggered` (ID+versi+source+condition), `dataSource` + `extractedAt`, `modelVersion` + `thresholdVersion`, `overrideReason` + `followUpStatus`, plus `triaseCategory` (bukan "fraud"). → 02:39-47
6. **Hapus klaim "Cumulative node" yang tidak dapat dibuktikan** - `oasis-dashboard.tsx:685` "4.563 edge" vs 4 edge fitur as-built (`data.ts:127-130`); `oasis-data.ts:98`. → 02:36

**P1 - dua minggu (agar spec bisa diuji):**
7. **Bangun pipeline evaluasi minimal** (Python atau TS): `leakage.yaml`/`leakage.ts` blocklist 8 kolom + `test_leakage` (arsip `:140-141`), `train.py`/`evaluate.py` (baseline XGBoost + graph-only + fusion), GroupKFold by faskes/pasien, seed tetap, 10 artefak 02 §5.5 (`experiment_manifest.json`, `metrics.json`, split IDs, per-klaim prediction, confusion matrix, error analysis, limitations). → 02:75-86, 08:29-35
8. **Implementasikan `camouflageDetected`** di `data-uploader.tsx:44-50` sesuai kontrak `data-contracts.md:156` (topology rendah + feature/semantik tinggi) - ini inti klaim MHGSL yang saat ini nol. → G-15
9. **Terapkan tri-state LOS** `src/types/dataset.ts:18` (`number | null` + `not_applicable | unknown`), tandai 109 baris `losHari: 0` (`notion-datasets.ts`), dan render "N/A" di `dataset-explorer.tsx:1130,2007`. → 02:21, 03:78-82, 02:99
10. **Isi 10 item ekspor** di `dataset-explorer.tsx:414,492,505`: nama+versi dataset, waktu ekspor, jumlah baris, checksum SHA-256, kamus data, daftar kolom dipakai/dikecualikan, definisi target+ambang, aturan pembersihan, ID split train/val/test, seed+versi kode. → 03:86-98
11. **Samakan tiga definisi fusi** (theory `:180-186` concat vs contracts `:217` weighted sum vs system-design `:60` attention) dan satu aktivasi (theory `:159` LeakyReLU vs system-design `:118` ReLU); selaraskan φ₀ (`:229` 0,20) vs b₀ (`:210` 0,30) dan term `φ^(shared)` (`:206` vs `:156`). → §5.1
12. **Hapus kalimat bukti kausal** `mhgsl-theory.md:236`; ganti "menunjukkan pola yang konsisten dengan kamuflase topologi, tidak membuktikan kausalitas" (02:38). → 02:38

**P2 - satu bulan (membuka reverence MVP):**
13. **Implementasikan API sesuai kontrak**: `GET /api` health + `POST /api` batch di `src/app/api/route.ts` (ganti stub), aturan validasi §2.1 (tipe, rentang, kode), dan `ScoredClaimOutput` lengkap. → G-14, data-contracts:222-264
14. **Bangun rule engine Tier 1** yang menghasilkan `rule_flag` + alasan spesifik, tiap aturan dengan ID/versi/sumber/input/kondisi/output/test-case/tanggal-tinjauan; registry aturan sebagai data, bukan narasi UI. → 02:24-26
15. **Realisasi entitas domain** di `prisma/schema.prisma` (Claim/Patient/Practitioner/Organization/Condition/Procedure/Medication/Referral) atau hapus Prisma+`next-auth` bila demo murni statis. → G-08, G-34
16. **Terapkan kontrol akses & audit log** minimal untuk demo: RBAC, `audit_log` append-only (aksi reviewer + alasan override), log akses & retensi; hapus klaim "Audit Trail Immutability" (`system-design.md:211-213`) sampai ada. → 02:90,93
17. **Tambahkan rule engine & gate artefak ke MVP acceptance** 02 §7 (`:96-106`) sebagai checklist yang bisa di-check, dan tutup D-01/D-02/D-03 (`02:109-111`) dengan artefak nyata, bukan konstanta.
18. **Selaraskan docs**: `system-design.md:163-200` (frontend hierarchy + 2 route), `navigation.md` (§4.5 & §4.6 untuk `/dataset`, `/simulasi`), `data-contracts.md:203` (versi rilis vs `package.json:3` vs `oasis-data.ts:79`), `data-contracts.md:213` (hapus kata "rekomendasi penolakan" → "rekomendasi telaah"), dan 3 router yang tidak terpetakan di `system-design.md`.
19. **Kembalikan proteksi yang hilang dari arsip** secara bertahap: `leakage.yaml` + test (P1 #7) → repeat CV ≥10 seed → AUPRC pada prevalensi 3-7% → per-sindikat hit-rate → paired t-test. → 12:47-50, 178-186
20. **Tambahkan `npm test` dan matikan `ignoreBuildErrors`** (`next.config.ts:6`), aktifkan `noImplicitAny` (`tsconfig.json:13`). → 02:11 (reproduksibilitas)

---

## Lampiran A - Ringkasan Perintah Verifikasi

```
# 1. API stub
find src/app/api -type f                                  → src/app/api/route.ts (1 file)
cat -n src/app/api/route.ts                              → 4 baris, GET {message:"Hello, world!"}

# 2. Skema DB
cat -n prisma/schema.prisma                              → model User(:16), model Post(:24), sqlite(:12)
grep -rn "lib/db" src/ | wc -l                           → 0
grep -rn "next-auth" src/ | wc -l                        → 0
grep -rn "fetch(" src/ | wc -l                           → 0

# 3. Artefak ML yang diwajibkan 02 §5.5
find . -name "*.py" -not -path "./node_modules/*"         → (kosong)
find . \( -name "experiment_manifest.json" -o -name "train.py" -o -name "evaluate.py" \
       -o -name "xai.py" -o -name "graph_builder.py" -o -name "edges.json" \
       -o -name "leakage*" \) -not -path "./node_modules/*" → (kosong)
ls tests/                                                → 3 file .sh runtime, nol test unit
grep '"test"' package.json                                → (tidak ada)

# 4. Ambang
sed -n '137p' src/components/mhgsl/data-uploader.tsx     → >=0.85 fraud : >=0.65 high : >=0.40 medium
sed -n '81p'  src/data/oasis-data.ts                      → theta_feat: 0.85
sed -n '74p'  docs/algorithms/mhgsl-theory.md            → θ_feat = 0.75
sed -n '106p' docs/architecture/system-design.md         → θ_feat = 0.75
sed -n '211,213p' docs/api/data-contracts.md             → θ_feat 0.75 / τ_high 0.65 / τ_fraud 0.85
sed -n '9p;113p' "N:/HEALTHKATHON/analysis/corpus/10-simulation-dataset.md" → <0.35 / >0.8

# 5. Impact ambang pada dataset aktif (node parse 300 record src/data/notion-datasets.ts)
fraud: 36 record, skor 0.80–0.95 → 11 record (0.80–0.84) < 0.85 ; 1 record tepat 0.80
high : 14 record, skor 0.62–0.79 → 5 record (0.62–0.64) < 0.65
low  : 240 record, 0.04–0.14 | medium: 10 record, 0.40–0.53

# 6. Anti-leakage di eksportir
sed -n '425,453p' src/components/dataset/dataset-explorer.tsx
  → :441 Skor Fraud, :442 Risiko, :443 Status, :444 Modus, :445 Sindikat,
    :446 Sinyal SHAP, :447 Kontribusi Saluran, :451 Alasan Audit
grep -c "checksum\|sha256\|seed\|split" src/components/dataset/dataset-explorer.tsx → 0

# 7. LOS
grep -n "losHari" src/types/dataset.ts                   → :18 losHari: number
node parse 300 record → losHari==0 : 109 (rawat jalan 106 + rawat inap 3)

# 8. 7 field UI §3.6
grep -n "aturan\|threshold\|versi\|override\|tindak lanjut" \
     src/components/mhgsl/fraud-drilldown-modal.tsx       → 0 hit (257 baris)

# 9. Graph statis
node parse src/components/mhgsl/data.ts                  → 12 node, 20 edge (topology 12, feature 4, semantic 4)
grep -n "MHGSL_NODES\|MHGSL_EDGES" src/components/mhgsl/multi-channel-graph.tsx → :16, :17

# 10. Field kontrak yang tak diimplementasi
grep -n "profileId" src/components/mhgsl/data.ts          → 0 (kontrak data-contracts.md:113)
grep -n "camouflageDetected" src/components/mhgsl/data-uploader.tsx → 0 (kontrak :156, :260)
```

## Lampiran B - Hal yang Diverifikasi BENAR (bukan temuan)

Agar laporan ini tidak dibaca sebagai menyeverything, berikut butir yang **tetap konsisten** dan tidak perlu tindakan:

- Distribusi dataset aktif: 300 ID unik KLM001–KLM300; risiko low 240 / medium 10 / high 14 / fraud 36; status auto_clear 240 / review 24 / escalate 36 - cocok `03-dataset-registry.md:17-29` dan `10-simulation-dataset.md:113`.
- Total nominal Rp3.526.650.000 dengan pecahan per status cocok `03:31-37` (dihitung ulang dari 300 record).
- Kualitas data: 1 `Alasan` kosong (KLM031, risiko low/status auto_clear), `Modus` null ×240, `Sindikat` null ×264, LOS kosong/0 ×109 - cocok `03:73-81`.
- Polaritas `Skor Sentimen` **terdefinisi dan tidak tumpang tindih**: negatif 72 (−0,9…−0,3), netral 58 (0,05…0,15), positif 170 (0,6…0,85) - memenuhi `03:69-70`.
- `cosine(KLM016, KLM017)` = 1,0000 bila dihitung dengan formula yang sama persis seperti `data-uploader.tsx:117` - **dapat direproduksi**, bukan angka karangan (tetapi klaim "cloning tertangkap" di `oasis-dashboard.tsx:685` menyalahartikan label: kedua klaim berlabel `high`/`review`, bukan `fraud`).
- `mhgsl-theory.md` memakai **HL7 FHIR R4** (bukan R5) di `system-design.md:72,209` - konsisten dengan 02:95.
- Sisa dokumen yang diperiksa: `02-architecture.md` 115 baris, `03-dataset-registry.md` 110, `05-decision-scope.md` 76, `08-training-protocol.md` 83, `00-dashboard.md` 94, `10-simulation-dataset.md`, `12-archive-architecture.md` 193.
