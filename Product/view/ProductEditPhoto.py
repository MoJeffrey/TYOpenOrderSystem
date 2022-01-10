"""
產品圖片修改
"""
import os
import shutil

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
    return render(request, "Product/ProductEditPhoto.html", {"Product": ProductData})

def ImgUpload(request):
    data = {
        'msg': '请检查填写的内容！'
    }

    if request.method == 'POST':
        img = request.FILES.get("file")
        Name = request.POST.get('Name')
        HavePhoto = request.POST.get('HavePhoto')

        # 删除旧文件
        if HavePhoto == "True":
            os.remove(os.path.join(ProductImgPath, Name + ".jpg"))

        if img is not None:
            destination = open(os.path.join(ProductImgPath, Name + ".jpg"), 'wb+')
            for chunk in img.chunks():
                destination.write(chunk)
            destination.close()

        data = {'code': 0}
    return JsonResponse(data)
