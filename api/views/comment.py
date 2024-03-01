from django.db.models import F
from django.forms import forms
from django.http import JsonResponse
from django.views import View

from api.utils.find_root_comment import find_root_comment
from api.views.login import clean_form
from app01.models import Comment, Articles


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
        # 文章评论数加1
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)

        if pid:
            # 不是根评论
            comment_obj = Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid,
                parent_comment_id=pid
            )
            # 根评论加1
            # 找根评论root
            root_comment_obj = find_root_comment(comment_obj)
            root_comment_obj.comment_count += 1
            root_comment_obj.save()
        else:
            # 根评论
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid
            )
        res['code'] = 0
        return JsonResponse(res)

    def delete(self, request, nid):
        # 自己的发布的评论才能删除或者超级管理员
        res = {
            'msg': '评论删除成功',
            'code': 412,
        }

        login_user = request.user
        comment_query = Comment.objects.filter(nid=nid)
        comment_user = comment_query.first().user
        if login_user == comment_user or login_user.is_superuser:
            # 可以删除
            # 找根评论root
            root_comment_obj = find_root_comment(comment_query.first())
            root_comment_obj.comment_count -= 1
            root_comment_obj.save()
            # 文章评论数-1
            aid = comment_query.first().article.nid
            Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - 1)

            comment_query.delete()
            res['code'] = 0
            return JsonResponse(res)

        res['msg'] = '用户验证失败'
        return JsonResponse(res)

