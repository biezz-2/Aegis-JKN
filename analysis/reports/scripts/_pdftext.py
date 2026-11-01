import sys, pymupdf
doc = pymupdf.open(sys.argv[1])
for i, page in enumerate(doc, 1):
    print(f"\n{'='*70}\n=== PAGE {i} ===\n{'='*70}")
    print(page.get_text("text"))
