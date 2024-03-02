from django.db.models import F
from django.forms import forms
from django.http import JsonResponse
from django.views import View

# from api.utils.find_root_comment import find_root_comment
from api.views.login import clean_form
from app01.models import Comment, Articles


# 所有父评论的回复数都+1
def comment_count_add(comment):
    parent_comment = comment.parent_comment
    if parent_comment:
        parent_comment.comment_count += 1
        parent_comment.save()
        return comment_count_add(parent_comment)


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
            # 所有父评论的回复数都+1
            comment_count_add(comment_obj)
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
        res = {
            'msg': '评论删除成功',
            'code': 412,
        }

        login_user = request.user
        comment_query = Comment.objects.filter(nid=nid)
        comment_user = comment_query.first().user
        # 文章id
        aid = request.data.get('aid')
        # 评论的最终根评论id
        pid = request.data.get('pid')
        # 自己的发布的评论才能删除或者超级管理员
        if not (login_user == comment_user or login_user.is_superuser):
            res['msg'] = '用户验证失败'
            return JsonResponse(res)

        # 可以删除
        count = comment_query.first().comment_count  # 子评论数
        if pid:  # 删除的是子评论
            # -根评论的回复数
            Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') - count - 1)
        # -文章评论数
        Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - count - 1)

        comment_query.delete()
        res['code'] = 0
        return JsonResponse(res)
