import sys, os, re

sys.stdout.reconfigure(encoding="utf-8")
TASKS = r"C:/Users/attab/AppData/Local/Temp/claude/N--HEALTHKATHON-Aegis-JKN-app/93e4f64f-c1ad-4481-af7d-c06c145a2ab0/tasks"
files = sorted(f for f in os.listdir(TASKS) if f.endswith(".output"))
blobs = {fn: open(os.path.join(TASKS, fn), encoding="utf-8", errors="replace").read() for fn in files}

CLEAN = [
    "rumah tangga",
    "ditulis dalam kurung",
    "closure criteria ditulis",
    "Di mana laporan",
    "tetapi belum harmonis",
    "komponen teknis",
    "titik data sintetis",
    "rencana on-prem",
    "harus bertahan selama masa transisi",
    "administrasi internal BPJS",
    "label kanal teks berada di hilir",
    "sudah seharusnya",
    "definisi asli hanya di",
    "tidak lagi diperlukan",
    "bergaya Wizard-of-Oz",
    "devDependency",
    "Stretch",
    "lembar instrumen SUS",
    "klaim AUPRC",
    "saat demo",
    "notebook yang memakainya",
    "pembangkitan deterministik",
    "inti proposal",
    "sudah ada",
    "Skala penghematan",
    "menyelamatkan ratusan miliar",
    "pengumpulan sumber",
    "gagal masuk ke pola",
    "menentukan \"netral\"",
    "mempresentasikan diri",
    "saya tidak melaporkannya",
    "di mana laporan",
    "jumlah skenario minimum",
]

for tok in CLEAN:
    hits = []
    for fn in files:
        raw = blobs[fn]
        n = raw.count(tok)
        if n:
            hits.append((fn[:10], n))
    print("%-45s %s" % (repr(tok), hits if hits else "-- none --"))
