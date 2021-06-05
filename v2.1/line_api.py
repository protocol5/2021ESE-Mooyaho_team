# -*- coding: cp949 -*- 

import requests, xmltodict, json
import pandas as pd


class API():
    def __init__(self, bus_id):
        super().__init__()

        key = 'BhRAUn32Inr%2FCjZHxRxcGkXhSps00YhpFe1QGWot6Jw89Yq65ZjVcUH59IJ8FiRMmE6u1I%2FAszW%2B7RNU1vThCg%3D%3D'
        url = "http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute?ServiceKey={}&busRouteId={}".format(key,bus_id)

        content = requests.get(url).content # GET요청
        dict=xmltodict.parse(content)
        jsonString = json.dumps(dict['ServiceResult']['msgBody']['itemList'], ensure_ascii=False) # dict을 json으로 변환
        jsonObj  = json.loads(jsonString)
        bus_info = pd.DataFrame(jsonObj)
        self.bus_info = bus_info[['station', 'stationNm', 'stationNo']]

    def getstationNm(self, index):
        return self.bus_info.iloc[index]['stationNm']

    def Nmtostation(self, index):
        return self.bus_info.iloc[index]['station']

    def stationNm(self, station):
        return self.bus_info[self.bus_info['station'] == str(station)].iloc[0][1]

        
if __name__ == '__main__':
    api = API(100100111)
    print(api.getstationNm(0))
    # print(api.stationNm(111001112))