#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fetch Medium images referenced in blog posts and store them under images/medium/.
- Scans blog/*/index.html for <img src> pointing to Medium CDN or external URLs
- Downloads and deduplicates by filename (or hash if collision)
- Optimizes JPEG/PNG (quality 85, progressive for JPEG)
- Rewrites HTML to use local /images/medium/<filename>
"""
import os
import re
import hashlib
import urllib.parse
from io import BytesIO

import requests
from PIL import Image

ROOT = os.path.dirname(__file__)
BLOG_DIR = os.path.join(ROOT, 'blog')
OUT_DIR = os.path.join(ROOT, 'images', 'medium')
SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'MediumImageFetcher/1.0'})
TIMEOUT = 15

IMG_RE = re.compile(r'<img[^>]+src=\"([^\"]+)\"', re.I)
EXTERNAL_RE = re.compile(r'^https?://', re.I)

os.makedirs(OUT_DIR, exist_ok=True)


def filename_from_url(url: str) -> str:
    parsed = urllib.parse.urlparse(url)
    name = os.path.basename(parsed.path) or 'image'
    if '.' not in name:
        # guess extension by query or default png
        ext = '.png'
        q = urllib.parse.parse_qs(parsed.query)
        if 'format' in q:
            ext = '.' + q['format'][0]
        name = name + ext
    return name


def unique_name(name: str, data: bytes) -> str:
    base, ext = os.path.splitext(name)
    path = os.path.join(OUT_DIR, name)
    if not os.path.exists(path):
        return name
    # if same content, reuse
    old = open(path, 'rb').read()
    if old == data:
        return name
    digest = hashlib.sha1(data).hexdigest()[:8]
    return f"{base}-{digest}{ext}"


def download_image(url: str) -> bytes | None:
    try:
        r = SESSION.get(url, timeout=TIMEOUT, allow_redirects=True)
        if r.status_code >= 400:
            return None
        return r.content
    except Exception:
        return None


def optimize_and_save(data: bytes, out_path: str):
    try:
        img = Image.open(BytesIO(data))
        img_format = (img.format or 'PNG').upper()
        params = {}
        if img_format in ('JPEG', 'JPG'):
            params = dict(quality=85, optimize=True, progressive=True)
            img = img.convert('RGB')
        elif img_format == 'PNG':
            params = dict(optimize=True)
        img.save(out_path, **params)
    except Exception:
        with open(out_path, 'wb') as f:
            f.write(data)


def process_html(html_path: str) -> int:
    s = open(html_path, 'r', encoding='utf-8', errors='ignore').read()
    changed = 0
    def repl(m):
        nonlocal changed
        src = m.group(1)
        if not EXTERNAL_RE.match(src):
            return m.group(0)
        data = download_image(src)
        if not data:
            return m.group(0)
        fname = unique_name(filename_from_url(src), data)
        out_path = os.path.join(OUT_DIR, fname)
        if not os.path.exists(out_path):
            optimize_and_save(data, out_path)
        changed += 1
        return m.group(0).replace(src, f"/images/medium/{fname}")

    ns = IMG_RE.sub(repl, s)
    if ns != s:
        open(html_path, 'w', encoding='utf-8').write(ns)
    return changed


def main():
    total = 0
    for dirpath, _, files in os.walk(BLOG_DIR):
        for f in files:
            if f != 'index.html':
                continue
            p = os.path.join(dirpath, f)
            total += process_html(p)
    print(f"Replaced images: {total}")

if __name__ == '__main__':
    main()
