from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA

import binascii
import os
import sys
import tempfile

def encrypt(file_route, key_file):
    try:
        basename = os.path.basename(file_route)
        file = open(file_route, 'rb')
        file_content = file.read().decode().encode("utf-8")

        encrypted_file = open(basename.replace('.txt', '_e.txt'), 'wb')

        pubkey = RSA.import_key(open(key_file, 'rb').read())
        session_key =  get_random_bytes(16)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(pubkey)
        encrypted_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        encrypted_content, tag = cipher_aes.encrypt_and_digest(file_content)

        [ encrypted_file.write(x) for x in (encrypted_session_key, cipher_aes.nonce, tag, encrypted_content) ]
        encrypted_file.close()

        return "File encrypted"
    except Exception as e:
        return str(e)

def decrypt(file_route, key_file):
    try:
        basename = os.path.basename(file_route)
        encrypted_file = open(file_route, "rb")

        privkey = RSA.import_key(open(key_file).read())

        encrypted_session_key, nonce, tag, encrypted_content = \
        [ encrypted_file.read(x) for x in (privkey.size_in_bytes(), 16, 16, -1) ]

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(privkey)
        session_key = cipher_rsa.decrypt(encrypted_session_key)

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        decrypted_content = cipher_aes.decrypt_and_verify(encrypted_content, tag)

        decrypted_file = open(basename.replace("_e", "_d"), 'wb')
        decrypted_file.write(decrypted_content)
        decrypted_file.close()

        return "File decrypted"
    except Exception as e:
        return str(e)

def decrypt_and_verify(file_route, public_key_file, private_key_file):
    #try:
    basename = os.path.basename(file_route)
    encrypted_file = open(file_route, "rb")

        #import rsa key
    privkey = RSA.import_key(open(private_key_file).read())
    pubkey = RSA.import_key(open(public_key_file).read())

        #read session key and content
    encrypted_session_key, nonce, tag, encrypted_content = \
    [ encrypted_file.read(x) for x in (privkey.size_in_bytes(), 16, 16, -1) ]

        # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(privkey)
    session_key = cipher_rsa.decrypt(encrypted_session_key)

        # Decrypt the data with the AES session key
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    decrypted_content = cipher_aes.decrypt_and_verify(encrypted_content, tag)

    with tempfile.TemporaryFile() as fp:
        fp.write(decrypted_content) # Write a byte string using fp.write()
        fp.seek(0) # Go to the start of the file
        content = fp.readlines()
        last_line = content[-1] 

        #hash funtion applied to original content
    sha1 = SHA.new()
    sha1.update(b''.join(content).replace(b'\n'+last_line, b''))

        #return from hexadecimal format
    signature = binascii.unhexlify(last_line)

        #RSA public key
    verifier = PKCS1_PSS.new(pubkey)

    decrypted_file = open(basename.replace("_esigned", "_dverified"), 'wb')
    decrypted_file.write(b''.join(content).replace(b'\n'+last_line, b''))
    decrypted_file.close()

        #signature verification
    if verifier.verify(sha1, signature):
        return "The signature is authentic."
    else:
        return "The signature is not authentic."
    #except Exception as e:
    #    return str(e)
    
def encrypt_and_sign(file_route, public_key_file, private_key_file):
    try:
        basename = os.path.basename(file_route)
        file = open(file_route, 'rb')
        file_content = file.read().decode().encode("utf-8")

        #hash funtion applied
        sha1 = SHA.new()
        sha1.update(file_content)

        encrypted_file = open(basename.replace('.txt', '_esigned.txt'), 'wb')

        #import rsa key and random aes key is generated
        pubkey = RSA.import_key(open(public_key_file, 'rb').read())
        privkey = RSA.import_key(open(private_key_file, 'rb').read())
        session_key =  get_random_bytes(16)

        #private RSA key for signature
        signer = PKCS1_PSS.new(privkey)
        signature = signer.sign(sha1)
        signatureHEX = binascii.hexlify(signature)

        # Encrypt the session key with the public RSA key
        cipher_rsa = PKCS1_OAEP.new(pubkey)
        encrypted_session_key = cipher_rsa.encrypt(session_key)

        # Encrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX)
        encrypted_content, tag = cipher_aes.encrypt_and_digest(file_content+b"\n" + signatureHEX)

        [ encrypted_file.write(x) for x in (encrypted_session_key, cipher_aes.nonce, tag, encrypted_content) ]
        encrypted_file.close()

        return "Process completed successfully"
    except Exception as e:
        return str(e)