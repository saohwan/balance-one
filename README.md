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

## 🚀 서버 실행

### 개발 환경
```bash
# 개발 서버 실행 (자동 리로드)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 개발 서버 실행 (리로드 없음)
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 프로덕션 환경
```bash
# 프로덕션 서버 실행 (워커 4개)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📊 데이터베이스 마이그레이션

### Alembic 초기 설정

```bash
# Alembic 초기화
alembic init alembic

# alembic.ini 파일 설정
# sqlalchemy.url = mysql+pymysql://user:password@db:3306/balance_one
```

### 마이그레이션 명령어

```bash
# 새로운 마이그레이션 생성
alembic revision --autogenerate -m "마이그레이션 설명"

# 마이그레이션 실행
alembic upgrade head

# 마이그레이션 롤백
alembic downgrade -1

# 마이그레이션 히스토리 조회
alembic history

# 현재 마이그레이션 상태 확인
alembic current
```

### 마이그레이션 파일 구조

```
alembic/
├── versions/           # 마이그레이션 파일
├── env.py             # 마이그레이션 환경 설정
├── README             # 마이그레이션 설명
├── script.py.mako     # 마이그레이션 템플릿
└── alembic.ini        # Alembic 설정 파일
```

### 마이그레이션 모범 사례

1. **마이그레이션 파일 명명 규칙**
   - 날짜_시간_설명 형식 사용 (예: 20240315_1430_create_user_table)
   - 설명은 명확하고 간단하게 작성

2. **데이터 마이그레이션**
   - 데이터 변경이 필요한 경우 별도의 마이그레이션 파일 생성
   - 롤백 가능한 방식으로 작성

3. **마이그레이션 순서**
   - 외래 키 제약조건이 있는 테이블은 참조되는 테이블 이후에 생성
   - 인덱스는 테이블 생성 후에 추가

4. **롤백 고려사항**
   - 모든 마이그레이션은 롤백 가능하도록 작성
   - 데이터 삭제 시 백업 데이터 생성 고려

## 📈 포트폴리오 유형 설정

### 포트폴리오 유형 정의

1. **공격형 포트폴리오**
   - **리스크 성향**: 높음
   - **주식 비중**: 70-80%
   - **채권 비중**: 20-30%
   - **특징**:
     - 고성장 주식 위주
     - 신흥 시장 비중 높음
     - 변동성 높음
     - 장기 투자 지향

2. **균형형 포트폴리오**
   - **리스크 성향**: 중간
   - **주식 비중**: 50-60%
   - **채권 비중**: 40-50%
   - **특징**:
     - 대형주 중심
     - 안정적 배당주 포함
     - 적정 변동성
     - 중장기 투자 지향

3. **방어형 포트폴리오**
   - **리스크 성향**: 낮음
   - **주식 비중**: 30-40%
   - **채권 비중**: 60-70%
   - **특징**:
     - 배당주 중심
     - 채권 비중 높음
     - 낮은 변동성
     - 단기 투자 지향

### 포트폴리오 구성 규칙

1. **섹터 분산**
   - 단일 섹터 최대 비중: 30%
   - 관련 섹터 최대 비중: 50%

2. **시가총액 분포**
   - 대형주 (시가총액 1조원 이상): 40-60%
   - 중형주 (시가총액 1천억원-1조원): 30-40%
   - 소형주 (시가총액 1천억원 미만): 10-20%

3. **리스크 관리**
   - 개별 종목 최대 비중: 10%
   - 베타 계수 제한: 1.5 이하
   - 변동성 제한: 연간 20% 이하

### 포트폴리오 리밸런싱

1. **리밸런싱 주기**
   - 정기 리밸런싱: 분기별
   - 특별 리밸런싱: 시장 변동성 20% 이상

2. **리밸런싱 기준**
   - 목표 비중 대비 ±5% 이상 차이
   - 시장 상황 급변 시
   - 개별 종목 특이사항 발생 시

3. **리밸런싱 제한**
   - 연간 최대 리밸런싱 횟수: 4회
   - 단일 종목 최대 조정 비중: 5%

### 포트폴리오 성과 평가

1. **수익률 지표**
   - 누적 수익률
   - 연간 수익률
   - 변동성 조정 수익률 (샤프 비율)

2. **리스크 지표**
   - 베타 계수
   - 변동성
   - 최대 낙폭 (MDD)

3. **분산 투자 지표**
   - 섹터 분산도
   - 시가총액 분포
   - 상관관계 분석

## 📝 API 엔드포인트

### 인증 관련
| 메서드 | 경로 | 설명 | 요청 본문 | 응답 |
|--------|------|------|-----------|------|
| POST | `/api/auth/register` | 회원가입 | ```json { "email": "string", "password": "string", "first_name": "string", "last_name": "string", "portfolio_type": "string" } ``` | ```json { "id": "string", "email": "string", "first_name": "string", "last_name": "string", "portfolio_type": "string", "is_active": true } ``` |
| POST | `/api/auth/login` | 로그인 | ```json { "username": "string", "password": "string" } ``` | ```json { "access_token": "string", "refresh_token": "string", "token_type": "bearer" } ``` |
| POST | `/api/auth/refresh` | 토큰 갱신 | ```json { "refresh_token": "string" } ``` | ```json { "access_token": "string", "token_type": "bearer" } ``` |

#### 인증 API 상세 설명

##### 회원가입 (`/api/auth/register`)
- 새로운 사용자 계정을 생성합니다.
- 이메일 중복 체크를 수행합니다.
- 비밀번호는 해시화하여 저장됩니다.
- 포트폴리오 유형(공격형/균형형)을 선택할 수 있습니다.
- 회원가입 시 감사 로그가 기록됩니다.

##### 로그인 (`/api/auth/login`)
- 이메일과 비밀번호로 사용자 인증을 수행합니다.
- 로그인 시도 횟수 제한이 적용됩니다 (30분 내 5회).
- 성공 시 JWT 액세스 토큰과 리프레시 토큰을 발급합니다.
- 실패한 로그인 시도는 기록됩니다.
- 비활성화된 계정은 로그인이 불가능합니다.

##### 토큰 갱신 (`/api/auth/refresh`)
- 리프레시 토큰을 사용하여 새로운 액세스 토큰을 발급합니다.
- 리프레시 토큰의 유효성을 검증합니다.
- 토큰 갱신 시 감사 로그가 기록됩니다.

### 계좌 관련
| 메서드 | 경로 | 설명 | 요청 본문 | 응답 |
|--------|------|------|-----------|------|
| POST | `/api/account/deposit` | 입금 | ```json { "amount": "number", "description": "string" } ``` | ```json { "transaction_id": "string", "amount": "number", "balance": "number", "created_at": "datetime" } ``` |
| POST | `/api/account/withdraw` | 출금 | ```json { "amount": "number", "description": "string" } ``` | ```json { "transaction_id": "string", "amount": "number", "balance": "number", "created_at": "datetime" } ``` |
| GET | `/api/account/balance` | 잔고 조회 | - | ```json { "balance": "number", "last_updated": "datetime" } ``` |
| GET | `/api/account/transactions` | 거래 내역 조회 | - | ```json { "transactions": [{ "id": "string", "type": "string", "amount": "number", "balance": "number", "description": "string", "created_at": "datetime" }], "total_count": "number", "page": "number", "size": "number" } ``` |

#### 계좌 API 상세 설명

##### 입금 (`/api/account/deposit`)
- 계좌에 자금을 입금합니다.
- 입금 금액은 양수여야 합니다.
- 입금 시 현재 잔고가 함께 반환됩니다.
- 입금 내역은 거래 내역에 기록됩니다.
- 입금 시 감사 로그가 기록됩니다.

##### 출금 (`/api/account/withdraw`)
- 계좌에서 자금을 출금합니다.
- 출금 금액은 잔고를 초과할 수 없습니다.
- 출금 시 현재 잔고가 함께 반환됩니다.
- 출금 내역은 거래 내역에 기록됩니다.
- 출금 시 감사 로그가 기록됩니다.

##### 잔고 조회 (`/api/account/balance`)
- 현재 계좌 잔고를 조회합니다.
- 마지막 업데이트 시간이 함께 반환됩니다.
- 실시간 잔고 정보를 제공합니다.

##### 거래 내역 조회 (`/api/account/transactions`)
- 계좌의 거래 내역을 조회합니다.
- 페이지네이션이 지원됩니다 (기본 페이지 크기: 20).
- 거래 유형(입금/출금), 금액, 잔고, 설명, 시간 정보를 포함합니다.
- 정렬 및 필터링이 지원됩니다.

### 자문 관련
| 메서드 | 경로 | 설명 | 요청 본문 | 응답 |
|--------|------|------|-----------|------|
| POST | `/api/advisory/request` | 자문 요청 | ```json { "investment_amount": "number", "risk_tolerance": "string", "investment_period": "number", "preferences": { "sectors": ["string"], "excluded_stocks": ["string"] } } ``` | ```json { "request_id": "string", "status": "string", "created_at": "datetime", "estimated_completion": "datetime" } ``` |
| GET | `/api/advisory/requests` | 자문 내역 조회 | - | ```json { "requests": [{ "id": "string", "status": "string", "investment_amount": "number", "created_at": "datetime", "completed_at": "datetime" }], "total_count": "number", "page": "number", "size": "number" } ``` |
| GET | `/api/advisory/requests/{request_id}` | 자문 상세 조회 | - | ```json { "id": "string", "status": "string", "investment_amount": "number", "risk_tolerance": "string", "investment_period": "number", "portfolio": [{ "stock_code": "string", "name": "string", "weight": "number", "price": "number" }], "created_at": "datetime", "completed_at": "datetime", "analysis": "string" } ``` |

#### 자문 API 상세 설명

##### 자문 요청 (`/api/advisory/request`)
- 맞춤형 포트폴리오 자문을 요청합니다.
- 투자 금액, 리스크 성향, 투자 기간을 지정할 수 있습니다.
- 선호하는 섹터와 제외하고 싶은 종목을 지정할 수 있습니다.
- 요청 시 예상 완료 시간이 제공됩니다.
- 자문 요청 시 감사 로그가 기록됩니다.

##### 자문 내역 조회 (`/api/advisory/requests`)
- 사용자의 자문 요청 내역을 조회합니다.
- 페이지네이션이 지원됩니다 (기본 페이지 크기: 20).
- 요청 상태, 투자 금액, 생성/완료 시간 정보를 포함합니다.
- 상태별 필터링이 지원됩니다.

##### 자문 상세 조회 (`/api/advisory/requests/{request_id}`)
- 특정 자문 요청의 상세 정보를 조회합니다.
- 추천된 포트폴리오 구성 정보를 포함합니다.
- 각 종목별 비중과 현재 가격 정보를 제공합니다.
- 자문 분석 내용이 포함됩니다.

### 관리자 관련
| 메서드 | 경로 | 설명 | 요청 본문 | 응답 |
|--------|------|------|-----------|------|
| POST | `/api/admin/stocks` | 증권 등록 | ```json { "code": "string", "name": "string", "sector": "string", "market_cap": "number", "current_price": "number", "description": "string" } ``` | ```json { "id": "string", "code": "string", "name": "string", "sector": "string", "market_cap": "number", "current_price": "number", "description": "string", "created_at": "datetime" } ``` |
| PUT | `/api/admin/stocks/{stock_id}` | 증권 수정 | ```json { "name": "string", "sector": "string", "market_cap": "number", "current_price": "number", "description": "string" } ``` | ```json { "id": "string", "code": "string", "name": "string", "sector": "string", "market_cap": "number", "current_price": "number", "description": "string", "updated_at": "datetime" } ``` |
| DELETE | `/api/admin/stocks/{stock_id}` | 증권 삭제 | - | ```json { "message": "string" } ``` |
| GET | `/api/admin/stocks` | 증권 목록 조회 | - | ```json { "stocks": [{ "id": "string", "code": "string", "name": "string", "sector": "string", "market_cap": "number", "current_price": "number", "description": "string" }], "total_count": "number", "page": "number", "size": "number" } ``` |
| GET | `/api/admin/audit-logs` | 감사 로그 조회 | - | ```json { "logs": [{ "id": "string", "user_id": "string", "action": "string", "details": "string", "ip_address": "string", "created_at": "datetime" }], "total_count": "number", "page": "number", "size": "number" } ``` |

#### 관리자 API 상세 설명

##### 증권 등록 (`/api/admin/stocks`)
- 새로운 증권을 시스템에 등록합니다.
- 증권 코드는 중복될 수 없습니다.
- 시가총액, 현재가, 섹터 정보를 포함합니다.
- 등록 시 감사 로그가 기록됩니다.

##### 증권 수정 (`/api/admin/stocks/{stock_id}`)
- 기존 증권의 정보를 수정합니다.
- 증권 코드는 수정할 수 없습니다.
- 수정 시 감사 로그가 기록됩니다.

##### 증권 삭제 (`/api/admin/stocks/{stock_id}`)
- 증권을 시스템에서 삭제합니다.
- 이미 포트폴리오에 포함된 증권은 삭제할 수 없습니다.
- 삭제 시 감사 로그가 기록됩니다.

##### 증권 목록 조회 (`/api/admin/stocks`)
- 등록된 모든 증권 목록을 조회합니다.
- 페이지네이션이 지원됩니다 (기본 페이지 크기: 20).
- 섹터별, 시가총액별 필터링이 지원됩니다.
- 정렬 기능이 지원됩니다.

##### 감사 로그 조회 (`/api/admin/audit-logs`)
- 시스템의 모든 감사 로그를 조회합니다.
- 페이지네이션이 지원됩니다 (기본 페이지 크기: 20).
- 사용자별, 액션별 필터링이 지원됩니다.
- 시간대별 필터링이 지원됩니다.
- IP 주소 정보가 포함됩니다.


