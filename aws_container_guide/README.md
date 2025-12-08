# AWS Docker 컨테이너 배포 가이드

> Windows 환경에서 Docker Desktop을 사용하여 FastAPI/Django 애플리케이션을 AWS에 배포하는 종합 가이드

## 📋 목차

- [개요](#개요)
- [시작하기 전에](#시작하기-전에)
- [빠른 시작 5분 완성](#빠른-시작-5분-완성)
- [개발 환경](#개발-환경)
- [프로젝트 구조](#프로젝트-구조)
- [사전 준비](#사전-준비)
- [FastAPI 가이드](#fastapi-가이드)
- [Django 가이드](#django-가이드)
- [환경 변수 관리](#환경-변수-관리)
- [데이터베이스 연결](#데이터베이스-연결)
- [배포 옵션](#배포-옵션)
- [실전 예제](#실전-예제)
- [성능 최적화](#성능-최적화)
- [CI/CD 파이프라인](#cicd-파이프라인)
- [트러블슈팅](#트러블슈팅)
- [FAQ](#faq)

---

## 개요

이 가이드는 Windows 로컬 환경에서 Docker Desktop을 사용하여 컨테이너 이미지를 빌드하고, AWS의 다양한 서비스에 배포하는 방법을 다룹니다.

### 지원하는 프레임워크
- **FastAPI**: 고성능 비동기 Python 웹 프레임워크
- **Django**: 완전한 기능을 갖춘 Python 웹 프레임워크

### 지원하는 AWS 배포 옵션
1. **AWS App Runner**: 완전 관리형, 가장 간단한 배포 (⭐ 초급)
2. **AWS ECS (Fargate)**: 서버리스 컨테이너 관리 (⭐⭐ 중급)
3. **AWS EKS**: Kubernetes 기반 오케스트레이션 (⭐⭐⭐ 고급)

---

## 시작하기 전에

### 필요한 배경 지식

이 가이드를 효과적으로 따라하기 위해 다음 기본 지식이 있으면 좋습니다:

#### 필수
- **기본 프로그래밍**: Python 기초 문법
- **터미널 사용**: PowerShell 또는 명령 프롬프트 기본 명령어
- **웹 개념**: HTTP, REST API 기본 이해
- **AWS 계정**: 활성화된 AWS 계정 (신용카드 등록 필요)

#### 권장
- **Docker 기초**: 컨테이너와 이미지 개념
- **Git 기초**: 버전 관리 기본 명령어
- **클라우드 기초**: AWS 서비스 기본 개념

### 학습 리소스

Docker나 AWS가 처음이신가요? 다음 리소스를 참고하세요:

- **Docker 입문**: [Docker 공식 튜토리얼](https://docs.docker.com/get-started/)
- **AWS 기초**: [AWS 시작하기](https://aws.amazon.com/getting-started/)
- **FastAPI 기초**: [FastAPI 튜토리얼](https://fastapi.tiangolo.com/tutorial/)
- **Django 기초**: [Django 튜토리얼](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)

### 예상 소요 시간

- **환경 설정**: 30분 ~ 1시간
- **첫 배포 (App Runner)**: 15 ~ 30분
- **중급 배포 (ECS)**: 1 ~ 2시간
- **고급 배포 (EKS)**: 2 ~ 4시간

---

## 빠른 시작 (5분 완성)

바로 시작하고 싶으신가요? 다음 단계를 따라 5분 안에 FastAPI 앱을 로컬에서 실행해보세요!

### 전제 조건
- Docker Desktop이 설치되어 실행 중이어야 합니다

### 단계별 가이드

#### 1. 프로젝트 디렉토리 생성
```powershell
mkdir C:\temp\fastapi-quick-start
cd C:\temp\fastapi-quick-start
```

#### 2. 간단한 FastAPI 앱 작성
**main.py** 파일 생성:
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
```

**requirements.txt** 파일 생성:
```txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
```

#### 3. Dockerfile 생성
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 4. 빌드 및 실행
```powershell
# 이미지 빌드
docker build -t fastapi-quick .

# 컨테이너 실행
docker run -d -p 8000:8000 --name fastapi-app fastapi-quick

# 작동 확인
curl http://localhost:8000
# 또는 브라우저에서: http://localhost:8000/docs
```

#### 5. 정리
```powershell
# 컨테이너 중지 및 제거
docker stop fastapi-app
docker rm fastapi-app
```

축하합니다! 첫 Docker 컨테이너 앱을 실행했습니다. 이제 본격적인 가이드를 따라가보세요.

---

## 개발 환경

### 필수 요구사항
```powershell
# 버전 확인
python --version   # Python 3.11 이상 권장 (Python 3.12 최신)
node --version     # Node.js 20 LTS 권장 (Django만 사용 시 불필요)
docker --version   # Docker Desktop 24.0 이상
aws --version      # AWS CLI v2.15 이상
```

### 선택사항
- **VSCode**: 추천 IDE
- **PowerShell 7**: 향상된 스크립팅 경험
- **Git**: 버전 관리용

---

## 프로젝트 구조

```
container_k8s_guide/
├── README.md (현재 파일)
│
├── fastapi-aws/                    # FastAPI 프로젝트
│   ├── 0-windows-setup/
│   │   ├── README.md              # Windows 환경 설정 가이드
│   │   ├── install-docker.md
│   │   └── install-aws-cli.md
│   │
│   ├── app/                       # FastAPI 애플리케이션
│   │   ├── main.py               # FastAPI 앱 진입점
│   │   ├── requirements.txt      # Python 의존성
│   │   └── .env.example          # 환경변수 템플릿
│   │
│   ├── Dockerfile                # 멀티스테이지 빌드
│   ├── docker-compose.yml        # 로컬 개발 환경
│   ├── .dockerignore
│   │
│   ├── scripts/                  # 자동화 스크립트
│   │   ├── build-local.ps1       # 로컬 빌드
│   │   ├── run-local.ps1         # 로컬 실행
│   │   ├── push-to-ecr.ps1       # ECR 푸시
│   │   └── test-api.ps1          # API 테스트
│   │
│   ├── deployments/
│   │   ├── 1-app-runner/
│   │   │   ├── README.md
│   │   │   └── apprunner.yaml
│   │   │
│   │   ├── 2-ecs-fargate/
│   │   │   ├── README.md
│   │   │   ├── task-definition.json
│   │   │   └── service.json
│   │   │
│   │   └── 3-eks/
│   │       ├── README.md
│   │       └── k8s/
│   │           ├── deployment.yaml
│   │           ├── service.yaml
│   │           └── ingress.yaml
│   │
│   └── README.md                 # FastAPI 프로젝트 가이드
│
└── django-aws/                    # Django 프로젝트
    └── (FastAPI와 동일한 구조)
```

---

## 사전 준비

### 1. Docker Desktop 설치 및 설정

#### 설치
1. [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) 다운로드
2. 설치 프로그램 실행
3. **WSL2 백엔드 옵션 선택** (필수)
4. 재시작 후 Docker Desktop 실행

#### 설정 확인
```powershell
# PowerShell에서 실행
docker --version
# 출력 예: Docker version 24.0.7, build afdd53b

docker compose version
# 출력 예: Docker Compose version v2.23.0

# Docker 데몬 실행 확인
docker ps
# 정상이면 컨테이너 목록 출력 (비어있어도 OK)
```

#### Docker Desktop 리소스 설정
1. Docker Desktop 열기
2. **Settings > Resources > WSL Integration**
3. 권장 설정:
   - **Memory**: 4GB 이상 (8GB 권장)
   - **CPUs**: 2 이상 (4 권장)
   - **Disk**: 20GB 이상
   - **Swap**: 1GB

### 2. AWS CLI 설치

#### Windows에서 AWS CLI 설치
```powershell
# PowerShell (관리자 권한)에서 실행
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# 또는 직접 다운로드
# https://awscli.amazonaws.com/AWSCLIV2.msi
```

#### 설치 확인
```powershell
aws --version
# 출력 예: aws-cli/2.15.0 Python/3.11.6 Windows/10 exe/AMD64 prompt/off
```

#### AWS 자격증명 구성
```powershell
aws configure
```

입력 정보:
```
AWS Access Key ID [None]: AKIAIOSFODNN7EXAMPLE
AWS Secret Access Key [None]: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
Default region name [None]: ap-northeast-2
Default output format [None]: json
```

**자격증명 확인:**
```powershell
# 현재 AWS 계정 확인
aws sts get-caller-identity

# 출력 예:
# {
#     "UserId": "AIDACKCEVSQ6C2EXAMPLE",
#     "Account": "123456789012",
#     "Arn": "arn:aws:iam::123456789012:user/myuser"
# }
```

### 3. Git 설치 (선택사항)

```powershell
# winget 사용 (Windows 11 또는 Windows 10 최신 버전)
winget install --id Git.Git -e --source winget

# 설치 확인
git --version
```

---

## FastAPI 가이드

### 빠른 시작

#### 1. 프로젝트 클론 또는 생성
```powershell
# GitHub에서 클론
git clone https://github.com/your-repo/container_k8s_guide.git
cd container_k8s_guide\fastapi-aws

# 또는 새로 생성
mkdir fastapi-aws
cd fastapi-aws
```

#### 2. 로컬에서 빌드 및 실행
```powershell
# 이미지 빌드
.\scripts\build-local.ps1

# 로컬에서 실행
.\scripts\run-local.ps1

# 브라우저에서 확인
# http://localhost:8000
# http://localhost:8000/docs  (Swagger UI)
```

### FastAPI 애플리케이션 예제

#### app/main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="FastAPI on AWS",
    description="FastAPI 애플리케이션 AWS 배포 예제",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class HealthResponse(BaseModel):
    status: str
    message: str

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.get("/")
async def root():
    return {"message": "Hello from FastAPI on AWS!"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for AWS"""
    return HealthResponse(
        status="healthy",
        message="Application is running"
    )

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

#### app/requirements.txt
```txt
fastapi==0.115.0
uvicorn[standard]==0.30.6
pydantic==2.9.2
python-multipart==0.0.12
```

### Dockerfile (멀티스테이지 빌드)

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# 의존성 설치
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# 보안: 비-root 사용자 생성
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Builder 스테이지에서 설치한 패키지 복사
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# 애플리케이션 코드 복사
COPY app/ .

# 소유권 변경
RUN chown -R appuser:appuser /app

# 비-root 사용자로 전환
USER appuser

# 포트 노출
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# 실행 명령
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml (로컬 개발용)

```yaml
version: '3.8'

services:
  fastapi:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi-app
    ports:
      - "8000:8000"
    environment:
      - ENV=development
      - DEBUG=true
    volumes:
      - ./app:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # PostgreSQL (필요한 경우)
  db:
    image: postgres:16-alpine
    container_name: fastapi-db
    environment:
      - POSTGRES_DB=fastapi_db
      - POSTGRES_USER=fastapi_user
      - POSTGRES_PASSWORD=fastapi_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### PowerShell 스크립트 예제

#### scripts/build-local.ps1
```powershell
# FastAPI 로컬 빌드 스크립트
Write-Host "================================" -ForegroundColor Cyan
Write-Host "FastAPI Docker 이미지 빌드 시작" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# 현재 디렉토리 확인
$currentDir = Get-Location
Write-Host "현재 디렉토리: $currentDir" -ForegroundColor Yellow

# Dockerfile 존재 확인
if (-not (Test-Path "Dockerfile")) {
    Write-Host "❌ Dockerfile을 찾을 수 없습니다!" -ForegroundColor Red
    exit 1
}

# 이미지 이름 설정
$IMAGE_NAME = "fastapi-aws"
$IMAGE_TAG = "latest"

# 빌드 시작
Write-Host "`n🔨 이미지 빌드 중..." -ForegroundColor Green
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ 빌드 성공!" -ForegroundColor Green
    Write-Host "이미지 이름: ${IMAGE_NAME}:${IMAGE_TAG}" -ForegroundColor Cyan
    
    # 이미지 크기 확인
    Write-Host "`n📊 이미지 정보:" -ForegroundColor Yellow
    docker images ${IMAGE_NAME}:${IMAGE_TAG}
} else {
    Write-Host "`n❌ 빌드 실패!" -ForegroundColor Red
    exit 1
}

Write-Host "`n다음 단계:" -ForegroundColor Yellow
Write-Host "1. 로컬 실행: .\scripts\run-local.ps1" -ForegroundColor White
Write-Host "2. ECR 푸시: .\scripts\push-to-ecr.ps1" -ForegroundColor White
```

#### scripts/run-local.ps1
```powershell
# FastAPI 로컬 실행 스크립트
Write-Host "================================" -ForegroundColor Cyan
Write-Host "FastAPI 로컬 실행" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$IMAGE_NAME = "fastapi-aws"
$IMAGE_TAG = "latest"
$CONTAINER_NAME = "fastapi-local"
$PORT = "8000"

# 기존 컨테이너 중지 및 제거
Write-Host "`n🧹 기존 컨테이너 정리 중..." -ForegroundColor Yellow
docker stop $CONTAINER_NAME 2>$null
docker rm $CONTAINER_NAME 2>$null

# 컨테이너 실행
Write-Host "`n🚀 컨테이너 시작 중..." -ForegroundColor Green
docker run -d `
    --name $CONTAINER_NAME `
    -p ${PORT}:8000 `
    ${IMAGE_NAME}:${IMAGE_TAG}

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ 컨테이너 실행 성공!" -ForegroundColor Green
    Write-Host "`n📡 접속 정보:" -ForegroundColor Yellow
    Write-Host "  - API: http://localhost:${PORT}" -ForegroundColor White
    Write-Host "  - Swagger UI: http://localhost:${PORT}/docs" -ForegroundColor White
    Write-Host "  - ReDoc: http://localhost:${PORT}/redoc" -ForegroundColor White
    
    # 로그 확인
    Write-Host "`n📋 컨테이너 로그 (Ctrl+C로 종료):" -ForegroundColor Yellow
    Start-Sleep -Seconds 2
    docker logs -f $CONTAINER_NAME
} else {
    Write-Host "`n❌ 컨테이너 실행 실패!" -ForegroundColor Red
    exit 1
}
```

#### scripts/push-to-ecr.ps1
```powershell
# ECR에 이미지 푸시하는 스크립트
Write-Host "================================" -ForegroundColor Cyan
Write-Host "AWS ECR에 이미지 푸시" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

# 설정값
$AWS_REGION = "ap-northeast-2"
$ECR_REPO_NAME = "fastapi-aws"
$IMAGE_TAG = "latest"

# AWS 계정 ID 가져오기
Write-Host "`n🔍 AWS 계정 정보 확인 중..." -ForegroundColor Yellow
$AWS_ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)

if (-not $AWS_ACCOUNT_ID) {
    Write-Host "❌ AWS 자격증명을 찾을 수 없습니다!" -ForegroundColor Red
    Write-Host "aws configure를 먼저 실행하세요." -ForegroundColor Yellow
    exit 1
}

Write-Host "AWS 계정 ID: $AWS_ACCOUNT_ID" -ForegroundColor Green

# ECR 로그인
Write-Host "`n🔐 ECR 로그인 중..." -ForegroundColor Yellow
$ECR_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

aws ecr get-login-password --region $AWS_REGION | `
    docker login --username AWS --password-stdin $ECR_URI

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ ECR 로그인 실패!" -ForegroundColor Red
    exit 1
}

# ECR 리포지토리 존재 확인
Write-Host "`n📦 ECR 리포지토리 확인 중..." -ForegroundColor Yellow
$repoExists = aws ecr describe-repositories `
    --repository-names $ECR_REPO_NAME `
    --region $AWS_REGION 2>$null

if (-not $repoExists) {
    Write-Host "리포지토리가 없습니다. 생성 중..." -ForegroundColor Yellow
    aws ecr create-repository `
        --repository-name $ECR_REPO_NAME `
        --region $AWS_REGION
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ 리포지토리 생성 완료!" -ForegroundColor Green
    } else {
        Write-Host "❌ 리포지토리 생성 실패!" -ForegroundColor Red
        exit 1
    }
}

# 이미지 태깅
Write-Host "`n🏷️  이미지 태깅 중..." -ForegroundColor Yellow
$ECR_IMAGE = "${ECR_URI}/${ECR_REPO_NAME}:${IMAGE_TAG}"

docker tag ${ECR_REPO_NAME}:${IMAGE_TAG} $ECR_IMAGE

# 이미지 푸시
Write-Host "`n⬆️  이미지 푸시 중..." -ForegroundColor Yellow
docker push $ECR_IMAGE

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ 이미지 푸시 성공!" -ForegroundColor Green
    Write-Host "ECR 이미지 URI: $ECR_IMAGE" -ForegroundColor Cyan
    
    Write-Host "`n다음 단계:" -ForegroundColor Yellow
    Write-Host "1. App Runner 배포: .\deployments\1-app-runner\README.md 참조" -ForegroundColor White
    Write-Host "2. ECS 배포: .\deployments\2-ecs-fargate\README.md 참조" -ForegroundColor White
    Write-Host "3. EKS 배포: .\deployments\3-eks\README.md 참조" -ForegroundColor White
} else {
    Write-Host "`n❌ 이미지 푸시 실패!" -ForegroundColor Red
    exit 1
}
```

#### scripts/test-api.ps1
```powershell
# API 테스트 스크립트
Write-Host "================================" -ForegroundColor Cyan
Write-Host "FastAPI 엔드포인트 테스트" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan

$BASE_URL = "http://localhost:8000"

# 1. Health Check
Write-Host "`n1️⃣  Health Check 테스트" -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "$BASE_URL/health" -Method Get
Write-Host "응답: $($response | ConvertTo-Json)" -ForegroundColor Green

# 2. Root Endpoint
Write-Host "`n2️⃣  Root Endpoint 테스트" -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "$BASE_URL/" -Method Get
Write-Host "응답: $($response | ConvertTo-Json)" -ForegroundColor Green

# 3. GET Item
Write-Host "`n3️⃣  GET Item 테스트" -ForegroundColor Yellow
$response = Invoke-RestMethod -Uri "$BASE_URL/items/42?q=test" -Method Get
Write-Host "응답: $($response | ConvertTo-Json)" -ForegroundColor Green

# 4. POST Item
Write-Host "`n4️⃣  POST Item 테스트" -ForegroundColor Yellow
$body = @{
    name = "Test Item"
    description = "Test Description"
    price = 99.99
    tax = 10.0
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "$BASE_URL/items/" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"

Write-Host "응답: $($response | ConvertTo-Json)" -ForegroundColor Green

Write-Host "`n✅ 모든 테스트 완료!" -ForegroundColor Green
```

---

## Django 가이드

### Django 애플리케이션 예제

#### Django 프로젝트 구조
```
django-aws/
├── app/
│   ├── manage.py
│   ├── requirements.txt
│   ├── myproject/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── api/
│       ├── __init__.py
│       ├── views.py
│       └── urls.py
```

#### app/requirements.txt
```txt
Django==5.0.1
gunicorn==21.2.0
psycopg2-binary==2.9.9
django-environ==0.11.2
whitenoise==6.6.0
```

### Django Dockerfile

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# 시스템 의존성
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성
COPY app/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# 시스템 의존성
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 비-root 사용자
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Builder에서 패키지 복사
COPY --from=builder /root/.local /home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH

# 애플리케이션 코드
COPY app/ .

# Static 파일 수집
RUN python manage.py collectstatic --noinput

# 소유권 변경
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

# Gunicorn으로 실행
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
```

### Django docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: django-app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - SECRET_KEY=django-insecure-dev-key
      - DATABASE_URL=postgresql://django_user:django_password@db:5432/django_db
    depends_on:
      - db
    volumes:
      - ./app:/app
    command: python manage.py runserver 0.0.0.0:8000

  db:
    image: postgres:16-alpine
    container_name: django-db
    environment:
      - POSTGRES_DB=django_db
      - POSTGRES_USER=django_user
      - POSTGRES_PASSWORD=django_password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 환경 변수 관리

환경 변수를 안전하게 관리하는 것은 프로덕션 배포에서 매우 중요합니다.

### 로컬 개발 환경

#### .env 파일 사용

**.env.example** (버전 관리에 포함)
```bash
# Application Settings
ENV=development
DEBUG=true
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# AWS Settings
AWS_REGION=ap-northeast-2
AWS_BUCKET_NAME=my-app-bucket

# API Keys (절대 실제 값을 넣지 마세요!)
API_KEY=your-api-key-here
THIRD_PARTY_API_KEY=your-third-party-key
```

**.env** (버전 관리에서 제외, .gitignore에 추가)
```bash
ENV=development
DEBUG=true
SECRET_KEY=super-secret-key-do-not-commit
DATABASE_URL=postgresql://myuser:mypass@localhost:5432/mydb
API_KEY=real-api-key-value
```

**.gitignore**
```
.env
*.env
!.env.example
```

#### FastAPI에서 환경 변수 사용

**config.py**
```python
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    env: str = "development"
    debug: bool = True
    secret_key: str
    database_url: str
    api_key: str

    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()

# 사용 예
settings = get_settings()
```

**main.py**
```python
from fastapi import FastAPI, Depends
from config import get_settings, Settings

app = FastAPI()

@app.get("/config")
def read_config(settings: Settings = Depends(get_settings)):
    return {
        "env": settings.env,
        "debug": settings.debug,
        # 민감한 정보는 노출하지 않음
    }
```

**requirements.txt에 추가**
```txt
pydantic-settings==2.5.2
python-dotenv==1.0.1
```

### Docker 환경에서 환경 변수

#### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    env_file:
      - .env
    environment:
      - ENV=${ENV}
      - DEBUG=${DEBUG}
      - DATABASE_URL=${DATABASE_URL}
    # 또는 직접 지정
    # environment:
    #   - ENV=production
    #   - DEBUG=false
```

#### Dockerfile에서 빌드 시 환경 변수
```dockerfile
# 빌드 타임 변수 (ARG)
ARG PYTHON_VERSION=3.12

FROM python:${PYTHON_VERSION}-slim

# 런타임 환경 변수 (ENV)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_HOME=/app

WORKDIR $APP_HOME
```

### AWS 배포 시 환경 변수

#### AWS App Runner
```yaml
# apprunner.yaml
version: 1.0
runtime: python3
build:
  commands:
    build:
      - pip install -r requirements.txt
run:
  runtime-version: 3.12
  command: uvicorn main:app --host 0.0.0.0 --port 8000
  network:
    port: 8000
    env:
      - name: ENV
        value: production
      - name: DEBUG
        value: "false"
```

#### AWS ECS Task Definition
```json
{
  "family": "fastapi-task",
  "containerDefinitions": [
    {
      "name": "fastapi",
      "image": "123456789.dkr.ecr.ap-northeast-2.amazonaws.com/fastapi:latest",
      "environment": [
        {
          "name": "ENV",
          "value": "production"
        },
        {
          "name": "AWS_REGION",
          "value": "ap-northeast-2"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:ap-northeast-2:123456789:secret:db-url"
        },
        {
          "name": "API_KEY",
          "valueFrom": "arn:aws:secretsmanager:ap-northeast-2:123456789:secret:api-key"
        }
      ]
    }
  ]
}
```

### AWS Secrets Manager 사용

#### 시크릿 생성
```powershell
# 시크릿 생성
aws secretsmanager create-secret `
    --name myapp/database-url `
    --description "Database connection URL" `
    --secret-string "postgresql://user:pass@host:5432/db"

# 시크릿 조회
aws secretsmanager get-secret-value `
    --secret-id myapp/database-url `
    --query SecretString `
    --output text
```

#### Python에서 Secrets Manager 사용
```python
import boto3
import json
from functools import lru_cache

def get_secret(secret_name: str, region_name: str = "ap-northeast-2"):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
        return get_secret_value_response['SecretString']
    except Exception as e:
        raise e

@lru_cache()
def get_database_url():
    return get_secret("myapp/database-url")
```

**requirements.txt에 추가**
```txt
boto3==1.35.0
```

### 환경별 설정 분리

**config/**
```
config/
├── __init__.py
├── base.py
├── development.py
├── production.py
└── test.py
```

**config/base.py**
```python
from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    app_name: str = "My FastAPI App"
    secret_key: str

    class Config:
        env_file = ".env"
```

**config/development.py**
```python
from .base import BaseConfig

class DevelopmentConfig(BaseConfig):
    debug: bool = True
    database_url: str = "sqlite:///./dev.db"
```

**config/production.py**
```python
from .base import BaseConfig

class ProductionConfig(BaseConfig):
    debug: bool = False
    database_url: str  # 반드시 설정되어야 함
```

**config/__init__.py**
```python
import os
from .development import DevelopmentConfig
from .production import ProductionConfig

def get_config():
    env = os.getenv("ENV", "development")

    if env == "production":
        return ProductionConfig()
    else:
        return DevelopmentConfig()

config = get_config()
```

---

## 데이터베이스 연결

컨테이너 애플리케이션을 데이터베이스와 연결하는 방법을 알아봅니다.

### FastAPI + PostgreSQL 연결

#### 1. 필요한 패키지 설치

**requirements.txt**
```txt
sqlalchemy==2.0.35
psycopg2-binary==2.9.9
alembic==1.13.3
```

#### 2. 데이터베이스 설정

**database.py**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

# 데이터베이스 URL
SQLALCHEMY_DATABASE_URL = settings.database_url

# 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # 연결 확인
    pool_size=10,
    max_overflow=20
)

# 세션 팩토리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 3. 모델 정의

**models.py**
```python
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

#### 4. 스키마 정의

**schemas.py**
```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
```

#### 5. CRUD 작업

**crud.py**
```python
from sqlalchemy.orm import Session
from models import Item
from schemas import ItemCreate

def get_item(db: Session, item_id: int):
    return db.query(Item).filter(Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
```

#### 6. API 엔드포인트

**main.py**
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

import crud
import models
import schemas
from database import engine, get_db

# 테이블 생성
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/items/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.get("/items/", response_model=List[schemas.ItemResponse])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def read_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}", response_model=schemas.ItemResponse)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
```

### Docker Compose로 로컬 테스트

**docker-compose.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://fastapi:fastapi123@db:5432/fastapi_db
    depends_on:
      - db
    volumes:
      - ./app:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=fastapi_db
      - POSTGRES_USER=fastapi
      - POSTGRES_PASSWORD=fastapi123
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fastapi"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### AWS RDS 연결

#### 1. RDS 인스턴스 생성

```powershell
# RDS PostgreSQL 인스턴스 생성
aws rds create-db-instance `
    --db-instance-identifier myapp-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 16.3 `
    --master-username admin `
    --master-user-password YourSecurePassword123! `
    --allocated-storage 20 `
    --vpc-security-group-ids sg-xxxxxxxxx `
    --db-subnet-group-name myapp-subnet-group `
    --backup-retention-period 7 `
    --publicly-accessible

# 엔드포인트 확인
aws rds describe-db-instances `
    --db-instance-identifier myapp-db `
    --query 'DBInstances[0].Endpoint.Address' `
    --output text
```

#### 2. 보안 그룹 설정

```powershell
# PostgreSQL 포트(5432) 인바운드 규칙 추가
aws ec2 authorize-security-group-ingress `
    --group-id sg-xxxxxxxxx `
    --protocol tcp `
    --port 5432 `
    --source-group sg-yyyyyyyyy  # ECS 태스크의 보안 그룹
```

#### 3. 연결 문자열

```bash
# Secrets Manager에 저장
DATABASE_URL=postgresql://admin:YourSecurePassword123!@myapp-db.xxxxxx.ap-northeast-2.rds.amazonaws.com:5432/postgres
```

#### 4. ECS Task Definition에서 RDS 사용

```json
{
  "family": "fastapi-task",
  "networkMode": "awsvpc",
  "containerDefinitions": [
    {
      "name": "fastapi",
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:ap-northeast-2:123456789:secret:database-url"
        }
      ]
    }
  ]
}
```

### 데이터베이스 마이그레이션 (Alembic)

#### 1. Alembic 초기화

```powershell
alembic init alembic
```

#### 2. alembic.ini 수정

```ini
# sqlalchemy.url을 주석 처리 (코드에서 동적으로 설정)
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

#### 3. alembic/env.py 수정

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# 모델과 설정 import
from database import SQLALCHEMY_DATABASE_URL
from models import Base

config = context.config

# alembic.ini에서 읽지 않고 직접 설정
config.set_main_option("sqlalchemy.url", SQLALCHEMY_DATABASE_URL)

target_metadata = Base.metadata

# ... 나머지 코드
```

#### 4. 마이그레이션 생성 및 적용

```powershell
# 마이그레이션 파일 자동 생성
alembic revision --autogenerate -m "Create items table"

# 마이그레이션 적용
alembic upgrade head

# 롤백
alembic downgrade -1
```

#### 5. Dockerfile에 마이그레이션 추가

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 시작 스크립트
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]
```

**start.sh**
```bash
#!/bin/bash

# 마이그레이션 실행
alembic upgrade head

# 애플리케이션 시작
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 배포 옵션

### 1. AWS App Runner (⭐ 초급)

#### 특징
- **난이도**: ⭐ 초급
- **관리 수준**: 완전 관리형
- **비용**: vCPU/메모리 시간당 과금
- **배포 시간**: 5-10분

#### 장점
✅ 가장 빠른 배포 (몇 분 안에 완료)
✅ HTTPS 자동 설정
✅ 자동 스케일링 (요청 기반)
✅ 인프라 관리 완전 불필요
✅ 롤링 배포 자동

#### 단점
❌ 제한된 커스터마이징
❌ VPC 통합 제한적
❌ 다른 AWS 서비스 통합 제약

#### 배포 명령어
```powershell
# ECR에 이미지 푸시 후
aws apprunner create-service `
    --service-name fastapi-app `
    --source-configuration file://apprunner.yaml
```

#### 예상 비용
```
vCPU: $0.064/vCPU-시간
메모리: $0.007/GB-시간

예시 (1 vCPU, 2GB, 24시간 실행):
= (1 × $0.064 + 2 × $0.007) × 24 × 30
= $57.6/월
```

### 2. AWS ECS (Fargate) (⭐⭐ 중급)

#### 특징
- **난이도**: ⭐⭐ 중급
- **관리 수준**: 서버리스 컨테이너
- **비용**: vCPU/메모리 시간당 과금
- **배포 시간**: 10-20분

#### 장점
✅ 서버 관리 불필요
✅ 세밀한 리소스 제어
✅ VPC 완전 통합
✅ 다른 AWS 서비스와 통합 용이 (RDS, ElastiCache 등)
✅ Blue/Green 배포 지원
✅ Auto Scaling 설정 가능

#### 단점
❌ App Runner보다 설정 복잡
❌ 러닝 커브 존재
❌ 네트워킹 지식 필요

#### 배포 명령어
```powershell
# 1. Task Definition 등록
aws ecs register-task-definition `
    --cli-input-json file://task-definition.json

# 2. 서비스 생성
aws ecs create-service `
    --cluster my-cluster `
    --service-name fastapi-service `
    --task-definition fastapi-task `
    --desired-count 2 `
    --launch-type FARGATE
```

#### 예상 비용
```
vCPU: $0.04656/vCPU-시간
메모리: $0.00511/GB-시간

예시 (0.5 vCPU, 1GB, 24시간 실행):
= (0.5 × $0.04656 + 1 × $0.00511) × 24 × 30
= $20.52/월
```

### 3. AWS EKS (⭐⭐⭐ 고급)

#### 특징
- **난이도**: ⭐⭐⭐ 고급
- **관리 수준**: Kubernetes 오케스트레이션
- **비용**: 클러스터 시간당 $0.10 + 워커 노드
- **배포 시간**: 30-60분

#### 장점
✅ Kubernetes 표준 사용
✅ 복잡한 마이크로서비스 아키텍처 지원
✅ 멀티 클라우드 호환성
✅ 강력한 스케일링 및 자동화
✅ Helm Charts 사용 가능
✅ Service Mesh 통합 (Istio, Linkerd)

#### 단점
❌ 높은 학습 곡선
❌ 관리 복잡도 증가
❌ 비용이 상대적으로 높음
❌ Kubernetes 지식 필수

#### 배포 명령어
```powershell
# 1. 클러스터 생성
eksctl create cluster `
    --name my-cluster `
    --region ap-northeast-2 `
    --nodegroup-name standard-workers `
    --node-type t3.medium `
    --nodes 2

# 2. kubectl 설정
aws eks update-kubeconfig --name my-cluster --region ap-northeast-2

# 3. 배포
kubectl apply -f k8s/
```

#### 예상 비용
```
클러스터: $0.10/시간 = $73/월
워커 노드 (t3.medium × 2): $0.0416/시간 × 2 = $60/월

총 예상 비용: $133/월
```

---

## 실전 예제

### 예제 1: FastAPI + App Runner 배포

#### 전체 워크플로우
```powershell
# 1. 프로젝트 디렉토리 생성
mkdir C:\projects\fastapi-aws
cd C:\projects\fastapi-aws

# 2. 애플리케이션 코드 작성
# (위의 FastAPI 예제 코드 사용)

# 3. 이미지 빌드
docker build -t fastapi-aws:latest .

# 4. 로컬 테스트
docker run -d -p 8000:8000 --name fastapi-test fastapi-aws:latest

# 브라우저에서 확인: http://localhost:8000/docs

# 5. ECR에 푸시
$AWS_ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
$AWS_REGION = "ap-northeast-2"

# ECR 로그인
aws ecr get-login-password --region $AWS_REGION | `
    docker login --username AWS --password-stdin `
    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# 리포지토리 생성
aws ecr create-repository --repository-name fastapi-aws --region $AWS_REGION

# 이미지 태깅 및 푸시
docker tag fastapi-aws:latest `
    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/fastapi-aws:latest

docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/fastapi-aws:latest

# 6. App Runner 서비스 생성
$ECR_IMAGE_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/fastapi-aws:latest"

aws apprunner create-service `
    --service-name fastapi-app `
    --source-configuration '{
        "ImageRepository": {
            "ImageIdentifier": "'$ECR_IMAGE_URI'",
            "ImageRepositoryType": "ECR",
            "ImageConfiguration": {
                "Port": "8000"
            }
        },
        "AutoDeploymentsEnabled": true
    }' `
    --instance-configuration '{
        "Cpu": "1 vCPU",
        "Memory": "2 GB"
    }'

# 7. 서비스 URL 확인
aws apprunner describe-service `
    --service-arn [SERVICE_ARN] `
    --query 'Service.ServiceUrl' `
    --output text
```

### 예제 2: Django + ECS Fargate 배포

```powershell
# 1. VPC 및 보안 그룹 생성
$VPC_ID = (aws ec2 create-vpc `
    --cidr-block 10.0.0.0/16 `
    --query 'Vpc.VpcId' `
    --output text)

# 2. ECS 클러스터 생성
aws ecs create-cluster --cluster-name django-cluster

# 3. Task Definition 등록
aws ecs register-task-definition --cli-input-json file://task-definition.json

# 4. 서비스 생성
aws ecs create-service `
    --cluster django-cluster `
    --service-name django-service `
    --task-definition django-task:1 `
    --desired-count 2 `
    --launch-type FARGATE `
    --network-configuration '{
        "awsvpcConfiguration": {
            "subnets": ["subnet-xxx", "subnet-yyy"],
            "securityGroups": ["sg-xxx"],
            "assignPublicIp": "ENABLED"
        }
    }'
```

### 예제 3: FastAPI + RDS + Secrets Manager 연동

이 예제는 FastAPI 애플리케이션을 RDS PostgreSQL과 연결하고, Secrets Manager를 사용하여 데이터베이스 자격증명을 안전하게 관리합니다.

#### 1. RDS 인스턴스 생성

```powershell
# RDS PostgreSQL 생성
aws rds create-db-instance `
    --db-instance-identifier fastapi-db `
    --db-instance-class db.t3.micro `
    --engine postgres `
    --engine-version 16.3 `
    --master-username dbadmin `
    --master-user-password "TempPassword123!" `
    --allocated-storage 20 `
    --backup-retention-period 7 `
    --db-name fastapidb

# 엔드포인트 확인 (생성 완료 후)
aws rds describe-db-instances `
    --db-instance-identifier fastapi-db `
    --query 'DBInstances[0].Endpoint.Address' `
    --output text
```

#### 2. Secrets Manager에 DB 자격증명 저장

```powershell
# 시크릿 생성
aws secretsmanager create-secret `
    --name fastapi/database `
    --description "FastAPI Database Credentials" `
    --secret-string '{
        "username": "dbadmin",
        "password": "SecurePassword123!",
        "engine": "postgres",
        "host": "fastapi-db.xxxxx.ap-northeast-2.rds.amazonaws.com",
        "port": 5432,
        "dbname": "fastapidb"
    }'

# 시크릿 ARN 확인
aws secretsmanager describe-secret `
    --secret-id fastapi/database `
    --query 'ARN' `
    --output text
```

#### 3. FastAPI 코드 수정 (database.py)

```python
import boto3
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

@lru_cache()
def get_db_credentials():
    """Secrets Manager에서 DB 자격증명 가져오기"""
    secret_name = "fastapi/database"
    region_name = "ap-northeast-2"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    secret_value = client.get_secret_value(SecretId=secret_name)
    return json.loads(secret_value['SecretString'])

def get_database_url():
    """데이터베이스 URL 생성"""
    creds = get_db_credentials()
    return (
        f"postgresql://{creds['username']}:{creds['password']}"
        f"@{creds['host']}:{creds['port']}/{creds['dbname']}"
    )

# 엔진 생성
engine = create_engine(
    get_database_url(),
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

#### 4. ECS Task Definition

```json
{
  "family": "fastapi-rds-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::123456789:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::123456789:role/fastapiTaskRole",
  "containerDefinitions": [
    {
      "name": "fastapi",
      "image": "123456789.dkr.ecr.ap-northeast-2.amazonaws.com/fastapi-app:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "ENV",
          "value": "production"
        },
        {
          "name": "AWS_REGION",
          "value": "ap-northeast-2"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/fastapi-app",
          "awslogs-region": "ap-northeast-2",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}
```

#### 5. IAM 역할 설정

```powershell
# Task Role에 Secrets Manager 권한 추가
aws iam attach-role-policy `
    --role-name fastapiTaskRole `
    --policy-arn arn:aws:iam::aws:policy/SecretsManagerReadWrite

# 또는 최소 권한 정책 생성
$POLICY_JSON = @"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue"
      ],
      "Resource": "arn:aws:secretsmanager:ap-northeast-2:123456789:secret:fastapi/database-*"
    }
  ]
}
"@

aws iam create-policy `
    --policy-name FastAPISecretsPolicy `
    --policy-document $POLICY_JSON
```

### 예제 4: Docker Compose를 사용한 풀스택 로컬 개발 환경

로컬에서 FastAPI, PostgreSQL, Redis를 모두 실행하는 완전한 개발 환경 구성

#### docker-compose.yml

```yaml
version: '3.8'

services:
  # FastAPI 애플리케이션
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: fastapi-api
    ports:
      - "8000:8000"
    environment:
      - ENV=development
      - DEBUG=true
      - DATABASE_URL=postgresql://fastapi:fastapi123@db:5432/fastapi_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - ./app:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    networks:
      - app-network

  # PostgreSQL 데이터베이스
  db:
    image: postgres:16-alpine
    container_name: fastapi-db
    environment:
      - POSTGRES_DB=fastapi_db
      - POSTGRES_USER=fastapi
      - POSTGRES_PASSWORD=fastapi123
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U fastapi -d fastapi_db"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  # Redis 캐시
  redis:
    image: redis:7-alpine
    container_name: fastapi-redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5
    networks:
      - app-network

  # pgAdmin (DB 관리 도구)
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: fastapi-pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@example.com
      - PGADMIN_DEFAULT_PASSWORD=admin
    ports:
      - "5050:80"
    depends_on:
      - db
    networks:
      - app-network

  # Redis Commander (Redis 관리 도구)
  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: fastapi-redis-commander
    environment:
      - REDIS_HOSTS=local:redis:6379
    ports:
      - "8081:8081"
    depends_on:
      - redis
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

#### Dockerfile.dev (개발용)

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 개발 도구 설치
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# 소스 코드는 볼륨 마운트로 제공됨
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

#### requirements-dev.txt

```txt
pytest==8.3.0
pytest-cov==5.0.0
pytest-asyncio==0.24.0
black==24.8.0
flake8==7.1.0
mypy==1.11.0
ipython==8.26.0
```

#### 사용 방법

```powershell
# 전체 환경 시작
docker-compose up -d

# 로그 확인
docker-compose logs -f api

# DB 마이그레이션
docker-compose exec api alembic upgrade head

# 테스트 실행
docker-compose exec api pytest

# 특정 서비스만 재시작
docker-compose restart api

# 전체 종료 및 데이터 삭제
docker-compose down -v

# 접속 정보:
# - API: http://localhost:8000
# - Swagger: http://localhost:8000/docs
# - pgAdmin: http://localhost:5050
# - Redis Commander: http://localhost:8081
```

### 예제 5: GitHub Actions로 자동 테스트 및 배포

완전한 CI/CD 파이프라인 구축

#### .github/workflows/ci-cd.yml

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  AWS_REGION: ap-northeast-2
  ECR_REPOSITORY: fastapi-app
  ECS_CLUSTER: fastapi-cluster
  ECS_SERVICE: fastapi-service

jobs:
  # 1. 코드 품질 검사
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install black flake8 mypy

      - name: Run Black (code formatting)
        run: black --check app/

      - name: Run Flake8 (linting)
        run: flake8 app/ --max-line-length=100

      - name: Run MyPy (type checking)
        run: mypy app/ --ignore-missing-imports

  # 2. 테스트
  test:
    needs: lint
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

      redis:
        image: redis:7-alpine
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379/0
        run: |
          pytest tests/ -v --cov=app --cov-report=xml --cov-report=html

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

  # 3. Docker 이미지 빌드 및 보안 스캔
  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.event_name == 'push'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          load: true
          tags: ${{ env.ECR_REPOSITORY }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.ECR_REPOSITORY }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  # 4. ECR 푸시 및 ECS 배포 (main 브랜치만)
  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker tag $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG $ECR_REGISTRY/$ECR_REPOSITORY:latest
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:latest
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Download task definition
        run: |
          aws ecs describe-task-definition \
            --task-definition fastapi-task \
            --query taskDefinition > task-definition.json

      - name: Fill in the new image ID in the Amazon ECS task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: task-definition.json
          container-name: fastapi
          image: ${{ steps.build-image.outputs.image }}

      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true

      - name: Send deployment notification
        if: success()
        run: |
          echo "Deployment successful! Image: ${{ steps.build-image.outputs.image }}"
          # Slack, Discord 등으로 알림 전송 가능
```

---

## 성능 최적화

컨테이너 이미지와 애플리케이션의 성능을 최적화하는 방법을 알아봅니다.

### Docker 이미지 최적화

#### 1. 멀티스테이지 빌드 활용

**최적화 전 (단일 스테이지)**
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
# 결과: ~1GB
```

**최적화 후 (멀티스테이지)**
```dockerfile
# Build stage
FROM python:3.12-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runtime stage
FROM python:3.12-slim
RUN useradd -m appuser
WORKDIR /app
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .
USER appuser
ENV PATH=/home/appuser/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
# 결과: ~200MB
```

#### 2. .dockerignore 파일 활용

**.dockerignore**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# 테스트 및 개발 도구
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.ruff_cache/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Git
.git/
.gitignore

# 문서
*.md
docs/
examples/

# 로그
*.log

# 환경 변수
.env
.env.*
!.env.example

# 기타
node_modules/
.DS_Store
Thumbs.db
```

#### 3. 레이어 캐싱 최적화

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 1. 변경이 적은 것부터 COPY (의존성)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. 자주 변경되는 것은 나중에 (소스 코드)
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

#### 4. Alpine vs Slim 이미지 비교

```dockerfile
# Alpine (최소 크기, 하지만 호환성 문제 가능)
FROM python:3.12-alpine  # ~50MB
RUN apk add --no-cache gcc musl-dev linux-headers

# Slim (권장, 균형잡힌 선택)
FROM python:3.12-slim  # ~150MB
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Full (피하기, 불필요하게 큼)
FROM python:3.12  # ~900MB+
```

#### 5. 이미지 크기 확인 및 분석

```powershell
# 이미지 크기 확인
docker images fastapi-app

# 이미지 레이어 분석
docker history fastapi-app:latest

# dive 도구로 상세 분석 (설치 필요)
dive fastapi-app:latest
```

### 애플리케이션 성능 최적화

#### 1. Uvicorn Worker 설정

**단일 Worker (개발용)**
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**멀티 Worker (프로덕션)**
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

**Gunicorn + Uvicorn Worker (권장)**
```dockerfile
# requirements.txt에 추가
# gunicorn==21.2.0

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

**Worker 수 계산**
```python
# 권장 Worker 수 = (2 x CPU 코어 수) + 1
# 예: 2 코어 -> 5 workers
# 예: 4 코어 -> 9 workers
```

#### 2. 연결 풀링 설정

**데이터베이스 연결 풀**
```python
from sqlalchemy import create_engine

engine = create_engine(
    DATABASE_URL,
    pool_size=10,          # 기본 연결 수
    max_overflow=20,       # 추가 가능한 최대 연결 수
    pool_timeout=30,       # 연결 대기 시간 (초)
    pool_recycle=3600,     # 연결 재사용 시간 (초)
    pool_pre_ping=True,    # 연결 유효성 검사
)
```

**Redis 연결 풀**
```python
from redis import ConnectionPool, Redis

pool = ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=50,
    decode_responses=True
)

redis_client = Redis(connection_pool=pool)
```

#### 3. 캐싱 전략

**메모리 캐싱 (functools.lru_cache)**
```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=128)
def get_expensive_data(param: str):
    # 비용이 큰 연산
    return perform_expensive_operation(param)
```

**Redis 캐싱**
```python
from fastapi import FastAPI
import redis
import json

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # 캐시 확인
    cache_key = f"item:{item_id}"
    cached = redis_client.get(cache_key)

    if cached:
        return json.loads(cached)

    # DB에서 조회
    item = db.query(Item).filter(Item.id == item_id).first()

    # 캐시 저장 (TTL 1시간)
    redis_client.setex(cache_key, 3600, json.dumps(item))

    return item
```

**HTTP 캐싱 헤더**
```python
from fastapi import Response

@app.get("/static-data")
async def get_static_data(response: Response):
    # 캐시 제어 헤더 설정
    response.headers["Cache-Control"] = "public, max-age=3600"
    response.headers["ETag"] = "v1.0.0"

    return {"data": "static content"}
```

#### 4. 비동기 처리

**비동기 데이터베이스 쿼리**
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Async 엔진
async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=True,
    pool_size=20
)

AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@app.get("/items/")
async def get_items():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Item))
        items = result.scalars().all()
        return items
```

**비동기 HTTP 요청**
```python
import httpx

@app.get("/fetch-external")
async def fetch_external_api():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
        return response.json()
```

#### 5. 압축 활용

**GZip 압축 미들웨어**
```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# 500 bytes 이상의 응답을 압축
app.add_middleware(GZipMiddleware, minimum_size=500)
```

#### 6. 페이지네이션

**Offset-based 페이지네이션**
```python
from fastapi import Query

@app.get("/items/")
async def get_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items
```

**Cursor-based 페이지네이션 (더 효율적)**
```python
@app.get("/items/")
async def get_items(
    cursor: Optional[int] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    query = db.query(Item)

    if cursor:
        query = query.filter(Item.id > cursor)

    items = query.order_by(Item.id).limit(limit).all()

    next_cursor = items[-1].id if items else None

    return {
        "items": items,
        "next_cursor": next_cursor
    }
```

### AWS 리소스 최적화

#### 1. ECS Fargate Task 크기 조정

```json
{
  "family": "fastapi-task",
  "cpu": "512",      // 0.5 vCPU (256, 512, 1024, 2048, 4096)
  "memory": "1024",  // 1GB (512MB ~ 30GB)
  "containerDefinitions": [
    {
      "name": "fastapi",
      "cpu": 256,     // 컨테이너별 할당
      "memory": 512,
      "memoryReservation": 256  // 소프트 리미트
    }
  ]
}
```

#### 2. Auto Scaling 설정

```powershell
# Target Tracking Scaling Policy
aws application-autoscaling put-scaling-policy `
    --service-namespace ecs `
    --scalable-dimension ecs:service:DesiredCount `
    --resource-id service/my-cluster/fastapi-service `
    --policy-name cpu-scaling-policy `
    --policy-type TargetTrackingScaling `
    --target-tracking-scaling-policy-configuration '{
        "TargetValue": 70.0,
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ECSServiceAverageCPUUtilization"
        },
        "ScaleOutCooldown": 60,
        "ScaleInCooldown": 120
    }'
```

#### 3. CloudFront CDN 사용

정적 자산을 CloudFront로 서빙하여 응답 시간 단축:

```python
# 정적 파일을 S3 + CloudFront로 분리
STATIC_URL = "https://d111111abcdef8.cloudfront.net/static/"
```

### 성능 모니터링

#### 로컬 프로파일링

```python
# 프로파일링 미들웨어
import time
from fastapi import Request

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

#### 부하 테스트

```powershell
# Apache Bench
ab -n 1000 -c 10 http://localhost:8000/

# wrk (더 강력함)
wrk -t12 -c400 -d30s http://localhost:8000/

# Locust (Python 기반)
pip install locust
locust -f locustfile.py
```

**locustfile.py**
```python
from locust import HttpUser, task, between

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def get_items(self):
        self.client.get("/items/")

    @task(1)
    def create_item(self):
        self.client.post("/items/", json={
            "name": "Test Item",
            "price": 99.99
        })
```

---

## CI/CD 파이프라인

GitHub Actions를 사용한 자동화된 배포 파이프라인을 구축합니다.

### GitHub Actions 워크플로우

#### 1. 기본 CI/CD 파이프라인

**.github/workflows/deploy.yml**
```yaml
name: Deploy to AWS

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

env:
  AWS_REGION: ap-northeast-2
  ECR_REPOSITORY: fastapi-app

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.12'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest --cov=app tests/

    - name: Upload coverage
      uses: codecov/codecov-action@v3

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to Amazon ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v2

    - name: Build, tag, and push image to Amazon ECR
      id: build-image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
        echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

    - name: Update ECS service
      run: |
        aws ecs update-service \
          --cluster my-cluster \
          --service fastapi-service \
          --force-new-deployment
```

#### 2. App Runner 자동 배포

**.github/workflows/deploy-apprunner.yml**
```yaml
name: Deploy to App Runner

on:
  push:
    branches: [ main ]

env:
  AWS_REGION: ap-northeast-2
  SERVICE_NAME: fastapi-app

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v4
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: ${{ env.AWS_REGION }}

    - name: Login to ECR
      id: login-ecr
      uses: aws-actions/amazon-ecr-login@v2

    - name: Build and push Docker image
      env:
        ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
        ECR_REPOSITORY: fastapi-app
        IMAGE_TAG: ${{ github.sha }}
      run: |
        docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
        docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

    - name: Deploy to App Runner
      run: |
        aws apprunner start-deployment \
          --service-arn ${{ secrets.APPRUNNER_SERVICE_ARN }}
```

#### 3. 멀티 환경 배포 (Dev/Staging/Prod)

**.github/workflows/deploy-multi-env.yml**
```yaml
name: Multi-Environment Deploy

on:
  push:
    branches:
      - develop
      - staging
      - main

jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      environment: ${{ steps.set-env.outputs.environment }}
    steps:
      - id: set-env
        run: |
          if [ "${{ github.ref }}" == "refs/heads/main" ]; then
            echo "environment=production" >> $GITHUB_OUTPUT
          elif [ "${{ github.ref }}" == "refs/heads/staging" ]; then
            echo "environment=staging" >> $GITHUB_OUTPUT
          else
            echo "environment=development" >> $GITHUB_OUTPUT
          fi

  deploy:
    needs: setup
    runs-on: ubuntu-latest
    environment: ${{ needs.setup.outputs.environment }}

    steps:
    - uses: actions/checkout@v4

    - name: Deploy to ${{ needs.setup.outputs.environment }}
      run: |
        echo "Deploying to ${{ needs.setup.outputs.environment }}"
        # 환경별 배포 로직
```

#### 4. Docker 이미지 캐싱

```yaml
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3

    - name: Cache Docker layers
      uses: actions/cache@v4
      with:
        path: /tmp/.buildx-cache
        key: ${{ runner.os }}-buildx-${{ github.sha }}
        restore-keys: |
          ${{ runner.os }}-buildx-

    - name: Build and push
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        tags: ${{ env.ECR_REGISTRY }}/${{ env.ECR_REPOSITORY }}:${{ github.sha }}
        cache-from: type=local,src=/tmp/.buildx-cache
        cache-to: type=local,dest=/tmp/.buildx-cache-new,mode=max
```

### GitLab CI/CD

**.gitlab-ci.yml**
```yaml
stages:
  - test
  - build
  - deploy

variables:
  AWS_REGION: ap-northeast-2
  ECR_REPOSITORY: fastapi-app

test:
  stage: test
  image: python:3.12
  before_script:
    - pip install -r requirements.txt
    - pip install pytest pytest-cov
  script:
    - pytest --cov=app tests/
  coverage: '/TOTAL.*\s+(\d+%)$/'

build:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  before_script:
    - apk add --no-cache python3 py3-pip
    - pip install awscli
    - aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $CI_REGISTRY
  script:
    - docker build -t $ECR_REPOSITORY:$CI_COMMIT_SHA .
    - docker tag $ECR_REPOSITORY:$CI_COMMIT_SHA $CI_REGISTRY/$ECR_REPOSITORY:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY/$ECR_REPOSITORY:$CI_COMMIT_SHA
  only:
    - main

deploy:
  stage: deploy
  image: python:3.12
  before_script:
    - pip install awscli
  script:
    - aws ecs update-service --cluster my-cluster --service fastapi-service --force-new-deployment
  only:
    - main
```

### 배포 전략

#### Blue/Green 배포

```yaml
# CodeDeploy를 사용한 Blue/Green 배포
deploy:
  steps:
    - name: Create CodeDeploy deployment
      run: |
        aws deploy create-deployment \
          --application-name my-app \
          --deployment-group-name my-deployment-group \
          --deployment-config-name CodeDeployDefault.ECSAllAtOnce \
          --description "Deployment from GitHub Actions"
```

#### Canary 배포

```yaml
# App Mesh를 사용한 Canary 배포
- name: Update virtual router
  run: |
    # 10% 트래픽을 신규 버전으로
    aws appmesh update-route \
      --route-name my-route \
      --virtual-router-name my-router \
      --spec '{
        "httpRoute": {
          "action": {
            "weightedTargets": [
              {"virtualNode": "my-app-v1", "weight": 90},
              {"virtualNode": "my-app-v2", "weight": 10}
            ]
          }
        }
      }'
```

---

## 트러블슈팅

### Windows 환경 관련

#### 문제: Docker Desktop이 시작되지 않음
**증상**: "Docker Desktop starting..." 무한 로딩
**해결방법**:
```powershell
# 1. WSL2 업데이트
wsl --update

# 2. WSL2를 기본값으로 설정
wsl --set-default-version 2

# 3. Docker Desktop 재시작
# 작업 관리자에서 Docker Desktop 프로세스 종료 후 재시작
```

#### 문제: 줄바꿈 문제 (CRLF vs LF)
**증상**: 리눅스 컨테이너에서 스크립트 실행 오류
**해결방법**:
```.gitattributes
* text=auto
*.sh text eol=lf
*.py text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
Dockerfile text eol=lf
```

```powershell
# Git 설정 변경
git config --global core.autocrlf input
```

#### 문제: 경로 인식 오류
**증상**: `C:\path\to\file` 같은 Windows 경로가 Docker에서 인식 안됨
**해결방법**:
```yaml
# docker-compose.yml에서
volumes:
  - ./app:/app  # ✅ 상대 경로 사용 (권장)
  - C:/projects/app:/app  # ✅ Windows 경로 (슬래시 사용)
  # ❌ C:\projects\app:/app (백슬래시 사용 금지)
```

### Docker 관련

#### 문제: 이미지 빌드 실패
**증상**: "ERROR [internal] load metadata for docker.io/library/python:3.11"
**해결방법**:
```powershell
# 1. 네트워크 확인
ping docker.io

# 2. Docker 데몬 재시작
# Docker Desktop > Troubleshoot > Restart Docker

# 3. 캐시 무시하고 재빌드
docker build --no-cache -t myapp:latest .

# 4. 빌드 로그 상세 확인
docker build --progress=plain -t myapp:latest .
```

#### 문제: 컨테이너 실행 실패
**증상**: 컨테이너가 즉시 종료됨
**해결방법**:
```powershell
# 로그 확인
docker logs [컨테이너_ID]

# 실시간 로그
docker logs -f [컨테이너_ID]

# 컨테이너 내부 접속하여 디버깅
docker exec -it [컨테이너_ID] /bin/bash

# 또는 sh (Alpine 기반 이미지)
docker exec -it [컨테이너_ID] /bin/sh
```

#### 문제: 이미지 크기 너무 큼
**증상**: 이미지 크기가 1GB 이상
**해결방법**:
```dockerfile
# 1. Slim 베이스 이미지 사용
FROM python:3.11-slim  # ✅ (150MB)
# FROM python:3.11  # ❌ (900MB+)

# 2. Alpine 사용 (더 작음)
FROM python:3.11-alpine  # ✅ (50MB)

# 3. 멀티스테이지 빌드
FROM python:3.11-slim as builder
# ... 빌드 단계 ...

FROM python:3.11-slim
COPY --from=builder /app /app

# 4. 불필요한 파일 제외
.dockerignore에 추가:
__pycache__
*.pyc
.git
.env
node_modules
```

### AWS 관련

#### 문제: AWS CLI 자격증명 오류
**증상**: "Unable to locate credentials"
**해결방법**:
```powershell
# 자격증명 확인
aws sts get-caller-identity

# 출력이 없으면 재설정
aws configure

# 특정 프로파일 사용
aws configure --profile myprofile
export AWS_PROFILE=myprofile  # Linux/Mac
$env:AWS_PROFILE="myprofile"  # PowerShell
```

#### 문제: ECR 로그인 실패
**증상**: "Error response from daemon: Get https://xxx.dkr.ecr.xxx.amazonaws.com/: unauthorized"
**해결방법**:
```powershell
# 1. 리전 확인
$AWS_REGION = "ap-northeast-2"

# 2. 계정 ID 확인
$AWS_ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
Write-Host "Account ID: $AWS_ACCOUNT_ID"

# 3. ECR 로그인 재시도
aws ecr get-login-password --region $AWS_REGION | `
    docker login --username AWS --password-stdin `
    ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com

# 4. Docker credential helper 사용
# ~/.docker/config.json에 추가:
{
  "credsStore": "ecr-login"
}
```

#### 문제: 이미지 푸시 실패
**증상**: "denied: Your authorization token has expired"
**해결방법**:
```powershell
# 1. 토큰 만료 - 재로그인
aws ecr get-login-password --region ap-northeast-2 | `
    docker login --username AWS --password-stdin `
    [AWS_ACCOUNT_ID].dkr.ecr.ap-northeast-2.amazonaws.com

# 2. 리포지토리 존재 확인
aws ecr describe-repositories --region ap-northeast-2

# 3. 리포지토리 없으면 생성
aws ecr create-repository `
    --repository-name myapp `
    --region ap-northeast-2

# 4. 정확한 태그로 푸시
docker tag myapp:latest `
    [AWS_ACCOUNT_ID].dkr.ecr.ap-northeast-2.amazonaws.com/myapp:latest

docker push [AWS_ACCOUNT_ID].dkr.ecr.ap-northeast-2.amazonaws.com/myapp:latest
```

### 네트워킹 관련

#### 문제: 로컬에서 컨테이너 접속 불가
**증상**: `curl localhost:8000` 연결 거부
**해결방법**:
```powershell
# 1. 포트 매핑 확인
docker ps
# PORTS 컬럼에 0.0.0.0:8000->8000/tcp 확인

# 2. 컨테이너 로그 확인
docker logs [컨테이너_ID]

# 3. 127.0.0.1 시도
curl http://127.0.0.1:8000

# 4. 방화벽 확인
# Windows Defender 방화벽 > 인바운드 규칙
# Docker Desktop 허용 확인

# 5. 포트 사용 중인지 확인
netstat -ano | findstr :8000
```

#### 문제: 컨테이너 간 통신 실패
**증상**: "Connection refused" 에러
**해결방법**:
```yaml
# docker-compose.yml
networks:
  app-network:
    driver: bridge

services:
  web:
    networks:
      - app-network
    environment:
      - DB_HOST=db  # ✅ 서비스 이름 사용
      # ❌ DB_HOST=localhost
  
  db:
    networks:
      - app-network
```

---

## FAQ

자주 묻는 질문과 답변을 모았습니다.

### 일반 질문

#### Q: Docker Desktop 없이 진행할 수 있나요?
**A**: 네, WSL2에서 Docker Engine만 설치하거나, 클라우드 빌드 서비스(AWS CodeBuild, GitHub Actions)를 사용할 수 있습니다. 하지만 로컬 개발을 위해서는 Docker Desktop이 가장 편리합니다.

#### Q: Mac이나 Linux에서도 이 가이드를 따라할 수 있나요?
**A**: 네, PowerShell 명령어를 Bash로 변경하고 경로 구분자를 조정하면 대부분의 내용이 동일하게 적용됩니다. Docker와 AWS CLI 사용법은 동일합니다.

#### Q: AWS 비용이 걱정됩니다. 무료로 테스트할 수 있나요?
**A**: AWS 프리티어를 활용하면 다음을 무료로 사용할 수 있습니다:
- ECR: 500MB 스토리지/월
- ECS Fargate: 월간 무료 사용량 있음 (처음 1개월)
- App Runner: 프리티어 없음 (최소 비용 발생)
- 테스트 후 리소스를 즉시 삭제하면 비용을 최소화할 수 있습니다.

#### Q: 어떤 배포 옵션을 선택해야 하나요?
**A**:
- **처음 시작** → App Runner (가장 간단)
- **프로덕션, 중소규모** → ECS Fargate (균형)
- **대규모, 복잡한 시스템** → EKS (유연성)
- **예산 제한** → ECS Fargate (가장 저렴)

### Docker 관련

#### Q: 이미지 빌드가 너무 느려요. 어떻게 해야 하나요?
**A**:
1. `.dockerignore` 파일을 작성하여 불필요한 파일 제외
2. 멀티스테이지 빌드 사용
3. Docker BuildKit 활성화: `$env:DOCKER_BUILDKIT=1`
4. 레이어 캐싱 최적화 (자주 변경되는 파일을 나중에 COPY)

#### Q: 컨테이너가 계속 재시작됩니다. 원인이 무엇인가요?
**A**:
```powershell
# 1. 로그 확인
docker logs [컨테이너_ID]

# 2. 일반적인 원인:
# - 애플리케이션 크래시 (코드 에러)
# - 메모리 부족 (OOM Killer)
# - Health check 실패
# - 잘못된 CMD/ENTRYPOINT

# 3. 메모리 제한 늘리기
docker run -m 2g myapp:latest
```

#### Q: Windows와 Linux 컨테이너의 차이는 무엇인가요?
**A**: 이 가이드는 Linux 컨테이너를 다룹니다. AWS도 Linux 컨테이너를 주로 지원합니다. Docker Desktop에서 Linux 컨테이너 모드를 사용하고 있는지 확인하세요 (기본값).

### AWS 관련

#### Q: ECR에 이미지가 푸시되지 않습니다. 왜 그런가요?
**A**:
```powershell
# 1. ECR 로그인 토큰은 12시간 후 만료됩니다. 재로그인하세요:
aws ecr get-login-password --region ap-northeast-2 | `
    docker login --username AWS --password-stdin [계정ID].dkr.ecr.ap-northeast-2.amazonaws.com

# 2. 이미지 태그 확인:
docker images  # ECR URI와 정확히 일치하는지 확인

# 3. IAM 권한 확인:
aws sts get-caller-identity  # 계정 확인
# ECR 권한: ecr:GetAuthorizationToken, ecr:PutImage 등
```

#### Q: ECS 태스크가 시작되지 않습니다. 어떻게 디버깅하나요?
**A**:
```powershell
# 1. 태스크 이벤트 확인
aws ecs describe-tasks --cluster my-cluster --tasks [task-id]

# 2. 일반적인 문제:
# - ECR 이미지 pull 실패 → IAM 역할 확인
# - 메모리/CPU 부족 → Task Definition 수정
# - Health check 실패 → Health check 설정 검토
# - 잘못된 환경 변수 → Secrets Manager 값 확인

# 3. CloudWatch Logs 확인
aws logs tail /ecs/my-app --follow
```

#### Q: RDS 연결이 안 됩니다. 보안 그룹 설정은 어떻게 하나요?
**A**:
```powershell
# 1. RDS 보안 그룹 인바운드 규칙:
# Type: PostgreSQL (5432)
# Source: ECS 태스크의 보안 그룹 ID

# 2. ECS와 RDS가 같은 VPC에 있는지 확인

# 3. RDS 엔드포인트가 올바른지 확인
aws rds describe-db-instances --db-instance-identifier myapp-db
```

### 성능 관련

#### Q: 애플리케이션 응답이 느립니다. 어떻게 개선하나요?
**A**:
1. **Worker 수 증가**: Gunicorn workers 설정
2. **캐싱 추가**: Redis, in-memory cache
3. **DB 쿼리 최적화**: N+1 문제 해결, 인덱스 추가
4. **비동기 처리**: async/await 활용
5. **Connection Pooling**: 데이터베이스 연결 풀 설정
6. **CDN 사용**: 정적 파일은 CloudFront로

#### Q: Docker 이미지 크기가 너무 큽니다. 어떻게 줄이나요?
**A**:
```dockerfile
# 1. slim 또는 alpine 베이스 이미지 사용
FROM python:3.12-slim  # 900MB → 150MB

# 2. 멀티스테이지 빌드
FROM python:3.12-slim as builder
# ... 빌드 ...
FROM python:3.12-slim
COPY --from=builder ...

# 3. 불필요한 파일 제외
# .dockerignore 파일 작성

# 4. 레이어 수 줄이기
RUN apt-get update && apt-get install -y pkg1 pkg2 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
```

### 배포 관련

#### Q: 배포 중 다운타임이 발생합니다. 무중단 배포가 가능한가요?
**A**: 네, 다음 방법을 사용하세요:
- **App Runner**: 자동 롤링 배포
- **ECS**: Rolling update 설정 (minimumHealthyPercent: 100)
- **ECS + ALB**: Blue/Green 배포
- **EKS**: Rolling update 또는 Canary 배포

#### Q: 배포한 버전에 문제가 있습니다. 어떻게 롤백하나요?
**A**:
```powershell
# ECS Fargate 롤백
aws ecs update-service \
    --cluster my-cluster \
    --service my-service \
    --task-definition my-task:2  # 이전 버전

# App Runner 롤백
aws apprunner start-deployment \
    --service-arn [ARN]  # 자동으로 이전 버전으로 롤백

# 또는 이전 이미지로 재배포
docker push [ECR_URI]:v1.0.0
```

#### Q: CI/CD 파이프라인에서 테스트가 실패합니다. 어떻게 해야 하나요?
**A**:
```yaml
# 로컬에서 먼저 테스트
pytest tests/ -v

# GitHub Actions에서 디버깅
- name: Run tests with debug
  run: |
    pytest tests/ -v --log-cli-level=DEBUG

# 테스트 환경 변수 설정
env:
  DATABASE_URL: sqlite:///test.db
  DEBUG: true
```

### 환경 변수 및 시크릿

#### Q: 환경 변수와 Secrets Manager, 언제 무엇을 사용하나요?
**A**:
- **환경 변수** (environment): 비밀이 아닌 설정 (ENV, DEBUG, AWS_REGION)
- **Secrets Manager** (secrets): 비밀 정보 (DATABASE_URL, API_KEY, 비밀번호)

#### Q: 로컬 .env 파일을 실수로 커밋했습니다. 어떻게 하나요?
**A**:
```powershell
# 1. Git 히스토리에서 제거
git filter-branch --force --index-filter \
    "git rm --cached --ignore-unmatch .env" \
    --prune-empty --tag-name-filter cat -- --all

# 2. 또는 BFG Repo-Cleaner 사용 (더 빠름)
bfg --delete-files .env

# 3. .gitignore에 추가
echo ".env" >> .gitignore

# 4. 비밀 정보 교체 (DB 비밀번호, API 키 등)
```

### 비용 관련

#### Q: 예상치 못한 AWS 비용이 발생했습니다. 어떻게 확인하나요?
**A**:
```powershell
# 1. Cost Explorer에서 비용 확인
# AWS Console → Cost Explorer

# 2. 주요 비용 발생 리소스:
# - ECS/EKS 태스크 실행 시간
# - NAT Gateway (시간당 + 데이터 전송량)
# - Load Balancer (시간당)
# - ECR 스토리지 (GB당)
# - RDS 인스턴스

# 3. 사용하지 않는 리소스 정리:
aws ecs list-services --cluster my-cluster
aws rds describe-db-instances
aws ec2 describe-nat-gateways
```

#### Q: 개발 환경 비용을 절감하려면 어떻게 해야 하나요?
**A**:
1. **야간/주말 중지**: Lambda로 스케줄링
2. **Spot Instances**: EC2 모드에서 70% 절감
3. **리소스 최소화**: 최소 vCPU/메모리로 시작
4. **로컬 개발**: Docker Compose 활용
5. **오토 스케일링**: 트래픽에 따라 자동 조절

### 데이터베이스

#### Q: 프로덕션에서 데이터베이스 마이그레이션을 어떻게 안전하게 실행하나요?
**A**:
```python
# 1. 백업 먼저 수행
aws rds create-db-snapshot \
    --db-instance-identifier myapp-db \
    --db-snapshot-identifier myapp-db-backup-$(date +%Y%m%d)

# 2. Blue/Green 배포 사용
# - 마이그레이션 스크립트를 별도 태스크로 실행
# - 실패 시 자동 롤백

# 3. Alembic 마이그레이션은 init 컨테이너로
# ECS에서는 별도 태스크 정의

# 4. 스키마 변경은 점진적으로
# - 컬럼 추가 → 배포 → 컬럼 사용 → 배포 → 기존 컬럼 제거
```

#### Q: 로컬 DB와 AWS RDS를 어떻게 동기화하나요?
**A**:
```powershell
# 1. RDS에서 덤프 생성
pg_dump -h myapp-db.xxxxx.rds.amazonaws.com -U admin -d mydb > backup.sql

# 2. 로컬에 복원
psql -U postgres -d local_db < backup.sql

# 3. 또는 Docker Compose로 로컬 DB 초기화
docker-compose down -v  # 볼륨 삭제
docker-compose up -d
```

---

## 다음 단계

### FastAPI 애플리케이션 배포
1. ✅ [Windows 환경 설정](./fastapi-aws/0-windows-setup/README.md)
2. ✅ [로컬에서 Docker 이미지 빌드](#fastapi-가이드)
3. 배포 방식 선택:
   - [App Runner로 배포](./fastapi-aws/deployments/1-app-runner/README.md)
   - [ECS Fargate로 배포](./fastapi-aws/deployments/2-ecs-fargate/README.md)
   - [EKS로 배포](./fastapi-aws/deployments/3-eks/README.md)

### Django 애플리케이션 배포
1. ✅ [Django 프로젝트 구조](#django-가이드)
2. ✅ [로컬에서 Docker 이미지 빌드](#django-가이드)
3. 배포 방식 선택:
   - [App Runner로 배포](./django-aws/deployments/1-app-runner/README.md)
   - [ECS Fargate로 배포](./django-aws/deployments/2-ecs-fargate/README.md)
   - [EKS로 배포](./django-aws/deployments/3-eks/README.md)

---

## 비용 예상

### App Runner 💰
```
vCPU: $0.064/vCPU-시간
메모리: $0.007/GB-시간

예상 월 비용 (1 vCPU, 2GB, 24시간):
= (1 × $0.064 + 2 × $0.007) × 24 × 30
= $57.6/월
```

### ECS Fargate 💰💰
```
vCPU: $0.04656/vCPU-시간
메모리: $0.00511/GB-시간

예상 월 비용 (0.5 vCPU, 1GB, 24시간):
= (0.5 × $0.04656 + 1 × $0.00511) × 24 × 30
= $20.52/월

예상 월 비용 (1 vCPU, 2GB, 24시간):
= (1 × $0.04656 + 2 × $0.00511) × 24 × 30
= $40.98/월
```

### EKS 💰💰💰
```
클러스터: $0.10/시간 = $73/월
워커 노드 (t3.medium × 2): $0.0416/시간 × 2 = $60/월

총 예상 비용: $133/월
```

### 💡 비용 절감 팁

1. **개발/테스트 환경**
   - App Runner 사용 (간단, 저렴)
   - 야간/주말에는 서비스 중지
   - 최소 리소스로 시작

2. **프로덕션 환경**
   - ECS Fargate 사용 (안정적, 합리적 비용)
   - Auto Scaling 설정 (트래픽 기반)
   - Spot Instances 고려 (EC2 모드)

3. **엔터프라이즈 환경**
   - EKS 사용 (대규모 서비스)
   - Reserved Instances 구매 (70% 할인)
   - Savings Plans 활용

---

## 참고 자료

### 공식 문서
- [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)
- [AWS CLI v2 설치 가이드](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-windows.html)
- [AWS App Runner 문서](https://docs.aws.amazon.com/apprunner/)
- [AWS ECS 문서](https://docs.aws.amazon.com/ecs/)
- [AWS EKS 문서](https://docs.aws.amazon.com/eks/)
- [AWS ECR 문서](https://docs.aws.amazon.com/ecr/)

### 프레임워크 문서
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Django 공식 문서](https://docs.djangoproject.com/)
- [Uvicorn 문서](https://www.uvicorn.org/)
- [Gunicorn 문서](https://docs.gunicorn.org/)

### Docker 관련
- [Docker 공식 문서](https://docs.docker.com/)
- [Docker Compose 문서](https://docs.docker.com/compose/)
- [Dockerfile 베스트 프랙티스](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [멀티스테이지 빌드](https://docs.docker.com/build/building/multi-stage/)

### Kubernetes (EKS용)
- [Kubernetes 공식 문서](https://kubernetes.io/docs/)
- [eksctl 문서](https://eksctl.io/)
- [Helm 문서](https://helm.sh/docs/)

---

## 기여 및 피드백

이 가이드에 대한 피드백이나 개선 제안은 언제든 환영합니다!

### 버그 리포트
- GitHub Issues를 통해 문제 보고
- 재현 가능한 예제 코드 첨부
- 환경 정보 (Windows 버전, Docker 버전 등) 포함

### 개선 제안
- Pull Request를 통해 개선 사항 제안
- 새로운 예제 추가
- 문서 오타 수정

---

## 라이선스

이 가이드는 교육 목적으로 제공되며, 자유롭게 사용하고 수정할 수 있습니다.
