#!/usr/bin/env python3
"""
Final comprehensive attempt - try everything
"""
import base64
import binascii

encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"
encrypted = encrypted_spaced.replace(" ", "")

print("="*80)
print("TRYING DIFFERENT ENCODINGS")
print("="*80)

# Try base64 (even though unlikely with these characters)
try:
    decoded = base64.b64decode(encrypted)
    print(f"Base64 decoded: {decoded}")
except:
    print("Not valid base64")

# Try hex
try:
    decoded = binascii.unhexlify(encrypted)
    print(f"Hex decoded: {decoded}")
except:
    print("Not valid hex")

# Try ASCII values - convert letters to numbers
print("\n" + "="*80)
print("LETTER TO NUMBER CONVERSIONS")
print("="*80)

# A=0, B=1, etc
numbers = [ord(c) - ord('A') for c in encrypted]
print(f"As numbers (A=0): {numbers[:20]}...")

# A=1, B=2, etc
numbers_1 = [ord(c) - ord('A') + 1 for c in encrypted]
print(f"As numbers (A=1): {numbers_1[:20]}...")

# Try Baconian cipher (every 5 letters represents one letter)
print("\n" + "="*80)
print("BACONIAN CIPHER")
print("="*80)

def baconian_decrypt(text):
    # In Baconian, A/B patterns map to letters
    # Convert to binary-like pattern: A=0, B=1
    # But we need to know which letters are A and which are B
    # Typically uses only A and B, but sometimes any two letters
    pass

# Try looking at the pattern more carefully
print("\n" + "="*80)
print("PATTERN ANALYSIS")
print("="*80)

# Look for repeated sequences
from collections import Counter

# Bigrams
bigrams = [encrypted[i:i+2] for i in range(len(encrypted)-1)]
print(f"Most common bigrams: {Counter(bigrams).most_common(10)}")

# Trigrams
trigrams = [encrypted[i:i+3] for i in range(len(encrypted)-2)]
print(f"Most common trigrams: {Counter(trigrams).most_common(10)}")

# Maybe it's a keyword cipher with a specific arrangement
# Try finding if there's a pattern in letter positions

# What if I just try the most successful Caesar result and manually add spaces?
print("\n" + "="*80)
print("MANUAL WORD IDENTIFICATION")
print("="*80)

# From earlier, shift1=16, shift2=4 had "the"
letters = encrypted_spaced.split()
pattern1 = ''.join([letters[i] for i in range(0, len(letters), 2)])
pattern2 = ''.join([letters[i] for i in range(1, len(letters), 2)])

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in text if c.isalpha())

# Try the most promising looking ones and output them cleanly
promising_shifts = [
    (16, 4),
    (1, 19),
    (3, 9),
    (7, 15),
    (10, 7),
]

for s1, s2 in promising_shifts:
    dec1 = caesar_decrypt(pattern1, s1)
    dec2 = caesar_decrypt(pattern2, s2)

    interleaved = ''
    for i in range(max(len(dec1), len(dec2))):
        if i < len(dec1):
            interleaved += dec1[i]
        if i < len(dec2):
            interleaved += dec2[i]

    print(f"\nShift ({s1}, {s2}):")
    print(interleaved)

    # Try to manually identify words by inserting spaces at likely boundaries
    text = interleaved.lower()

    # Look for common 3-letter words
    for common in ['the', 'and', 'you', 'for', 'are', 'but', 'not', 'all', 'can', 'her',
                   'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how']:
        if common in text:
            idx = text.index(common)
            print(f"   Found '{common}' at position {idx}: ...{interleaved[max(0,idx-5):min(len(interleaved),idx+15)]}...")

# Actually, let me try a completely different approach
# What if the entire message needs a simple ROT13?
print("\n" + "="*80)
print("SIMPLE ROT13 ON FULL MESSAGE")
print("="*80)

rot13 = caesar_decrypt(encrypted, 13)
print(f"ROT13: {rot13}")

# Try all simple Caesar shifts on the full message (not split)
print("\n" + "="*80)
print("SIMPLE CAESAR ON FULL MESSAGE (looking for readable text)")
print("="*80)

for shift in range(26):
    decrypted = caesar_decrypt(encrypted, shift)
    # Check if it looks like English
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'YOU', 'HAVE', 'THAT', 'WITH', 'THIS']
    found = []
    for word in common_words:
        if word in decrypted:
            found.append(word)

    if found:
        print(f"\nShift {shift}: {decrypted}")
        print(f"   Contains: {found}")
