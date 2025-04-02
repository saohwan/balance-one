# FastAPI 프로젝트 구조 트리

## 주요 기능
* FastAPI 프로젝트 구조 트리
* 사용자 모듈
    - id, 이름, 성, **이메일** (사용자명), **비밀번호**, 역할, 활성화 상태, 생성일, 수정일
* 관리자 대시보드 => sqladmin
* 인증 => JWT
* DB 마이그레이션 => alembic
* 미들웨어
* 3가지 서버 환경
    - 프로덕션, 개발, 테스트
* UUID를 기본 키로 사용
* RBAC(역할 기반 접근 제어) 적용
* 구글 인증(OAuth2) 적용

## 프로젝트 구조
```sh
├── alembic     # 데이터베이스 마이그레이션 관리
├── alembic.ini
├── app
│   ├── api
│   │   ├── endpoints   # 각 기능별 모듈 (사용자, 상품, 결제 등)
│   │   │   ├── __init__.py
│   │   │   └── user
│   │   │       ├── auth.py
│   │   │       ├── functions.py
│   │   │       ├── __init__.py
│   │   │       └── user.py
│   │   ├── __init__.py
│   │   └── routers     # FastAPI 라우터, 각 기능별 라우터 포함
│   │       ├── main_router.py
│   │       ├── __init__.py
│   │       └── user.py
│   ├── core    # 데이터베이스 관리, 의존성 등 핵심 기능
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── __init__.py
│   ├── main.py     # FastAPI 앱 초기화 및 컴포넌트 통합
│   ├── models      # 사용자, 상품, 결제 등 데이터베이스 모델 정의
│   │   ├── admin.py
│   │   ├── common.py
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas    # Pydantic 모델 (데이터 검증)
│   │   ├── __init__.py
│   │   └── user.py
│   └── utils       # 여러 기능에서 사용되는 유틸리티 함수
├── requirements.txt # 프로젝트 의존성 목록
```

## 설치 및 실행 방법

1. 저장소 클론:
```sh

```

2. 가상환경 생성 및 활성화:
```sh
$ cd fastapi-production-boilerplate
$ python -m venv venv
$ source venv/bin/activate  # macOS/Linux
# Windows의 경우: venv\Scripts\activate
```

3. 의존성 설치:
```sh
# 고정 버전 설치
(venv)$ pip install -r requirements.txt

# 또는 최신 버전 설치
(venv)$ pip install -r dev.txt
```

4. 환경 설정:
- `.env.example` 파일을 `.env`로 복사하고 필요한 정보를 입력하세요.

5. 데이터베이스 마이그레이션:
```sh
(venv)$ alembic upgrade head
```

6. 서버 실행:
```sh
# uvicorn으로 직접 실행 (버전 0.100.0 이전)
(venv)$ uvicorn app.main:app --reload

# 또는 FastAPI CLI 사용 (버전 0.100.0 이후)
(venv)$ fastapi dev app/main.py
```

## 사용자 모듈 API
| 번호 | 메서드 | 경로 | 기능 | 필드 | 접근 권한 | 
|------|--------|------|------|------|-----------|
| 1 | POST | `/login` | 로그인 | **이메일**, **비밀번호** | 모든 사용자 |
| 2 | POST | `/refresh/?refresh_token=` | 액세스 토큰 갱신 | 없음 | 모든 사용자 |
| 3 | POST | `/users/` | 새 사용자 생성 | **이메일**, **비밀번호**, 이름, 성 | 모든 사용자 |
| 4 | GET | `/users/` | 전체 사용자 목록 조회 | 이메일, 비밀번호, 이름, 성, 역할, 활성화 상태, 생성일, 수정일, id | 관리자 |
| 5 | GET | `/users/me/` | 현재 사용자 정보 조회 | 이메일, 비밀번호, 이름, 성, 역할, 활성화 상태, 생성일, 수정일, id | 로그인한 사용자 |
| 6 | GET | `/users/{user_id}` | 특정 사용자 정보 조회 | 이메일, 비밀번호, 이름, 성, 역할, 활성화 상태, 생성일, 수정일, id | 로그인한 사용자 |
| 7 | PATCH | `/users/{user_id}` | 사용자 정보 부분 수정 | 이메일, 비밀번호, 활성화 상태, 역할 | 관리자 |
| 8 | DELETE | `/users/{user_id}` | 사용자 삭제 | 없음 | 관리자 |
| 9 | GET | `/` | 홈페이지 | 없음 | 모든 사용자 |
| 10 | GET | `/admin` | 관리자 대시보드 | 없음 | 모든 사용자 |

## OAuth2 - 소셜 로그인
| 번호 | 메서드 | 경로 | 기능 | 필드 | 접근 권한 | 
|------|--------|------|------|------|-----------|
| 1 | GET | `/social/google/login` | 구글 로그인 | 없음 | 모든 사용자 |
| 2 | GET | `/social/auth/google/callback` | 구글 콜백 | 없음 | 모든 사용자 |

## 기술 스택
### 백엔드
#### 언어:
    Python

#### 프레임워크:
    FastAPI
    pydantic
	
#### 기타 라이브러리 / 도구:
    SQLAlchemy
    starlette
    uvicorn
    python-jose
    alembic

## ⚠️ 주의사항
* 제공된 시크릿 키를 그대로 사용하지 마세요.
* 각 프로젝트마다 새로운 시크릿 키를 생성하세요.
* 다음 명령어로 새로운 시크릿 키를 생성할 수 있습니다:
```sh
openssl rand -hex 32
```

