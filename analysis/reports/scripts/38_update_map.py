import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = 'N:/HEALTHKATHON/analysis/reports/00-EXECUTIVE-SUMMARY.md'
lines = open(P, encoding='utf-8').read().split('\n')

# ---- 1. rebuild the source map section from the actual F-row citations ----
frows = [l for l in lines if re.match(r'^\| F-\d\d ', l)]
f2src = {}
for l in frows:
    fid = l.split('|')[1].strip()
    srcs = re.findall(r'`([0-9A-Za-z\-_]+\.md):', l)
    f2src.setdefault(fid, set()).update(srcs)

rep2f = {}
for l in frows:
    fid = l.split('|')[1].strip()
    for m in re.finditer(r'`([0-9A-Za-z\-_]+\.md):', l):
        rep2f.setdefault(m.group(1), set()).add(fid)

start = next(i for i, l in enumerate(lines) if l.startswith('| Laporan | Temuan yang disumbangkan'))
end = next(i for i, l in enumerate(lines[start:], start) if not l.strip().startswith('|'))
order = sorted(rep2f, key=lambda f: (not f.startswith('0'), f))
newmap = ['| Laporan | Temuan yang disumbangkan | Jumlah |', '|---|---|---|']
for f in order:
    ids = sorted(rep2f[f], key=lambda x: int(x.split('-')[1]))
    newmap.append('| `%s` | %s | %d |' % (f, ', '.join(ids), len(ids)))
lines[start:end] = newmap
print('source map rebuilt:', len(order), 'reports')

# ---- 2. methodology item 1: 23 -> 24 ----
for i, l in enumerate(lines):
    if l.startswith('1. Polling laporan dijalankan'):
        lines[i] = l.replace('23 laporan', '24 laporan')
        lines[i] = lines[i].replace(
            'Laporan dengan nomor 21 ada dua berkas, yaitu `21-colab-dashboard-provenance.md` dan `21-numbers-of-record.md`.',
            'Laporan dengan nomor 21 ada dua berkas, yaitu `21-colab-dashboard-provenance.md` dan `21-numbers-of-record.md`, '
            'dan satu laporan lagi bernomor 22, yaitu `22-proposal-docx-audit.md` yang mengaudit naskah DOCX yang benar-benar '
            'dikirim. Angka pada bagian 6 dan 6.1 merujuk `21-numbers-of-record.md` sebagai kanon, tanpa mengubah laporan itu.')
        print('methodology item 1 updated')
    if l.startswith('2. Semua temuan bersumber dari'):
        lines[i] = l.replace('23 laporan', '24 laporan')
        print('methodology item 2 updated')

# ---- 3. readiness dimension 1: DOCX kernel gaps ----
for i, l in enumerate(lines):
    if l.startswith('| 1 | Kesiapan proposal dan naskah |'):
        lines[i] = l.replace(
            'dan 12 dari 20 item checklist submit kosong (F-38). |',
            'dan 12 dari 20 item checklist submit kosong (F-38). Audit DOCX menambah: dokumen kirim tidak reproducible dari skrip repo '
            '(F-39), kernel proposal tidak lengkap (F-40), 13 kontradiksi internal naskah, dan nol sitasi dalam teks untuk 18 rujukan. |')
        print('score dim 1 updated')
    if l.startswith('| 6 | Reproduksibilitas dan artefak |'):
        lines[i] = l.replace(
            'dan 9 dari 9 artefak wajib v2.1 hilang (F-15, F-07). |',
            'dan 9 dari 9 artefak wajib v2.1 hilang (F-15, F-07). Naskah DOCX yang dikirim pun tidak reproducible dari skrip builder '
            'karena ada jalur build kedua yang tidak tercatat (F-39). |')
        print('score dim 6 updated')

# ---- 4. scenario A: add DOCX risk ----
for i, l in enumerate(lines):
    if l.startswith('| A. Submit apa adanya dengan klaim diturunkan |'):
        lines[i] = l.replace(
            'Tidak ada video, deck, atau daftar berkas wajib saat submit. |',
            'Menemukan dokumen yang dikirim tidak reproducible dari skrip repo dan tidak berisi satu pun gambar meski Daftar Gambar '
            'mendaftarkan 7 (F-39); menemukan kernel proposal kosong, termasuk nol protokol eksperimen dan nol sitasi dalam teks (F-40). '
            'Tidak ada video, deck, atau daftar berkas wajib saat submit. |')
        print('scenario A updated')
    if l.startswith('| C. Submit setelah perbaikan penuh |'):
        lines[i] = l.replace(
            'rotasi token Notion, serta repo publik dengan README dan tautan demo yang benar. |',
            'rotasi token Notion, rebuild dokumen proposal dari skrip repo dengan 7 gambar yang dikembalikan, field PAGE pada footer, '
            'penanda sitasi untuk 18 rujukan, dan abstrak, daftar singkatan, identitas bertanda tangan, serta bagian batasan eksplisit. |')
        print('scenario C updated')

# ---- 5. action table: insert a DOCX action, renumber ----
act_start = next(i for i, l in enumerate(lines) if l.startswith('| Prioritas | Aksi | Owner |'))
rows = []
for l in lines[act_start:]:
    if not l.strip().startswith('|'):
        break
    if l.startswith('|---') or l.startswith('| Prioritas |'):
        continue
    rows.append(l)
print('action rows found:', len(rows))

NEW_ACTIONS = [
    ('| 1 | Bangun ulang dokumen proposal DOCX dari skrip repo, kembalikan 7 gambar, atau hapus seluruh entri Daftar Gambar, '
     'tambahkan field PAGE pada footer, dan dokumentasikan atau hilangkan jalur build kedua | Dev | '
     '`22-proposal-docx-audit.md:49-59,295-297` (F-39) | 8 jam | 24 Okt 2026 |'),
    ('| 2 | Tambahkan kernel proposal yang hilang: abstrak, daftar singkatan, identitas bertanda tangan, protokol eksperimen ringkas, '
     'metode statistik, batasan eksplisit, dan penanda sitasi untuk 18 rujukan; atau pangkas daftar pustaka | Tim | '
     '`22-proposal-docx-audit.md:71-92,305-308` (F-40) | 8 jam | 26 Okt 2026 |'),
]
# new priorities 1 and 2; old 1..9 become 3..11, old 10 stays last -> we need only 10 total
old = rows[:]
for idx, r in enumerate(old):
    cells = r.split('|')
    p = int(cells[1].strip())
    if p <= 8:
        cells[1] = ' ' + str(p + 2) + ' '
    elif p == 9:
        cells[1] = ' 10 '
    else:
        cells[1] = ' 10 '
    rows[idx] = '|'.join(cells)
# drop old priority 9 row to keep 10 total
rows = [r for r in rows if r.split('|')[1].strip() != '10' or True]
final = NEW_ACTIONS + rows[:9]
# fix the numbering: final list should be 1..10
for i, r in enumerate(final):
    cells = r.split('|')
    cells[1] = ' ' + str(i + 1) + ' '
    final[i] = '|'.join(cells)
end = act_start
for l in lines[act_start:]:
    if not l.strip().startswith('|'):
        break
    end += 1
lines[act_start:end] = final
print('action table now', len(final), 'rows')

open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('written')
