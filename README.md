# **2021ESE-Mooyaho_team**
Mooyaho(It's that much fun) team's project repos. Lecture is 2021 Embedded Systems and Experiment.

---
## What is ***Bus - No Stop  prevention System*** ?

### 1. **Architectures**
![image](https://user-images.githubusercontent.com/68097267/119214887-2088d100-bb05-11eb-9727-e45ee50fafc5.png)

![image](https://user-images.githubusercontent.com/68097267/119214895-2da5c000-bb05-11eb-8982-121555db8a86.png)

![image](https://user-images.githubusercontent.com/68097267/119214932-680f5d00-bb05-11eb-9691-f054c56bde27.png)

### 2. **Introduction**
 무정차 방지 및 승객의 안전을 고려한 사용자 친화적인 정류장 승차 시스템은 버스를 이용하는 이용객과 버스 기사들의 편의성과 안전을 제공하는 시스템이다. 무정차 문제를 해결하기 위해 이용객은 해당 시스템을 이용하며 시스템에 지정된 번호를 통해 가장 가까운 버스에 해당 버스를 이용할 이용객이 있음을 알린다. 또한, 이미지 인식을 통해서 이용객의 안전을 파악하고 가까운 공공기관에 사고 알림을 알리게 된다. 이를 통해서 도심 외곽 쪽에서 계속 대두되는 문제인 무정차 문제와 일반적으로 취약한 치안 문제를 동시에 해결하고자 한다. 시스템은 기준 이하의 전송속도를 가지며 UX를 고려해 직관적이고 간단한 인터페이스를 제공한다.

---

## Bus stop Interface

### 버스 정류장 인터페이스 구현

# Bus stop Interface
### 버스 정류장 인터페이스 구현

#### 구현사항

 - 공공 데이터 포털에서 제공하는 서울시 버스도착정보 API를 이용해 특정 버스 정류장에 도착하는 버스 및 버스가 도착하는 시간을 가져온다.
 - 도착하는 버스들의 번호를 클릭할 수 있는 버튼으로 만들어 클릭할 수 있도록한다.
 - 버스 번호를 선택하면 해당 버튼은 다시 누를 수 없도록 구현한다.
 - 해당 버스가 정류장을 통과하면 버튼은 다시 누를 수 있는 상태가 된다.
 - 특정 정류장에서 도착할 수 있는 정류장들을 UI상에 띄우기
 - 정류장 선택 버튼 만들기
 - 정류장 선택시 해당 정류장에 도착하는 버스 중 가장 빠르게 오는 버스에 승차 신호 전송


설문조사 및 피드백을 참고해서 UI 다시 
- 버스 버튼 클릭 시 음성이 출력되도록 수정(버스 버튼 클릭 시, 버스 취소 시, 운행종료 버스 선택 시)
- 버튼 클릭 및 클릭되지 않은 것을 한눈에 알아볼 수 있도록 수정
- UI의 위쪽에 도움말 추가
![0618](https://user-images.githubusercontent.com/68097144/122436974-3ab6b180-cfd4-11eb-96d1-9cd270b08cd0.png)

#### csv, xml files
  - bus_routd_id.csv는 버스의 번호와 그에 맞는 고유의 id가 저장
  - bus_stop_id.csv는 버스정류장의 고유 id, 고유 ARS번호,버스정류장 이름이 저장됨
  - bus_stop.xml 파일에는 특정 버스정류장에서 출력할 버스정류장들의 id가 들어감
#### python files
  - bus_stop_interface.py는 버스 정류장 인터페이스 소스코드. 필요한 모듈 설치 후 python3로 해당 파일 실행 시 버스 정류장 인터페이스 실행
  - 한 달간 버스 승하차 정보를 바탕으로 도착할 수 있는 정류장으 히차객 내림차순 정렬
#### voice flies
  - 버스 정류장 인터페이스에서 버튼 클릭 시 출력될 음성들 버스 버튼 선택, 버스 버튼 취소, 운행 종료 시 
#### png files
  - 버스 정류장 인터페이스 구현에 사용되는 이미지 파일들
  - end_bus.png, push_button.png , pop_button.png는 버스번호 버튼에서 사용되는 이미지
  - bus_stop_list.png는 버스 정류장 버튼에 사용되는 이미지 파일


----
## FALL - DETECTION PART
   


**1. Fall-Detection 개요**   
도심 외곽지역의 이용객이 적은 정류장을 이용하는 승객의 안전을 보장하기 위해 쓰러짐을 감지하는 시스템을 의미한다. 알고리즘 진행은 다음과 같다. 카메라를 통해 얻어온 이미지에서 인공지능 모델을 이용해 사람을 감지하고, 추가적인 내부 연산을 통해 사람이 쓰러졌음을 판단한다. 그 다음, 일정 시간동안 쓰러짐이 유지되면 SFTP 프로토콜을 이용해 서버에 이미지를 전송하고, 버스 API를 이용해 해당 정류장에 가장 먼저 도착 예정인 버스의 정보(UID 등)을 얻은 후, DB에 접근해 해당 버스의 FALL-D SIG 플래그를 올린다. 버스 기사 단말기는 서버에 주기적으로 접속해 FALL-D SIG가 올라가 있다면 서버에 저장된 이미지를 받아와 팝업을 띄운다. 이를 통해 버스기사는 사고 발생 현장을 제일 먼저 목격하고 조치를 취하도록 유도한다.
   
   
**2. 알고리즘 구현**   
Fall-Detection 기초 구현과 이미지 전송 과정을 알고리즘 진행 순서대로 설명한다.

**가) 객체 인식**
웹캠에서 실시간으로 얻어오는 이미지들을 Yolov3-416 사물인식 인공지능 모델을 이용해 객체들을 인식한다. 최종적으로는 사람, 자전거, 개, 휴대전화 등등 무수히 많은 사물이 인식된다. 하지만 Fall-detection 알고리즘에서 필요한 객체는 사람뿐이므로, 사람 이외에 인식된 모든 객체들은 무시하고, 오직 사람에 대해서만 ROI 박스가 그려지게 수정했다. 아래 사진 중 왼쪽이 수정 전, 오른쪽이 수정 후이다.   
![image](https://user-images.githubusercontent.com/74461222/119269316-0dbfea80-bc32-11eb-8541-902da8b4a0c6.png)![image](https://user-images.githubusercontent.com/74461222/119269326-16b0bc00-bc32-11eb-9f17-d10e4acc39b4.png)


**나) 쓰러짐 인식**   
인공지능 모델을 이용해 얻은 사람의 ROI 박스 크기를 참조해 쓰러짐을 판별한다. 박스의 width를 height로 나눈 값이 1.1보다 크다면 사람이 쓰러진 상태라고 판단한다. 즉, 사람에 그려진 박스가 가로로 넓어진다면 쓰러진 상태라고 판단하는 것이다.   
![image](https://user-images.githubusercontent.com/74461222/119269364-4f509580-bc32-11eb-819b-c03f5e072a9b.png)![image](https://user-images.githubusercontent.com/74461222/119269367-52e41c80-bc32-11eb-9cd5-c2cb3017dc27.png)   

**다) 쓰러진 이미지 저장**   
사람이 쓰러져있는 이미지를 버스 기사 단말기에 보내기 위해서는 먼저 젯슨 보드 내에 이미지를 저장할 필요가 있다. 그러나 쓰러짐이 감지되었을 때 바로 이미지를 저장하고 전송한다면, 넘어진 상태가 아닌데 잘못 인식했을 경우가 있을 수 있다.   
![image](https://user-images.githubusercontent.com/74461222/119269449-bc642b00-bc32-11eb-9001-81a08154eb25.png)   
카메라 1대로는 쓰러짐이 인식이 안되는 경우가 있었다. 이를 해결하기 위해 다음과 같이 각각 다른 높이, 각도로 설치된 2대의 카메라를 통해 쓰러짐을 감지하도록 구현했다.

<img src = "https://user-images.githubusercontent.com/74461222/122674215-1266c700-d20f-11eb-9793-469281700c98.png" width="300" height="300"><img src = "https://user-images.githubusercontent.com/74461222/122674218-17c41180-d20f-11eb-9c92-9ef5291be2e9.png" width="300" height="300">



위 사진처럼 사람이 카메라 앞으로 가까이 지나가서 ROI 박스의 가로가 넓게 측정될 수도 있으므로, 쓰러짐이 지속적으로 감지될 때부터 진짜 사고가 일어났다고 인지한다. 따라서 쓰러짐이 6초 이상 감지될 때부터 이미지를 젯슨 보드 내에 저장하도록 하는 기능을 추가했다. 이 때, 이미지는 계속 한 파일에 덮어씌운다. 6초 이상을 기준으로 한 이유는, 한 장의 이미지가 Yolov3-416 모델을 통해 객체 인식이 될 때의 시간이 약 0.6초(평균 fps = 1.67) 걸렸기 때문이다. 즉, 최소 이미지 10장이 처리될 동안 쓰러짐이 유지된다면, 젯슨 보드 내에 해당 이미지가 지속적으로 저장된다.

**라) 이미지 전송**   
젯슨 보드 내에 저장된 이미지를 서버에 전송하기 위해서 SSH 파일 전송 프로토콜(Secure File Transfer Protocol, SFTP)을 이용한다.
기본적인 전송 과정은 다음과 같다. 쓰러짐이 지속되어 이미지가 덮어씌워져 저장된다면, 해당 이미지의 수정시간이 갱신될 것이다. 만약 수정시간이 갱신되었다면, 쓰러짐이 새로 발생했다는 의미이므로, 해당 이미지를 SFTP 프로토콜을 이용해 웹서버에 전송한다. 이후, 무한루프에 빠지게 되어 젯슨 내의 이미지 파일의 수정시간이 갱신될 때까지 기다린다. 이 과정을 무한히 반복하게 된다. 


**마) DB 접근 후, FALL-D SIG 플래그 수정**   
쓰러짐이 지속적으로 발생해서 이미지를 서버로 전송한 후, 가장 가까운 버스에게 쓰러짐 이미지를 받아가야 한다는 신호를 주어야 한다. 이것을 위해 웹서버 DB에 FALL-D SIG라는 플래그를 추가한 상태이다.
젯슨 보드는 쓰러짐 이미지를 클라우드 서버에 전송한 후, 버스 API를 이용해 해당 정류장에 가장 가까이 있는 버스에 대한 정보(UID 등)을 얻어온다. 이후, DB에 접근해 가장 가까이 있는 버스의 FALL-D SIG를 해당 버스 UID로 올린다. 그리고 쓰러짐이 감지되지 않는다면 해당 플래그를 0으로 다시 내린다. 이 기능을 구현한다면, 추후에 버스 기사 단말기가 서버에 접근해서 FALL-D SIG가 올라갔을 때 쓰러짐 이미지를 받아갈 수 있을 것이다.


**3. Fall-Detection 구현 영상**      
여러 가지 상황에서의 Fall-Detection 시연 영상을 촬영했다.

**가) 카메라 2대를 이용한 쓰러짐 인식**


https://user-images.githubusercontent.com/74461222/122674640-10056c80-d211-11eb-99fb-4cca2b2cefa2.mp4


**나) 여러 사람이 있을 때 쓰러짐 인식**


https://user-images.githubusercontent.com/74461222/122674651-185da780-d211-11eb-9135-6a6fe88a7da6.mp4


**다) 야간 상황에서의 쓰러짐 인식**


https://user-images.githubusercontent.com/74461222/122674659-214e7900-d211-11eb-891e-0c914185a4a5.mp4


----


## GCP Web Server

### What is GCP Web Server?
**1. GCP 웹 서버 및 데이터베이스 개요**
GCP(Google Cloud Platform)을 이용한 클라우드 웹 서버를 구축하였다. GCP를 이용한 웹서버 구축은 경제성, 유지보수성, 보안성, 복구성(Server Recovery)가 유리하다는 장점이 있다. 구축된 웹서버는 무정차 방지 전체 시스템에서 필요로 하는 버스 UID(Unique ID), 버스정차 시그널(flag), Fall-Detection 시그널(flag) 데이터들을 관리하는 데이터 베이스내용이 포함하고 있다.

**2.웹 서버 인프라스트럭처(Infrastructure) 및 플랫폼(Platform) 구축**
GCP는 인프라스트럭처와 플랫폼 구축이 쉽고 간편하다. 먼저 GCP 컴퓨터 엔진 인스턴스 즉, 인프라스트럭처를 아래 그림과 같이 사용자가 구축하고자하는 시스템 목적에 맞는 리소스에 맞춰 인스턴스를 구축할 수 있다. 

**3.데이터베이스 구축**
데이터 베이스는 Mysql 5.7을 사용하여 구축하였다. 데이터베이스의 구성은 bus_info database안에 bus_info table을 가지고 있다. 아래 사진과 같이 bus_info 초기 데이터베이스는 list넘버, 버스번호, 버스UID, 정차신호 플래그, 데이터 업데이트 날짜 순으로 예제 데이터를 가지고 있다.

![image](https://user-images.githubusercontent.com/68097267/119213926-d0f2d700-bafd-11eb-908c-0989c0942092.png)
![image](https://user-images.githubusercontent.com/68097267/119213927-d2bc9a80-bafd-11eb-8460-49669e37250e.png)

 bus_info 데이터베이스는 실제 버스UID 정보와 클라이언트들이 요구되는 추가적인 데이터 정보에 따라 수정이 가능하며, 아래 그림과 같이 CSV파일을 통해 얻은 실제 버스들의 정보들을 매크로 형식 dump의 데이터 정보를 불러와 데이터베이스를 새로 구축할 수 있도록 하였다.
 
 ![image](https://user-images.githubusercontent.com/68097267/119213931-dbad6c00-bafd-11eb-813c-ca99e458e0f4.png)

**4.웹 데이터베이스 매니저 구축**
웹 DB 비전문가 관리자도 손 쉽게 DB를 관리할 수 있도록 웹 데이터베이스 매니저를 구축하였다. 기본적으로 PHP로 구축되어있으며, Mysql API를 통해 데이터베이스에 접근할 수 있도록 하였다. 데이터 기본 처리기능인 CRUD(Create, Read, Update, Delete)기능이 ‘add.php’, ‘list.php’, ‘edit.php’, ‘delete(기능)’형태로 제공되고 있다.

![image](https://user-images.githubusercontent.com/68097267/119213940-f1229600-bafd-11eb-8ac2-167bfe5402dc.png)
![image](https://user-images.githubusercontent.com/68097267/119213947-fa136780-bafd-11eb-91be-19e4727d0b0c.png)
![image](https://user-images.githubusercontent.com/68097267/119213949-fb449480-bafd-11eb-9b37-2347afe520af.png)

edit과 add, list 조회는 ‘gcp-ip/bs/login.php’ URI를 통해서 로그인세션을 통과한 후에 접근할 수 있도록 하였고, 로그인이 되지 않은 상태에서 add, edit, list URI를 통해 접근 시 아래 그림과 같은 login 세션으로 리디렉션한다. 또한, edit과 add과정을 거치지 않고 update, insert 메소드 과정에서 URI로 접근시 Wrong access!메시지를 나타낸다.

![image](https://user-images.githubusercontent.com/68097267/119213955-04356600-bafe-11eb-9352-a62621045fb6.png)
![image](https://user-images.githubusercontent.com/68097267/119213958-0697c000-bafe-11eb-8ade-f7de075af813.png)

**5.Mysql Database API를 이용한 DB매니징**
각 클라이언트(bus-stop, bus driver, fall-detection 모듈)에서는 ‘PyMysql’ 파이썬 클라이언트 라이브러리를 이용하여 웹서버 DB에 접근하여 CRUD 과정을 진행한다. 

API는 [PyPI](https://pypi.org/project/PyMySQL/)에서 제공하는 매뉴얼을 참조하였다.

### How To Use This Branch Files?

1. 먼저 DB관리를 하기 위한 ***데이터베이스 관리 시스템이 설치*** 되어야 한다. 본 파일은 [MySql](https://www.mysql.com/) 기준으로 구축되었다.
2. *bus_db* 폴더에서 아래와 같이 입력한다.
```
$ mysql -u root -p < bus_info.sql
```
3. 데이터베이스가 제대로 import되었는지 확인 후, mysql을 종료한다.
```
> show databases;
> use bus_info;
> show tables;

...

> exit;
```
4. *web_db_manager* 폴더의 내용을 다음 경로에 옮기고, 폴더 명을 변경한다.
> 폴더 저장 PATH : /var/www/html
```
$ sudo mv ./web_db_manager ./bs
```
5. 폴더 내의 .php 파일들은 mysql DB에 API를 통해 접속한다. 이때, 그림과 같이 U와 P 부분을 DB username 과 password로 바꿔준다.

![image](https://user-images.githubusercontent.com/68097267/119214511-61331b00-bb02-11eb-9d8a-4dcb91b3b1e7.png)

6. 다음 URL로 접근하여 출력되는지 확인한다.
> Server Static IP/bs/login.php

> Server Static IP는 서버 고정 아이피를 뜻한다.

---
## Bus Driver Interface

### 구현사항
서버에 업데이트 된 데이터를 바탕으로 버스 드라이버 인터페이스에 갱신된 데이터를 바탕으로 UI를 출력하는 시스템 구현을 목표로 한다. 구현되어야 하는 시스템은 크게 이미지 출력, 신호 출력, 데이터 가져오기가 있다. 데이터는 웹 서버에서 가져와야 하는데 아직 웹 서버가 구축 중이기 때문에 데이터 송/수신을 웹 서버와의 통신이 아니라 소켓 통신을 이용하여 기본적인 기능을 갖춘 서버와 클라이언트 사이에서 통신을 진행하고 이를 기반으로 이미지와 신호(메시지) 등을 출력하거나 팝업 하는 기능을 구현하였다.

- 쓰레드를 이용한 서버 - 클라이언트 소켓 통신
- 클라이언트에서 서버로 메시지 송신 시스템 및 UI
- 클라이언트에서 메시지로 이미지 요청 시 서버에서 해당 이미지 전송 및 클라이언트 창에서 팝업

![1](https://user-images.githubusercontent.com/72551588/119267850-49a38180-bc2b-11eb-9223-7e9439537f84.jpg)
server와 client 디렉토리에 있는 windows를 실행하면 사진과 같은 UI가 출력된다. 사진에서 보이는 것 처럼 왼쪽은 서버, 오른쪽은 클라이언트이다. 서버 UI에서 먼저 할당할 수 있는 IP와 PORT 번호를 입력하고 실행하면 정상적인 IP와 PORT 번호가 입력되었을 때 서버가 실행되면서 **[서버실행]** 버튼이 **[서버종료]** 버튼으로 바뀌게 된다.
실행한 서버에 입력된 IP와 PORT 번호를 클라이언트에 입력하여 **[서버접속]** 버튼을 누르면 사진과 같이 **[접속종료]** 버튼으로 바뀌게 되고 서버에는 접속한 클라이언트의 IP와 PORT 번호가 들어오게 된다. 이를 사용자가 원하는 대로 출력해서 사진과 같이 출력할 수 있게 했다.

![2](https://user-images.githubusercontent.com/72551588/119267852-4d370880-bc2b-11eb-95aa-cc39ff5a70b3.jpg)
연결된 상태에서는 클라이언트에서 메시지를 서버에 송신할 수 있다. 서버에 수신된 메시지가 일반적인 메시지라면 다시 클라이언트에 그 메시지를 보내주고 클라이언트는 정상적으로 수신이 되었다면 해당 메시지를 **받은 메시지**창에 띄워준다. 만약에 이미지 파일을 요청한다면 _(ex: 'abc.jpg')_ 해당 이미지가 서버에 존재한다면 그 이미지를 전송해준다. 클라이언트는 이미지가 정상적으로 전송이 된다면 이를 사진과 같이 팝업창으로 출력해준다.

### 구현해야 할 사항
- 새로 구현하는 시스템에 적합한 버스 기사 UI 구축
- 소켓 통신으로 데이터 전송이 아닌 웹 서버에서 데이터를 가져오는 클라이언트 구축
- 데이터를 기반으로 출력해야 하는 신호 또는 이미지를 버스 기사 인터페이스에 출력
- 승차벨 신호, 정류장 상황 이미지, 예외 상황에 따라 출력되는 이미지가 변하도록 수정
- 버스 공공 데이터(API)를 활용한 앞/뒤차 거리 출력

