#!/usr/bin/env python3
"""
Try variations of DEFENSE and double encryption
"""

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

def caesar_decrypt(text, shift):
    """Decrypt text using Caesar cipher with given shift"""
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - ascii_offset - shift) % 26 + ascii_offset)
        else:
            result += char
    return result

def check_for_common_words(text):
    """Check if text contains common English words"""
    text_lower = text.lower()
    common = ['the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'have', 'this', 'that', 'with', 'from', 'they', 'been', 'have', 'been', 'were', 'have']
    found = [word for word in common if ' ' + word + ' ' in ' ' + text_lower + ' ' or text_lower.startswith(word + ' ') or text_lower.endswith(' ' + word)]
    return found

print("="*80)
print("TRYING VARIATIONS OF 'DEFENSE' KEY")
print("="*80)

# Try related keywords
related_keys = ['DEFENSE', 'DEFENCE', 'DEFEND', 'DEFENSIVE', 'DEFENSES', 'NATIONAL', 'CYBERDEFENSE', 'SECURITY']

for key in related_keys:
    decrypted = vigenere_decrypt(encrypted, key)
    print(f"\nKey '{key}':")
    print(decrypted)
    words = check_for_common_words(decrypted)
    if words:
        print(f"  *** Found common words: {words} ***")

print("\n" + "="*80)
print("TRYING DOUBLE VIGENÈRE (DEFENSE then other keys)")
print("="*80)

# First decrypt with DEFENSE
intermediate = vigenere_decrypt(encrypted, 'DEFENSE')

# Then try other keys
second_keys = ['CYBER', 'COMMAND', 'KEY', 'CODE', 'SECRET', 'MILITARY', 'ALPHA', 'BRAVO']

for key2 in second_keys:
    decrypted = vigenere_decrypt(intermediate, key2)
    print(f"\nDEFENSE then '{key2}':")
    print(decrypted[:100] + "...")
    words = check_for_common_words(decrypted)
    if words:
        print(f"  *** Found common words: {words} ***")
        print(f"  FULL TEXT: {decrypted}")

print("\n" + "="*80)
print("TRYING VIGENÈRE (DEFENSE) + CAESAR")
print("="*80)

intermediate = vigenere_decrypt(encrypted, 'DEFENSE')

for shift in range(26):
    decrypted = caesar_decrypt(intermediate, shift)
    words = check_for_common_words(decrypted)
    if words or any(common in decrypted.lower() for common in ['the', 'and', 'for', 'you', 'have']):
        print(f"\nDEFENSE + Caesar shift {shift}:")
        print(decrypted)
        if words:
            print(f"  *** Found common words: {words} ***")

print("\n" + "="*80)
print("TRYING CAESAR + VIGENÈRE (DEFENSE)")
print("="*80)

for shift in range(26):
    intermediate = caesar_decrypt(encrypted, shift)
    decrypted = vigenere_decrypt(intermediate, 'DEFENSE')
    words = check_for_common_words(decrypted)
    if words or any(common in decrypted.lower() for common in ['the', 'and', 'for', 'you', 'have']):
        print(f"\nCaesar shift {shift} + DEFENSE:")
        print(decrypted)
        if words:
            print(f"  *** Found common words: {words} ***")
