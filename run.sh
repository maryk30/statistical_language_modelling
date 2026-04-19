#!/bin/bash

set -e

echo "===================================="
echo "  NLP Classification Pipeline"
echo "===================================="

# ---------------- INPUTS ----------------
TRAIN_FILE="data/train.txt"
EVAL_FILE="data/eval-questions.txt"
TEST_FILE="data/test-questions.txt"
VERIFY_FILE="data/eval-labels.txt"
COUNT_DIR="counts"
COUNT_DIR2="counts2"

#1.Unprocessed Data
#a. Compute unigrams and bigrams on unprocessed data
python3 counter.py "$TRAIN_FILE"

#b. Classify and evaluate based on unigrams
python3 classifier.py unigrams "$COUNT_DIR" "$EVAL_FILE" > data/results/results_unprocessed_unigrams.txt
python3 evaluate.py -v data/results/results_unprocessed_unigrams.txt "$VERIFY_FILE"

#c. Classify and evaluate based on bigrams
python3 classifier.py bigrams "$COUNT_DIR2" "$EVAL_FILE" > data/results/results_unprocessed_bigrams.txt
python3 evaluate.py -v data/results/results_unprocessed_bigrams.txt "$VERIFY_FILE"

#d. Classify and evaluate based on bigrams with smoothing
python3 classifier.py smooth "$COUNT_DIR2" "$EVAL_FILE" > data/results/results_unprocessed_smooth.txt
python3 evaluate.py -v data/results/results_unprocessed_smooth.txt "$VERIFY_FILE"

#2. Preprocessed Data
#a. Preprocess training data
python3 preprocessor.py "$TRAIN_FILE"

#b. Compute unigrams and bigrams
python3 counter_preprocessed.py data/train_preprocessed.txt

#b. Classify and evaluate based on unigrams
python3 classifier_preprocessed.py unigrams "$COUNT_DIR" "$EVAL_FILE" > data/results/results_preprocessed_unigrams.txt
python3 evaluate.py -v data/results/results_preprocessed_unigrams.txt "$VERIFY_FILE"

#c. Classify and evaluate based on bigrams
python3 classifier_preprocessed.py bigrams "$COUNT_DIR2" "$EVAL_FILE" > data/results/results_preprocessed_bigrams.txt
python3 evaluate.py -v data/results/results_preprocessed_bigrams.txt "$VERIFY_FILE"

#d. Classify and evaluate based on bigrams with smoothing
python3 classifier_preprocessed.py smooth "$COUNT_DIR2" "$EVAL_FILE" > data/results/results_preprocessed_smooth.txt
python3 evaluate.py -v data/results/results_preprocessed_smooth.txt "$VERIFY_FILE"

#3. Test File
#a. Preprocessing
python3 test_preprocessor.py "$EVAL_FILE"

#c. Chosen result
python3 classifier_preprocessed.py unigrams "$COUNT_DIR" "$TEST_FILE" > results/test-guess.txt

