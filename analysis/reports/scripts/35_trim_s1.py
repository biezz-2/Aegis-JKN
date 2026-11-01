import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

P = 'N:/HEALTHKATHON/analysis/reports/00-EXECUTIVE-SUMMARY.md'
lines = open(P, encoding='utf-8').read().split('\n')
lines[352] = (
    "Ada satu temuan yang layak ditambahkan di sini: 23 dari 36 klaim fraud (63,9 persen) punya sinyal teks negatif, "
    "sedangkan 13 dari 36 (36,1 persen) tidak punya sinyal teks negatif sama sekali. Artinya kanal teks, bahkan kalau "
    "sempurna, tidak bisa menjangkau lebih dari dua pertiga kasus fraud. Ini batas struktural data, bukan cacat "
    "implementasi, dan sebaiknya ditulis terbuka di naskah."
)
open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('fixed line 353')
print(lines[352])
