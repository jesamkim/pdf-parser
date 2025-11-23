# PDF to Markdown Converter

AWS Bedrock Claude 기반 PDF → Markdown 변환기

## 기능

- **PDF를 이미지로 변환**: 각 페이지를 고해상도 이미지로 변환 (450 DPI)
- **OCR 변환**: AWS Bedrock Claude Sonnet 4.5를 사용해 이미지에서 텍스트 추출
- **이미지 추출**: PDF 내 임베디드 이미지 자동 추출 및 저장
- **구조 보존**: 테이블, 목록, 제목 등 문서 구조를 Markdown으로 정확히 변환
- **스트리밍 처리**: 페이지별 처리로 메모리 효율적 대용량 PDF 처리
- **재시도 로직**: 실패한 페이지 자동 재처리

## 시스템 요구사항

### Python 패키지
```bash
pip install -r requirements.txt
```

### 시스템 패키지 (pdf2image 의존성)
**Ubuntu/Debian:**
```bash
sudo apt-get install poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Windows:**
- Poppler을 다운로드하고 PATH에 추가: https://github.com/oschwartz10612/poppler-windows/releases/

### AWS 설정
1. AWS CLI 설치 및 설정:
```bash
aws configure --profile your-profile
```

2. Bedrock 모델 액세스 권한 필요:
   - Claude Sonnet 4.5 (`global.anthropic.claude-sonnet-4-5-20250929-v1:0`)
   - Claude Haiku 4.5 (`global.anthropic.claude-haiku-4-5-20251001-v1:0`)

## 사용법

### 기본 사용법
```bash
cd pdf-converter
python src/pdf_to_markdown.py path/to/document.pdf
```

결과: `output/document.md` 생성

### 출력 경로 지정
```bash
python src/pdf_to_markdown.py path/to/document.pdf -o custom_output.md
```

### 특정 페이지만 변환
```bash
# 10-20 페이지만 변환
python src/pdf_to_markdown.py document.pdf --first-page 10 --last-page 20
```

### 모델 선택
```bash
# Haiku 모델 사용 (빠르고 저렴)
python src/pdf_to_markdown.py document.pdf --model haiku

# Sonnet 모델 사용 (더 정확, 기본값)
python src/pdf_to_markdown.py document.pdf --model sonnet
```

### DPI 설정
```bash
# 고해상도 변환 (더 정확하지만 느림)
python src/pdf_to_markdown.py document.pdf --dpi 600
```

### AWS 설정 변경
```bash
python src/pdf_to_markdown.py document.pdf --profile my-profile --region us-east-1
```

## 설정 커스터마이징

`src/config.py` 파일에서 다음을 변경할 수 있습니다:

```python
# AWS 설정
AWS_PROFILE = "profile2"
AWS_REGION = "us-west-2"

# PDF 처리 설정
PDF_DPI = 450  # 이미지 해상도 (높을수록 정확하지만 느림)

# 이미지 추출 설정
SAVE_PAGE_IMAGES = True  # 전체 페이지 이미지 저장
EXTRACT_EMBEDDED_IMAGES = True  # PDF 내 이미지 추출
MIN_IMAGE_WIDTH = 100  # 최소 이미지 크기 (작은 아이콘 필터링)
MIN_IMAGE_HEIGHT = 100

# API 설정
MAX_TOKENS = 8192  # Claude 응답 최대 토큰
TEMPERATURE = 0.05  # 낮을수록 일관된 결과
```

## 출력 구조

```
output/
├── document.md                        # Markdown 결과
├── document_images/                   # 이미지 디렉토리 (옵션)
│   ├── page_001.png                  # 전체 페이지 이미지
│   ├── page_001_img_001.png          # 추출된 이미지
│   └── ...
├── document_images_metadata.json      # 이미지 메타데이터 (옵션)
└── document_failed_pages.json         # 실패한 페이지 목록 (오류 발생 시)
```

## 주요 기능 설명

### 1. 스트리밍 처리
대용량 PDF 처리를 위해 페이지별로 처리하고 즉시 파일에 기록:
- 메모리 효율적
- 중간 결과 저장
- 진행 상황 실시간 확인

### 2. 재시도 로직
네트워크 오류나 일시적 API 오류 시 자동 재시도:
- 최대 3회 재시도
- 지수 백오프 (2초, 4초, 8초)
- 실패한 페이지는 오류 메시지와 함께 기록

### 3. 이미지 처리
- **전체 페이지 이미지**: 각 페이지를 PNG로 저장
- **임베디드 이미지**: PDF 내 이미지 추출 및 메타데이터 기록
- **이미지 참조**: Markdown에서 `![title](IMAGE_PLACEHOLDER)` 자동 변환

### 4. 정확한 OCR
Claude의 비전 모델을 사용해:
- 테이블 구조 보존
- 다국어 지원 (한글, 영어, 일본어, 중국어 등)
- 병합된 셀 처리
- 시각적으로 유사한 문자 구분 (예: 교/고, 율/률)

## Python 코드에서 사용

```python
from src.pdf_to_markdown import PDFToMarkdownConverter

# 변환기 초기화
converter = PDFToMarkdownConverter(
    profile_name="your-profile",
    region_name="us-west-2",
    model_id="global.anthropic.claude-sonnet-4-5-20250929-v1:0"
)

# PDF 변환
result = converter.convert_pdf_to_markdown(
    pdf_path="document.pdf",
    output_path="output/document.md",
    dpi=450,
    first_page=1,
    last_page=10
)

print(result)  # "Conversion completed: 10/10 pages successful (100.0%)"
```

## 문제 해결

### 1. Poppler 설치 오류
```
PDFInfoNotInstalledError: Unable to get page count. Is poppler installed and in PATH?
```
**해결**: 시스템에 맞는 Poppler 설치 (위 "시스템 요구사항" 참조)

### 2. AWS 인증 오류
```
NoCredentialsError: Unable to locate credentials
```
**해결**: AWS CLI 설정 확인
```bash
aws configure --profile your-profile
```

### 3. Bedrock 모델 액세스 오류
```
AccessDeniedException: Could not access model
```
**해결**: AWS Console에서 Bedrock 모델 액세스 요청

### 4. 메모리 부족
큰 PDF 처리 시 메모리 부족:
- DPI를 낮춤 (예: 300)
- 페이지 범위를 나눠서 처리
- `SAVE_PAGE_IMAGES = False`로 설정

## 비용 예상

AWS Bedrock Claude Sonnet 4.5 기준:
- 입력: $3.00 / 1M 토큰
- 출력: $15.00 / 1M 토큰

450 DPI, 100페이지 문서 기준 예상 비용:
- 페이지당 약 $0.05-0.10
- 100페이지: $5-10

비용 절감 팁:
- Haiku 모델 사용 (약 5배 저렴)
- DPI 낮춤 (300으로 설정 시 약 40% 비용 절감)

## 라이선스

이 코드는 Samsung C&T ESG 프로젝트에서 추출되었습니다.

## 기술 스택

- **Amazon Bedrock**: Claude Sonnet 4.5 / Haiku 4.5 비전 모델
- **pdf2image**: PDF → 이미지 변환
- **PyMuPDF**: PDF 이미지 추출
- **Pillow**: 이미지 처리
- **boto3**: AWS SDK
