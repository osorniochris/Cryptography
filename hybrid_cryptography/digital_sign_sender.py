import binascii
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA

def sign_file(message_filename, privatekey_filename):
    try:
        #Archivo a firmar
        file = open(message_filename, 'rb')
        file_content = file.read().decode().encode("utf-8")

        #Se obtiene el HASH del contenido
        sha1 = SHA.new()
        sha1.update(file_content)

        #Llave privada RSA
        key = RSA.importKey(open(privatekey_filename, 'rb').read())
        signer = PKCS1_PSS.new(key)

        #Se crea la firma con RSA y la llave privada sobre el HASH
        signature = signer.sign(sha1)
        signatureHEX = binascii.hexlify(signature)

        #Archivo firmado
        signed_file = open(message_filename.replace(".txt", "_signed.txt"), 'wb')

        #Se agrega el contenido original y la firma
        signed_file.write(file_content + b"\n" + signatureHEX)
        return "File signed successfully!"
    except Exception as e:
        return "Something went wrong: " + str(e)
        


#Código ejemplo (corregido)

# message = 'To be signed'.encode('utf-8')
# key = RSA.importKey(open('private.pem').read())
# h = SHA.new()
# h.update(message)
# signer = PKCS1_PSS.new(key)
# signature = signer.sign(h)

# key = RSA.importKey(open('public.pem').read())
# h = SHA.new()
# h.update(message)
# verifier = PKCS1_PSS.new(key)
# if verifier.verify(h, signature):
#     print ("The signature is authentic.")
# else:
#     print ("The signature is not authentic.")