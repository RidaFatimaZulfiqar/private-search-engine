"""A private search engine in one file. No libraries, no internet, no logs.

Step 1  Collect   read every .txt / .md file in a folder
Step 2  Clean     lowercase, split into words, drop stop words, stem
Step 3  Index     inverted index: word -> {doc_id: count}
Step 4  Rank      BM25 score for each matching document
Step 5  Show      title, score and a snippet

Run:  python private_search.py ./my_notes
"""
import math, os, re, sys
from collections import defaultdict

STOP = set("a an and are as at be but by for from has have how i if in is it of on or that the to was we what when where which who why with you".split())

def stem(w):
    for suffix in ("ing", "ed", "es", "s"):
        if len(w) > len(suffix) + 3 and w.endswith(suffix):
            return w[: -len(suffix)]
    return w

def tokens(text):
    return [stem(w) for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]

class Engine:
    def __init__(self, folder):
        self.docs, self.index, self.lengths = [], defaultdict(dict), []
        for name in sorted(os.listdir(folder)):
            if name.endswith((".txt", ".md")):
                with open(os.path.join(folder, name), encoding="utf-8") as f:
                    self.add(name, f.read())
        self.avg = sum(self.lengths) / max(len(self.lengths), 1)

    def add(self, title, text):
        doc_id = len(self.docs)
        self.docs.append((title, text))
        words = tokens(title + " " + text)
        self.lengths.append(len(words))
        for w in words:
            self.index[w][doc_id] = self.index[w].get(doc_id, 0) + 1

    def search(self, query, k1=1.5, b=0.75):
        n, scores = len(self.docs), defaultdict(float)
        for term in set(tokens(query)):
            postings = self.index.get(term, {})
            idf = math.log(1 + (n - len(postings) + 0.5) / (len(postings) + 0.5))
            for doc_id, f in postings.items():
                norm = f + k1 * (1 - b + b * self.lengths[doc_id] / self.avg)
                scores[doc_id] += idf * f * (k1 + 1) / norm
        return sorted(scores.items(), key=lambda x: -x[1])

    def snippet(self, doc_id, query):
        wanted = set(tokens(query))
        sentences = re.split(r"(?<=[.!?])\s+", self.docs[doc_id][1])
        best = max(sentences, key=lambda s: len(wanted & set(tokens(s))))
        return best[:200]

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "."
    engine = Engine(folder)
    print(f"Indexed {len(engine.docs)} documents, {len(engine.index)} unique terms.")
    while True:
        q = input("\nsearch> ").strip()
        if q in ("", "quit", "exit"):
            break
        results = engine.search(q)[:5]
        if not results:
            print("No matches.")
        for doc_id, score in results:
            print(f"\n{engine.docs[doc_id][0]}  (score {score:.2f})\n  {engine.snippet(doc_id, q)}")
