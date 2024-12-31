from django.shortcuts import render
from django.http import HttpResponse

from .models import Posts

# 게시글 등록
def create_post(request):
    return HttpResponse('게시글 등록')

# 게시글 보기
def get_post(request, post_id):
    return HttpResponse('게시글 보기')

# 게시글 수정
def update_post(request, post_id):
    return HttpResponse('게시글 수정')

# 게시글 삭제
def delete_post(request, post_id):
    return HttpResponse('게시글 삭제')

# # 게시글 목록
# def get_posts(request):
#     return HttpResponse('게시글 목록')

# 게시글 목록
def get_posts(request):
    posts = Posts.objects.all().order_by('-created_at')
    return render(request, 'posts/list.html', {'posts':posts})