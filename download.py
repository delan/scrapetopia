import sys
import re
import subprocess

i = 0
for line in sys.stdin:
	i += 1
	url = line.strip()
	name = re.match('.+/(.+)$', url).group(1)
	print '\nFetching file', str(i) + ':', name
	subprocess.call(['curl', '-#OC-', url])
