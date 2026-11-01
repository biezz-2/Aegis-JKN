#!/usr/bin/env python3
"""22_extract_docx.py - stdlib-only DOCX text/table/media extraction.

Usage: python -I 22_extract_docx.py <docx> <outdir> <tag>
Writes:
  <outdir>/<tag>_paragraphs.txt   - one paragraph per line, with index
  <outdir>/<tag>_tables.txt      - tables with index and cell text
  <outdir>/<tag>_meta.txt        - media count, headers/footers, core props
"""
import sys, os, re, zipfile

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def unesc(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
             .replace("&quot;", '"').replace("&apos;", "'"))


def paragraphs(xml):
    """Yield (style, text) for each <w:p> in document order, including inside tables."""
    out = []
    for m in re.finditer(r"<w:p\b[^>]*/>|<w:p\b.*?</w:p>", xml, re.S):
        blk = m.group(0)
        if blk.endswith("/>"):
            out.append(("", ""))
            continue
        style = ""
        ms = re.search(r'<w:pStyle w:val="([^"]+)"', blk)
        if ms:
            style = ms.group(1)
        texts = re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", blk, re.S)
        txt = unesc("".join(texts))
        # tabs / breaks
        if "<w:tab/>" in blk:
            txt = txt.replace("\t", " ")
        out.append((style, txt.strip()))
    return out


def main():
    path, outdir, tag = sys.argv[1], sys.argv[2], sys.argv[3]
    os.makedirs(outdir, exist_ok=True)
    z = zipfile.ZipFile(path)
    names = z.namelist()
    doc = z.read("word/document.xml").decode("utf-8", "replace")

    # --- media ---
    media = sorted([n for n in names if n.startswith("word/media/")])
    media_info = []
    for n in media:
        try:
            data = z.read(n)
            media_info.append((n, len(data)))
        except Exception as e:
            media_info.append((n, -1))

    # --- paragraphs ---
    pars = paragraphs(doc)
    pfile = os.path.join(outdir, tag + "_paragraphs.txt")
    with open(pfile, "w", encoding="utf-8") as f:
        for i, (st, tx) in enumerate(pars):
            f.write("[%04d]%s %s\n" % (i, ("<" + st + ">") if st else "", tx))

    # --- tables ---
    tables = []
    for tm in re.finditer(r"<w:tbl>.*?</w:tbl>", doc, re.S):
        tb = tm.group(0)
        rows = []
        for rm in re.finditer(r"<w:tr\b.*?</w:tr>", tb, re.S):
            rb = rm.group(0)
            cells = []
            for cm in re.finditer(r"<w:tc>.*?</w:tc>", rb, re.S):
                cb = cm.group(0)
                cellpars = paragraphs(cb)
                cells.append(" ".join(t for _, t in cellpars if t).strip())
            rows.append(cells)
        tables.append(rows)

    tfile = os.path.join(outdir, tag + "_tables.txt")
    with open(tfile, "w", encoding="utf-8") as f:
        for ti, rows in enumerate(tables):
            f.write("=== TABLE %d (rows=%d) ===\n" % (ti, len(rows)))
            for ri, r in enumerate(rows):
                f.write("  R%02d | %s\n" % (ri, " || ".join(r)))
            f.write("\n")

    # --- meta ---
    mfile = os.path.join(outdir, tag + "_meta.txt")
    with open(mfile, "w", encoding="utf-8") as f:
        f.write("FILE: %s  size=%d bytes\n" % (path, os.path.getsize(path)))
        f.write("paragraph_count=%d\n" % len(pars))
        f.write("table_count=%d\n" % len(tables))
        f.write("media_count=%d\n" % len(media))
        for n, s in media_info:
            f.write("  MEDIA %s %d bytes\n" % (n, s))
        f.write("--- headers/footers ---\n")
        for n in sorted(names):
            if re.match(r"word/(header|footer)\d*\.xml", n):
                hx = z.read(n).decode("utf-8", "replace")
                txt = " | ".join(t for _, t in paragraphs(hx) if t)
                f.write("  %s: %s\n" % (n, txt[:2000]))
        f.write("--- core props ---\n")
        if "docProps/core.xml" in names:
            f.write(z.read("docProps/core.xml").decode("utf-8", "replace")[:3000] + "\n")
        f.write("--- app props ---\n")
        if "docProps/app.xml" in names:
            f.write(z.read("docProps/app.xml").decode("utf-8", "replace")[:3000] + "\n")
        f.write("--- all zip parts ---\n")
        for n in names:
            f.write("  %s\n" % n)

    # drawings & inline images in document order
    dfile = os.path.join(outdir, tag + "_drawings.txt")
    with open(dfile, "w", encoding="utf-8") as f:
        for i, (st, tx) in enumerate(pars):
            f.write("[%04d] %s\n" % (i, tx))
        f.write("\n--- drawing count in doc xml ---\n")
        f.write("w:drawing=%d  pict=%d  blip=%d\n" % (
            doc.count("<w:drawing"), doc.count("<w:pict"), doc.count("a:blip")))
        f.write("--- rels ---\n")
        if "word/_rels/document.xml.rels" in names:
            f.write(z.read("word/_rels/document.xml.rels").decode("utf-8", "replace"))

    print("OK %s: paras=%d tables=%d media=%d" % (tag, len(pars), len(tables), len(media)))


main()
