import sys
sys.path.append('..')
from Django_Logger import DjangoLogger
from django.core.management.base import BaseCommand
from Library_Browser.models import Book, Author


import os
import json
from pprint import pprint
import requests
import logging as log
basicConfig = log.basicConfig(filename="InitalFill_Log.log",filemode='a', level=log.DEBUG)
searchLog = log.getLogger('Search_Log')
makeAuthorLog = log.getLogger('Make_Author_Log')

# from .. import Django_logger


'''
python manage.py InitialFill

run to fill books db from bookInfo
'''

class Command(BaseCommand):
    help = 'initial database fill'

    def add_arguments(self, parser):
        self.numBooks = int(input('Number of Books: '))

    # Fetch books from dir and fill Book model
    def handle(self, **options):
        mainLog = DjangoLogger(homePath = r'C:\Users\User\Documents\Programming\Python_stuff\Dj_Folder')
        self.roamLog = mainLog.make_log(name='roam')
        self.makeAuthorLog = mainLog.make_log(name='make_author')
        self.makeBookLog = mainLog.make_log(name='make_book')
        self.roamLog.info('**************************\nBEGIN NEW TEST')
        #! Table for cleaning titles with title.translate(translationTable)
        #! ord('x') returns the unicode point for x
        translationTable = {
            ord(':'): '',
            ord(','): '',
            ord(' '): '_',
            ord('.'): '',
            ord('?'): '',
            ord('-'): '',
            ord('('): '',
            ord(')'): '',
            ord('â'): ''
        }

        # Open temp log file
        self.roamLog.info(f'Number of books: {self.numBooks}')

        def searchIsbn(searchParams, searchType):
            """ DocString
            Search ISBN with isbn/searchType/searchParams

            Args:
                searchParams (str): author name | book title
                searchType (str): "books" | "author"

            Returns:
                Dict(): 
                For searchType=Author
                    {author: author
                        books:[
                            {}
                            {}
                        ]
                    }

                For searchType=Books
                {books:[
                        {}
                        {}
                    ]
                }
            """            
            
            self.roamLog.info(f'\tSearched for: {searchParams}, type: {searchType}')
            API_KEY = '47499_f78bac55d9b443f63af60271fc8273f4'
            headers = {
            'Authorization': API_KEY,
            }
            pagination = 'page=1&pageSize=1'
            searchTerm = searchParams
            params = {
                'page': 1,
                'pageSize':2
                }
            if searchType == 'book':
                url = f"https://api2.isbndb.com/books/{searchTerm}"
            elif searchType == 'author':
                url = f"https://api2.isbndb.com/author/{searchTerm}"
            self.roamLog.info(f'\tSearchUrl: {url}')
            '''
            Get json obj from isbn api
            {
                author: author
                books:[
                    {}
                    {}
                ]
            }
            '''
            searchResult = {}
            try:
                searchResult = requests.get(url, headers=headers, params=params).json()
                self.roamLog.info('\tSuccess')
            except Exception as e:
                self.roamLog.exception(e)
                print(e)
                return None
            
            # API Lockout Handler
            if searchResult.get('message') == 'User is not authorized to access this resource with an explicit deny':
                print(searchResult)
                self.roamLog.error('Ran out of API calls')
                return None

            self.roamLog.info(f'Total Results: {searchResult.get("total")}')
            return searchResult
        
        def cleanAuthorISBN(authors):
            pass
            
        def makeBook(result, writers):
            """ Makes or updates a book model with a list of contributing authors

            Args:
                result (dict): single book result from ISDB
                writers (list(Author)): a list of author models to attach to the book

            Returns:
                newBook: Final book model with updated authors
            """            
            self.makeBookLog.info(f'Title: {result.get("title")}')
            
            # Checks if result.title matches an existing book in db
            filt = Book.objects.filter(title=result.get('title'))
            if len(filt) != 0:
                oldBook = filt[0]
                self.makeBookLog.warn(f'Filtered {oldBook.title}')
                for author in writers:
                    oldBook.author.add(author)
                return oldBook
            
            # If not creates new book
            newBook = Book(
                title=result.get('title'),
                # titleLong=result.get('titleLong'),
                imageLink=result.get('image'),
                isbn=result.get('isbn'),
                # publishedDate=result.get('date_published')
            )

            # check if msrp exists; add
            try: 
                msrp = float(result.get('msrp'))
                newBook.msrp = msrp
            except Exception as e:
                self.makeBookLog.info('No MSRP\n')

            # check if pageCount exists: add
            try:
                pageCount = int(result.get('pages'))
                newBook.pageCount = pageCount
            except Exception as e:
                self.makeBookLog.info('No PageCount')
            newBook.save()
            
            # Add the book to all contributing writers
            for author in writers:
                newBook.author.add(author)
                self.makeBookLog.info(f'Book: {newBook.title}\nWritten By: {author.last_name}')
                
            return newBook
            
            
        def makeAuthor(name):
            """
            Takes a name object (LAST, FIRST | FIRST LAST | LAST, FIRST MI.)
            Creates a new AuthorObj(first_name=first, last_name=last) if doesnt exist

            ! Error with first except statement, worked without it
            !   -Would create author(John, Smith) & Author(Smith, John)
            ! Worked without
            Args:
                name (str): name from searchedBook

            Returns:
                Author: AUthor object, either existing or created

            """  
            
            raw = name.split(' ')
            self.makeAuthorLog.info(f'*** BEGIN MAKE AUTHOR ***\nName: {name}\tRAW: {raw}')          

            # Default name to fill
            fullName = {
                'first': 'z',
                'middle': 'z',
                'last': 'z',}
            
            # Fill full name according to input data
            if len(raw) == 1:
                fullName['first'] = raw[0]
                
            elif len(raw) == 2:
                if ',' in raw[0]:
                    fullName['last'] = raw[0].replace(',', '')
                    fullName['first'] = raw[1]
                else:
                    fullName['first'] = raw[0]
                    fullName['last'] = raw[1]
                    
            elif len(raw) == 3:
                if ',' in raw[0]:
                    fullName['last'] = raw[0].replace(',', '')
                    fullName['first'] = raw[1]
                    fullName['middle'] = raw[2]
                else:
                    fullName['first'] = raw[0]
                    fullName['middle'] = raw[1].replace(',', '')
                    fullName['last'] = raw[2]
            self.makeAuthorLog.info(f'Full Name: {fullName}')

            # get list of existing authors, reverse for bad formatting
            filt = Author.objects.filter(first_name=fullName['first'],
                                        middle_initial=fullName['middle'],
                                        last_name=fullName['last'])
            
            revFilt = Author.objects.filter(first_name=fullName['last'],
                                            middle_initial=fullName['middle'],
                                            last_name=fullName['first'])
            
            # if overlap return that Author model
            if len(filt) != 0 or len(revFilt) != 0:
                self.roamLog.info(f'Repeat Filtered {fullName}')
                self.roamLog.info(f'Filt: {len(filt)}\t RevFilt: {len(revFilt)}')
                try:
                    oldAuthor = filt[0]
                    self.roamLog.info(f'Returned: {oldAuthor.pk}')
                    return oldAuthor
                except Exception as e:
                    oldAuthor = revFilt[0]
                    self.roamLog.info(f'Returned: {oldAuthor.pk}')
                    return oldAuthor
                
            # if no overlap return new author
            else:
                try:
                    newAuthor = Author(first_name=fullName['first'],
                                        middle_initial=fullName['middle'],
                                        last_name=fullName['last'])
                    newAuthor.save()
                    pk = newAuthor.pk
                    self.roamLog.info(f'Created {newAuthor.first_name} {newAuthor.last_name} {pk}')
                    return newAuthor
                
                # if failed return none
                except Exception as e:
                    self.roamLog.warn(f'Failed to create{newAuthor.first_name} {newAuthor.last_name}')
                    self.roamLog.error(e)
                    return None
            
        def fillAuthors():
            # Chdir to books and list file names
            bookInfoPath = 'C:\\Users\\User\\Documents\\Programming\\Python_stuff\\LibraryBuilder\\Book_Info_Json'
            bookInfo = os.listdir(bookInfoPath)
            os.chdir(bookInfoPath)
            self.roamLog.info(f'Book Info Path: {bookInfoPath}')
            # Generate list of books and load json object from each
            bookCount = 0
            authorList = []
            for book in bookInfo[:self.numBooks]:
                with open(book, 'r') as b:
                    info = json.load(b)
                title = info.get('title')

                # Get first author from booksInfo and search isbn
                # Return either info{} or None
                fileAuthor = ''
                try:
                    fileAuthor = info.get('authors')[0].translate(translationTable)
                except TypeError as e:
                    break

                try:
                    self.roamLog.info(f'-----------------------\nTitle: {title}\nFileAuthor: {fileAuthor}\n')
                except Exception as e:
                    self.roamLog('Cannot Write !!!!')
                
                searchInfo = searchIsbn(title, 'book')
                if searchInfo:
                    
                    # Split author first and last name
                    # isbnLog.write(f'Raw Author: {searchInfo.get("author")}\n')
                    searchedBookResults = searchInfo.get('books')
                    try:
                        for searchedBook in searchedBookResults:
                            self.roamLog.info(f'\tSearchedBook: {searchedBook.get("title")}')
                            searchedAuthors = searchedBook.get('authors')
                            collaborators = []
                            for author in searchedAuthors:
                                self.roamLog.info(f'\t\tSearchedAuthor: {author}')
                                authorList.append(author)
                                authObj = makeAuthor(author)
                                collaborators.append(authObj)
                                
                                bookCount += 1
                            self.roamLog.warning(f'Collab: {collaborators}')
                            makeBook(searchedBook, collaborators)
                    except TypeError as e:
                        self.roamLog.warning(f'Cannot find: {fileAuthor}')
                        pass
                
            return authorList

        authorCount = fillAuthors()
        print(authorCount)
        print(f'Number of Authors: {authorCount}')
        
        log.shutdown()
        


'''
Doesnt write over author
'''
