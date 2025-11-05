#!/usr/bin/env python3
"""
Final decryption with ROT13 (shift 13)
"""

# The encrypted message (with original spacing)
encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"

# Remove spaces
encrypted = encrypted_spaced.replace(" ", "")

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

# Decrypt with shift 13 (ROT13)
decrypted = caesar_decrypt(encrypted, 13)

print("ENCRYPTED MESSAGE:")
print(encrypted_spaced)
print("\n" + "="*80)
print("\nDECRYPTED MESSAGE (ROT13 - Shift 13):")
print(decrypted)
print("\n" + "="*80)

# Try to make it more readable by adding spaces based on common words
words = []
i = 0
text = decrypted.lower()

# Common word patterns
common_starts = ['the', 'and', 'for', 'you', 'with', 'have', 'this', 'that', 'from', 'will', 'been', 'were', 'are']

print("\nAttempting to identify word boundaries:")
print(decrypted)
