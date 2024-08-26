from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Document, Rating
from .forms import RatingForm
from .forms import FileUploadForm
#for upload files
from django.shortcuts import render, redirect #for upload files
from .forms import FileUploadForm #for upload files
from .models import UploadedFile #for upload file
from django.conf import settings
import os
from django.http import JsonResponse
from django.contrib.auth import login



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

def success(request):
    return render(request, 'fileupload/success.html')
 
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
 
def home(request):
    return render(request, 'home.html')

def search_results(request):
    query = request.GET.get('q')
    results = Document.objects.filter(name__icontains=query)  # Replace 'name' with the field you want to search
    return render(request, 'searchresults.html', {'results': results, 'query': query})

