# 💁‍♀️ 프로젝트 개요
Django를 이용한 게시판 CRUD api 구현

## 프로젝트 ERD
![board_erd](https://user-images.githubusercontent.com/73830753/138736778-f69e25a6-72d6-42a9-bd79-9f48625ffb97.png)

## 유저
- 게시판에 글을 수정하거나 삭제할 때 유저 인증이 필요하여 회원가입, 로그인 기능 구현
### 회원가입 (signup)
- request로 name, email, password를 받는다.
- 이메일 이미 존재할 시 `EMAIL_ALREADY_EXISTS` 에러 반환
- 아이디, 비밀번호 정규표현식을 이용하여 형식 지정
    - 아이디 `@`와 `.` 필수 포함
    - 패스워드 8자리 이상, 영문&숫자 필수 포함, 특수문자 가능
    - 아이디, 패드워드 정규식 형식과 일치하지 않을 시 `EMAIL_FORMAT_ERROR`, `PASSWORD_FORMAT_ERROR` 에러 반환
- 패스워드 bcrypt를 이용하여 암호화
- 유저 생성에 성공할 시 `SIGNUP_SUCCESS` 메시지 반환
- 키 에러 발생 시 `KEY_ERROR` 에러 반환
- 디코드 에러 발생 시 `JSONDecodeError` 에러 반환

### 로그인 (login)
- request로 email, password를 받는다.
- request email과 일치하는 user를 찾는다.
    - db에 request email과 일치하는 email이 없을 시  `EMAIL_DOES_NOT_EXISTS` 에러 반환
- request password와 db에 저장되어 있는 암호화된 패스워드를 비교한다.
    - 일치하지 않을 시 `WRONG PASSWORD` 에러 반환
- jwt로 고유한 유저 id값을 사용하여 access_token을 발급한다.
    - access_token을 발급할 때 사용되는 SECRET_KEY와 ALGORITHM은 보안을 위해 my_settings.py 파일에 저장되어 있다. 
- 로그인에 성공했을 시 `LOGIN_SUCCESS` 메시지와 함께 access_token을 발급한다.
- 유저에서 하나 이상의 객체가 리턴되었을 시 `MUTIPLE_OBJECTS_RETURNED` 에러가 반환된다.

### endpoint
유저 회원가입 : http://localhost:8000/users/signin
![signup](https://user-images.githubusercontent.com/73830753/138814642-4c282c06-7f0e-457e-b78a-87cac0cf2c01.png)

유저 로그인 : http://localhost:8000/users/login
![login](https://user-images.githubusercontent.com/73830753/138814637-a6984e2a-8e83-44fa-86d8-14a97e0202b1.png)


## 포스팅
- 유저 로그인 후 글 작성, 글 확인, 글 수정, 글 삭제 기능 구현
- 로그인 하지 않은 유저는 전체 글 확인 가능

### 글 작성 (create)
#### 유저 권한 확인
- 글 작성 전 utils 파일에 있는 log_in_confirm 함수를 decorator로 사용하여 유저의 권한을 확인한다.
- token을 decode하여 user의 id값을 가져와 user를 불러온다.
#### 권한 확인 후 글 작성
- 사용자가 글 내용(content)를 입력하지 않았을 시 `EMPTY_CONTENT` 에러를 반환한다.
- 글 내용, 이미지 url을 사용자에게 받아 글을 생성한다.

### 글 확인 (read)
- page를 쿼리로 받는다.
- 한 페이지에 4개의 글씩 출력한다.
- 존재하지 않는 페이지 접속 시 첫번째 페이지로 이동한다.
- 유저가 작성한 글이 존재하지 않는 경우 `POST_DOES_NOT_EXISTS` 에러를 반환한다.
- 유저의 id를 db에서 확인하여 유저가 작성한 글 목록을 확인한다.

### 글 수정 (update)
- 쿼리 파라미터를 통해 수정할 글 내용과 이미지 url을 받는다.
- 만약 비어있다면 ''를 반환한다.
- user와 post_id가 일치하지 않는다면 `NO_PERMISSION_TO_UPDATE` 에러를 반환한다.

### 글 삭제 (delete)

### 글 목록 확인 (read)
- 한 페이지에 4개의 글 출력
- 존재하지 않는 페이지 요청 시 첫번째 페이지 글 출력

### endpoint
글 작성 : http://localhost:8000/post
![post](https://user-images.githubusercontent.com/73830753/138814951-8edde119-36e9-4eba-9073-3e7642139527.png)

글 확인 : http://localhost:8000/post?page={page}
![my_post_list](https://user-images.githubusercontent.com/73830753/138815067-0078e5d2-83e6-4e35-85bc-7d9142e42da8.png)

글 목록 확인 : http://localhost:8000/posts?page={page}
![post_list](https://user-images.githubusercontent.com/73830753/138815192-f2580617-fd22-44db-bf00-a6b67a157968.png)

글 수정 : http://localhost:8000/update/{post_id}?content={content}&image_url={image_url}
![update](https://user-images.githubusercontent.com/73830753/138815385-0b2ff25e-0096-48e7-ab92-a43263db4629.png)
![update_결과](https://user-images.githubusercontent.com/73830753/138815459-6ee2bb8c-945c-4271-95f1-ce8a4ac3994b.png)

글 삭제 : http://localhost:8000/post?post_id={post_id}
![delete](https://user-images.githubusercontent.com/73830753/138817826-8c6874e9-0a3f-45a5-a816-9c1161084f7f.png)