from django import template

# 注册
register = template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, article=None):
    img_list = [
        '/static/my/img/header/1.jpg',
        '/static/my/img/header/2.jpg',
        '/static/my/img/header/3.jpg',
        '/static/my/img/header/4.jpg',
        '/static/my/img/header/5.jpg',
    ]
    if article:  # 说明是文章页
        cover = article.cover.url.url
        img_list = [cover]
        pass
    return {'img_list': img_list}