import os
import sys
import math
import re
import json
import flask
import sqlite3

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

basedir = os.path.dirname(__file__)
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
	o = None
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
	elif kind == 'lectures_total':
		r = c.execute('SELECT COUNT(*) FROM lecture')
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

@app.route('/units/')
def units():
	o = {}
	r = c.execute('SELECT * FROM unit')
	o['aaData'] = r.fetchall()
	return flask.Response(json.dumps(o), mimetype='application/json')

@app.route('/units/<unit>')
def lectures_by_unit(unit):
	o = {}
	r = c.execute('SELECT * FROM lecture WHERE lectopia_unit = ?',
		(unit,))
	o['aaData'] = r.fetchall()
	return flask.Response(json.dumps(o), mimetype='application/json')

@app.route('/lectures/<lecture>')
def files_by_lecture(lecture):
	o = {}
	r = c.execute('SELECT * FROM file WHERE lectopia_lecture = ?',
		(lecture,))
	o['aaData'] = r.fetchall()
	return flask.Response(json.dumps(o), mimetype='application/json')

@app.route('/meta/<lecture>')
def meta_by_lecture(lecture):
	o = {}
	r = c.execute('SELECT * FROM meta WHERE lectopia_lecture = ?',
		(lecture,))
	o['aaData'] = r.fetchall()
	return flask.Response(json.dumps(o), mimetype='application/json')

@app.route('/files/<fname>')
def file_by_name(fname):
	# Flask does not support serving a partial static file with Range.
	# Roll our own handler here instead.
	fname = os.path.join(mediadir, fname)
	mime = {
		'3gp': 'audio/3gpp',
		'm4b': 'audio/mp4a-latm',
		'mov': 'video/quicktime',
		'mp3': 'audio/mpeg',
		'mp4': 'video/mp4',
		'wma': 'audio/x-ms-wma',
		'wmv': 'video/x-ms-wmv'
	}[re.match('^.+\\.([^.]+)$', fname).group(1)]
	try:
		size = os.stat(fname).st_size
	except OSError:
		return flask.Response(status=404)
	begin = 0
	end = size - 1
	if flask.request.headers.has_key('Range'):
		ranges = re.findall('\\d+', flask.request.headers['Range'])
		begin = int(ranges[0])
		if len(ranges) > 1:
			end = int(ranges[1])
		length = 1 + end - begin
		if begin < end < size:
			data = None
			with open(fname, 'rb') as f:
				f.seek(begin)
				data = f.read(length)
			response = flask.Response(data, status=206)
			response.headers.add('Content-Type', mime)
			response.headers.add('Accept-Ranges', 'bytes')
			response.headers.add('Content-Range',
				'bytes %d-%d/%d' % (begin, end, size))
			return response
		else:
			return flask.Response(status=416)
	return flask.Response(open(fname, 'rb'), mimetype=mime)

if __name__ == '__main__':
	if len(sys.argv) == 2:
		mediadir = sys.argv[1]
	elif len(sys.argv) == 3:
		mediadir = sys.argv[1]
		PORT = sys.argv[2]
	else:
		sys.exit("usage: scweb.py [mediadir] [port]")
	server = HTTPServer(WSGIContainer(app))
	print 'Now listening on port ' + str(PORT)
	server.listen(PORT)
	IOLoop.instance().start()
