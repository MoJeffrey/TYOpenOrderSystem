"""
基礎設置
"""

from django.db import models

class PrintSettings(models.Model):
    Name = models.CharField(max_length=248)
    Address = models.CharField(max_length=248)
    Phone = models.CharField(max_length=248)
    Payment = models.CharField(max_length=248)
    Memo = models.TextField()

    class Meta:
        db_table = "PrintSettings"
