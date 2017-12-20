DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Books;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY,
	fname TEXT,
    lname TEXT,
    email EMAIL,
    password PASSWORD
);

CREATE TABLE Books (
	id INTEGER PRIMARY KEY,
	isbn TEXT,
	title TEXT,
	author TEXT,
	summary TEXT,
	image TEXT,
	averageRating TEXT,
	pageCount TEXT,
	uid INTEGER,
    dateInserted DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);


