#!/usr/bin/env python3
"""
Analyze the original spacing in the message
"""

# Original with spaces
encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"

encrypted = encrypted_spaced.replace(" ", "")

print("="*80)
print("ANALYZING ORIGINAL SPACING")
print("="*80)

# The message appears to have single-letter spacing
# Let's split by spaces and analyze
letters = encrypted_spaced.split()
print(f"Number of letters: {len(letters)}")
print(f"Letters: {letters[:20]}...")

# Try taking every Nth letter
print("\n" + "="*80)
print("PATTERN EXTRACTION")
print("="*80)

# Every 2nd letter starting from 0
pattern1 = ''.join([letters[i] for i in range(0, len(letters), 2)])
print(f"\nEvery 2nd letter (starting at 0): {pattern1}")

# Every 2nd letter starting from 1
pattern2 = ''.join([letters[i] for i in range(1, len(letters), 2)])
print(f"Every 2nd letter (starting at 1): {pattern2}")

# Try decrypting these patterns with Caesar
def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
        else:
            result += char
    return result

print("\n" + "="*80)
print("CAESAR ON PATTERN 1 (even positions)")
print("="*80)

for shift in range(26):
    decrypted = caesar_decrypt(pattern1, shift)
    if any(word in decrypted.lower() for word in ['the', 'and', 'you', 'for', 'have', 'that', 'with']):
        print(f"\nShift {shift}: {decrypted}")
        print("  *** POSSIBLE MATCH ***")

print("\n" + "="*80)
print("CAESAR ON PATTERN 2 (odd positions)")
print("="*80)

for shift in range(26):
    decrypted = caesar_decrypt(pattern2, shift)
    if any(word in decrypted.lower() for word in ['the', 'and', 'you', 'for', 'have', 'that', 'with']):
        print(f"\nShift {shift}: {decrypted}")
        print("  *** POSSIBLE MATCH ***")

# Try Vigenère on these patterns
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

print("\n" + "="*80)
print("VIGENÈRE ON PATTERNS")
print("="*80)

keys = ['DEFENSE', 'CYBER', 'COMMAND', 'SECRET', 'KEY']

for key in keys:
    dec1 = vigenere_decrypt(pattern1, key)
    dec2 = vigenere_decrypt(pattern2, key)

    if any(word in dec1.lower() for word in ['the', 'and', 'you', 'for', 'have']):
        print(f"\nPattern 1 with key '{key}': {dec1}")
        print("  *** POSSIBLE MATCH ***")

    if any(word in dec2.lower() for word in ['the', 'and', 'you', 'for', 'have']):
        print(f"\nPattern 2 with key '{key}': {dec2}")
        print("  *** POSSIBLE MATCH ***")

# Try combinations - maybe pattern1 and pattern2 need to be interleaved after decryption?
print("\n" + "="*80)
print("TRYING INTERLEAVED DECRYPTION")
print("="*80)

# Try Caesar on both patterns and interleave
for shift1 in range(26):
    for shift2 in range(26):
        dec1 = caesar_decrypt(pattern1, shift1)
        dec2 = caesar_decrypt(pattern2, shift2)

        # Interleave them back
        interleaved = ''
        for i in range(max(len(dec1), len(dec2))):
            if i < len(dec1):
                interleaved += dec1[i]
            if i < len(dec2):
                interleaved += dec2[i]

        if any(word in interleaved.lower() for word in ['the', 'and', 'you', 'have', 'been', 'that']):
            print(f"\nShift1={shift1}, Shift2={shift2}:")
            print(interleaved)
            print("  *** POSSIBLE MATCH ***")
