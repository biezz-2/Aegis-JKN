"""Dump all HEALTHKATHON Notion pages to local markdown files for agent analysis."""
import json
import os
import time
import urllib.request

TOKEN = os.environ["NOTION_TOKEN"]
BASE = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}

OUT = r"N:\HEALTHKATHON\analysis\corpus"
os.makedirs(OUT, exist_ok=True)

PAGES = {
    "00-dashboard": "4003e603-1ab7-815a-89bd-edc0c4d92c2f",
    "01-proposal": "4003e603-1ab7-8170-bc22-fe391c6a3a2a",
    "02-architecture": "4003e603-1ab7-81ef-bcda-c7b0dbdd0cad",
    "03-dataset-registry": "4003e603-1ab7-8174-9a55-d4ee8fff3fd2",
    "04-evidence-matrix": "4003e603-1ab7-814f-8ac3-f37808c0a4a5",
    "05-decision-scope": "4003e6031ab78156b244cccd2c5ecd9e",
    "06-research-notes": "4003e603-1ab7-8135-a0fa-ce33631104ab",
    "07-dataset-v2-catalog": "4003e6031ab78179bcc7ca76a0b80fbc",
    "08-training-protocol": "4003e603-1ab7-8197-8715-f1de059e82ef",
    "09-draft-hub": "4003e603-1ab7-8040-a0eb-ec875c0954eb",
    "10-simulation-dataset": "3f23e603-1ab7-81bf-99a7-d3f1768f1708",
    "11-archive-proposal": "3f63e603-1ab7-8141-a724-fc301304942b",
    "12-archive-architecture": "3ef3e603-1ab7-81d1-962a-f8955843ed0f",
    "13-archive-deep-research": "3fe3e603-1ab7-8008-8ce1-f3201c252bed",
    "14-index": "3f23e603-1ab7-808d-b2cb-fe92cd62391d",
}


def get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def rich_text(items):
    out = []
    for it in items or []:
        t = it.get("plain_text", "")
        if it.get("href"):
            t = f"[{t}]({it['href']})"
        out.append(t)
    return "".join(out)


def block_to_md(b, depth=0):
    t = b.get("type")
    body = b.get(t, {}) if isinstance(b.get(t), dict) else {}
    txt = rich_text(body.get("rich_text"))
    indent = "  " * depth
    lines = []

    if t == "paragraph":
        lines.append(f"{indent}{txt}" if txt else "")
    elif t in ("heading_1", "heading_2", "heading_3"):
        lvl = int(t[-1])
        lines.append(f"{indent}{'#' * lvl} {txt}")
    elif t == "bulleted_list_item":
        lines.append(f"{indent}- {txt}")
    elif t == "numbered_list_item":
        lines.append(f"{indent}1. {txt}")
    elif t == "to_do":
        mark = "x" if body.get("checked") else " "
        lines.append(f"{indent}- [{mark}] {txt}")
    elif t == "toggle":
        lines.append(f"{indent}**{txt}**")
    elif t == "quote":
        lines.append(f"{indent}> {txt}")
    elif t == "callout":
        lines.append(f"{indent}> **{body.get('icon', {})}** {txt}")
    elif t == "code":
        lines.append(f"{indent}```{body.get('language', '')}\n{indent}{txt}\n{indent}```")
    elif t == "divider":
        lines.append(f"{indent}---")
    elif t == "table":
        rows = body.get("cells", [])
        for i, row in enumerate(rows):
            cells = [rich_text(c).replace("\n", " ") for c in row]
            lines.append(f"{indent}| " + " | ".join(cells) + " |")
            if i == 0:
                lines.append(f"{indent}|" + "---|" * len(cells))
    elif t == "child_page":
        lines.append(f"{indent}## [Sub-page] {body.get('title', '')}")
    elif t in ("child_database",):
        lines.append(f"{indent}## [Database] {body.get('title', '')}")
    elif t == "table_row":
        cells = [rich_text(c).replace("\n", " ") for c in body.get("cells", [])]
        lines.append(f"{indent}| " + " | ".join(cells) + " |")
    elif t == "equation":
        lines.append(f"{indent}$ {txt} $")
    elif t == "bookmark":
        lines.append(f"{indent}[Bookmark] {body.get('url', '')}")
    elif t == "link_preview":
        lines.append(f"{indent}[Link] {body.get('url', '')}")
    else:
        if txt:
            lines.append(f"{indent}{txt}")

    if b.get("has_children"):
        for child in fetch_children(b["id"], depth):
            lines.extend(block_to_md(child, depth + 1 if t in ("toggle", "bulleted_list_item", "numbered_list_item") else depth))
    return lines


def fetch_children(block_id, depth=0):
    out = []
    cursor = None
    while True:
        url = f"{BASE}/blocks/{block_id}/children?page_size=100"
        if cursor:
            url += f"&start_cursor={cursor}"
        d = get(url)
        out.extend(d.get("results", []))
        if not d.get("has_more"):
            break
        cursor = d.get("next_cursor")
        time.sleep(0.3)
    return out


def render(page_id):
    lines = []
    for b in fetch_children(page_id):
        lines.extend(block_to_md(b))
    return "\n".join(lines)


if __name__ == "__main__":
    for name, pid in PAGES.items():
        path = os.path.join(OUT, f"{name}.md")
        if os.path.exists(path):
            print(f"skip {name}")
            continue
        try:
            md = render(pid)
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"<!-- source: notion page {pid} -->\n\n{md}")
            print(f"ok {name} ({len(md)} chars)")
        except Exception as e:
            print(f"FAIL {name}: {e}")
        time.sleep(0.4)
