"""
查看產品詳情
以及修改
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Product.models import Product

import re

@xframe_options_exempt
def index(request):
    ProductData = None
    if request.method == "GET":
        ID = request.GET.get('ID')
        if ID is not None:
            ProductData = Product.GetLabelAndDetails(ID)
    return render(request, "Product/SeeOrEditToLabelAndDetails.html", {"Product": ProductData})

def Edit(request):
    data = {
        'msg': '请检查填写的内容！'
    }
    if request.method == "POST":
        Label = request.POST.get('Label')
        Details = request.POST.get('Details')
        ProductID = request.POST.get('ProductID')

        # 删除emoji
        try:
            co = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

        Details = co.sub('', Details)

        if (Label is not None
                and Details is not None):

            Product.EditProductDetails(Label=Label,
                                       Details=Details,
                                       ProductID=ProductID)
            data = {
                'status': 'OK！'
            }

    return JsonResponse(data)
