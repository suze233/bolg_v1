import os


def find_sub_comments(root_comment, sub_comment_list):
    for sub_comment in root_comment.comment_set.all():
        sub_comment_list.append(sub_comment)
        find_sub_comments(sub_comment, sub_comment_list)


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v1.settings")
    import django

    django.setup()

    from app01.models import Articles, Comment

    #  找到某个文章的所有评论
    comment_query = Comment.objects.filter(article_id=1)
    comment_list = []
    #
    for comment in comment_query:
        if not comment.parent_comment:
            c_list = []
            find_sub_comments(comment, c_list)
            comment.sub_comment = c_list
            comment_list.append(comment)
            continue
    print(comment_list)
    for c in comment_list:
        print(c, c.sub_comment)
