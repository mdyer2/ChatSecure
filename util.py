from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import os

# Key creation
key = os.urandom(32)

# Function to encrypt the message using AES cipher
def encrypt_message(message):
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(message.encode(), AES.block_size))
    return b64encode(iv + encrypted).decode()

# Function to decrypt the message using base64 and AES cipher
def decrypt_message(encrypted_message):
    encrypted_message = b64decode(encrypted_message)
    iv = encrypted_message[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_message[16:]), AES.block_size)
    return decrypted.decode()
