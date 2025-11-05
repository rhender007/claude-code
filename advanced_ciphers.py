#!/usr/bin/env python3
"""
Try more advanced cipher types
"""

encrypted = "ZHVAJCJHKDFRHJHZMIRHJYRGFLNRHLJAJSHZEXOLDDOLRIAWLJRMAAZZTDVBIKUCDHEZEFRXXIHRKDUXEXFJDKVLRJXFOHJJQRRLEFJDCOXEJYBFEJHRDSEXXHMZOFWJFGMDSUCZXRLBHDLYQW"

# Let's try Playfair with common keywords
def generate_playfair_matrix(key):
    """Generate 5x5 Playfair matrix from keyword"""
    key = key.upper().replace('J', 'I')
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # I/J combined

    # Remove duplicates from key
    seen = set()
    key_unique = []
    for char in key:
        if char not in seen and char in alphabet:
            seen.add(char)
            key_unique.append(char)

    # Add remaining letters
    for char in alphabet:
        if char not in seen:
            key_unique.append(char)

    # Create 5x5 matrix
    matrix = []
    for i in range(5):
        matrix.append(key_unique[i*5:(i+1)*5])

    return matrix

def find_position(matrix, char):
    """Find position of character in Playfair matrix"""
    char = char.upper().replace('J', 'I')
    for i, row in enumerate(matrix):
        for j, c in enumerate(row):
            if c == char:
                return (i, j)
    return None

def playfair_decrypt(ciphertext, key):
    """Decrypt using Playfair cipher"""
    matrix = generate_playfair_matrix(key)
    ciphertext = ciphertext.upper().replace('J', 'I')

    # Split into digraphs
    pairs = [ciphertext[i:i+2] for i in range(0, len(ciphertext)-1, 2)]
    if len(ciphertext) % 2 == 1:
        pairs.append(ciphertext[-1] + 'X')

    result = []
    for pair in pairs:
        if len(pair) == 2:
            pos1 = find_position(matrix, pair[0])
            pos2 = find_position(matrix, pair[1])

            if pos1 and pos2:
                row1, col1 = pos1
                row2, col2 = pos2

                if row1 == row2:  # Same row
                    result.append(matrix[row1][(col1-1) % 5])
                    result.append(matrix[row2][(col2-1) % 5])
                elif col1 == col2:  # Same column
                    result.append(matrix[(row1-1) % 5][col1])
                    result.append(matrix[(row2-1) % 5][col2])
                else:  # Rectangle
                    result.append(matrix[row1][col2])
                    result.append(matrix[row2][col1])

    return ''.join(result)

print("="*80)
print("PLAYFAIR CIPHER")
print("="*80)

playfair_keys = ['DEFENSE', 'CYBER', 'COMMAND', 'SECRET', 'KEYWORD', 'CRYPTOGRAPHY', 'SECURITY']

for key in playfair_keys:
    decrypted = playfair_decrypt(encrypted, key)
    print(f"\nKey '{key}':")
    print(decrypted)
    if any(word in decrypted.lower() for word in ['the', 'and', 'for', 'have', 'that', 'with']):
        print("  *** POSSIBLE MATCH ***")

# Try simple transposition - maybe it's written backwards or in columns
print("\n" + "="*80)
print("SIMPLE TRANSFORMATIONS")
print("="*80)

# Reverse
print("\nReversed:")
print(encrypted[::-1])

# Reverse pairs
pairs = [encrypted[i:i+2] for i in range(0, len(encrypted), 2)]
reversed_pairs = [p[::-1] for p in pairs]
print("\nReversed pairs:")
print(''.join(reversed_pairs))

# Swap adjacent letters
swapped = []
for i in range(0, len(encrypted)-1, 2):
    swapped.append(encrypted[i+1])
    swapped.append(encrypted[i])
if len(encrypted) % 2 == 1:
    swapped.append(encrypted[-1])
print("\nSwapped adjacent letters:")
print(''.join(swapped))

# Try Beaufort cipher (related to Vigenère)
def beaufort_decrypt(ciphertext, key):
    """Beaufort cipher decryption"""
    key = key.upper()
    result = []
    for i, char in enumerate(ciphertext):
        if char.isalpha():
            key_char = key[i % len(key)]
            result.append(chr((ord(key_char) - ord(char)) % 26 + ord('A')))
        else:
            result.append(char)
    return ''.join(result)

print("\n" + "="*80)
print("BEAUFORT CIPHER")
print("="*80)

for key in ['DEFENSE', 'CYBER', 'COMMAND', 'SECRET']:
    decrypted = beaufort_decrypt(encrypted, key)
    print(f"\nKey '{key}':")
    print(decrypted[:100] + "...")
    if any(word in decrypted.lower() for word in ['the', 'and', 'for', 'have']):
        print(f"  *** POSSIBLE MATCH ***")
        print(f"Full text: {decrypted}")

# Try Autokey cipher
def autokey_decrypt(ciphertext, key):
    """Autokey cipher decryption"""
    key = key.upper()
    result = []
    full_key = key

    for i, char in enumerate(ciphertext):
        if char.isalpha():
            if i < len(full_key):
                shift = ord(full_key[i]) - ord('A')
            else:
                shift = ord(full_key[i]) - ord('A')

            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            result.append(decrypted_char)
            full_key += decrypted_char
        else:
            result.append(char)

    return ''.join(result)

print("\n" + "="*80)
print("AUTOKEY CIPHER")
print("="*80)

for key in ['DEFENSE', 'CYBER', 'COMMAND', 'SECRET']:
    decrypted = autokey_decrypt(encrypted, key)
    print(f"\nKey '{key}':")
    print(decrypted[:100] + "...")
    if any(word in decrypted.lower() for word in ['the', 'and', 'for', 'have']):
        print(f"  *** POSSIBLE MATCH ***")
        print(f"Full text: {decrypted}")
