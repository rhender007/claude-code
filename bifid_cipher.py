#!/usr/bin/env python3
"""
Try Bifid cipher decryption
"""

encrypted = "ZHVAJCJHKDFRHJHZMIRHJYRGFLNRHLJAJSHZEXOLDDOLRIAWLJRMAAZZTDVBIKUCDHEZEFRXXIHRKDUXEXFJDKVLRJXFOHJJQRRLEFJDCOXEJYBFEJHRDSEXXHMZOFWJFGMDSUCZXRLBHDLYQW"

def generate_polybius_square(key=""):
    """Generate 5x5 Polybius square from keyword"""
    key = key.upper().replace('J', 'I')
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # I/J combined

    # Remove duplicates from key
    seen = set()
    chars = []
    for char in key:
        if char not in seen and char in alphabet:
            seen.add(char)
            chars.append(char)

    # Add remaining letters
    for char in alphabet:
        if char not in seen:
            chars.append(char)

    # Create 5x5 grid
    grid = []
    for i in range(5):
        grid.append(chars[i*5:(i+1)*5])

    # Create lookup dictionaries
    char_to_pos = {}
    pos_to_char = {}
    for i, row in enumerate(grid):
        for j, char in enumerate(row):
            char_to_pos[char] = (i, j)
            pos_to_char[(i, j)] = char

    return grid, char_to_pos, pos_to_char

def bifid_decrypt(ciphertext, key="", period=5):
    """Decrypt using Bifid cipher"""
    ciphertext = ciphertext.upper().replace('J', 'I')
    grid, char_to_pos, pos_to_char = generate_polybius_square(key)

    # Split into periods
    result = []
    for block_start in range(0, len(ciphertext), period):
        block = ciphertext[block_start:block_start + period]

        # Get positions
        rows = []
        cols = []
        for char in block:
            if char in char_to_pos:
                r, c = char_to_pos[char]
                rows.append(r)
                cols.append(c)

        # Combine rows and cols
        combined = rows + cols

        # Split back and decrypt
        mid = len(combined) // 2
        for i in range(mid):
            r = combined[i]
            c = combined[mid + i]
            if (r, c) in pos_to_char:
                result.append(pos_to_char[(r, c)])

    return ''.join(result)

print("="*80)
print("BIFID CIPHER DECRYPTION")
print("="*80)

# Try different keys and periods
keys = ['', 'DEFENSE', 'CYBER', 'COMMAND', 'SECRET', 'KEY']
periods = [3, 4, 5, 6, 7, 8, 10]

for key in keys:
    for period in periods:
        decrypted = bifid_decrypt(encrypted, key, period)

        # Check for English words
        common_words = ['THE', 'AND', 'YOU', 'FOR', 'ARE', 'HAVE', 'THAT', 'WITH', 'THIS']
        found = [w for w in common_words if w in decrypted]

        if found:
            print(f"\nKey: '{key}', Period: {period}")
            print(f"Found words: {found}")
            print(f"Text: {decrypted}")

# Also try with no keyword but different periods
print("\n" + "="*80)
print("TRYING VARIOUS PERIODS (no keyword)")
print("="*80)

for period in range(2, 20):
    decrypted = bifid_decrypt(encrypted, "", period)
    # Just show first few to check
    if 'THE' in decrypted or 'AND' in decrypted:
        print(f"\nPeriod {period}: {decrypted[:100]}...")
        print(f"Full: {decrypted}")
