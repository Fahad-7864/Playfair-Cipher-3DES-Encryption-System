# Part 2
import random

class DiffieHellman:
    # Initialize the Diffie-Hellman class with a prime number and a primitive root modulo prime.
    def __init__(self, prime, g):
        self.prime = prime  # The large prime number.
        self.g = g  # The base number, a primitive root modulo prime.
        self.private_key = None
        self.public_key = None
        self.shared_secret = None

    # Manually set the private key. Useful for when the private key is predetermined.
    def set_private_key(self, private_key):
        # Allow the user to manually set the private key
        self.private_key = private_key

    # Automatically generate a random private key less than the prime number if not already set.
    def generate_private_key(self):
        # The private key would be a random number less than the prime number
        if self.private_key is None:  # Check if the private key has not been manually set
            self.private_key = random.randint(1, self.prime - 1)
        return self.private_key

    # Generate the public key based on the private key and parameters (prime and g).
    def generate_public_key(self):
        if self.private_key is None:
            raise ValueError("Private key not set. Generate or set a private key first.")
        # Public key calculation using modular exponentiation:
        # (g^private_key) mod prime
        # This public key is then shared with the other party.
        self.public_key = pow(self.g, self.private_key, self.prime)
        return self.public_key

    def generate_shared_secret(self, other_public_key):
        # Generate the shared secret key
        if self.private_key is None:
            raise ValueError("Private key not set. Generate or set a private key first.")
        # Shared secret calculation using modular exponentiation:
        # (other_public_key^private_key) mod prime
        # This results in a shared secret that both parties can compute and use, 
        # but which cannot be derived from the public keys alone.
        self.shared_secret = pow(other_public_key, self.private_key, self.prime)
        return self.shared_secret


# User input their own values for prime and g
prime = int(input("Enter a prime number: "))  # For example, 23
g = int(input("Enter a primitive root modulo the prime number: "))  # For example, 5

# Party A creates their Diffie-Hellman instance
A = DiffieHellman(prime, g)
A_private_key = int(input("A, enter your private key: "))  
A.set_private_key(A_private_key)
A_public_key = A.generate_public_key()

# Party B creates their Diffie-Hellman instance
B = DiffieHellman(prime, g)
B_private_key = int(input("B, enter your private key: "))  
B.set_private_key(B_private_key)
B_public_key = B.generate_public_key()

# A and B exchange public keys and compute the shared secret
A_shared_secret = A.generate_shared_secret(B_public_key)
B_shared_secret = B.generate_shared_secret(A_public_key)

# Output the results
print("A's Private Key:", A_private_key)
print("A's Public Key:", A_public_key)
print("A's Shared Secret:", A_shared_secret)
print("B's Private Key:", B_private_key)
print("B's Public Key:", B_public_key)
print("B's Shared Secret:", B_shared_secret)

assert A_shared_secret == B_shared_secret, "The shared secrets do not match!"


from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import hashlib

#Hash the shared secret to derive a key suitable for 3DES.
def adjust_key_for_3des(shared_secret, bits=168):
    # Convert the shared_secret integer to a byte array. Adding 7 before dividing by 8 ensures any remainder
    # from the bit_length calculation is rounded up, thereby accounting for every part of a byte.
    # This process ensures that even a fractional byte is counted as a full byte in the final byte count.
    shared_secret_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, byteorder='big')
    # Hash the byte representation of shared_secret to produce a more random and suitable key.
    hashed = hashlib.sha256(shared_secret_bytes).digest()

    if bits == 112:
        key = hashed[:16]  # Get the first 16 bytes for a 112-bit key
        key += key[:8]     # Repeat the first 8 bytes to complete the key
    elif bits == 168:
        key = hashed[:21]  
        key += hashed[:3]  # Add 3 more bytes to complete the 24 bytes key
    else:
        raise ValueError("Unsupported key size. Only 112 and 168 bits are supported.")

    # Adjust the key parity to comply with DES3 requirements. DES3 keys require each byte's parity to be odd,
    # and this method sets the least significant bit of each byte to make the parity odd.
    return DES3.adjust_key_parity(key)

#Encrypt a message with 3DES using the specified mode.
def encrypt_3des(msg, key, mode='ECB'):
    if mode == 'ECB':
        cipher = DES3.new(key, DES3.MODE_ECB)
    elif mode == 'CFB':
        cipher = DES3.new(key, DES3.MODE_CFB)
    elif mode == 'CBC':
        cipher = DES3.new(key, DES3.MODE_CBC)
    else:
        raise ValueError("Unsupported mode")

    # Apply padding to ensure the message length is a multiple of the 8-byte block size required by 3DES.
    # Using 64 bit block size
    padding_length = 8 - len(msg) % 8
    msg += chr(padding_length) * padding_length
    ciphertext = cipher.encrypt(msg.encode('utf-8'))
    return (cipher.iv if mode != 'ECB' else None, ciphertext)  # Return IV only for CFB and CBC

#Decrypt a message with 3DES using the specified mode.
def decrypt_3des(iv, ciphertext, key, mode='ECB'):
    if mode == 'ECB':
        cipher = DES3.new(key, DES3.MODE_ECB)
    elif mode == 'CFB':
        cipher = DES3.new(key, DES3.MODE_CFB, iv=iv)
    elif mode == 'CBC':
        cipher = DES3.new(key, DES3.MODE_CBC, iv=iv)
    else:
        raise ValueError("Unsupported mode")

    plaintext = cipher.decrypt(ciphertext).decode('utf-8')
    # Remove padding to restore the original message length and content.
    padding_length = ord(plaintext[-1])
    return plaintext[:-padding_length]
    

print("Tripe DES section")
# Example usage
shared_secret = A_shared_secret  # or B_shared_secret, since they should be the same

key_size = int(input("Enter key size (112 or 168): "))
key = adjust_key_for_3des(shared_secret, key_size)


bytes_of_number = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8, 'big')
print("Int value fo shared key:" ,A_shared_secret)
print("Byte representation of shared secret:", bytes_of_number)

print ("Key" , key)

msg = input("Enter your message to encrypt: ")


# Encrypt and Decrypt using ECB mode
iv, ciphertext = encrypt_3des(msg, key, 'ECB')
print(f'ECB Cipher text: {ciphertext}')
plaintext = decrypt_3des(iv, ciphertext, key, 'ECB')
print(f'ECB Plain text: {plaintext}')

# Encrypt and Decrypt using CBC mode 
iv, ciphertext = encrypt_3des(msg, key, 'CBC')
print(f'CFB Cipher text: {ciphertext}')

plaintext = decrypt_3des(iv, ciphertext, key, 'CBC')
print(f'CBC Plain text: {plaintext}')

# Encrypt and Decrypt using CBC mode 
iv, ciphertext = encrypt_3des(msg, key, 'CFB')
print(f'CFB Cipher text: {ciphertext}')

plaintext = decrypt_3des(iv, ciphertext, key, 'CFB')
print(f'CFB Plain text: {plaintext}')

 