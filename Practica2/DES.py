from PIL import Image 
from Crypto.Cipher import DES

ENCRYPT = 0
DECRYPT = 1

ECB = 'ecb'
CBC = 'cbc'
CFB = 'cfb'
OFB = 'ofb'

def convert_to_RGB(data): 
    r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data)) if i % 3 == d], [0, 1, 2])) 
    pixels = tuple(zip(r,g,b)) 
    return pixels

#action: ENCRYPT/DECRYPT
#method: ECB/CBC/CFB/OFB
def des(key, image_path, action, method):
	image = Image.open(image_path)
	image_content = image.convert("RGB").tobytes()

	final_image_name = ''
	final_content = None
	cipher = None

	if method == ECB:
		cipher = DES.new(key, DES.MODE_ECB)

	elif method == CBC:
		cipher = DES.new(key, DES.MODE_CBC)

	elif method == CFB:
		cipher = DES.new(key, DES.MODE_CFB)

	elif method == OFB:
		cipher = DES.new(key, DES.MODE_OFB, image_content[:DES.block_size])


	if action == ENCRYPT:
		final_image_name = image_path.replace('.bmp', '_' + method + '.bmp')

		if method == OFB:
			final_content = convert_to_RGB(cipher.iv + cipher.encrypt(image_content[DES.block_size:]))

		else:
			final_content = convert_to_RGB(cipher.encrypt(image_content))

	elif action == DECRYPT:
		final_image_name = image_path.replace('.bmp', '_d.bmp')

		if method == OFB:
			final_content = convert_to_RGB(cipher.iv + cipher.decrypt(image_content[DES.block_size:]))

		else:
			final_content = convert_to_RGB(cipher.decrypt(image_content))

	final_image = Image.new(image.mode, image.size)
	final_image.putdata(final_content)

	final_image.save(final_image_name, "BMP")
