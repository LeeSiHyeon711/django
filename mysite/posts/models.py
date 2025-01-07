from django.db import models

# 게시글 모델
class Posts(models.Model):
    title = models.CharField(verbose_name="제목", max_length=100)
    content = models.TextField(verbose_name="내용")
    password = models.CharField(verbose_name="비밀번호", max_length=100)
    username = models.CharField(verbose_name="글쓴이", max_length=10)
    filename = models.CharField(verbose_name="파일명", max_length=100, null=True, blank=True)
    original_filename = models.CharField(verbose_name="원본파일명", max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="작성일시", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="수정일시", auto_now=True)

    class Meta:
        db_table = "posts"
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
    
    def __str__(self):
        return self.title