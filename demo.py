from pathlib import Path
import re
import time

from capture import getClipboardImage, NoImageData

PATHNAME_REGEX = re.compile(r'(\w+\.*)*\w')

def regexMatch(regex, s):
	return regex.fullmatch(s) != None

def imgCompare(img1, img2):
	if (not img1) or (not img2):
		return False
	
	h, w = img1.size
	if not img2.size == (h, w):
		return False
	
	for i in range(h):
		for j in range(w):
			if not img1.getpixel((i, j)) == img2.getpixel((i, j)):
				return False
	
	return True

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
			if imgCompare(img, lstimg):
				time.sleep(.2)
				continue
			img.save(wdir + str(wdcnt) + '.png')
			wdcnt += 1
			
			lstimg = img
	
	with open(wdir + '.wdinfo', 'w') as file:
		file.write(str(wdcnt) + '\n')

main()