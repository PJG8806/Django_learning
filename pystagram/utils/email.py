from django.core.mail import send_mail
from django.conf import settings

def send_email(subject, message, to_email):
    to_email = to_email if isinstance(to_email, list) else [to_email] # 리스트가 아니면 리스트로 만들어 준다
    # if isinstance(to_email, list): # 위 내용
    #     to_email = to_email
    # else:
    #     to_email = [to_email]


    send_mail(subject, message, settings.EMAIL_HOST_USER, to_email) # 이메일 보내는 부분( 제목 본문 보내는사람 받는사람)