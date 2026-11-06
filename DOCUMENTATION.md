# Hush Search: Technical Documentation

## 0. Summary for reviewers
Hush Search is a private search engine: it builds an inverted index of documents, ranks results with BM25 and shows highlighted snippets, all inside the browser. A smart address bar adds one-step access to websites, downloads and other search engines. A Python crawler produces indexes from real websites, and `python-version/private_search.py` shows the same engine in plain Python.

## 1. Problem
Mainstream search engines log queries, IP addresses and clicks to build advertising profiles. Hush Search is a small, transparent alternative: a launcher that sends no data to any server of its own, plus a private search engine for personal documents.

## 2. Objectives
1. Open any website, app page or search from a single box.
2. Search a private document collection with a real ranking algorithm.
3. Collect no user data.
4. Deploy for free as a static site.

## 3. Architecture
```
                 ┌──────────────────────────────┐
  user input ──▶ │ Smart address bar  direct()  │
                 └───────┬───────────┬──────────┘
        URL / site /     │           │ plain text
        download / !bang │           ▼
                         │   ┌───────────────┐   engine = web
                         │   │ Engine picker │ ───────────────▶ new tab (Google, DDG...)
                         │   └──────┬────────┘
                         ▼          │ engine = My private index
                   new browser tab  ▼
                          ┌───────────────────────┐
  crawler.py ─JSON─▶      │ tokenize → stop words │
  manual add / import ──▶ │ → stem → inverted idx │
                          │ → BM25 → snippets     │
                          └──────────┬────────────┘
                                     ▼
                              ranked results (DOM)
```

## 4. Components (all in `index.html`)

| Part | Function | Purpose |
|---|---|---|
| Tokenizer | `tokens(text)` | lowercase, split into words, remove stop words, stem |
| Stemmer | `stem(word)` | strips common suffixes (ing, ed, es, s, ly) |
| Indexer | `build()` | builds a `Map`: term → list of `[docId, termFrequency]` |
| Ranker | `search(q)` | scores documents with BM25 |
| Snippets | `snippet()`, `hl()` | picks the best sentence and highlights matches |
| Address bar | `direct(t)` | decides whether input is a URL, site name, download request or `!bang` |
| Dispatcher | `go(term)` | opens a new tab or runs the local search |
| Storage | `save()`, `load()` | keeps documents in `localStorage` |

### 4.1 Inverted index
Each unique term points to the documents that contain it. A query looks up only its own terms instead of scanning every document. Titles are indexed twice, so title matches rank higher.

### 4.2 BM25 ranking
For each query term `t` and document `d`:

```
idf(t)      = ln(1 + (N - n_t + 0.5) / (n_t + 0.5))
score(d, t) = idf(t) * f * (k1 + 1) / (f + k1 * (1 - b + b * |d| / avgdl))
score(d)    = sum of score(d, t) over query terms
```
`N` documents in total, `n_t` documents containing `t`, `f` frequency of `t` in `d`, `|d|` document length, `avgdl` average length. Defaults: `k1 = 1.5`, `b = 0.75`. Repeating a word has diminishing returns, and long documents are normalised.

### 4.3 Smart address bar rules (checked in order)
1. Starts with `http://` or `https://`: open as is.
2. Looks like a domain (`instagram.com`): open `https://` + input. Names such as `node.js` are excluded.
3. Matches a known site name (`whatsapp`, `youtube`, `gmail`...): open that site.
4. `download <name>` or `install <name>`: open the official download page if known (Python, VS Code, Node, Git, Chrome, Docker), otherwise a Play Store search.
5. `!yt query`, `!gh query`, `!so query`, `!g`, `!ddg`, `!b`, `!mdn`, `!npm`: search that site directly.
6. Otherwise: use the selected engine, or the private index.

To add a site, add one line to `SITES`. To add a download, add one line to `DL`.

## 5. Data format
The index is a JSON array. Both the importer and the crawler use it:
```json
[{ "title": "Page title", "url": "https://example.com/page", "text": "Plain text of the page" }]
```

## 6. Crawler (`crawler/crawler.py`)
Breadth-first crawl from a seed URL. It stays on one domain, reads `robots.txt` first, skips non-HTML responses, removes scripts, styles and navigation, waits `--delay` seconds between requests and truncates each page to 5000 characters. Use it only on sites you are allowed to crawl.

## 7. Privacy model
- No server of our own, so there is nothing to log.
- No analytics, cookies or third-party scripts. The only external request is the Google Fonts stylesheet for the heading typeface. Remove that `<link>` for a fully offline page.
- `noopener,noreferrer` on every outgoing link.
- Stored locally: document list and last engine choice. Clear them with **Reset to samples** or by clearing site data.

## 8. Testing checklist
| Input | Engine | Expected result |
|---|---|---|
| `youtube` | any | YouTube opens in a new tab |
| `instagram.com` | any | Instagram opens |
| `download python` | any | python.org downloads page |
| `download spotify` | any | Play Store search for spotify |
| `!yt lofi music` | any | YouTube search results |
| `full stack roadmap` | Google | Google results in a new tab |
| `inverted index` | My private index | Matching documents, highlighted |
| Add a document, then search its words | My private index | New document appears |
| Export then Import | My private index | Same document count |
| Import a non-JSON file | any | Clear error message, nothing lost |
| Resize to 375 px wide | any | No horizontal scroll |

## 9. Limitations and future work
See README. Planned: Electron desktop app (embeds real pages), semantic search with sentence embeddings (FAISS or Chroma), encrypted index (Web Crypto API), PageRank, user-defined shortcuts.

## 10. Report and presentation outline
1. Introduction and problem statement
2. Related work (Google, DuckDuckGo, SearXNG)
3. Architecture diagram (section 3)
4. Algorithms: inverted index, BM25, stemming
5. Implementation and tech stack: HTML, CSS, JavaScript, Python, GitHub Pages
6. Screenshots and test results (section 8)
7. Privacy analysis
8. Limitations and future work
9. Conclusion

## 11. Sample LinkedIn post
> I built Hush Search, a private search engine and launcher that runs entirely in the browser. It has an inverted index with BM25 ranking, a smart address bar for websites and downloads, and a Python crawler. No server, no tracking. Live demo and source: https://YOUR-USERNAME.github.io/hush-search/ #WebDevelopment #JavaScript #Python #Privacy #OpenSource
