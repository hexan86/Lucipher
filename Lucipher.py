"""
LUCIPHER
Author: Hexan
Date: 12/07/2025

Just for fun I've created this poly-alphabetic substitution cipher.
It isn't particularly 'secure', but it seems that this specific method has never been implemented before.
I was thinking to modify known methods for a while and the other day, after taking a class on Cryptography 
and talking about Cipher methods with the professor, I just put together some ideas and created Lucipher.
This is my first experiment with ciphers and I'm still learning python, so it's likely to have bugs or errors.

The inner mechanism is quite simple, to be honest: it takes the number of characters in the text and uses 
this value (SIRN, passed to IRN) to shift the characters, like a well known Caesar's cipher.
The difference is that for every following letter it shifts of another position: the first letter is shifted 
by the value of IRN, the second letter by IRN+1, the third letter by IRN+2 and so on.
On top of that, the second word is not following the same scheme, and the first letter is not shifted 
by IRN or IRN+x where x is the increasing value of the previous word, but is going back to IRN+1. 
At the same way the third word starts by shifting by IRN+2 and this goes for the full sentence. 

When a sentence ends, the IRN is set back to the starting value (stored in SIRN). I was going to implement 
a function to use the SIRN to increase even more the shifting for every sentence, like Shift=Sirn+Sirn 
or something similar, but it was giving me some hard time to create the decode function.
"""


import sys
import os

def get_sirn(text):
    # Calculate the Static Initial Rotation Number
    return len(text)

def encode(text):
    # Encode: use the SIRN as a starting point to calculate the shifting
    sirn = get_sirn(text)
    irn = sirn
    encoded_text = []
    word_count = 0


    # Find spaces to separate words and alter the shifting
    for i, char in enumerate(text):
        if char == ' ':
            word_count += 1
            irn = sirn + word_count  # Increment IRN for the next word
            encoded_text.append(char)
        elif char.isalpha():
            shift = irn + (i - sum(1 for c in text[:i] if c == ' '))  # Calculate shift based on position
            encoded_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A')) if char.isupper() else \
                           chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            encoded_text.append(encoded_char)
        else:
            encoded_text.append(char)  # Non-alphabetic characters remain unchanged

    return ''.join(encoded_text)

def decode(text):
    # Decode: use the SIRN to shift back the text 
    sirn = get_sirn(text)
    irn = sirn
    decoded_text = []
    word_count = 0

    for i, char in enumerate(text):
        if char == ' ':
            word_count += 1
            irn = sirn + word_count  # Increment IRN for the next word
            decoded_text.append(char)
        elif char.isalpha():
            shift = -(irn + (i - sum(1 for c in text[:i] if c == ' ')))  # Calculate shift based on position
            decoded_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A')) if char.isupper() else \
                           chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            decoded_text.append(decoded_char)
        else:
            decoded_text.append(char)  # Non-alphabetic characters remain unchanged

    return ''.join(decoded_text)

def main():
    if len(sys.argv) != 3:
        print("Usage: lucipher -e|-d <file>")
        sys.exit(1)

    mode = sys.argv[1]
    filename = sys.argv[2]

    if not os.path.isfile(filename):
        print(f"File {filename} does not exist.")
        sys.exit(1)

    with open(filename, 'r') as file:
        text = file.read()

    if mode == '-e':
        encoded_text = encode(text)
        with open(filename + '.enc', 'w') as file:
            file.write(encoded_text)
        print(f"Encoded text written to {filename}.enc")
    elif mode == '-d':
        decoded_text = decode(text)
        with open(filename + '.dec', 'w') as file:
            file.write(decoded_text)
        print(f"Decoded text written to {filename}.dec")
    else:
        print("Invalid mode. Use -e to encode or -d to decode.")
        sys.exit(1)

if __name__ == "__main__":
    main()
