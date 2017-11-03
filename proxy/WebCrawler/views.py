from .models import ProxyMessage
from django.http import HttpResponse
from background_task import background
from background_task.models import Task
import random
import json
# 爬虫部分导入
from .Crawlers import main

# 定时爬虫任务
@background(schedule=60*60*6)  # 六个小时启动一次
def _getMore():
    main._IP_Clear()
    if ProxyMessage.objects.count() < 50:
        one = main.GetProxy()
        one.GETMORE()
    if Task.objects.count() < 1:
        _getMore()

# Create your views here.
def getMore(request):
    if ProxyMessage.objects.count() == 0:
        one = main.GetProxy()
        one.GETMORE()
    if Task.objects.count() < 1:
        _getMore()
        return HttpResponse("It will run.")
    else:
        return HttpResponse("It's running.")

def getJson(request, Type):
    data = ProxyMessage.objects.filter(Type=Type)[random.randint(0, ProxyMessage.objects.filter(Type=Type).count() - 1)]
    while not main._IP_Test(data):
        data.delete()
        data = ProxyMessage.objects.filter(Type=Type)[random.randint(0, ProxyMessage.objects.filter(Type=Type).count() - 1)]
    return HttpResponse(json.dumps({"IP":data.IP,"Area":data.Area,"Port":data.Port,"Type":data.Type,"Address":data.Address}))
