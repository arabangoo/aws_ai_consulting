## [MCP on AWS 활용]    

본 MCP on AWS 매뉴얼은 Amazon Q Developer CLI를 활용한다는 전제 하에 작성한다.      
Amazon Q Developer CLI는 WSL이나 EC2를 통해 우분투 리눅스에서 실행하도록 한다.      
여기서는 AWS의 우분투 리눅스 EC2를 활용하도록 하겠다.       
<br/>
   
(1) AWS에서 우분투 리눅스 EC2 한 개를 생성한 후 접속한다.   
<img width="600" alt="image1" src="https://github.com/user-attachments/assets/b4e3c26d-93b1-4d78-b191-ff9422ba2b2e" />
<br/><br/>
                
(2) 시스템 업데이트 및 필수 패키지 설치를 진행한다.   
명령어 (1) : apt update && apt upgrade -y   
명령어 (2) : apt install -y curl git python3 python3-venv unzip   
<br/>
        
(3) Amazon Q Developer CLI를 설치한다.   
명령어 (1) : wget https://desktop-release.q.us-east-1.amazonaws.com/latest/amazon-q.deb   
명령어 (2) : apt-get install -f   
명령어 (3) : dpkg --force-depends -i amazon-q.deb   
<br/>

(4) Amazon Q Developer CLI 버전을 확인하고 로그인한다.   
로그인 링크가 출력되면 로컬 PC 웹브라우저에서 해당 링크로 접속 후 Builder ID로 로그인한다.   
명령어 (1) : q --version   
명령어 (2) : q login   
<img width="400" alt="image2" src="https://github.com/user-attachments/assets/acbaccc0-c134-4de8-a72c-66e4ca0bc721" />   

<img width="400" alt="image3" src="https://github.com/user-attachments/assets/b5ffe8ea-b28a-4c62-b491-4f4288dd2aba" />
<br/>

(5) GitHub에서 AWS 샘플 MCP 서버 코드를 클론한다.   
그 다음 실습 경로까지 들어간다.   
명령어 (1) : git clone https://github.com/aws-samples/aws-kr-startup-samples.git   
명령어 (2) : cd aws-kr-startup-samples/gen-ai/mcp-tutorial/module-01/part-01/src/example-1     
<br/>

(6) python 가상환경을 만들어주는 uv를 설치한다.   
명령어 (1) : curl -LsSf https://astral.sh/uv/install.sh | sh   
<img width="1200" alt="image4" src="https://github.com/user-attachments/assets/384f13f2-0fa2-4787-95d2-09fc1c4bc404" />
<br/><br/>

(7) uv 설치 후 터미널 재시작을 하거나 아래 명령어를 실행한다.   
명령어 (1) : source ~/.bashrc   
명령어 (2) : uv --version   
<br/>

(8) MCP 서버용 가상환경을 설정하고 의존 패키지를 설치한다.      
명령어 (1) : uv venv      
명령어 (2) : source .venv/bin/activate      
명령어 (3) : uv add "mcp[cli]" httpx   
<img width="1000" alt="image5" src="https://github.com/user-attachments/assets/206272b4-3c69-453f-b243-dbfc0a55e57c" />
<br/><br/>

(9) MCP 서버를 Amazon Q CLI에 연결한다. (mcp.json 설정)   
명령어 (1) : mkdir -p ~/.aws/amazonq   
명령어 (2) : vi ~/.aws/amazonq/mcp.json   
<br/>

(10) vi로 mcp.json 파일을 만들어준다.       
이때 소스파일을 clone했던 경로를 잘 확인하고 수정해준다.      

```python           
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/root/aws-kr-startup-samples/gen-ai/mcp-tutorial/module-01/part-01/src/example-1",
        "run",
        "weather.py"
      ]
    }
  }
}
```
<img width="800" alt="image6" src="https://github.com/user-attachments/assets/67a58b95-29e8-496c-a14b-a48e5a92936a" />
<br/><br/><br/>

(11) MCP 서버를 백그라운드에서 실행하도록 아래 명령어를 실행한다.    
MCP 서버는 Amazon Q CLI가 연결될 수 있도록 백그라운드에서 실행중이어야 한다.   
명령어 (1) : uv run weather.py    
<br/>

(12) 터미널을 그대로 두고 새로운 탭이나 세션을 연다.   
새 터미널 세션에서 Amazon Q CLI를 통해 weather MCP를 테스트하겠다.   
명령어 (1) : q chat      
<img width="600" alt="image7" src="https://github.com/user-attachments/assets/de0d3cd3-ad2f-4d1a-ba69-c93378561bcf" />
<br/><br/>

(13) 아래와 같은 프롬프트를 입력해본다.          
액션을 실행하겠냐는 메시지가 뜨면 't'를 입력한다.         
명령어 (1) : What are the active weather alerts in Texas?      
<img width="700" alt="image8" src="https://github.com/user-attachments/assets/acb12ecf-25cd-415f-a5f4-73946cc7fc40" />
<br/><br/>

(14) AI 응답이 뜨면 MCP 서버 테스트에 성공한 것이다.   
<img width="1200" alt="image9" src="https://github.com/user-attachments/assets/137dc10f-453e-4541-b08d-38225771e624" />
<br/><br/>

(15) 한국어로 말해달라고 해도 잘 대답해준다.   
<img width="1000" alt="image10" src="https://github.com/user-attachments/assets/87de3402-9d85-40c2-8a60-b6f25f5c37cb" />
