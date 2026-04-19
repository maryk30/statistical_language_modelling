import re
import sys

OUTPUT_FILE = "data/test_preprocessed.txt"


# ---------- PREPROCESS FUNCTION ----------
def preprocess(text):
    text = text.lower()

    # Replace years (e.g., 1999, 2020)
    text = re.sub(r'\b(1[0-9]{3}|20[0-9]{2})\b', '_YEAR_', text)

    # Replace other numbers
    text = re.sub(r'\b\d+\b', '_NUM_', text)

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

            # Expect: sentence \t answer
            parts = line.split('\t')

            if len(parts) != 2:
                continue

            sentence, answer = parts

            # preprocess ONLY sentence
            processed_sentence = preprocess(sentence)

            # write output
            outfile.write(f"{processed_sentence}\t{answer}\n")

    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 preprocessor.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    preprocess_file(input_file)