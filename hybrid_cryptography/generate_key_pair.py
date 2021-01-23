from Crypto.PublicKey import RSA

def create_key(filename, size):
    try:
        key = RSA.generate(int(size))
        f = open(filename+"_private.pem", "wb")
        f.write(key.exportKey('PEM'))
        f.close()

        pubkey = key.publickey()
        f = open(filename +"_public.pem", "wb")
        f.write(pubkey.exportKey('OpenSSH'))
        f.close()
        return "RSA Key created successfully"
    except Exception as e:
        return str(e)