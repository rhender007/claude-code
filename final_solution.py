#!/usr/bin/env python3
"""
Final solution attempt - try interpreting as different formats
"""

# Our best result so far
best_text = "JDFWTYTDUZPNRFRVWEBDTUBCPHXNRHTWTORVOTYHNZYHBEKSVFBIKWJVDZFXSGEYNDOVPNJTHERNUZETOTPFNGFHBFHBYDTFANBHPFNYYTOFIXPATDBZCTRIJKPSTBQINOEYJTBHLDNHIMG"

print("="*80)
print("CHECKING IF PLAINTEXT IS IN A SPECIAL FORMAT")
print("="*80)

# Try interpreting letters as numbers (A=1, B=2, etc.)
def letters_to_numbers(text):
    return [ord(c) - ord('A') + 1 for c in text if c.isalpha()]

numbers = letters_to_numbers(best_text)
print(f"\nAs numbers (A=1): {numbers[:20]}...")

# Check if numbers form coordinates or patterns
print(f"Sum: {sum(numbers)}")
print(f"Average: {sum(numbers)/len(numbers):.2f}")

# Try as hex pairs
try:
    hex_string = ''.join([best_text[i:i+2] for i in range(0, len(best_text), 2)])
    print(f"\nAs hex pairs: {hex_string[:50]}...")
except:
    pass

# Maybe it's actually a keyword or passphrase hidden in there
# Look for capitalization patterns or acrostics
first_letters = best_text[0]
print(f"\nFirst letter: {first_letters}")

# Try reading every 5th, 7th, etc. letter
for step in [5, 7, 11, 13]:
    extracted = ''.join([best_text[i] for i in range(0, len(best_text), step)])
    print(f"Every {step}th letter: {extracted}")

# What if I need to look at the ORIGINAL encrypted message pattern?
print("\n" + "="*80)
print("LOOKING AT ORIGINAL MESSAGE PATTERN")
print("="*80)

encrypted_spaced = "Z H V A J C J H K D F R H J H Z M I R H J Y R G F L N R H L J A J S H Z E X O L D D O L R I A W L J R M A A Z Z T D V B I K U C D H E Z F R Z X X I H R K D U X E X F J D K V L R J X F O H J J Q R R L F J D C O X E J Y B F E J H R D S X H M Z O F W J F G M D S U C Z X R L B H D L Y Q W"

# Maybe the answer is hidden in the spacing or structure?
letters = encrypted_spaced.split()
print(f"Number of letters: {len(letters)}")
print(f"First 10: {letters[:10]}")
print(f"Last 10: {letters[-10:]}")

# Maybe acrostic?
first_of_each = ''.join(letters)
print(f"\nAll letters concatenated: {first_of_each[:50]}...")

# Let me also check our best decryption one more time with better word detection
print("\n" + "="*80)
print("COMPREHENSIVE WORD SEARCH IN BEST RESULT")
print("="*80)

# Create all possible "words" of length 3-8
possible_words = []
for length in range(3, 9):
    for i in range(len(best_text) - length + 1):
        word = best_text[i:i+length]
        possible_words.append((i, word))

# Common English words to check
common_words = [
    'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU', 'ALL', 'CAN',
    'HER', 'WAS', 'ONE', 'OUR', 'OUT', 'DAY', 'GET', 'HAS', 'HIM',
    'HIS', 'HOW', 'ITS', 'MAY', 'NEW', 'NOW', 'OLD', 'SEE', 'TWO',
    'WAY', 'WHO', 'BOY', 'DID', 'HAVE', 'THIS', 'THAT', 'WITH',
    'FROM', 'THEY', 'BEEN', 'WERE', 'SAID', 'EACH', 'WHICH', 'THEIR',
    'WOULD', 'THESE', 'COULD', 'FIRST', 'AFTER', 'WHERE', 'THERE',
    'CYBER', 'COMMAND', 'CODE', 'FLAG', 'SECURITY', 'DEFENSE'
]

found_words = []
for idx, word in possible_words:
    if word in common_words:
        found_words.append((idx, word))

if found_words:
    print("\nFound words:")
    for idx, word in found_words:
        print(f"  Position {idx}: '{word}' in context: ...{best_text[max(0,idx-5):min(len(best_text),idx+len(word)+5)]}...")

# Final output
print("\n" + "="*80)
print("FINAL ANSWER CANDIDATES")
print("="*80)
print(f"\n1. Best decryption (shifts 16, 4):")
print(best_text)
print(f"\n2. First 50 chars: {best_text[:50]}")
print(f"\n3. Last 50 chars: {best_text[-50:]}")

# What if only part of it is the answer?
# Look for the most "readable" substring
best_substring_score = 0
best_substring = ""
best_substring_pos = 0

for length in range(20, 50):
    for i in range(len(best_text) - length):
        substring = best_text[i:i+length]
        # Score based on common letters
        score = sum([substring.count(c) for c in 'ETAOINSHRDLU'])
        if score > best_substring_score:
            best_substring_score = score
            best_substring = substring
            best_substring_pos = i

print(f"\n4. Most 'English-like' substring (position {best_substring_pos}):")
print(best_substring)

# Check if it contains readable phrases
if 'THER' in best_text:
    idx = best_text.index('THER')
    print(f"\n5. Around 'THER' (position {idx}):")
    print(best_text[max(0,idx-10):min(len(best_text),idx+30)])

print("\n" + "="*80)
print("If none of these work, the cipher might require additional context")
print("from the challenge page or a cipher type I haven't implemented.")
print("="*80)
