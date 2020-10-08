import os, random, struct
from Crypto.Cipher import AES

def encrypt_file(key, file_path, file_name,  chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        file_path:
            Path of the input file

        file_name:
            Name of the input file

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    try: 
        out_filename = file_name.replace(".txt", "_C.txt")

        encryptor = AES.new(key.encode("utf8"), AES.MODE_ECB)

        with open(file_path, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b'0' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))
        
        return 0
    except:
        return 1

def decrypt_file(key, file_path, file_name):
    """ Decrypts a file using AES (CBC mode) with the
        given key. 
    """

    try:
        out_filename = file_name.replace(".txt", "_D.txt")

        with open(file_path, 'rb') as infile:
            read_bytes = infile.read()

        decryptor = AES.new(key.encode('utf8'), AES.MODE_ECB)
        decrypt_file = decryptor.decrypt(read_bytes)

        with open(out_filename, 'wb') as outfile:
            outfile.write(decrypt_file.rstrip(b'0'))

        return 0
    except:
        return 1