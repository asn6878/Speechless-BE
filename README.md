# 진행 과정 아래 링크에서 확인 가능합니다.
https://chief-longship-e57.notion.site/4b76388dee2a4cd8a6091545656d269a?v=f04c81a7b9604464a4664cca71a20b43&pvs=4

### Speechless-BE Developers
|Name|GitHub|
|------|---|
|__안성윤__|[asn6878](https://github.com/asn6878)|
|__김경민__|[Tibet-Fox](https://github.com/Tibet-Fox)|

Database는 개발 동안 원활한 테스트를 위해 sqlite3를 사용중입니다.<br><br>





## 로컬환경에서 사용하는 방법 (FE 개발간 연동시 참고!) 🎈
1. `git clone https://github.com/Likelion-YeungNam-Univ/Speechless-BE.git` (프로젝트파일 받아오기)
2. `cd Speechless-BE` (프로젝트 디렉토리로 이동하기)
3. `python -m venv venv` 혹은 `python3 -m venv venv` (파이썬 가상환경 생성하기)
4. `pip install -r requirements.txt` (의존 라이브러리 설치하기)
5. BE 팀원에게 `mysettings.py` 파일을 받아 Speechless-BE 디렉토리에 넣어두기
6. `source venv/script/activate` 혹은 `source venv/bin/activate` (가상환경 실행하기)
7. `python manage.py runserver` 혹은 `python3 manage.py runserver` (서버 실행하기)
   ```
   ...
   System check identified no issues (0 silenced).
   August 00, 2000 - 00:00:00
   Django version 4.2.3, using settings 'config.settings'
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CTRL-BREAK.
   ```
나올시 실행성공. 127.0.0.1:8000 (로컬호스트) 로 api 요청 가능!