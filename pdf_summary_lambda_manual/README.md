## [Lambda에서 Bedrock AI 모델을 호출하여 PDF 요약]

(1) 일단 아래와 같이 파이썬 런타임 기반으로 Lambda 함수를 작성하자.   
여기서는 Python 3.10 버전을 사용하겠다.      
추가로 AdministratorAccess 권한을 가진 임시 역할을 생성해서 할당한다.      
![그림1](https://github.com/user-attachments/assets/46efabb9-f2eb-46c2-8bfc-644b60c624d2)
<br/>
                
(2) 함수가 생성되면 메모리와 임시 스토리지 용량을 늘려주고 제한 시간도 15분으로 설정해준다.   
AI/ML을 위한 Lambda 함수는 메모리, 임시 스토리지, 제한 시간을 여유롭게 설정해줘야 한다.          
![그림2](https://github.com/user-attachments/assets/d6b050f6-d3cc-40e6-835c-01972a4d7d8d)
<br/>
        
(3) 다음은 코드와 연동될 환경 변수를 설정해줘야 한다.    
이번 테스트의 람다 함수 코드와 연동되는 환경 변수는 아래와 같다.   
일단 베드락에서 AI 모델이 사용 허가 상태여야 한다.    
![image3](https://github.com/user-attachments/assets/66caf17b-ddf5-4dc6-a1d3-c8b6936bfcec)
<br/>
                                
(4) 이제 람다 함수에 zip 파일을 업로드하는 방식으로 코드를 등록하면 된다.   
다만, 이 zip 파일의 경우 amazon linux에서 도커를 통해 패키징을 해줘야 한다.   
이런 사전 절차를 거쳐서 zip 파일을 패키징 해줘야 코드가 에러나지 않는다.   
![image4](https://github.com/user-attachments/assets/779f079f-ab63-47e9-861b-12165be5afc7)
<br/>

(5) 파일질라 등의 FTP 클라이언트 프로그램을 통해 ai_pdf_summary_lambda.py 파이썬 코드 파일을 서버로 복사해준다.   
해당 파일은 amazon linux 서버의 /home/ec2-user 경로로 복사하면 된다.   

```python           
import boto3
import json
import pdfplumber
from io import BytesIO
import os

# S3 및 Bedrock 클라이언트 생성
s3 = boto3.client('s3')
bedrock_runtime = boto3.client(service_name='bedrock-runtime')

# 환경 변수에서 S3 버킷, 폴더, Bedrock 모델 정보 가져오기
bucket_name = os.getenv('BUCKET_NAME')  # 예: 'ai-pdf-test-bucket'
folder_name = os.getenv('FOLDER_NAME')  # 예: 'ai-pdf-folder/'
model_id = os.getenv('MODEL_ID')  # 예: 'anthropic.claude-3-5-sonnet-20240620-v1:0'

def invoke_bedrock(query, model_id, max_tokens=8192, temperature=0.7, top_p=0.9, top_k=250):
    # Bedrock 모델 호출 요청 데이터 생성
    request_data = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "messages": [{"role": "user", "content": [{"type": "text", "text": query}]}],
    }
    # 요청을 JSON 형태로 변환
    request_body = json.dumps(request_data)

    # Bedrock 모델 호출
    response = bedrock_runtime.invoke_model(
        body=request_body,
        modelId=model_id,
        contentType="application/json",
        accept="application/json"
    )

    # 응답 처리
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']

def get_all_texts_from_pdf(file_content):
    # PDF 파일에서 텍스트 추출
    with pdfplumber.open(BytesIO(file_content)) as pdf:
        return "".join([page.extract_text() for page in pdf.pages])

def lambda_handler(event, context):
    # S3 이벤트에서 업로드된 파일 정보 가져오기
    for record in event['Records']:
        s3_object = record['s3']['object']['key']
        # PDF 파일만 처리
        if s3_object.endswith('.pdf'):
            try:
                # S3에서 PDF 파일 다운로드
                file_obj = s3.get_object(Bucket=bucket_name, Key=s3_object)
                file_content = file_obj['Body'].read()

                # PDF 텍스트 추출
                pdf_text = get_all_texts_from_pdf(file_content)

                # Bedrock 모델에 보낼 프롬프트 생성
                prompt = f"다음 PDF 문서의 내용을 요약하세요: {pdf_text[:30000]}"
                
                # Bedrock 모델을 사용하여 요약 생성
                summary = invoke_bedrock(prompt, model_id)

                # 요약 파일 이름 생성 및 S3에 저장
                summary_file_name = s3_object.replace('.pdf', '_summary.txt')
                s3.put_object(
                    Bucket=bucket_name,
                    Key=f"{folder_name}summaries/{summary_file_name}",
                    Body=summary.encode('utf-8')
                )
                print(f"요약 파일 저장 완료: {summary_file_name}")

            except Exception as e:
                # 오류 발생 시 로그 저장
                print(f"파일 {s3_object} 처리 중 오류 발생: {str(e)}")
                error_log = f"파일: {s3_object}\n오류: {str(e)}\n"
                s3.put_object(
                    Bucket=bucket_name,
                    Key=f"{folder_name}error_logs/{s3_object}_error.log",
                    Body=error_log.encode('utf-8')
                )
```
<br/>

(6) 다음은 putty 등을 통해 서버에 접속하여 도커 환경을 구성해준다.     
아래 순서대로 명령어를 실행하여 서버에 도커 환경을 구성하고 zip 파일 패키징을 한다.    

1.  새로운 Amazon Linux 2 컨테이너 실행      
- docker run -it --rm amazonlinux:2 bash          

2. 필요한 개발 도구 및 라이브러리 설치 (SSL 관련 패키지 추가)          
- yum update -y         
- yum groupinstall -y "Development Tools"          
- yum install -y bzip2-devel libffi-devel wget openssl11 openssl11-devel sqlite-devel          

3. Python 3.10 소스코드 다운로드 및 설치       
- cd /opt       
- wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz       
- tar xzf Python-3.10.13.tgz       
- cd Python-3.10.13       

4. SSL 지원을 포함하여 configure (중요: LDFLAGS와 CPPFLAGS 추가)       
- export LDFLAGS="-Wl,-rpath=/usr/local/lib"       
- export CPPFLAGS="-I/usr/include/openssl11"       
- ./configure --enable-optimizations --with-openssl11       
- make altinstall       

5. 불필요한 파일 정리       
- cd /opt       
- rm -f Python-3.10.13.tgz       

6. 심볼릭 링크 생성        
- ln -sf /usr/local/bin/python3.10 /usr/local/bin/python3       
- ln -sf /usr/local/bin/pip3.10 /usr/local/bin/pip3       

7. 버전 확인       
- python3.10 --version       
- pip3.10 --version       

8. pip 업그레이드        
- python3.10 -m pip install --upgrade pip       

9. Lambda 패키지 생성       
Lambda 함수에 필요한 라이브러리를 /lambda-package 디렉토리에 설치한다.       
- mkdir /lambda-package       
- python3.10 -m pip install pdfplumber -t /lambda-package       
컨테이너 안에서 필수 라이브러리 설치가 완료되면 ssh 터미널창 하나를 더 띄워서 서버에 접속한다.         
즉, 지금부터는 ssh 터미널창 2개로 서버 작업을 하는 것이다.       
일단 새로운 터미널창에서 /home/ec2-user 경로로 들어간 후 아래 절차대로 진행한다.       

10. Lambda 코드 복사       
호스트 시스템에서 Lambda 함수 파일을 컨테이너로 복사한다.       
- docker ps  # 실행 중인 컨테이너 ID 확인       
- docker cp ai_pdf_summary_lambda.py <컨테이너 ID>:/lambda-package/       

11. 다시 기존 ssh 터미널창으로 잠깐 돌아와 zip 파일 패키징을 시작한다.       
- cd /lambda-package       
- zip -r9 /tmp/ai_pdf_summary_lambda.zip .       

12. 이번에는 새롭게 연 ssh 터미널창에서 zip 파일 복사 작업을 한다.       
- docker cp <컨테이너 ID>:/tmp/ai_pdf_summary_lambda.zip .        
<br/>

(7) 다시 파일질라 등의 FTP 클라이언트 프로그램을 통해 로컬 PC로 zip 파일을 복사한다.   
그 다음 Lambda 함수에 zip파일을 업로드해서 코드를 등록한다.   
![그림3](https://github.com/user-attachments/assets/7e710e83-5612-4db4-b848-aad5e55bae79)
<br/>
   
(8) 핸들러 이름을 변경해야 코드가 정상 작동한다.   
일단 본 테스트에서는 "ai_pdf_summary_lambda.lambda_handler"라고 이름을 변경한다.   
런타임 설정에서 파이썬 버전도 변경할 수 있으니    
추후 다른 파이썬 버전으로 코드를 다시 패키징해서 올리는 경우 런타임 설정에서 파이썬 버전도 변경해준다.   
![그림4](https://github.com/user-attachments/assets/fb27e0a9-c557-40b3-a9fe-9493ba21393a)
<br/>
    
(9) 이제 테스트 json 코드를 작성해보자.   
Lambda 함수 테스트 항목에 들어가서 아래와 같이 코드를 작성한 후 테스트를 실행한다.   
PDF 파일 이름은 본인이 가지고 있는 PDF 파일 이름으로 바꾼다.   

```
{
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "2024-09-25T12:00:00.000Z",
      "eventName": "ObjectCreated:Put",
      "s3": {
        "s3SchemaVersion": "1.0",
        "bucket": {
          "name": "ai-pdf-test-bucket",
          "arn": "arn:aws:s3:::ai-pdf-test-bucket"
        },
        "object": {
          "key": "ai-pdf-folder/231215_reCap 2023_AIML_v2.pdf"
        }
      }
    }
  ]
}
```
<br/>

![image8](https://github.com/user-attachments/assets/8c62d1b2-e88d-42b0-8ac0-89b59a770c06)
<br/>
          
(10) 테스트를 실행할 때마다 아래와 같이 별도의 summay 버킷과 파일이 만들어지면 성공이다.       
![image9](https://github.com/user-attachments/assets/044e72b3-7e0e-4a44-a42b-25b37775c4ca)
<br/>

---
<br/>

이번에는 PDF 업로드시 자동 PDF 요약을 진행해보겠다.   
Lambda 함수에 S3 트리거를 추가하면 S3 버킷 폴더에 PDF 업로드시 Lambda가 실행되어 PDF 자동 요약을 해준다.   
<br/>
(1) Lambda 함수 아래 있는 트리거 추가 버튼을 클릭하고 S3를 소스로 지정한 다음 이미지와 같이 설정한다.   
접두사의 경우 S3 버킷의 폴더 이름을 기입하면 되고 접미사의 경우 S3에 업로드하는 파일의 형식을 기입하면 된다.   
![image10](https://github.com/user-attachments/assets/21898c4c-840b-4a7d-bbf6-0839a22f02d9)
<br/>

(2) 아래와 같이 Lambda 함수와 S3 트리거가 연결되면    
이제 지정한 S3 버킷 폴더에 PDF 파일이 업로드될 때마다 Lambda 함수가 실행되어 내용을 요약한다.   
![image11](https://github.com/user-attachments/assets/80e46f06-6ffb-4c84-9913-c77a562997d2)
<br/>

(3) 논문 요약 테스트를 위해 arXiv 등의 논문 사이트에서 논문 PDF를 다운로드해서 테스트 해보자.    
PDF 파일 요약 속도를 확인하며 너무 성능이 떨어지지 않게 Lambda 사양을 조절해주면 된다.   
![image12](https://github.com/user-attachments/assets/1d63f609-b9a5-4fdc-85ad-93628d5208cd)
