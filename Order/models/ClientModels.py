"""
顧客數據
"""
import os

from django.db import models, connection

class Client(models.Model):
    Name = models.CharField(max_length=128)
    Address = models.CharField(max_length=248)
    Phone = models.CharField(max_length=248)

    class Meta:
        db_table = "Client"
        unique_together = ["Name", "Address", "Phone"]
        index_together = ["Name", "Address", "Phone"]

    def GetClientID(self, Name: str, Address: str, Phone: str):
        """
        先嘗試添加新客戶
        如果客戶存在則不進行添加

        查找該客戶ID並返回
        :return:
        """
        self.AddNewClient(Name, Address, Phone)

        cursor = connection.cursor()

        SQL = """
                SELECT
                    id
                FROM 
                    `Client`
                WHERE
                    Name = "{Name}" AND
                    Address = "{Address}" AND
                    Phone = "{Phone}";
                    """.format(Name=Name,
                               Address=Address,
                               Phone=Phone)

        cursor.execute(SQL)
        rst = cursor.fetchone()
        return rst[0]

    @staticmethod
    def AddNewClient(Name: str, Address: str, Phone: str):
        """
        关键字/句：
        insert ignore into，
        如果插入的数据会导致UNIQUE索引或PRIMARY KEY发生冲突/重复，
        则忽略此次操作/不插入数据

        添加新客戶資料
        :return:
        """
        cursor = connection.cursor()

        SQL = """
            INSERT IGNORE INTO 
                `Client`(`Name`, `Address`, `Phone`) 
            VALUES ("{Name}","{Address}","{Phone}")
            """.format(Name=Name,
                       Address=Address,
                       Phone=Phone)

        cursor.execute(SQL)
        return

    @staticmethod
    def GetClientList(Name: str, Phone: str):
        """
        查找關鍵字客戶，供前台下拉項選擇
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                SELECT
                    Name,
                    Address,
                    Phone
                FROM 
                    `Client`
                """

        if Name is not None and Name != "":
            SQL += "WHERE Name like '%{Name}%'".format(Name=Name)

        if (Phone is not None and Phone != "") and (Name is not None and Name != ""):
            SQL += "OR Phone like '%{Phone}%'".format(Phone=Phone)

        if (Phone is not None and Phone != "") and (Name is None and Name == ""):
            SQL += "WHERE Name like '%{Name}%'".format(Name=Name)

        # 排序
        SQL += " ORDER BY -id;"

        cursor.execute(SQL)
        row = cursor.fetchall()

        ClientList = []
        for Data in row:
            ClientList.append(
                {
                    "Name": Data[0],
                    "Address": Data[1],
                    "Phone": Data[2]
                }
            )

        return ClientList
