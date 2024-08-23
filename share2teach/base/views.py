from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Document, Rating
from .forms import RatingForm

def home(request):
    return render(request, 'home.html')

# Create your views here.
from django.shortcuts import render

def register(request):
    # Your registration logic here
    return render(request, 'register.html')

def login(request):
    # Your registration logic here
    return render(request, 'login.html')

def home_view(request):
    documents = Document.objects.all()
    return render(request, 'home.html', {'documents': documents})

def document_detail_view(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    form = RatingForm(request.POST or None)
    if form.is_valid():
        rating = form.save(commit=False)
        rating.document = document
        rating.save()
    return render(request, 'document_detail.html', {'document': document, 'form': form})