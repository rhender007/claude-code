#!/usr/bin/env python3
"""
Comprehensive brute force with proper English scoring
"""
import re

encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"

letters = encrypted_spaced.split()
pattern1 = ''.join([letters[i] for i in range(0, len(letters), 2)])
pattern2 = ''.join([letters[i] for i in range(1, len(letters), 2)])

def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
    return result

def score_english_advanced(text):
    """Advanced English scoring"""
    text_lower = text.lower()
    score = 0

    # Very common words (high weight)
    very_common = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i',
                   'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at',
                   'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she',
                   'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their']

    for word in very_common:
        # Count occurrences with word boundaries
        pattern = r'\b' + word + r'\b'
        matches = len(re.findall(pattern, text_lower))
        score += matches * 100

    # Common bigrams
    bigrams = ['th', 'he', 'in', 'er', 'an', 're', 'nd', 'on', 'en', 'at',
               'ou', 'ed', 'ha', 'to', 'or', 'it', 'is', 'hi', 'es', 'ng']
    for bg in bigrams:
        score += text_lower.count(bg) * 2

    # Common trigrams
    trigrams = ['the', 'and', 'ing', 'her', 'hat', 'his', 'tha', 'ere', 'for', 'ent',
                'ion', 'ter', 'was', 'you', 'ith', 'ver', 'all', 'wit', 'thi', 'tio']
    for tg in trigrams:
        score += text_lower.count(tg) * 3

    # Penalize uncommon letter combinations
    bad_bigrams = ['qx', 'qz', 'qj', 'jq', 'jz', 'zj', 'zx', 'xz', 'xj', 'jx']
    for bg in bad_bigrams:
        score -= text_lower.count(bg) * 10

    # Bonus for lowercase/sentence structure (we converted to lowercase but check original)
    # Check for reasonable letter frequency
    letter_freq = {}
    for c in text_lower:
        if c.isalpha():
            letter_freq[c] = letter_freq.get(c, 0) + 1

    # Most common letters in English
    if 'e' in letter_freq and letter_freq['e'] > len(text_lower) * 0.08:
        score += 50
    if 't' in letter_freq and letter_freq['t'] > len(text_lower) * 0.06:
        score += 30

    return score

print("="*80)
print("BRUTE FORCE WITH ADVANCED SCORING")
print("="*80)

best_results = []

for shift1 in range(26):
    for shift2 in range(26):
        dec1 = caesar_decrypt(pattern1, shift1)
        dec2 = caesar_decrypt(pattern2, shift2)

        # Interleave
        interleaved = ''
        for i in range(max(len(dec1), len(dec2))):
            if i < len(dec1):
                interleaved += dec1[i]
            if i < len(dec2):
                interleaved += dec2[i]

        score = score_english_advanced(interleaved)
        best_results.append((shift1, shift2, score, interleaved))

# Sort by score
best_results.sort(key=lambda x: x[2], reverse=True)

print(f"\nTop 20 results:\n")

for i, (s1, s2, score, text) in enumerate(best_results[:20], 1):
    print(f"{i}. Shift1={s1:2d}, Shift2={s2:2d} | Score: {score:5d}")
    print(f"   {text}")

    # Try to add spaces at reasonable points
    words = []
    i = 0
    temp = text.lower()

    # Try to identify common words
    common_words = ['the', 'and', 'you', 'have', 'that', 'with', 'from', 'they',
                    'been', 'were', 'will', 'would', 'could', 'this', 'there', 'their',
                    'which', 'about', 'when', 'what', 'your', 'can', 'said', 'each',
                    'them', 'then', 'some', 'into', 'time', 'has', 'look', 'two',
                    'more', 'these', 'her', 'see', 'him', 'has', 'may', 'after',
                    'back', 'use', 'than', 'first', 'been', 'its', 'who', 'now',
                    'people', 'my', 'made', 'over', 'did', 'down', 'way', 'only',
                    'may', 'find', 'use', 'how', 'said', 'new', 'make', 'know',
                    'most', 'other', 'take', 'come', 'than', 'them']

    # Check if we can identify full sentences
    for word in common_words:
        if word in temp:
            print(f"   Contains: '{word}'")
            break

    print()

print("\n" + "="*80)
print("BEST CANDIDATE (highest score):")
print("="*80)

if best_results:
    s1, s2, score, text = best_results[0]
    print(f"Shift1={s1}, Shift2={s2}")
    print(f"Score: {score}")
    print(f"\nDecrypted text:\n{text}")

    # Try to parse it intelligently
    print(f"\nAttempting to add spaces:")
    # Simple word detection
    text_lower = text.lower()

    # Try to find word boundaries by matching against dictionary
    # For now, just show it formatted
    formatted = ""
    i = 0
    while i < len(text_lower):
        # Try to match longest word first
        found = False
        for length in range(min(15, len(text_lower) - i), 0, -1):
            word = text_lower[i:i+length]
            # Check if it's a common word
            common = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
                      'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him',
                      'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two',
                      'way', 'who', 'boy', 'did', 'end', 'let', 'put', 'say', 'too',
                      'use', 'have', 'this', 'that', 'with', 'from', 'they', 'been',
                      'have', 'were', 'said', 'each', 'which', 'their', 'would', 'about',
                      'could', 'these', 'first', 'after', 'where', 'there']
            if word in common:
                formatted += word + " "
                i += length
                found = True
                break
        if not found:
            formatted += text_lower[i]
            i += 1

    print(formatted[:200])
