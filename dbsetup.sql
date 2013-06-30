CREATE TABLE unit (
	lectopia_unit INTEGER NOT NULL,
	short_name TEXT,
	human_name TEXT,
	PRIMARY KEY (lectopia_unit)
);
CREATE TABLE lecture (
	lectopia_lecture INTEGER NOT NULL,
	lectopia_unit INTEGER NOT NULL,
	timestamp INTEGER,
	minutes INTEGER,
	PRIMARY KEY (lectopia_lecture),
	FOREIGN KEY (lectopia_unit) REFERENCES unit (lectopia_unit)
);
CREATE TABLE file (
	lectopia_file INTEGER NOT NULL,
	lectopia_lecture INTEGER NOT NULL,
	bytes INTEGER,
	format TEXT,
	url TEXT,
	PRIMARY KEY (lectopia_file),
	FOREIGN KEY (lectopia_lecture) REFERENCES lecture (lectopia_lecture)
);
CREATE TABLE meta (
	lectopia_lecture INTEGER NOT NULL,
	key TEXT,
	value TEXT,
	PRIMARY KEY (lectopia_lecture, key),
	FOREIGN KEY (lectopia_lecture) REFERENCES lecture (lectopia_lecture)
);
