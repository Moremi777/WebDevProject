from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Document, Rating
from .forms import RatingForm
#for upload files
from django.shortcuts import render, redirect #for upload files #for upload files
from .models import UploadedFile #for upload file
from django.conf import settings
import os
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Document, Report, Message
from .forms import ReportForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.core.files.storage import default_storage
from .forms import DocumentUploadForm
from .utils import add_watermark  
from django.core.files.storage import FileSystemStorage
from .forms import DocumentUploadForm
from .utils import add_watermark
from .utils import add_pdf_watermark
from PIL import UnidentifiedImageError


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
            # Get the uploaded file from the form
            file = request.FILES['file']
            
            # Save the file to Azure File Storage using the custom storage backend
            filename = default_storage.save(f'uploads/{file.name}', file)
            
            # Create an instance of the model and save the file URL to the database
            uploaded_file = UploadedFile(file=filename)  # Save the path or URL
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

def search_results(request):
    query = request.GET.get('q')
    results = Document.objects.filter(name__icontains=query)  # Replace 'name' with the field you want to search
    return render(request, 'searchresults.html', {'results': results, 'query': query})


def subject_documents(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    documents = Document.objects.filter(subject=subject)
    return render(request, 'subject_documents.html', {'subject': subject, 'documents': documents})

def report_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.document = document
            report.save()

            # Create a message for the admin
            message_content = f"The document '{document.title}' has been reported. Reason: {report.reason}"
            if report.submitted_by:
                message_content += f" Submitted by: {report.submitted_by}"
            Message.objects.create(report=report, content=message_content)

            messages.success(request, 'Report submitted successfully.')
            return redirect('document_detail', document_id=document.id)
    else:
        form = ReportForm()

    return render(request, 'report_document.html', {'form': form, 'document': document})


@staff_member_required
def view_messages(request):
    messages = Message.objects.filter(is_read=False).order_by('-created_at')
    return render(request, 'view_messages.html', {'messages': messages})

@staff_member_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    messages.success(request, 'Message deleted successfully.')
    return redirect('view_messages')

@staff_member_required
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_read = True
    message.save()
    messages.success(request, 'Message marked as read.')
    return redirect('view_messages')


from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from django.http import HttpResponse

def metrics_view(request):
    metrics_page = generate_latest()
    return HttpResponse(metrics_page, content_type=CONTENT_TYPE_LATEST)


def document_detail(request, document_id):
    document = get_object_or_404(Document, pk=document_id)
    session_id = request.session.session_key

    # Ensure the session exists
    if not session_id:
        request.session.create()

    # Check if this session has already rated the document
    existing_rating = Rating.objects.filter(session_id=session_id, document=document).first()

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid() and not existing_rating:  # Only allow if the session hasn't rated this document
            rating = form.save(commit=False)
            rating.session_id = session_id
            rating.document = document
            rating.save()

            # Update document's rating data
            document.ratings_sum += rating.rating
            document.total_ratings += 1
            document.avg_rating = document.calculate_average_rating()
            document.save()

            return redirect('document_detail', document_id=document.id)
    else:
        form = RatingForm()

    context = {
        'document': document,
        'form': form,
        'avg_rating': document.calculate_average_rating(),
        'existing_rating': existing_rating,
    }
    return render(request, 'document_detail.html', context)

def upload_document(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded document to the database
            uploaded_document = form.save()

            # Get the uploaded file
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            file_path = fs.save(uploaded_file.name, uploaded_file)

            # Determine file extension to handle images and PDFs separately
            _, file_extension = os.path.splitext(uploaded_file.name)

            try:
                if file_extension.lower() in ['.jpg', '.jpeg', '.png']:  # Image files
                    watermark_text = "© Share2Teach | NWU"
                    output_image_path = fs.path(file_path)  # Same file path for saving the updated file
                    add_watermark(fs.path(file_path), output_image_path, watermark_text)
                elif file_extension.lower() == '.pdf':  # PDF files
                    watermark_pdf_path = fs.path("'O:\CMPG 323 IT DEVELOPMENT\backend\WebDevProject\share2teach\base\static\nwu-licence.pdf")  # Path to watermark PDF
                    add_pdf_watermark(fs.path(file_path), fs.path(file_path), watermark_pdf_path)
                else:
                    messages.error(request, 'Unsupported file format for watermarking.')
                    return redirect('document_upload')

                messages.success(request, 'Document uploaded and watermarked successfully!')
            except UnidentifiedImageError:
                messages.error(request, 'Error identifying the image file.')
            except Exception as e:
                messages.error(request, f'An error occurred: {e}')

            return redirect('document_list')  # Redirect to the document list
    else:
        form = DocumentUploadForm()

    return render(request, 'fileupload/upload.html', {'form': form})

def document_list(request):
    documents = Document.objects.all()
    return render(request, 'document_list.html', {'documents': documents})


def report_document(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.document = document
            report.save()
            return redirect('document_detail', id=document_id)  # Redirect after submission
    else:
        form = ReportForm()

    return render(request, 'report_document.html', {'form': form, 'document': document})
