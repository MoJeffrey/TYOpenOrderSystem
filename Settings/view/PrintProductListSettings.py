"""
打印產品列表信息设置
"""
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Settings.models.PrintProductListSettingsModels import PrintProductListSettings


@xframe_options_exempt
def index(request):

    # noinspection PyBroadException
    try:
        PrintProductListSettingsData = PrintProductListSettings.objects.get(id=1)
        preHtml = PrintProductListSettingsData.preHtml
        suffixHtml = PrintProductListSettingsData.suffixHtml

    except Exception:
        preHtml = ""
        suffixHtml = ""

    return render(request, "Settings/PrintProductListSetting.html", {"preHtml": preHtml, "suffixHtml": suffixHtml})

def Save(request):
    data = {
        'msg': '请检查填写的内容！'
    }
    if request.method == "POST":
        preHtml = request.POST.get('preHtml')
        suffixHtml = request.POST.get('suffixHtml')
        PrintProductListSettingsData = PrintProductListSettings.objects.filter(id=1)
        if PrintProductListSettingsData.exists():
            PrintProductListSettingsData.update(preHtml=preHtml, suffixHtml=suffixHtml)
        else:
            PrintProductListSettings(preHtml=preHtml, suffixHtml=suffixHtml).save()
        data = {
            'status': 'OK！'
        }
    return JsonResponse(data)

def GetPrintData(request):
    data = {
        'msg': '请检查填写的内容！'
    }
    if request.method == "POST":
        PrintProductListSettingsData = PrintProductListSettings.objects.get(id=1)

        data = {
            'status': 'OK！',
            "preHtml": PrintProductListSettingsData.preHtml,
            "suffixHtml": PrintProductListSettingsData.suffixHtml,
        }
    return JsonResponse(data)
