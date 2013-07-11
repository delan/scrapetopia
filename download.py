import sys
import re
import subprocess

i = 0
for line in sys.stdin:
	i += 1
	url = line.strip()
	origurl = url
	url = re.sub('ftp\.ilectures\.curtin\.edu\.au', '134.7.37.39', url)
	name = re.match('.+/(.+)$', url).group(1)
	print '\nFetching file', str(i) + ':', name
	while True:
		retval = subprocess.call(['curl', '-#OC-', url])
		if retval in (0, 33):
			print 'Success!'
			break
		else:
			print '\nRetrying, error', retval
	done = open('done.txt', 'a')
	done.write(origurl + '\n')
	done.close()
