from django.http import JsonResponse
from django.shortcuts import render
import json

# Create your views here.


def index(request):

    return render(request, 'index.html')


def news(request):
    return render(request, 'news.html')


def login(request):
    if request.method == 'POST':
        data = request.data
        print(data)
        return JsonResponse(data)
    return render(request, 'login.html', locals())


def sign(request):
    return render(request, 'sign.html')
