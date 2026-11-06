# Hush Search

**A private search engine and launcher that runs entirely in the browser. No server, no tracking, no query logs.**

**Live demo:** https://YOUR-USERNAME.github.io/hush-search/

## For recruiters: 60-second summary
**What I built:** a working private search engine. It indexes documents with an inverted index, ranks them with the BM25 algorithm used by Elasticsearch and Lucene, and shows highlighted snippets. A smart address bar also opens websites, app downloads and searches on Google, DuckDuckGo, YouTube and GitHub without sending data to any server of mine.

**Problem:** mainstream search engines log queries and build profiles of users. This project shows a transparent alternative where I can point to the exact code that handles every query.

**Skills demonstrated**
| Area | Evidence in this repo |
|---|---|
| Information retrieval | Tokenizer, stop words, stemmer, inverted index, BM25 (`index.html`, `python-version/private_search.py`) |
| JavaScript | Maps, closures, DOM rendering, `localStorage`, file import/export, no frameworks |
| Python | Polite web crawler with `robots.txt` support, argparse CLI (`crawler/crawler.py`) |
| Privacy by design | No backend, no analytics, `noopener,noreferrer` links, queries never stored |
| UI and accessibility | Responsive layout, dark mode, visible keyboard focus, reduced-motion support |
| Delivery | Deployed free on GitHub Pages, documented architecture and test checklist |

**Try it in 30 seconds**
1. Open the live demo. With **My private index** selected, search `bm25 ranking` to see ranked results with highlights.
2. Type `youtube` or `instagram.com` to open a site, `download python` for the download page, or `!gh react` to search GitHub.
3. Open **Add your own documents** to add text, then search it.

**Key engineering decisions**
- **BM25 over plain TF-IDF:** it saturates term frequency and normalises document length, which gives better rankings.
- **Static, client-side design:** the privacy claim is easy to verify because there is no server.
- **Web results open in a new tab:** Google, YouTube and WhatsApp block embedding with `X-Frame-Options`, so a new tab is the only reliable approach.
- **Separate Python crawler:** browsers cannot crawl other sites because of CORS.

Where to read the code: `tokens()`, `build()` and `search()` in `index.html` (the engine), `direct()` and `go()` (the address bar), and `docs/DOCUMENTATION.md` (full architecture and the BM25 formula).

## What it does
- **Smart address bar.** Type a website (`youtube`, `instagram.com`), an app request (`download python`, `download spotify`), a shortcut (`!yt lofi music`, `!gh react`, `!so cors error`), or any search.
- **Engine picker.** Google, DuckDuckGo, Bing, Brave, Stack Overflow, GitHub, MDN, npm, YouTube. Results open in a new tab with no referrer sent.
- **Launcher tiles.** One tap to WhatsApp, Instagram, YouTube, Gmail, Maps, Play Store and more.
- **Private index.** Your own documents, searched with an inverted index and BM25 ranking, with highlighted snippets. Add, import and export documents as JSON.
- **Python crawler.** Builds an index file from any website while respecting `robots.txt`.

## Quick start
Open `index.html` in a browser. There is no build step and nothing to install.

## Project structure
```
hush-search/
├── index.html            the whole web app (HTML + CSS + JavaScript)
├── crawler/
│   ├── crawler.py        polite same-domain crawler, outputs hush-index.json
│   └── requirements.txt
├── python-version/
│   └── private_search.py the same engine in about 70 lines of plain Python
├── docs/
│   └── DOCUMENTATION.md  architecture, algorithms, testing, report outline
├── LICENSE
└── README.md
```

## Deploy on GitHub Pages
1. Create a public repository named `hush-search` and upload every file in this folder.
2. Settings → Pages → Source: Deploy from a branch → `main` / `(root)` → Save.
3. After a minute the site is live at `https://YOUR-USERNAME.github.io/hush-search/`.
4. Replace `YOUR-USERNAME` in `index.html` (footer) and in this README.

## Use the crawler
```bash
cd crawler
pip install -r requirements.txt
python crawler.py https://example.com --max-pages 30 --delay 1.0
```
Then open the site, expand **Add your own documents**, click **Import JSON** and choose `hush-index.json`. Switch the engine to **My private index** and search.

## Privacy
- No backend, analytics or cookies.
- Queries are never stored. Only your own documents and your last engine choice are saved in your browser's localStorage.
- Outgoing links use `noopener,noreferrer`, so the destination site does not learn that you came from Hush Search.
- Web searches still reach the engine you choose (for example Google). Pick DuckDuckGo or Brave if you want a more private engine.

## Limitations
- Google, YouTube, WhatsApp and Instagram refuse to load inside other pages, so they open in a new tab. A true embedded browser would need an Electron app or a browser extension.
- A browser cannot crawl other sites (CORS), which is why the crawler is a separate Python script.
- The stemmer is a small rule-based one, not a full Porter stemmer.

## Future work
Electron desktop version, semantic search with embeddings, encrypted index, PageRank, more launcher tiles and custom shortcuts.

## License
MIT. See `LICENSE`.
