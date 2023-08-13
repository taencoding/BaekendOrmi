from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

# test
# def test(request):
#     data = [
#         {'name': 'leehojun', 'age':10},
#         {'name': 'leehojun2', 'age':20}
#     ]
#     # return HttpResponse('hello world') # 1
#     # return HttpResponse('<h1>hello world</h1>') # 2
#     # 결국 render도 HttpResponse를 리턴합니다. :)
#     s = render_to_string('main/test.txt', {'data': data})
#     header = '<h2>hello world</h2>'
#     footer = '<h2>bye world</h2>'
#     return HttpResponse(header + s + footer) # 3
#     # return render(request, 'main/test.html')

# test
# FBV에서 사용하는 방법
# @api_view(['GET'])
# def test(request):
#     data = [
#         {'name': 'leehojun', 'age':10},
#         {'name': 'leehojun2', 'age':20}
#     ]
#     # return Response('hello')
#     return Response(data)

# CBV에서 사용하는 방법
class TestView(APIView):
    def get(self, request):
        data = [
            {'name': 'leehojun', 'age':10},
            {'name': 'leehojun2', 'age':20}
        ]
        return Response(data)
test = TestView.as_view()