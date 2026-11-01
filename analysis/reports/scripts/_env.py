"""(1) How many claims depend on a reachable Ollama? (2) contradiction counts
(3) 300-dataset sentiment distribution vs the 62/14/24 spec."""
import csv, io, collections, sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

print("=== (1) LLM coupling in Aegis_JKN_FIXX.ipynb ===")
print("   TOTAL_STEPS = 300, LLM_EVERY = 100 -> LLM branch fires at i = 1, 100, 200, 300")
print("   => 4 LLM calls; llm_ptr advances 4; only 4 of 100 claims can receive LLM text")
print("   => 96 of 100 claims ALWAYS use tweet_template/reddit_template (heuristik-lokal)")
print("   => the 93.0% headline therefore depends on whether a local Ollama is reachable:")
print("      - no Ollama (repro on any laptop): 100% template -> 186/200 = 93.0%")
print("      - Ollama up: 4 claims get free-form LLM text -> sentiment labels may change")
print("      The PDF header records model 'mistral-oasis:24b', so the published run used LLM text")
print("      for 4 claims whose contribution to the 200-classification denominator is 4/200 = 2%.")
print("   Code comment says 'tiap klaim diproses 10x (1000/100)' but TOTAL_STEPS is 300,")
print("   so each claim is actually visited 3x. The 1000-step assumption in the comment is stale.")

print("\n=== (2) contradiction counts ===")
rows = list(csv.DictReader(io.StringIO(
    open("N:/HEALTHKATHON/analysis/reports/work22/claims_300_nb.csv", "rb").read().decode("utf-8-sig"))))
kn = [r for r in rows if r["kontradiksi_narasi"].strip().lower() in ("true", "1", "ya", "yes")]
print(f"   300-claim CSV kontradiksi_narasi truthy: {len(kn)}")
print(f"   ids: {[r['claim_id'] for r in kn]}")
print("   100-claim FIXX generator: 8 (KLM001-006, KLM018, KLM024) - hand-picked in code")

print("\n=== (3) sentiment distribution 300-claim CSV ===")
print("  ", collections.Counter(r["sentimen"] for r in rows))
print("   FIXX/10-simulation-dataset spec (100 claims): 62 positif / 14 netral / 24 negatif")

print("\n=== (4) does the 300 CSV contain the 8 KLM ids the FIXX queue flags? ===")
ids = {r["claim_id"]: r for r in rows}
for cid in ["KLM001", "KLM002", "KLM003", "KLM004", "KLM005", "KLM006",
            "KLM018", "KLM024", "KLM016", "KLM017"]:
    r = ids.get(cid)
    if not r:
        print(f"   {cid}: MISSING")
        continue
    print(f"   {cid} 300: risiko={r['risiko']:6s} skor_fraud={r['skor_fraud']:5s} "
          f"is_fraud={r['is_fraud']} modus={r['modus']:20s} sindikat={r['sindikat']:8s} "
          f"biaya={int(float(r['biaya_rp'])):>12,d} dx={r['diagnosis_code']:6s} proc={r['prosedur_code']}")
print("\n   FIXX 100-claim values for the same ids (from generator):")
import importlib.util
spec = importlib.util.spec_from_file_location("fx", r"N:/HEALTHKATHON/analysis/reports/scripts/_fixx_repro.py")
fx = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fx)
for c in fx.CLAIMS:
    if c["id"] in ("KLM001", "KLM002", "KLM003", "KLM004", "KLM005", "KLM006",
                   "KLM016", "KLM017", "KLM018", "KLM024"):
        print(f"   {c['id']} 100: skor={c['skor']} modus={c['modus']:20s} sindikat={c['sindikat']:9s} "
              f"biaya={c['biaya']:>12,d} dx={c['dx']:6s} proc={c['proc']} qty={c['qty']}")
