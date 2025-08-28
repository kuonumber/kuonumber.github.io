#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple local link checker for the static site.
- Crawls from the base URL (default http://localhost:8000)
- Follows internal links only
- Checks anchors and key assets (img/link/script)
- Reports non-200 responses and exceptions
"""
import sys
import re
import time
import urllib.parse
from collections import deque

import requests
from bs4 import BeautifulSoup

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
TIMEOUT = 8
HEADERS = {"User-Agent": "LocalLinkChecker/1.0"}

SKIP_SCHEMES = ("mailto:", "tel:", "javascript:", "data:")
EXTERNAL_RE = re.compile(r"^https?://", re.I)


def is_internal(url: str) -> bool:
    if not url:
        return False
    if url.startswith(SKIP_SCHEMES):
        return False
    if EXTERNAL_RE.match(url):
        return urllib.parse.urlparse(url).netloc == urllib.parse.urlparse(BASE_URL).netloc
    return True


def absolutize(url: str, base: str) -> str:
    return urllib.parse.urljoin(base, url)


def fetch(url: str):
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        return r
    except Exception as e:
        return e


def extract_links(html: str, page_url: str):
    soup = BeautifulSoup(html, "html.parser")
    anchors = [a.get("href") for a in soup.find_all("a")]
    assets = []
    for tag, attr in (("img", "src"), ("script", "src"), ("link", "href")):
        for t in soup.find_all(tag):
            assets.append(t.get(attr))
    links = [absolutize(h, page_url) for h in anchors if is_internal(h)]
    assets = [absolutize(s, page_url) for s in assets if is_internal(s)]
    return links, assets


def main():
    queue = deque([BASE_URL])
    visited_pages = set()
    bad_urls = []
    checked_assets = set()

    print(f"Crawling from {BASE_URL} ...")
    while queue:
        url = queue.popleft()
        if url in visited_pages:
            continue
        visited_pages.add(url)
        res = fetch(url)
        if isinstance(res, Exception):
            bad_urls.append((url, f"EXC: {res}"))
            continue
        status = res.status_code
        if status >= 400:
            bad_urls.append((url, status))
            continue
        links, assets = extract_links(res.text, url)
        for a in assets:
            if a in checked_assets:
                continue
            checked_assets.add(a)
            r = fetch(a)
            if isinstance(r, Exception) or getattr(r, "status_code", 599) >= 400:
                bad_urls.append((a, getattr(r, "status_code", f"EXC: {r}")))
        for l in links:
            if l not in visited_pages and l.startswith(BASE_URL):
                queue.append(l)
        # be gentle
        time.sleep(0.02)

    print("\nChecked pages:", len(visited_pages))
    print("Checked assets:", len(checked_assets))
    if bad_urls:
        print("\nErrors found:")
        for u, s in bad_urls:
            print(f"- {s} -> {u}")
        sys.exit(1)
    else:
        print("\nNo errors found (2xx/3xx only). ✅")


if __name__ == "__main__":
    main()
