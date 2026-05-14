from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse, unquote

import requests
from bs4 import BeautifulSoup, Tag
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ---------------------------------------------------------------------------
# HTTP session
# ---------------------------------------------------------------------------

UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)
DEFAULT_HEADERS = {
    "User-Agent": UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/json;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}
TOTAL_TIMEOUT = (10, 25)


def _make_session() -> requests.Session:
    s = requests.Session()
    s.headers.update(DEFAULT_HEADERS)
    retry = Retry(
        total=4, connect=3, read=3, backoff_factor=0.6,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=frozenset(["GET", "HEAD"]),
        respect_retry_after_header=True, raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


session = _make_session()


def fetch(url: str) -> str:
    r = session.get(url, timeout=TOTAL_TIMEOUT)
    r.raise_for_status()
    return r.text


def api_get(params: dict, base: str) -> dict:
    params = {**params, "format": "json"}
    r = session.get(f"{base}/api.php", params=params, timeout=TOTAL_TIMEOUT)
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Volume:
    volume: int
    title: str
    chapters: list[str] = field(default_factory=list)

    def chapter_count(self) -> int:
        return sum(len(expand_chapter(c)) for c in self.chapters)

    def expanded_chapters(self) -> list[str]:
        out: list[str] = []
        for c in self.chapters:
            out.extend(expand_chapter(c))
        return out


@dataclass
class ScrapeResult:
    volumes: tuple[Volume, ...]
    title: Optional[str]
    source_url: Optional[str]
    strategy: str = "unknown"

    @property
    def total_chapters(self) -> int:
        return sum(v.chapter_count() for v in self.volumes)


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _clean_text(s: str) -> str:
    s = re.sub(r"\[[^\]]*\]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


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


# ---------------------------------------------------------------------------
# URL routing
# ---------------------------------------------------------------------------

def detect_source(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if "wikipedia.org" in host:
        return "wikipedia"
    if "fandom.com" in host or "wikia.com" in host or "wikia.org" in host:
        return "fandom"
    raise ValueError(f"Unsupported source for URL: {url}")


def _fandom_base_and_page(url: str) -> tuple[str, str]:
    """From https://onepiece.fandom.com/wiki/Chapters_and_Volumes
    -> ('https://onepiece.fandom.com', 'Chapters_and_Volumes')."""
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path
    m = re.match(r"^/wiki/(.+)$", path)
    page = unquote(m.group(1)) if m else ""
    return base, page.replace("_", " ")


# ---------------------------------------------------------------------------
# FANDOM scraper — parse the table-of-volumes hub page at the given URL.
# Mirrors the original HubPage strategy but driven by the URL the user supplied.
# ---------------------------------------------------------------------------

# Strip Japanese furigana parentheticals like "( 緑 谷 , Midoriya ? )"
_FURIGANA_RE = re.compile(
    r'\s*\(\s*[^)]*?[\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef][^)]*?\)\s*'
)

# Patterns to split a cell-of-chapters into individual chapter entries.
# Each pattern's split() yields [pre, num1, title1, num2, title2, ...].
_CHAPTER_SPLIT_PATTERNS = [
    # "Chapter NNN: Title" / "Chapter NNN | Title" / "Chapter NNN Title" / "Chapter NNN"
    re.compile(r'(?:^|\s)Chapter\s+(\d+(?:-\d+)?)\s*(?:[:|.\-–]\s*|\s+(?=\S)|$)', re.I),
    # "Round NNN: Title" (Hajime no Ippo style)
    re.compile(r'(?:^|\s)(?:Round|Episode|Ep\.?)\s+(\d+(?:-\d+)?)\s*[:|.\-–]\s*', re.I),
    # "001. Title" / "001: Title" / "0-01. \"Title\"" / "-108. Title"
    re.compile(r'(?:^|\s)(-?\d{1,4}(?:-\d+)?)\s*[.:]\s+'),
]


def _extract_chapters_from_cell(cell) -> list[str]:
    list_el = cell.find(["ol", "ul"])
    if list_el:
        items = []
        for li in list_el.find_all("li", recursive=False):
            t = li.get_text(" ", strip=True)
            t = re.sub(r'\s+', ' ', t).strip().strip('"').strip()
            if t:
                items.append(t)
        if items:
            return items

    text = cell.get_text(" ", strip=True)
    # Strip leading labels: "Chapters list:", "List of Chapters:",
    # "Volume N Chapters:", "Chapters:", etc.
    text = re.sub(r'^\s*(?:list\s+of\s+)?chapters?(?:\s*list)?\s*:?\s*',
                  '', text, flags=re.I)
    text = re.sub(r'^\s*Volume\s*\d+\s*Chapters?\s*:?\s*', '', text, flags=re.I)
    # Remove Japanese furigana parentheticals to keep titles clean and to
    # prevent stray digits inside parens from confusing splits.
    clean = _FURIGANA_RE.sub(' ', text)

    best: list[str] = []
    for pat in _CHAPTER_SPLIT_PATTERNS:
        parts = pat.split(' ' + clean)
        if len(parts) < 3:
            continue
        chapters: list[str] = []
        for i in range(1, len(parts) - 1, 2):
            num = parts[i]
            title = parts[i + 1]
            # Cut off trailing junk after a double-space gap or pipe.
            title = title.strip().strip('|').strip().strip('"').strip()
            title = re.sub(r'\s+', ' ', title)
            # Drop trailing parenthetical fragments without titles.
            if not title:
                title = f'Chapter {num}'
            chapters.append(title)
        if len(chapters) > len(best):
            best = chapters
    return best


def scrape_fandom(url: str, console) -> ScrapeResult:
    console.print(f"[Fandom] Fetching: {url}")
    wiki_base, page = _fandom_base_and_page(url)

    # Prefer the parsed HTML via api.php (cleaner DOM, follows redirects).
    html = ""
    fetch_page = page
    for _ in range(3):  # follow soft-redirects (Template:Redirect pages)
        if not fetch_page:
            break
        try:
            data = api_get({"action": "parse", "page": fetch_page,
                            "prop": "text", "redirects": 1}, base=wiki_base)
            html = (data.get("parse", {}).get("text", {}) or {}).get("*", "")
        except Exception as e:
            console.print(f"[Fandom] api.php failed ({e}); falling back to raw HTML.")
            html = ""
            break
        # Detect a soft redirect: a near-empty page containing only a
        # redirectMsg block. Re-fetch the link inside.
        probe = BeautifulSoup(html, "html.parser")
        rmsg = probe.select_one("div.redirectMsg")
        if rmsg and not probe.find("table"):
            link = rmsg.find("a", href=True)
            if link:
                from urllib.parse import unquote
                href = link["href"]
                # /wiki/Foo/Bar → "Foo/Bar"
                m = re.match(r'^/wiki/(.+)$', href)
                if m:
                    fetch_page = unquote(m.group(1))
                    console.print(f"[Fandom] Following soft redirect → {fetch_page}")
                    continue
        break
    if not html:
        html = fetch(url)

    soup = BeautifulSoup(html, "html.parser")
    volumes: list[Volume] = []
    seen_nums: set = set()


    # Volume header recognizer: bare number ("3") or "Volume 3".
    vol_hdr_re = re.compile(r'^\s*(?:Volume\s+)?(\d{1,3})\s*$', re.I)

    # Pass 1 (generic walker): for every table, walk rows in order.
    # When a row's first cell is a volume header, set current_vol.
    # On any subsequent row (or remaining cells of the same row), try to
    # extract a chapter list from any cell. The first cell that yields >= 1
    # chapter is attached to the pending volume.
    for tbl in soup.find_all("table"):
        current_vol: Optional[int] = None
        for row in tbl.find_all("tr"):
            cells = row.find_all(["th", "td"])
            if not cells:
                continue
            first_txt = cells[0].get_text(" ", strip=True)
            m = vol_hdr_re.match(first_txt)
            if m:
                current_vol = int(m.group(1))
                # Also try chapter extraction from remaining cells in same row
                # (handles compact navbox-style "Volume 1 || ch1 ch2 ..." rows
                # where the header and chapter list share a row).
                if current_vol not in seen_nums:
                    for c in cells[1:]:
                        chs = _extract_chapters_from_cell(c)
                        if chs:
                            seen_nums.add(current_vol)
                            volumes.append(Volume(volume=current_vol,
                                                  title=f"Volume {current_vol}",
                                                  chapters=chs))
                            current_vol = None
                            break
                continue
            if current_vol is None or current_vol in seen_nums:
                continue
            for c in cells:
                chs = _extract_chapters_from_cell(c)
                if chs:
                    seen_nums.add(current_vol)
                    volumes.append(Volume(volume=current_vol,
                                          title=f"Volume {current_vol}",
                                          chapters=chs))
                    current_vol = None
                    break

    # Pass 2 (fallback): scan any cell that looks like a chapter list AND
    # contains an inline volume marker. Useful for tables where the volume
    # number is not in a separate header row (e.g. "Volume N Chapters: ...").
    if not volumes:
        vol_inline_re = re.compile(r'Volume\s+(\d{1,3})\b', re.I)
        for tbl in soup.find_all("table"):
            for c in tbl.find_all(["td", "th"]):
                txt = c.get_text(" ", strip=True)
                vm = vol_inline_re.search(txt[:80])
                if not vm:
                    continue
                chs = _extract_chapters_from_cell(c)
                if not chs:
                    continue
                vol_num = int(vm.group(1))
                if vol_num in seen_nums:
                    continue
                seen_nums.add(vol_num)
                volumes.append(Volume(volume=vol_num,
                                      title=f"Volume {vol_num}",
                                      chapters=chs))


    volumes.sort(key=lambda v: v.volume)
    title = page or wiki_base
    return ScrapeResult(tuple(volumes), title, url, "Fandom")


# ---------------------------------------------------------------------------
# WIKIPEDIA scraper — "List of X chapters" pages.
#
# Common layout: one or more <table class="wikitable"> where each volume is
# represented by a row with the volume number in the first column, followed
# by a row whose single cell contains an <ol> (or <ul>) of chapter titles.
# ---------------------------------------------------------------------------

def _is_volume_number_cell(text: str) -> Optional[int]:
    m = re.match(r'^\s*(\d{1,3})\s*$', text)
    return int(m.group(1)) if m else None


def _chapters_from_wp_list(list_el: Tag) -> list[str]:
    out: list[str] = []
    for li in list_el.find_all("li", recursive=False):
        t = _node_text(li)
        t = re.sub(r'^\s*\d+(?:\s*[–-]\s*\d+)?\s*[.:)-]\s*', '', t)
        t = t.strip().strip('"').strip()
        if t:
            out.append(t)
    return out


def scrape_wikipedia(url: str, console) -> ScrapeResult:
    console.print(f"[Wikipedia] Fetching: {url}")
    html = fetch(url)
    soup = BeautifulSoup(html, "html.parser")

    # Strip references and edit links to keep titles clean.
    for sel in (".reference", ".mw-editsection", "sup.reference"):
        for el in soup.select(sel):
            el.decompose()

    page_title_el = soup.find("h1", id="firstHeading")
    page_title = page_title_el.get_text(" ", strip=True) if page_title_el else url

    volumes: list[Volume] = []
    seen_nums: set = set()

    for tbl in soup.select("table.wikitable"):
        rows = tbl.find_all("tr", recursive=False)
        if not rows:
            tbody = tbl.find("tbody")
            if tbody:
                rows = tbody.find_all("tr", recursive=False)
        if not rows:
            continue

        # Walk rows: a "header" row carries the volume number; the next row
        # (or a row inside the same group) carries the chapter list.
        i = 0
        while i < len(rows):
            row = rows[i]
            cells = row.find_all(["th", "td"], recursive=False)
            vol_num = None
            for c in cells[:2]:
                vol_num = _is_volume_number_cell(c.get_text(" ", strip=True))
                if vol_num is not None:
                    break
            if vol_num is None or vol_num in seen_nums:
                i += 1
                continue

            # Look for an embedded chapter list in this row, then in the next
            # row (the typical "expanded details" row).
            chapters: list[str] = []
            for probe in (row, rows[i + 1] if i + 1 < len(rows) else None):
                if probe is None:
                    continue
                list_el = probe.find(["ol", "ul"])
                if list_el:
                    chapters = _chapters_from_wp_list(list_el)
                    if chapters:
                        break

            if chapters:
                seen_nums.add(vol_num)
                volumes.append(Volume(volume=vol_num,
                                      title=f"Volume {vol_num}",
                                      chapters=chapters))
                i += 2
            else:
                i += 1

    volumes.sort(key=lambda v: v.volume)
    return ScrapeResult(tuple(volumes), page_title, url, "Wikipedia")


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def write_output(manga: str, source_url: str, volumes, path: str,
                 verbose: bool = False):
    has_empty_tail = any(v.chapter_count() == 0 for v in volumes)
    with open(path, "w", encoding="utf-8") as f:
        if verbose:
            f.write(f"Title: {manga}\n")
            f.write(f"Source: {source_url}\n\n")
        global_n = 0
        endpoints = []
        for v in volumes:
            count = v.chapter_count()
            if count == 0:
                if verbose:
                    f.write(f"volume {v.volume}: -\n")
                continue
            start = global_n + 1
            end = global_n + count
            global_n = end
            if verbose:
                if start == end:
                    f.write(f"volume {v.volume}: {start}\n")
                else:
                    f.write(f"volume {v.volume}: {start}-{end}\n")
            else:
                endpoints.append(str(end))
        if not verbose:
            f.write(", ".join(endpoints))
        elif has_empty_tail:
            f.write(
                "Note: one or more volumes have no chapter list on the source "
                "page (typical for unreleased / very recent volumes). Manual "
                "checkup recommended for those volumes.\n"
            )


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def run(url: str, dest_path: Optional[str] = None,
        verbose: bool = False, console=None) -> bool:
    source = detect_source(url)
    if source == "wikipedia":
        result = scrape_wikipedia(url, console)
    else:
        result = scrape_fandom(url, console)

    console.print(f"Source: {result.strategy}  "
                  f"Volumes: {len(result.volumes)}  "
                  f"Chapters: {result.total_chapters}")

    if not result.volumes:
        console.print("Error: no volumes parsed from the page. No file written.")
        return False

    if any(v.chapter_count() == 0 for v in result.volumes):
        console.print(
            "WARNING: some volumes have no chapter list on the source page."
        )

    base = re.sub(r'[^A-Za-z0-9]+', '_',
                  result.title or urlparse(url).path or "manga").strip('_') or "manga"
    out = dest_path or f"{base}_chapters.txt"
    write_output(result.title or url, result.source_url or url,
                 list(result.volumes), out, verbose)
    console.print(f"Wrote: {out}")
    return True
