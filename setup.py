import sys
import subprocess

# Detect version requirements
py_ver = sys.version_info[0: 2]
req_ver = (3, 0)
if py_ver < req_ver:
	raise Exception('Python version should be >=', req_ver)

# Setup from requirements
subprocess.run(['python', '-m', 'pip', 'install', '-r', 'requirements.txt'])

# Install additional files if needed
if sys.platform.startswith('linux'):
	subprocess.run(['sudo', 'apt-get', 'install', 'xclip', 'python3-tk'])