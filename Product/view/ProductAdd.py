"""
商品添加
"""
import django

from django.db import IntegrityError
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from Product.models import Product

@xframe_options_exempt
def index(request):
    return render(request, "Product/ProductAdd.html")

def Add(request):
    data = {
        'msg': '请检查填写的内容！'
    }
    if request.method == "POST":
        Name = request.POST.get('Name')
        Label = request.POST.get('Label')
        QuantityPerBox = request.POST.get('QuantityPerBox')
        PurchasePrice = request.POST.get('PurchasePrice')

        if (Name is not None
                and Label is not None
                and QuantityPerBox is not None
                and PurchasePrice is not None):

            try:
                Product.AddProduct(Name=Name,
                                   Label=Label,
                                   QuantityPerBox=QuantityPerBox,
                                   PurchasePrice=PurchasePrice)

                data = {
                    'status': "OK"
                }

            except django.db.utils.IntegrityError:
                data = {
                    'msg': '注意產品名稱與標籤不能重複！'
                }

            except django.db.utils.DataError:
                data = {
                    'msg': '注意產品名稱不能包含emoji！'
                }

    return JsonResponse(data)
