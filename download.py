import sys
import subprocess

i = 0
for line in sys.stdin:
	i += 1
	url = line.strip()
	name = re.match('.+/(.+)$').group(0)
	print '\nFetching file', i + ':', name
	subprocess.call(['curl', '-#OC-', name])
