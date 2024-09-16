#Part 1 PlayFair Cipher

import string

# Convert numbers in a key to their corresponding letter representations.
def convert_numbers_in_key(key):
    # Simple mapping: 0 -> A, 1 -> B, and then the 10th letter goes back to 0
    conversion_map = {str(i): chr((i + 1) % 10 + 64) for i in range(10)}
    converted_key = "".join(conversion_map.get(char, char) for char in key)
    return converted_key

#Create the Playfair matrix from the given key, including conversion of numbers to letters."""
def create_playfair_matrix(key):
    matrix = ['' for _ in range(5)]
    seen = set()
    alphabet = string.ascii_lowercase.replace('j', 'i')
    
    # Convert numbers in the key to letters first
    key = convert_numbers_in_key(key.lower()).replace('j', 'i')
    
    combined = key + alphabet
    row, col = 0, 0
    
    for char in combined:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix[row] += char
            col += 1
            if col > 4:
                col = 0
                row += 1
            if row >= 5:  # Prevent row index from exceeding the matrix size
                break

    return matrix


# Process plaintext for Playfair encryption by splitting into bigrams.
def process_plaintext(plaintext):
    plaintext = plaintext.lower().replace(" ", "").replace('j', 'i')
    processed_text = []
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        if i+1 < len(plaintext):
            b = plaintext[i+1]
            if a == b:
                # Insert 'X' after the letter if next letter is the same to avoid duplicates in a bigram
                processed_text.append(a + 'x')
                i += 1  # Advance one letter only to insert 'X' after the duplicate
            else:
                processed_text.append(a + b)
                i += 2 # Increment index by 2 to jump to the next pair
        else:
            processed_text.append(a + 'x')  # Pad with 'X' if odd number of letters
            break
    return processed_text

# Encrypt a bigram using the Playfair cipher rules.
def encrypt_bigram(bigram, matrix):
    r1, c1, r2, c2 = [0] * 4 # Initialize row and column indices
    for i, row in enumerate(matrix):
        if bigram[0] in row:
            r1, c1 = i, row.index(bigram[0])
        if bigram[1] in row:
            r2, c2 = i, row.index(bigram[1])

    if r1 == r2:
        # If characters are in the same row, shift right
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        # If characters are in the same column, shift down
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        # If characters form a rectangle, swap the columns
        return matrix[r1][c2] + matrix[r2][c1]


# Encrypt plaintext using the Playfair cipher with the specified key.
def encrypt_playfair(plaintext, key):
    """Encrypt plaintext using the Playfair cipher."""
    matrix = create_playfair_matrix(key)
    processed_text = process_plaintext(plaintext)
    encrypted_text = ' '.join([encrypt_bigram(bigram, matrix) for bigram in processed_text]).upper()
    return encrypted_text


# Interactive user input
key_input = input("Enter the encryption key: ")
plaintext_input = input("Enter the plaintext to encrypt: ")
encrypted_text = encrypt_playfair(plaintext_input, key_input)
matrix = create_playfair_matrix(key_input)
generated_matrix_output = "Generated Matrix:\n" + "\n".join([' '.join(row) for row in matrix])
print(generated_matrix_output)
print("Encrypted text:", encrypted_text)



# Decrypt a bigram according to Playfair rules.
def decrypt_bigram(bigram, matrix):
    r1, c1, r2, c2 = [0] * 4
    # Locate each character of the bigram in the matrix
    for i, row in enumerate(matrix):
        if bigram[0] in row:
            r1, c1 = i, row.index(bigram[0])
        if bigram[1] in row:
            r2, c2 = i, row.index(bigram[1])

    # If characters are in the same row, shift left
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    # If characters are in the same column, shift up
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    # If characters form a rectangle, swap the columns
    else:
        return matrix[r1][c2] + matrix[r2][c1]

# Decrypt ciphertext using the Playfair cipher.
def decrypt_playfair(ciphertext, key):
    matrix = create_playfair_matrix(key)
    bigrams = ciphertext.lower().split()
    # Decrypt each bigram and join them into a single string
    decrypted_text = ''.join([decrypt_bigram(bigram, matrix) for bigram in bigrams])
    
    # Use the dedicated post-processing function
    final_text = post_process_decrypted_text(decrypted_text)
    return final_text


# Intelligently remove 'X's used for padding in decrypted text.
def post_process_decrypted_text(decrypted_text):
    final_text = ""
    i = 0
    while i < len(decrypted_text):
        # Handle the last character if it's 'X'
        if i == len(decrypted_text) - 1:
            if decrypted_text[i] != 'x':
                final_text += decrypted_text[i]
            break
        
        # Handle 'X' between identical letters or as padding
        if decrypted_text[i + 1] == 'x':
            if i + 2 < len(decrypted_text) and decrypted_text[i] == decrypted_text[i + 2]:
                final_text += decrypted_text[i]
                i += 2  # Move past the 'X' and the repeated character
            else:
                final_text += decrypted_text[i]
                i += 1  # Treat 'X' as part of the text if it's not separating identical letters
        else:
            # Include the character and move to the next
            final_text += decrypted_text[i]
            i += 1

    return final_text


# Interactive user input
key_input = input("Enter the decryption key: ")
ciphertext_input = input("Enter the ciphertext to decrypt (make sure to separate bigrams with spaces): ")
decrypted_text = decrypt_playfair(ciphertext_input, key_input)
print("Decrypted text:", decrypted_text)

# ask the user if they want to see the challenge code
user_input = input("Would you like to see the Playfair cipher with PRNG key? (yes/no): ")
if user_input.lower() == "yes":
    print("Generating Playfair cipher with PRNG key...")

else:
    print("Exiting program.")


import string
import random

# Generate a more secure key using a PRNG, seeded with a predetermined value.
def generate_prng_key_with_seed(seed):
    random.seed(seed)
    enhanced_key = ''
    seen = set()
    while len(enhanced_key) < 26:
        char = random.choice(string.ascii_lowercase)
        if char not in seen:
            seen.add(char)
            enhanced_key += char
    return enhanced_key
    
# Modified the create_playfair_matrix function to use the enhanced key directly
def create_playfair_matrix_with_enhanced_key(enhanced_key):
    matrix = ['' for _ in range(5)] # Initialize a 5x5 matrix
    seen = set()
    enhanced_key = enhanced_key.replace('j', 'i')
    combined = enhanced_key
    row, col = 0, 0
    
    for char in combined:
        if char not in seen and char.isalpha():
            seen.add(char) # Track characters to avoid duplicates
            matrix[row] += char
            col += 1
            if col > 4: # Move to the next row after 5 characters
                col = 0
                row += 1
            if row >= 5: # Prevent row index from exceeding the matrix size
                break
    return matrix


# Encrypt Playfair with the modified key generation
def encrypt_playfair(plaintext, seed):
    enhanced_key = generate_prng_key_with_seed(seed)
    matrix = create_playfair_matrix_with_enhanced_key(enhanced_key)
    processed_text = process_plaintext(plaintext)
    encrypted_text = ' '.join([encrypt_bigram(bigram, matrix) for bigram in processed_text]).upper()
    return encrypted_text

# Decrypt Playfair with the modified key generation
def decrypt_playfair(ciphertext, key):
    enhanced_key = generate_prng_key_with_seed(seed)
    matrix = create_playfair_matrix_with_enhanced_key(enhanced_key)
    bigrams = ciphertext.lower().split()
    decrypted_text = ''.join([decrypt_bigram(bigram, matrix) for bigram in bigrams])
    
    final_text = post_process_decrypted_text(decrypted_text)
    return final_text
    

# Example usage


seed = 23  # Predetermined seed
enhanced_key = generate_prng_key_with_seed(seed)
print("Enhanced Key:", enhanced_key)

# Use the enhanced key to create the Playfair matrix
matrix = create_playfair_matrix_with_enhanced_key(enhanced_key)
# print the generated matrix
generated_matrix_output = "Generated Matrix:\n" + "\n".join([' '.join(row) for row in matrix])
print(generated_matrix_output)
# Example usage
plaintext = input("Enter the plaintext to encrypt: ")
ciphertext = encrypt_playfair(plaintext, seed)
print("Encrypted Text:", ciphertext)

# To decrypt, you would use the same seed
decrypted_text = decrypt_playfair(ciphertext, seed)
print("Decrypted Text:", decrypted_text)




