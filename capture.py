import io as _io
import sys as _sys
from warnings import warn as _warn

class NoImageData(Exception):
	def __init__(self):
		super().__init__('No image data in clipboard.')

if _sys.platform in ('darwin', 'win32'):
	from PIL import ImageGrab as _ImageGrab
	
	def getClipboardImage():
		img = _ImageGrab.grabclipboard()
		if not img:
			raise NoImageData
		
		return img

else:
	# Testing needed!
	_warn("""Module is only tested in macOS & Windows, other platform might not be supported. \
		Feel free to feedback to me if it doesn't work, or vice versa!""")
	
	import tkinter as _tk
	_img_grabber = _tk.Tk()
	_img_grabber.iconify()
	_img_grabber.title('Clipboarder process')
	_tk.Label(_img_grabber, text='This is Clipboarder inner process. DO NOT close this while running.').pack()
	
	def getClipboardImage():
		MIMEs = ['image/png', 'image/jpeg', 'image/bmp', 'image/gif', 'image/vnd.microsoft.icon', 'image/svg+xml', 'image/tiff', 'image/webp']
		for mimex in MIMEs:
			try:
				images = _img_grabber.clipboard_get(type=mimex)
				imgbyte = bytes(images)  # Might be: bytes(images.split()[0])
			except tk.TclError:
				continue
			else:
				img = PIL.Image.open(_io.BytesIO(imgbyte))
				return img
		
		# It's either no data OR not supported
		raise NoImageData

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
	rooot.title('View clipboard image')
	
	imgLabel = tk.Label(root, text='Image Output')
	imgLabel.image = ImageTk.PhotoImage(img)
	imgLabel.configure(image=imgLabel.image)
	imgLabel.pack()
	
	root.mainloop()

if __name__ == "__main__":
	_main()
#--------------------------------------------------------------------