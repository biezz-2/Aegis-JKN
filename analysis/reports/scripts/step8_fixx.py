import json, os, sys
BASE=r"N:\HEALTHKATHON"
p=os.path.join(BASE,r"mechine-learning-deep-learning\colab\Aegis_JKN_FIXX.ipynb")
nb=json.load(open(p,encoding="utf-8"))
sys.stdout.reconfigure(encoding="utf-8")
print("cells",len(nb["cells"]))
for i,c in enumerate(nb["cells"]):
    src="".join(c["source"]); lines=src.splitlines()
    outs=c.get("outputs") or []
    ot=""
    for o in outs:
        if "text" in o: ot+="".join(o["text"])
        elif "data" in o and "text/plain" in o["data"]: ot+="".join(o["data"]["text/plain"])
    print(f"[{i:>2}] {c['cell_type']:<8} outs={len(outs):<2} | {(lines[0] if lines else '')[:95]}")
