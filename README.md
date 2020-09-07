# HASHcrypt

### Multi-Key One-Time Pad Cipher
> Encrypts and decrypts messages using a character-value dictionary controlled by a user-defined random state and a securely-random decryption key unique to each encrypted message.

### Strengths
> The resulting ciphertext will be impossible to decrypt as long as:

 - The key is truly random (achieved in code).
 - The key is at least as long as the plaintext (achieved in code).
 - The key is never reused in whole or in part (achieved in code).
 - The key and random state are kept completely secret.

### Usage
#### Encryption:
 - Define a reproducible random state which dictates the character-value mapping
 - Enter a plaintext message
 - A securely-random key is generated
 - The character-value mapping converts these into lists of integers
 - XOR bitwise operation between these lists produces the cipher values
 - The cipher values are joined into a list as the encrypted message
 - The script returns the encrypted message and unique key
 
#### Decryption:
 - Enter the random state used to encrypt the original message
 - Enter the encrypted message
 - Enter the corresponding unique key
 - The character-value mapping converts the key into a list of integers
 - XOR bitwise operation between these lists produces the message values
 - The message values are converted into characters by the character-value mapping
 - The script returns the decrypted message
