from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView
from django.contrib.auth import login
from users.forms import SignupForm, LoginForm
from users.models import User
from utils.email import send_email


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "registration/signup.html"

    def form_valid(self, form):
        user = form.save()
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signed_dump = signing.dumps(signed_user_email)
        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/users/verify/?code={signed_dump}'

        subject = f'[Todo]{user.email}님의 이메일 인증을 완료해주세요'
        message = f'다음 링크를 클릭해주세요 "{url}"'

        send_email(subject, message, user.email)

        return render(
            self.request,
            template_name= 'registration/signup_done.html',
            context={'user':user}
        )
def verify_email(request):
    cod = request.GET.get('code', '')
    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(cod)
        email = signer.unsign(decoded_user_email, max_age=60 * 30)
    except(TypeError, SignatureExpired):
        return render(request, 'user/not_verifiex.html')

    user = get_object_or_404(User, email=email, is_active=True)
    user.is_active = True
    user.save()
    return render(request, 'registration/verify_success.html')

class LoginView(FormView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('todo:cbv_todo_list')

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user=user)
        return HttpResponseRedirect(self.get_success_url())