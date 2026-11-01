"""
Aegis-JKN AI Reporting Service.
Uses the designated 'aegis-jkn' model from the configured 9router endpoint
to generate clinical audit reports, contradiction analyses, and verification dossiers.
"""
import json
import logging
import urllib.request
import urllib.error
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(usecwd=True))

logger = logging.getLogger(__name__)

ROUTER_BASE_URL = os.getenv("ROUTER_BASE_URL", "https://9router.biezz.my.id/v1")
ROUTER_URL = f"{ROUTER_BASE_URL.rstrip('/')}/chat/completions"
API_KEY = os.getenv("ROUTER_API_KEY", "")
MODEL_NAME = os.getenv("REPORTING_MODEL_NAME", "aegis-jkn")

def get_headers() -> Dict[str, str]:
    key = os.getenv("ROUTER_API_KEY", API_KEY)
    return {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "User-Agent": "Aegis-JKN-Reporting-Service/1.0"
    }

import re

def sanitize_ai_report(content: str) -> str:
    """
    Strips out any internal thinking traces (<think> tags, English chain-of-thought, etc.)
    to ensure only 100% clean, professional Indonesian clinical audit content is returned.
    """
    if not content:
        return ""

    # 1. Strip explicit thinking tags <think>...</think> and <thought>...</thought>
    cleaned = re.sub(r"<think>[\s\S]*?</think>", "", content, flags=re.IGNORECASE)
    cleaned = re.sub(r"<thought>[\s\S]*?</thought>", "", cleaned, flags=re.IGNORECASE)

    # 2. Check if text starts with English reasoning preamble (e.g. "The user wants...", "Let me analyze...")
    # Find the start of the actual Indonesian report headers
    header_patterns = [
        r"(#+\s*LAPORAN\s+AUDIT[\s\S]*)",
        r"(\*\*ID Klaim:\*\*[\s\S]*)",
        r"(#+\s*1\.\s*RINGKASAN[\s\S]*)",
        r"(\*?\*?1\.\s*\[ANALISIS[\s\S]*)",
        r"(\*?\*?1\.\s*\*\*\[ANALISIS[\s\S]*)"
    ]

    for pat in header_patterns:
        match = re.search(pat, cleaned, flags=re.IGNORECASE)
        if match:
            cleaned = match.group(1)
            break

    return cleaned.strip()


def call_aegis_jkn_model(messages: list, max_tokens: int = 3000, temperature: float = 0.1) -> str:
    """
    Calls the 9router API using the 'aegis-jkn' model.
    Extracts strictly the Indonesian content and strips any thinking or reasoning tokens.
    """
    active_model = os.getenv("REPORTING_MODEL_NAME", MODEL_NAME)
    payload = {
        "model": active_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature
    }

    req = urllib.request.Request(
        ROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=get_headers()
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            raw = response.read().decode("utf-8")
            
            # Clean possible trailing SSE stream chunks like 'data: [DONE]'
            clean_json_str = raw.split("data: [DONE]")[0].strip()
            data = json.loads(clean_json_str)
            
            choice = data["choices"][0]
            # Strictly read 'content', ignore 'reasoning'
            raw_content = choice["message"].get("content") or ""
            return sanitize_ai_report(raw_content)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        logger.error(f"HTTP Error {e.code} calling {MODEL_NAME}: {err_msg}")
        raise RuntimeError(f"Gagal memanggil model {MODEL_NAME} (HTTP {e.code}): {err_msg}")
    except Exception as e:
        logger.error(f"Exception calling {MODEL_NAME}: {str(e)}")
        raise RuntimeError(f"Gagal terhubung ke model {MODEL_NAME}: {str(e)}")

    req = urllib.request.Request(
        ROUTER_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=get_headers()
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            raw = response.read().decode("utf-8")
            
            # Clean possible trailing SSE stream chunks like 'data: [DONE]'
            clean_json_str = raw.split("data: [DONE]")[0].strip()
            data = json.loads(clean_json_str)
            
            choice = data["choices"][0]
            # Strictly read 'content', ignore 'reasoning'
            raw_content = choice["message"].get("content") or ""
            return sanitize_ai_report(raw_content)
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="ignore")
        logger.error(f"HTTP Error {e.code} calling {MODEL_NAME}: {err_msg}")
        raise RuntimeError(f"Gagal memanggil model {MODEL_NAME} (HTTP {e.code}): {err_msg}")
    except Exception as e:
        logger.error(f"Exception calling {MODEL_NAME}: {str(e)}")
        raise RuntimeError(f"Gagal terhubung ke model {MODEL_NAME}: {str(e)}")

def generate_claim_audit_report(claim: Dict[str, Any], mhgsl_scores: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Generates an expert clinical audit report for a specific claim.
    """
    claim_id = claim.get("id") or claim.get("Name", "KLM001")
    diagnosis = claim.get("diagnosisIcd10") or claim.get("Diagnosis ICD-10", "-")
    procedure = claim.get("procedureIcd9") or claim.get("Prosedur ICD-9-CM", "-")
    cost = claim.get("costRp") or claim.get("Biaya Rp", 0)
    los = claim.get("losDays") or claim.get("LOS hari", 0)
    narrative = claim.get("clinicalNarrative") or claim.get("Narasi Rekam Medis", "-")
    feedback = claim.get("patientFeedback") or claim.get("Umpan Balik Pasien", "-")
    contradiction = claim.get("hasContradiction") or claim.get("Kontradiksi Narasi", False)
    
    t_score = mhgsl_scores.get("topology", 0.33) if mhgsl_scores else 0.33
    f_score = mhgsl_scores.get("feature", 0.33) if mhgsl_scores else 0.33
    s_score = mhgsl_scores.get("semantic", 0.34) if mhgsl_scores else 0.34
    fraud_score = mhgsl_scores.get("fraud_score", 0.5) if mhgsl_scores else claim.get("fraudScore", 0.5)

    system_prompt = (
        "Kamu adalah Spesialis Auditor Medis & Pencegahan Kecurangan (Anti-Fraud P2PK) BPJS Kesehatan tingkat ahli.\n"
        "ATURAN MUTLAK:\n"
        "1. Gunakan 100% BAHASA INDONESIA formal medis standar BPJS Kesehatan.\n"
        "2. DILARANG KERAS memunculkan proses berpikir internal (thinking/chain-of-thought/preamble) dalam bahasa Inggris.\n"
        "3. DILARANG menulis kalimat pengantar seperti 'The user wants...' atau 'Let me analyze...'.\n"
        "4. LANGSUNG mulai respons dengan judul laporan:\n"
        "# LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN"
    )

    user_prompt = f"""
Berkas Klaim BPJS Kesehatan:
- ID Klaim: {claim_id}
- Faskes: {claim.get('hospital') or claim.get('Faskes', '-')}
- Dokter DPJP: {claim.get('doctor') or claim.get('Dokter', '-')}
- Diagnosis Primer (ICD-10): {diagnosis}
- Prosedur Ditagih (ICD-9-CM): {procedure}
- Biaya Klaim: Rp {cost:,.0f} | Lama Rawat (LOS): {los} hari
- Narasi Rekam Medis DPJP: "{narrative}"
- Umpan Balik Pasien: "{feedback}"
- Flag Kontradiksi Narasi: {'YA (TERDETEKSI KONTRADIKSI KLINIS)' if contradiction else 'TIDAK'}

    system_prompt = (
        "Kamu adalah Spesialis Auditor Medis & Pencegahan Kecurangan (Anti-Fraud P2PK) BPJS Kesehatan tingkat ahli.\n"
        "ATURAN MUTLAK:\n"
        "1. Gunakan 100% BAHASA INDONESIA formal medis standar BPJS Kesehatan.\n"
        "2. DILARANG KERAS memunculkan proses berpikir internal (thinking/chain-of-thought/preamble) dalam bahasa Inggris.\n"
        "3. DILARANG menulis kalimat pengantar seperti 'The user wants...' atau 'Let me analyze...'.\n"
        "4. LANGSUNG mulai respons dengan judul laporan:\n"
        "# LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN\n"
        "5. WAJIB menyertakan 4 section LENGKAP dengan konten substansial (minimal 3-4 kalimat per section).\n"
        "6. SETIAP section WAJIB memiliki konten substansial (minimal 3-4 kalimat per section).\n"
        "7. JANGAN gunakan format bullet points yang terlalu singkat - gunakan paragraf penjelasan lengkap.\n"
        "6. SETIAP section WAJIB memiliki konten substansial (minimal 3-4 kalimat per section).\n"
        "7. JANGAN gunakan format bullet points yang terlalu singkat - gunakan paragraf penjelasan lengkap.\n"
    )

    # Pre-format all values to avoid f-string formatting issues
    formatted_cost = f"{cost:,.0f}"
    formatted_fraud_pct = f"{fraud_score * 100:.1f}"
    formatted_risk_pct = f"{fraud_score * 100:.0f}"
    formatted_t_score = f"{t_score:.2f}"
    formatted_f_score = f"{f_score:.2f}"
    formatted_s_score = f"{s_score:.2f}"
    formatted_fraud_score = f"{fraud_score:.2f}"
    
        user_prompt = f"""
        Berkas Klaim BPJS Kesehatan:
        - ID Klaim: {claim_id}
        - Faskes: {claim.get('hospital') or claim.get('Faskes', '-')}
        - Dokter DPJP: {claim.get('doctor') or claim.get('Dokter', '-')}
        - Diagnosis Primer (ICD-10): {diagnosis}
        - Prosedur Ditagih (ICD-9-CM): {procedure}
        - Biaya Klaim: Rp {formatted_cost} | Lama Rawat (LOS): {los} hari
        - Narasi Rekam Medis DPJP: "{narrative}"
        - Umpan Balik Pasien: "{feedback}"
        - Flag Kontradiksi Narasi: {'YA (TERDETEKSI KONTRADIKSI KLINIS)' if contradiction else 'TIDAK'}

        Hasil Inferensi Model Graf MHGSL:
        - Probabilitas Fraud: {formatted_fraud_pct}%
        - Kontribusi Kanal: Topologi T={formatted_t_score}, Fitur F={formatted_f_score}, Semantik S={formatted_s_score}

        Susun laporan audit dalam format markdown berikut:
        # LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN
        **ID Klaim:** {claim_id} | **Faskes:** {claim.get('hospital') or claim.get('Faskes', '-')} | **Status Risiko:** {formatted_risk_pct}%

        ## 1. [ANALISIS KLINIS & KODING INA-CBG]
        Evaluasi kesesuaian diagnosis dan tindakan medis yang ditagihkan. Jelaskan mengapa diagnosis dan prosedur sesuai atau tidak sesuai secara klinis. Bandingkan dengan standar INA-CBG dan pedoman klinis.

        ## 2. [EVALUASI KONTRADIKSI NARASI]
        Analisis diskrepansi antara rekam medis dokter dan pengakuan pasien. Jelaskan apakah ada kontradiksi antara narasi DPJP dengan aduan pasien, serta indikasi phantom billing atau upcoding.

        ## 3. [INTERPRETASI GRAF MHGSL & ANTI-KAMUFLASE]
        Uraikan arti bobot 3 kanal (Topologi, Fitur, Semantik) dalam mendeteksi sindikat kolusi. Jelaskan bagaimana bobot T={formatted_t_score}, F={formatted_f_score}, S={formatted_s_score} berkontribusi pada skor fraud {formatted_fraud_score}. Jelaskan mekanisme anti-kamuflase sindikat.

        ## 4. [REKOMENDASI PUTUSAN VERIFIKATOR]
        Putusan definitif (SETUJUI / KLARIFIKASI RS / ESKALASI P2PK) beserta dasar regulasi penjaminan. Jelaskan alasan putusan secara rinci berdasarkan bukti klinis dan graf MHGSL.

        KETENTUAN WAJIB:
        - SETIAP section WAJIB memiliki minimal 3-4 kalimat penjelasan lengkap.
        - JANGAN gunakan format bullet points yang terlalu singkat - gunakan paragraf penjelasan lengkap.
        - WAJIB menyertakan analisis mendalam untuk setiap section.
        - JANGAN singkat atau memotong penjelasan.
        - WAJIB menyertakan analisis mendalam untuk setiap section.
        """

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        report_text = call_aegis_jkn_model(messages, max_tokens=3000, temperature=0.1)

        return {
            "claim_id": claim_id,
            "model_used": MODEL_NAME,
            "report": report_text,
            "fraud_score": fraud_score
        }
        - Umpan Balik Pasien: "{feedback}"
        - Flag Kontradiksi Narasi: {'YA (TERDETEKSI KONTRADIKSI KLINIS)' if contradiction else 'TIDAK'}

        Hasil Inferensi Model Graf MHGSL:
        - Probabilitas Fraud: {formatted_fraud_pct}%
        - Kontribusi Kanal: Topologi T={formatted_t_score}, Fitur F={formatted_f_score}, Semantik S={formatted_s_score}

        Susun laporan audit dalam format markdown berikut:
        # LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN
        **ID Klaim:** {claim_id} | **Faskes:** {claim.get('hospital') or claim.get('Faskes', '-')} | **Status Risiko:** {formatted_risk_pct}%

        ## 1. [ANALISIS KLINIS & KODING INA-CBG]
        Evaluasi kesesuaian diagnosis dan tindakan medis yang ditagihkan. Jelaskan mengapa diagnosis dan prosedur sesuai atau tidak sesuai secara klinis. Bandingkan dengan standar INA-CBG dan pedoman klinis.

        ## 2. [EVALUASI KONTRADIKSI NARASI]
        Analisis diskrepansi antara rekam medis dokter dan pengakuan pasien. Jelaskan apakah ada kontradiksi antara narasi DPJP dengan aduan pasien, serta indikasi phantom billing atau upcoding.

    report_text = call_aegis_jkn_model(messages, max_tokens=3000, temperature=0.1)

        return {
            "claim_id": claim_id,
            "model_used": MODEL_NAME,
            "report": report_text,
            "fraud_score": fraud_score
        }
    - Umpan Balik Pasien: "{feedback}"
    - Flag Kontradiksi Narasi: {'YA (TERDETEKSI KONTRADIKSI KLINIS)' if contradiction else 'TIDAK'}

    Hasil Inferensi Model Graf MHGSL:
    - Probabilitas Fraud: {formatted_fraud_pct}%
    - Kontribusi Kanal: Topologi T={formatted_t_score}, Fitur F={formatted_f_score}, Semantik S={formatted_s_score}

    Susun laporan audit dalam format markdown berikut:
    # LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN
    **ID Klaim:** {claim_id} | **Faskes:** {claim.get('hospital') or claim.get('Faskes', '-')} | **Status Risiko:** {formatted_risk_pct}%

    ## 1. [ANALISIS KLINIS & KODING INA-CBG]
    Evaluasi kesesuaian diagnosis dan tindakan medis yang ditagihkan. Jelaskan mengapa diagnosis dan prosedur sesuai atau tidak sesuai secara klinis. Bandingkan dengan standar INA-CBG dan pedoman klinis.

    ## 2. [EVALUASI KONTRADIKSI NARASI]
    Analisis diskrepansi antara rekam medis dokter dan pengakuan pasien. Jelaskan apakah ada kontradiksi antara narasi DPJP dengan aduan pasien, serta indikasi phantom billing atau upcoding.

    ## 3. [INTERPRETASI GRAF MHGSL & ANTI-KAMUFLASE]
    Uraikan arti bobot 3 kanal (Topologi, Fitur, Semantik) dalam mendeteksi sindikat kolusi. Jelaskan bagaimana bobot T={formatted_t_score}, F={formatted_f_score}, S={formatted_s_score} berkontribusi pada skor fraud {formatted_fraud_score}. Jelaskan mekanisme anti-kamuflase sindikat.

    ## 4. [REKOMENDASI PUTUSAN VERIFIKATOR]
    Putusan definitif (SETUJUI / KLARIFIKASI RS / ESKALASI P2PK) beserta dasar regulasi penjaminan. Jelaskan alasan putusan secara rinci berdasarkan bukti klinis dan graf MHGSL.

    KETENTUAN WAJIB:
    - SETIAP section WAJIB memiliki minimal 3-4 kalimat penjelasan lengkap.
    - JANGAN gunakan format bullet points yang terlalu singkat - gunakan paragraf penjelasan lengkap.
    - WAJIB menyertakan analisis mendalam untuk setiap section.
    - JANGAN singkat atau memotong penjelasan.
    - WAJIB menyertakan analisis mendalam untuk setiap section.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    report_text = call_aegis_jkn_model(messages, max_tokens=3000, temperature=0.1)

    return {
        "claim_id": claim_id,
        "model_used": MODEL_NAME,
        "report": report_text,
        "fraud_score": fraud_score
    }
    Uraikan arti bobot 3 kanal (Topologi, Fitur, Semantik) dalam mendeteksi sindikat kolusi. Jelaskan bagaimana bobot T={t_score:.2f}, F={f_score:.2f}, S={s_score:.2f} berkontribusi pada skor fraud {fraud_score:.2f}. Jelaskan mekanisme anti-kamuflase sindikat.

    ## 4. [REKOMENDASI PUTUSAN VERIFIKATOR]
    Putusan definitif (SETUJUI / KLARIFIKASI RS / ESKALASI P2PK) beserta dasar regulasi penjaminan. Jelaskan alasan putusan secara rinci berdasarkan bukti klinis dan graf MHGSL.

    KETENTUAN WAJIB:
    - SETIAP section WAJIB memiliki minimal 3-4 kalimat penjelasan lengkap.
    - JANGAN gunakan format bullet points yang terlalu singkat - gunakan paragraf penjelasan lengkap.
    - WAJIB menyertakan analisis mendalam untuk setiap section.
    - JANGAN singkat atau memotong penjelasan.
    - WAJIB menyertakan analisis mendalam untuk setiap section.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    report_text = call_aegis_jkn_model(messages, max_tokens=3000, temperature=0.1)

    return {
        "claim_id": claim_id,
        "model_used": MODEL_NAME,
        "report": report_text,
        "fraud_score": fraud_score
    }

## 1. [ANALISIS KLINIS & KODING INA-CBG]
Evaluasi kesesuaian diagnosis dan tindakan medis yang ditagihkan.

## 2. [EVALUASI KONTRADIKSI NARASI]
Analisis diskrepansi antara rekam medis dokter dan pengakuan pasien.

    system_prompt = (
        "Kamu adalah Spesialis Auditor Medis & Pencegahan Kecurangan (Anti-Fraud P2PK) BPJS Kesehatan tingkat ahli.\n"
        "ATURAN MUTLAK:\n"
        "1. Gunakan 100% BAHASA INDONESIA formal medis standar BPJS Kesehatan.\n"
        "2. DILARANG KERAS memunculkan proses berpikir internal (thinking/chain-of-thought/preamble) dalam bahasa Inggris.\n"
        "3. DILARANG menulis kalimat pengantar seperti 'The user wants...' atau 'Let me analyze...'.\n"
        "4. LANGSUNG mulai respons dengan judul laporan:\n"
        "# LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN\n"
        "5. WAJIB menyertakan 4 section LENGKAP dengan konten substansial (minimal 3-4 kalimat per section).\n"
        "6. SETIAP section WAJIB memiliki konten substansial (minimal 3-4 kalimat per section).\n"
    formatted_t_score = f"{t_score:.2f}"
    formatted_f_score = f"{f_score:.2f}"
    formatted_s_score = f"{s_score:.2f}"
    formatted_fraud_score = f"{fraud_score:.2f}"
    
    user_prompt = f"""
    - ID Klaim: {claim_id}
    - Faskes: {claim.get('hospital') or claim.get('Faskes', '-')}
    - Dokter DPJP: {claim.get('doctor') or claim.get('Dokter', '-')}
    - Diagnosis Primer (ICD-10): {diagnosis}
    - Prosedur Ditagih (ICD-9-CM): {procedure}
    - Biaya Klaim: Rp {formatted_cost} | Lama Rawat (LOS): {los} hari
    - Narasi Rekam Medis DPJP: "{narrative}"
    - Umpan Balik Pasien: "{feedback}"
    - Flag Kontradiksi Narasi: {'YA (TERDETEKSI KONTRADIKSI KLINIS)' if contradiction else 'TIDAK'}

    - Probabilitas Fraud: {formatted_fraud_pct}%
    - Kontribusi Kanal: Topologi T={formatted_t_score}, Fitur F={formatted_f_score}, Semantik S={formatted_s_score}
    Susun laporan audit dalam format markdown berikut:
    # LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN
    **ID Klaim:** {claim_id} | **Faskes:** {claim.get('hospital') or claim.get('Faskes', '-')} | **Status Risiko:** {formatted_risk_pct}%

    ## 1. [ANALISIS KLINIS & KODING INA-CBG]
    Evaluasi kesesuaian diagnosis dan tindakan medis yang ditagihkan. Jelaskan mengapa diagnosis dan prosedur sesuai atau tidak sesuai secara klinis. Bandingkan dengan standar INA-CBG dan pedoman klinis.
    ...

## 1. [ANALISIS KLINIS & KODING INA-CBG]
Evaluasi kesesuaian diagnosis dan tindakan medis yang ditagihkan. Jelaskan mengapa diagnosis dan prosedur sesuai atau tidak sesuai secara klinis. Bandingkan dengan standar INA-CBG dan pedoman klinis.

## 2. [EVALUASI KONTRADIKSI NARASI]
Analisis diskrepansi antara rekam medis dokter dan pengakuan pasien. Jelaskan apakah ada kontradiksi antara narasi DPJP dengan aduan pasien, serta indikasi phantom billing atau upcoding.
## 3. [INTERPRETASI GRAF MHGSL & ANTI-KAMUFLASE]
Uraikan arti bobot 3 kanal (Topologi, Fitur, Semantik) dalam mendeteksi sindikat kolusi. Jelaskan bagaimana bobot T={formatted_t_score}, F={formatted_f_score}, S={formatted_s_score} berkontribusi pada skor fraud {formatted_fraud_score}. Jelaskan mekanisme anti-kamuflase sindikat.
Putusan definitif (SETUJUI / KLARIFIKASI RS / ESKALASI P2PK) beserta dasar regulasi penjaminan. Jelaskan alasan putusan secara rinci berdasarkan bukti klinis dan graf MHGSL.

KETENTUAN WAJIB:
- SETIAP section WAJIB memiliki minimal 3-4 kalimat penjelasan lengkap.
- JANGAN gunakan format bullet points yang terlalu singkat - gunakan paragraf penjelasan lengkap.
- WAJIB menyertakan analisis mendalam untuk setiap section.
- JANGAN singkat atau memotong penjelasan.
- WAJIB menyertakan analisis mendalam untuk setiap section.

"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    report_text = call_aegis_jkn_model(messages, max_tokens=3000, temperature=0.1)

    return {
        "claim_id": claim_id,
        "model_used": MODEL_NAME,
        "report": report_text,
        "fraud_score": fraud_score
    }
