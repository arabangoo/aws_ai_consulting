## [Amazon Q Developer CLI 활용]    

[Amazon Q Developer CLI로 가능한 것들]
1. AWS 리소스 생성, 삭제, 수정
2. 로그 조회 및 분석
3. 작업 스케줄링 설정
4. 어플리케이션 배포 
<br/>
   
(1) AWS에서 우분투 리눅스 EC2 한 개를 생성한 후 접속한다.   
<img width="600" alt="image1" src="https://github.com/user-attachments/assets/b4e3c26d-93b1-4d78-b191-ff9422ba2b2e" />
<br/><br/>
                
(2) 시스템 업데이트를 진행한다.   
명령어 (1) : apt update && apt upgrade -y     
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
<br/><br/>

(5) 아래 명령어로 Amazon Q Developer CLI 채팅을 시작하면 된다.   
명령어 (1) : q chat      
<img width="600" alt="image7" src="https://github.com/user-attachments/assets/de0d3cd3-ad2f-4d1a-ba69-c93378561bcf" />
<br/><br/>
