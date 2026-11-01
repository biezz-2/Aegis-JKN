import json,sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
path=sys.argv[1]
nb=json.load(open(path,encoding="utf-8"))
src="\n".join("".join(c.get("source",[])) for c in nb["cells"])
print("LEN",len(src))
for pat in sys.argv[2:]:
    hits=[l for l in src.split("\n") if pat in l]
    print(f"### {pat}: {len(hits)}")
    for h in hits[:6]: print("   ", h[:200])
