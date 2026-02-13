from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False
    bucket_name = 'oz-pystagram'
    custom_domain = f'{bucket_name}.s3.amazonaws.com'

    # python manage.py collectstatic
    # python manage.py collectstatic --settings=config.prod
    # aws에 s3 에 설정으로 폴더 업로드

    # certbot 에서 사용방법으로 사용시 http -> https로 변경 2달마다 갱신을 해줘야 한다
    # 리눅스 크론탭 스캐줄로 주기적으로 가능하게 추가해주는 방법 이 방법으로 주기적으로 갱신 하게 한다