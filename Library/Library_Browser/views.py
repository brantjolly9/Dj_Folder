from django.shortcuts import get_object_or_404, render
from Library_Browser.models import Author, Book


# Create your views here.
def index(request):
    context = {}
    
    return render(request, 'browser/index.html', context=context)
    
def authors_home(request):
    context = {}
    return render(request, 'browser/author_home.html', context=context)

def author_detail(request, pk):
    authorDetail = get_object_or_404(Author, pk=pk)
    context = {'author': author_detail}
    return render(request, 'browser/author_detail.html', context=context)
    

def books_home(request):
    pass

def book_detail(request):
    pass
