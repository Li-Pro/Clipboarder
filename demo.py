from hashlib import sha256
from pathlib import Path
import re
import time

from capture import getClipboardImage, NoImageData

PATHNAME_REGEX = re.compile(r'(\w+\.*)*\w')

def regexMatch(regex, s):
	return regex.fullmatch(s) != None

def imgChecksum(img):
	pixelSum = bytes()
	h, w = img.size
	for i in range(h):
		for j in range(w):
			pixelSum += bytes([img.getpixel((i, j))])
	
	hashval = sha256(pixelSum).digest()
	return (h, w, hashval)

def captureProc():
	return

def main():
	iwdir = input('Working directory: ')
	if not regexMatch(PATHNAME_REGEX, iwdir):
		raise Exception('Invalid directory name.')
	
	wdir = 'saves/' + iwdir + '/'
	Path(wdir).mkdir(parents=True, exist_ok=True)
	
	# Init workspace
	if Path(wdir + '.wdinfo').is_file():
		with open(wdir + '.wdinfo', 'r') as file:
			try:
				wdcnt = int(file.readline())
			except:
				raise Exception('Error while loading workspace.')	
	else:
		wdcnt = 0
	
	# Wait for input
	lstimg = None
	while True:
		try:
			img = getClipboardImage()
		except NoImageData:
			time.sleep(.1)
			continue
		else:
			chksum = imgChecksum(img)
			if chksum == lstimg:
				time.sleep(.1)
				continue
			
			img.save(wdir + str(wdcnt) + '.png')
			wdcnt += 1
			if wdcnt % 5 == 0:
				break
			else:
				lstimg = chksum
	
	with open(wdir + '.wdinfo', 'w') as file:
		file.write(str(wdcnt) + '\n')

main()