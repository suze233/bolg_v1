from django.forms import forms
from django.http import JsonResponse
from django.views import View
from api.views.login import clean_form
from app01.models import Comment


class CommentView(View):
    #  分布评论
    def post(self, request, nid):
        res = {
            'msg': '文章评论成功',
            'code': 412,
            'self': None
        }
        data = request.data
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)

        content = data.get('content')
        if not content:
            res['msg'] = '请输入评论内容'
            res['self'] = 'content'
            return JsonResponse(res)

        # 评论校验成功
        pid = data.get('pid')
        if pid:
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid,
                parent_comment_id=pid
            )
        else:
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid
            )
        res['code'] = 0
        return JsonResponse(res)
