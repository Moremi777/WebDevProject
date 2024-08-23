from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import FAQ
from .forms import FAQForm


# Create your views here.
# FAQ VIEWS STARTS HERE
def faq_list(request):
    faqs = FAQ.objects.filter(status='published').order_by('priority')
    return render(request, 'faq_list.html', {'faqs': faqs})

def faq_detail(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    return render(request, 'faq_detail.html', {'faq': faq})

def faq_create(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('faq_list')
    else:
        form = FAQForm()
    return render(request, 'faq_form.html', {'form': form})

def faq_update(request, pk):
    faq = get_object_or_404(FAQ, pk=pk)
    if request.method == 'POST':
        form = FAQForm(request.POST, instance=faq)
        if form.is_valid():
            form.save()
            return redirect('faq_detail', pk=faq.pk)
    else:
        form = FAQForm(instance=faq)
    return render(request, 'faq_form.html', {'form': form})
# FAQ VIEWS ENDS HERE