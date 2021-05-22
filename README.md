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

1. **구현사항**

 - 공공 데이터 포털에서 제공하는 서울시 버스도착정보 API를 이용해 특정 버스 정류장에 도착하는 버스 및 버스가 도착하는 시간을 가져온다.
 - 도착하는 버스들의 번호를 클릭할 수 있는 버튼으로 만들어 클릭할 수 있도록한다.
 - 버스 번호를 선택하면 해당 버튼은 다시 누를 수 없도록 구현한다.
 - 해당 버스가 정류장을 통과하면 버튼은 다시 누를 수 있는 상태가 된다.

![image](https://user-images.githubusercontent.com/68097144/118111434-a67a8d00-b41e-11eb-9118-5527857e148e.png)



2. **구현해야할 사항**
  - 특정 정류장에서 도착할 수 있는 정류장들을 UI상에 띄우기
  - 정류장 선택 버튼 만들기
  - 정류장 선택시 해당 정류장에 도착하는 버스 중 가장 빠르게 오는 버스에 승차 신호 전송

3. **csv 파일**
  - bus_routd_id.csv는 버스의 번호와 그에 맞는 고유의 id가 저장
  - bus_stop_id.csv는 버스정류장의 고유 id, 고유 ARS번호,버스정류장 이름이 

----
## FALL - DETECTION PART
   

#### 기능 1 : fall-detection 구현

Yolov3-416 모델을 이용해 사람을 인식하고, 생성된 box의 너비와 높이 비율을 이용해 넘어짐을 감지한다.   

1. 영상   

https://user-images.githubusercontent.com/74461222/117812298-9a66c200-b29c-11eb-8c00-ee61b187bff4.mp4
<hr/>



#### 기능 2 : fall-detect가 5초 이상 지속될 때, 마지막 이미지 저장
기초 구현완료
   
<hr/>


#### 기능 3 : 저장된 이미지를 ftp 프로토콜을 이용해 라즈베리파이에 전송
기초 구현완료 
<hr/>   

#### 기능 4 : ftp 서버가 구축된 라즈베리파이에서 이미지파일을 새로 전송받거나 수정시간이 갱신될 때 이미지 팝업 띄우기
기초 구현완료
<hr/>

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
