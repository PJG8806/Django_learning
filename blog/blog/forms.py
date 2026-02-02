from django import forms

from blog.models import Blog, Comment


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content')  # 전체'__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control'}) # 화면에 어떻게 나타낼지 설정
            #attrs는 html에 안에 어떻게 넣어줄지 (input class='form-contral' 위 코드로 이렇게 들어간다)
        }
        labels = {
            'content': '댓글'
        }