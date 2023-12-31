"""
URL configuration for v1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path
from app01 import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('news/', views.news),
    path('login/', views.login),
    path('login/random_code/', views.get_random_code),
    path('sign/', views.sign),
    path('logout/', views.logout),
    path('backend/', views.backend),  # 个人中心
    path('backend/edit_avatar/', views.edit_avatar),  # 修改头像
    path('backend/reset_passwd/', views.reset_passwd),  # 修改密码
    path('backend/add_article/', views.add_article),  # 添加文章
    re_path(r'^backend/edit_article/(?P<nid>\d+)/', views.edit_article),  # 编辑文章

    re_path(r'^article/(?P<nid>\d+)/', views.article),  # 文章页
    # 路由分发，将所有api开头的请求分发出去
    re_path(r'^api/', include('api.urls')),
    # 用户上传文件
    re_path(r'media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
