from pathlib import Path
import re
import time

from capture import getClipboardImage, NoImageData

PATHNAME_REGEX = re.compile(r'(\w+\.*)*\w')

def regexMatch(regex, s):
	return regex.fullmatch(s) != None

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
	while True:
		try:
			img = getClipboardImage()
		except NoImageData:
			time.sleep(.1)
			continue
		else:
			img.save(wdir + str(wdcnt) + '.png')
			wdcnt += 1
			break
	
	with open(wdir + '.wdinfo', 'w') as file:
		file.write(str(wdcnt) + '\n')

main()