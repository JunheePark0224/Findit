# FindIt 프로젝트

## 프로젝트 개요
이 프로젝트는 딥러닝을 사용하여 음성을 텍스트로 변환하고, 텍스트 요약 및 키워드 추출을 통해 강의 내용을 빠르게 이해할 수 있는 웹 애플리케이션입니다. 

## 소개 영상
[![FindIt 프로젝트 소개 영상](https://img.youtube.com/vi/ufrvlhjS7l4/0.jpg)](https://www.youtube.com/watch?v=ufrvlhjS7l4)

## 설치 및 실행 방법

### 필수 조건
- Python 3.x
- Node.js
- MySQL 데이터베이스

### 설치 방법
1. 저장소를 클론합니다.
    ```bash
    git clone https://github.com/JunheePark0224/Findit.git
    ```
2. 백엔드 디렉토리로 이동하여 필요한 라이브러리를 설치합니다.
    ```bash
    cd Findit/backend
    pip install -r requirements.txt
    ```
3. 프론트엔드 디렉토리로 이동하여 필요한 라이브러리를 설치합니다.
    ```bash
    cd ../frontend
    npm install
    ```

### 데이터베이스 설정
1. MySQL 데이터베이스를 설정합니다.
2. 아래의 SQL 명령어를 사용하여 데이터베이스와 테이블을 생성합니다.
    ```sql
    CREATE DATABASE findit;
    USE findit;

    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(100) PRIMARY KEY,
        password VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS notes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(100),
        title VARCHAR(255),
        memo TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        audio_text LONGTEXT DEFAULT NULL,
        summary TEXT DEFAULT NULL,
        keywords TEXT DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ```

### 실행 방법
1. 백엔드 서버를 실행합니다.
    ```bash
    cd ../backend
    python flask_server.py
    ```
2. 프론트엔드 서버를 실행합니다.
    ```bash
    cd ../frontend
    npm start
    ```

### 환경 변수 설정
서버 실행 전에 필요한 환경 변수들을 설정합니다.
- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`
- `KAKAO_API_KEY`
- `GOOGLE_SEARCH_ENGINE_ID`
- `GOOGLE_API_KEY`

## 사용된 기술 스택
- **프론트엔드**: HTML, CSS, Bootstrap, JavaScript
- **백엔드**: Flask, Python, MySQL, Express.js
- **데이터베이스**: MySQL

## 주요 기능
- **회원가입 및 로그인**: 사용자는 회원가입을 통해 계정을 만들고 로그인할 수 있습니다.
- **음성 파일 업로드**: 사용자가 음성 파일을 업로드할 수 있습니다.
- **텍스트 변환 및 요약**: 업로드된 음성 파일을 텍스트로 변환하고 요약합니다.
- **키워드 추출**: 요약된 텍스트에서 주요 키워드를 추출합니다.
- **검색 결과 제공**: 추출된 키워드를 바탕으로 관련 검색 결과를 제공합니다.

## 프로젝트 구조

알겠습니다. Docker 관련 내용을 제외하고 README.md 파일을 다시 작성해드리겠습니다. 다음은 주신 코드와 설명을 바탕으로 한 README.md 파일의 예시입니다.

markdown
코드 복사
# FindIt 프로젝트

## 프로젝트 개요
이 프로젝트는 딥러닝을 사용하여 음성을 텍스트로 변환하고, 텍스트 요약 및 키워드 추출을 통해 강의 내용을 빠르게 이해할 수 있는 웹 애플리케이션입니다. 

## 설치 및 실행 방법

### 필수 조건
- Python 3.x
- Node.js
- MySQL 데이터베이스

### 설치 방법
1. 저장소를 클론합니다.
    ```bash
    git clone https://github.com/JunheePark0224/Findit.git
    ```
2. 백엔드 디렉토리로 이동하여 필요한 라이브러리를 설치합니다.
    ```bash
    cd Findit/backend
    pip install -r requirements.txt
    ```
3. 프론트엔드 디렉토리로 이동하여 필요한 라이브러리를 설치합니다.
    ```bash
    cd ../frontend
    npm install
    ```

### 데이터베이스 설정
1. MySQL 데이터베이스를 설정합니다.
2. 아래의 SQL 명령어를 사용하여 데이터베이스와 테이블을 생성합니다.
    ```sql
    CREATE DATABASE findit;
    USE findit;

    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(100) PRIMARY KEY,
        password VARCHAR(100) NOT NULL
    );

    CREATE TABLE IF NOT EXISTS notes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(100),
        title VARCHAR(255),
        memo TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        audio_text LONGTEXT DEFAULT NULL,
        summary TEXT DEFAULT NULL,
        keywords TEXT DEFAULT NULL,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ```

### 실행 방법
1. 백엔드 서버를 실행합니다.
    ```bash
    cd ../backend
    python flask_server.py
    ```
2. 프론트엔드 서버를 실행합니다.
    ```bash
    cd ../frontend
    npm start
    ```

### 환경 변수 설정
서버 실행 전에 필요한 환경 변수들을 설정합니다.
- `NAVER_CLIENT_ID`
- `NAVER_CLIENT_SECRET`
- `KAKAO_API_KEY`
- `GOOGLE_SEARCH_ENGINE_ID`
- `GOOGLE_API_KEY`

## 사용된 기술 스택
- **프론트엔드**: HTML, CSS, Bootstrap, JavaScript
- **백엔드**: Flask, Python, MySQL, Express.js
- **데이터베이스**: MySQL

## 주요 기능
- **회원가입 및 로그인**: 사용자는 회원가입을 통해 계정을 만들고 로그인할 수 있습니다.
- **음성 파일 업로드**: 사용자가 음성 파일을 업로드할 수 있습니다.
- **텍스트 변환 및 요약**: 업로드된 음성 파일을 텍스트로 변환하고 요약합니다.
- **키워드 추출**: 요약된 텍스트에서 주요 키워드를 추출합니다.
- **검색 결과 제공**: 추출된 키워드를 바탕으로 관련 검색 결과를 제공합니다.

## 프로젝트 구조
Findit/
├── backend/
│ ├── flask_server.py
│ ├── requirements.txt
│ └── ...
├── frontend/
│ ├── completestyle.css
│ ├── joinstyle.css
│ ├── loginstyle.css
│ ├── mainstyle.css
│ ├── index.html
│ ├── login.html
│ ├── join.html
│ ├── complete.html
│ └── ...
├── config/
│ ├── databaseconfig.json
├── Findit_database.sql
├── README.md
├── package-lock.json
├── package.json
└── svr.js


## API 엔드포인트


### 회원가입
- **URL**: `/process/join`
- **메서드**: POST
- **설명**: 새로운 사용자 계정을 생성합니다.
- **요청 바디**:
  ```json
  {
    "id": "example_user",
    "password": "example_password"
  }

응답:
성공 시: 회원가입 성공 페이지로 리다이렉트 (/frontend/complete.html)
실패 시: 오류 메시지 반환

### 로그인
- **URL**: `/process/login`
- **메서드**: POST
- **설명**: 사용자 로그인을 처리합니다.
- **요청 바디**:
  ```json
  {
    "id": "example_user",
    "password": "example_password"
  }

응답:
성공 시: 사용자 공간 페이지로 리다이렉트 (/frontend/space.html?id=example_user)
실패 시: 오류 메시지 반환

### 노트 추가
- **URL**: `/api/notes`
- **메서드**: POST
- **설명**: 사용자 로그인을 처리합니다.
- **요청 바디**:
  ```json
  {
   "user_id": "example_user",
   "title": "example_title",
   "memo": "example_memo",
   "audio_text": "example_audio_text",
   "summary": "example_summary",
   "keywords": "example_keywords"
  }

응답:
성공 시: {
  "id": 1,
  "message": "노트 저장 성공"
}

실패 시: 오류 메시지 반환

### 노트 조회
- **URL**: `/api/notes/:user_id`
- **메서드**: GET
- **설명**: 특정 사용자의 노트를 조회합니다.
- **경로 매개 변수**: `user_id`: 조회할 사용자의 ID
- **요청 바디**: 
  ```json
  {
    "id": 1,
    "user_id": "example_user",
    "title": "example_title",
    "memo": "example_memo",
    "created_at": "2023-01-01T00:00:00Z",
    "audio_text": "example_audio_text",
    "summary": "example_summary",
    "keywords": "example_keywords"
  }

응답:
성공 시: 노트 목록
실패 시: 오류 메시지 반환


### 노트 삭제
- **URL**: `/api/notes/:id`
- **메서드**: DELETE
- **설명**: 특정 노트를 삭제합니다.
- **경로 매개 변수**: `id`: 삭제할 노트의 ID
- **요청 바디**:
  ```json
  {
   "노트 삭제 성공"
  }

응답:
성공 시: {
  "id": 1,
  "message": "노트 저장 성공"
}


### 음성 파일 업로드 및 처리
- **URL**: `/upload_audio`
- **메서드**: POST
- **설명**: 음성 파일을 업로드하고 텍스트 변환, 요약 및 키워드 추출을 처리합니다.
- **요청 바디**:Multipart/form-data로 음성 파일 포함
  
응답:
성공 시: {
  "text": "example_audio_text",
  "summary": "example_summary",
  "keywords": ["example_keyword1", "example_keyword2"]
}
실패 시: 오류 메시지 반환

### 검색
- **URL**: `/api/search`
- **메서드**: GET
- **설명**: 검색어에 대한 결과를 제공합니다.
- **쿼리 매개변수**: `query`: 검색어
`wanted_row`: 원하는 검색 결과 수 (기본값: 100)
  
응답:
성공 시: [
  {
    "Title": "example_title",
    "Link": "http://example.com",
    "Description": "example_description",
    "search_engine": "Google"
  },
  ...
]
실패 시: 오류 메시지 반환

## 현재 상태
현재 원격 서버가 접속 불가능하여 원격 데이터베이스 (MySQL)와 관련된 기능이 작동하지 않습니다. 따라서 프로젝트의 일부 기능이 제한될 수 있습니다. 로컬 개발 환경에서 SQLite를 사용하여 기능을 테스트할 수 있습니다.

## 추가 설명
flask_server.py: 기본 음성 인식 기능을 구현한 Python 서버 코드입니다. Python의 speech_recognition 모듈을 사용하여 음성 파일을 텍스트로 변환합니다.
flask_server2.py: 딥러닝 모델을 이용한 음성 인식 기능을 구현하기 위한 준비 단계 코드입니다. 아직 완성되지 않았습니다.