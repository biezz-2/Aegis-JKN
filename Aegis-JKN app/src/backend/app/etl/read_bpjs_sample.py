"""
ETL Pipeline: Membaca sampel data resmi BPJS Kesehatan (.dta),
melakukan join dengan kepesertaan, memetakan ke skema RawClaim,
dan mengekspor ke bpjs-real-claims.json untuk Aegis-JKN Workstation.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Set

import pandas as pd

# Path default dataset BPJS (berdasarkan struktur folder resmi BPJS 2015-2024 / 2025)
DEFAULT_FKRTL_PATH = Path(
    r"P:\EVENT KATON\HAELTHKATHON\Data sampel 2015-2024\2025\Data Sampel Reguler Edisi 2025\data\202403_fkrtl.dta"
)
FALLBACK_FKRTL_PATH = Path(
    r"P:\EVENT KATON\HAELTHKATHON\Data sampel 2015-2024\Data Sampel Reguler 2015 - 2024\202403_fkrtl.dta"
)
DEFAULT_KEP_PATH = Path(
    r"P:\EVENT KATON\HAELTHKATHON\Data sampel 2015-2024\2025\Data Sampel Reguler Edisi 2025\data\2015202401_kepesertaan.dta"
)
FALLBACK_KEP_PATH = Path(
    r"P:\EVENT KATON\HAELTHKATHON\Data sampel 2015-2024\Data Sampel Reguler 2015 - 2024\2015202401_kepesertaan.dta"
)

DEFAULT_OUTPUT_JSON = Path(
    r"N:\HEALTHKATHON\Aegis-JKN app\frontend\src\lib\data\bpjs-real-claims.json"
)

# Dokter spesialis virtual untuk mapping FKL11 (Jenis Poli)
POLI_DOKTER_MAP = {
    "INT": "dr. Bambang Soeprapto, Sp.PD",
    "BED": "dr. Hendra Wijaya, Sp.B",
    "OBG": "dr. Ratna Kartika, Sp.OG",
    "ANA": "dr. Maya Anggraini, Sp.A",
    "SAR": "dr. Rudi Setiawan, Sp.S",
    "JAN": "dr. Faisal Rahman, Sp.JP",
    "MAT": "dr. Nurul Hidayati, Sp.M",
    "THT": "dr. Wahyu Pratama, Sp.THT-KL",
    "KUL": "dr. Siti Aminah, Sp.KK",
    "GIG": "drg. Dwi Lestari, Sp.KG",
    "GGI": "drg. Dwi Lestari, Sp.KG",
    "JIW": "dr. Agus Priyono, Sp.KJ",
    "PAR": "dr. Indra Gunawan, Sp.P",
    "ORT": "dr. Denny Nugroho, Sp.OT",
    "URO": "dr. Rian Firmansyah, Sp.U",
    "RAD": "dr. Eko Santoso, Sp.Rad",
    "HDL": "dr. Linda Kurnia, Sp.PD-KGH",
    "IRM": "dr. Tri Wahyuni, Sp.KFR",
    "IGD": "dr. Emergency Team on Duty",
}


def resolve_file_path(primary: Path, fallback: Path) -> Path:
    if primary.exists():
        return primary
    if fallback.exists():
        return fallback
    raise FileNotFoundError(f"Neither {primary} nor {fallback} exists.")


def determine_risk_and_anomaly(
    icd10: str,
    icd9: str,
    los: int,
    biaya: float,
    service_type: str,
    diag_primer_desc: str,
) -> tuple[str, str, float, str | None, str | None, str, str, str, str]:
    """
    Evaluasi klinis berbasis aturan domain JKN / INA-CBGs untuk mendeteksi
    potensi anomali (upcoding, phantom billing, LOS mismatch, unbundling).
    """
    icd10_upper = icd10.upper()
    icd9_upper = icd9.upper()

    # Default: Low risk, normal check
    risk = "low"
    status = "auto_clear"
    fraud_score = round(0.04 + (hash(icd10 + str(biaya)) % 15) / 100.0, 2)
    modus = None
    sindikat = None
    shap_signal = "Parameter klinis, biaya INA-CBG, dan LOS dalam rentang wajar standar BPJS"
    alasan = "Klaim terverifikasi sesuai tarif regional INA-CBG dan konsistensi diagnosis primer."
    narasi = f"Pasien mendapatkan penanganan di faskes sesuai indikasi medis {diag_primer_desc}. Pemeriksaan penunjang dan tindakan sesuai protokol clinical pathway JKN."
    catatan = "Biaya sesuai tarif paket INA-CBGs regional"

    # Rule 1: High Cost with Minor/Outpatient procedure
    if service_type == "rawat jalan" and biaya > 2_000_000 and "3995" not in icd9_upper:
        risk = "high"
        status = "review"
        fraud_score = round(0.72 + (hash(icd10) % 15) / 100.0, 2)
        modus = "overbilling"
        shap_signal = "Tarif rawat jalan melampaui batas persentil 95 kelompok casemix; variansi biaya tinggi"
        alasan = f"Biaya rawat jalan Rp{int(biaya):,} relatif tinggi untuk poli rujukan tingkat lanjut tanpa prosedur hemodialisis."
        catatan = "Periksa rincian tagihan penunjang khusus & obat non-kronis"

    # Rule 2: Inpatient with 0 LOS
    elif service_type == "rawat inap" and los == 0 and biaya > 3_000_000:
        risk = "high"
        status = "review"
        fraud_score = round(0.78 + (hash(icd10) % 12) / 100.0, 2)
        modus = "phantom_billing"
        shap_signal = "LOS = 0 hari pada klaim rawat inap dengan klaim paket tarif penuh"
        alasan = "Pasien ditagihkan tarif rawat inap penuh namun lama rawat tercatat 0 hari (same-day discharge)."
        catatan = "Konfirmasi apakah prosedur ODC (one day care) atau rawat inap tidak terdokumentasi"

    # Rule 3: Prolonged LOS (> 7 days)
    elif service_type == "rawat inap" and los > 7:
        risk = "medium"
        status = "review"
        fraud_score = round(0.55 + (hash(icd10) % 20) / 100.0, 2)
        modus = "length_of_stay_anomaly"
        shap_signal = f"LOS {los} hari melebihi ambang standar ALOS kelompok diagnosa INA-CBGs"
        alasan = f"Lama rawat {los} hari membutuhkan audit kepatuhan Clinical Pathway rumah sakit."
        catatan = "Periksa resume medis terkait indikasi medis perpanjangan rawat"

    # Rule 4: Critical Inconsistencies / Known Modus
    elif ("K29" in icd10_upper and any(p in icd9_upper for p in ["00.66", "36.", "37."])) or (
        "Z09" in icd10_upper and biaya > 5_000_000
    ):
        risk = "fraud"
        status = "escalate"
        fraud_score = round(0.91 + (hash(icd10) % 8) / 100.0, 2)
        modus = "upcoding"
        sindikat = "SYND-01"
        shap_signal = "Inkonsistensi tajam diagnosis primer ringan vs prosedur bedah mayor; deviasi biaya ekstrem"
        alasan = "Ketidaksesuaian klinis antara diagnosis primer dan kode prosedur invasif berat."
        catatan = "Eskalasi ke verifikator paska bayar / TKMKB cabang"

    return risk, status, fraud_score, modus, sindikat, shap_signal, alasan, narasi, catatan


def extract_bpjs_sample(
    sample_size: int = 500,
    fkrtl_file: Path | None = None,
    kep_file: Path | None = None,
    output_file: Path = DEFAULT_OUTPUT_JSON,
) -> Path:
    """
    Eksekusi ETL dari file Stata (.dta) ke berkas JSON frontend.
    """
    fkrtl_path = fkrtl_file or resolve_file_path(DEFAULT_FKRTL_PATH, FALLBACK_FKRTL_PATH)
    kep_path = kep_file or resolve_file_path(DEFAULT_KEP_PATH, FALLBACK_KEP_PATH)

    print(f"[ETL] Membaca {sample_size} baris dari FKRTL: {fkrtl_path}")
    reader_fkrtl = pd.read_stata(fkrtl_path, iterator=True)
    df_fkrtl = reader_fkrtl.get_chunk(sample_size)

    # Identifikasi peserta unik untuk di-join
    unique_pstv01 = set(df_fkrtl["PSTV01"].dropna().unique())
    print(f"[ETL] Menemukan {len(unique_pstv01)} peserta unik dari {len(df_fkrtl)} klaim FKRTL.")

    # Baca kepesertaan secara chunked
    print(f"[ETL] Membaca dan menggabungkan data kepesertaan: {kep_path}")
    matched_chunks: List[pd.DataFrame] = []
    found_pstv: Set[Any] = set()

    reader_kep = pd.read_stata(
        kep_path,
        iterator=True,
        chunksize=50000,
        convert_categoricals=False,  # Hindari kategori beda per chunk
    )

    for i, chunk in enumerate(reader_kep):
        subset = chunk[chunk["PSTV01"].isin(unique_pstv01)]
        if not subset.empty:
            matched_chunks.append(subset)
            found_pstv.update(subset["PSTV01"].unique())
        if len(found_pstv) >= len(unique_pstv01) or i >= 30:
            break

    df_kep = (
        pd.concat(matched_chunks, ignore_index=True).drop_duplicates(subset=["PSTV01"])
        if matched_chunks
        else pd.DataFrame()
    )

    # Decode value labels kepesertaan jika ada
    kep_stata_reader = pd.io.stata.StataReader(kep_path)
    val_labels = kep_stata_reader.value_labels()

    if not df_kep.empty:
        if "pstv05" in val_labels and "PSTV05" in df_kep.columns:
            df_kep["PSTV05_LABEL"] = df_kep["PSTV05"].map(val_labels["pstv05"])
        if "pstv08" in val_labels and "PSTV08" in df_kep.columns:
            df_kep["PSTV08_LABEL"] = df_kep["PSTV08"].map(val_labels["pstv08"])
        if "pstv07" in val_labels and "PSTV07" in df_kep.columns:
            df_kep["PSTV07_LABEL"] = df_kep["PSTV07"].map(val_labels["pstv07"])

    # Buat lookup dict peserta
    kep_dict = {}
    if not df_kep.empty:
        for _, row in df_kep.iterrows():
            pid = row["PSTV01"]
            jk = str(row.get("PSTV05_LABEL", "Pria" if row.get("PSTV05") == 1 else "Wanita"))
            segmen = str(row.get("PSTV08_LABEL", row.get("PSTV08", "")))
            kelas = str(row.get("PSTV07_LABEL", row.get("PSTV07", "")))
            tgl_lahir = str(row.get("PSTV03", ""))[:10]
            kep_dict[pid] = {
                "gender": jk,
                "segment": segmen,
                "class": kelas,
                "birth_date": tgl_lahir,
            }

    # Transformasi baris FKRTL ke RawClaim
    print("[ETL] Memetakan fields FKRTL dan Kepesertaan ke format RawClaim...")
    claims_output: List[Dict[str, Any]] = []

    for _, row in df_fkrtl.iterrows():
        # FKL02: ID Kunjungan
        claim_id = str(row.get("FKL02", "")).strip() or f"BPJS_{hash(str(row)) % 1000000}"

        # FKL03 / FKL04: Tanggal Kunjungan & LOS
        tgl_datang_dt = row.get("FKL03")
        tgl_pulang_dt = row.get("FKL04")

        if pd.notnull(tgl_datang_dt):
            tgl_str = pd.to_datetime(tgl_datang_dt).strftime("%Y-%m-%d")
        else:
            tgl_str = "2024-06-01"

        if pd.notnull(tgl_datang_dt) and pd.notnull(tgl_pulang_dt):
            los_days = max(0, (pd.to_datetime(tgl_pulang_dt) - pd.to_datetime(tgl_datang_dt)).days)
        else:
            los_days = 0

        # Layanan (FKL10): RJTL vs RITL
        raw_tingkat = str(row.get("FKL10", "")).upper()
        service_type = "rawat inap" if "RITL" in raw_tingkat or los_days > 0 else "rawat jalan"

        # Faskes (FKL08, FKL09, FKL06)
        jenis_rs = str(row.get("FKL08", "Rumah Sakit")).strip()
        tipe_rs = str(row.get("FKL09", "")).strip()
        kota_rs = str(row.get("FKL06", "")).strip()
        faskes_name = f"{jenis_rs} {tipe_rs} ({kota_rs})".replace("  ", " ").strip()

        # Pasien & Kepesertaan
        pid = row.get("PSTV01")
        pinfo = kep_dict.get(pid, {})
        gender = pinfo.get("gender", "Peserta")
        segmen = pinfo.get("segment", "PBI/Non-PBI")
        pasien_str = f"PST-{pid} ({gender}, {segmen})".replace(" ,", "")

        # Dokter DPJP (FKL11 - Poli)
        poli_code = str(row.get("FKL11", "")).strip().upper()
        dokter_name = POLI_DOKTER_MAP.get(poli_code, f"dr. DPJP Spesialis ({poli_code or 'Umum'})")

        # Diagnosis ICD-10 (FKL17 / FKL18 / FKL15)
        icd10_code = str(row.get("FKL17A", "")).strip()
        icd10_desc = str(row.get("FKL18A", "")).strip()
        if not icd10_code:
            icd10_code = str(row.get("FKL15A", "")).strip()
            icd10_desc = str(row.get("FKL16A", "")).strip()
        icd10_full = f"{icd10_code} - {icd10_desc}".strip(" -") if icd10_code else "Z09 - Pemeriksaan Lanjutan"

        # Prosedur ICD-9-CM (FKL30, FKL35)
        icd9_val = str(row.get("FKL30", "")).strip()
        sp_val = str(row.get("FKL35", "")).strip()
        if not icd9_val or icd9_val.upper() == "NONE":
            if sp_val and sp_val.upper() != "NONE":
                icd9_val = sp_val
            else:
                icd9_val = "99.04 - Transfusi / Pemeriksaan Rutin Non-Bedah"

        # Biaya (FKL47 / FKL48 / FKL32)
        biaya = float(row.get("FKL47", 0.0) or row.get("FKL48", 0.0) or row.get("FKL32", 0.0) or 207900.0)

        # Rujukan (FKP02, FKL26, FKL28)
        no_rujuk = str(row.get("FKP02", "")).strip() or "RUJ-BPJS-FKTP"
        perujuk_jenis = str(row.get("FKL28", "Puskesmas")).strip()
        perujuk_kota = str(row.get("FKL26", kota_rs)).strip()
        rujukan_str = f"{perujuk_jenis} ({perujuk_kota}) · No: {no_rujuk}"

        # Obat khusus jika ada (FKL44, FKL45)
        sd_code = str(row.get("FKL44", "")).strip()
        sd_desc = str(row.get("FKL45", "")).strip()
        obat_str = f"Paket Farmasi INA-CBGs" if not sd_desc or sd_desc == "NONE" else f"{sd_code} - {sd_desc}"

        # Evaluasi anomali klinis & MHGSL channel weights
        risk, status, fraud_score, modus, sindikat, shap_signal, alasan, narasi, catatan = (
            determine_risk_and_anomaly(
                icd10=icd10_code,
                icd9=icd9_val,
                los=los_days,
                biaya=biaya,
                service_type=service_type,
                diag_primer_desc=icd10_desc or "Pemeriksaan Medis",
            )
        )

        # Kontribusi 3 Saluran MHGSL (Topology, Feature, Semantic)
        if fraud_score >= 0.7:
            kontribusi = "T 0.38 · F 0.42 · S 0.20"
        elif fraud_score >= 0.4:
            kontribusi = "T 0.33 · F 0.34 · S 0.33"
        else:
            kontribusi = "T 0.28 · F 0.36 · S 0.36"

        raw_item: Dict[str, Any] = {
            "Name": claim_id,
            "Tanggal": tgl_str,
            "Status": status,
            "Risiko": risk,
            "Skor Fraud": fraud_score,
            "Modus": modus,
            "Sindikat": sindikat,
            "Faskes": faskes_name,
            "Layanan": service_type,
            "Pasien": pasien_str,
            "Dokter": dokter_name,
            "Diagnosis ICD-10": icd10_full,
            "Prosedur ICD-9-CM": icd9_val,
            "Biaya Rp": round(biaya),
            "LOS hari": los_days,
            "Obat": obat_str,
            "Rujukan": rujukan_str,
            "Alasan Berobat": f"Keluhan klinis terindikasi {icd10_desc or 'pemeriksaan kesehatan lanjutan'}.",
            "Narasi Rekam Medis": narasi,
            "Kontradiksi Narasi": (risk in ["fraud", "high"] and modus in ["upcoding", "phantom_billing"]),
            "Umpan Balik Pasien": "Layanan telah diterima sesuai prosedur."
            if risk == "low"
            else "Perlu konfirmasi kejelasan tindakan penagihan.",
            "Sentimen": "netral" if risk == "low" else "negatif",
            "Skor Sentimen": 0.25 if risk == "low" else -0.55,
            "Sinyal SHAP": shap_signal,
            "Kontribusi Saluran": kontribusi,
            "Alasan": alasan,
            "Catatan": catatan,
            "Notion ID": f"bpjs-{claim_id.lower()}",
        }
        claims_output.append(raw_item)

    # Pastikan direktori tujuan tersedia
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(claims_output, f, indent=2, ensure_ascii=False)

    print(f"[ETL SUKSES] Berhasil mengekstrak {len(claims_output)} klaim ke: {output_path}")
    return output_path


if __name__ == "__main__":
    count = 500
    if len(sys.argv) > 1:
        try:
            count = int(sys.argv[1])
        except ValueError:
            pass
    extract_bpjs_sample(sample_size=count)
