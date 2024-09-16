# Playfair-Cipher and 3DES-Encryption-System

This project demonstrates two cryptographic systems implemented using Python: the **Playfair Cipher** with added security features, and the **Diffie-Hellman key exchange** with **Triple DES (3DES)** for secure communication. Both encryption and decryption functionalities are included, ensuring secure data transmission and confidentiality.

## Part 1: Playfair Cipher

The Playfair Cipher implementation in this project enhances security by converting numbers in the encryption key into letter representations. Additionally, a **pseudorandom number generator (PRNG)** is used to generate a more secure encryption key based on a seed. The Playfair cipher is designed to process and encrypt text, split into bigrams, and apply encryption rules based on a 5x5 matrix.

### Features
- **Customisable Playfair Matrix:** Create the cipher matrix from any key, including number-to-letter conversion.
- **Bigram Processing:** Handles duplicate letters and inserts padding where necessary to encrypt text efficiently.
- **PRNG Integration:** Generates a more secure encryption key using a seeded pseudorandom number generator.


## Part 2: Diffie-Hellman Key Exchange with Triple DES (3DES)

This part implements the **Diffie-Hellman key exchange** algorithm to securely generate a shared secret between two parties. Once the shared secret is established, **Triple DES (3DES)** encryption is used to encrypt and decrypt messages using this shared key. Different modes like **ECB**, **CFB**, and **CBC** are supported for encryption.

### Features
- **Diffie-Hellman Key Exchange:** Securely generates a shared secret using a large prime number and a primitive root.
- **Triple DES (3DES) Encryption:** Encrypts and decrypts messages using a shared secret key in multiple modes (ECB, CFB, CBC).
- **Key Adjustments for 3DES:** The shared secret is hashed and adjusted to meet 3DES key requirements (112-bit or 168-bit keys).
## Technologies Used
- **Python**
- **Diffie-Hellman Algorithm**
- **Crypto.Cipher (PyCryptodome)** for 3DES encryption and decryption
- **Hashlib** for key adjustment

## How to Run the Project

1. Clone the repository:
    ```bash
    git clone https://github.com/Fahad-7864/Playfair-Cipher-3DES-Encryption-System/tree/main
    ```

2. Install required dependencies:
    ```bash
    pip install pycryptodome
    ```

3. Run the Playfair Cipher:
    ```bash
    python playfair_cipher.py
    ```

4. Run the Diffie-Hellman with 3DES:
    ```bash
    python diffie_hellman_3des.py
    ```

## Project Structure
- **playfair_cipher.py**: Script for Playfair Cipher encryption and decryption with PRNG integration.
- **diffie_hellman_3des.py**: Script for Diffie-Hellman key exchange and Triple DES encryption.
