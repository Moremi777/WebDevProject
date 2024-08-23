from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

def home(request):
    return render(request, 'home.html')


