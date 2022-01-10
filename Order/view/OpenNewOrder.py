"""
新增訂單
"""
import datetime

import django
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Order.models.ClientModels import Client
from Order.models.OrderModels import Order

@xframe_options_exempt
def index(request):
    OrderID = Order().GetNewOrderID()
    Date = datetime.datetime.now().strftime("%Y%m%d")
    return render(request, "Order/OpenNewOrder.html", {"OrderID": OrderID, "Date": Date})

def Create(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        OrderID = request.POST.get('OrderID')
        Date = request.POST.get('Date')
        Name = request.POST.get('Name')
        Address = request.POST.get('Address')
        Phone = request.POST.get('Phone')

        ClientID = Client().GetClientID(Name, Address, Phone)
        try:
            Order.CreateNewOrder(OrderID, Date, ClientID)
            data = {
                'status': "OK"
            }
        except django.db.utils.IntegrityError:
            data['msg'] = "不能重复單號！"

    return JsonResponse(data)

def GetClientList(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        Name = request.POST.get('Name')
        Phone = request.POST.get('Phone')

        ClientList = Client().GetClientList(Name, Phone)

        data = {
            "status": "OK",
            'data': ClientList,
        }

    return JsonResponse(data)
