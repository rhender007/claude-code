#!/usr/bin/env python3
"""
Comprehensive decryption attempt with multiple strategies
"""
import random
from collections import Counter

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
            key_index += 1
        else:
            result.append(char)
    return ''.join(result)

def score_english(text):
    """Score text for English-likeness"""
    score = 0
    text_upper = text.upper()

    # Common words
    common_words = ['THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
                    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM',
                    'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO',
                    'WAY', 'WHO', 'BOY', 'DID', 'HAVE', 'THIS', 'THAT', 'WITH',
                    'FROM', 'THEY', 'BEEN', 'WERE', 'WILL', 'MORE', 'WHEN', 'THERE',
                    'THEIR', 'WOULD', 'ABOUT', 'COULD', 'WHICH']

    for word in common_words:
        score += text_upper.count(word) * len(word) * 10

    # Common bigrams
    bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ON', 'AT', 'EN', 'ND', 'TO', 'ES', 'OR', 'TE', 'OF']
    for bigram in bigrams:
        score += text_upper.count(bigram) * 2

    # Common trigrams
    trigrams = ['THE', 'AND', 'THA', 'ENT', 'FOR']
    for trigram in trigrams:
        score += text_upper.count(trigram) * 3

    return score

print("="*80)
print("VIGENÈRE CIPHER - EXTENSIVE KEYWORD TESTING")
print("="*80)

# Extensive keyword list
keywords = [
    # Cyber/Military terms
    'CYBER', 'COMMAND', 'CYBERCOMMAND', 'MILITARY', 'SECURITY', 'DEFENSE',
    'ARMY', 'NAVY', 'FORCE', 'INTEL', 'AGENT', 'MISSION', 'OPERATION',
    'ALPHA', 'BRAVO', 'CHARLIE', 'DELTA', 'ECHO', 'FOXTROT',
    # Common cipher keys
    'KEY', 'CODE', 'SECRET', 'CIPHER', 'CRYPTO', 'PASSWORD', 'PASS',
    'ENCRYPTION', 'DECRYPT', 'DECODE', 'ENCODED', 'CRYPTOGRAPHY',
    # Tech terms
    'COMPUTER', 'NETWORK', 'SYSTEM', 'SERVER', 'DATA', 'PROTOCOL',
    # Other
    'EAGLE', 'FALCON', 'HAWK', 'SHIELD', 'SWORD', 'WARRIOR', 'GUARDIAN',
    'FLAG', 'CAPTURE', 'CTF', 'CHALLENGE', 'HACK', 'HACKER', 'PENETRATION'
]

best_score = 0
best_result = ""
best_key = ""

for key in keywords:
    decrypted = vigenere_decrypt(encrypted, key)
    score = score_english(decrypted)

    if score > best_score:
        best_score = score
        best_result = decrypted
        best_key = key
        print(f"\n*** NEW BEST: Key '{key}' (score: {score}) ***")
        print(f"Text: {decrypted}")

    # Also show any result with score > 50
    elif score > 50:
        print(f"\nKey '{key}' (score: {score}):")
        print(f"{decrypted[:100]}...")

print("\n" + "="*80)
print("BEST VIGENÈRE RESULT")
print("="*80)
print(f"Key: {best_key}")
print(f"Score: {best_score}")
print(f"Decrypted: {best_result}")

# Try Columnar Transposition with different column counts
print("\n" + "="*80)
print("COLUMNAR TRANSPOSITION")
print("="*80)

def columnar_decrypt(text, cols):
    """Simple columnar transposition decrypt"""
    rows = len(text) // cols + (1 if len(text) % cols else 0)
    grid = [[''] * cols for _ in range(rows)]

    idx = 0
    for col in range(cols):
        for row in range(rows):
            if idx < len(text):
                grid[row][col] = text[idx]
                idx += 1

    result = ''.join([''.join(row) for row in grid])
    return result

for num_cols in range(2, 15):
    decrypted = columnar_decrypt(encrypted, num_cols)
    score = score_english(decrypted)
    if score > 30:
        print(f"\nColumns {num_cols} (score: {score}):")
        print(f"{decrypted[:100]}...")

# Try Playfair-style approach (digraph substitution)
print("\n" + "="*80)
print("CHECKING FOR DIGRAPH PATTERNS")
print("="*80)

# Extract digraphs
digraphs = [encrypted[i:i+2] for i in range(0, len(encrypted)-1, 2)]
print(f"Number of digraphs: {len(digraphs)}")
print(f"Unique digraphs: {len(set(digraphs))}")
print(f"Most common digraphs: {Counter(digraphs).most_common(10)}")
