from django.shortcuts import render
import datetime
# Create your views here.

from PathVisualization.models import GeographicInformation, PandemicInformation


# Create your views here.

def getdata(request, orderid):
    '''
        需要在自己的safe数据库的GeographicInformation表加入几条数据
        若订单号为01，运行：
        http://127.0.0.1:8000/pathvisualization/path/01
    '''
    province_covid = PandemicInformation.objects.filter(date__contains=datetime.date(2021, 12, 19))
    heatmapdata = []  #('北京市','#FFFF00')
    for x in province_covid:
        province = x.place
        number = x.number
        # color = '#00FF00'
        if number >= 5:
            color = '#ff9900'
        elif number > 0:
            color = '#FFFF00'
        heatmapdata.append((province, color))
    dot_list = GeographicInformation.objects.filter(dno=int(orderid))
    # path_dot = []
    path_dot = [("112.368904","39.913423"), ("116.382122","39.901176"), ("116.387271","39.912501"), ("118.398258","39.904600")]
    for i in range(len(dot_list)):
        loc = dot_list[i].dloc
        latlon = loc.split(",")
        lat = latlon[0]
        lon = latlon[1]
        path_dot.append((str(float(lat)), str(float(lon))))
    '''
        path_dot格式：
        [(31.498294737149,120.37330074071), (31.498294737149,121.37330074071)]
        heatmapdata格式：
        [(上海,#FFFF00), (北京,#FFFF00)]
        查看源码后发现前端可以正常取出字段，但展示不出来
        效果可参考nodatabase.html
    '''
    return render(request, "PathVisualization/withdatabase.html",
                  context={'heatmapdata': heatmapdata, "path_dot": path_dot})
