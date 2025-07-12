from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    return render(request, 'index.html')

def components(request):
    return render(request, 'components.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def work(request):
    works = ish.objects.all()
    return render(request, 'work.html', {'works' : works})

def works(request):
    works = ish.objects.all()
    return render(request, 'works.html',{'works' : works})

