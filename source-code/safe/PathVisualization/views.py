from django.shortcuts import render

# Create your views here.

from PathVisualization.models import Location, covid


# Create your views here.

def showpath(request, orderid):
    province_covid = covid.objects.filter(date='2021-12-19 00:00:00')
    heatmapdata = []
    for i in range(len(province_covid)):
        province = province_covid[i].place
        number = province_covid[i].number
        color = '#00FF00'
        if number >= 5:
            color = '#FF0000'
        elif number > 0:
            color = '#FFFF00'
        heatmapdata.append((province, color))
    dot_list = Location.objects.filter(dno=int(orderid))
    path_dot = []
    for i in range(len(dot_list)):
        loc = dot_list[i].dloc
        latlon = loc.split(",")
        lat = latlon[0]
        lon = latlon[1]
        path_dot.append((float(lat), float(lon)))
    return render(request, "PathVisualization/path.html",
                  context={'heatmapdata': heatmapdata, "path_dot": path_dot})
