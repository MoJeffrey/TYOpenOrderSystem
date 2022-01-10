from django.urls import path
from .view import BasisSettings
from .view import PrintSettings
from .view import PrintProductListSettings

urlpatterns = [
    path(r'BasisSettings', BasisSettings.index),
    path(r'BasisSettings/Save/', BasisSettings.Save),

    path(r'PrintSettings', PrintSettings.index),
    path(r'PrintSettings/Save/', PrintSettings.Save),
    path(r'PrintSettings/GetPrintData/', PrintSettings.GetPrintData),

    path(r'PrintProductListSettings', PrintProductListSettings.index),
    path(r'PrintProductListSettings/Save/', PrintProductListSettings.Save),
    path(r'PrintProductListSettings/GetPrintData/', PrintProductListSettings.GetPrintData),
]
