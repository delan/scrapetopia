#!/usr/bin/env python

import os
import re

i = 0
f = open(os.path.join('data', 'list.txt'))
result = []
for line in f:
	url = line.strip()
	match = re.match('.+/(.*)', url)
	if match:
		fn = match.group(1)
		if not os.path.exists(os.path.join('data', 'media', fn)):
			result.append(url)
		i += 1
		if i % 100 == 0
			print i,
f.close()

print ''

f = open(os.path.join('data', 'list.txt'), 'w')
for url in result:
	f.write(url + '\n')
f.close()
