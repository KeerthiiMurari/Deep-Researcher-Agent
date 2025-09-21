# app.py
import os
import re
from collections import Counter
from math import sqrt

def clean(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()

def tokenize(text):
    return clean(text).split()

def cosine_score(q, t):
    q_words = tokenize(q)
    t_words = tokenize(t)
    q_vec = Counter(q_words)
    t_vec = Counter(t_words)

    common = set(q_vec) & set(t_vec)
    dot = sum(q_vec[w] * t_vec[w] for w in common)

    q_mag = sqrt(sum(v ** 2 for v in q_vec.values()))
    t_mag = sqrt(sum(v ** 2 for v in t_vec.values()))
    return dot / (q_mag * t_mag + 1e-6)

def read_chunks(file_path, chunk_size=80):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        words = f.read().split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def main():
    print("🔎 Simple Researcher (No libraries needed!)\n")
    query = input("Enter your research question: ").strip()

    data_dir = "data"
    results = []

    for fname in os.listdir(data_dir):
        if fname.endswith(".txt"):
            path = os.path.join(data_dir, fname)
            chunks = read_chunks(path)
            for i, chunk in enumerate(chunks):
                score = cosine_score(query, chunk)
                if score > 0:
                    results.append((score, fname, i, chunk))

    results.sort(reverse=True)
    print(f"\nTop results for: {query}\n")

    for rank, (score, fname, chunk_id, chunk) in enumerate(results[:3], 1):
        print(f"🔹 Result {rank} — {fname} (chunk {chunk_id}) — Score: {score:.4f}")
        print(chunk.strip())
        print("-" * 50)

if __name__ == "__main__":
    main()
