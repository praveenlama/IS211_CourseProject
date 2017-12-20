
class Book:
    def __init__(self, bid, isbn, title, author, summary, image, averageRating, pageCount):
        self.id = bid
        self.isbn = isbn
        self.title = title
        self.author = author
        self.summary = summary
        self.image = image
        self.averageRating = averageRating
        self.pageCount = pageCount

    def getID(self):
        return self.id

    def getISBN(self):
        return self.isbn

    def getTitle(self):
        return self.title

    def getAuthor(self):
        return self.author

    def getSummary(self):
        return self.summary

    def getImage(self):
        return self.image

    def getAverageRating(self):
        return self.averageRating

    def getPageCount(self):
        return self.pageCount