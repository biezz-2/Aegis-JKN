import io, re, sys
p = r"N:\HEALTHKATHON\analysis\reports\13-text-channel.md"
lines = io.open(p, encoding="utf-8").read().split("\n")
out = io.open(r"N:\HEALTHKATHON\analysis\reports\scripts\_chk5.out", "w", encoding="utf-8")
# section 7 table rows
start = next(i for i, l in enumerate(lines) if l.startswith("## 7. Tabel Spec Gap"))
end = next(i for i, l in enumerate(lines) if l.startswith("## 8."))
rows = [l for l in lines[start:end] if l.startswith("| **")]
out.write(f"sec7 table rows: {len(rows)}\n")
for r in rows:
    m = re.match(r"\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|", r)
    out.write(f"  {m.group(1)[:40]:42} -> {m.group(2)[:32]}\n")
full = sum(1 for r in rows if "✅" in r.split("|")[2])
partial = sum(1 for r in rows if "⚠️" in r.split("|")[2])
none = sum(1 for r in rows if "❌" in r.split("|")[2])
out.write(f"full={full} partial={partial} none={none} total={full+partial+none}\n")
out.close()
