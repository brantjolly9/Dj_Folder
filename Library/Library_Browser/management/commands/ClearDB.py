from django.core.management.base import BaseCommand
from Library_Browser.models import Author, Book
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
        print(f'1: Clear All\n2: Clear Authors\n3: Clear Books\n0: Clear None')
        
        # choice = int(input('Enter Choice: '))
        choice = None
        while not choice:
            i = input('Enter Choice: ')
            try:
                choice = int(i)
                if choice < 0 or choice > 3:
                    choice = None
            except ValueError:
                pass

        if choice == 0:
            return None

        elif choice == 1:
            try:
                deletedAuths = Author.objects.all().delete()
                print(len(deletedAuths))
            except Exception:
                print('1 Author failed')
                
            try:
                deletedBooks = Book.objects.all().delete()
                print(len(deletedBooks))
            except Exception as e:
                print('1 Book Failed')

        elif choice == 2:
            try:
                deletedAuths = Author.objects.all().delete()
                pprint(deletedAuths)
            except Exception as e:
                print('2 Auth Failed')

        elif choice == 3:
            try:
                deletedBooks = Book.objects.all().delete()
                print(len(deletedBooks))
            except Exception as e:
                print(f'3 Book Failed')
            