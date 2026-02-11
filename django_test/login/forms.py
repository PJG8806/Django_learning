from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class LoginForm(forms.Form): # ModelForm은 자동으로 만들어 주는 부분 Form은 직접 또는 로그인시 사용
    username = forms.CharField(label='아이디')
    password = forms.CharField(label='비밀번호', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None


class SignUp(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ('password1', 'password2'):
            self.fields[field].help_text = ''

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
        labels = {
            'username' : '이름',
            'email': '이메일',
            'password1': '비밀번호',
            'password2': '비밀번호 확인',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@example.com'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호를 입력해주세요'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '비밀번호를 다시 입력해주세요'}),
        }