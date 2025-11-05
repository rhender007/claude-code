#!/usr/bin/env python3
"""
Parse the result that starts with YOU
"""

encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"

letters = encrypted_spaced.split()
pattern1 = ''.join([letters[i] for i in range(0, len(letters), 2)])
pattern2 = ''.join([letters[i] for i in range(1, len(letters), 2)])

def caesar_decrypt(text, shift):
    return ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in text if c.isalpha())

# Shifts (1, 19)
dec1 = caesar_decrypt(pattern1, 1)
dec2 = caesar_decrypt(pattern2, 19)

interleaved = ''
for i in range(max(len(dec1), len(dec2))):
    if i < len(dec1):
        interleaved += dec1[i]
    if i < len(dec2):
        interleaved += dec2[i]

print("Result with shifts (1, 19):")
print(interleaved)
print()

# This starts with YOU - very promising!
# Let me try to manually parse it

text = interleaved

# Try adding spaces at likely word boundaries
print("="*80)
print("ATTEMPTING MANUAL WORD PARSING")
print("="*80)

# Start with YOU
if text.startswith('YOU'):
    print("Starts with: YOU")
    remaining = text[3:]
    print(f"Remaining: {remaining}")

    # Try common patterns after YOU
    # "YOU HAVE", "YOU ARE", "YOU CAN", "YOU WILL", etc.
    if remaining.startswith('H'):
        print("\nPossible: YOU H... (HAVE?)")
        if remaining[1:4] == 'IJI':
            print("  Doesn't match HAVE")

# Let me try a different approach - sliding window to find valid words
print("\n" + "="*80)
print("SLIDING WINDOW WORD DETECTION")
print("="*80)

common_words_dict = set([
    'you', 'the', 'and', 'for', 'are', 'but', 'not', 'all', 'can',
    'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him',
    'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see', 'two',
    'way', 'who', 'boy', 'did', 'end', 'let', 'put', 'say', 'too',
    'use', 'have', 'this', 'that', 'with', 'from', 'they', 'been',
    'were', 'said', 'each', 'which', 'their', 'would', 'could', 'about',
    'other', 'than', 'then', 'them', 'these', 'some', 'time', 'very',
    'when', 'come', 'made', 'find', 'like', 'long', 'make', 'many',
    'over', 'such', 'take', 'than', 'them', 'well', 'only', 'come',
    'made', 'find', 'give', 'call', 'came', 'show', 'every', 'thing',
    'think', 'great', 'where', 'after', 'never', 'under', 'might',
    'story', 'again', 'found', 'still', 'while', 'along', 'asked',
    'shall', 'those', 'until', 'right', 'place', 'being', 'going',
])

# Try to greedily match words
text_lower = text.lower()
pos = 0
parsed = []
word_count = 0

while pos < len(text_lower):
    found_word = False
    # Try longest words first
    for length in range(min(10, len(text_lower) - pos), 0, -1):
        word = text_lower[pos:pos+length]
        if word in common_words_dict:
            parsed.append(word)
            pos += length
            found_word = True
            word_count += 1
            break

    if not found_word:
        # Can't match a word, take one character
        parsed.append(text_lower[pos])
        pos += 1

result = ' '.join(parsed)
print(f"\nParsed result ({word_count} words found):")
print(result[:200])

if word_count > 5:
    print(f"\n*** LIKELY SOLUTION ***")
    print(f"Full text: {result}")

# Also try every Nth character starting from "YOU"
print("\n" + "="*80)
print("PATTERN EXTRACTION FROM 'YOU' RESULT")
print("="*80)

for step in range(3, 10):
    extracted = ''.join([text[i] for i in range(0, len(text), step)])
    print(f"\nEvery {step}th char: {extracted}")
    # Check if it's more readable
    words_found = []
    for word in ['YOU', 'THE', 'AND', 'HAVE', 'ARE']:
        if word in extracted:
            words_found.append(word)
    if words_found:
        print(f"  Contains: {words_found}")

# Maybe the "YOU" result just needs better spacing?
print("\n" + "="*80)
print("TRYING TO ADD INTELLIGENT SPACING")
print("="*80)

# Let me manually try to parse the beginning
manual_parse = "YOU "

rest = text[3:]
print(f"\nManually parsing: {manual_parse}")
print(f"Remaining: {rest[:50]}...")

# Look for patterns
# After YOU, common words: HAVE, ARE, CAN, WILL, SHOULD, WOULD, COULD, MUST
print("\nChecking common words after 'YOU':")
for word in ['HAVE', 'ARE', 'CAN', 'WILL', 'SHOULD', 'WOULD', 'COULD', 'MUST']:
    if rest.startswith(word):
        print(f"  Found: {word}")
        manual_parse += word
        break
