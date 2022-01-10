"""
基础设置
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Settings.models.BasisSettingsModels import BasisSettings


@xframe_options_exempt
def index(request):
    BasisSettingsData = BasisSettings.objects.get(id=1)
    Name = BasisSettingsData.Name
    return render(request, "Settings/BasisSettings.html", {"Name": Name})

def Save(request):
    data = {
        'msg': '请检查填写的内容！'
    }
    if request.method == "POST":
        Name = request.POST.get('Name')
        BasisSettingsData = BasisSettings.objects.filter(id=1)
        if BasisSettingsData.exists():
            BasisSettingsData.update(Name=Name)
        else:
            BasisSettings(Name=Name).save()
        data = {
            'status': 'OK！'
        }
    return JsonResponse(data)
