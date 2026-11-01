import fitz, sys, io, os
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
pdf=sys.argv[1]; outdir=sys.argv[2]
doc=fitz.open(pdf)
print("pages:",doc.page_count)
print("meta:",doc.metadata)
for i,p in enumerate(doc):
    t=p.get_text().strip()
    print(f"page {i+1}: text_len={len(t)} images={len(p.get_images(full=True))} rect={p.rect}")
