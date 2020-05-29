import sys
import subprocess

from warnings import warn as _warn

# Detect version requirements
py_ver = sys.version_info[0: 2]
req_ver = (3, 0)
if py_ver < req_ver:
	raise Exception('Python version should be >=', req_ver)

# Setup from requirements
# subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
APT_INST = ['sudo', 'apt-get', 'install']
PIP_INST = [sys.executable, '-m', 'pip', 'install']

COMMON_DEP = [
	[*PIP_INST, 'Pillow==7.1.2']
]

LINUX_DEP = [
	[*APT_INST, 'xclip', 'python3-tk']
]

WIN_DARWIN_DEP = [
]

# Install additional files if needed
for depends in COMMON_DEP:
	subprocess.run(depends)

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
