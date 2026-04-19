import re
import sys

OUTPUT_FILE = "data/train_preprocessed.txt"

CATEGORIES = {"LITERATURE", "HISTORY", "MUSIC", "GEOGRAPHY", "SCIENCE"}


# ---------- PREPROCESS FUNCTION ----------
def preprocess(text):
    text = text.lower()

    # Replace years (e.g., 1999, 2020)
    text = re.sub(r'\b(1[0-9]{3}|20[0-9]{2})\b', '_YEAR_ ', text)

    # Replace other numbers
    text = re.sub(r'\b\d+\b', '_NUM_ ', text)

    # Remove punctuation (keep underscores)
    text = re.sub(r'[^\w\s]', '', text)

    # Clean spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


# ---------- MAIN ----------
def preprocess_file(input_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:

        for line in infile:
            line = line.strip()
            if not line:
                continue

            # Split into CATEGORY and rest
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue

            category, rest = parts

            if category not in CATEGORIES:
                continue

            # Extract sentence and answer
            # Assumes: CATEGORY "sentence" answer
            first_quote = rest.find('"')
            last_quote = rest.rfind('"')

            if first_quote != -1 and last_quote != -1 and first_quote != last_quote:
                sentence = rest[first_quote + 1:last_quote]
                answer = rest[last_quote + 1:].strip()
            else:
                # fallback if no quotes
                parts_rest = rest.rsplit(maxsplit=1)
                if len(parts_rest) != 2:
                    continue
                sentence, answer = parts_rest

            # Preprocess ONLY the sentence
            processed_sentence = preprocess(sentence)

            # Reconstruct line (keep answer unchanged)
            outfile.write(f'{category}\t{processed_sentence}\t{answer}\n')

    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 preprocessor.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    preprocess_file(input_file)
