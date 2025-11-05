#!/usr/bin/env python3
"""
Extract the most readable parts and try additional processing
"""

# Best result from shifts (16, 4)
best_text = "JDFWTYTDUZPNRFRVWEBDTUBCPHXNRHTWTORVOTYHNZYHBEKSVFBIKWJVDZFXSGEYNDOVPNJTHERNUZETOTPFNGFHBFHBYDTFANBHPFNYYTOFIXPATDBZCTRIJKPSTBQINOEYJTBHLDNHIMG"

print("Best decryption result:")
print(best_text)
print()

# The text contains "THER" which might be "THERE" or part of "ANOTHER" etc.
# Let me look at the context
print("Context around 'THER':")
idx = best_text.index('THER')
print(f"...{best_text[max(0,idx-10):min(len(best_text),idx+20)]}...")
print()

# Let me try additional Caesar shifts on this result
def caesar_shift(text, shift):
    return ''.join(chr((ord(c) - ord('A') + shift) % 26 + ord('A')) for c in text)

print("="*80)
print("TRYING ADDITIONAL CAESAR SHIFTS ON BEST RESULT")
print("="*80)

for shift in range(1, 26):
    shifted = caesar_shift(best_text, shift)
    # Check for very common words
    if 'THE ' in shifted or ' THE' in shifted or 'AND ' in shifted or ' AND' in shifted:
        print(f"\nShift +{shift}: {shifted[:100]}...")

# What if I need to reverse it?
print("\n" + "="*80)
print("TRYING REVERSAL")
print("="*80)

reversed_text = best_text[::-1]
print(f"Reversed: {reversed_text[:100]}...")

# Check for words in reversed
common = ['THE', 'AND', 'YOU', 'HAVE', 'THAT', 'WITH']
found = [w for w in common if w in reversed_text]
if found:
    print(f"Found in reversed: {found}")
    print(f"Full reversed: {reversed_text}")

# What if certain positions need different shifts?
# Let me try the "NJTHER" part specifically
print("\n" + "="*80)
print("ANALYZING 'NJTHER' SECTION")
print("="*80)

section = "DOVPNJTHERNUZETOTPFNGFHBFHBYDTFANBHP"
print(f"Section: {section}")

# Try shifting this section
for shift in range(26):
    shifted = caesar_shift(section, shift)
    if any(word in shifted for word in ['THE', 'AND', 'ANOTHER', 'NORTHERN', 'SOUTHERN']):
        print(f"\nShift +{shift}: {shifted}")

# Maybe the answer is actually in a specific format
print("\n" + "="*80)
print("CHECKING IF ANSWER IS A SPECIFIC FORMAT")
print("="*80)

# CTF flags often look like: flag{...}, CTF{...}, or just a phrase
# Let me see if there's a pattern

# What if I need to extract every Nth character?
for n in range(2, 10):
    extracted = ''.join([best_text[i] for i in range(0, len(best_text), n)])
    print(f"\nEvery {n}th character: {extracted}")
    if 'THE' in extracted or 'FLAG' in extracted:
        print("   *** Possible match! ***")

# Or first letter of every Nth group?
print("\n" + "="*80)
print("FIRST LETTER OF GROUPS")
print("="*80)

for group_size in range(3, 8):
    groups = [best_text[i:i+group_size] for i in range(0, len(best_text), group_size)]
    first_letters = ''.join([g[0] if g else '' for g in groups])
    print(f"\nGroup size {group_size}: {first_letters}")
    if len(first_letters) > 10:
        # Try Caesar on this
        for shift in range(26):
            shifted = caesar_shift(first_letters, shift)
            if 'THE' in shifted or 'CYBER' in shifted or 'COMMAND' in shifted:
                print(f"   Shift {shift}: {shifted}")

print("\n" + "="*80)
print("FINAL BEST GUESS")
print("="*80)
print(f"Text with shifts (16, 4):")
print(best_text)
print()
print("Most readable section:")
print("...NJTHERN... (possibly 'NORTHERN' or similar)")
