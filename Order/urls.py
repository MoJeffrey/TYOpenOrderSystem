from django.urls import path
from .view import OrderList
from .view import OpenNewOrder
from .view import OrderInfo
from .view import AddItem
from .view import AutomaticIdentification

urlpatterns = [
    path(r'OrderList', OrderList.index),
    path(r'OrderList/GetOrderList/', OrderList.GetOrderList),

    path(r'OpenNewOrder', OpenNewOrder.index),
    path(r'OpenNewOrder/Create/', OpenNewOrder.Create),
    path(r'OpenNewOrder/GetClientList/', OpenNewOrder.GetClientList),

    path(r'OrderInfo', OrderInfo.index),
    path(r'OrderInfo/DelItems/', OrderInfo.DelItems),
    path(r'OrderInfo/GetItemList/', OrderInfo.GetItemList),
    path(r'OrderInfo/UploadPaymentVoucher/', OrderInfo.UploadPaymentVoucher),
    path(r'OrderInfo/PaymentToChange/', OrderInfo.PaymentToChange),
    path(r'OrderInfo/ShippingStatusToChange/', OrderInfo.ShippingStatusToChange),
    path(r'OrderInfo/SaveMemo/', OrderInfo.SaveMemo),
    path(r'OrderInfo/DelOrder/', OrderInfo.DelOrder),

    path(r'AddItem', AddItem.index),
    path(r'AddItem/Add/', AddItem.Add),
    path(r'AddItem/GetItemList/', AddItem.GetItemList),

    path(r'AutomaticIdentification', AutomaticIdentification.index),
    path(r'AutomaticIdentification/Distinguish/', AutomaticIdentification.Distinguish)
]
