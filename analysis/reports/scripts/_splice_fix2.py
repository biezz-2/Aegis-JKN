import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

REPORTS_DIR = r"N:\HEALTHKATHON\analysis\reports"

# The exact corrupted bytes from position 20-32: b + 12 non-Latin chars
# "b" (0x62) + "\u09be\u09b0\u0e37\u0e2d\u0e17\u0e16\u0e39\u0e01\u0e15\u0e49\u0e2d\u0e07"
REPAIRS = [
    ("20-repo-artifact-integrity.md",
     "punyab" + "\u09be\u09b0\u0e37\u0e2d\u0e17\u0e16\u0e39\u0e01\u0e15\u0e49\u0e2d\u0e07",
     "artefak"),
]

def main():
    for fname, old, new in REPAIRS:
        filepath = os.path.join(REPORTS_DIR, fname)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
        if old in text:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text.replace(old, new))
            print("fixed: %s" % fname)
        else:
            print("MISS: %s | old len=%d" % (fname, len(old)))

if __name__ == "__main__":
    main()