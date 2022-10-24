# 靡不有初，鲜克有终
# 开发时间：2022/3/18 11:32
# -*- coding: utf-8 -*-
import pandas as pd
import csv
import re
import time
import json
from urllib.request import urlopen
import urllib

# 原数据文件格式： 序号 + 起点纬度 + 起点经度 + 终点纬度 + 终点经度
origin_path = "C://Users//张晨皓//Desktop//无模型强化学习//data//起点终点坐标.txt"  # 原始坐标文件路径
result_path = "C://Users//张晨皓//Desktop//无模型强化学习//data//起终点距离.txt"  # 爬取数据文件保存路径

"""# 百度地图提供的api服务网址
"http://api.map.baidu.com/routematrix/v2/driving?output=json"  # 驾车(routematrix 批量算路)
'http://api.map.baidu.com/routematrix/v2/riding?output=json'  # 骑行
'http://api.map.baidu.com/routematrix/v2/walking?output=json'  # 步行
'http://api.map.baidu.com/direction/v2/transit?output=json'  # bus(direction路线规划)
"""

# 声明坐标格式,bd09ll(百度经纬度坐标);bd09mc(百度摩卡托坐标);gcj02(国测局加密坐标),wgs84(gps设备获取的坐标)
cod = r"&coord_type=bd09ll"

# AK为从百度地图网站申请的秘钥
AK = ['83C2EqcqH49Uunau00nU0sMAV5oSR9Hz']

dfBase = pd.read_csv(
    origin_path,
    sep=",",
)


dataList = []  # 储存获取的路线数据
akn = 0  # 使用第几个ak
for i in range(len(dfBase)):
    ID = i + 1
    print(i)
    ak = AK[akn]
    out_lat = dfBase.at[i, '起点纬度']
    out_lng = dfBase.at[i, '起点经度']
    des_lat = dfBase.at[i, '终点纬度']
    des_lng = dfBase.at[i, '终点经度']
    """
    # 获取驾车路径:常规路线规划(不考虑路况) 
    以下是可选参数
    #  tactics =10不走高速;=11常规路线;=12距离较短;=13距离较短
    """
    url_drive = r"http://api.map.baidu.com/routematrix/v2/driving?output=json&origins={0},{1}&destinations={2},{3}&{4}&tactics=11&ak={4}".format(out_lat, out_lng, des_lat, des_lng, ak)
    result_drive = json.loads(urlopen(url_drive).read())  # json转dict
    status_drive = result_drive['status']
    # print('ak秘钥：{0}  获取驾车路线状态码status：{1}'.format(ak, status_drive))
    if status_drive == 0:  # 状态码为0：无异常
        distance_drive = result_drive['result'][0]['distance']['value']  # 里程(米)
        timesec_drive = result_drive['result'][0]['duration']['value']  # 耗时(秒)
    elif status_drive == 302 or status_drive == 210 or status_drive == 201:  # 302:额度不足;210:IP验证未通过
        distance_drive = timesec_drive = 'AK错误'
        akn += 1
        ak = AK[akn]
    else:
        distance_drive = timesec_drive = '请求错误'

    dataList.append([ID, distance_drive, timesec_drive])

dfresult = pd.DataFrame(dataList, columns=['ID', 'distance', 'time'])
print(dfresult)

dfresult.to_csv(result_path, index=False)