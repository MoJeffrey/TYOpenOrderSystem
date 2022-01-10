"""
打印設置
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Settings.models import PrintSettings

@xframe_options_exempt
def index(request):
    PrintSettingsData = PrintSettings.objects.get(id=1)
    Data = {
        "Name": PrintSettingsData.Name,
        "Address": PrintSettingsData.Address,
        "Phone": PrintSettingsData.Phone,
        "Payment": PrintSettingsData.Payment,
        "Memo": PrintSettingsData.Memo,
    }
    return render(request, "Settings/PrintSettings.html", Data)

def Save(request):
    data = {
        'msg': '请检查填写的内容！'
    }
    if request.method == "POST":
        Name = request.POST.get('Name')
        Address = request.POST.get('Address')
        Phone = request.POST.get('Phone')
        Payment = request.POST.get('Payment')
        Memo = request.POST.get('Memo')

        PrintSettingsData = PrintSettings.objects.filter(id=1)
        if PrintSettingsData.exists():
            PrintSettingsData.update(Name=Name,
                                     Address=Address,
                                     Phone=Phone,
                                     Payment=Payment,
                                     Memo=Memo)
        else:
            PrintSettings(Name=Name,
                          Address=Address,
                          Phone=Phone,
                          Payment=Payment,
                          Memo=Memo).save()
        data = {
            'status': 'OK！'
        }
    return JsonResponse(data)

def GetPrintData(request):
    data = {
        'msg': '请检查填写的内容！'
    }
    if request.method == "POST":
        PrintSettingsData = PrintSettings.objects.get(id=1)

        data = {
            'status': 'OK！',
            "Name": PrintSettingsData.Name,
            "Address": PrintSettingsData.Address,
            "Phone": PrintSettingsData.Phone,
            "Payment": PrintSettingsData.Payment,
            "Memo": PrintSettingsData.Memo,
        }
    return JsonResponse(data)
