#!/usr/bin/env python3

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

print("="*80)
print("Shift 13:")
print(caesar_decrypt(encrypted, 13))
print("\n" + "="*80)
print("Shift 23:")
print(caesar_decrypt(encrypted, 23))
print("\n" + "="*80)

# Let me also try all shifts and look for readable text manually
for i in range(26):
    decrypted = caesar_decrypt(encrypted, i)
    print(f"\nShift {i:2d}: {decrypted}")
