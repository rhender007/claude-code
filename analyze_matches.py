#!/usr/bin/env python3
"""
Analyze the promising matches
"""

# Original with spaces
encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"

letters = encrypted_spaced.split()
pattern1 = ''.join([letters[i] for i in range(0, len(letters), 2)])
pattern2 = ''.join([letters[i] for i in range(1, len(letters), 2)])

def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            result += char
    return result

def score_english(text):
    """Score text for English-likeness"""
    score = 0
    text_lower = text.lower()

    # Common words with higher weight
    common_words = {
        'the': 100, 'and': 80, 'you': 70, 'for': 60, 'are': 60,
        'but': 50, 'not': 50, 'have': 80, 'that': 70, 'with': 70,
        'from': 60, 'they': 60, 'been': 60, 'this': 70, 'will': 60,
        'your': 60, 'what': 50, 'when': 50, 'there': 70, 'their': 70,
        'which': 60, 'would': 60, 'could': 60, 'about': 50, 'other': 50,
        'were': 60, 'been': 60, 'more': 50, 'into': 40, 'only': 40,
        'time': 40, 'than': 40, 'them': 40, 'then': 40, 'also': 40,
        'some': 40, 'make': 40, 'like': 40, 'these': 40, 'need': 40
    }

    for word, weight in common_words.items():
        if ' ' + word + ' ' in ' ' + text_lower + ' ' or text_lower.startswith(word + ' ') or text_lower.endswith(' ' + word):
            score += weight * text_lower.count(word)

    return score

# Test all promising combinations
promising = [
    (1, 19),
    (3, 9),
    (7, 4),
    (7, 15),
    (9, 11),
    (10, 21),
    (10, 22),
    (13, 8),
    (13, 13),
    (14, 24),
    (16, 4),
    (18, 1),
    (22, 4),
    (22, 9),
    (23, 23),
]

results = []
for shift1, shift2 in promising:
    dec1 = caesar_decrypt(pattern1, shift1)
    dec2 = caesar_decrypt(pattern2, shift2)

    # Interleave them back
    interleaved = ''
    for i in range(max(len(dec1), len(dec2))):
        if i < len(dec1):
            interleaved += dec1[i]
        if i < len(dec2):
            interleaved += dec2[i]

    score = score_english(interleaved)
    results.append((shift1, shift2, score, interleaved))

# Sort by score
results.sort(key=lambda x: x[2], reverse=True)

print("="*80)
print("TOP CANDIDATES BY ENGLISH SCORE")
print("="*80)

for i, (s1, s2, score, text) in enumerate(results[:10], 1):
    print(f"\n{i}. Shift1={s1}, Shift2={s2} (Score: {score})")
    print(f"Text: {text}")
    print()

# Let me manually check the top few
print("="*80)
print("MANUAL INSPECTION OF TOP CANDIDATES")
print("="*80)

for i, (s1, s2, score, text) in enumerate(results[:5], 1):
    print(f"\n{i}. Shifts ({s1}, {s2}):")
    # Try to identify word boundaries by looking for common patterns
    text_lower = text.lower()
    print(f"   {text}")

    # Look for sequences that might be words
    if 'you' in text_lower:
        idx = text_lower.index('you')
        print(f"   Found 'you' at position {idx}: ...{text[max(0,idx-10):idx+20]}...")

    if 'the' in text_lower:
        idx = text_lower.index('the')
        print(f"   Found 'the' at position {idx}: ...{text[max(0,idx-10):idx+20]}...")

    if 'and' in text_lower:
        idx = text_lower.index('and')
        print(f"   Found 'and' at position {idx}: ...{text[max(0,idx-10):idx+20]}...")

    if 'have' in text_lower:
        idx = text_lower.index('have')
        print(f"   Found 'have' at position {idx}: ...{text[max(0,idx-10):idx+20]}...")
