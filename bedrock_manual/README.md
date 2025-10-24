## [Amazon 생성형 AI 서비스 베드락(Bedrock)]    
<br/>     

베드락(Bedrock)은 아마존이 ChatGPT의 대항마로 내놓은 생성형 AI 서비스다.      
ChatGPT 등의 생성형 AI를 이용해본 사람은 베드락에서도 비슷한 기능을 이용할 수 있다.     
다만 일반 사용자 입장에서는 편의성이나 기능이 ChatGPT가 압도적으로 좋다.      
본 문서는 베드락에 대해 참고 사항 수준으로 작성한다.     
<br/>  
  
1. 베드락은 사용 가능 리전이 제한되어 있다.   
사용하기 전에 먼저 사용 가능한 리전을 확인해본다.  
<img width="400" alt="image" src="https://github.com/user-attachments/assets/54f8127a-3a1d-4910-93fc-9bfe91c36897">
<br/><br/>
 
2. AWS에서 베드락 서비스로 들어간다.  
<img width="1400" alt="image" src="https://github.com/user-attachments/assets/8069c7c6-4fd0-4e2d-a353-521b0b3b656a">
<br/><br/>     
    
3. 보통은 AI 모델에 대한 액세스 권한이 없다.  
AI 모델을 사용하기 위해서는 하단의 "모델 액세스"에서 액세스 권한을 요청해야 한다.  
![image](https://github.com/user-attachments/assets/ba486729-6fb4-4f1d-b15e-2e418a306c49)
<br/><br/> 
  
4. "모델 액세스"에서 사용을 원하는 AI 모델을 선택하고 액세스 권한을 요청한다.  
엔트로픽 모델은 사용 사례 세부 정보를 제출해야 한다. (보통은 테스트용으로 기입하면 됨)  
다른 모델은 액세스 권한을 요청하면 바로 사용 가능하다.  
<img width="1400" alt="image" src="https://github.com/user-attachments/assets/64d715ec-9817-4ba1-86be-ab0bb718122c">
<img width="1800" alt="image" src="https://github.com/user-attachments/assets/3208cefb-a39b-48e7-bdc0-9e147aaf9313">
<br/><br/>  
           
5. 이제 "플레이그라운드 -> 텍스트"에 들어가서 AI 모델을 선택하고 ChatGPT 등의 생성형 AI를 사용하듯이 AI와 소통해보자.  
<img width="1400" alt="image" src="https://github.com/user-attachments/assets/966491da-99bc-4c55-82f3-9139b0c3fcc9">
<img width="1400" alt="image" src="https://github.com/user-attachments/assets/1a250a03-c3a2-4edd-b0d5-a5dae67a1b99">
<br/><br/>  
  
6. 이번에는 이미지 AI 모델을 이용해서 이미지를 생성해보자.  
텍스트 AI 모델과 비슷한 방식으로 이미지 AI 모델 액세스 권한을 요청하면 된다.  
여기서는 Amazon Titan 모델을 이용해보도록 하겠다.  
<img width="1800" alt="image" src="https://github.com/user-attachments/assets/32d455b2-442f-4418-bcd0-a855c2e8500d">
<br/><br/>  
  
7. 이제 "플레이그라운드 -> 이미지"에 들어가서 AI 모델을 선택하고 ChatGPT, Bing 이미지 크리에이터 등의 이미지 생성형 AI를 사용하듯이 AI와 소통해보자.  
<img width="1800" alt="image" src="https://github.com/user-attachments/assets/84f3f5b0-9f00-46b3-a354-c14f5f1ae45f">
<br/><br/>  
  
8. 한글로 명령어를 내리면 엉뚱한 이미지를 생성할 수도 있다.  
아직 한글 명령어가 제대로 실행되지 않는다는 뜻이니 영어로 바꿔서 명령어를 실행하자.  
<img width="1200" alt="image" src="https://github.com/user-attachments/assets/70945767-5a73-4383-b6e8-0212ab593291">
<br/><br/>  
  
9. 영어로 명령어를 내리면 제대로 이미지를 생성하는 것을 확인할 수 있다.  
ChatGPT나 Bing 이미지 크리에이터에서 한글 명령어가 제대로 실행되는 점과 비교해보면 아직 베드락이 부족한 건 사실이다.    
<img width="1400" alt="image" src="https://github.com/user-attachments/assets/6c98ddd5-fdab-4119-a42e-9f793d294237">
<br/><br/>  
  
10. 베드락은 AI 모델을 사용하는 경우에만 요금이 부과된다.  
요금은 많이 나온다고 볼 수는 없으나 여전히 편의성이나 기능만을 보면 일반 사용자 입장에서는 ChatGPT, Claude 등이 훨씬 낫다.    
![image](https://github.com/user-attachments/assets/0bb0810a-4eb5-43f3-a66c-ccb66f61c9ec)
<img width="1200" alt="image" src="https://github.com/user-attachments/assets/d6d773cd-734b-455c-9058-e9296d43069d">
<br/><br/>  
  
---
<br/>  
  
AWS 콘솔이 아닌 파이썬 코드를 통해 로컬 PC나 윈도우 서버에서 베드락을 실행시키는 방법은 아래와 같다.  
해당 방법을 응용하면 베드락을 연동하여 별도의 웹 서비스를 구성할 수 있다.  
<br/><br/>  
  
1. AWS 콘솔 Bedrock "모델 액세스"에서 사용을 원하는 AI 모델을 선택하고 액세스 권한을 요청하는 것은 동일하다.   
AI 액세스 권한이 없으면 로컬 PC에서 코드를 실행해도 동작하지 않는다.  
여기서는 텍스트 생성 작업을 테스트 할 예정이라 현재 가장 성능이 좋은 엔트로픽 클로드 모델을 선택하도록 하겠다.  
<img width="1400" alt="image" src="https://github.com/user-attachments/assets/caf007c9-3815-4c98-b4d9-edd8104741dc">  
<br/><br/>  
  
2. 로컬 PC나 윈도우 서버 상에 아래의 파이썬 스크립트 파일(bedrock_test.py)을 작성해 놓는다.  
영어권 대학생들에게 블랙홀에 대해 설명하라는 내용이다.  
<br/>  
  
```python
import boto3
import json
brt = boto3.client(service_name='bedrock-runtime')

body = json.dumps({
    "prompt": "\n\nHuman: explain black holes to university student\n\nAssistant:",
    "max_tokens_to_sample": 500,
    "temperature": 0.1,
    "top_p": 0.9,
})

modelId = 'anthropic.claude-v2'
accept = 'application/json'
contentType = 'application/json'

response = brt.invoke_model(body=body, modelId=modelId, accept=accept, contentType=contentType)

response_body = json.loads(response.get('body').read())

# text
print(response_body.get('completion'))
```
<br/> 
  
AI 모델 ID의 경우 Bedrock 제공업체 항목에서 하단의 API 요청 부분을 보면 나와있다.  
코드를 작성할 때 AI 모델 ID를 기입해야 하는 경우 해당 부분을 참고해서 코드를 작성하면 된다.  
<img width="1800" alt="image" src="https://github.com/user-attachments/assets/fd25b974-5515-42cc-a46e-87eff14cd5dd">  
<br/>  
  
3. 윈도우 cmd 창에서 aws configure 명령어를 통해 적절한 권한이 있는 액세스키, 베드락 사용 리전, json 포맷을 등록한다.   
보통 액세스키에 AmazonBedrockFullAccess 권한을 주면 되나 해당 권한으로 안 되는 것이 있으면 다른 AWS 권한들을 추가해준다.  
<br/>  
  
4. 파이썬 스크립트 파일 내용을 살펴보고 필요한 모듈이 있다면 미리 설치해주자.  
boto3 등의 모듈이 없으면 pip install boto3 명령어로 모듈을 설치해주면 된다.  
<br/>  
  
5. 파이썬 스크립트 파일을 실행하기 위한 모든 모듈 설치가 완료되면 윈도우 cmd 창에서 python bedrock_test.py 명령어를 통해 베드락 AI를 호출해보도록 하자.    
<img width="1600" alt="image" src="https://github.com/user-attachments/assets/0d3adf09-c1ad-411f-aa92-33b9b3373ef7">
<br/><br/>

---
<br/>      

## [베드락 기반 플레이그라운드 파티락(PartyRock)]
<br/>

파티락(PartyRock)은 Amazon Bedrock 기반 AI 앱 놀이터(playground)다.   
코드를 작성하거나 AWS 계정을 생성하지 않고도 생성형 AI를 테스트하고,    
프롬프트 엔지니어링에 대해 배우고, 미니 앱을 빌드하고, 친구들과 공유할 수 있다.    
공유된 앱으로 시작한 다음 이를 리믹스하여 더욱 기능을 향상시킬 수도 있다.   
<br/>

1. 파티락은 아래 주소에 접속하면 사용할 수 있다.   
파티락 주소 - https://partyrock.aws/    
Apple, Amazon 또는 Google 계정을 사용하여 로그인할 수 있다.   
<img width="1800" alt="image1" src="https://github.com/user-attachments/assets/129fcf6d-02e2-45b8-8fb1-1ae889f54f2f">
<br/><br/> 

2. 샘플 앱을 검토하거나 직접 앱 빌드하기를 클릭하여 시작할 수 있다.      
빌드하려는 앱의 설명을 입력하고 PartyRock의 생성형 AI를 사용하여 실행을 시작하거나 위젯별로 직접 빌드할 수 있다.   
아래 이미지와 같이 생성하길 원하는 앱에 대한 설명을 작성하고 "Generate"를 클릭하자.   
<img width="600" alt="image2" src="https://github.com/user-attachments/assets/93824312-2a00-4e58-b274-fe1540313af8">
<br/><br/> 
     
3. 어플리케이션이 생성되면 제대로 작동하는지 테스트를 해보자. 
<img width="1800" alt="image3" src="https://github.com/user-attachments/assets/05c77b73-6bec-48e1-9ed6-848e493b01da">
<br/><br/> 

4. 상단의 "Share"를 클릭하면 본인이 만든 파티락 앱의 링크를 다른 사람에게 공유할 수 있다.
<img width="400" alt="image4" src="https://github.com/user-attachments/assets/4c99adff-218c-49a8-8eec-2b957798bd55">
<br/><br/> 
        
5. 상단의 "Edit"를 클릭하면 위젯의 위치를 수정하거나 새로운 위젯을 추가할 수 있다.
<img width="400" alt="image5" src="https://github.com/user-attachments/assets/8ec0536c-0e5e-4dfe-aa25-0f3e272d80d8">
<img width="1600" alt="image6" src="https://github.com/user-attachments/assets/7878546a-5d3f-40c2-83e9-a0048a054a6c">
<br/><br/> 

파티락의 다른 기능들은 아래와 같다.
<br/><br/> 

빈 앱 – 빈 앱에서 시작을 선택하고 위젯을 선택한 다음 원하는 대로 설정할 수도 있다.
![image7](https://github.com/user-attachments/assets/a586dc14-5e96-404a-b8d5-306bbf7c8e1f)
<br/>

리믹스 – 기존 앱(내 앱 또는 다른 공개 앱)으로 시작한 다음 리믹스하여 사용자 지정하거나 개선할 수 있다.
![image8](https://github.com/user-attachments/assets/e99f3455-7e69-4520-9845-dd1ef4b6cb74)
<br/>

챗봇 위젯 – 프롬프트를 시작점으로 사용하여 앱과 상호작용할 수 있다. 
![image9](https://github.com/user-attachments/assets/0175fda0-6741-4951-9820-9d0689d98f96)
<br/>

@ 참조 – 앱을 빌드하는 동안 ‘@’을 사용하여 이름을 기준으로 다른 위젯을 참조할 수 있다.
![image10](https://github.com/user-attachments/assets/80669d97-0c91-418a-a110-6505bc1cd87a)
<br/>

고급 설정 – 일부 위젯은 고급 설정을 제공합니다.    
예를 들어, 텍스트 생성 위젯은 모델에 대한 Temperature 및 Top P 파라미터를 제어할 수 있는 옵션을 제공한다.

![image11](https://github.com/user-attachments/assets/aad8120f-aefb-46ff-b383-774b6d914f05)
<br/>

백스테이지 – PartyRock 백스테이지에서 내 앱과 PartyRock 크레딧의 누적 사용량을 확인할 수 있다.
![image12](https://github.com/user-attachments/assets/b7e4ee0a-37ad-4c14-bec9-4ef116ebd21f)
<br/>

파티락 요금 :   
AWS는 제한된 기간 동안 신규 PartyRock 사용자에게 신용카드 정보 입력이나 AWS 계정 가입 없이 무료 평가판을 제공하므로 비용 발생에 대해 걱정하지 않고 기본 기술 학습을 시작할 수 있다.    
Backstage에서 크레딧 사용량을 추적할 수 있으며 크레딧 사용량은 입력 토큰, 출력 토큰, 생성된 이미지를 기반으로 계산된다.   
