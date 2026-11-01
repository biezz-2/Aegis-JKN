import json,sys,io
f=sys.argv[1]
nb=json.load(open(f,encoding='utf-8'))
out=io.StringIO()
for i,c in enumerate(nb['cells']):
    src=''.join(c['source'])
    out.write(f"\n{'='*70}\n### CELL {i} [{c['cell_type']}] outputs={len(c.get('outputs',[]))}\n{'='*70}\n")
    out.write(src+"\n")
    for o in c.get('outputs',[]):
        out.write(f"--- OUTPUT type={o.get('output_type')} ---\n")
        t=o.get('text')
        if t: out.write(''.join(t) if isinstance(t,list) else t)
        d=o.get('data',{})
        for k,v in d.items():
            s=''.join(v) if isinstance(v,list) else str(v)
            out.write(f"[{k}] {s[:3000]}\n")
        if o.get('output_type')=='error':
            out.write(str(o.get('ename'))+': '+str(o.get('evalue'))+"\n")
print(out.getvalue())
