from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01.utils.random_code import random_code
from django import forms
from django.contrib import auth
from app01.models import UserInfo
from app01.models import Articles, Tags, Cover


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


def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    if not article_query:
        return redirect('/')
    article = article_query.first()
    return render(request, 'article.html', locals())


def backend(request):
    if not request.user.username:  # 没有登陆
        return redirect('/')
    return render(request, 'backend/backend.html', locals())


def add_article(request):
    # 拿到所有分类标签，文章封面
    tag_list = Tags.objects.all()
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
        })

    return render(request, 'backend/add_article.html', locals())


def edit_avatar(request):
    return render(request, 'backend/edit_avatar.html', locals())


def reset_passwd(request):
    return render(request, 'backend/reset_passwd.html', locals())
