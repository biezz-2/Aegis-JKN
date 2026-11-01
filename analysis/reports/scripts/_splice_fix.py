import sys
import os

sys.stdout.reconfigure(encoding="utf-8")

REPORTS_DIR = r"N:\HEALTHKATHON\analysis\reports"

# All verified corruptions from triage: (file, old_string, new_string)
REPAIRS = [
    # 00-EXECUTIVE-SUMMARY.md
    ("00-EXECUTIVE-SUMMARY.md", "Where laporan", "Di mana laporan"),

    # 01-governance.md
    ("01-governance.md", "tetapiOUN harmonisasi", "tetapi belum harmonis"),
    ("01-governance.md", "Tidak adaMinimal jumlah skenario", "Tidak ada jumlah skenario minimum"),
    ("01-governance.md", "Closure criteria, shown in kurung", "kriteria penyelesaian, ditulis dalam kurung"),
    ("01-governance.md", "Prioritas P3 (rumahTBS):", ""),  # fabricated heading - remove entirely
    ("01-governance.md", "Cakupan/pembagianّق", "Cakupan/pembagian yang"),
    ("01-governance.md", "Dokumenاند benar", "Dokumen land"),  # reconstruct from context
    ("01-governance.md", "Gerbang experimentally mustahil", "Gerbang eksperimen mustahil"),
    ("01-governance.md", "Klaimfinancial", "Klaim financial"),
    ("01-governance.md", "L344–L348/Linux", "L344–L348"),
    ("01-governance.md", "(arel ini diturunkan", "(angka ini diturunkan"),
    ("01-governance.md", "klaimbery quantitatively", "klaim kuantitatif"),
    ("01-governance.md", "-ولة yang sama", "- yang sama"),

    # 03-architecture.md
    ("03-architecture.md", 'Angka"Ilmu" yang', 'Angka "ilmu" yang'),
    ("03-architecture.md", "angka-angka similar", "angka-angka yang serupa"),
    ("03-architecture.md", "menghapusProjection teknis", "menghapus komponen teknis"),

    # 05-evidence.md
    ("05-evidence.md", '### 5.2 Tahun 2026 dan "volumePlaceholder"', '### 5.2 Tahun 2026 dan volume placeholder'),
    ("05-evidence.md", "Keduanya failing into the pola khas rujukan yang ditambahkan untukHmengisi celah", "Keduanya gagal masuk ke pola khas rujukan yang ditambahkan untuk mengisi celah"),
    ("05-evidence.md", 'Pola "volumePlaceholder" juga muncul pada baris 10: nama dataset paper "Medical-A/Medical-B" disebut "Medical-1/Medical-2" oleh review - indikasi review menulis dari sumber kedua menulis dari sumber kedua tanpa membuka paper aslinya.', ""),
    ("05-evidence.md", "baris 21 & 28, both bersumber domain mati", "baris 21 & 28, keduanya bersumber dari domain mati"),
    ("05-evidence.md", "pengcollectoran sumber", "pengumpulan sumber"),
    ("05-evidence.md", "wasted effort", "pekerjaan sia-sia"),
    ("05-evidence.md", "статус pemakaian", "status pemakaian"),

    # 06-graph-mhgsl.md
    ("06-graph-mhgsl.md", "muncul di brief tugas danAJAX Anda", "muncul di brief tugas dan pertanyaan Anda"),
    ("06-graph-mhgsl.md", '"Seb-saving ratusan miliar rupiah DJS setiapMSA"', '"menyelamatkan ratusan miliar rupiah Dana Jaminan Sosial (DJS) Kesehatan setiap tahun."'),

    # 07-generator.md
    ("07-generator.md", 'memDnama "netral"', 'menentukan "netral"'),

    # 08-frontend.md
    ("08-frontend.md", "mengPresentasikan diri", "mempresentasikan diri"),

    # 09-security.md
    ("09-security.md", "dataPoints sintetis", "titik data sintetis"),
    ("09-security.md", "saya tidakURITY melaporkannya", "saya tidak melaporkannya"),

    # 10-competition.md
    ("10-competition.md", "on-prem plan semua kuat", "rencana on-prem semua kuat"),

    # 11-compliance.md
    ("11-compliance.md", "proposal Mestinya survive the period of transition", "proposal harus bertahan selama masa transisi"),
    ("11-compliance.md", "Regulasi own-administrative BPJS", "Regulasi administrasi internal BPJS"),
    ("11-compliance.md", "prinsip:yos terbatas", "prinsip: tujuan terbatas"),
    ("11-compliance.md", "collecting data ограничен", "collecting data dibatasi"),
    ("11-compliance.md", "pembaruandata", "pembaruan data"),
    ("11-compliance.md", "kali communicates", "komunikasi"),
    ("11-compliance.md", "berlaku tanpa دون persetujuan", "berlaku tanpa persetujuan"),
    ("11-compliance.md", "per Prescription", "per resep"),
    ("11-compliance.md", "`SYND`OBAT-related rules", "`SYND-04 Drug Diversion`-related rules"),

    # 13-text-channel.md
    ("13-text-channel.md", "text channel labels are downstream of", "label kanal teks berada di hilir dari"),

    # 14-language.md
    ("14-language.md", "sudah SHOULD namun dilanggar", "sudah seharusnya namun dilanggar"),
    ("14-language.md", "definisioki hanya di", "definisi asli hanya di"),

    # 15-code-quality.md
    ("15-code-quality.md", "yang tidak lagiNeeded karena", "yang tidak lagi diperlukan karena"),
    ("15-code-quality.md", "padahal kontennyaWizard-of-Oz", "padahal kontennya bergaya Wizard-of-Oz"),
    ("15-code-quality.md", "CLI seharusnya devDep.", "CLI seharusnya devDependency."),
    ("15-code-quality.md", "kualitas &-have; **P3** =Stretch", "kualitas &-have; **P3** = Stretch"),

    # 17-roadmap.md
    ("17-roadmap.md", "lembar instrumentSUS tersimpan", "lembar instrumen SUS tersimpan"),
    ("17-roadmap.md", "klaimAUPRC tidak sah", "klaim AUPRC tidak sah"),
    ("17-roadmap.md", "Data looked-but-not-verified", "Data terlihat tetapi belum diverifikasi"),
    ("17-roadmap.md", "Demo butuh internet saatQgshow", "Demo butuh internet saat demo"),
    ("17-roadmap.md", "`labels.py` + notebookUsesIt", "`labels.py` + notebook yang memakainya"),

    # 20-repo-artifact-integrity.md
    ("20-repo-artifact-integrity.md", "cara senatorsDeterministiknya", "cara pembangkitan deterministiknya"),
    ("20-repo-artifact-integrity.md", "pada barisriset di database Notion", "pada baris registrasi di database Notion"),
    ("20-repo-artifact-integrity.md", "Arti القسم 3", "Arti Bagian 3"),
    ("20-repo-artifact-integrity.md", "Tidak satu pun punyabارء تلكتحقق manifest eksperimen", "Tidak satu pun artefak manifest eksperimen"),

    # 22-proposal-docx-audit.md
    ("22-proposal-docx-audit.md", "kelengkapan kernelDAY proposal", "kelengkapan inti proposal"),
    ("22-proposal-docx-audit.md", "sudahala", "sudah ada"),
    ("22-proposal-docx-audit.md", "dokumen ini寧gly mengulang", "dokumen ini secara gamblang mengulang"),
    ("22-proposal-docx-audit.md", "Денominator", "Penyebut"),
    ("22-proposal-docx-audit.md", "yang支持 salah satu pun", "yang mendukung salah satu pun"),
    ("22-proposal-docx-audit.md", "yaituInitializer squarely triliunan", "yaitu squarely triliunan"),
    ("22-proposal-docx-audit.md", "tanda petik二重 Indonesia", 'tanda petik « » Indonesia'),
    ("22-proposal-docx-audit.md", "SkalaSaving nasional", "Skala penghematan nasional"),
    ("22-proposal-docx-audit.md", "dan平均值 overcharge", "dan rata-rata overcharge"),
]

def fix_file(filepath, old, new):
    """Apply a single repair to a file, return True if fixed, False if not found."""
    if not os.path.exists(filepath):
        print(f"  MISS: {filepath} (file not found)")
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()
    if old in text:
        text = text.replace(old, new)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"  fixed: {filepath}")
        return True
    else:
        print(f"  MISS: {filepath} | '{old[:60]}...'")
        return False

def main():
    total_fixed = 0
    total_miss = 0
    for fname, old, new in REPAIRS:
        filepath = os.path.join(REPORTS_DIR, fname)
        if fix_file(filepath, old, new):
            total_fixed += 1
        else:
            total_miss += 1
    print(f"\n=== Summary ===")
    print(f"Fixed: {total_fixed}")
    print(f"Missed: {total_miss}")
    print(f"Total repairs: {len(REPAIRS)}")

if __name__ == "__main__":
    main()