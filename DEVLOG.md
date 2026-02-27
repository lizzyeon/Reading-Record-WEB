# 📒 BOOKSNAP Development Log

## 2026-02-26

<div style="display: flex; justify-content: center; gap: 20px;">
  <img src="static/d_images/2026-02-26-1.png" width="500">
  <img src="static/d_images/2026-02-26-2.png" width="500">
</div>

### 🧾 Join / Login 화면 UI 구현
- Bootstrap form-floating 구조를 활용해 입력 폼 구성
  - 기본 height만 수정 시 스타일이 적용되지 않는 문제 발생
  - form-floating은 height, min-height, padding 등이 동시에 계산되도록 설계되어 있어
    height만 수정 시 min-height 규칙에 의해 무시되기 때문
  - Bootstrap의 min-height, padding, label transform 구조까지 함께 수정하여 정상 동작 구현


📌 **배운 점**
- Bootstrap 컴포넌트는 단순한 스타일 모음이 아니라 여러 CSS 속성이 서로 연결되어 동작하는 구조적 시스템임을 이해
- 특정 속성(height)만 수정하면 다른 속성(min-height, padding, transform 등)에 의해 동작이 유지되거나 깨질 수 있다는 점을 경험
- 원하는 UI를 구현하려면 개별 속성 수정이 아니라 컴포넌트 전체 동작 구조를 파악한 뒤 함께 조정해야 함을 이해
<br><br><br><br>

---

## 2026-02-24

<img src="static/d_images/2026-02-24-1.png" width="500">
<img src="static/d_images/2026-02-24-2.png" width="500">

### 📝 Modal2 공유 기능 구현 및 서버 연동
- '#feed_create_button' 클릭 이벤트 구현
- textarea에 입력한 글(content), 업로드한 이미지 파일(file), 작성자 정보(user_id, profile_image)를 jQuery로 수집
- FormData 객체를 생성하여 파일과 텍스트 데이터를 함께 구성
- $.ajax()를 사용해 /content/upload 경로로 POST 요청 전송
- 요청 완료 후 location.replace("/main")로 메인 페이지 재이동 처리

### 🔗 urls.py 경로 연결
- /content/upload 경로를 UploadFeed 뷰와 연결하여 AJAX 요청이 처리되도록 설정
- 🛠 views.py 파일 저장 및 DB 생성
- request.FILES['file']로 이미지 파일 수신
- request.data.get()으로 글 내용 및 사용자 정보 수신
- MEDIA_ROOT 경로에 파일 저장 (uuid 기반 파일명 사용)
- Feed.objects.create()로 새로운 피드 데이터 DB 저장
- Response(status=200) 반환하여 요청 성공 처리

### 🗂 settings.py 및 미디어 경로 설정
- settings.py에 MEDIA_ROOT, MEDIA_URL 설정 추가
- MEDIA_ROOT를 기준으로 업로드 이미지가 media 폴더에 저장되도록 저장 경로 구성
- MEDIA_URL을 활용하여 {% get_media_prefix %}{{ feed.image }} 형태로 이미지 경로를 구성, media 폴더의 파일이 화면에 출력되도록 처리
- uuid 기반 파일명을 생성하여 업로드 파일명 중복 방지

📌 **배운 점**
- (공유하기 클릭 → 데이터 모아서 → 서버에 보내고 → 서버가 저장 → 다시 화면에 보여줌)
- 공유하기 클릭 → <브라우저 JS>  FormData 생성 → AJAX 이용, POST 방식으로 '/content/upload'에 전송 
              → <Django 서버> (urls.py) url(/content/upload)과 UploadFeed와 연결 
                           → (views.py) 'def post(self, request)' 실행(request에서 데이터 꺼내기) 
                           → 'media'에 파일 저장 + 'Feed.objects.create()'로 DB 저장 → 응답 반환 
              → <브라우저>    '/main'으로 이동

- AJAX를 통해 페이지 새로고침 없이 서버와 비동기 통신이 가능함을 이해
<br><br><br><br>

---

## 2026-02-23

<img src="static/d_images/2026-02-23-1.png" width="500">
<img src="static/d_images/2026-02-23-2.png" width="500">

### 🪟 Drop 이후 모달 전환 로직 구현(second_modal)
- first_modal, second_modal로 id를 분리하여 모달 상태를 구분
- 이미지 파일이 정상적으로 감지되면 #first_modal은 display: none, #second_modal은 display: flex로 변경
- 기존 e.target 대신 .img_upload_space 선택자로 변경하여 모달 전환 후에도 정상적으로 이미지가 표시되도록 수정
- second_modal에서 왼쪽(70%) 이미지 창과 오른쪽(30%) 글쓰는 창 배치
- second_modal에서 flex 레이아웃을 적용해 이미지(70%)와 글쓰기 영역(30%)을 분리

📌 **배운 점**
- 모달에 id를 지정하여 JS에서 특정 요소를 제어 할 수 있음
- e.target을 .img_upload_space를 사용하여, 드롭 위치가 아닌 second_modal 기준으로 이미지가 표시됨을 이해
<br><br><br><br>

---

## 2026-02-22

<img src="static/d_images/2026-02-22.png" width="500">

### 🪟 Modal 구현 및 동작 연결
- 모달 HTML 구조 및 CSS 스타일링 완료
- `#nav_bar_add_box` 클릭 시 `.modal_overlay`를 `display: flex`로 변경하여 모달 오픈
- `overflow: hidden` 적용하여 배경 스크롤 제거

### 🖱 Drag & Drop 이미지 업로드 구현
- `.img_upload_space`에 `dragover`, `dragleave`, `drop` 이벤트 연결
- `e.preventDefault()`와 `e.stopPropagation()`을 사용해 브라우저 기본 동작 제어
- `dataTransfer.files`를 통해 드롭된 파일 정보 접근
- 이미지 파일인지 검사 후 `background-image`로 미리보기 구현

📌 **배운 점**
- HTML은 화면의 구조를 만들고 JS는 동작을 제어하며, 두 요소가 결합되어 동적인 UI가 완성된다는 것 이해
- 'Drog & Drop'의 내부 흐름(이벤트 발생 → 파일 정보 전달 → 파일 접근 → 화면 반영)을 이해
<br><br><br><br>

---

## 2026-02-21

### 🔄 클래스형 뷰 적용
- 함수형 뷰에서 클래스형 뷰로 구조 변경
- `Main(View)` 형태로 수정
- `urls.py`에서 `Main.as_view()`로 연결

### 🗂 Feed 데이터 템플릿 연동
- `Feed.objects.all()`로 전체 피드 조회
- context에 `{"feeds": feed_list}` 형태로 전달
- 템플릿에서 `{% for feed in feeds %}` 반복문 적용
- `{{ feed.content }}`, `{{ feed.user_id }}` 등 DB 데이터 동적 출력 구현

📌 **배운 점**
- 함수형 뷰 → 하나의 **함수** 안에서 요청을 처리 (GET/POST를 **직접 분기**해야 함)
- 클래스형 뷰 → 하나의 **클래스** 안에서 여러 요청(GET, POST 등)을 메서드로 **분리해서 처리**

- HTML 서버 → 서버가 **완성된 HTML 화면을 만들어서** 브라우저에 전달
- API 서버 → 서버는 **데이터(JSON)만 전달**하고, 화면은 프론트엔드가 구성
<br><br><br><br>
---

## 2026-02-20

### 🏗 MTV 구조 이해  
- Model: 데이터 구조 정의 및 DB와 연결  
- Template: 화면(UI) 구성  
- View: 요청을 처리하고 Model과 Template를 연결  
- Django는 MTV 패턴을 기반으로 동작함을 구조적으로 이해  

### ⚙ ORM 개념 이해  
- Django ORM(Object Relational Mapping) 개념 학습  
- SQL을 직접 작성하지 않고 Python 코드로 DB 조작 가능  
- `Feed.objects.create()` 형태로 데이터 생성  
- Python 코드가 내부적으로 SQL로 변환되어 실행되는 구조 이해 

### 🗂 Feed 모델 생성  
- `Feed` 모델 정의 
- (content, image, profile_image, user_id, like_count)  
- `makemigrations` / `migrate` 실행  
- `content_feed` 테이블 생성 확인  
- PyCharm Database 콘솔에서 SQL 직접 실행

📌 **배운 점**
- ORM을 사용하면 Model과 DB가 자동으로 매핑되어 SQL을 직접 작성하지 않아도 DB를 관리할 수 있음   
- 레이아웃(프론트엔드)을 먼저 구현한 뒤, 데이터의 동작 원리의 큰 흐름을 이해
<br><br><br><br>
---

## 2026-02-19

### 🔧 Navbar 개선
- flex 기반 space-between 정렬 적용
- flex-wrap: nowrap 설정
- CSS 참고 (studiomeal)

### 📱 Feed 레이아웃 1차 구현
- 화면 분할 구조 구현 (좌측 스크롤 / 우측 고정)

#### ⬅ 왼쪽 피드
- 프로필 사진 영역
- 사진 업로드 UI
- 좋아요 / 댓글 / 보관 아이콘
- 댓글 입력창

#### ➡ 오른쪽 영역
- 추천 회원 목록 UI 구성

📌 **배운 점**
- Flexbox 기반 레이아웃 구조를 직접 구성하며 CSS 속성의 동작 원리를 이해함
- 원하는 UI를 구현하기 위해 CSS 속성을 검색하고 적용해보는 과정을 통해 문제를 해결함
- 부모 요소의 너비와 자식 요소의 배치 방식이 전체 레이아웃에 미치는 영향을 체감함
- 특히 `display: flex`, `justify-content`, `flex-direction`, `position: fixed`를 사용해 봄
<br><br><br><br>
---

## 2026-02-13

### 🎨 프로젝트 로고 제작 및 적용

- 서비스 이름을 **BOOKSNAP**으로 결정
    - BOOK + SNAP의 의미 결합
    - 독서를 사진으로 기록하고 감상평을 남긴다는 컨셉
- 카메라와 책을 활용하여 모던하고 심플한 로고 제작
- navbar 왼쪽에 로고 삽입

### 🛠 Static 이미지 404 문제 해결

- 로고 이미지가 `/static/images/...` 경로에서 로드되지 않음
- Django static 설정 문제로 판단
- `STATICFILES_DIRS` 설정 추가 후 해결

📌 **배운 점**
- Django static 파일 로드 구조 이해
- settings.py 설정의 중요성
- Git을 통한 기능 단위 관리 시작
<br><br><br><br>
---

## 2026-02-12

### 🧩 네비게이션바 레이아웃 구현

- Bootstrap 기반 navbar 구조 설계
- 좌 / 중앙 / 우 영역으로 레이아웃 분리
- 초기에는 모든 요소가 왼쪽으로 정렬되는 문제 발생
  - `d-flex`, `ms-auto` 클래스가 적용되지 않음
  - Bootstrap CSS가 로드되지 않는 것을 확인
  - CDN 링크의 integrity 값 오류로 인해 브라우저가 파일 로드를 차단함
  - integrity 속성 제거 후 정상 작동 확인

📌 **배운 점**
- CDN integrity 속성의 역할 이해
- Bootstrap이 로드되지 않으면 유틸리티 클래스가 무효화됨
- 개발자 도구(Network 탭)로 CSS 로드 여부 확인 가능
