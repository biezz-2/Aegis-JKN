import json, os, sys
BASE=r"N:\HEALTHKATHON"
p=os.path.join(BASE,r"mechine-learning-deep-learning\notebooks\Aegis-JKN.ipynb")
nb=json.load(open(p,encoding="utf-8"))
print("nbformat",nb.get("nbformat"),"cells",len(nb["cells"]))
out=[]
for i,c in enumerate(nb["cells"]):
    src="".join(c["source"])
    outs=c.get("outputs") or []
    otext=""
    for o in outs:
        if "text" in o: otext+="".join(o["text"])
        elif "data" in o and "text/plain" in o["data"]: otext+="".join(o["data"]["text/plain"])
    out.append({"idx":i,"type":c["cell_type"],"nlines":len(src.splitlines()),
                "src":src,"outputs":otext,"n_out":len(outs)})
with open("nb_main_dump.json","w",encoding="utf-8") as f: json.dump(out,f,ensure_ascii=False,indent=1)
sys.stdout.reconfigure(encoding="utf-8")
for c in out:
    first=c["src"].splitlines()[0] if c["src"].splitlines() else ""
    print(f"[{c['idx']:>2}] {c['type']:<8} lines={c['nlines']:<3} outs={c['n_out']:<2} | {first[:100]}")
