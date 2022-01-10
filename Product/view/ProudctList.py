"""
处理產品列表的事務
"""
import json
import django

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Product.models import Product


@xframe_options_exempt
def index(request):
    return render(request, "Product/ProductList.html")

def GetProductList(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        Key = request.POST.get('Key')
        SellPrice = float(request.POST.get('SellPrice'))
        page = request.POST.get('page')
        limit = request.POST.get('limit')
        ShowAll = request.POST.get('ShowAll')
        ProductList, Count = Product.GetProductList(Key, SellPrice, page, limit, ShowAll)

        data = {
            "code": 0,
            'data': ProductList,
            'count': Count
        }

    return JsonResponse(data)

def ExcelAdd(request):
    data = {
        'msg': '请检查内容！'
    }
    if request.method == "POST":
        data = request.POST.get('data')
        if data is not None:
            dataJson = json.loads(data)
            try:
                ChangeScore, SaveNewProduct = Product.BatchAddProduct(dataJson)
                data = {
                    "status": "OK",
                    "SaveNewProduct": SaveNewProduct,
                    "ChangeScore": ChangeScore,
                }
            except django.db.utils.ProgrammingError as e:
                data = {
                    'msg': '請檢查名稱是否包含特殊符號！' + repr(e)
                }

    return JsonResponse(data)

def Del(request):
    data = {
        'msg': '请检查内容！'
    }
    if request.method == "POST":
        DelList = request.POST.get('DelList')
        if DelList is not None:
            print(str(DelList))
            Product.DelProducts(DelList.split(","))
            data = {'status': 'OK'}
    return JsonResponse(data)
