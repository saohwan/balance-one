# 증권 자문 시스템 (Balance One)

증권 자문 시스템은 FastAPI 기반의 웹 애플리케이션으로, 사용자들에게 맞춤형 포트폴리오 추천과 자문 서비스를 제공합니다.

## 🌟 주요 기능

- **사용자 관리**
  - 회원가입 및 로그인
  - JWT 기반 인증
  - 계정 관리

- **계좌 관리**
  - 입금/출금
  - 잔고 조회
  - 거래 내역 조회

- **자문 시스템**
  - 포트폴리오 유형 선택 (공격형/균형형)
  - 자동 포트폴리오 추천
  - 자문 내역 조회

- **관리자 기능**
  - 증권 등록/수정/삭제
  - 감사 로그 조회

## 🛠 기술 스택

- **백엔드**
  - FastAPI
  - SQLAlchemy
  - MySQL
  - JWT 인증

- **개발 도구**
  - Docker
  - Docker Compose
  - phpMyAdmin

## 📁 프로젝트 구조

```
├── app/
│   ├── api/            # API 엔드포인트
│   ├── core/           # 핵심 설정
│   ├── models/         # 데이터베이스 모델
│   ├── schemas/        # Pydantic 스키마
│   └── utils/          # 유틸리티 함수
├── alembic/            # 데이터베이스 마이그레이션
├── tests/              # 테스트 코드
├── Dockerfile          # Docker 설정
├── docker-compose.yml  # Docker Compose 설정
└── requirements.txt    # Python 패키지 의존성
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 저장소 클론
git clone [repository-url]

# 프로젝트 디렉토리 이동
cd balance-one

# Docker 컨테이너 실행
docker-compose up -d
```

### 2. 서비스 접근

- **FastAPI 애플리케이션**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **phpMyAdmin**: http://localhost:8080

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 환경 변수를 설정합니다:

```env
# 데이터베이스
DATABASE_URL=mysql+pymysql://user:password@db:3306/balance_one

# 보안
SECRET_KEY=your-secret-key-here
REFRESH_SECRET_KEY=your-refresh-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 환경
ENVIRONMENT=development
```

## 🔧 Docker 명령어

```bash
# 컨테이너 실행
docker-compose up -d

# 컨테이너 중지
docker-compose down

# 로그 확인
docker-compose logs -f

# 데이터베이스 초기화
docker-compose down -v
docker-compose up -d
```

## 📝 API 엔드포인트

### 인증 관련
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/auth/register` | 회원가입 |
| POST | `/api/auth/login` | 로그인 |
| POST | `/api/auth/refresh` | 토큰 갱신 |

### 계좌 관련
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/account/deposit` | 입금 |
| POST | `/api/account/withdraw` | 출금 |
| GET | `/api/account/balance` | 잔고 조회 |
| GET | `/api/account/transactions` | 거래 내역 조회 |

### 자문 관련
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/advisory/request` | 자문 요청 |
| GET | `/api/advisory/requests` | 자문 내역 조회 |
| GET | `/api/advisory/requests/{request_id}` | 자문 상세 조회 |

### 관리자 관련
| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/admin/stocks` | 증권 등록 |
| PUT | `/api/admin/stocks/{stock_id}` | 증권 수정 |
| DELETE | `/api/admin/stocks/{stock_id}` | 증권 삭제 |
| GET | `/api/admin/stocks` | 증권 목록 조회 |
| GET | `/api/admin/audit-logs` | 감사 로그 조회 |


