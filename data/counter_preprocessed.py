from collections import Counter
import re
import os

INPUT_FILE = "data/train_preprocessed.txt"
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

    OUTPUT_DIR_UNIGRAMS = "counts"
    os.makedirs(OUTPUT_DIR_UNIGRAMS, exist_ok=True)

    for category in CATEGORIES:
        freq = Counter(category_words[category])

        output_file = os.path.join(OUTPUT_DIR_UNIGRAMS, f"unigrams_{category}_preprocessed.txt")
        with open(output_file, 'w', encoding='utf-8') as out:
            for word, count in sorted(freq.items()): 
                out.write(f"{word} {count}\n")

        print(f"Saved: {output_file}")

def compute_bigrams():
    category_bigrams = {cat: [] for cat in CATEGORIES}

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

                # Process ONLY the sentence
                words = re.findall(r'\b\w+\b', sentence.lower())

                # Generate bigrams
                bigrams = [(words[i], words[i+1]) for i in range(len(words) - 1)]
                category_bigrams[category].extend(bigrams)
    OUTPUT_DIR_BIGRAMS = "counts2"
    os.makedirs(OUTPUT_DIR_BIGRAMS, exist_ok=True)

    for category in CATEGORIES:
        freq = Counter(category_bigrams[category])

        output_file = os.path.join(OUTPUT_DIR_BIGRAMS, f"bigrams_{category}_preprocessed.txt")
        with open(output_file, 'w', encoding='utf-8') as out:
            for (w1, w2), count in sorted(freq.items()):
                out.write(f"{w1} {w2} {count}\n")

        print(f"Saved: {output_file}")
    
if __name__ == "__main__":
    compute_unigrams()
    compute_bigrams()