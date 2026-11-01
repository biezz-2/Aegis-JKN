import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
BASE = 'N:/HEALTHKATHON/analysis/reports/'
anchors = {
    '02-proposal.md': ['Accuracy 93', 'Precision 94', 'ROC-AUC 0,9825', 'AUPRC 0,9142', 'masking',
                       'False positive', '45%', '3,2', '82,5', '507.370.000', 'K-01', 'K-02', 'M-01',
                       'M-02', 'Lampiran A', 'Lampiran C', 'Tabel Severity', 'Rata-rata'],
    '10-competition.md': ['C13', 'C15', 'P0-1', 'P0-5', 'Rp35', 'Rp25', 'SmartClaim', '2,6 dari 5',
                          'Checklist submit', 'video demo', 'tautan demo'],
    '19-consistency.md': ['34 kontradiksi', '109 baris', 'Rp539.650.000', 'Rp542,56', 'Daftar Kontradiksi',
                          'Temuan paling berbahaya', 'Audit `14-index'],
    '04-data-quality.md': ['7-19', '7-7', '7-3', '7-4', 'Tabel severity', 'dokter_raw'],
    '13-text-channel.md': ['S4', 'S5', 'S2', 'Tabel Severity', 'Lampiran A', 'spec gap'],
    '11-compliance.md': ['C-01', 'C-02', 'C-03', 'C-04', 'C-05', 'C-06', 'C-07', 'C-08', 'C-11', 'C-12',
                         'C-13', 'Prioritas 1', 'R-01', 'R-17', 'Pasal 34'],
    '06-graph-mhgsl.md': ['C-07', 'C-08', 'C-12', 'C-14', 'C-16', 'C-20', 'E-01', 'E-05', 'E-06',
                          'Status severity', 'Verdict akhir', 'Lampiran: Ringkasan'],
    '21-numbers-of-record.md': ['sha256', 'F1 = 0,3448', 'i18n.tsx:791', '2.192', 'Los kosong',
                                '16.667', '45%', 'Rp 539.650.000', 'separability', 'A_feat'],
}
for f, ks in anchors.items():
    t = open(BASE + f, encoding='utf-8', errors='replace').read().split('\n')
    print('=====', f, 'lines', len(t))
    for k in ks:
        hits = [i + 1 for i, l in enumerate(t) if k in l][:5]
        print('   ', k, '->', hits)
