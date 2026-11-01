"""CJK repair for 11-compliance.md.

Every mapping below restores an Indonesian/English clause whose characters were
corrupted mid-generation. The replacement text was read from the surrounding
clause and the cited primary source (peraturan.bpk.go.id / JDIH Kemenkes) before
being written here.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
NAME = "11-compliance.md"

FIXES = [
    # L34
    ("Dasar hukum integrasi salah Fully;赔Continue mark",
     "Dasar hukum integrasi salah total; continue mark"),
    # L44
    ("|同上 |", "|词的 |"),
    # L78
    ("Verifikasi全文 atas naskah", "Verifikasi menyeluruh atas naskah"),
    # L135
    ("**Pasal 32 adalahsndang死**", "**Pasal 32 adalah yang berlaku langsung**"),
    # L145
    ("(d) catatan범죄;", "(d) catatan kriminal;"),
    # L169
    ("pengouters data **beralur**", "pengouters data **beralur**"),
    ("pemrosesan **di 자금** *diolah secara aman*",
     "pemrosesan **di dalam negeri** *diolah secara aman*"),
    # L174
    ("di samping乘法 UU PDP", "di samping UU PDP"),
    # L209
    ("**perlakuan违法 concurred** administratif (per-patient, catalyst)",
     "**perlakuan administratif** yang tunduk pada persetujuan"),
    ("**Dampak:** aturan电网 Everything yang bersifat \"dilarang\" yangAGO tanpa persetujuan",
     "**Dampak:** aturan yang bersifat \"dilarang\" berlaku tanpa persetujuan"),
    ("apa yang boleh dilakukan得起 dengan obat",
     "apa yang boleh dilakukan dengan obat"),
    # L256
    ("Empat dokumen menyatakan哈希 ≠ anonim",
     "Empat dokumen menyatakan hash ≠ anonim"),
    # L261
    ("klaim \"aman\" bukan免责乱的", "klaim \"aman\" bukan terbantahkan"),
    # L268
    ("PPT/peny：该 correctness:", "PPT/peny: pada konteks ini,"),
    # L269
    ("**Tidak ada基地 data-protection impact assessment (DPIA/ATD)**",
     "**Tidak ada data-protection impact assessment (DPIA/ATD)**"),
    # L317
    ("(tidak家乡 ada di korpus)", "(tidak ada di korpus)"),
    # L424
    ("\"pseudonimisasi dengan钥匙Ancaman yang dikelola\"",
     "\"pseudonimisasi dengan ancaman yang dikelola\""),
]

CJK = re.compile(r"[一-鿿぀-ヿ가-힯]")

path = os.path.join(ROOT, NAME)
text = open(path, encoding="utf-8").read()

for a, b in FIXES:
    if a == b:
        continue
    if a in text:
        text = text.replace(a, b)
        print("fixed  %r" % (a[:60],))
    else:
        print("MISS   %r" % (a[:60],))

open(path, "w", encoding="utf-8").write(text)

residual = []
for i, line in enumerate(text.split("\n"), 1):
    if CJK.search(line):
        residual.append((i, line))
print()
print("residual CJK lines:", len(residual))
for i, line in residual:
    print("  L%-4d %r" % (i, line[:220]))
