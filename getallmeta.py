#!/usr/bin/env python

import time
import subprocess

budget = 8
reach = 9999
workers = [None] * budget
unit = 0

def hire(slot):
	global unit
	print unit
	workers[slot] = subprocess.Popen(['python', 'getmeta.py', str(unit)])
	unit += 1

for i in range(budget):
	hire(i)

while True:
	if unit > reach:
		break
	for i in range(budget):
		if workers[i].poll() is not None:
			hire(i)
	time.sleep(1)
