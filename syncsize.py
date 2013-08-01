import os
import sys
import shutil

def copy(n, x, y):
	sys.stdout.flush()
	shutil.copyfile(os.path.join(x, n), os.path.join(y, n))

if len(sys.argv) != 3:
	sys.exit("usage: syncsize.py [source_dir] [destination_dir]")

i = 0
x = sys.argv[1]
y = sys.argv[2]

for n in os.listdir(sys.argv[1]):
	i += 1
	print i, n,
	try:
		a = os.stat(os.path.join(x, n))
	except OSError:
		print '?'
		continue
	try:
		b = os.stat(os.path.join(y, n))
	except OSError:
		copy(n, x, y)
		print '+', a.st_size
		continue
	if a.st_size == b.st_size:
		print '=', a.st_size
	else:
		copy(n, x, y)
		print '*', a.st_size
