import sys
import re
import time
import calendar
import urllib2
import bs4
import sqlite3

c = sqlite3.connect('data/meta.db')

prefix = 'http://dbs.ilectures.curtin.edu.au/lectopia/lectopia.lasso?ut='
prefix2 = 'http://dbs.ilectures.curtin.edu.au/lectopia/downloadpage.lasso?fid='
prefix3 = 'http://dbs.ilectures.curtin.edu.au/lectopia/'
tzoffset = 28800 # lecture times are UTC+8

def fetch_wrapper(url):
	print url
	return urllib2.urlopen(url).read()

def normalise_whitespace(text):
	text = re.sub('\s+', ' ', text, flags=re.UNICODE)
	text = re.sub('^\s+|\s+$', '', text, flags=re.UNICODE)
	return text

soup = bs4.BeautifulSoup(fetch_wrapper(prefix + sys.argv[1]))

m = re.match('(.+) \(([A-Za-z0-9_-]+)\)', soup.h2.string)

lectopia_unit = sys.argv[1]
short_name = m.group(2)
human_name = m.group(1)

c.execute('INSERT INTO unit VALUES (?, ?, ?)',
	(lectopia_unit, short_name, human_name))
c.commit()

while True:
	for lecture in soup.find_all(class_='mainindex'):
		heading = lecture.find(class_='sectionHeading').find_all('td')
		lectopia_lecture = int(normalise_whitespace(heading[0].a['id']))
		timestamp = normalise_whitespace(heading[0].a.string)
		timestamp = time.strptime(timestamp, '%d %b %Y - %H:%M')
		timestamp = calendar.timegm(timestamp) - tzoffset
		minutes = normalise_whitespace(heading[1].string)
		minutes = int(re.match('(\d+) mins', minutes).group(1))
		c.execute('INSERT INTO lecture VALUES (?, ?, ?, ?)',
			(lectopia_lecture, lectopia_unit, timestamp, minutes))
		c.commit()
		meta = lecture.find_all(class_='metaTag')
		for k in meta:
			v = k.next_sibling.next_sibling
			if v and v.string:
				key = normalise_whitespace(k.string)
				value = normalise_whitespace(v.string)
				c.execute('INSERT INTO meta VALUES (?, ?, ?)',
					(lectopia_lecture, key, value))
				c.commit()
		form_filter = {'name': 'Download' + str(lectopia_lecture)}
		form = lecture.find(attrs=form_filter)
		if form is None:
			continue
		option_filter = {'title': re.compile('.+')}
		options = form.find_all('option', attrs=option_filter)
		for file in options:
			m = re.match('(.+) \((\d+\.\d+) MB\)', file['title'])
			lectopia_file = re.match('\d+,(\d+)', file['value'])
			lectopia_file = int(lectopia_file.group(1))
			# Lectopia defines MB = 1048576 B
			bytes = int(float(m.group(2)) * 1048576)
			format = m.group(1)
			download_soup = prefix2 + str(lectopia_file)
			download_soup = fetch_wrapper(download_soup)
			download_soup = bs4.BeautifulSoup(download_soup)
			url = download_soup.a['href']
			c.execute('INSERT INTO file VALUES (?, ?, ?, ?, ?)',
				(lectopia_file, lectopia_lecture,
					bytes, format, url))
			c.commit()
	next = soup.find('a', text='next')
	if next:
		soup = bs4.BeautifulSoup(fetch_wrapper(prefix3 + next['href']))
	else:
		break

c.commit()
c.close()
