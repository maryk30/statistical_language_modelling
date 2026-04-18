from collections import Counter
import re

INPUT_FILE = "train.txt"
CATEGORIES = {"LITERATURE", "HISTORY", "MUSIC", "GEOGRAPHY", "SCIENCE"}

def compute_unigrams():
    category_words = {cat: [] for cat in CATEGORIES}

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) != 3:
                continue

            category, sentence, answer = parts

            if category not in CATEGORIES:
                continue

            # Only process the sentence (ignore answer)
            words = re.findall(r'\b\w+\b', sentence.lower())
            category_words[category].extend(words)

    for category in CATEGORIES:
        freq = Counter(category_words[category])

        output_file = f"unigrams_{category}.txt"
        with open(output_file, 'w', encoding='utf-8') as out:
            for word, count in sorted(freq.items()):
                out.write(f"{word} {count}\n")

        print(f"Saved: {output_file}")

if __name__ == "__main__":
    compute_unigrams()