"""
基礎設置
"""

from django.db import models, connection

class BasisSettings(models.Model):
    Name = models.CharField(max_length=248)

    class Meta:
        db_table = "BasisSettings"
