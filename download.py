import sys
import time
import re
import subprocess

i = 0
for line in sys.stdin:
	i += 1
	url = line.strip()
	origurl = url
	url = re.sub('ftp\.ilectures\.curtin\.edu\.au', '134.7.37.39', url)
	name = re.match('.+/(.+)$', url).group(1)
	print 'Fetching file', str(i) + ':', name, '...',
	retry = 0
	wait = 0.1
	while True:
		retval = subprocess.call(['curl', '-fsOC-', url])
		if retval in (0, 33):
			print 'success!'
			break
		else:
			retry += 1
			time.sleep(wait)
			print 'error', retval
			print 'Retry #' + str(retry), '...',
			wait = (wait * 2) if wait < 15 else 30
	done = open('done.txt', 'a')
	done.write(origurl + '\n')
	done.close()