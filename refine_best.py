#!/usr/bin/env python3
"""
Refine the best candidate
"""

encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"

letters = encrypted_spaced.split()
pattern1 = ''.join([letters[i] for i in range(0, len(letters), 2)])
pattern2 = ''.join([letters[i] for i in range(1, len(letters), 2)])

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in text if c.isalpha())

# Best candidate so far: (16, 4)
dec1 = caesar_decrypt(pattern1, 16)
dec2 = caesar_decrypt(pattern2, 4)

interleaved = ''
for i in range(max(len(dec1), len(dec2))):
    if i < len(dec1):
        interleaved += dec1[i]
    if i < len(dec2):
        interleaved += dec2[i]

print("Best candidate (16, 4):")
print(interleaved)
print()

# Try applying another Caesar shift to the whole thing
print("Applying additional Caesar shifts:")
for extra_shift in range(26):
    result = caesar_decrypt(interleaved, extra_shift)
    # Check for common English words
    common = ['THE ', ' THE', 'AND ', ' AND', 'HAVE ', 'THAT ', 'WITH ', 'FROM ',
              'THIS ', 'BEEN ', 'HAVE', 'WERE', 'WILL', 'YOUR', 'WHAT', 'WHEN',
              'THERE', 'THEIR', 'WHICH', 'WOULD', 'COULD', 'ABOUT', 'OTHER',
              'PEOPLE', 'BECAUSE', 'THROUGH', 'SHOULD', 'AFTER', 'BEFORE']

    # Add spaces to check
    result_spaced = ' ' + result + ' '
    found = []
    for word in common:
        if word in result_spaced.upper():
            found.append(word.strip())

    if found or 'CYBER' in result or 'COMMAND' in result or 'DECRYPT' in result:
        print(f"\nExtra shift {extra_shift}: {result}")
        if found:
            print(f"   Found: {found}")

# Try frequency analysis substitution on the best result
print("\n" + "="*80)
print("FREQUENCY ANALYSIS ON BEST CANDIDATE")
print("="*80)

from collections import Counter
freq = Counter(interleaved)
print("Letter frequencies:")
for letter, count in freq.most_common(10):
    print(f"  {letter}: {count}")

# English letter frequency: E T A O I N S H R D L C U M W F G Y P B V K J X Q Z
# Try manual substitutions based on this

# Looking at the text: JDFWTYTDUZPNRFRVWEBDTUBCPHXNRHTWTORVOTYHNZYHBEKSVFBIKWJVDZFXSGEYNDOVPNJTHERNUZETOTPFNGFHBFHBYDTFANBHPFNYYTOFIXPATDBZCTRIJKPSTBQINOEYJTBHLDNHIMG

# It has "THER" which is likely "THERE" or part of "THERE"
# Let's see if THERN could be a word...
# Maybe NJTHERN is actually a phrase?

# Let me try substituting based on patterns
text = interleaved

# Look for repeated patterns
print("\nLooking for repeated 3-letter+ sequences:")
for length in range(3, 6):
    seen = {}
    for i in range(len(text) - length):
        substring = text[i:i+length]
        if substring in seen:
            seen[substring] += 1
        else:
            seen[substring] = 1

    repeats = {k: v for k, v in seen.items() if v > 1}
    if repeats:
        print(f"\n{length}-letter repeats: {repeats}")

# Let me manually try to decode around "THER"
print("\n" + "="*80)
print("CONTEXT AROUND 'THER':")
print("="*80)

idx = interleaved.index('THER')
print(f"Full context: {interleaved[max(0, idx-20):min(len(interleaved), idx+30)]}")

# What if I try different shift combinations around this area?
# Actually, let me see if I can use a dictionary to find valid words

# Print with spaces every N characters to see patterns
print("\n" + "="*80)
print("WITH SPACING EVERY 5 CHARS:")
print("="*80)

spaced = ' '.join([interleaved[i:i+5] for i in range(0, len(interleaved), 5)])
print(spaced)
