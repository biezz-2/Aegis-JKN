import io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = 'N:/HEALTHKATHON/analysis/reports/00-EXECUTIVE-SUMMARY.md'
lines = open(P, encoding='utf-8').read().split('\n')


def row_index(fid):
    for i, l in enumerate(lines):
        if l.startswith('| %s |' % fid):
            return i
    raise SystemExit('row not found: ' + fid)


def add_cite(fid, cite):
    """Append a citation into the source cell (index 3) of an F row."""
    i = row_index(fid)
    cells = lines[i].split('|')
    assert len(cells) == 7, (fid, len(cells))
    src = cells[3].strip()
    if cite in src:
        print('  already cited', fid)
        return
    cells[3] = ' ' + src + '; ' + cite + ' '
    lines[i] = '|'.join(cells)


def replace_in(fid, old, new):
    i = row_index(fid)
    assert old in lines[i], (fid, old[:60])
    lines[i] = lines[i].replace(old, new)
    print('  edited', fid)


def replace_doc(old, new, count=1):
    global lines
    n = sum(1 for l in lines if old in l)
    assert n >= 1, ('NOT FOUND:', old[:90])
    lines = [l.replace(old, new) for l in lines]
    print('  replaced x%d' % n, old[:60])


print('== 1. add citations from 22-proposal-docx-audit.md ==')
add_cite('F-01', '`22-proposal-docx-audit.md:192-202`')
add_cite('F-03', '`22-proposal-docx-audit.md:107-108,170,182`')
add_cite('F-15', '`22-proposal-docx-audit.md:49-59,295`')
add_cite('F-19', '`22-proposal-docx-audit.md:112-130`')
add_cite('F-24', '`22-proposal-docx-audit.md:248-255`')
add_cite('F-29', '`22-proposal-docx-audit.md:150-166,176-178,182-184`')
add_cite('F-30', '`22-proposal-docx-audit.md:134-148,180`')
add_cite('F-31', '`22-proposal-docx-audit.md:201,203`')
add_cite('F-32', '`22-proposal-docx-audit.md:90,270-271`')
add_cite('F-33', '`22-proposal-docx-audit.md:85-87`')

print('== 2. fold old F-39 into F-31, old F-40 into F-38 ==')
replace_in('F-31',
    'Melanggar Standar Dokumen bagian 7 dan berisiko keliru faktual',
    'Melanggar Standar Dokumen bagian 7 dan berisiko keliru faktual. Angka 872 dari `10-competition.md:72` juga penghitung API live lintas '
    'kategori dengan rincian 0/0/0 sehingga tidak boleh diklaim sebagai 872 tim di kategori Fasilitas Kesehatan, dan prevalensi 3-7% '
    'berasal dari GAO-24-105833 yang mengukur kewajiban federal AS non-kesehatan')
replace_in('F-38',
    'Risiko tidak lolos seleksi project akhir',
    'Risiko tidak lolos seleksi project akhir. Deadline di corpus juga masih salah: `dataset_research_live.json` dan artikel IDN Times '
    'menyebut 14 September 2026, sedangkan API resmi menyatakan submit project akhir 19 Oktober sampai 1 November 2026 dan Grand Final '
    '7 November 2026')

print('== 3. rewrite F-39 and F-40 as the new DOCX critical findings ==')
i39 = row_index('F-39')
i40 = row_index('F-40')
lines[i39] = (
    '| F-39 | Dokumen proposal yang dikirim tidak reproducible dari skrip repo: cover memuat kota CIMAHI dan tanggal 9 Oktober 2026 '
    'sedangkan skrip builder menyertakan JAKARTA dan "Jakarta, Oktober 2026"; dokumen berisi 7 entri Daftar Gambar tetapi nol objek '
    'gambar di `word/document.xml` dan nol berkas di `word/media/`, sedangkan cadangan `.bak` masih menyimpan 3 gambar dan 17 tabel; '
    'metadata dokumen kosong dengan creator "python-docx"; dan Caption Gambar 6.1 berbeda antara cadangan dan dokumen kirim. Artinya '
    'ada jalur build kedua yang tidak tercatat di repo | `22-proposal-docx-audit.md:49-59,295-297` | Naskah yang diserahkan juri tidak '
    'dapat diaudit, diregenerasi, atau dikoreksi deterministik; setiap perbaikan angka akan hilang pada build berikutnya | P0 |'
)
lines[i40] = (
    '| F-40 | Kernel proposal belum lengkap: nol abstrak, nol daftar singkatan, nol glosarium, nol lampiran, nol anggaran, nol '
    'identitas bertanda tangan, nol nama anggota tim, nol kontak, nol protokol eksperimen (tidak ada split, seed, ambang, atau prosedur '
    'evaluasi selain sebutan seed 20260707), nol metode statistik, nol persetujuan etika, nol batasan eksplisit studi, dan nol penanda '
    'sitasi dalam teks untuk 18 rujukan pustaka. Ditambah 13 kontradiksi internal naskah, footer tanpa field PAGE, Daftar Isi sebagai '
    'teks statis bukan field TOC, hanya satu style paragraf, dan penyampur pemisah desimal titik dengan koma | '
    '`22-proposal-docx-audit.md:71-92,244-289` | Unsur kernel yang menentukan kelayakan ilmiah tidak ada; pemeriksa akan membuka '
    'lampiran dan menemukan kekosongan | P0 |'
)

print('== 4. header counts 23 -> 24 ==')
replace_doc('Ruang lingkup: konsolidasi 23 laporan audit internal',
            'Ruang lingkup: konsolidasi 24 laporan audit internal')
replace_doc('Dasar: 23 laporan di `N:\\HEALTHKATHON\\analysis\\reports\\`',
            'Dasar: 24 laporan di `N:\\HEALTHKATHON\\analysis\\reports\\`')
replace_doc('Metode: polling laporan selesai (idle 8 menit tercapai pada elapsed 1445 detik, log di `scripts\\poll_log.txt`), lalu seluruh 23 laporan dibaca utuh, bukan hanya judulnya',
            'Metode: polling laporan selesai (idle 8 menit tercapai pada elapsed 1445 detik, log di `scripts\\poll_log.txt`), lalu seluruh 24 laporan dibaca utuh, bukan hanya judulnya')
replace_doc('## 2. Register Temuan Konsolidasi (F-01 sampai F-40)',
            '## 2. Register Temuan Konsolidasi (F-01 sampai F-40)')

open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('written')
