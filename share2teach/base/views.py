from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
#for upload files
from django.shortcuts import render, redirect #for upload files
from .forms import FileUploadForm #for upload files
from .models import UploadedFile #for upload file
from django.conf import settings
import os


def home(request):
    return render(request, 'home.html')


#for upload files
def upload_file(request):#for upload files
    if request.method == 'POST':#for upload files
        form = FileUploadForm(request.POST, request.FILES)#for upload files
        if form.is_valid():#for upload files
            uploaded_file = UploadedFile(file=request.FILES['file'])  # Create an instance of the model #for upload files
            uploaded_file.save()  # Save the file instance to the database #for upload files
            return redirect('success')#for upload files
    else: #for upload files
        form = FileUploadForm() #for upload files
    return render(request, 'fileupload/upload.html', {'form': form}) #for upload files

def success(request): #for upload files
    return render(request, 'fileupload/success.html') #for upload files

def file_list(request): #for upload files/view file
    files = UploadedFile.objects.all() #for upload files/view files
    return render(request, 'fileupload/file_list.html', {'files': files}) #for upload files/ view files

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

