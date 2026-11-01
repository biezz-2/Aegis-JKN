import json, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
nb = json.load(open(r"N:/HEALTHKATHON/mechine-learning-deep-learning/colab/Aegis_JKN_FIXX.ipynb", encoding="utf-8"))
c = nb["cells"][5]
for i, o in enumerate(c.get("outputs", [])):
    t = o.get("output_type")
    print(f"===== output {i} type={t}")
    if t == "stream":
        for l in "".join(o.get("text", [])).split("\n"):
            print("  ", l.rstrip()[:200])
    elif t in ("execute_result", "display_data"):
        d = o.get("data", {})
        if "text/plain" in d:
            for l in "".join(d["text/plain"]).split("\n"):
                print("  RES>", l.rstrip()[:200])
        if "text/html" in d:
            h = "".join(d["text/html"])
            print("   [html len]", len(h))
            for kw in ("Akurasi", "93", "Deteksi", "Sindikat", "Kontradiksi", "Kapasitas", "Prevalensi", "Feat Edge", "Density", "Edge"):
                for l in h.split("\n"):
                    if kw in l:
                        print("    HTML>", l.strip()[:200])
                        break
