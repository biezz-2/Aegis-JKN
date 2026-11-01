import re, urllib.request, os, concurrent.futures
base = "https://healthkathon.bpjs-kesehatan.go.id/"
out = "N:/HEALTHKATHON/analysis/reports/work22/hkchunks"
rt = open("N:/HEALTHKATHON/analysis/reports/work22/runtime.js", encoding="utf-8", errors="replace").read()
m = re.search(r'f\.u=e=>\(8592===e\?"common":e\)\+"\."\+\{(.*?)\}\[e\]\+"\.js"', rt, re.S)
pairs = re.findall(r'(\d+):"([a-f0-9]{16})"', m.group(1))
def get(p):
    n, h = p
    url = f"{base}{n}.{h}.js"
    try:
        d = urllib.request.urlopen(url, timeout=40).read().decode("utf-8", "replace")
        open(os.path.join(out, f"{n}.js"), "w", encoding="utf-8").write(d)
        return n, len(d)
    except Exception as e:
        return n, "ERR " + str(e)[:60]
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    for n, r in ex.map(get, pairs):
        if not isinstance(r, int):
            print("FAILED", n, r)
print("retry done")
