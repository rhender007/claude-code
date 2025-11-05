#!/usr/bin/env python3
"""
Intelligent cipher solver using n-gram statistics
"""
import random
import math

encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"
encrypted = encrypted_spaced.replace(" ", "")
letters = encrypted_spaced.split()

# Common English trigrams and their frequencies
TRIGRAMS = {
    'THE': 3.509, 'AND': 1.594, 'THA': 1.200, 'ENT': 1.069, 'ION': 1.035,
    'TIO': 1.002, 'FOR': 0.979, 'NDE': 0.967, 'HAS': 0.961, 'NCE': 0.875,
    'TIS': 0.835, 'OFT': 0.827, 'MEN': 0.799, 'ING': 0.772, 'ETH': 0.765
}

BIGRAMS = {
    'TH': 3.56, 'HE': 3.07, 'IN': 2.43, 'ER': 2.05, 'AN': 1.99,
    'RE': 1.85, 'ON': 1.76, 'AT': 1.49, 'EN': 1.45, 'ND': 1.35,
    'TI': 1.34, 'ES': 1.34, 'OR': 1.28, 'TE': 1.20, 'OF': 1.17
}

def score_text_ngrams(text):
    """Score using n-gram statistics"""
    score = 0
    text = text.upper()

    # Trigram scoring
    for i in range(len(text) - 2):
        trigram = text[i:i+3]
        if trigram in TRIGRAMS:
            score += TRIGRAMS[trigram] * 100

    # Bigram scoring
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        if bigram in BIGRAMS:
            score += BIGRAMS[bigram] * 10

    # Common words
    words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
             'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM',
             'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO',
             'WAY', 'WHO', 'BOY', 'DID', 'END', 'LET', 'PUT', 'SAY', 'TOO']

    for word in words:
        score += text.count(word) * 50

    return score

def decrypt_alternating_caesar(text, shift1, shift2):
    """Decrypt with alternating Caesar shifts"""
    result = []
    for i, char in enumerate(text):
        if char.isalpha():
            shift = shift1 if i % 2 == 0 else shift2
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

def decrypt_pattern_caesar(letters_list, shift1, shift2):
    """Decrypt alternating pattern with Caesar shifts"""
    pattern1 = ''.join([letters_list[i] for i in range(0, len(letters_list), 2)])
    pattern2 = ''.join([letters_list[i] for i in range(1, len(letters_list), 2)])

    dec1 = ''.join(chr((ord(c) - ord('A') - shift1) % 26 + ord('A')) for c in pattern1)
    dec2 = ''.join(chr((ord(c) - ord('A') - shift2) % 26 + ord('A')) for c in pattern2)

    # Interleave
    result = []
    for i in range(max(len(dec1), len(dec2))):
        if i < len(dec1):
            result.append(dec1[i])
        if i < len(dec2):
            result.append(dec2[i])

    return ''.join(result)

# Method 1: Try all shifts with proper scoring
print("="*80)
print("METHOD 1: ALTERNATING PATTERN CAESAR WITH N-GRAM SCORING")
print("="*80)

best_score = 0
best_result = ""
best_shifts = (0, 0)

for s1 in range(26):
    for s2 in range(26):
        decrypted = decrypt_pattern_caesar(letters, s1, s2)
        score = score_text_ngrams(decrypted)

        if score > best_score:
            best_score = score
            best_result = decrypted
            best_shifts = (s1, s2)

print(f"Best result:")
print(f"Shifts: {best_shifts}, Score: {best_score}")
print(f"Text: {best_result}")

# Try to add spaces intelligently
print("\nAttempting word segmentation:")

def segment_text(text):
    """Try to add spaces between words"""
    common_words = set([
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
        'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
        'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
        'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their',
        'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go',
        'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know',
        'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them',
        'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its',
        'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our',
        'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any',
        'these', 'give', 'day', 'most', 'us', 'is', 'was', 'are', 'been', 'has',
        'had', 'were', 'said', 'did', 'having', 'may', 'should', 'am', 'being',
    ])

    text = text.lower()
    n = len(text)

    # Dynamic programming approach
    # best[i] = (score, segmentation) for text[0:i]
    best = [(-float('inf'), [])] * (n + 1)
    best[0] = (0, [])

    for i in range(1, n + 1):
        # Try all possible last words
        for j in range(max(0, i - 15), i):  # words up to 15 chars
            word = text[j:i]
            if word in common_words:
                new_score = best[j][0] + len(word) ** 2
                if new_score > best[i][0]:
                    best[i] = (new_score, best[j][1] + [word])
            elif len(word) == 1 and word in 'ai':
                new_score = best[j][0] + 1
                if new_score > best[i][0]:
                    best[i] = (new_score, best[j][1] + [word])

    return ' '.join(best[n][1]) if best[n][1] else text

segmented = segment_text(best_result)
print(segmented)

if segmented != best_result.lower():
    print("\n*** Found word boundaries! ***")

# Method 2: Try simple Caesar on whole text
print("\n" + "="*80)
print("METHOD 2: SIMPLE CAESAR ON WHOLE TEXT")
print("="*80)

def caesar_decrypt_simple(text, shift):
    return ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in text if c.isalpha())

best_caesar_score = 0
best_caesar_result = ""
best_caesar_shift = 0

for shift in range(26):
    decrypted = caesar_decrypt_simple(encrypted, shift)
    score = score_text_ngrams(decrypted)

    if score > best_caesar_score:
        best_caesar_score = score
        best_caesar_result = decrypted
        best_caesar_shift = shift

print(f"Best Caesar shift: {best_caesar_shift}, Score: {best_caesar_score}")
print(f"Text: {best_caesar_result}")

# Compare the two methods
print("\n" + "="*80)
print("COMPARISON")
print("="*80)
print(f"Pattern method score: {best_score}")
print(f"Simple Caesar score: {best_caesar_score}")

if best_score > best_caesar_score:
    print(f"\n*** BEST RESULT (Pattern method) ***")
    print(f"Shifts: {best_shifts}")
    print(f"Text: {best_result}")
    print(f"Segmented: {segment_text(best_result)}")
else:
    print(f"\n*** BEST RESULT (Simple Caesar) ***")
    print(f"Shift: {best_caesar_shift}")
    print(f"Text: {best_caesar_result}")
    print(f"Segmented: {segment_text(best_caesar_result)}")
