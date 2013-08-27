#!/usr/bin/env python

import os
import sqlite3

c = sqlite3.connect(os.path.join('data', 'meta.db'))
for i in c.execute('SELECT url FROM file;').fetchall():
	print i[0]
