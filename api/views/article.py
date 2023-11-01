import random

from django import forms
from django.views import View
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery

from api.views.login import clean_form
from app01.models import Tags, Articles, Cover


# 添加、编辑文章的验证
class AddArticleForm(forms.Form):
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    abstract = forms.CharField(required=False)  # 不进行为空验证
    cover_id = forms.IntegerField(required=False)
    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    # pwd_activate = forms.BooleanField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

    # 全局钩子 验证分类和文章密码
    def clean(self):
        category = self.cleaned_data['category']
        if not category:
            self.cleaned_data.pop('category')

        pwd = self.cleaned_data['pwd']
        if not pwd:
            self.cleaned_data.pop('pwd')

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if not abstract:
            # 获取正文前30个字符
            content = self.cleaned_data.get('content')
            if content:
                abstract = PyQuery(markdown(content)).text()[:30]
        return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if not cover_id:  # 没有封面随机选一张
            cover_set = Cover.objects.all().values('nid')
            cover_id = random.choice(cover_set)['nid']
        return cover_id


# 给文章添加标签
def add_article_tags(article_obj, tags):
    for tag in tags:
        tag_isdigit = tag.isdigit()
        if (tag_isdigit and not Tags.objects.filter(nid=tag)) or not tag_isdigit:
            tag_obj = Tags.objects.create(title=tag)
            article_obj.tag.add(tag_obj.nid)
        else:
            article_obj.tag.add(tag)


class ArticleView(View):
    # 添加文章
    def post(self, request):
        res = {
            'msg': '文章发布成功',
            'code': 233,
            'data': None
        }
        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 验证通过
        form.cleaned_data['author'] = self.request.user.username
        form.cleaned_data['source'] = self.request.user.username

        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        # 添加标签
        add_article_tags(article_obj, tags)

        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 编辑文章
    def put(self, request, nid):
        res = {
            'msg': '文章修改成功',
            'code': 233,
            'data': None
        }
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误'
            return JsonResponse(res)
        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            # 验证不通过
            res['self'], res['msg'] = clean_form(form)
            return JsonResponse(res)
        # 验证通过
        article_query.update(**form.cleaned_data)
        tags = data.get('tags')
        # 标签修改
        article_query.first().tag.clear()  # 删除所有标签
        add_article_tags(article_query.first(), tags)  # 重新添加标签

        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)

# 文章
# class ArticleView(View):
#     # 发布文章
#     def post(self, request):
#         res = {
#             'msg': '网站发布成功！',
#             'code': 233,
#             'data': None,
#         }
#         data: dict = request.data
#         title = data.get('title')
#         content = data.get('content')
#         abstract = data.get('abstract')
#         category = data.get('category_id')
#         cover_id = data.get('cover_id')
#         recommend = data.get('recommend')
#         pwd = data.get('pwd')
#         pwd_active = data.get('pwd_active')
#
#         if not content:
#             res['msg'] = '请输入文章内容'
#             return JsonResponse(res)
#
#         if not title:
#             res['msg'] = '请输入文章标题'
#             return JsonResponse(res)
#
#         extra = {
#             'title': title,
#             'content': content,
#             'recommend': recommend,
#             'status': 1,
#         }
#
#         if not abstract:
#             # 解析文本内容
#             abstract = PyQuery(markdown(content)).text()[:30]
#         extra['abstract'] = abstract
#
#         if category:
#             extra['category'] = category
#
#         if cover_id:
#             extra['cover_id'] = cover_id
#         else:
#             extra['cover_id'] = 1
#
#         if pwd_active:
#             if pwd:
#                 extra['pwd'] = pwd
#             else:
#                 res['msg'] = '请输入文章密码'
#                 return JsonResponse(res)
#
#         # 添加文章
#         article_obj = Articles.objects.create(**extra)
#
#         # 标签
#         tags = data.get('tags')
#         if tags:
#             for tag in tags:
#                 if not tag.isdigit():
#                     tag_obj = Tags.objects.create(title=tag)
#                     article_obj.tag.add(tag_obj)
#                 else:
#                     article_obj.tag.add(tag)
#
#         res['code'] = 0
#         res['data'] = article_obj.nid
#         return JsonResponse(res)
