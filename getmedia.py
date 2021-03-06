#!/usr/bin/env python

import os
import sys
import time
import re
import subprocess

sys.stdout = sys.stderr
f = open(os.path.join('data', 'list.txt'))
done = open(os.path.join('data', 'done.txt'), 'a')
os.chdir(os.path.join('data', 'media'))

i = 0
for line in f:
	i += 1
	url = line.strip()
	if not re.match('http://ftp\.ilectures\.curtin\.edu\.au/', url):
		continue
	origurl = url
	url = re.sub('ftp\.ilectures\.curtin\.edu\.au', '134.7.37.39', url)
	name = re.match('.+/(.+)$', url).group(1)
	print 'Fetching file', str(i) + ':', name, '...',
	retry = 0
	wait = 0.1
	while True:
		retval = subprocess.call(['curl', '-fsOC-', url])
		if retval in (0, 18, 33):
			print 'success!'
			break
		else:
			retry += 1
			time.sleep(wait)
			print 'error', retval
			print 'Retry #' + str(retry), '...',
			wait = (wait * 2) if wait < 15 else 30
	done.write(origurl + '\n')
	done.flush()
done.close()
