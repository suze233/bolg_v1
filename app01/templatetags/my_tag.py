from django import template

# 注册
register = template.Library()


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name):
    img_list = [
        '/static/my/img/header/1.jpg',
        '/static/my/img/header/2.jpg',
        '/static/my/img/header/3.jpg',
        '/static/my/img/header/4.jpg',
        '/static/my/img/header/5.jpg',
    ]
    return {'img_list': img_list}