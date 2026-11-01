import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = 'N:/HEALTHKATHON/analysis/reports/00-EXECUTIVE-SUMMARY.md'
lines = open(P, encoding='utf-8').read().split('\n')

act_start = next(i for i, l in enumerate(lines) if l.startswith('| Prioritas | Aksi | Owner |'))
end = act_start
while end < len(lines) and lines[end].strip().startswith('|'):
    end += 1

old = []
for l in lines[act_start:end]:
    if l.startswith('|---') or l.startswith('| Prioritas |'):
        continue
    old.append(l)
print('current action rows:', len(old))
for l in old:
    print('   ', l.split('|')[1].strip(), l.split('|')[2].strip()[:60])

# rebuild the table body from scratch: 10 rows
NEW = [
    (1, 'Unduh Participant Guide secara manual (SharePoint 403 untuk bot) dan petakan daftar berkas wajib Submit project akhir; '
        'verifikasi akun portal Healthkathon termasuk 2FA', 'Tim',
        '`10-competition.md:404,406,457` (C13, C15) dan `22-proposal-docx-audit.md:81-83` (F-40)', '2 jam', '23 Okt 2026'),
    (2, 'Bangun ulang dokumen proposal DOCX dari skrip repo, kembalikan 7 gambar atau hapus seluruh entri Daftar Gambar, tambahkan field '
        'PAGE pada footer, dan dokumentasikan atau hilangkan jalur build kedua', 'Dev',
        '`22-proposal-docx-audit.md:49-59,295-297` (F-39)', '8 jam', '24 Okt 2026'),
    (3, 'Tambahkan kernel proposal yang hilang: abstrak, daftar singkatan, identitas bertanda tangan, protokol eksperimen ringkas, '
        'metode statistik, batasan eksplisit, dan penanda sitasi untuk 18 rujukan; atau pangkas daftar pustaka menjadi yang dirujuk',
        'Tim', '`22-proposal-docx-audit.md:71-92,305-308` (F-40)', '8 jam', '26 Okt 2026'),
    (4, 'Buang seluruh angka yang tidak reproducible dari naskah, deck, dan UI: 93,0%, 94,12%, 0,9825, 0,9142, 0,71, 89,4%, 10,6%, '
        '45%, 3,2x, SUS 82,5, rasio 1:15, override 12,4%, Rp507.370.000, dan Rp14,4 M; kualifikasi 93% sebagai akurasi leksikon sentimen '
        '(186 dari 200 uji); bila FPR 10,6% masih dipakai, wajib disebut bersamaan dengan presisi 56,25% pada ambang 0,14, dan '
        'tambahkan AUPRC acak 0,12 sebagai pembanding', 'Frontend + Tim',
        '`10-competition.md:464`; `16-red-team.md:320`; `21-numbers-of-record.md:72-80`; `22-proposal-docx-audit.md:190-205`',
        '6 jam', '24 Okt 2026'),
    (5, 'Hapus ground truth dari bundle: buang `gtSent`, `sentiment_gt`, `syndHit` dari `public/payload-aegis-jkn.json`, perbaiki '
        '`innerHTML` tanpa escaping seragam di `dashboard-aegis-jkn.html`, dan blokir 8 kolom terlarang di eksportir CSV', 'Dev',
        '`09-security.md:309,319`; `16-red-team.md:61-62`; `08-frontend.md:217`', '4 jam', '25 Okt 2026'),
    (6, 'Perbaiki rujukan hukum di corpus dan naskah DOCX: judul resmi Permenkes 16/2019, hapus HL7 FHIR R4 dari dasar Permenkes '
        '24/2022 dan arahkan ke Pasal 10 ayat (4) plus Permenkes 18/2022, koreksi Pasal 65 dan 66 menjadi 67 dan 68, "3x24 jam" ke '
        'Pasal 46 ayat (1), "Data Pribadi Spesifik" ke Pasal 4 ayat (2), hapus HIPAA, dan tambahkan Pasal 34 sebagai deliverable DPIA',
        'Tim', '`11-compliance.md:413-417,431`; `05-evidence.md:126-127`; `22-proposal-docx-audit.md:244-255`', '5 jam', '25 Okt 2026'),
    (7, 'Tulis definisi label final dengan satu fungsi ambang tunggal di satu file konfigurasi, kunci ambang 0,80 secara inklusif dengan '
        'kasus batas KLM115, hapus tiga skala ambang yang tersisa, dan regenerate Tabel 7.2 DOCX beserta nominal sindikat dan peringkat '
        'modus dari CSV', 'Tim data', '`04-data-quality.md:365,368`; `15-code-quality.md:25`; `19-consistency.md:554`; '
        '`22-proposal-docx-audit.md:134-166`', '8 jam', '26 Okt 2026'),
    (8, 'Bangun pipeline evaluasi minimal beserta artefak wajibnya: split GroupKFold pada `Pasien` plus LOGO pada `Faskes`, hitung '
        'adjacency dan scaler di dalam fold, seed 20260707, satu file prediksi held-out, satu skrip metrik, `experiments/manifest.json`, '
        'serta `tests/test_leakage.py` dan `configs/leakage.yaml` yang benar-benar ada', 'ML',
        '`10-competition.md:392-393,461`; `06-graph-mhgsl.md:329,376-400,457-461`; `15-code-quality.md:16,446`; '
        '`20-repo-artifact-integrity.md:90-91`', '16 jam', '28 Okt 2026'),
    (9, 'Perbaiki angka dan kode yang tampil di layar dan di naskah: 240 rawat inap dan 60 jalan menjadi 189 dan 111, 8 dari 8 '
        'kontradiksi menjadi 12, 14 edge berlebih menjadi 13, Rp 3,53 M menjadi Rp 3,53 Miliar, label 00,66 dan 93,90, insulin glargine '
        'di FORNAS, selisih 1000 kali pada `i18n.tsx:791`, dan pemisah desimal titik menjadi koma', 'Frontend + Tim',
        '`18-ux.md:369`; `08-frontend.md:214-218`; `11-compliance.md:38-40,306,314,333`; `21-numbers-of-record.md:212`; '
        '`22-proposal-docx-audit.md:209-229`', '6 jam', '27 Okt 2026'),
    (10, 'Buat video demo 3-5 menit (voice-over, alur upcoding sampai drilldown, keputusan), deck maksimal 10 slide tanpa angka yang '
         'belum reproducible, arahkan demo ke 300 klaim, perbaiki URL Vercel dan URL clone di README, dan selaraskan klaim dataset '
         '300 versus 100 di dalam naskah', 'Tim + Dev',
         '`10-competition.md:400-403,463,467` (C9-C12, P0-7, P0-11); `22-proposal-docx-audit.md:279`', '10 jam', '30 Okt 2026'),
]

body = ['| Prioritas | Aksi | Owner | Sumber temuan | Estimasi effort | Deadline |', '|---|---|---|---|---|---|']
for p, aksi, owner, src, effort, dl in NEW:
    body.append('| %d | %s | %s | %s | %s | %s |' % (p, aksi, owner, src, effort, dl))

NOTE = [
    '',
    'Dua butir P1 tetap berada di luar tabel 10 teratas dan tidak boleh terlupakan: rotasi token Notion di Integrations dengan '
    'penggantian literal di lima file skrip menjadi pembacaan environment variable, plus penambahan `Notion-docs\\` dan `analysis\\` ke '
    '`.gitignore` (`20-repo-artifact-integrity.md:139-140,182,217-219`, tenggat 28 Okt 2026); serta matikan '
    '`typescript.ignoreBuildErrors` sambil menambahkan `npm run typecheck` sebagai gate (`15-code-quality.md:18,226`, tenggat 28 Okt 2026). '
    'Keduanya murah, tetapi keduanya Kearifan.',
]

lines[act_start:end] = body + NOTE
open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('action table rebuilt with', len(NEW), 'rows')
