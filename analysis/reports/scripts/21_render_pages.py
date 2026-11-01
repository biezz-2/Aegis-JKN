import pymupdf, sys, io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',errors='replace')
pdf=sys.argv[1]; outdir=sys.argv[2]
pages=[int(x) for x in sys.argv[3].split(',')]
doc=pymupdf.open(pdf)
for pno in pages:
    p=doc[pno-1]
    pix=p.get_pixmap(dpi=150)
    out=f"{outdir}/21_pdf_p{pno:02d}.png"
    pix.save(out)
    print(out, pix.width, pix.height)
