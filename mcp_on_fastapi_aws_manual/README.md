## [MCP on FastAPI - AWS 활용]    

본 매뉴얼에서는 AWS의 우분투 리눅스 EC2를 활용하도록 하겠다.         
<br/>
   
(1) AWS에서 우분투 리눅스 EC2 한 개를 생성한 후 접속한다.     
<img width="600" alt="image1" src="https://github.com/user-attachments/assets/b4e3c26d-93b1-4d78-b191-ff9422ba2b2e" />
<br/><br/>   

(2) 시스템 업데이트를 진행한다.   
명령어 (1) : apt update && apt upgrade -y            
<br/>       

(3) 도커를 설치하고 활성화한다.   
명령어 (1) : apt install -y docker.io   
명령어 (2) : systemctl start docker   
명령어 (3) : systemctl enable docker    
<br/>

(4) 파일질라 등을 통해 필수 파일을 서버로 옮겨놓는다.   
그 뒤, 해당 경로로 이동한다.    
필수 파일 : Dockerfile / main.py / requirements.txt   
<img width="500" alt="image2" src="https://github.com/user-attachments/assets/f6c20980-1c23-41b3-a9bd-e68d4968eb70" />
<br/><br/> 

(5) 도커 이미지를 빌드한다.   
명령어 (1) : docker build -t fastapi-mcp .   
<br/>

(6) 컨테이너를 실행한다.    
-d 옵션으로 인해 컨테이너가 백그라운드로 영구 실행된다.   
--restart always 옵션으로 인해 서버가 중지되었다가 다시 시작되면 컨테이너도 재실행된다.   
명령어 (1) : docker run -d --restart always -p 8000:8000 fastapi-mcp   
<br/>

(7) 도커 컨테이너의 상태를 확인한다.      
명령어 (1) : docker ps      
<img width="900" alt="image3" src="https://github.com/user-attachments/assets/6940eb5a-b933-4f28-b273-e4ff0da8ec36" />
<br/><br/> 

(8) 웹브라우저에서 아래 주소를 입력하고 출력 내용을 확인한다.   
이미지와 같이 { "status": "healthy" } 값이 나오면 정상인 것이다.       
http://<ec2_public_ip>:8000/health     
<img width="300" alt="image4" src="https://github.com/user-attachments/assets/b2f3cc1e-45d5-40a5-bf04-542f2509e555" />
<br/><br/>

(9) 이제 AWS 콘솔에서 다음 사항을 참고하여 ALB를 만든다.     
1. 리스너 : 80 (HTTP)    
2. 대상 그룹 : EC2 인스턴스(8000 포트) 등록    
3. 헬스체크 : /health     
4. ALB DNS 주소 확인     
<br/>

(10) 웹브라우저에서 아래 주소를 입력하고 출력 내용을 확인한다.          
만약 EC2 IP로는 정상 출력이 되는데 ALB 주소로 정상 출력이 안 되면 보안그룹이나 리스너가 잘못 등록된 것이니 확인해본다.      
http://<alb_dns_name>/health         
<br/>

(11) ALB와 대상그룹까지 만들어지면 클로드 데스크탑을 통해 MCP 서버와 통신할 수 있다.   
일단 클로드 데스크탑을 설치하기 전에 로컬 PC에서 아래 명령어로 Node.js와 npm을 설치하도록 하자.   
명령어 (1) : winget install OpenJS.NodeJS   
<img width="900" alt="image5" src="https://github.com/user-attachments/assets/a6bb1548-c429-4c58-9abc-3969123cbf1a" />
<br/><br/>

(12) 클로드 데스크탑을 다운로드 한다.   
다운로드 링크 : https://claude.ai/download   
<br/>

(13) "파일 -> 설정 -> 개발자" 경로에서 MCP를 설정할 수 있다.               
![image6](https://github.com/user-attachments/assets/467bd16d-a0bf-4991-a3bd-699927ed488b)   
<img width="950" alt="image7" src="https://github.com/user-attachments/assets/60b4753d-fb00-43af-bfa9-47e990469be7" />   
<br/>

(14) 클로드 폴더가 열리고 "claude_desktop_config.json" 파일을 확인한다.       
메모장으로 해당 파일을 열어 json 내용을 기입한다.      
예시 파일에는 desktop-commander라는 기존 MCP 서버에 추가로 weather-server라는 MCP 서버를 추가했다.            
weather-server를 호출하는 ALB 주소는 본인이 생성한 ALB 주소에 맞게 수정해줘야 한다.         
<img width="800" alt="image8" src="https://github.com/user-attachments/assets/805b9c3b-9e68-480c-8ff5-ed58e255d204" />
<br/><br/>

(15) 일단 MCP 서버를 적용하면 클로드 데스크탑 재시작을 해야한다.      
그러면 망치 아이콘이 확인될 텐데 MCP 서버가 적용되었다는 뜻이다.           
<img width="700" alt="image9" src="https://github.com/user-attachments/assets/41fc84af-929e-4966-9998-006beaa7a55b" />
<br/><br/>

(16) 미국 지역 날씨를 조회해보면 정상적으로 AI 응답이 출력되는 것을 확인할 수 있다.       
<img width="700" alt="image10" src="https://github.com/user-attachments/assets/7502bb14-0a3c-4c33-a39a-1fc49dd118a1" />
<br/><br/>

(17) MCP 서버를 Smithery에 올려놓고 호출하면 클로드 데스크탑 설정 json에 들어갈 내용도 간단해진다.   
MCP 서버가 퍼블릭 공간에 올려놓을 수 있는 내용이면 smithery에 올려놓고 호출하자.    
Smithery는 MCP 클라이언트만 간편하게 배포하는 것이고 백엔드 서비스(ALB/EC2)는 그대로 유지된다.   

[ALB를 직접 호출하는 경우]
```txt  
"weather-server": {
  "command": "node",
  "args": ["-e", "매우 긴 JavaScript 코드..."]
}
```

[smithery에서 호출하는 경우]
```txt
"weather-server": {
  "command": "cmd", 
  "args": ["/c", "npx", "-y", "@smithery/cli@latest", "run", "@your-username/aws-weather-mcp-server"]
}
```
