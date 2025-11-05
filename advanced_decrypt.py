#!/usr/bin/env python3
"""
Advanced decryption techniques
"""
import itertools

encrypted = "ZHVAJCJHKDFRHJHZMIRHJYRGFLNRHLJAJSHZEXOLDDOLRIAWLJRMAAZZTDVBIKUCDHEZEFRXXIHRKDUXEXFJDKVLRJXFOHJJQRRLEFJDCOXEJYBFEJHRDSEXXHMZOFWJFGMDSUCZXRLBHDLYQW"

def vigenere_decrypt(ciphertext, key):
    """Decrypt using Vigenère cipher"""
    key = key.upper()
    result = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
            key_index += 1
        else:
            result.append(char)

    return ''.join(result)

def rail_fence_decrypt(ciphertext, rails):
    """Decrypt Rail Fence cipher"""
    if rails == 1:
        return ciphertext

    fence = [['' for _ in range(len(ciphertext))] for _ in range(rails)]
    direction = -1
    row, col = 0, 0

    # Mark the positions
    for _ in range(len(ciphertext)):
        if row == 0 or row == rails - 1:
            direction *= -1
        fence[row][col] = '*'
        col += 1
        row += direction

    # Fill the fence with ciphertext
    index = 0
    for i in range(rails):
        for j in range(len(ciphertext)):
            if fence[i][j] == '*' and index < len(ciphertext):
                fence[i][j] = ciphertext[index]
                index += 1

    # Read the plaintext
    result = []
    row, col = 0, 0
    direction = -1
    for _ in range(len(ciphertext)):
        if row == 0 or row == rails - 1:
            direction *= -1
        result.append(fence[row][col])
        col += 1
        row += direction

    return ''.join(result)

def atbash_decrypt(text):
    """Atbash cipher (reverse alphabet)"""
    result = []
    for char in text:
        if char.isupper():
            result.append(chr(ord('Z') - (ord(char) - ord('A'))))
        elif char.islower():
            result.append(chr(ord('z') - (ord(char) - ord('a'))))
        else:
            result.append(char)
    return ''.join(result)

def reverse_text(text):
    """Simple reversal"""
    return text[::-1]

print("="*80)
print("TRYING VIGENÈRE CIPHER WITH COMMON KEYS")
print("="*80)

common_keys = ['KEY', 'CODE', 'SECRET', 'CIPHER', 'CRYPTO', 'PASSWORD', 'CYBER', 'COMMAND']
for key in common_keys:
    decrypted = vigenere_decrypt(encrypted, key)
    print(f"\nKey '{key}': {decrypted[:80]}...")
    # Check for common words
    if any(word in decrypted.lower() for word in ['the ', ' and ', ' for ', ' you ', ' have ', ' with ']):
        print(f"  *** POSSIBLE MATCH ***")
        print(f"  Full text: {decrypted}")

print("\n" + "="*80)
print("TRYING RAIL FENCE CIPHER")
print("="*80)

for rails in range(2, 6):
    decrypted = rail_fence_decrypt(encrypted, rails)
    print(f"\nRails {rails}: {decrypted[:80]}...")
    if any(word in decrypted.lower() for word in ['the ', ' and ', ' for ', ' you ', ' have ', ' with ']):
        print(f"  *** POSSIBLE MATCH ***")
        print(f"  Full text: {decrypted}")

print("\n" + "="*80)
print("TRYING ATBASH CIPHER")
print("="*80)

atbash_result = atbash_decrypt(encrypted)
print(f"Atbash: {atbash_result}")

if any(word in atbash_result.lower() for word in ['the ', ' and ', ' for ', ' you ', ' have ', ' with ']):
    print("  *** POSSIBLE MATCH ***")

print("\n" + "="*80)
print("TRYING REVERSE")
print("="*80)

reversed_result = reverse_text(encrypted)
print(f"Reversed: {reversed_result}")

print("\n" + "="*80)
print("TRYING ALTERNATING PATTERNS")
print("="*80)

# Try taking every 2nd letter starting from position 0
pattern1 = ''.join([encrypted[i] for i in range(0, len(encrypted), 2)])
print(f"Every 2nd letter (from 0): {pattern1}")

# Try taking every 2nd letter starting from position 1
pattern2 = ''.join([encrypted[i] for i in range(1, len(encrypted), 2)])
print(f"Every 2nd letter (from 1): {pattern2}")
