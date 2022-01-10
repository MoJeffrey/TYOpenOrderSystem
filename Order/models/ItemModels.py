"""
訂單中商品資料
"""
from django.db import models, connection

class Item(models.Model):
    OrderID = models.IntegerField()
    Name = models.CharField(max_length=128)
    Num = models.IntegerField()
    Price = models.CharField(max_length=248)

    class Meta:
        db_table = "Item"
        unique_together = ["OrderID", "Name"]
        index_together = ["OrderID", "Name"]

    @staticmethod
    def GetOrderAllItem(OrderID: str):
        """
        傳回訂單的全部商品
        :return:
        """
        cursor = connection.cursor()
        OrderID = int(OrderID[1:])

        SQL = """
                SELECT
                    Name,
                    Num,
                    Price
                FROM `Item`
                WHERE OrderID={OrderID}
                ORDER BY id
                """.format(OrderID=OrderID)

        cursor.execute(SQL)
        row = cursor.fetchall()

        ItemList = []
        x = 1
        for Data in row:
            ItemList.append(
                {
                    "No": x,
                    "Name": Data[0],
                    "Num": Data[1],
                    "Price": Data[2]
                }
            )
            x += 1

        return ItemList

    @staticmethod
    def AddItem(OrderID: str, Name: str, Num: str, Price: str):
        """
        添加產品
        :return:
        """
        cursor = connection.cursor()
        OrderID = int(OrderID[1:])

        SQL = """
                INSERT INTO 
                    `Item`(`OrderID`, `Name`, `Num`, `Price`) 
                VALUES ("{OrderID}","{Name}","{Num}","{Price}")
                """.format(OrderID=OrderID,
                           Name=Name,
                           Num=Num,
                           Price=Price)

        cursor.execute(SQL)
        return

    @staticmethod
    def BatchAddItem(OrderID: str, ItemList: list):
        """
        批量添加
        :param OrderID:
        :param ItemList:
        :return:
        """
        cursor = connection.cursor()
        OrderID = int(OrderID[1:])

        for ItemData in ItemList:
            SQL = """
                    INSERT INTO 
                        `Item`(`OrderID`, `Name`, `Num`, `Price`) 
                    VALUES ("{OrderID}","{Name}","{Num}","{Price}")
                    """.format(OrderID=OrderID,
                               Name=ItemData[0],
                               Num=ItemData[1],
                               Price=ItemData[2])

            cursor.execute(SQL)
        return

    @staticmethod
    def DelItems(OrderID: str, DelList: list):
        """
        :param OrderID:
        :param DelList:
        :return:
        """
        cursor = connection.cursor()
        OrderID = int(OrderID[1:])

        SQL = """
                DELETE FROM Item
                WHERE OrderID={OrderID} AND (
                """.format(OrderID=OrderID)

        for Name in DelList:
            SQL += " Name='{Name}' OR".format(Name=Name)
        SQL = SQL[:-3] + ");"

        cursor.execute(SQL)
        return

    @staticmethod
    def GetItemList(Name: str):
        """
        :param Name:
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                SELECT
                    Name,
                    Num,
                    Price
                FROM 
                    `Item`
                WHERE Name like '%{Name}%'""".format(Name=Name)

        # 排序
        SQL += " ORDER BY -id"

        cursor.execute(SQL)
        row = cursor.fetchall()

        ItemList = []
        for Data in row:
            ItemList.append(
                {
                    "Name": Data[0],
                    "Num": Data[1],
                    "Price": Data[2]
                }
            )

        return ItemList
