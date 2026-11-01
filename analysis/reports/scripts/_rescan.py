import re, glob, sys, os

sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

ALLOW = {
    "GroupKFold", "LeaveOneGroupOut", "HeteroData", "OpenAlex", "EuropePMC", "PathSim",
    "GraphSAINT", "LeakyReLU", "MedicationDispense", "DatasetExplorer", "SearXNG",
    "ChargeItem", "ClaimResponse", "CurtisPKF", "PartialAUC", "XGBoost", "SHAP",
    "DeepSHAP", "SubgraphX", "FastAPI", "StandardScaler", "GradientBoosting", "TreeExplainer",
    "GradientSHAP", "NextResponse", "PostHog", "includeSubDomains", "PrismaClient",
    "ResearchGate", "SharePoint", "SmartClaim", "JavaScript", "TypeScript", "NalarAI",
    "HybridGNN", "GraphSAGE", "OpenAI", "PrismaClient", "WhatsApp", "MixedCase",
    "featureScore", "semanticScore", "topologyScore", "fusionScore", "riskLabel",
    "camouflageDetected", "scoredRow", "scamd", "OasisDashboard", "ShortcutsHint",
    "GlossaryButton", "ProblemSection", "MultiChannelGraph", "MathFormulas", "FraudRing",
    "BackToTop", "twFeed", "rdFeed", "syndicateHitRate", "losHari", "profileId",
    "statusOrder", "createdAt", "updatedAt", "authorId", "localStorage", "setState",
    "parseCSV", "openGraph", "CodeMirror", "noEmit", "createVM", "CreateVM", "textContradictions",
    "fraudClaimsV", "groundTruthSyndicates", "socialPosts", "featureEdges", "notionBV",
    "NotionBV", "riskScore", "fullTextXML", "ahtFQsoAAAAJ", "ylwNQM", "PatuhRadar",
    "curtisPKF", "medicationDispense",
}

pat = re.compile(r"(?<![A-Za-z@])([a-z]{2,}[A-Z][a-zA-Z]*|[A-Z][a-z]+[a-z]{2,}[A-Z][a-zA-Z]*)(?![A-Za-z@])")
out = open(os.path.join(ROOT, "scripts", "_mixed_scan2.txt"), "w", encoding="utf-8")
for f in sorted(glob.glob(os.path.join(ROOT, "*.md"))):
    hits = []
    for i, line in enumerate(open(f, encoding="utf-8").read().split("\n"), 1):
        body = re.sub(r"`[^`]*`", "@@", line)
        for m in pat.finditer(body):
            w = m.group(1)
            if w in ALLOW:
                continue
            hits.append((i, w, line.strip()[:170]))
    if hits:
        out.write("=== %s %d\n" % (os.path.basename(f), len(hits)))
        for i, w, l in hits:
            out.write("  L%-4d %-24s %s\n" % (i, w, l))
out.close()
print("written")
