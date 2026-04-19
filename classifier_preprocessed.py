import sys
import os
import math
import re
from collections import defaultdict

CATEGORIES = ["LITERATURE", "HISTORY", "MUSIC", "GEOGRAPHY", "SCIENCE"]

# ---------- TOKENIZATION ----------
def tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())


# ---------- LOAD UNIGRAM MODELS ----------
def load_unigrams(counts_dir):
    models = {}
    totals = {}

    for cat in CATEGORIES:
        model = defaultdict(int)
        total = 0

        file_path = os.path.join(counts_dir, f"unigrams_{cat}_preprocessed.txt")

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                word, count = line.strip().split()
                count = int(count)
                model[word] = count
                total += count

        models[cat] = model
        totals[cat] = total

    return models, totals


# ---------- LOAD BIGRAM MODELS ----------
def load_bigrams(counts_dir):
    models = {}
    totals = {}

    for cat in CATEGORIES:
        model = defaultdict(int)
        total = 0

        file_path = os.path.join(counts_dir, f"bigrams_{cat}_preprocessed.txt")

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                w1, w2, count = line.strip().split()
                count = int(count)
                model[(w1, w2)] = count
                total += count

        models[cat] = model
        totals[cat] = total

    return models, totals

def compute_global_vocab_size(train_file):
    vocab = set()
    with open(train_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) != 3:
                continue

            _, sentence, _ = parts

            words = re.findall(r'\b\w+\b', sentence.lower())
            vocab.update(words)

    return len(vocab)

# ---------- SCORING FUNCTIONS ----------
def score_unigrams(words, model, total):
    score = 0.0
    for w in words:
        count = model.get(w, 0)
        if count > 0:
            score += math.log(count / total)
        else:
            score += math.log(1e-6)  # unseen word penalty
    return score


def score_bigrams(words, model, total):
    score = 0.0
    for i in range(len(words) - 1):
        bg = (words[i], words[i+1])
        count = model.get(bg, 0)
        if count > 0:
            score += math.log(count / total)
        else:
            score += math.log(1e-6)
    return score


def score_bigrams_smooth(words, bigram_model, unigram_model, V):
    if len(words) < 2:
        return math.log(1e-6)

    score = 0.0

    for i in range(len(words) - 1):
        w1, w2 = words[i], words[i + 1]

        bigram_count = bigram_model.get((w1, w2), 0)
        unigram_count = unigram_model.get(w1, 0)

        prob = (bigram_count + 1) / (unigram_count + V)
        score += math.log(prob)

    return score / (len(words) - 1)


# ---------- CLASSIFIER ----------
def classify(model_type, counts_dir, eval_file):
    if model_type == "unigrams":
        unigram_models, unigram_totals = load_unigrams(counts_dir)

    elif model_type == "bigrams":
        bigram_models, bigram_totals = load_bigrams(counts_dir)

    elif model_type == "smooth":
        unigram_models, unigram_totals = load_unigrams("counts")
        bigram_models, bigram_totals = load_bigrams(counts_dir)
        V = compute_global_vocab_size("data/train.txt")


    with open(eval_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            words = tokenize(line)

            best_label = None
            best_score = -float('inf')

            for cat in CATEGORIES:
                if model_type == "unigrams":
                    score = score_unigrams(
                        words,
                        unigram_models[cat],
                        unigram_totals[cat]
                    )

                elif model_type == "bigrams":
                    score = score_bigrams(
                        words,
                        bigram_models[cat],
                        bigram_totals[cat]
                    )

                elif model_type == "smooth":
                    score = score_bigrams_smooth(
                        words,
                        bigram_models[cat],
                        unigram_models[cat],
                        V
                    )

                else:
                    print("Invalid model type")
                    sys.exit(1)

                if score > best_score:
                    best_score = score
                    best_label = cat

            print(best_label)


# ---------- MAIN ----------
if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 classifier.py <model_type> <counts_dir> <eval_file>")
        sys.exit(1)

    model_type = sys.argv[1]
    counts_dir = sys.argv[2]
    eval_file = sys.argv[3]

    classify(model_type, counts_dir, eval_file)