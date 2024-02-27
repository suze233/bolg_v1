from app01.models import Comment


def find_sub_comment(root_comment, sub_comment_list):
    for sub_comment in root_comment.comment_set.all():
        sub_comment_list.append(sub_comment)
        find_sub_comment(sub_comment, sub_comment_list)


def sub_comment_list(nid):
    comment_query = Comment.objects.filter(article_id=1).order_by('-create_time')
    comment_list = []

    for comment in comment_query:
        if not comment.parent_comment:
            c_list = []
            find_sub_comment(comment, c_list)
            comment.sub_comment = c_list
            comment_list.append(comment)
            continue
    return comment_list
