# 한 달간 버스 승하차 정보를 바탕으로 도착할 수 있는 정류장의 하차 내림차순 정령

import csv
import requests, xmltodict, json
import pandas as pd



busstop_id = 105000102 #서울시립대학교 앞

##########################################################

########################33 버스 정류장의 버스를 가져오는 부분####################################
bus_array = []
bus_array_rtnm = []

key = "gHcpum2l%2Bw3H75tj8jtT%2BsZ7MSiSpkzn1FlH0mpM4meW1yoDcQmtZv0T5XiDOYXqV5kGvwVi5Rdu7p%2FiJBuezg%3D%3D"

url = "http://ws.bus.go.kr/api/rest/arrive/getLowArrInfoByStId?ServiceKey={}&stId={}".format(key, busstop_id)
content = requests.get(url).content
dict = xmltodict.parse(content)
jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
jsonObj = json.loads(jsonString)

for i, item in enumerate(jsonObj['itemList']):
    bus_array.append(item['busRouteId'])
    bus_array_rtnm.append(item['rtNm'])
print('bus_array', bus_array)
##################################################################################################################

############################ 버스 정류장 정렬하는 부분
f = open('may.csv', 'r', encoding="euc-kr")
rdr = csv.reader(f)
fd = open('output1.csv','w')
wr = csv.writer(fd)

for i , line in enumerate(rdr):
    if i == 0 :
        wr.writerow(line)
    if line[1] in bus_array_rtnm:
        wr.writerow(line)

f.close()
fd.close()
############################3 버스 정류장에 도착하는 버스들의 정류장만 추출 완료

###########################같은 정류장의 하차객 수 더하기

f = open('output1.csv', 'r')
rdr = csv.reader(f)
fd = open('output2.csv','w')
wr = csv.writer(fd)

sum = 0
bus_stop_id = ''
bus_stop_ars = ''
bus_stop_name = ''
array = []

arrr = ['bus_stop_id', 'bus_stop_ars', 'bus_stop_name', 'sum']

for i, line in enumerate(rdr):
    if i == 0 :
        wr.writerow(arrr)

    else :
        if i ==1 :
            bus_stop_id = line[3]
            bus_stop_ars = line[4]
            bus_stop_name = line[5]

        if bus_stop_id == line[3]:
            sum += int(line[7])

        else :
            array.append(bus_stop_id)
            array.append(bus_stop_ars)
            array.append(bus_stop_name)
            array.append(sum)
            wr.writerow(array)
            array = []
            bus_stop_id = line[3]
            bus_stop_ars = line[4]
            bus_stop_name = line[5]
            sum = int(line[7])

f.close()
fd.close()
#output2 => 해당 버스 정류장을 지나는 버스가 도착하는 정류장만 있음
##############################################

###### 이 정류장 이후의 정류장만 api를 이용해 추출하는 부분


key = "YCw62AJ77rUCLVLmI%2BrkReS65%2F5H4XavS%2BIVCLqjeDLq9MaS9v2BkixjD1xgDBvFG%2F6MvUlcmJ44d1PGxruD4A%3D%3D"
bus_stop_array = []
for i, bus_id in enumerate(bus_array) :

    flag = 0
    url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?serviceKey={}&busRouteId={}".format(key, bus_id)
    content = requests.get(url).content
    dict = xmltodict.parse(content)
    jsonString = json.dumps(dict['ServiceResult']['msgBody'], ensure_ascii=False)
    jsonObj = json.loads(jsonString)

    for i, item in enumerate(jsonObj['itemList']):
        if item['station'] == str(busstop_id):
            flag = 1
            continue
        if flag == 1 :
            if item['station'] in bus_stop_array :
                continue
            else :
                bus_stop_array.append(item['station'])

print(bus_stop_array)

# bus_stop_array 에는 현재 버스정류장에서 갈 수 있는 정류장들만 나타남

# 이제 마지막으로 output2에서 갈 수 있는 정류장들만 추린다.

f = open('output2.csv', 'r')
rdr = csv.reader(f)
fd = open('output3.csv', 'w')
wr = csv.writer(fd)

for i , line in enumerate(rdr):
    if i == 0 :
        wr.writerow(line)
    if line[0] in bus_stop_array :
        wr.writerow(line)

f.close()
fd.close()

##########################3 정렬 완료 이제 내림차순 정렬해서 사람이 뽑기만 하면 됨

df = pd.read_csv('output3.csv',encoding='utf8') 
df1 = df.sort_values(by = 'sum', ascending=False)
df1.to_csv('result.csv')