import re, sys, zlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"N:/HEALTHKATHON/mechine-learning-deep-learning/colab/Hasil simulasi dari 300 dataset notion.pdf"
d = open(p, "rb").read()
print("bytes:", len(d))
print("size_match_3800507:", len(d) == 3800507)
for k in (b"/Producer", b"/Title", b"/CreationDate", b"/Creator"):
    m = re.findall(k + rb"\s*\(([^)]*)\)", d)
    print(k.decode(), "->", m[:3])
print("/Type /Page occurrences:", len(re.findall(rb"/Type\s*/Page[^s]", d)))
print("/Type /Pages occurrences:", len(re.findall(rb"/Type\s*/Pages", d)))
m = re.findall(rb"/Count\s+(\d+)", d)
print("/Count values:", m[:10])
# linearized / page tree
try:
    import fitz
    doc = fitz.open(p)
    print("pymupdf pages:", doc.page_count, "metadata:", doc.metadata)
except Exception as e:
    print("pymupdf:", e)
