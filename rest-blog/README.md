

## 설정
```shell
$ cd config
$ ln -sf local.py settings.py
```

### Poetry 추출
```shell
$ poetry export --without-hashes --format=requirements.txt > requirements.txt
```

### 무료배포 사이트
```shell
https://www.pythonanywhere.com/
깃을 통해 서버에 다운 받고
$ pip install -r requirements.txt 
$ python manage.py collectstatic
설치 및 static_root로 모은기 
pwd로 현재 프로젝트 최상단 경로 가져와서 배포 사이트 웹에 들어가서
code -> Source code pwd 경로 삽입
wgrs 부분 클릭하여 
hellow 부분에서(19) urf-8 부분까지(47) 주석 처리
Django 부분 주석 해지(76)
path 부분에 pwd 경로를 입력
os.environ 부분 입력을 'config.settings'로 변경후 저장
하단에 static files 부분 URL-> /static/ directory는 모으기 했을때 나오는 경로 입력
만약 오류에서 패키지 설치 안되었다고 나오면 pip3.12 install --user 패키지명 으로 python 기본
부분에 설치 3.12는 사용할 파이썬 버전
```