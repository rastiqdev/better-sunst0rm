import wiki
from remotezip import RemoteZip

def get_keys(identifier, board, buildid):
	try:
		f = wiki.get_firmware_keys(identifier, board, buildid)
	except Exception:
		if input(f"[?] Keys not found for this IPSW ({buildid}) for the board {board}. Do you want to enter keys manually? (y/n) ") == "y":
			iBSS_iv = input("  - Enter the iBSS IV: ")
			iBSS_key = input("  - Enter the iBSS Key: ")
			iBEC_iv = input("  - Enter the iBEC IV: ")
			iBEC_key = input("  - Enter the iBEC Key: ")
			return iBSS_iv, iBSS_key, iBEC_iv, iBEC_key
		else:
			exit()
		print("Requesting keys...")
	
	iBSS_iv = f['iBSSIV']
	iBSS_key = f['iBSSKey']
	iBEC_iv = f['iBECIV']
	iBEC_key = f['iBECKey']

	try:
		return iBSS_iv, iBSS_key, iBEC_iv, iBEC_key
	except UnboundLocalError:
		print("[WARNING] Unable to get firmware keys, either the bootchain is not encrypted or theapplewiki.com does not have it.")
		input("Continue or not? (Press ENTER to continue, Ctrl-C to quit)")

def partialzip_download(url, file, dest):
	with RemoteZip(url) as zip:
		data = zip.read(file)
	with open(dest, 'wb') as f:
		f.write(data)