from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.random_code import random_code
from django import forms
from django.contrib import auth
from app01.models import UserInfo


# Create your views here.


def index(request):
    return render(request, 'index.html', {'request': request})


def news(request):
    return render(request, 'news.html')


def login(request):
    return render(request, 'login.html')


def get_random_code(request):  # 获取验证码
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


def sign(request):
    return render(request, 'sign.html')


def logout(request):
    auth.logout(request)
    return redirect('/')
