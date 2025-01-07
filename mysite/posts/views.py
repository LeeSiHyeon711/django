import os
import uuid
from mysite import settings

from urllib.parse import quote
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages

from .models import Posts
from .form import PostCreateForm
from .form2 import PostUpdateForm

# 게시글 등록
def create_post(request):
    form = PostCreateForm()

    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.password = make_password(form.cleaned_data['password'])
            post.save()

            # 파일 업로드
            if request.FILES.get('uploadFile'):
                filename = uuid.uuid4().hex
                file = request.FILES.get('uploadFile')

                file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), str(filename))
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)

                post.filename = filename
                post.original_filename = file.name
                post.save()

            messages.success(request, '게시글이 등록되었습니다.')
            return redirect("posts:read", post_id=post.id)
        else:
            messages.error(request, '게시글 등록에 실패했습니다.')
    return render(request, 'posts/create.html', {'form': form})

# 게시글 보기
def get_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    return render(request, 'posts/read.html', {'post': post})

# 게시글 수정
def update_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    form = PostUpdateForm(instance=post)

    if request.method == 'POST':
        form = PostUpdateForm(request.POST, instance=post)

        if form.is_valid():
            if check_password(form.cleaned_data['password'], post.password):
                post = form.save(commit=False)
                post.password = make_password(form.cleaned_data['password'])
                post.save()
                messages.success(request, '게시글이 수정되었습니다.')
                return redirect('posts:read', post_id=post.id)
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.')
        else:
            messages.error(request, '게시글 수정에 실패했습니다.')

    return render(request, 'posts/update.html', {'form': form})

# 게시글 삭제
def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    password = request.POST.get('password')

    if request.method == 'POST':
        if check_password(password, post.password):
            post.delete()
            messages.success(request, '게시글이 삭제되었습니다.')
            return redirect('posts:list')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return redirect('posts:read', post_id=post.id)

# 게시글 목록
def get_posts(request):
    page = request.GET.get('page', '1')
    posts = Posts.objects.all().order_by('-created_at')

    searchType = request.GET.get('searchType', '')
    searchKeyword = request.GET.get('searchKeyword', '')

    if searchType and searchKeyword:
        if searchType == 'all':
            posts = posts.filter(
                Q(title__contains=searchKeyword) |
                Q(content__contains=searchKeyword) |
                Q(username__contains=searchKeyword)
            )
        elif searchType == 'title':
            posts = posts.filter(Q(title__contains=searchKeyword))
        elif searchType == 'content':
            posts = posts.filter(Q(content__contains=searchKeyword))
        elif searchType == 'username':
            posts = posts.filter(Q(username__contains=searchKeyword))

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)

    start_index = paginator.count - (paginator.per_page * (page_obj.number - 1))

    for index, post in enumerate(page_obj, start=0):
        post.index_number = start_index - index
    
    return render(request, 'posts/list.html', {
        'posts': page_obj,
        'searchType': searchType,
        'searchKeyword': searchKeyword
    })

# 첨부 파일 다운로드
def download_file(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    file_path = os.path.join(settings.MEDIA_ROOT, 'posts', str(post.id), post.filename)

    if os.path.exists(file_path):
        try:
            with open(file_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                encoded_filename = quote(post.original_filename)
                response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{encoded_filename}'
                return response
        except IOError:
            return HttpResponse(status=500)
    return HttpResponse(status=404)
