#Praveen Lama

from user import User
from book import Book
from database import DBConnector
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import session
import urllib2
import json

app = Flask(__name__)
dbConnector = DBConnector()


@app.route('/')
def showIndex():
    # check if not logged in
    if 'loggedState' not in session:
        return redirect("/login")
    listOfBooks = getBooksByCategories("christmas")

    return render_template('index.html', Username=session['username'], Carousellist = listOfBooks)


@app.route('/categories')
def showCategories():
    # check if not logged in
    if 'loggedState' not in session:
        return redirect("/login")
    Sports = getBooksByCategories("sports")
    Business = getBooksByCategories("business")
    Kids = getBooksByCategories("kids")
    Teen = getBooksByCategories("teen")
    Home = getBooksByCategories("home")
    Fashion = getBooksByCategories("fashion")

    return render_template('categories.html', Username=session['username'], Sports = Sports, Business = Business, Kids = Kids
                           , Teen = Teen, Home = Home, Fashion = Fashion)


@app.route('/login', methods=['GET'])
def showLogin():
    # First check if the user is already logged in
    if 'loggedState' in session:
        return redirect("/")
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    # Note: we take care of the invalid input in the front end for better efficiency
    # Validating input in the front end not only takes load off the back end service,
    # but also provides extra security i.e. sql injection etc
    email = request.form['email']
    password = request.form['password']
    login_failed = False

    if dbConnector.authenticateUser(email, password):
        session['loggedState'] = True
        session['uid'] = dbConnector.getCurrUserID(email, password)
        session['username'] = dbConnector.getCurrUsername(session['uid'])
        return redirect("/")  # redirect to dashboard
    else:
        login_failed = True
        return render_template("login.html",login_failed=login_failed)

    return redirect("/login")


@app.route('/logout')
def logout():
    del session['loggedState']
    del session['uid']
    return redirect("/login")


@app.route('/register', methods=['POST'])
def register():
    # Note: we take care of the invalid input in the front end for better efficiency
    # Validating input in the front end not only takes load off the back end service,
    # but also provides extra security i.e. sql injection etc
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    password = request.form['password']

    dbConnector.insertUser(fname, lname, email, password)

    return redirect("/login")


@app.route('/books', methods=['GET'])
def showBooks():
    listOfBooks = []
    # check if not logged in
    if 'loggedState' not in session:
        return redirect("/login")

    result = dbConnector.getAllBooks()

    for book in result:
        listOfBooks.append(Book(book[0],book[1], book[2], book[3], book[4], book[5], book[6], book[7]))

    return render_template('books.html', Username=session['username'], Books=listOfBooks)


@app.route('/addBook', methods=['GET'])
def showAddBook():
    # check if not logged in
    if 'loggedState' not in session:
        return redirect("/login")
    return render_template('addBook.html', Username=session['username'])


@app.route('/addBook', methods=['POST'])
def addBook():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    summary = request.form['summary']
    image = request.form['image']
    averageRating = request.form['averageRating']
    pageCount = request.form['pageCount']
    uid = session['uid']

    dbConnector.insertBook(isbn, title, author, summary, image, averageRating, pageCount, uid)
    notice = "Book has been successfully added"

    return render_template('addBook.html', notice=notice)


@app.route('/addCategoriesBook', methods=['POST'])
def addCategoriesBook():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    summary = request.form['summary']
    image = request.form['image']
    averageRating = request.form['averageRating']
    pageCount = request.form['pageCount']
    uid = session['uid']

    dbConnector.insertBook(isbn, title, author, summary, image, averageRating, pageCount, uid)
    notice = "Book has been successfully added"

    Sports = getBooksByCategories("sports")
    Business = getBooksByCategories("business")
    Kids = getBooksByCategories("kids")
    Teen = getBooksByCategories("teen")
    Home = getBooksByCategories("home")
    Fashion = getBooksByCategories("fashion")

    return render_template('categories.html', Username=session['username'], notice=notice, Sports=Sports, Business=Business, Kids=Kids
                           , Teen=Teen, Home=Home, Fashion=Fashion)


@app.route('/addHomeBook', methods=['POST'])
def addHomeBook():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    summary = request.form['summary']
    image = request.form['image']
    averageRating = request.form['averageRating']
    pageCount = request.form['pageCount']
    uid = session['uid']

    dbConnector.insertBook(isbn, title, author, summary, image, averageRating, pageCount, uid)
    notice = "Book has been successfully added"

    listOfBooks = getBooksByCategories("christmas")

    return render_template('index.html', Username=session['username'], notice=notice, Carousellist=listOfBooks)


@app.route('/deleteBook', methods=['POST'])
def deleteBook():
    id = request.form['id']
    listOfBooks = []
    dbConnector.deleteBook(id)
    notice = "Book has been successfully deleted"

    result = dbConnector.getAllBooks()
    for book in result:
        listOfBooks.append(Book(book[0], book[1], book[2], book[3], book[4], book[5]))

    return render_template('books.html', Username=session['username'], notice=notice, Books=listOfBooks)


@app.route('/search', methods=['POST'])
def search():
    listOfBooks = []
    cBooks = getBooksByCategories("christmas")
    isbn = request.form['search']
    apiURL = "https://www.googleapis.com/books/v1/volumes?q=+isbn:"+isbn
    response = urllib2.urlopen(apiURL)
    jsonResponse = json.load(response)

    if jsonResponse['totalItems'] > 0:

        for book in jsonResponse['items']:
            #print book['volumeInfo']
            id = "tempid"
            isbn = isbn
            title = book['volumeInfo']['title']

            if 'authors' in book['volumeInfo']:
                author = book['volumeInfo']['authors'][0]
            elif 'publisher' in book['volumeInfo']:
                author = book['volumeInfo']['publisher']
            else:
                author = ""

            if 'description' in book['volumeInfo']:
                summary = book['volumeInfo']['description']
            elif 'searchInfo' in book:
                summary = book['searchInfo']['textSnippet']
            else:
                summary = ""

            if 'imageLinks' in book['volumeInfo']:
                image = book['volumeInfo']['imageLinks']['thumbnail']
            else:
                image = ""

            if 'averageRating' in book['volumeInfo']:
                averageRating = book['volumeInfo']['averageRating']
            else:
                averageRating = "0"

            if 'pageCount' in book['volumeInfo']:
                pageCount = book['volumeInfo']['pageCount']
            else:
                pageCount = "0"

            listOfBooks.append(Book(id, isbn, title, author, summary, image, averageRating, pageCount))
    else:
        error = "No Books Available"
        return render_template('index.html', errorNotice=error, Carousellist=cBooks)

    return render_template('index.html', Username=session['username'], searchResults=listOfBooks, Carousellist=cBooks)


def getBooksByCategories(category):
    listOfBooks = []
    apiURL = "https://www.googleapis.com/books/v1/volumes?q="+category+"&printType=books"
    response = urllib2.urlopen(apiURL)
    jsonResponse = json.load(response)

    for book in jsonResponse['items']:
        id = "tempid"
        isbn = book['volumeInfo']['industryIdentifiers'][0]['identifier']
        title = book['volumeInfo']['title']

        if 'authors' in book['volumeInfo']:
            author = book['volumeInfo']['authors'][0]
        elif 'publisher' in book['volumeInfo']:
            author = book['volumeInfo']['publisher']
        else:
            author = ""

        if 'description' in book['volumeInfo']:
            summary = book['volumeInfo']['description']
        elif 'searchInfo' in book:
            summary = book['searchInfo']['textSnippet']
        else:
            summary = ""

        if 'imageLinks' in book['volumeInfo']:
            image = book['volumeInfo']['imageLinks']['thumbnail']
        else:
            image = ""

        if 'averageRating' in book['volumeInfo']:
            averageRating = book['volumeInfo']['averageRating']
        else:
            averageRating = "0"

        if 'pageCount' in book['volumeInfo']:
            pageCount = book['volumeInfo']['pageCount']
        else:
            pageCount = "0"


        title = (title[:10] + '..') if len(title) > 10 else title
        summary = (summary[:50] + '..') if len(summary) > 50 else summary
        listOfBooks.append(Book(id, isbn, title, author, summary, image, averageRating, pageCount))

    return listOfBooks


def main():
    dbConnector.loadDatabase()
    dbConnector.insertUser("praveen", "lama", "praveenlama@gmail.com","pass123")
    #dbConnector.insertBook("12345678", "A Sample Book", "Lama, Praveen", "This is a sample summary."
    #                     , "http://books.google.com/books/content?id=4NJwAQAACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api","3.4", "170",1)
    #dbConnector.closeDBConnector()
    app.run()

app.secret_key = '\x17\x96e\x94]\xa0\xb8\x1e\x8b\xee\xdd\xe9\x91^\x9c\xda\x94\t\xe8S\xa1Oe_'

if __name__ == '__main__':
    main()