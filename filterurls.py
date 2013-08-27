#!/usr/bin/env python

import os
import re
import sqlite3

c = sqlite3.connect(os.path.join('data', 'meta.db'))
h = {}
for line in open(os.path.join('data', 'done.txt')):
	h[line.strip()] = True
for line in open(os.path.join('data', 'urls.txt')):
	if not h.has_key(re.split('/', line.strip())[-1]):
		print line.strip()
