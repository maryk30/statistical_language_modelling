from collections import Counter
import re

INPUT_FILE = "train.txt"
CATEGORIES = {"LITERATURE", "HISTORY", "MUSIC", "GEOGRAPHY", "SCIENCE"}

def compute_bigrams():
    category_bigrams = {cat: [] for cat in CATEGORIES}

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue

            category, sentence = parts

            if category not in CATEGORIES:
                continue

            words = re.findall(r'\b\w+\b', sentence.lower())

            # Generate bigrams
            bigrams = [(words[i], words[i+1]) for i in range(len(words) - 1)]
            category_bigrams[category].extend(bigrams)

    for category in CATEGORIES:
        freq = Counter(category_bigrams[category])

        output_file = f"bigrams_{category}.txt"
        with open(output_file, 'w', encoding='utf-8') as out:
            for (w1, w2), count in sorted(freq.items()):
                out.write(f"{w1} {w2} {count}\n")

        print(f"Saved: {output_file}")

if __name__ == "__main__":
    compute_bigrams()