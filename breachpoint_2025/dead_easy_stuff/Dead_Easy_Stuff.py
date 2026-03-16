from Crypto.Cipher import DES
from Crypto.Util.Padding import pad

# Known DES weak key example (one of the 4 weak keys)
weak_key = bytes.fromhex('0101010101010101')

# Read plaintext from file (assume filename "plaintext.txt")
with open("Dead_Easy_Stuff (1).txt", "rb") as f:
    plaintext = f.read()

# Pad plaintext to 8-byte blocks
padded_text = pad(plaintext, 8)

# Create DES cipher in ECB mode with weak key
cipher = DES.new(weak_key, DES.MODE_ECB)

# Encrypt once
ciphertext = cipher.encrypt(padded_text)

with open("decoded.txt","wb") as f:
    f.write(ciphertext)
