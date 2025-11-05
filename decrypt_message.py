#!/usr/bin/env python3
"""
Decrypt the encrypted message using various cipher techniques
"""

# The encrypted message (removing spaces between letters for analysis)
encrypted = "ZHVAJCJHKDFRHJHZMIRHJYRGFLNRHLJAJSHZEXOLDDOLRIAWLJRMAAZZTDVBIKUCDHEZEFRXXIHRKDUXEXFJDKVLRJXFOHJJQRRLEFJDCOXEJYBFEJHRDSEXXHMZOFWJFGMDSUCZXRLBHDLYQW"

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

def analyze_frequency(text):
    """Analyze character frequency"""
    freq = {}
    for char in text:
        if char.isalpha():
            freq[char] = freq.get(char, 0) + 1
    return dict(sorted(freq.items(), key=lambda x: x[1], reverse=True))

def print_all_caesar_shifts():
    """Try all 26 possible Caesar cipher shifts"""
    print("Trying all Caesar cipher shifts:\n")
    for shift in range(26):
        decrypted = caesar_decrypt(encrypted, shift)
        print(f"Shift {shift:2d}: {decrypted[:80]}...")
        # Check for common English words
        if any(word in decrypted.lower() for word in ['the', 'and', 'have', 'that', 'for', 'you', 'with']):
            print(f"  *** POSSIBLE MATCH (contains common words) ***")
        print()

def try_substitution_cipher():
    """Try to solve as a substitution cipher using frequency analysis"""
    print("\n" + "="*80)
    print("FREQUENCY ANALYSIS")
    print("="*80)

    # English letter frequency (most common to least)
    english_freq = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

    freq = analyze_frequency(encrypted)
    print("\nLetter frequencies in encrypted text:")
    for char, count in list(freq.items())[:10]:
        print(f"{char}: {count} ({count/len(encrypted)*100:.1f}%)")

    # Create a mapping based on frequency
    cipher_freq = ''.join(freq.keys())
    mapping = {}
    for i, cipher_char in enumerate(cipher_freq):
        if i < len(english_freq):
            mapping[cipher_char] = english_freq[i]

    # Decrypt using mapping
    result = ""
    for char in encrypted:
        result += mapping.get(char, char)

    print("\nAttempted decryption using frequency analysis:")
    print(result)
    return result

if __name__ == "__main__":
    print("ENCRYPTED MESSAGE:")
    print(encrypted)
    print(f"\nLength: {len(encrypted)} characters")
    print("\n" + "="*80)

    # Try Caesar cipher
    print_all_caesar_shifts()

    # Try frequency analysis
    try_substitution_cipher()
