from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
 
from django.shortcuts import render, get_object_or_404
from .models import Document, Rating
from .forms import RatingForm
 
#for upload files
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from django.conf import settings
import os
 
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from .forms import RegistrationForm
from .models import CustomUser
from .forms import LoginForm
from .utils import send_verification_code  
from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer

# VIEWS START HERE
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
 

def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to a dashboard or home page
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = False
            user.save()
            send_verification_code(user)
            return redirect('verify_account')
    else:
        form = RegistrationForm()
        print(form)  # Debugging line
    return render(request, 'auth/register.html', {'form': form})

 
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
 
#for upload files
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_path = os.path.join(settings.MEDIA_ROOT, file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return redirect('success')
    else:
        form = FileUploadForm()
    return render(request, 'fileupload/upload.html', {'form': form})

def success(request):
    return render(request, 'fileupload/success.html')
 
def verify_account(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            user = CustomUser.objects.get(verification_code=code)
            user.is_active = True
            user.save()
            return redirect('login')
        except CustomUser.DoesNotExist:
            # Handle error (e.g., render with an error message)
            pass
    return render(request, 'auth/verify.html')
 
def home(request):
    return render(request, 'home.html')

def search_results(request):
    query = request.GET.get('q')
    results = Document.objects.filter(name__icontains=query)  # Replace 'name' with the field you want to search
    return render(request, 'searchresults.html', {'results': results, 'query': query})

