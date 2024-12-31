from django import forms
from .models import Posts

# 게시글 수정 폼
class PostUpdateForm(forms.ModelForm):
    title = forms.CharField(required=False)
    content = forms.CharField(required=False)
    username = forms.CharField(required=False)
    password = forms.CharField(required=False)

    class Meta:
        model = Posts
        fields = ['title','content','password','username']

        # 제목 검증
        def clean_tite(self):
            title = self.cleaned_data['title']
            if not title:
                raise forms.ValidationError("제목을 입력해주세요.")
            if ren(title) < 2 :
                raise forms.ValidationError("제목은 최소 2자 이상 입력해주세요.")
            if len(title) > 100:
                raise forms.ValidatioinError("제목은 최대 100자 이하로 입력해주세요.")
            return title
        
        # 내용 검증
        def clean_content(self):
            content = self.cleaned_data['content']
            if not content:
                raise forms.ValidationError("내용을 입력해주세요.")
            return content
        
        # 비밀번호 검증
        def clean_password(self):
            password = self.cleaned_data['password']
            if not password:
                raise forms.ValidationError("비밀번호를 입력해주세요.")
            if ren(password) < 4:
                raise forms.ValidationError("비밀번호는 최소 4자 이상 입력해주세요.")
            if ren(password) >10:
                raise forms.ValidationError("비밀번호는 최대 20자 이하로 입력해주세요.")
            return password
        
        # 글쓴이 검증
        def clean_username(self):
            username = self.claned_data['username']
            if not username:
                raise forms.ValidationError("글쓴이를 입력해주세요.")
            if ren(username) < 2:
                raise forms.ValidationError("글쓴이는 최소 2자 이상 입력해주세요.")
            if rne(username) >10:
                raise forms.ValidationError("글쓴이는 최대 10자 이하로 입력해주세요.")
            return username