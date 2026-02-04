from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()# settings 에 AUTH_USER_MODEL 설정을 가져오며 없으면 기본 유저 사용

class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs): # 폼의 정보를 바꾼다
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            # if field.startswith('password'):
            #     self.fields[field].label = '비밀번호'
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = 'password'
            if field == 'password1':
                self.fields[field].label = '비밀번호'
            else:
                self.fields[field].label = '비밀번호 확인'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'nickname')
        labels = {
            'email': '이메일',
            'nickname': '닉네임',
        }
        widgets = {
            'email': forms.EmailInput(
                attrs={
                    'placeholder': 'example@example.com',
                    'class': 'form-control'
                }
            ),
            'nickname': forms.TextInput(
                attrs={
                    'placeholder': '닉네임',
                    'class': 'form-control',
                }
            )
        }

class LoginForm(forms.Form): # ModelForm 사용 안하는 이유는 save 할때 유저가 저장된다 Form은 필드를 입력 해줘야 한다
    email = forms.CharField(
        label = '이메일',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'example@example.com',
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        label='패스워드',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean() # is_valid 한뒤 clean 데이터가 나온다
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        self.user = authenticate(email=email, password=password)

        if not self.user.is_active:
            raise forms.ValidationError('유저가 인증되지 않았습니다.')
        return cleaned_data


