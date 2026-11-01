import io, re, sys
p = r"N:\HEALTHKATHON\analysis\reports\13-text-channel.md"
lines = io.open(p, encoding="utf-8").read().split("\n")
out = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_scan2.out", "w", encoding="utf-8")

CJK = re.compile(r"[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]")
# camelCase-merged words (lowercase followed by uppercase inside a word)
CAMEL = re.compile(r"[a-z]{2,}[A-Z][a-z]")
BADWORD = re.compile(r"\b(newsa|newsaya|ntissue|wallet|meter|dalamnya|sejaknya|adanya)\b", re.I)
for i, ln in enumerate(lines):
    flags = []
    if CJK.search(ln):
        flags.append("CJK")
    for m in CAMEL.finditer(ln):
        w = m.group(0)
        if w not in ("Skor",):
            flags.append("CAMEL:" + w)
    if "=" in ln and re.search(r"[a-z]=[a-z]", ln) and "==" not in ln and "≠" not in ln:
        flags.append("EQ")
    if flags:
        out.write(f"L{i+1} [{','.join(flags)}] {ln}\n")

# long tokens without space (possible lost space)
for i, ln in enumerate(lines):
    for m in re.finditer(r"\b([a-z]{2,})([a-z]{2,})\b", ln):
        pass
# double-word / lost space heuristics: known joins
JOINS = ["textchannel","modelyang","yangdi","dandengan","andadengan","ker攻坚"]
out.write("\n--- suspicious lowercase-run words (len>18, no uppercase) ---\n")
for i, ln in enumerate(lines):
    for m in re.finditer(r"\b[a-z]{19,}\b", ln):
        out.write(f"L{i+1} {m.group(0)} :: {ln[:160]}\n")
out.close()
