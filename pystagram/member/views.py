from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import signing
from django.core.signing import TimestampSigner, SignatureExpired
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import FormView, DetailView

from member.forms import SignupForm, LoginForm
from member.models import UserFollowing
from utils.email import send_email

User = get_user_model()


class SignupView(FormView):
    template_name = 'auth/signup.html'
    form_class = SignupForm
    #success_url = reverse_lazy('signup_done')

    def form_valid(self, form):
        user = form.save()
        signer = TimestampSigner()
        signed_user_email = signer.sign(user.email)
        signer_dump = signing.dumps(signed_user_email)
        # print(signer_dump)
        #
        # decoded_user_email = signing.loads(signer_dump)
        # print(decoded_user_email)
        # email = signer.unsign(decoded_user_email, max_age=60 * 30)
        # print(email) #복호화는 다른 곳에서
        # http://localhost:8000/verify/?code=asdasdsa
        url = f'{self.request.scheme}://{self.request.META["HTTP_HOST"]}/verify/?code={signer_dump}' # 배포할때 url 바뀌는걸 자동으로 해주기 위해
        if settings.DEBUG: # 개발할때 print(url) 찍어서 확인 테스트
            print(url)
        else: # 개발 아니면 이메일 발송
            subject = '[Pystagram]이메일 인증을 완료해주세요'
            message = f'다음 링크를 클릭해주세욤 <a href="{url}">{url}</a>'

            send_email(subject, message, user.email)

        return render(
            self.request,
            template_name='auth/signup_done.html',
            context={'user': user}
        )

def verify_email(request): # SignupView form_valid url의 code 값을 가져온다
    cod = request.GET.get('code', '') # 코드가 없으면 공백 추가

    signer = TimestampSigner()
    try:
        decoded_user_email = signing.loads(cod)
        email = signer.unsign(decoded_user_email, max_age=60 * 30)
    except (TypeError, SignatureExpired):
        return render(request, 'auth/not_verified.html')

    user = get_object_or_404(User, email=email, is_active=False) # 활성화가 안된 유저 가져와서
    user.is_active = True # 활성화
    user.save()
    # TODO: 나중에 Redirect 시키기
    # return redirect(reverse('login'))
    return render(request, 'auth/email_verified_done.html', {'user': user})

class LoginView(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        # email = form.cleaned_data['email']
        # user = User.objects.get(email=email)
        # login(self.request, user)
        user = form.user # forms에서 __init__ 추가하면 다시 불러오지 않아도 된다 clean에 authenticate가 db불러오기 때문에
        login(self.request, user)

        next_page = self.request.GET.get('next')
        if next_page:
            return HttpResponseRedirect(next_page)
        return HttpResponseRedirect(self.get_success_url())

class UserProfileView(DetailView):
    model = User
    template_name = 'profile/detail.html'
    slug_field = 'nickname' # nickname 컬럼 슬러그 필드에서 찾아서 매칭한다, slug로 받은 값으로 컬럼 nickname에서 조회한다
    slug_url_kwarg = 'slug' # slug 키로 받아서 (url에 slug 입력 또는 urls.py 에서 <str:slug> 방식으로 값을 받는 설정)
    queryset = User.objects.all()\
        .prefetch_related('post_set', 'post_set__images', 'following', 'followers')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data['is_follow'] = UserFollowing.objects.filter(
                to_user=self.object,
                from_user=self.request.user
            )

        return data


class UserFollowingView(LoginRequiredMixin,View):
    def post(self, *args, **kwargs):
        pk = kwargs.get('pk',0) # kwargs는 딕셔너리
        to_user = get_object_or_404(User, pk=pk)

        if to_user == self.request.user: # 나 자신이 팔로우 하면
            raise Http404()

        following, created = UserFollowing.objects.get_or_create( # 있으면 가져오고 없으면 만든다
            to_user= to_user,
            from_user= self.request.user,
        ) # models에서 두 필드가 중복 막는 설정 추가로 if문 없이 값을 가져오면 밑에 삭제 처리를 한다

        if not created:
            following.delete()

        return HttpResponseRedirect(
            reverse('profile:detail', kwargs={'slug':to_user.nickname})
        )


        # 이미 팔로우가 되어 있으면 팔로우 취소 ==> UserFollowing row 삭제
        # 안되어 있으면 팔로우 시작 => UserFollowing row 생성