#!/usr/bin/env python3
"""
Solve substitution cipher using frequency analysis and pattern matching
"""
import re
from collections import Counter

encrypted = "ZHVAJCJHKDFRHJHZMIRHJYRGFLNRHLJAJSHZEXOLDDOLRIAWLJRMAAZZTDVBIKUCDHEZEFRXXIHRKDUXEXFJDKVLRJXFOHJJQRRLEFJDCOXEJYBFEJHRDSEXXHMZOFWJFGMDSUCZXRLBHDLYQW"

# English letter frequency (from most to least common)
ENGLISH_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# Common English words
COMMON_WORDS = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM', 'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO', 'WAY', 'WHO', 'BOY', 'DID', 'HER']

def get_frequency(text):
    """Get character frequency in order"""
    counter = Counter(char for char in text if char.isalpha())
    return ''.join([char for char, _ in counter.most_common()])

def apply_mapping(text, mapping):
    """Apply a character mapping to text"""
    result = []
    for char in text:
        result.append(mapping.get(char, char))
    return ''.join(result)

def score_text(text):
    """Score text based on English characteristics"""
    score = 0
    text_upper = text.upper()

    # Check for common words
    for word in COMMON_WORDS:
        score += text_upper.count(word) * len(word)

    # Check for common bigrams
    common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ON', 'ES', 'ST', 'EN', 'AT', 'TO', 'NT', 'HA', 'ND', 'OU', 'EA', 'NG', 'AS', 'OR', 'TI', 'IS', 'ET', 'IT', 'AR', 'TE', 'SE', 'HI', 'OF']
    for bigram in common_bigrams:
        score += text_upper.count(bigram)

    # Check for common trigrams
    common_trigrams = ['THE', 'AND', 'THA', 'ENT', 'ION', 'TIO', 'FOR', 'NDE', 'HAS', 'NCE', 'EDT', 'TIS', 'OFT', 'STH', 'MEN']
    for trigram in common_trigrams:
        score += text_upper.count(trigram) * 2

    return score

def find_word_patterns(text):
    """Find repeated patterns that might be common words"""
    words = re.findall(r'[A-Z]+', text)
    patterns = {}
    for word in words:
        if len(word) >= 3:
            patterns[word] = patterns.get(word, 0) + 1
    return dict(sorted(patterns.items(), key=lambda x: x[1], reverse=True))

# Get frequency of encrypted text
cipher_freq = get_frequency(encrypted)
print("="*80)
print("FREQUENCY ANALYSIS")
print("="*80)
print(f"English frequency: {ENGLISH_FREQ}")
print(f"Cipher frequency:  {cipher_freq}")
print()

# Create initial mapping based on frequency
initial_mapping = {}
for i, cipher_char in enumerate(cipher_freq):
    if i < len(ENGLISH_FREQ):
        initial_mapping[cipher_char] = ENGLISH_FREQ[i]

print("Initial mapping based on frequency:")
print(initial_mapping)
print()

initial_decrypt = apply_mapping(encrypted, initial_mapping)
print(f"Initial decryption: {initial_decrypt}")
print(f"Score: {score_text(initial_decrypt)}")
print()

# Look for patterns
print("="*80)
print("PATTERN ANALYSIS")
print("="*80)

# Look for double letters
doubles = re.findall(r'(.)\1', encrypted)
print(f"Double letters in ciphertext: {set(doubles)}")
print("Common double letters in English: L, S, E, F, O, T")
print()

# Look for single letters (could be 'A' or 'I')
# The encrypted message has no spaces, so we can't identify single-letter words

# Try specific mappings for common patterns
print("="*80)
print("TRYING MANUAL ADJUSTMENTS")
print("="*80)

# Looking at the encrypted text, let's try some manual substitutions
# DD could be LL, EE, SS, OO, FF, TT
# Let me try mapping based on that

test_mappings = []

# If HJ appears multiple times, it might be TH, HE, IN, ER, AN
hj_pattern = encrypted.count('HJ')
print(f"'HJ' appears {hj_pattern} times")

# Let's try a more systematic approach
# Looking for THE pattern (most common 3-letter word)
print("\nSearching for 'THE' pattern...")

# THE has pattern ABB (last two letters different from first, middle and last different)
# Actually THE has all different letters

# Let me try a Hill Climbing approach
import random

best_mapping = initial_mapping.copy()
best_score = score_text(initial_decrypt)
best_text = initial_decrypt

print(f"\nStarting Hill Climbing optimization...")
print(f"Initial score: {best_score}")

# Try random swaps to improve the mapping
for iteration in range(1000):
    # Make a random swap
    new_mapping = best_mapping.copy()
    chars = list(cipher_freq)
    if len(chars) >= 2:
        i, j = random.sample(range(min(len(chars), len(ENGLISH_FREQ))), 2)
        # Swap the plaintext assignments
        temp = new_mapping.get(chars[i], chars[i])
        new_mapping[chars[i]] = new_mapping.get(chars[j], chars[j])
        new_mapping[chars[j]] = temp

    new_text = apply_mapping(encrypted, new_mapping)
    new_score = score_text(new_text)

    if new_score > best_score:
        best_score = new_score
        best_mapping = new_mapping
        best_text = new_text
        if iteration % 100 == 0:
            print(f"Iteration {iteration}: New best score {best_score}")
            print(f"Text: {best_text[:80]}...")

print("\n" + "="*80)
print("BEST RESULT FROM HILL CLIMBING")
print("="*80)
print(f"Score: {best_score}")
print(f"Mapping: {best_mapping}")
print(f"Decrypted text: {best_text}")
