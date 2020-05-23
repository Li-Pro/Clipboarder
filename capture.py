import io as _io
import sys as _sys
import subprocess as _subprocess
from warnings import warn as _warn
from PIL import ImageGrab as _ImageGrab, Image as _Image

class NoImageData(Exception):
	def __init__(self):
		super().__init__('No image data in clipboard.')

if _sys.platform in ('darwin', 'win32'):
	def getClipboardImage():
		img = _ImageGrab.grabclipboard()
		if not img:
			raise NoImageData
		
		return img

elif _sys.platform.startswith('linux'):
	def getClipboardImage():
		MIMEs = ['image/png', 'image/jpeg', 'image/bmp', 'image/gif', 'image/vnd.microsoft.icon', 'image/svg+xml', 'image/tiff', 'image/webp']
		for mimex in MIMEs:
			try:
				result = _subprocess.run(['xclip', '-o', '-target', mimex, '-selection', 'clipboard'], capture_output=True)
			except:
				print('Error: cannot run underlying functions.')
				print('Either dependencies not satisfied, or platform unsupported.')
				print('Please run setup.py for installation.')
				
				raise NotImplementedError
				
			else:
				if result.returncode != 0:
					continue
				
				imgbyte = result.stdout
				img = _Image.open(_io.BytesIO(imgbyte))
				return img
		
		raise NoImageData

else:
	warn("""Module is only tested in macOS & Windows & Linux (Ubuntu), other platform might not be supported. \
		Feel free to feedback to me if it doesn't work, or vice versa!""")

#-------------------------- Testing ---------------------------------

def _main():
	import time
	import tkinter as tk
	from PIL import Image, ImageTk
	
	# Wait for data input
	while True:
		try:
			img = getClipboardImage()
		except NoImageData:
			time.sleep(0.5)
			continue
		else:
			break
	
	sz = img.size
	nsz = tuple(int(x*.7) for x in sz)
	img.thumbnail(nsz)
	
	root = tk.Tk()
	root.title('View clipboard image')
	
	imgLabel = tk.Label(root, text='Image Output')
	imgLabel.image = ImageTk.PhotoImage(img)
	imgLabel.configure(image=imgLabel.image)
	imgLabel.pack()
	
	root.mainloop()

if __name__ == "__main__":
	_main()
#--------------------------------------------------------------------
