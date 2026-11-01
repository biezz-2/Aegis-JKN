"""Parse 10-simulation-dataset.md entity tables directly and compare against
(1) the 100-claim FIXX generator and (2) the 300-claim dataset."""
import csv, io, re, sys, collections, importlib.util
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DOC = r"N:/HEALTHKATHON/analysis/corpus/10-simulation-dataset.md"
CSVP = "N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv"

text = open(DOC, encoding="utf-8").read()


def table_after(header_re, ncols):
    """Return list of row-cell-lists from the first markdown table whose header
    matches header_re."""
    m = re.search(header_re, text)
    if not m:
        return []
    rest = text[m.end():]
    rows = []
    started = False
    for line in rest.split("\n"):
        s = line.strip()
        if not s.startswith("|"):
            if started:
                break
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not started:
            started = True
            continue  # header row
        if set("".join(cells)) <= set("-: "):
            continue  # separator
        rows.append(cells)
    return rows


def num(s):
    """Parse a doc cell. 'Rp 58.000.000' -> 58000000 (Indonesian separators);
    '0.95' -> 0.95 (decimal)."""
    s = s.strip()
    if s.startswith("Rp"):
        s = s[2:].replace(".", "").replace(",", ".").strip()
    try:
        return float(s)
    except Exception:
        return None


# ---- doc tables ----
faskes_rows = table_after(r"## Faskes", 9)
dokter_rows = table_after(r"## Dokter", 7)
pasien_rows = table_after(r"## Pasien", 10)
dx_rows = table_after(r"## Diagnosis \(ICD-10\)", 6)
proc_rows = table_after(r"## Prosedur \(ICD-9-CM\)", 7)

doc_faskes = {r[0]: (int(num(r[6])), num(r[7]), r[8]) for r in faskes_rows}
doc_dokter = {r[0]: (int(num(r[4])), num(r[5]), r[6]) for r in dokter_rows}
doc_pasien = {r[0]: (int(num(r[7])), num(r[8]), r[9]) for r in pasien_rows}
doc_dx = {r[0]: (int(num(r[3])), num(r[4]), r[5]) for r in dx_rows}
doc_proc = {r[0]: (int(num(r[4])), num(r[5]), r[6]) for r in proc_rows}
doc_tarif = {r[0]: num(r[3]) for r in proc_rows}

print("=== DOC TABLES PARSED ===")
print("faskes:", doc_faskes)
print("dokter:", doc_dokter)
print("pasien:", doc_pasien)
print("dx:", doc_dx)
print("proc:", doc_proc)
print("sum faskes n:", sum(v[0] for v in doc_faskes.values()))
print("sum dokter n:", sum(v[0] for v in doc_dokter.values()))
print("sum pasien n:", sum(v[0] for v in doc_pasien.values()))
print("sum dx n:", sum(v[0] for v in doc_dx.values()))
print("sum proc n:", sum(v[0] for v in doc_proc.values()))

# ---- 100-claim FIXX generator ----
spec = importlib.util.spec_from_file_location("fx", r"N:/HEALTHKATHON/analysis/reports/scripts/_fixx_repro.py")
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
CL = fx.CLAIMS

v1_f = collections.Counter(c["faskes"] for c in CL)
v1_fx = collections.defaultdict(float)
v1_d = collections.Counter(c["dokter"] for c in CL)
v1_dxn = collections.Counter(c["dx"] for c in CL)
v1_dx = collections.defaultdict(float)
v1_p = collections.Counter(c["pasien"] for c in CL)
v1_px = collections.defaultdict(float)
v1_pr = collections.Counter(c["proc"] for c in CL)
for c in CL:
    v1_fx[c["faskes"]] = max(v1_fx[c["faskes"]], c["skor"])
    v1_dx[c["dx"]] = max(v1_dx[c["dx"]], c["skor"])
    v1_px[c["pasien"]] = max(v1_px[c["pasien"]], c["skor"])
print("\n=== v1 (PDF source) faskes ===", dict(v1_f))
print("=== v1 dokter ===", dict(v1_d))
print("=== v1 pasien ===", dict(v1_p))
print("=== v1 dx ===", {k: (v1_dx[k], v1_dx[k]) for k in v1_dx})
print("=== v1 proc ===", dict(v1_pr))

# ---- 300 dataset ----
rows = list(csv.DictReader(io.StringIO(open(CSVP, "rb").read().decode("utf-8-sig"))))
v2_f = collections.Counter(r["faskes_id"] for r in rows)
v2_d = collections.Counter(r["dokter_id"] for r in rows)
v2_p = collections.Counter(r["pasien_id"] for r in rows)
v2_dx = collections.Counter(r["diagnosis_code"] for r in rows)
v2_dxmax = collections.defaultdict(float)
v2_pr = collections.Counter(r["prosedur_code"] for r in rows)
for r in rows:
    v2_dxmax[r["diagnosis_code"]] = max(v2_dxmax[r["diagnosis_code"]], float(r["skor_fraud"]))
print("\n=== v2 (300) faskes ===", dict(v2_f))
print("=== v2 dokter ===", dict(v2_d))
print("=== v2 pasien (first 20) ===", {f"P{i:02d}": v2_p.get(f"P{i:02d}", 0) for i in range(1, 21)})
print("=== v2 dx ===", dict(v2_dx))
print("=== v2 proc ===", dict(v2_pr))

# ---- comparisons ----
print("\n\n=== COMPARISON: doc vs v1 generator (100 klaim, apples-to-apples) ===")
def cmp_table(name, docmap, v1map, v1max, v2map, v2max=None, keys=None):
    nm = nm2 = ns = ns2 = 0
    for k in sorted(docmap):
        dn, ds, dr = docmap[k]
        a1 = v1map.get(k, 0)
        a2 = v2map.get(k, 0)
        s1 = v1max.get(k) if v1max else None
        s2 = v2max.get(k) if v2max else None
        o1 = "N" if dn != a1 else "="
        o2 = "N" if dn != a2 else "="
        if dn != a1: nm += 1
        if dn != a2: nm2 += 1
        sm = ""
        if v1max is not None:
            same = (s1 is not None and ds is not None and abs(s1 - ds) < 1e-9)
            sm += "  skor_doc=%s v1=%s %s" % (ds, s1, "MATCH" if same else "MISMATCH")
            if not same: ns += 1
        if v2max is not None:
            same2 = (s2 is not None and ds is not None and abs(s2 - ds) < 1e-9)
            sm += " | v2=%s %s" % (s2, "MATCH" if same2 else "MISMATCH")
            if not same2: ns2 += 1
        print(f"  {k:8s} n_doc={dn:3d} n_v1={a1:3d}[{o1}] n_v2={a2:3d}[{o2}]{sm}")
    tot = len(docmap)
    print(f"  -> {name}: n-mismatch vs v1: {nm}/{tot} | vs v2: {nm2}/{tot} | "
          f"skor-mismatch vs v1: {ns}/{tot} | vs v2: {ns2}/{tot}")
    return nm, nm2, ns, ns2

cmp_table("FASKES", doc_faskes, v1_f, v1_fx, v2_f)
cmp_table("DOKTER", doc_dokter, v1_d, None, v2_d)
cmp_table("PASIEN", doc_pasien, v1_p, v1_px, v2_p)
cmp_table("DIAGNOSIS", doc_dx, v1_dxn, v1_dx, v2_dx, v2_dxmax)
cmp_table("PROSEDUR", doc_proc, v1_pr, None, v2_pr)

print("\n=== TARIF: doc vs nominal biaya in the 300 dataset ===")
byproc = collections.defaultdict(list)
for r in rows:
    byproc[r["prosedur_code"]].append(int(float(r["biaya_rp"])))
for k in sorted(doc_tarif):
    t = doc_tarif[k]
    vals = byproc.get(k, [])
    if not vals:
        print(f"  {k:8s} tarif_doc={t:,.0f}  300-dataset: no rows")
        continue
    print(f"  {k:8s} tarif_doc={t:,.0f}  300 n={len(vals):3d} "
          f"min={min(vals):,} max={max(vals):,} "
          f"nominal>tarif: {sum(1 for v in vals if v > t)}/{len(vals)}")

print("\n=== PROSEDUR: full proc table in FIXX ===")
for k, v in sorted(v1_pr.items()):
    print(f"  {k:8s} n={v}")
print("  codes in FIXX not in doc:", sorted(set(v1_pr) - set(doc_proc)))
print("  codes in doc not in FIXX:", sorted(set(doc_proc) - set(v1_pr)))
