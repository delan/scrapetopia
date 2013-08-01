import os
import sys
import math
import json
import flask
import sqlite3

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

basedir = os.path.dirname(__file__)
mediadir = '/cygdrive/e/lectopia1'

app = flask.Flask(__name__, static_folder=os.path.join(basedir, 'static'))
PORT = 7542

c = sqlite3.connect(os.path.join('..', 'data', 'meta.db'), timeout=30.0)

def bytes(n, decimal=True, dp=3):
	base = (2, 10)[decimal];
	exp = (10, 3)[decimal];
	if decimal:
		units = ('B', 'KB', 'MB', 'GB', 'TB', 'PB')
	else:
		units = ('B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB')
	for i in range(5, -1, -1):
		if n >= math.pow(base, i * exp) - 1:
			x = n / math.pow(base, i * exp)
			return str(round(x, dp)) + ' ' + units[i];

@app.route('/')
def hello():
	kwargs = {}
	return flask.render_template('index.html', **kwargs)

@app.route('/stats/<kind>')
def stats(kind):
	o = {}
	if kind == 'units_total':
		r = c.execute('SELECT COUNT(*) FROM unit')
		o = r.fetchone()[0]
	elif kind == 'units_useful':
		r = c.execute('SELECT COUNT(*) FROM unit \
			WHERE lectopia_unit IN \
			(SELECT lectopia_unit FROM lecture \
				WHERE lectopia_lecture IN \
				(SELECT lectopia_lecture FROM file))')
		o = r.fetchone()[0]
	elif kind == 'lectures_useful':
		r = c.execute('SELECT COUNT(*) FROM lecture \
			WHERE lectopia_lecture IN \
			(SELECT lectopia_lecture FROM file)')
		o = r.fetchone()[0]
	elif kind == 'files_total':
		r = c.execute('SELECT COUNT(*) FROM file')
		o = r.fetchone()[0]
	elif kind == 'files_useful':
		o = len(os.listdir(mediadir))
	elif kind == 'files_total_size':
		r = c.execute('SELECT SUM(bytes) FROM file')
		o = bytes(r.fetchone()[0])
	elif kind == 'files_useful_size':
		o = 0
		for f in os.listdir(mediadir):
			o += os.stat(os.path.join(mediadir, f)).st_size
		o = bytes(o)
	return flask.Response(json.dumps(o), mimetype='application/json')

# @app.route('/dummy')
# def xyz():
# 	return flask.send_from_directory(app.static_folder, 'index.html')

# @app.route('/raw')
# def raw():
# 	o = json.dumps({})
# 	return flask.Response(o, mimetype='application/json')

if __name__ == '__main__':
	if len(sys.argv) > 1:
		PORT = sys.argv[1]
	server = HTTPServer(WSGIContainer(app))
	print 'Now listening on port ' + str(PORT)
	server.listen(PORT)
	IOLoop.instance().start()
