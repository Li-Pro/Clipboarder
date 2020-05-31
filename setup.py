#######################
# check / install pip #
#######################
try:
	import pip
except:
	try:
		import ensurepip
		ensurepip.bootstrap()
		
		import pip
	except:
		raise Exception('PIP does not exist, and can not be installed.')


###############################
# Detect version requirements #
###############################
import pip
import sys
import subprocess

from warnings import warn as _warn

py_ver = sys.version_info[0: 2]
pip_ver = tuple(map(int, pip.__version__.split('.')))

req_py_ver = (3, 5)
suggest_pip_ver = (20, 1)
if py_ver < req_py_ver:
	raise Exception('Python version should be >=', req_py_ver)

if pip_ver < suggest_pip_ver:
	_warn('PIP might need to be upgraded (currently using {})'.format('.'.join(map(str, pip_ver))))


###########################
# Setup from requirements #
###########################
APT_INST = ['sudo', 'apt-get', 'install']
PIP_INST = [sys.executable, '-m', 'pip', 'install']

COMMON_DEP = [
	[*PIP_INST, 'Pillow==7.1.2']
]

for depends in COMMON_DEP:
	subprocess.run(depends)


######################################
# Install additional files if needed #
######################################
LINUX_DEP = [
	[*APT_INST, 'xclip', 'python3-tk']
]

WIN_DARWIN_DEP = [
]

if sys.platform in ('darwin', 'win32'):
	for depends in WIN_DARWIN_DEP:
		subprocess.run(depends)

elif sys.platform.startswith('linux'):
	for depends in LINUX_DEP:
		subprocess.run(depends)

else:
	_warn('Platform other than Windows, macOS and Linux might be unsupported.')
	for depends in LINUX_DEP:
		subprocess.run(depends)

print()
print('Setup completed.')