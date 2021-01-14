import binascii
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

def check_signature(filename, publickey_filename):

    try:
        #Archivo a verificar
        file = open(filename, 'rb')
        file_content = file.read().decode().encode("utf-8")

        #Se obtiene la última línea (firma)
        lines = file_content.splitlines()
        last_line = lines[-1]

        #Se obtiene el contenido sin la firma
        first_part = file_content.replace(b"\n" + last_line, b'')

        #Se obtiene el HASH del contenido
        sha1 = SHA.new()
        sha1.update(first_part)

        #Se regresa de hexadecimal la firma
        signature = binascii.unhexlify(last_line)

        #Se usa RSA con la llave pública
        key = RSA.importKey(open(publickey_filename).read())
        verifier = PKCS1_PSS.new(key)

        #Se compara el HASH con la firma y RSA
        if verifier.verify(sha1, signature):
            return "The signature is authentic."
        else:
            return "The signature is not authentic."
    except Exception as e:
        return "Something went wrong: " + str(e)
        