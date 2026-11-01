import json

def extract_props(props):
    res = {}
    for k, v in props.items():
        vtype = v.get('type')
        if vtype == 'title':
            res[k] = ''.join([t.get('plain_text', '') for t in v.get('title', [])])
        elif vtype == 'rich_text':
            res[k] = ''.join([t.get('plain_text', '') for t in v.get('rich_text', [])])
        elif vtype == 'select':
            res[k] = v.get('select', {}).get('name') if v.get('select') else None
        elif vtype == 'url':
            res[k] = v.get('url')
        elif vtype == 'number':
            res[k] = v.get('number')
        elif vtype == 'date':
            res[k] = v.get('date', {}).get('start') if v.get('date') else None
        elif vtype == 'checkbox':
            res[k] = v.get('checkbox', False)
        else:
            res[k] = None
    return res

with open('n:/HEALTHKATHON/Notion-docs/dataset_db.json', 'r', encoding='utf-8') as f:
    ds_raw = json.load(f)['results']

research_records = []
for item in ds_raw:
    p = extract_props(item['properties'])
    clean_id = item['id'].replace('-', '')
    research_records.append({
        'id': item['id'],
        'item': p.get('Item', ''),
        'kategori': p.get('Kategori', 'Umum'),
        'relevansi': p.get('Relevansi', 'Tinggi'),
        'statusVerifikasi': p.get('Status Verifikasi', 'Terverifikasi'),
        'sumberRiset': p.get('Sumber Riset'),
        'deskripsi': p.get('Deskripsi', ''),
        'pendekatanTeknis': p.get('Pendekatan Deteksi/Teknis', ''),
        'catatanRiset': p.get('Catatan Riset', ''),
        'notionUrl': item.get('url', f'https://notion.so/{clean_id}')
    })

with open('n:/HEALTHKATHON/Notion-docs/claims_db.json', 'r', encoding='utf-8') as f:
    cl_raw = json.load(f)['results']

claim_records = []
for item in cl_raw:
    p = extract_props(item['properties'])
    clean_id = item['id'].replace('-', '')
    claim_records.append({
        'id': p.get('Name', ''),
        'notionId': item['id'],
        'tanggal': p.get('Tanggal', ''),
        'layanan': p.get('Layanan', 'rawat inap'),
        'faskes': p.get('Faskes', ''),
        'rujukan': p.get('Rujukan', ''),
        'dokter': p.get('Dokter', ''),
        'pasien': p.get('Pasien', ''),
        'diagnosisIcd10': p.get('Diagnosis ICD-10', ''),
        'prosedurIcd9': p.get('Prosedur ICD-9-CM', ''),
        'obat': p.get('Obat', ''),
        'biayaRp': p.get('Biaya Rp', 0),
        'losHari': p.get('LOS hari', 0),
        'alasanBerobat': p.get('Alasan Berobat', ''),
        'narasiRekamMedis': p.get('Narasi Rekam Medis', ''),
        'kontradiksiNarasi': bool(p.get('Kontradiksi Narasi', False)),
        'skorFraud': p.get('Skor Fraud', 0.0),
        'risiko': p.get('Risiko', 'low'),
        'modus': p.get('Modus'),
        'sindikat': p.get('Sindikat'),
        'sinyalShap': p.get('Sinyal SHAP', ''),
        'kontribusiSaluran': p.get('Kontribusi Saluran', ''),
        'sentimen': p.get('Sentimen', 'netral'),
        'skorSentimen': p.get('Skor Sentimen', 0.0),
        'umpanBalikPasien': p.get('Umpan Balik Pasien', ''),
        'status': p.get('Status', 'auto_clear'),
        'alasan': p.get('Alasan', ''),
        'catatan': p.get('Catatan', '')
    })

research_json = json.dumps(research_records, ensure_ascii=False, indent=2)
claims_json = json.dumps(claim_records, ensure_ascii=False, indent=2)

ts_content = f'''import type {{ ClaimRecord, ResearchRecord }} from "@/types/dataset";

export const NOTION_RESEARCH_DATASET: ResearchRecord[] = {research_json};

export const NOTION_CLAIMS_DATASET: ClaimRecord[] = {claims_json};
'''

with open('n:/HEALTHKATHON/Aegis-JKN/src/data/notion-datasets.ts', 'w', encoding='utf-8') as f:
    f.write(ts_content)

print(f"Successfully exported {len(research_records)} research records and {len(claim_records)} claims records to src/data/notion-datasets.ts")
