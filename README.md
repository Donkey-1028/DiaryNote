# DiaryNote

## 1. DiaryNote란?
	django-rest-framework 를 연습하기 위해 주제를 생각하던 중
	일기장이라는 개념을 가지고 CRUD 게시판을 만들어 보고자
	DiaryNote란 프로젝트를 진행하였습니다.
	

## 2. 프로젝트 제작 목적
	 docker, docker-compose를 이용한 개발환경 구축 및 개발
	 
	 '클린 코드를 위한 테스트 주도 개발' 
	 책을 공부 한 내용을 토대로 테스트코드 연습
	 
	 RESTful API 학습
	 django-rest-framwork 학습
	 

## 3. 주요 기능
#### 3.1 diary
* 기본적인 CRUD
* Token, Session 인증
* 기능별 TEST 코드 작성
#### 3.2 users
* django user model
* user register, Login
* 로그인 된 유저 Token 확인
* 회원 가입시 Token 자동 생성



## 4. Skill Stack

#### 4.1 back-end
	python Django framework
	python Django rest framework
	python Django rest framework swagger
#### 4.2 Dev-Ops
	Docker, Docker-compose, Ubuntu, postgres
	
	
## 5. Run Process
    1. docker-compose build ,docker image 만들기
    2. docker-compose up , docker 개발환경 시작
    3. vim 다운받기
    4. superuser 만들기
    5. swagger base.html staticfiles를 static 으로 바꾸기
        (django 3.0 부터는 staticfiles가 없어졌기 때문에 에러발생)
    
    
    
    