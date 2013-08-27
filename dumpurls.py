#!/usr/bin/env python

import os
import re
import sqlite3

c = sqlite3.connect(os.path.join('data', 'meta.db'))
for i in c.execute('SELECT url FROM file;').fetchall():
	if re.match('^http://ftp\.ilectures\.curtin\.edu\.au/', i[0]):
		print i[0]
