from book import Book
import pickle

class bookDB(Book):
    def __init__(self):
        try:
            with open('bookDB.pickle', 'rb') as handle:
                self.books = pickle.load(handle)
        except:
            self.books = {}
        

    def NEW(self, author, title, year, bookid):
        newbook = Book(author, title, year, bookid)
        self.books[newbook.getID()] = newbook
        with open('bookDB.pickle', 'wb') as handle:
            pickle.dump(self.books, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
    def SHOW(self, id):
        return self.books[id]

    def AUTHORS(self):
        authors = []
        for key, bk in self.books.items():
            authors.append(bk.getAuthor())

        print(authors)
    
    def SEARCH_AUTH(self, author):
        books = []
        for key, bk in self.books.items():
            if bk.getAuthor() == author:
                books.append(bk)

        for bk in books:
            print(bk)

    def SEARCH_YEAR(self, year):
        books = []
        for key, bk in self.books.items():
            if bk.getYear() == int(year):
                books.append(bk)
        for bk in books:
            print(bk)