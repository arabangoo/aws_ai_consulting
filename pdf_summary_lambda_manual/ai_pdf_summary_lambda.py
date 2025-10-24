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

