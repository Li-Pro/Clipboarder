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
	
	return img1.tobytes() == img2.tobytes()

def main():
	iwdir = input('Working directory: ')
	if not regexMatch(PATHNAME_REGEX, iwdir):
		raise Exception('Invalid directory name.')
	
	wdir = Path('saves') / iwdir
	wdir.mkdir(parents=True, exist_ok=True)
	
	## Init workspace
	wdinfo = Path(wdir) / '.wdinfo'
	if wdinfo.is_file():
		with wdinfo.open() as file:
			try:
				wdcnt = int(file.readline())
			except:
				raise Exception('Error while loading workspace.')	
	else:
		wdcnt = 0
	
	## Wait for input
	lstimg = None
	while True:
		try:
			img = getClipboardImage()
		
		except NoImageData:
			time.sleep(.1)
			continue
		
		except (KeyboardInterrupt, SystemExit):
			break
		
		else:
			if imgCompare(img, lstimg):
				time.sleep(.2)
				continue
			
			img_path = wdir / '{}.png'.format(wdcnt)
			img.save(img_path.resolve())
			
			wdcnt += 1
			lstimg = img
		
		finally:
			with wdinfo.open('w') as file:
				file.write('{}\n'.format(wdcnt))
	

main()