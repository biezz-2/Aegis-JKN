import re, urllib.request, os, concurrent.futures
base = "https://healthkathon.bpjs-kesehatan.go.id/"
out = "N:/HEALTHKATHON/analysis/reports/work22/hkchunks"
os.makedirs(out, exist_ok=True)
rt = open("N:/HEALTHKATHON/analysis/reports/work22/runtime.js", encoding="utf-8", errors="replace").read()
m = re.search(r'f\.u=e=>\(8592===e\?"common":e\)\+"\."\+\{(.*?)\}\[e\]\+"\.js"', rt, re.S)
pairs = re.findall(r'(\d+):"([a-f0-9]{16})"', m.group(1))
print(len(pairs), "chunks")
def get(p):
    n, h = p
    url = f"{base}{n}.{h}.js"
    try:
        d = urllib.request.urlopen(url, timeout=30).read().decode("utf-8", "replace")
        open(os.path.join(out, f"{n}.js"), "w", encoding="utf-8").write(d)
        return n, len(d)
    except Exception as e:
        return n, str(e)[:50]
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
    res = list(ex.map(get, pairs))
ok = sum(1 for n, r in res if isinstance(r, int))
print("downloaded", ok)
