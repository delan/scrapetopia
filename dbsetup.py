import sqlite3

c = sqlite3.connect('data/meta.db')
c.executescript(open('dbsetup.sql').read())
c.commit()
c.close()
