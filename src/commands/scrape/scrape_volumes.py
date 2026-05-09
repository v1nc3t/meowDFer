from __future__ import annotations

import re
import sys
import requests
import urllib.parse

from bs4 import BeautifulSoup, Tag

UA = "Mozilla/5.0 (manga-scraper; +https://example.org)"
WIKI = "https://en.wikipedia.org"

session = requests.Session()
session.headers.update({"User-Agent": UA})


def fetch(url: str) -> str:
    r = session.get(url, timeout=30)
    r.raise_for_status()
    return r.text


def api_get(params: dict) -> dict:
    params = {**params, "format": "json"}
    r = session.get(f"{WIKI}/w/api.php", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def validate_manga(name: str) -> str | None:
    data = api_get({
        "action": "query",
        "list": "search",
        "srsearch": f'"{name}" manga',
        "srlimit": 8,
    })

    hits = data.get("query", {}).get("search", [])

    if not hits:
        return None
    
    name_l = name.lower()
    ordered = sorted(hits, key=lambda h: 0 if name_l in h["title"].lower() else 1)
    
    for hit in ordered:
        title = hit["title"]
        if _is_manga_page(title):
            return title
    
    return None


def _is_manga_page(title: str) -> bool:
    data = api_get({
        "action": "query",
        "prop": "categories|extracts",
        "titles": title,
        "exintro": 1,
        "explaintext": 1,
        "cllimit": "max",
    })

    pages = data.get("query", {}).get("pages", [])
    if not pages:
        return False
        
    page = next(iter(pages.values()))
    cats = " ".join(c.get("title", "").lower() for c in page.get("categories", []))
    extract = page.get("extract", "").lower()

    return "manga" in cats or "manga" in extract[:800]


def find_chapters_page(name: str, manga_title: str | None = None) -> str | None:
    if manga_title:
        linked = _chapters_link_from_article(manga_title)
        if linked:
            return linked

    for cand in (
        f"List of {name} chapters",
        f"List of {name} manga chapters",
        f"List of {name} volumes",
        f"{name} chapters",
    ):
        t = _page_exists(cand)
        if t:
            return t

    data = api_get({
        "action": "query",
        "list": "search",
        "srsearch": f'intitle:"List of" intitle:"{name}" intitle:chapters',
        "srlimit": 5,
    })
    for hit in data.get("query", {}).get("search", []):
        title = hit["title"]
        low = title.lower()
        if low.startswith("list of") and ("chapter" in low or "volume" in low):
            return title
    return None


def _chapters_link_from_article(title: str) -> str | None:
    """Look for a link like 'List of <X> chapters' on the manga's own page."""
    data = api_get({
        "action": "query",
        "prop": "links",
        "titles": title,
        "pllimit": "max",
        "plnamespace": 0,
    })
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return None
    page = next(iter(pages.values()))
    for link in page.get("links", []):
        t = link.get("title", "")
        low = t.lower()
        if low.startswith("list of") and ("chapter" in low or "volume" in low):
            resolved = _page_exists(t)
            if resolved:
                return resolved
    return None


def _page_exists(title: str) -> str | None:
    data = api_get({
        "action": "query",
        "titles": title,
        "redirects": 1
    })
    
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return None
    page = next(iter(pages.values()))

    if "missing" not in page:
        return page["title"]
    
    return None


def extract_volumes(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    for stop_id in ("References", "Notes"):
        h = soup.find(id=stop_id)
        if h:
            anchor = h.parent if h.parent and h.parent.name in ("h1", "h2", "h3", "h4") else h
            for sib in list(anchor.find_all_next()):
                sib.decompose()
            anchor.decompose()
    
    for ref in soup.select(".references"):
        ref.decompose()
    
    volumes: list[dict] = []
    vol_headers = soup.find_all(id=re.compile(r"^vol\d+$"))

    for idx, th in enumerate(vol_headers):
        m = re.match(r"^vol(\d+)$", th.get("id", ""))
        if not m:
            continue
        
        vol_num = int(m.group(1))
        vol_title = f"Volume {vol_num}"

        # volume title: first <td> sibling after the <th>
        td = th.find_next("td")
        if td:
            italic = td.find("i")
            raw_title = _node_text(italic) if italic else _node_text(td)
            if not re.match(
                r'^(?:\d{1,2}\s+\w+\s+\d{4}|\w+\s+\d{1,2},?\s+\d{4}|'
                r'\d{4}-\d{2}-\d{2}|\d+|ISBN.*)$',
                raw_title.strip(),
            ):
                vol_title = raw_title
        
        # find chapter list - next <ol>/<ul> after this th
        # but stop before next vol header

        next_th = vol_headers[idx + 1] if idx + 1 < len(vol_headers) else None
        chapters: list[str] = []

        for lst in th.find_all_next(["ol", "ul"]):
            if next_th is not None and _comes_after(lst, next_th):
                break
            classes = " ".join(lst.get("class", [])).lower()
            if "references" in classes:
                continue
            for li in lst.find_all("li"):
                text = _node_text(li)
                text = re.sub(r'^\s*\d+(?:\s*[–-]\s*\d+)?\s*\.\s*', '', text)
                text = text.strip().strip('"').strip()
                if text:
                    chapters.append(text)

        volumes.append({
            "volume": vol_num,
            "title": vol_title,
            "chapters": chapters,
        })
    
    return volumes


        
def _node_text(node: Tag) -> str:
    clone = BeautifulSoup(str(node), "html.parser")
    
    for bad in clone.find_all(["sup", "style", "script"]):
        bad.decompose()
    
    for span in clone.find_all("span"):
        if span.parent is None:
            continue
        
        lang = (span.get("lang") or "").lower()
        style = (span.get("style") or "").lower()
        
        if lang.startswith("ja") or "font-weight: normal" in style:
            span.decompose()

    return _clean_text(clone.get_text(" "))


def _clean_text(s: str) -> str:
    s = re.sub(r"\[[^\]]*\]", "", s)  # strip [1], [note 2]
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _comes_after(a: Tag, b: Tag) -> bool:
    """True if `a` appears after `b` in document order."""
    for el in b.find_all_next():
        if el is a:
            return True
    return False


_RANGE_RE = re.compile(
    r'^\s*(?:(\d+)\s*[–-]\s*(\d+)\s*\.\s*)?"?\s*(.+?)\s*\((\d+)\s*[–-]\s*(\d+)\)\s*"?\s*$'
)

def expand_chapter(raw: str) -> list[str]:
    m = _RANGE_RE.match(raw)
    if not m:
        return [raw]
    base = m.group(3).strip().strip('"').strip()
    a, b = int(m.group(4)), int(m.group(5))
    if b < a or b - a > 30:
        return [raw]
    return [f'{base} ({i})' for i in range(a, b + 1)]


def write_output(manga: str, source_url: str, volumes: list[dict], path: str, verbose: bool = False):
    with open(path, "w", encoding="utf-8") as f:
        if verbose:
            f.write(f"Title: {manga}\n")
            f.write(f"Source: {source_url}\n\n")
        
        global_n = 0
        endpoints = []

        for v in volumes:
            count = sum(len(expand_chapter(ch)) for ch in v["chapters"])
        
            if count == 0:
                if verbose:
                    f.write(f"volume {v['volume']}: -\n")
                continue
            
            start = global_n + 1
            end = global_n + count
            global_n = end
            if verbose:
                if start == end:
                    f.write(f"volume {v['volume']}: {start}\n")
                else:
                    f.write(f"volume {v['volume']}: {start}-{end}\n")
            else:
                endpoints.append(str(end))
        
        if not verbose:
            f.write(", ".join(endpoints))


def run(name, dest_path, verbose=False, console=None):
    # validate if manga has wikipedia page 
    console.print(f"Validating '{name}' as a manga on Wikipedia...")
    title = validate_manga(name)
    if not title:
        console.print(f"Error '{name}' does not appear to be a valid manga on Wikipedia.\n"
                      f"No file was written. Manual lookup required.")
        return False
    console.print(f"Validated manga: {title}")
    
    # find chapters page of manga
    base = re.sub(r"\s*\(manga\)\s*$", "", title, flags=re.I)
    chapters_title = (
        find_chapters_page(base, manga_title=title)
        or find_chapters_page(name, manga_title=title)
        or _page_exists(title)
    )
    if not chapters_title:
        console.print("Error: could not find a chapters page on Wikipedia.\n"
                      "No file was written. Manual lookup required.")
        return False
    console.print(f"Chapters page: {chapters_title}")

    #clear
    url = f"{WIKI}/wiki/{urllib.parse.quote(chapters_title.replace(' ', '_'))}"
    html = fetch(url)
    volumes = extract_volumes(html)
    total_ch = sum(sum(len(expand_chapter(c)) for c in v['chapters']) for v in volumes)
    console.print(f"Parsed {len(volumes)} volume(s), {total_ch} chapter(s)")

    if not volumes or total_ch == 0:
        console.print(f"Error: no volumes/chapters could be parsed from {url}\n"
                      f"No file was written. Manual lookup required.")
        return False
    
    out = dest_path or f"{re.sub(r'[^A-Za-z0-9]+', '_', name).strip('_')}_chapters.txt"
    write_output(title, url, volumes, out, verbose)
    console.print(f"Wrote: {out}")
    return True
