from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
#for upload files
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from django.conf import settings
import os

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
