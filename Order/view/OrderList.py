"""
处理訂單列表
"""
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Order.models.OrderModels import Order

@xframe_options_exempt
def index(request):
    return render(request, "Order/OrderList.html")

def GetOrderList(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        Key = request.POST.get('Key')
        DataDisplay = request.POST.get('DataDisplay')
        page = request.POST.get('page')
        limit = request.POST.get('limit')
        OrderList, Count = Order().GetOrderList(Key, DataDisplay, page, limit)

        data = {
            "code": 0,
            'data': OrderList,
            'count': Count
        }

    return JsonResponse(data)
