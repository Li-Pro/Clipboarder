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
	
	# print('#', h, w, h*w, len(img1.tobytes()), len(img2.tobytes()))
	# exit(0)
	# return True
	
	# for i in range(h):
		# for j in range(w):
			# if not img1.getpixel((i, j)) == img2.getpixel((i, j)):
				# return False
	
	# return True
	return img1.tobytes() == img2.tobytes()

def captureProc():
	return

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
		# nowtime = time.perf_counter()
		try:
			img = getClipboardImage()
			# print('#getClipboardImage: {}'.format(time.perf_counter() - nowtime))
			# nowtime = time.perf_counter()
			
		except NoImageData:
			time.sleep(.1)
			# print('#NoImageData: {}'.format(time.perf_counter() - nowtime))
			# nowtime = time.perf_counter()
			
			continue
		
		except (KeyboardInterrupt, SystemExit):
			break
		
		else:
			# print('#1: {}'.format(time.perf_counter() - nowtime))
			# nowtime = time.perf_counter()
			
			if imgCompare(img, lstimg):
				# print('#imgCompare: {}'.format(time.perf_counter() - nowtime))
				# nowtime = time.perf_counter()
				
				time.sleep(.2)
				continue
			
			# print('#2: {}'.format(time.perf_counter() - nowtime))
			# nowtime = time.perf_counter()
			
			img_path = wdir / '{}.png'.format(wdcnt)
			img.save(img_path.resolve())
			# print('#img.save: {}'.format(time.perf_counter() - nowtime))
			# nowtime = time.perf_counter()
			
			wdcnt += 1
			lstimg = img
			# print('#img =: {}'.format(time.perf_counter() - nowtime))
			# nowtime = time.perf_counter()
		
		finally:
			with wdinfo.open('w') as file:
				file.write('{}\n'.format(wdcnt))
	

main()