from django.shortcuts import render


# Create your views here.
def index(request):
    context = {}
    
    return render(request, 'browser/index.html', context=context)
    
def authors_home(request):
    context = {}
    return render(request, 'browser/author_home.html', context=context)

def author_detail(request):
    pass

def books_home(request):
    pass

def book_detail(request):
    pass
