# -*- coding: utf-8 -*-

import mysql.connector
import random

#造出两组数据
pointArr1 = [{lng: 120.37330074071, lat: 31.498294737149}, {lng: 120.57330074071, lat: 31.498294737149},
            {lng: 120.87330074071, lat: 31.498294737149}, {lng: 121.37330074071, lat: 31.498294737149}]
pointArr2 = [{lng: 113.39505673967, lat: 22.94738905789}, {lng: 120.57330074071, lat: 31.498294737149},
            {lng: 112.830583950802, lat: 34.27474928498}, {lng: 116.46473277246, lat: 39.934649603730}]

datetime1 = ["2021-12-19 14:00:00 ", "2021-12-20 07:34:12", "2021-12-20 19:46:95", "2021-12-21 13:23:37"]
datetime2 = ["2021-11-15 19:30:00 ", "2021-11-18 20:34:54", "2021-11-21 09:43:26", "2021-11-24 13:24:49"]

#将输入的物流订单输入到变量deliverorder
deliverorder = dno

#物流订单号奇偶数
if deliverorder % 2 == 0:
    for i in range(4):
        dno = dno
        dloc = pointArr1[i]
        dupdate = datetime1[i]
else:
    for i in range(4):
        dno = dno
        dloc = pointArr2[i]
        dupdate = datetime1[i]