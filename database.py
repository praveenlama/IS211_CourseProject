import sqlite3

class DBConnector:
    def __init__(self):
        self.conn = sqlite3.connect('storage.db')
        self.currUserID = 0
        self.currUsername = ""

    def loadDatabase(self):
        f = open('schema.sql', 'r')
        sql = f.read()
        self.conn.executescript(sql)
        self.conn.commit()

    def authenticateUser(self,email,password):
        connStatement = 'SELECT COUNT(*) FROM Users WHERE email == "' + email + '"AND password == "'+password+'"'
        result = self.conn.execute(connStatement)
        result = result.fetchone()
        self.conn.commit()
        if result[0] > 0:
            return True
        return False

    def getCurrUserID(self,email,password):
        connStatement = 'SELECT id FROM Users WHERE email == "' + email + '"AND password == "'+password+'"'
        result = self.conn.execute(connStatement)
        result = result.fetchone()
        self.conn.commit()
        self.currUserID = result[0]
        return self.currUserID

    def getCurrUsername(self,id):
        connStatement = 'SELECT fname,lname FROM Users WHERE id == ' + str(id)
        result = self.conn.execute(connStatement)
        result = result.fetchone()
        self.conn.commit()
        self.currUsername = result[1] + ", " + result[0]
        return self.currUsername

    def insertUser(self,fname, lname, email, password):
        connStatement = 'INSERT INTO Users(fname, lname, email, password) VALUES("%s", "%s", "%s", "%s");' % (
            fname, lname, email, password)
        self.conn.execute(connStatement)
        self.conn.commit()

    def insertBook(self,isbn, title, author, summary, image, averageRating, pageCount, uid):
        connStatement = 'INSERT INTO Books(isbn, title, author, summary, image, averageRating, pageCount, uid) VALUES("%s","%s", "%s", "%s", "%s", "%s", "%s", "%s");' % (
            isbn.replace('"',''), title.replace('"',''), author.replace('"',''), summary.replace('"',''), image, averageRating, pageCount, uid)
        self.conn.execute(connStatement)
        self.conn.commit()

    def deleteBook(self,id):
        connStatement = 'DELETE FROM Books WHERE id == ' + id
        self.conn.execute(connStatement)
        self.conn.commit()

    def selectUserByID(self,id):
        connStatement = 'SELECT * FROM Users WHERE id == ' + id
        result = self.conn.execute(connStatement)
        result = result.fetchone()
        self.conn.commit()
        return result

    def selectBookByISBN(self,isbn):
        connStatement = 'SELECT * FROM Books WHERE isbn == ' + isbn
        result = self.conn.execute(connStatement)
        result = result.fetchone()
        self.conn.commit()
        return result

    def getAllBooks(self):
        connStatement = 'SELECT * FROM Books WHERE uid == ' + str(self.currUserID)
        result = self.conn.execute(connStatement)
        result = result.fetchall()
        self.conn.commit()
        return result

    def getAllSearchResult(self):
        connStatement = 'SELECT * FROM SearchResults'
        result = self.conn.execute(connStatement)
        result = result.fetchall()
        self.conn.commit()
        return result

    def closeDBConnector(self):
        self.conn.close()