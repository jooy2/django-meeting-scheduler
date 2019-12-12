# Django-Meeting-Scheduler
Django 프레임워크를 사용한 회의 스케줄 관리 애플리케이션


## Key features
- 간편한 설치와 관리 기능
- 주간 회의 관리
- 내가 참여한 회의 한 눈에 보기
- 간편한 회의록 정리


## Dependencies
- Python 3.7.x
- Django 2.2.x


## Installation
다음 튜토리얼을 참고하여 Python 가상환경을 구성합니다.: https://docs.python.org/3/tutorial/venv.html

이후 다음 명령어를 사용하여 필수 패키지를 설치합니다.:
```shell script
(venv)$ pip install -r requirements.txt
```

데이터베이스 접속 및 원활한 실행 환경을 위해 환경변수가 담긴 secret.json 파일을 최상위 경로에 생성해야 합니다. secret.json 파일에는 다음과 같은 내용이 포함되어야 합니다.
```json
{
  "SECRET_KEY": "{{Django secret key}}",
  "DB_NAME": "{{Schema name}}",
  "DB_USER": "{{Username}}",
  "DB_PASSWORD": "{{Password}}",
  "DB_HOST": "{{Hostname}}",
  "DB_PORT": 3306
}
```

데이터베이스 환경을 구성한 후 meetscheduler 스키마를 생성합니다. 이후 다음 명령어로 마이그레이션 파일을 생성한 다음, 서버를 시작합니다.: 
```shell script
(venv)$ python manage.py makemigrations
(venv)$ python manage.py migrate
(venv)$ python managy.py runserver
```

관리자 권한을 가진 사용자가 필요한 경우 다음 명령어로 사용자를 생성할 수 있습니다. 일반 사용자는 회원가입 페이지에서 등록이 가능합니다.:
```shell script
(venv)$ python manage.py createsuperuser
```


## Contributors
프로젝트에 기여하고자 하는 경우 누구나 이슈를 제기하거나 Merge request를 보낼 수 있습니다.
* **leejooy96** (leejooy96@gmail.com)
* **jangdoll** (yunjang2@gmail.com)


## Roadmap
- [x] 회의 등록 페이지
- [x] 주간 회의 보기
- [x] 회의 일정 자세히 보기 및 수정
- [ ] 사용자 프로필 페이지
- [ ] 관리자 페이지
- [ ] 사이트 디자인 및 기능 설정
- [ ] 업로드 파일 관리


## License
```text
MIT License

Copyright (c) 2019 leejooy96, jangdoll

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```