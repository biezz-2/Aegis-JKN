import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
nb = json.load(open(r"N:/HEALTHKATHON/mechine-learning-deep-learning/colab/Aegis_JKN_FIXX.ipynb", encoding="utf-8"))
print("cells:", len(nb["cells"]))
for i, c in enumerate(nb["cells"]):
    src = "".join(c["source"])
    outs = c.get("outputs", [])
    print(f"--- cell {i} type={c['cell_type']} outs={len(outs)} srclen={len(src)}")
    for line in src.split("\n"):
        low = line.lower()
        if any(k in low for k in ("mistral", "ollama_model", "model =", "MODEL", "ollama pull", "OLLAMA_HOST")):
            print("     ", line.strip()[:140])
    for o in outs:
        t = o.get("output_type")
        if t == "stream":
            txt = "".join(o.get("text", []))
            hits = [l for l in txt.split("\n") if any(k in l.lower() for k in ("mistral", "model", "ollama", "gpu", "btop"))]
            for l in hits[:12]:
                print("   OUT>", l.strip()[:140])
        elif t in ("execute_result", "display_data"):
            d = o.get("data", {})
            if "text/plain" in d:
                txt = "".join(d["text/plain"])
                for l in txt.split("\n")[:8]:
                    print("   RES>", l.strip()[:140])
