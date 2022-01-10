"""
添加訂單產品
"""

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Order.models.ItemModels import Item

@xframe_options_exempt
def index(request):
    return render(request, "Order/AddItem.html")

def Add(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        OrderID = request.POST.get('OrderID')
        Name = request.POST.get('Name')
        Num = request.POST.get('Num')
        Price = request.POST.get('Price')
        Item.AddItem(OrderID, Name, Num, Price)

        data = {
            'status': "OK"
        }

    return JsonResponse(data)

def GetItemList(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        Name = request.POST.get('Name')

        ItemList = Item().GetItemList(Name)

        data = {
            "status": "OK",
            'data': ItemList,
        }

    return JsonResponse(data)
