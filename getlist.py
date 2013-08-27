#!/usr/bin/env python

import os
import re
import sqlite3

c = sqlite3.connect(os.path.join('data', 'meta.db'))
f = open(os.path.join('data', 'list.txt'), 'w')
h = {}

for i in os.listdir(os.path.join('data', 'media')):
	h[i] = True

for i in c.execute('SELECT * FROM file;').fetchall():
	if re.match('http://ftp\.ilectures\.curtin\.edu\.au/', i[4]):
		n = re.split('/', i[4])[-1]
		if not h.has_key(n):
			f.write(i[4] + '\n')

f.close()
