from django.shortcuts import render

# Create your views here.

from PathVisualization.models import Logistics_Location


# Create your views here.

def showpath(request, orderid):
    record_list = Logistics_Location.objects.filter(dno=orderid)
    path_dot = []
    for i in range(len(record_list)):
        loc = record_list[i].dloc
        latlon = loc.split(",")
        lat = latlon[0]
        lon = latlon[1]
        path_dot.append((float(lat), float(lon)))
    return render(request, 'PathVisualization/path.html', {"path_dot": path_dot})

def showdata(request):
    heatmap = request.GET.get('heatmapdata')
    print('heatmapdata1=', heatmapdata)
    return render(request, 'path.html',{'heatmapdata': json.dumps(heatmapdata)} )
