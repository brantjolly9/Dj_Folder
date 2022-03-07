import sys
sys.path.append('..')
from Django_Logger import DjangoLogger
from django.core.management.base import BaseCommand
from Library.Library_Browser.models import Book, Author


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
        mainLog = DjangoLogger(homePath = r'C:\Users\User\Documents\Programming\Python_stuff\Dj_Library')
        self.roamLog = mainLog.make_log(name='roam')
        self.makeAuthorLog = mainLog.make_log(name='make_author')
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
                int: Author.pk (Author's primary key)

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
                fullName['last'] = raw[0].replace(',', '')
                fullName['first'] = raw[1]
            elif len(raw) == 3:
                fullName['last'] = raw[0].replace(',', '')
                fullName['first'] = raw[1]
                fullName['middle'] = raw[2]
            self.makeAuthorLog.info(f'Full Name: {fullName}')

            # Check if Author(first, last) already exists
            try:
                
                existingAuthor = Author.objects.get(
                    first_name=fullName.get('first'),
                    last_name=fullName.get('last')
                    )
                self.makeAuthorLog.warn(f'Author with first={fullName.get("first")},  last={fullName.get("last")} already exists')

            # If doesnt exist: make new, save, return pk
            except Author.DoesNotExist as e:
                self.makeAuthorLog.exception(e)
                self.makeAuthorLog.warning('Creating new author')
                newAuthor = Author(
                    first_name="F_"+fullName.get('first'),
                    middle_initial="M_"+fullName.get('middle'),
                    last_name="L_"+fullName.get('last')
                )
                newAuthor.save()
                pk = newAuthor.pk
                self.makeAuthorLog.info(f'newAuthor.pk: {pk}')
                return pk

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
                            for author in searchedAuthors:
                                self.roamLog.info(f'\t\tSearchedAuthor: {author}')
                                authorList.append(author)
                                pk = makeAuthor(author)
                                bookCount += 1
                    except TypeError as e:
                        self.roamLog.warning(f'Cannot find: {fileAuthor}')
                        pass
                
            return authorList

        authorCount = fillAuthors()
        print(authorCount)
        print(f'Number of Authors: {authorCount}')
        
        log.shutdown()
        
        # for authorObject in Author.objects.all():
        #     # Collect all name values 
        #     fullName = [
        #     authorObject.first_name,
        #     authorObject.middle_initial,
        #     authorObject.last_name,
        #     ]
        #     pk = authorObject.pk
        #     print(fullName)
        #     searchName = ''

        #     # Only searches authors with <2 'z'
        #     if fullName.count('z') < 2:
        #         for i in fullName:
        #             if i != 'z':
        #                 searchName += i + ' '
        #         searchInfo = searchIsbn(searchName, 'author')

        #         try:

        #             # Get each book from author's booklist
        #             for result in searchInfo.get('books'): 
        #                 isbnLog.write('--Result--\n')
        #                 json.dump(result, isbnLog, indent=2)
        #                 isbnLog.write('----------\n')
        #                 lang = result.get('language')

        #                 # Gets results that dont have 'lang' or lang= en_US | English
        #                 if not lang or lang == 'en_US' or lang == 'English':
        #                     newBook = Book(
        #                         title=result.get('title'),
        #                         # titleLong=result.get('titleLong'),
        #                         imageLink=result.get('image'),
        #                         isbn=result.get('isbn'),
        #                         author=authorObject,               #! Pass newAuthor into Book model
        #                         # publishedDate=result.get('date_published')
        #                     )

        #                     # check if msrp exists; add
        #                     try: 
        #                         msrp = float(result.get('msrp'))
        #                         newBook.msrp = msrp
        #                     except Exception as e:
        #                         isbnLog.write('No MSRP\n')

        #                     # check if pageCount exists: add
        #                     try:
        #                         pageCount = int(result.get('pages'))
        #                         newBook.pageCount = pageCount
        #                     except Exception as e:
        #                         isbnLog.write('No PageCount')

        #                     isbnLog.write(f'Book: {newBook.title}\tWritten By: {authorObject.last_name}\nISBN: {newBook.isbn}\n')
        #                     newBook.save()
        #         except TypeError as e:
        #             print(searchName)
        #         except AttributeError as e:
        #             print(searchName)
                

'''
Doesnt write over author
'''
