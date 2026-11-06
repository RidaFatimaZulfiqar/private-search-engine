#!/usr/bin/env python3
"""Hush Search crawler.

Crawls one website (same domain only), respects robots.txt, waits between
requests, and writes hush-index.json. Import that file in the Hush Search
page with Add your own documents -> Import JSON.

Usage:
    pip install -r requirements.txt
    python crawler.py https://example.com --max-pages 30 --delay 1.0
"""
import argparse
import json
import re
import time
from collections import deque
from urllib.parse import urljoin, urldefrag, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

UA = "HushSearchBot/1.0 (student project)"


def load_robots(seed):
    rp = RobotFileParser()
    rp.set_url(urljoin(seed, "/robots.txt"))
    try:
        rp.read()
    except Exception:
        rp.allow_all = True  # robots.txt unreachable: treat as no rules
    return rp


def extract(html, url):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "noscript", "svg"]):
        tag.decompose()
    title = soup.title.get_text(strip=True) if soup.title else url
    text = re.sub(r"\s+", " ", soup.get_text(" ")).strip()
    return soup, title or url, text


def crawl(seed, max_pages=30, delay=1.0):
    host = urlparse(seed).netloc
    robots = load_robots(seed)
    queue, seen, docs = deque([seed]), {seed}, []
    while queue and len(docs) < max_pages:
        url = queue.popleft()
        if not robots.can_fetch(UA, url):
            print("blocked by robots.txt:", url)
            continue
        try:
            r = requests.get(url, headers={"User-Agent": UA}, timeout=10)
        except requests.RequestException as e:
            print("error:", url, e)
            continue
        if r.status_code != 200 or "text/html" not in r.headers.get("Content-Type", ""):
            continue
        soup, title, text = extract(r.text, url)
        if len(text) > 50:
            docs.append({"title": title[:150], "url": url, "text": text[:5000]})
            print(f"[{len(docs)}/{max_pages}] {url}")
        for a in soup.find_all("a", href=True):
            link = urldefrag(urljoin(url, a["href"]))[0]
            if link.startswith("http") and urlparse(link).netloc == host and link not in seen:
                seen.add(link)
                queue.append(link)
        time.sleep(delay)
    return docs


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Crawl a site into hush-index.json")
    ap.add_argument("seed", help="start URL, e.g. https://example.com")
    ap.add_argument("--max-pages", type=int, default=30)
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests")
    ap.add_argument("--out", default="hush-index.json")
    args = ap.parse_args()
    result = crawl(args.seed, args.max_pages, args.delay)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(result)} documents to {args.out}")
