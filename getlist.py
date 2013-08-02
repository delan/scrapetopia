#!/usr/bin/env python

import os
import re
import sqlite3

c = sqlite3.connect(os.path.join('data', 'meta.db'))
f = open(os.path.join('data', 'list.txt'), 'w')

for i in c.execute('SELECT * FROM file;').fetchall():
	if re.match('http://ftp\.ilectures\.curtin\.edu\.au/', i[4]):
		f.write(i[4] + '\n')

f.close()
