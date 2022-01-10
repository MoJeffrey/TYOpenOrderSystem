"""
產品修改
"""
import os

import django
from django.db import IntegrityError
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.clickjacking import xframe_options_exempt

from PConceptOpenOrderSystem.settings import BASE_DIR
from Product.models import Product

ProductImgPath = os.path.join(BASE_DIR, "templates/static/images/Product")

@xframe_options_exempt
def index(request):
    ProductData = None
    if request.method == "GET":
        ID = request.GET.get('ID')
        if ID is not None:
            ProductData = Product.GetProduct(ID)
    return render(request, "Product/ProductEdit.html", {"Product": ProductData})

def Edit(request):
    data = {
        'msg': '请检查填写的内容！'
    }
    if request.method == "POST":
        Name = request.POST.get('Name')
        OldName = request.POST.get('OldName')
        Label = request.POST.get('Label')
        QuantityPerBox = request.POST.get('QuantityPerBox')
        PurchasePrice = request.POST.get('PurchasePrice')
        ProductID = request.POST.get('ProductID')
        HavePhoto = request.POST.get('HavePhoto')

        if (Name is not None
                and Label is not None
                and QuantityPerBox is not None
                and PurchasePrice is not None):

            try:
                Product.EditProduct(Name=Name,
                                    Label=Label,
                                    QuantityPerBox=QuantityPerBox,
                                    PurchasePrice=PurchasePrice,
                                    ProductID=ProductID)

                # 更改图片名称
                if HavePhoto == "True":
                    srcFile = os.path.join(ProductImgPath, OldName + ".jpg")
                    dstFile = os.path.join(ProductImgPath, Name + ".jpg")
                    try:
                        os.rename(srcFile, dstFile)
                    except FileNotFoundError:
                        pass

                data = {
                    'status': "OK"
                }

            except django.db.utils.IntegrityError:
                data = {
                    'msg': '注意產品名稱與標籤不能重複！'
                }

    return JsonResponse(data)
