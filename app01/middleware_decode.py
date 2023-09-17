from django.utils.deprecation import MiddlewareMixin
import json


class Md1(MiddlewareMixin):  # 解析POST请求
    # 请求中间件
    def process_request(self, request):
        if request.method == 'POST':
            data = json.loads(request.body, encoding='utf8')  # json请求存储在body中
            request.data = data

    # 响应中间件
    def process_response(self, request, response):
        return response
