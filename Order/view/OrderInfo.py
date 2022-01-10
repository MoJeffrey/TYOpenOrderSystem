"""
訂單詳情頁面
"""
import datetime
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Order.models.ItemModels import Item
from Order.models.OrderModels import Order
from PConceptOpenOrderSystem.settings import BASE_DIR

SavePath = os.path.join(BASE_DIR, "templates/static/images/PaymentVoucher")

@xframe_options_exempt
def index(request):
    OrderID = request.GET.get('OrderID')
    OrderInfo = Order().GetOrderInfo(OrderID)
    return render(request, "Order/OrderInfo.html", {"OrderInfo": OrderInfo})

def GetItemList(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        OrderID = request.POST.get('OrderID')
        ItemList = Item.GetOrderAllItem(OrderID)

        data = {
            "code": 0,
            'data': ItemList
        }

    return JsonResponse(data)

def DelItems(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        OrderID = request.POST.get('OrderID')
        DelList = request.POST.get('DelList').split(",")
        Item.DelItems(OrderID, DelList)

        data = {
            'status': "OK"
        }

    return JsonResponse(data)

def UploadPaymentVoucher(request):
    data = {
        'msg': '请检查填写的内容！'
    }

    if request.method == 'POST':
        img = request.FILES.get("file")
        OrderID = request.POST.get("OrderID")
        if img is not None:
            FileName = Order().SavePaymentVoucher(OrderID, img.name)
            destination = open(os.path.join(SavePath, FileName), 'wb+')

            for chunk in img.chunks():
                destination.write(chunk)
            destination.close()
    return JsonResponse(data)

def PaymentToChange(request):
    data = {
        'msg': '请检查填写的内容！'
    }

    if request.method == 'POST':
        OrderID = request.POST.get("OrderID")
        Payment = int(request.POST.get("Payment"))
        Order.PaymentToChange(OrderID, Payment)

    return JsonResponse(data)

def ShippingStatusToChange(request):
    data = {
        'msg': '请检查填写的内容！'
    }

    if request.method == 'POST':
        OrderID = request.POST.get("OrderID")
        ShippingStatus = int(request.POST.get("ShippingStatus"))
        Order.ShippingStatusToChange(OrderID, ShippingStatus)

    return JsonResponse(data)


def SaveMemo(request):
    """
    保存備忘
    :param request:
    :return:
    """
    data = {
        'msg': '请检查填写的内容！'
    }

    if request.method == 'POST':
        OrderID = request.POST.get("OrderID")
        Memo = request.POST.get("Memo")
        PaymentMemo = request.POST.get("PaymentMemo")
        ShippingMemo = request.POST.get("ShippingMemo")
        Order.SaveMemo(OrderID, Memo, PaymentMemo, ShippingMemo)

    return JsonResponse(data)

def DelOrder(request):
    data = {
        'msg': '请检查内容！'
    }
    if request.method == "POST":
        OrderID = request.POST.get('OrderID')
        if OrderID is not None:
            Order.objects.get(OrderID=int(OrderID[1:])).delete()
            data = {'status': 'OK'}
    return JsonResponse(data)
