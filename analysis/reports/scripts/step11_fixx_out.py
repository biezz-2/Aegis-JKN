import json,sys
sys.stdout.reconfigure(encoding="utf-8")
nb=json.load(open(r"N:\HEALTHKATHON\mechine-learning-deep-learning\colab\Aegis_JKN_FIXX.ipynb",encoding="utf-8"))
for i,c in enumerate(nb["cells"]):
    print("="*25,"CELL",i,"="*25)
    print("".join(c["source"])[:1500])
    for o in (c.get("outputs") or []):
        t="".join(o.get("text") or []) if "text" in o else ""
        if not t and "data" in o: t="".join(o["data"].get("text/plain") or [])
        print("--- OUT ---"); print(t[:4000])
