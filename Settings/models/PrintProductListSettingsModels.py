"""
打印產品列表信息
"""

from django.db import models

class PrintProductListSettings(models.Model):
    preHtml = models.CharField(max_length=248)
    suffixHtml = models.CharField(max_length=248)

    class Meta:
        db_table = "PrintProductListSettings"
