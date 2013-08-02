#!/usr/bin/env python

import os
import sqlite3

print 'Creating directories ...',

path = os.path.join('data', 'media')
try:
	os.stat(path)
except OSError:
	os.makedirs(path)
	print 'done'
else:
	print 'already done'

print 'Initialising database ...',

path = os.path.join('data', 'meta.db')
try:
	os.stat(path)
except OSError:
	c = sqlite3.connect(path)
	c.executescript(open('schema.sql').read())
	c.commit()
	c.close()
	print 'done'
else:
	print 'already done'
