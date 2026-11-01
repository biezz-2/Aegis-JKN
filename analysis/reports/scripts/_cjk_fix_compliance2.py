"""Second repair pass for 11-compliance.md.

The first pass fixed the CJK characters. This pass fixes the English words
that were spliced INTO Indonesian words by the same generation corruption, and
a handful of English phrases left inline in an otherwise Indonesian report.
Each replacement restores the clause the surrounding sentence calls for.
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
NAME = "11-compliance.md"

FIXES = [
    # L36 - "pasalDidn'tcriminal" -> "pasal pidana"
    ("bukan pasalDidn'tcriminal", "bukan pasal pidana"),
    # L56 - "salahEYang" -> "salah ejaan"
    ("yang **salahEYang**", "yang **salah ejaan**"),
    # L158 - "untukMIỆU" -> "untuk bukti"
    ("berguna justru untukMIỆU proposal",
     "berguna justru sebagai bukti bagi proposal"),
    # L173 - "benarnichLQBIAT" -> "benar"
    ("sudah benarnichLQBIAT integrasi SATUSEHAT/V-Claim",
     "sudah benar bahwa integrasi SATUSEHAT/V-Claim"),
    # L269 - "yangDoing" -> "yang ada"
    ("(DPIA/ATD)** yangDoing - Pasal 34 UU PDP",
     "(DPIA/ATD)** yang ada - Pasal 34 UU PDP"),
    # L333 - "apotekFilteringamed BPJS" -> "apotek BPJS"
    ("diberikan FPKTP atau apotekFilteringamed BPJS",
     "diberikan FPKTP atau apotek BPJS"),
    # L394 - "Recently framework" and "IntelligentYPersembahan"
    ("kapitasi, Recently framework. Tidak boleh IntelligentYPersembahan sebagai \"BPJS\" generik tanpa dasar",
     "kapitasi, dan kerangka Primary Care. Tidak boleh menyebutnya sebagai \"BPJS\" generik tanpa dasar hukum"),
    # L398 - "menyPreparationn upcoming regulatory shift"
    ("Proposal harus menyPreparationn upcoming regulatory shift",
     "Proposal harus menyesuaikan diri dengan perubahan regulasi yang akan datang"),
    # L173 - "tidak quoted di mana pun" -> Indonesian
    ("**PP 71/2019 tidak quoted di mana pun**",
     "**PP 71/2019 tidak disebut di mana pun**"),
    # L7 - "primary , failover ." -> restore hostnames
    ("MCP SearXNG (primary , failover )",
     "MCP SearXNG (primary `http://localhost:8088`, failover `http://192.168.101.19:8089`)"),
    # L5 - "Lingkup:  (15 dokumen" -> restore path
    ("**Lingkup:**  (15 dokumen markdown + 4 berkas data)",
     "**Lingkup:** `N:\\HEALTHKATHON\\analysis\\corpus\\` (15 dokumen markdown + 4 berkas data)"),
    # L7 - empty parens for source URLs
    ("terhadap JDIH BPK (), PDF JDIH Kemenkes (), WHO ICD-10 Browser (), CDC ICD-9-CM",
     "terhadap JDIH BPK (`peraturan.bpk.go.id`), PDF JDIH Kemenkes (`jdih.kemenkes.go.id`), WHO ICD-10 Browser (`icd.who.int`), CDC ICD-9-CM"),
]

path = os.path.join(ROOT, NAME)
text = open(path, encoding="utf-8").read()

for a, b in FIXES:
    if a == b:
        continue
    if a in text:
        text = text.replace(a, b)
        print("fixed  %r" % (a[:64],))
    else:
        print("MISS   %r" % (a[:64],))

open(path, "w", encoding="utf-8").write(text)

print()
pat = re.compile(r"(?<![A-Za-z@])([a-z]{2,}[A-Z][a-zA-Z]*|[A-Z][a-z]+[a-z]{2,}[A-Z][a-zA-Z]*)(?![A-Za-z@])")
ALLOW = {"SearXNG", "ChargeItem", "ClaimResponse"}
residual = []
for i, line in enumerate(text.split("\n"), 1):
    body = re.sub(r"`[^`]*`", "@@", line)
    for m in pat.finditer(body):
        w = m.group(1)
        if w in ALLOW:
            continue
        residual.append((i, w, line[:200]))
print("residual mixed-case tokens:", len(residual))
for i, w, l in residual:
    print("  L%-4d %-24s %r" % (i, w, l))
