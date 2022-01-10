"""
首頁
"""
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt

from Settings.models.BasisSettingsModels import BasisSettings

def index(request):
    BasisSettingsData = BasisSettings.objects.get(id=1)
    Name = BasisSettingsData.Name
    return render(request, "LayuiBasis/index.html", {"Name": Name})

@xframe_options_exempt
def Welcome(request):
    BasisSettingsData = BasisSettings.objects.get(id=1)
    Name = BasisSettingsData.Name
    return render(request, "LayuiBasis/Welcome.html", {"Name": Name})
