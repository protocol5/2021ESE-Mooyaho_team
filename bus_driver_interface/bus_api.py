# -*- coding: cp949 -*- 

import requests, xmltodict, json
import pandas as pd
import server

class API():
    def __init__(self, bus_id, bus_No):
        super().__init__()

        bus_id = bus_id
        self.__bus_No = bus_No
        key = 'PNLQdi4%2Brx08vsestd7TMEB%2BGAOP2%2BlJopPQV6JY%2BTWk3FmfH6Iox8O%2F44voxMysl6Q5DNzm6jRBl4X%2Bnkp3oA%3D%3D'
        # key = 'BhRAUn32Inr%2FCjZHxRxcGkXhSps00YhpFe1QGWot6Jw89Yq65ZjVcUH59IJ8FiRMmE6u1I%2FAszW%2B7RNU1vThCg%3D%3D'
        self.__url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid?ServiceKey={}&busRouteId={}".format(key,bus_id)
        self.__index = -1

    def getbusinfo(self):
        content = requests.get(self.__url).content # GET요청
        dict=xmltodict.parse(content)
        jsonString = json.dumps(dict['ServiceResult']['msgBody']['itemList'], ensure_ascii=False) # dict을 json으로 변환
        jsonObj  = json.loads(jsonString)
        bus_info = pd.DataFrame(jsonObj)
        bus_info = bus_info[['dataTm', 'isrunyn', 'nextStTm', 'plainNo', 'sectOrd', 'sectionId', 'stopFlag', 'vehId']]
        return bus_info

    def targetinfo(self):
        bus_info = self.getbusinfo()
        self.target = bus_info[bus_info['plainNo'] == self.__bus_No]
        self.__index = self.target.index[0]

        if self.__index < len(bus_info) - 1:
            self.front = bus_info.iloc[self.__index+1]
            self.front = pd.DataFrame(self.front).T
        else: self.front = []
        if self.__index > 0:
            self.back = bus_info.iloc[self.__index-1]
            self.back = pd.DataFrame(self.back).T
        else: self.back = []
        # print(bus_info)
        # print(self.target)
        # print(self.front)
        # print(self.back)
        
        
if __name__ == '__main__':
    bus = '1227'
    s = server.SQL()
    s.connect()
    api = API(s.num_to_uid(bus), '서울74사6219')
    print(api.getbusinfo())