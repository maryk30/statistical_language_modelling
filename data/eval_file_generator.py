INPUT_FILE = "eval.txt"
QUESTIONS_FILE = "eval-questions.txt"
LABELS_FILE = "eval-labels.txt"

def process_eval():
    with open(INPUT_FILE, 'r', encoding='utf-8') as infile, \
         open(QUESTIONS_FILE, 'w', encoding='utf-8') as qfile, \
         open(LABELS_FILE, 'w', encoding='utf-8') as lfile:

        for line in infile:
            line = line.strip()
            if not line:
                continue

            # Extract TAG (first word)
            parts = line.split(maxsplit=1)
            if len(parts) != 2:
                continue

            tag, rest = parts

            # Write TAG to labels file
            lfile.write(tag + "\n")

            first_quote = rest.find('"')
            last_quote = rest.rfind('"')

            if first_quote != -1 and last_quote != -1 and first_quote != last_quote:
                sentence = rest[first_quote:last_quote+1]
                answer = rest[last_quote+1:].strip()

                qfile.write(f"{sentence} {answer}\n")
            else:
                qfile.write(rest + "\n")

    print(f"Saved: {QUESTIONS_FILE}")
    print(f"Saved: {LABELS_FILE}")

if __name__ == "__main__":
    process_eval()