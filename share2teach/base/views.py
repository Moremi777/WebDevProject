from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render, get_object_or_404
#from .models import Document, Rating
#from .forms import RatingForm
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
 

#for upload files begin
def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = UploadedFile(file=request.FILES['file'])  # Create an instance of the model
            uploaded_file.save()  # Save the file instance to the database
            return redirect('success')
    else:
        form = FileUploadForm()
    return render(request, 'fileupload/upload.html', {'form': form})

def success(request):
    return render(request, 'fileupload/success.html')

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'fileupload/file_list.html', {'files': files})
#for upload files end

 
def home(request):
    return render(request, 'home.html')

def search_results(request):
    query = request.GET.get('q')
    results = Document.objects.filter(name__icontains=query)  # Replace 'name' with the field you want to search
    return render(request, 'searchresults.html', {'results': results, 'query': query})

