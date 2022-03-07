from django.core.management.base import BaseCommand
from Library.Library_Browser.models import Author
import os
import json
from pprint import pprint

'''
python manage.py InitialAuthorFill

run to grab authors from bookInfo and fill models
'''

class Command(BaseCommand):
    help = 'initial database fill'

    # Dont know
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        # chdir to books and list file names
        bookInfoPath = 'C:\\Users\\User\\Documents\\Programming\\Python_stuff\\LibraryBuilder\\Book_Info_Json'
        bookInfo = os.listdir(bookInfoPath)
        os.chdir(bookInfoPath)

        # Sort Authors by number of names and fill model accordingly
        for book in bookInfo[:5]:
            with open(book, 'r') as b:
                info = json.load(b)
            authors = info.get('authors')
            for a in authors:
                names = a.split(' ')
                if len(names) > 2:
                    mi = names[1].replace('.', '')
                    
                    new_author = Author(first_name= names[0],
                                        middle_initial= mi,
                                        last_name= names[2])
                else:
                    new_author = Author(first_name= names[0],
                                        last_name= names[1])
                new_author.save()
