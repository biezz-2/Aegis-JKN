"""Dump live Notion databases (claims v2, dataset research) to local CSV/JSON for agent analysis."""
import csv
import json
import os
import time
import urllib.request

TOKEN = os.environ["NOTION_TOKEN"]
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
OUT = r"N:\HEALTHKATHON\analysis\corpus"

CLAIMS_DB = "c783afb3d0d4458295456180b7b7756b"
DATASET_DB = "310b35a5934642dfaf47df9897cdcda1"


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def post(url, payload):
    req = urllib.request.Request(url, headers=HEADERS, data=json.dumps(payload).encode())
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def rt(items):
    return "".join(i.get("plain_text", "") for i in (items or []))


def prop_to_val(p):
    t = p.get("type")
    if t == "title":
        return rt(p["title"])
    if t == "rich_text":
        return rt(p["rich_text"])
    if t == "number":
        return p.get("number")
    if t == "select":
        return (p.get("select") or {}).get("name")
    if t == "multi_select":
        return "; ".join(s["name"] for s in p.get("multi_select", []))
    if t == "checkbox":
        return p.get("checkbox")
    if t == "date":
        return (p.get("date") or {}).get("start")
    if t == "url":
        return p.get("url")
    if t == "formula":
        return p.get("formula")
    if t == "number":
        return p.get("number")
    return None


def query_all(db_id):
    rows = []
    cursor = None
    while True:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor
        d = post(f"https://api.notion.com/v1/databases/{db_id}/query", payload)
        rows.extend(d.get("results", []))
        if not d.get("has_more"):
            break
        cursor = d.get("next_cursor")
        time.sleep(0.3)
    return rows


def dump(db_id, out_name, title_key):
    rows = query_all(db_id)
    # collect columns in stable order
    cols = []
    for r in rows:
        for k in r.get("properties", {}):
            if k not in cols:
                cols.append(k)
    out = []
    for r in rows:
        rec = {c: prop_to_val(r["properties"].get(c, {})) for c in cols}
        rec["_notion_page_id"] = r["id"]
        rec["_last_edited"] = r.get("last_edited_time")
        out.append(rec)
    path = os.path.join(OUT, out_name)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols + ["_notion_page_id", "_last_edited"])
        w.writeheader()
        for rec in out:
            w.writerow({c: ("" if rec[c] is None else rec[c]) for c in cols + ["_notion_page_id", "_last_edited"]})
    print(f"{out_name}: {len(out)} rows, {len(cols)} cols -> {path}")
    return out


if __name__ == "__main__":
    claims = dump(CLAIMS_DB, "claims_v2_live.csv", "Name")
    ds = dump(DATASET_DB, "dataset_research_live.csv", "Item")
    # also raw json for full fidelity
    with open(os.path.join(OUT, "claims_v2_live.json"), "w", encoding="utf-8") as f:
        json.dump(claims, f, ensure_ascii=False, indent=1)
    with open(os.path.join(OUT, "dataset_research_live.json"), "w", encoding="utf-8") as f:
        json.dump(ds, f, ensure_ascii=False, indent=1)
    print("json written")
