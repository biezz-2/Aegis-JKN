"""Why 93.0% and why every syndicate hit-rate is 100%:
- which 14/200 sentiment classifications fail, and why
- how fragile the 100% syndicate hit-rate is w.r.t. queue size
"""
import importlib.util, sys, collections

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
spec = importlib.util.spec_from_file_location("fx", r"N:/HEALTHKATHON/analysis/reports/scripts/_fixx_repro.py")
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
CLAIMS = fx.CLAIMS

print("=== 1. The 14 failing sentiment classifications ===")
fails = []
for c in CLAIMS:
    if c["tw_label"] != c["gt_sentimen"]:
        fails.append((c["id"], "tw", c["gt_sentimen"], c["tw_label"], c["tw_score"],
                      c["signal"], fx.analyze_sentiment(c["tw_text"])["signal"]))
    if c["rd_label"] != c["gt_sentimen"]:
        fails.append((c["id"], "rd", c["gt_sentimen"], c["rd_label"], c["rd_score"],
                      c["signal"], fx.analyze_sentiment(c["rd_text"])["signal"]))
print(f"total failures: {len(fails)}/200  -> accuracy {(200-len(fails))/200*100:.1f}%")
for f in fails:
    print(f"   {f[0]} {f[1]}: gt={f[2]:7s} got={f[3]:7s} score={f[4]:+.3f} "
          f"signal='{f[5]}' detected_phrase='{f[6]}'")

print("\n=== 2. Fragility of the 100% syndicate hit-rate ===")
ordered = sorted(CLAIMS, key=lambda c: c["p_fused"], reverse=True)
fraud_ids = {c["id"] for c in CLAIMS if c["risk"] == "fraud"}
print("rank of each claim by p_fused, with fraud/non-fraud marker:")
for i, c in enumerate(ordered, 1):
    mark = "FRAUD" if c["id"] in fraud_ids else "     "
    if i <= 26:
        print(f"   #{i:2d} {c['id']} p={c['p_fused']:.3f} {mark} synd={c['sindikat']:9s} {c['modus']}")

print("\nsyndicate hit-rate as a function of queue size (QUEUE_RATE):")
for q in range(10, 31, 1):
    qids = {c["id"] for c in ordered[:q]}
    rates = []
    for s in ["SYND-01", "SYND-02", "SYND-03", "SYND-04", "SYND-05"]:
        mem = [c for c in CLAIMS if c["sindikat"] == s]
        rates.append(sum(1 for c in mem if c["id"] in qids) / len(mem))
    ok = all(r > 0 for r in rates)
    det = sum(1 for c in CLAIMS if c["risk"] == "fraud" and c["id"] in qids) / 14
    print(f"   queue={q:2d} ({q/100:.0%}): det_rate={det:.1%} synd_rates="
          f"{[round(r,2) for r in rates]} all>0={ok}")

print("\n=== 3. Rank positions of syndicate members ===")
pos = {c["id"]: i for i, c in enumerate(ordered, 1)}
for s in ["SYND-01", "SYND-02", "SYND-03", "SYND-04", "SYND-05"]:
    mem = [c for c in CLAIMS if c["sindikat"] == s]
    print(f"   {s} ({mem[0]['modus']:18s}) ranks = "
          f"{[ (c['id'], pos[c['id']], c['skor']) for c in sorted(mem, key=lambda x: pos[x['id']])]}")

print("\n=== 4. What happens if the risk scale changes? ===")
# If fraud threshold were 0.75 instead of 0.80 (a plausible alternative cut)
for thr in (0.70, 0.75, 0.80, 0.85):
    fr = [c for c in CLAIMS if c["skor"] > thr]
    qids = {c["id"] for c in ordered[:20]}
    det = sum(1 for c in fr if c["id"] in qids)
    print(f"   threshold>{thr}: fraud set n={len(fr):2d}, caught in top-20 = {det:2d} "
          f"({det/len(fr):.0%})")
