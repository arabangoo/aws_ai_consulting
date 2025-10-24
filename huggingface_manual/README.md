![image1](https://github.com/user-attachments/assets/1068e438-ffca-4444-aad5-cb4df8c7d301)

Hugging Face(허깅페이스)란 자연어 처리, 이미지 생성모델, 컴퓨터 비전모델 등 다양한 도구와 라이브러리를 제공하는 곳이다.   
쉽게 말해서 다양한 인공지능 모델들을 오픈 소스로 제공하는 곳이라고 생각하면 된다.   
또한 간단한 파이썬 지식이 있다면 학습 모델들을 쉽게 사용해볼 수 있는 곳이라고도 할 수 있다.   
허깅페이스는 트랜스포머 기반의 다양한 모델들과 학습 스크립트를 구현해놓았다.   
기존의 트랜스포머를 학습시킨다고 하면 딥러닝 프레임워크를 선택하고 그에 맞게 구현을 해야했다.    
하지만 허깅페이스는 그런 함수들이 이미 정의 되어있기 때문에 간단하게 모델을 불러서 쓸 수 있다.    
즉, 따로 구현을 하지 않고 arguments를 줌으로써 편하게 사용이 가능하다.     
<br/><br/>     

1. 허깅페이스 가입하기
<br/>     
(1) 우선 허깅페이스 사이트에 들어가서 계정을 만들도록 하자.
<br/>

https://huggingface.co/
![image2](https://github.com/user-attachments/assets/f3de8983-4f31-41e0-8a14-4f9326d6d1d4)
<br/>
        
(2) 허깅페이스 계정을 만든 후 사이트 상단에 보이는 이메일 인증을 해준다.   
"Resend confirmation email" 버튼을 클릭할 필요는 없고 가입시 등록한 이메일의 메일함을 보면 된다.   
또한 Welcome 페이지에 나오는 리포지토리 생성 작업 역시 아직 할 필요없다.    
![image3](https://github.com/user-attachments/assets/4927a3f3-b792-4b5b-8a41-172fff8eaaff)
<br/>
        
(3) 이메일 인증까지 완료하면 아래와 같은 첫 메인 페이지를 볼 수 있다.
![image4](https://github.com/user-attachments/assets/bccf7ae0-5ed1-4c2b-9293-47253c36b2b6)
<br/>

(4) 상단의 "Models" 항목을 클릭하면 허깅페이스를 통해 사용 가능한 AI 모델을 볼 수가 있다.   
가능한 경우 Hosted inference API를 활용해서 모델을 사용해 볼 수 있다.   
![image5](https://github.com/user-attachments/assets/48c93d45-d700-4ec5-b61a-6f5ed8120a65)
<br/>

(5) 상단의 "Datasets" 항목을 클릭하면 허깅페이스를 통해 사용 가능한 데이터셋을 볼 수가 있다.   
머신러닝에 활용할 수 있는 데이터셋을 확인할 수 있다.    
위키, 뉴스, 웹 데이터 등 다양한 데이터들을 사람들이 올린다.      
![image6](https://github.com/user-attachments/assets/2de5c12f-2104-489d-abd3-a17edc7fef6d)
<br/>

(6) 상단의 "Spaces" 항목을 클릭하면 커뮤니티에 의해 개발된 다양한 머신러닝 앱을 사용해 볼 수 있다.
![image7](https://github.com/user-attachments/assets/c27a86ea-7a29-4bb0-a706-bcb0030338d8)
<br/>

(7) Post는 유저들이 글을 작성하고 게시할 수 있는 공간이다.
![image8](https://github.com/user-attachments/assets/44d2fba1-e449-4e9f-9589-c2470e0f6b3e)
<br/>

(8) Docs는 항목별로 API 레퍼런스, 가이드 등이 카테고리별로 정리되어 있다. 
![image9](https://github.com/user-attachments/assets/34c2d1e3-03c8-46db-a746-d9c3cd058dc5)
<br/>

(9) 마지막으로 "HuggingChat"에 대해 알아보도록 하겠다.   
맨 우측 상단의 세 줄 아이콘을 클릭하고 "HuggingChat"을 선택한다.   
![image10](https://github.com/user-attachments/assets/09e6891a-5a88-49a0-a897-3637aa65de69)
<br/>

(10) 그러면 ChatGPT나 Claude 등에서 볼 수 있는 채팅창이 열리고 AI와 대화할 수 있다.
![image11](https://github.com/user-attachments/assets/d22d6385-f4bf-46e4-aeb1-8242b75567e1)
![image12](https://github.com/user-attachments/assets/e69be82d-9be1-4e5e-b674-7de11c5c4e32)
<br/>

(11) 좌측 항목에서 "Models"을 클릭하면 허깅페이스에서 자유롭게 쓸 수 있는 인공지능 모델을 선택할 수 있다.
![image13](https://github.com/user-attachments/assets/3b6fcaea-76d4-4b04-8467-c1577fa7643e)
<br/><br/>

2. 허깅페이스 기능 및 도구
<br/>
    
(1) Transformers 라이브러리   
Hugging Face의 Transformers 라이브러리는 BERT, GPT-2, GPT-3, RoBERTa, T5 등   
다양한 NLP 모델들을 제공하는 오픈소스 라이브러리다.          
이 라이브러리는 복잡한 AI 모델을 쉽게 사용할 수 있도록 설계되었으며   
특히 자연어 이해(NLU), 자연어 생성(NLG) 작업에서 큰 성과를 내고 있다.          
Transformers 라이브러리는 수백 개의 미리 훈련된 모델을 지원하며   
이를 특정 작업에 맞게 미세 조정(Fine-Tuning)할 수 있는 기능도 제공한다.          
예를 들어 사용자는 Transformers를 사용하여   
텍스트 분류, 감정 분석, 번역, 텍스트 요약, 질문 답변 등의 작업을 손쉽게 수행할 수 있다.         
<br/>

(2) Datasets 라이브러리   
AI 모델을 훈련시키기 위해서는 대규모 데이터셋이 필요하다.          
Hugging Face의 Datasets 라이브러리는 데이터셋에 쉽게 접근할 수 있는 도구를 제공하며    
연구자들이 모델을 훈련시킬 수 있도록 지원한다.          
이 라이브러리는 텍스트, 이미지, 오디오 등 다양한 형식의 데이터를 빠르게 로드하고 전체 작업을 단순화한다.         
Datasets 라이브러리는 대규모 데이터셋을 효율적으로 처리할 수 있도록 설계되었으며,    
데이터의 크기가 아무리 커도 원활하게 작동한다.          
또한, 데이터 증강(Data Augmentation), 샘플링, 전처리 등의 작업을 위한 다양한 유틸리티를 제공한다.         
<br/>

(3) Hugging Face Hub   
Hugging Face Hub는 AI 모델과 데이터셋을 공유하고 재사용할 수 있는 플랫폼이다.          
전 세계의 연구자와 개발자가 자신이 만든 모델을 업로드하고,    
다른 사람들이 이를 활용할 수 있도록 허브 형태로 운영되고 있다.       
이를 통해 커뮤니티 내 협업이 활발히 이루어지며,    
시기성을 빠르게 맞출 수 있도록 지원한다.      
Hub에 업로드된 모델은 다양한 작업에 맞도록 미리 훈련된 상태로 제공되며    
모델 및 데이터 버전 관리, 권한 설정, 협업 도구 등을 지원한다.       
이를 통해 대규모 팀이 효율적으로 프로젝트를 관리할 수 있도록 돕는다.      
<br/>

(4) Inference API   
허깅페이스는 Inference API를 통해 실시간 AI 모델 제공 서비스를 운영하고 있다.       
이 API를 사용하면 복잡한 인프라 없이도 AI 모델을 즉시 배포하고 사용할 수 있다.       
예를 들어 웹 애플리케이션에서 실시간으로 텍스트를 번역하거나 감정 분석을 수행하는 등의 작업이 가능하다.      
Inference API는 다양한 프로그래밍 언어와 프레임워크에서 쉽게 통합될 수 있다.      
그리고 REST API를 통해 간편하게 호출할 수 있다.      
이는 특히 AI 모델을 웹 서비스나 모바일 애플리케이션에 통합하고자 하는 개발자들에게 유용하다.      
<br/>

3. 허깅페이스 커뮤니티와 협력 활동
<br/>

(1) 허깅페이스의 성공 비결 중 하나는 강력한 오픈소스 커뮤니티이다.       
수많은 개발자와 연구자들이 이 플랫폼에 기여하고 있으며 서로의 지식을 공유하고 협력한다.      
허깅페이스는 GitHub와 같은 플랫폼을 통해 코드와 모델을 공유하며 이를 통해 커뮤니티가 공동으로 발전해 나간다.      
예를 들어 사용자는 새로운 모델을 훈련시키고 이를 Hugging Face Hub에 업로드하여 다른 사람들이 사용하도록 공유한다.      
<br/>

(2) 허깅페이스는 다양한 연구 기관 및 기업과 협력하여 AI 기술의 발전을 이끌고 있다.   
예를 들어 Google, Microsoft, Amazon과 같은 주요 기술 기업들은 허깅페이스의 라이브러리를       
자사의 클라우드 플랫폼과 통합하여 고객들이 AI 모델을 더 쉽게 사용하도록 지원하고 있다.       
또한, 대학과 연구소와의 협력을 통해 새로운 모델 아키텍처나 훈련 기업을 개발하는데 기여하고 있다.
![image14](https://github.com/user-attachments/assets/ab4d01c4-dc4a-4475-94c0-8cef93a2632c)
<br/><br/>

4. Hugging Face의 활용 사례
<br/>

(1) 금융 업계 - 고객 서비스 자동화            
NLP 모델을 활용한 고객 지원 챗봇과 문서 분석 시스템을 개발하는데 사용된다.      
이를 통해 고객 응대 속도를 높이고 문서 처리를 자동화할 수 있다.              
<br/><br/>
BNP Paribas : 유럽의 대형 은행인 BNP Paribas는 Hugging Face의 NLP 모델을 사용해 고객 서비스 자동화를 구현했다.          
이를 통해 고객의 질문을 자동으로 처리하고, 맞춤형 금융 솔루션을 제공할 수 있었다.          
고객 만족도와 응답 속도가 크게 개선되었으며 고객 지원 팀의 효율성도 향상되었다.         
<br/>

(2) 의료 업계 - 의료 기록 분석   
환자의 의료 기록을 분석하여 진단을 지원하거나 환자와의 대화를 통해 건강 상태를 모니터링하는 시스템을 구축하는 데 활용된다.       
NLP 모델은 의료 데이터의 자연어 처리를 통해 의료 전문가의 의사 결정을 돕는다.      
<br/>

Roche : 글로벌 제약 회사인 Roche는 허깅페이스 NLP 기술을 활용해 의료 기록을 분석하고    
환자의 건강 상태를 모니터링하는 시스템을 개발했다.       
이를 통해 의료진은 환자의 상태를 실시간으로 모니터링할 수 있고 필요한 경우 신속하게 대응할 수 있었다.       
또한, 연구 개발 과정에서 중요한 데이터 인사이트를 도출할 수 있었다.   
<br/>

(3) 전자상거래 업계 - 제품 추천   
제품 리뷰 분석, 고객 피드백 분석, 상품 추천 등 다양한 작업에 Hugging Face의 모델이 사용된다.       
이를 통해 사용자의 경험을 개선하고 개인화된 서비스를 제공할 수 있다.      
<br/>

Shopify : Shopify는 허깅페이스의 모델을 사용하여 개인화된 제품 추천 시스템을 개발했다.      
이를 통해 사용자들이 검색하거나 관심을 가진 제품과 관련된 추천을 제공함으로써 구매 전환율을 높였다.      
AI를 통한 맞춤형 추천은 고객 경험을 향상시키고, 판매를 촉진하는데 중요한 역할을 했다.      
<br/>

(4) 전자상거래 업계 - 제품 추천   
교육용 챗봇, 학습 자료 분석, 온라인 학습 도구 등 다양한 교육용 애플리케이션에서 Hugging Face의 모델이 활용된다.      
AI를 통한 교육의 개인화와 자동화가 가능하다.      
<br/>

Duolingo : 언어 학습 플랫폼 Duolingo는 허깅페이스의 NLP 기술을 활용해 사용자 맞춤형 학습 경험을 제공한다.      
이를 통해 학습자의 수준에 맞는 문제를 제시하고 자연어로 피드백을 제공하여 학습 효과를 극대화하고 있다.
<br/><br/> 

5. 허깅페이스 비즈니스 모델과 가격 정책
<br/>      
(1) Hugging Face의 비즈니스 모델   
허깅페이스 비즈니스 모델은 프리미엄 서비스와 API 사용료가 있다.   
<br/>

프리미엄 서비스 : 허깅페이스는 기본적인 도구와 모델을 오픈소스로 제공하지만 기업 고객을 위한 프리미엄 서비스도 운영한다.   
이러한 서비스에는 맞춤형 모델 개발, 기술 지원, 클라우드 배포 옵션 등이 포함되며 기업의 요구에 맞춘 솔루션을 제공한다.   
<br/>

API 사용료 : 허깅페이스는 Inference API를 통해 AI 모델을 쉽게 배포할 수 있는 서비스를 제공한다.   
Inference API는 사용량에 따라 과금하는 방식으로 수익을 창출한다.   
이 API는 특히 웹 애플리케이션이나 모바일 애플리케이션에 AI 기능을 통합하려는 기업에게 유용한 도구이다.   
<br/>

(2) Hugging Face의 가격 정책   
Hugging Face는 다양한 사용자층을 고려한 유연한 가격 정책을 제공하고 있다.    
주로 오픈소스 라이브러리와 서비스는 무료로 제공되지만 기업 고객과 대규모 프로젝트를 위한 프리미엄 옵션도 마련되어 있다.    
<br/>

- 무료 플랜 :    
Hugging Face의 많은 기본 기능은 무료로 제공된다.    
특히, 오픈소스 라이브러리인 Transformers와 Datasets 라이브러리는 누구나 자유롭게 사용할 수 있다.    
이 플랜에서는 모델을 사용하거나 학습할 수 있으며 제한된 리소스로 서비스를 운영할 수 있다.
<br/>

- Pro 플랜 :    
프로 플랜은 월 $9 정도의 요금으로 제공되며 추가적인 API 호출량, 더 높은 성능의 모델 실행, 그리고 더 많은 데이터 처리 능력을 제공한다.    
이 플랜은 중소기업이나 팀 프로젝트에 적합하다.
<br/>

- 기업용 플랜 (Enterprise) :    
기업 고객을 위한 맞춤형 플랜으로 비용은 사용자의 요구 사항에 따라 변동된다.    
이 플랜은 전용 지원, 맞춤형 솔루션, 더 높은 수준의 보안, 그리고 무제한 API 호출을 포함한 다양한 혜택을 제공한다.    
가격은 고객과의 협의에 따라 결정된다.
<br/>

- Inference API :    
Inference API를 통해 실시간으로 AI 모델을 배포할 수 있으며 사용량에 따라 비용이 부과된다.    
이 API는 특히 웹 애플리케이션, 챗봇, 자동화된 시스템에서 실시간 AI 기능을 구현하는데 사용된다.    
가격은 사용량에 따라 다르며 일반적으로 API 호출당 몇 센트에서 수십 센트 사이이다.
<br/>

Hugging Face의 가격 정책에 관해서는 아래 공식 사이트에서 더 상세히 확인 가능하다.      
https://huggingface.co/pricing
![image15](https://github.com/user-attachments/assets/bd8b1c0b-20bf-4efc-9cfe-0a3c86680b6d)
<br/>
   
      
6. 허깅페이스 GitHub 리포지토리    
허깅페이스에서 제공하는 GitHub 리포지토리는 아래 링크에서 확인 가능하다.   
https://github.com/huggingface
<img width="1800" alt="image16" src="https://github.com/user-attachments/assets/3e0ea123-c4f1-4f5f-9b7d-3b84f36d6c30">
<br/><br/>

---
<br/>

## Amazon SageMaker에서 허깅페이스 사용      
<br/>

(1) AWS 콘솔에서 오레곤 리전의 Amazon 세이지메이커 서비스에 들어간다.      
그 후, "Notebooks" 항목을 클릭한다.          
<img width="1800" alt="image1" src="https://github.com/user-attachments/assets/aa2210bf-d37d-48c8-85d3-6772ec49fd09">
<br/>
        
(2) 노트북 인스턴스 이름과 유형, 볼륨 크기, 권한, 네트워크를 지정해주자.   
이번 테스트에는 ml.m5.2xlarge 정도의 인스턴스 타입을 사용하겠다.   
![image2](https://github.com/user-attachments/assets/f2637f03-d808-4ff1-a151-783e4dc628c4)
<br/>    
                    
(3) 노트북 인스턴스 상태가 "InService"로 바뀌면 주피터나 주피터랩을 실행하면 된다.
![image3](https://github.com/user-attachments/assets/be3d220a-e008-4c88-a2fa-bcb60030d166)
<br/>
             
(4) Jupyter를 열고 New를 클릭하면 여러 가지 항목들이 보인다.    
일단 테스트를 위해서는 conda_python3를 클릭해보자.    
![image4](https://github.com/user-attachments/assets/16c5bef8-34ad-41f7-adf6-269ca0d444dd)
<br/>
        
(5) 제일 먼저 아래 명령어를 순서대로 실행해준다.    
명령어 (1) : pip install torch    
명령어 (2) : pip install transformers  
<br/>
(6) 노트가 열리면 아래의 코드를 복사한 후 실행한다.   
"Hugging Face 토큰" 부분에는 허깅페이스에서 발급받은 토큰을 기입한다.    
<br/>

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from huggingface_hub import login

# Hugging Face 토큰으로 로그인
login(token="Hugging Face 토큰")

# 사용할 모델 ID (Meta Llama 3.1-8B)
model_id = "meta-llama/Meta-Llama-3.1-8B"

# 토크나이저와 모델 로드 (float16으로 메모리 절약)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype="auto")

# 텍스트 생성 파이프라인 생성
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# 입력 프롬프트에 따라 언어 설정 (한국어면 한국어로 답변)
def get_prompt_language(prompt):
    if any(char.isalpha() for char in prompt) and not any('\u3131' <= char <= '\uD79D' for char in prompt):
        return "English"  # 영어 프롬프트
    return "Korean"  # 한국어 프롬프트

# 프롬프트 설정
prompt = input("질문을 입력하세요: ")

# 한국어 질문인 경우 한국어로 답변하도록 프롬프트 변경
language = get_prompt_language(prompt)
if language == "Korean":
    prompt = "한국에서 대표적인 관광지 5곳을 추천해주세요."

# 텍스트 생성 (반복 방지를 위해 temperature, top_p, repetition_penalty 설정)
outputs = generator(
    prompt, 
    max_length=2000,                 # 더 짧게 제한
    num_return_sequences=1,         # 한 번에 1개의 텍스트 생성
    temperature=0.7,                # 무작위성 추가
    top_p=0.9,                      # 상위 90% 확률 토큰들만 사용
    repetition_penalty=1.2          # 동일한 단어의 반복을 억제
)

# 생성된 텍스트 출력
print("Generated text:")
for output in outputs:
    print(output["generated_text"])
```
<br/>
    
(7) 질문창이 열리면 질문을 입력한다. 잠시 기다리면 답변이 출력된다.   
답변이 출력되면 일단 SageMaker에서의 테스트도 완료다.   
![image5](https://github.com/user-attachments/assets/568f5d16-a9ff-49d9-a4d6-9293622e415c)
<br/><br/>

---
<br/>

## Amazon EC2에서 허깅페이스 사용      
<br/>
   
허깅페이스를 이용해 EC2에서 아래와 같은 환경을 구성할 수도 있다.
<br/>

Hugging Face 모델이 한 번 로컬(EC2 인스턴스)에 다운로드되면    
이후에는 Hugging Face 사이트와 통신하지 않고 EC2 인스턴스 내의 로컬 캐시에서 모델을 불러와 실행할 수 있다.    
즉, 모델이 로컬에 저장된 후에는 네트워크 연결 없이 로컬 자원만으로도 모델을 실행할 수 있다.   
<br/>

(1) 로컬 캐시에 저장 :   
모델 파일, 토크나이저 파일, 구성 파일이 로컬 캐시(~/.cache/huggingface/transformers)에 저장된다.   
같은 모델을 다시 호출할 때는 Hugging Face 사이트에 재연결하지 않고 로컬 캐시에서 해당 모델 파일을 불러온다.   
<br/>

(2) 네트워크 연결이 불필요 :   
모델이 캐시에 저장된 후에는 Hugging Face 서버와 다시 통신할 필요가 없다.    
EC2 인스턴스 내의 로컬 자원으로 모델을 불러와 실행할 수 있다.   
이렇게 하면 네트워크 연결 상태와 무관하게 모델을 사용할 수 있다.   
<br/>

(3) 성능 향상 :
로컬 캐시에서 모델을 불러오기 때문에 네트워크 속도에 의존하지 않고, 매우 빠르게 모델을 실행할 수 있다.      
네트워크 트래픽을 줄이고, 인터넷 연결 없이도 모델을 계속 사용할 수 있는 장점이 있다.      
<br/>
![image1](https://github.com/user-attachments/assets/c0003641-0c38-4950-bfbb-d0a33c0a34b9)
<br/><br/>
             
1. 허깅페이스 AMI로 EC2 인스턴스 생성
<br/>
    
(1) EC2 인스턴스는 엔비디아 GPU 칩셋이 달린 g4dn.8xlarge 타입으로 생성한다.   
g4dn.8xlarge 타입이 사용 불가면 Service Quotas에서 신청한다.   
Service Quotas에서는 vCPU 기반으로 신청하기 때문에 g4dn.8xlarge를 사용하려면 32정도를 신청해야 한다.   
https://aws.amazon.com/ko/ec2/instance-types/g4/   
![image2](https://github.com/user-attachments/assets/58223c15-e88d-45d3-8d8f-a2850971f5ab)   
![image3](https://github.com/user-attachments/assets/f1e0d3e1-3ed6-4b35-90ff-6380e48d76f8)   
<br/>
       
(2) 가능한 "Nvidia Driver AMI GPU PyTorch" 문구가 들어가 있는 AMI로 서버를 생성하자.       
서버에서 AI/ML 서비스를 실행할 때 호환성 문제를 최소화할 수 있다.       
![image4](https://github.com/user-attachments/assets/bae3efa9-7ad6-498b-8873-50d215b8424a)
<br/><br/>

2. EC2 서버에서 허깅페이스 환경 구성
<br/>

(1) 이제 서버에 접속하여 Nvidia 드라이버 버전과 CUDA 버전을 확인하자.      
CUDA는 NVIDIA에서 개발한 병렬 컴퓨팅 플랫폼이자 프로그래밍 모델로       
GPU를 사용하여 복잡한 계산을 가속화할 수 있게 해주는 기술이다.      
Nvidia 칩셋으로 딥러닝할 때 PyTorch와 GPU 가속을 위해 필수다.      
명령어 : nvidia-smi   
![image5](https://github.com/user-attachments/assets/7ee5129b-7b68-4624-af72-1dabeaec2b6f)  
<br/>

(2) 다음은 아래 순서대로 명령어를 실행하여 pip 최신 버전을 설치하고 업데이트를 하자.         
명령어 (1) : apt update         
명령어 (2) : apt install -y python3-pip         
명령어 (3) : pip install --upgrade pip         
<br/>

(3) 다음은 아래 명령어로 GPU 가속을 위한 CUDA 지원이 포함된 PyTorch를 설치한다.      
반드시 GPU 가속을 위한 CUDA 지원 버전의 PyTorch를 설치해야 한다.      
명령어 : pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117      
<br/>

(4) GPU 가속을 위한 PyTorch가 정상적으로 설치되었는지 확인하기 위해       
아래와 같이 명령어를 실행한 후 Python 인터프리터에서 코드를 실행하자.      
명령어 : python3      
<br/>

Python 환경에서 아래 코드를 실행하면 된다.      
<br/>

코드 (1) : import torch        
<br/>
코드 (2) : print(torch.cuda.is_available())           
GPU가 사용 가능한지 확인. True를 반환하면 GPU를 사용한 PyTorch 가속이 가능하다는 뜻이다.
<br/>       
코드 (3) : print(torch.cuda.device_count())           
사용 가능한 GPU의 수. 1 이상이 반환되면 GPU를 인식하고 있다는 의미다.
<br/>     
코드 (4) : print(torch.cuda.current_device())           
현재 사용 중인 GPU ID 확인.
<br/>   
코드 (5) : print(torch.cuda.get_device_name(torch.cuda.current_device()))          
현재 사용 중인 GPU 이름 반환. 예를 들어 Tesla T4 같은 결과를 볼 수 있다.         
<br/>

아래와 같은 결과가 출력되면 PyTorch가 GPU를 정상적으로 인식하고 있는 것이다.      
<br/>

True   
1   
0   
Tesla T4   
<br/>

GPU 가속 상태 확인이 끝나면 아래 명령어로 python 인터프리터를 나온다.      
코드 : exit()   
<br/>

(5) 끝으로 허깅페이스 모델을 다루기 위해 transformers, accelerate, datasets 패키지를 설치한다.      
허깅페이스 라이브러리까지 설치하면 허깅페이스에서 모델을 호출하기 위한 준비가 완료되는 것이다.      
명령어 : pip install transformers datasets accelerate      
<br/>

3. 허깅페이스에서 모델 호출 테스트
<br/>
        
(1) CLI로 Hugging Face에 로그인하도록 하자.       
그러면 이후에는 자동으로 API 토큰이 인증된다.      
명령어 : huggingface-cli login
![image6](https://github.com/user-attachments/assets/7e004178-4a8e-4885-a819-7a3325109b80)     
<br/>

(2) vi 편집기 등을 사용하여 허깅페이스 모델 호출 테스트를 위한 스크립트(huggingface_test.py)를 작성한다.      
명령어 : vi huggingface_test.py       
<br/>

```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# 사용할 모델 ID (Meta Llama 3.1-8B)
model_id = "meta-llama/Meta-Llama-3.1-8B"

# 토크나이저와 모델 로드 (float16으로 메모리 절약)
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

# 텍스트 생성 파이프라인 생성 
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

# 입력 프롬프트에 따라 언어 설정 (한국어면 한국어로 답변)
def get_prompt_language(prompt):
    if any(char.isalpha() for char in prompt) and not any('\u3131' <= char <= '\uD79D' for char in prompt):
        return "English"  # 영어 프롬프트
    return "Korean"  # 한국어 프롬프트

# 프롬프트 설정
prompt = input("질문을 입력하세요: ")

# 한국어 질문인 경우 한국어로 답변하도록 프롬프트 변경
language = get_prompt_language(prompt)
if language == "Korean":
    prompt = f"다음 질문에 한국어로 답변해주세요: {prompt}"
else:
    prompt = f"Please answer the following question in English: {prompt}"

# 텍스트 생성 (반복 방지를 위해 temperature, top_p, repetition_penalty 설정)
outputs = generator(
    prompt, 
    max_length=2000,                 # 더 짧게 제한
    num_return_sequences=1,          # 한 번에 1개의 텍스트 생성
    temperature=0.7,                 # 무작위성 추가
    top_p=0.9,                       # 상위 90% 확률 토큰들만 사용
    repetition_penalty=1.2,          # 동일한 단어의 반복을 억제
    do_sample=True,                  # 샘플링 활성화
    truncation=True,                 # 입력 텍스트 자동 자르기
    pad_token_id=tokenizer.eos_token_id  # 패딩 토큰 설정
)

# 생성된 텍스트 출력
print("Generated text:")
for output in outputs:
    print(output["generated_text"])    
```
<br/>

(3) 아래 명령어로 스크립트를 실행한다.      
명령어 : python3 huggingface_test.py 
![image7](https://github.com/user-attachments/assets/3e091fe5-a215-49c0-b05d-e2d698fef77d)
<br/>
        
(4) EC2 서버 초기 환경에서는 영어로 질문을 해야 더 정확한 답변을 받을 수 있다.
![image8](https://github.com/user-attachments/assets/7cab37a9-5cdf-451c-a336-90c899cb1573)
<br/>
