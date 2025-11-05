#!/usr/bin/env python3
"""
Try Vigenère on each alternating pattern
"""

# Original with spaces
encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"

letters = encrypted_spaced.split()
pattern1 = ''.join([letters[i] for i in range(0, len(letters), 2)])
pattern2 = ''.join([letters[i] for i in range(1, len(letters), 2)])

print("Pattern 1 (even positions):", pattern1)
print("Pattern 2 (odd positions):", pattern2)
print()

def vigenere_decrypt(ciphertext, key):
    key = key.upper()
    result = []
    key_index = 0
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def has_english_words(text):
    """Check for common English words"""
    text_lower = text.lower()
    words = ['the', 'and', 'you', 'for', 'are', 'but', 'not', 'have', 'this', 'that',
             'with', 'from', 'they', 'been', 'were', 'will', 'would', 'could', 'should',
             'when', 'there', 'their', 'what', 'which', 'these', 'those', 'about']
    return [w for w in words if w in text_lower]

# Try all combinations of keys on both patterns
keys = ['CYBER', 'COMMAND', 'DEFENSE', 'SECRET', 'KEY', 'CODE', 'CRYPTO', 'CIPHER',
        'SECURITY', 'MILITARY', 'ALPHA', 'BRAVO', 'CHARLIE', 'DELTA', 'PASSWORD']

print("="*80)
print("TRYING VIGENÈRE ON BOTH PATTERNS SEPARATELY")
print("="*80)

best_results = []

for key1 in keys:
    for key2 in keys:
        dec1 = vigenere_decrypt(pattern1, key1)
        dec2 = vigenere_decrypt(pattern2, key2)

        # Interleave
        interleaved = ''
        for i in range(max(len(dec1), len(dec2))):
            if i < len(dec1):
                interleaved += dec1[i]
            if i < len(dec2):
                interleaved += dec2[i]

        # Check for English words
        found_words = has_english_words(interleaved)
        if len(found_words) >= 3:  # At least 3 common words
            best_results.append((key1, key2, len(found_words), found_words, interleaved))

# Sort by number of words found
best_results.sort(key=lambda x: x[2], reverse=True)

print(f"\nFound {len(best_results)} promising combinations\n")

for i, (k1, k2, count, words, text) in enumerate(best_results[:20], 1):
    print(f"{i}. Key1='{k1}', Key2='{k2}' ({count} words: {words})")
    print(f"   {text[:100]}...")
    if count >= 5:
        print(f"   FULL TEXT: {text}")
    print()

# Also try Caesar on pattern1 and Vigenère on pattern2 (and vice versa)
print("="*80)
print("TRYING CAESAR ON ONE PATTERN, VIGENÈRE ON OTHER")
print("="*80)

def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
    return result

for shift in range(26):
    for key in keys:
        # Caesar on pattern1, Vigenère on pattern2
        dec1 = caesar_decrypt(pattern1, shift)
        dec2 = vigenere_decrypt(pattern2, key)

        interleaved = ''
        for i in range(max(len(dec1), len(dec2))):
            if i < len(dec1):
                interleaved += dec1[i]
            if i < len(dec2):
                interleaved += dec2[i]

        found_words = has_english_words(interleaved)
        if len(found_words) >= 4:
            print(f"\nCaesar({shift}) + Vigenère('{key}'): {len(found_words)} words {found_words}")
            print(f"{interleaved[:100]}...")
            if len(found_words) >= 6:
                print(f"FULL TEXT: {interleaved}")

        # Vigenère on pattern1, Caesar on pattern2
        dec1 = vigenere_decrypt(pattern1, key)
        dec2 = caesar_decrypt(pattern2, shift)

        interleaved = ''
        for i in range(max(len(dec1), len(dec2))):
            if i < len(dec1):
                interleaved += dec1[i]
            if i < len(dec2):
                interleaved += dec2[i]

        found_words = has_english_words(interleaved)
        if len(found_words) >= 4:
            print(f"\nVigenère('{key}') + Caesar({shift}): {len(found_words)} words {found_words}")
            print(f"{interleaved[:100]}...")
            if len(found_words) >= 6:
                print(f"FULL TEXT: {interleaved}")
