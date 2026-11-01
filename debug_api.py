import urllib.request, json, os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(usecwd=True))

headers = {
    'Authorization': f'Bearer {os.getenv("ROUTER_API_KEY")}',
    'Content-Type': 'application/json',
    'User-Agent': 'Aegis-JKN-Test/1.0'
}

claim_id = '238520824V006219'
system_prompt = (
    "Kamu adalah Spesialis Auditor Medis & Pencegahan Kecurangan (Anti-Fraud P2PK) BPJS Kesehatan tingkat ahli.\n"
    "ATURAN MUTLAK:\n"
    "1. Gunakan 100% BAHASA INDONESIA formal medis standar BPJS Kesehatan.\n"
    "2. DILARANG KERAS memunculkan proses berpikir internal (thinking/chain-of-thought/preamble) dalam bahasa Inggris.\n"
    "3. DILARANG menulis kalimat pengantar seperti 'The user wants...' atau 'Let me analyze...'.\n"
    "4. LANGSUNG mulai respons dengan judul laporan:\n"
    "# LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN"
)

user_prompt = """
Berkas Klaim BPJS Kesehatan:
- ID Klaim: 238520824V006219
- Faskes: Rumah sakit RS Kelas B (KOTA LANGSA)
- Dokter DPJP: dr. DPJP Spesialis
- Diagnosis Primer (ICD-10): S72 - Pertrochanteric fracture, closed
- Prosedur Ditagih (ICD-9-CM): 3995 - Hemodialysis; 7935 - Open reduction of fracture of femur with internal fixation; 8826 - Other skeletal x-ray of pelvis and hip; 8827 - Skeletal x-ray of thigh, knee, and lower leg; 8952 - Electrocardiogram; 9904 - Transfusion of packed cells
- Biaya Klaim: Rp 25,097,100 | Lama Rawat (LOS): 10 hari
- Narasi Rekam Medis DPJP: "Pasien dirawat dengan indikasi S72 Pertrochanteric fracture, closed. Tindakan dan pemeriksaan penunjang sesuai protokol klinis."
- Umpan Balik Pasien: "Pemeriksaan dan tindakan operasi berjalan baik."
- Flag Kontradiksi Narasi: TIDAK

Hasil Inferensi Model Graf MHGSL:
- Probabilitas Fraud: 68.0%
- Kontribusi Kanal: Topologi T=0.33, Fitur F=0.33, Semantik S=0.34

Susun laporan audit dalam format markdown berikut:
# LAPORAN AUDIT KLINIS KLAIM BPJS KESEHATAN
**ID Klaim:** 238520824V006219 | **Faskes:** Rumah sakit RS Kelas B (KOTA LANGSA) | **Status Risiko:** 68%

## 1. [ANALISIS KLINIS & KODING INA-CBG]
Evaluasi kesesuaian diagnosis dan tindakan medis yang ditagihkan.

## 2. [EVALUASI KONTRADIKSI NARASI]
Analisis diskrepansi antara rekam medis dokter dan pengakuan pasien.

## 3. [INTERPRETASI GRAF MHGSL & ANTI-KAMUFLASE]
Uraikan arti bobot 3 kanal dan indikasi sindikat kolusi.

## 4. [REKOMENDASI PUTUSAN VERIFIKATOR]
Putusan definitif (SETUJUI / KLARIFIKASI RS / ESKALASI P2PK) beserta dasar regulasi penjaminan.
"""

payload = {
    'model': 'aegis-jkn',
    'messages': [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ],
    'max_tokens': 800,
    'temperature': 0.1
}

req = urllib.request.Request('https://9router.biezz.my.id/v1/chat/completions', data=json.dumps(payload).encode('utf-8'), headers=headers)
with urllib.request.urlopen(req, timeout=60) as resp:
    raw = resp.read().decode('utf-8').split('data: [DONE]')[0].strip()
    data = json.loads(raw)
    choice = data['choices'][0]
    print('finish_reason:', choice.get('finish_reason'))
    print('usage:', data.get('usage'))
    print('choice keys:', list(choice.keys()))
    msg = choice.get('message', {})
    print('message keys:', list(msg.keys()))
    print('reasoning length:', len(msg.get('reasoning') or ''))
    print('content length:', len(msg.get('content') or ''))
    print('content text:\n', msg.get('content') or '')
