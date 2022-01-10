"""
批量添加商品
用于直接复制資料
自動識別
添加數據庫
"""
from itertools import groupby

import django
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Order.models.ItemModels import Item


@xframe_options_exempt
def index(request):
    return render(request, "Order/AutomaticIdentification.html")

def Distinguish(request):
    data = {
        "code": 1,
        'msg': "發生錯誤"
    }
    if request.method == "POST":
        OrderID = request.POST.get('OrderID')
        AddItemsListStr = request.POST.get('AddItemsListStr')
        if AddItemsListStr != "" and AddItemsListStr is not None:
            ItemsList = AnalyzeAddItemsList(AddItemsListStr).GetItemsList()

            try:
                Item().BatchAddItem(OrderID, ItemsList)
            except django.db.utils.IntegrityError:
                data["msg"] = "檢查内容是否有重复產品!"
                return JsonResponse(data)

            data = {
                'status': "OK"
            }
        else:
            data['msg'] = "請輸入完整的資料！"

    return JsonResponse(data)


class AnalyzeAddItemsList:
    __AddItemsListStr = None
    __ItemsList = None

    def __init__(self, AddItemsListStr: str):
        self.__AddItemsListStr = AddItemsListStr
        self.__ItemsList = []

        self.Analyze()
        return

    def Analyze(self):
        ListStr = self.__AddItemsListStr.split("\n")
        for line in ListStr:

            if "x" in line and "$" in line:

                if "(" in line in line:
                    Info = line.split("(")
                    ItemName = Info[0].strip()
                    Info = [''.join(list(g)) for k, g in groupby(Info[1], key=lambda x: x.isdigit())]

                    if Info[-2] == '.':
                        self.__ItemsList.append([ItemName, Info[-5], Info[-3] + "." + Info[-1]])
                    else:
                        self.__ItemsList.append([ItemName, Info[-3], Info[-1]])
                else:
                    Info = [''.join(list(g)) for k, g in groupby(line, key=lambda x: x.isdigit())]
                    if Info[-2] == '.':
                        self.__ItemsList.append([Info[0], Info[-5], Info[-3] + "." + Info[-1]])
                    else:
                        self.__ItemsList.append([Info[0], Info[-3], Info[-1]])
        return

    def GetItemsList(self):
        return self.__ItemsList

if __name__ == '__main__':
    a = ("""呀信

明太子5包x$49
烏冬3盒x$68
三色5盒x$55
城市6盒x$42
透明12盒x$65
新雙22盒x$37.1""")

    b = ("""電話 61521789

地址  旺角豉油街110號華富園
11／F   A室

英文名收件人
Chan ka ming

打哈欠小新小夜燈1箱 (36個) x$60.5""")

    c = ("""Bowie

韓國🇰🇷BOTO 低分子魚膠原蛋白紅石榴汁 100包 56箱x$225""")

    d = ("""
        更正

大埔昌運 hoiki

Clean yes KD-AD口罩3箱(30) x$71.5

Kf94 (3000)片x$2.7
Kf94 黑色(1000)片x$2.7
    """)
    print(AnalyzeAddItemsList(d).GetItemsList())
