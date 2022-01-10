"""
訂單數據
"""
import os

from django.db import models, connection

class Order(models.Model):
    OrderID = models.IntegerField(db_index=True, unique=True)
    Date = models.CharField(max_length=10)
    Client = models.IntegerField()
    Memo = models.TextField()

    WhetherPaid = models.BooleanField()
    PaymentRecordPhoto = models.CharField(max_length=250)
    PaymentMemo = models.TextField()

    ShippingStatus = models.IntegerField()
    ShippingMemo = models.TextField()

    class Meta:
        db_table = "Order"
        ordering = ['-OrderID']

    def GetOrderList(self, Key: str, DataDisplay: int, page: str, limit: str):
        """
        :return:
        """
        def GetProductCount(Where):
            CountSQL = ("SELECT count(*) FROM "
                        "(SELECT DISTINCT O.OrderID AS ID "
                        "FROM `Order` AS O "
                        "LEFT JOIN `Client` AS C ON O.Client = C.id "
                        "LEFT JOIN `Item` AS I ON O.OrderID = I.OrderID" + Where + ") AS A")

            cursor.execute(CountSQL)
            rst = cursor.fetchone()
            return rst[0]

        cursor = connection.cursor()

        SQL = """
                SELECT DISTINCT 
                    O.OrderID,
                    O.Date,
                    O.WhetherPaid,
                    O.ShippingStatus,
                    C.Name,
                    C.Phone
                FROM `Order` AS O
                LEFT JOIN `Client` AS C
                ON O.Client = C.id
                LEFT JOIN `Item` AS I
                ON O.OrderID = I.OrderID
                """

        WhereSQL = """
                   WHERE 
                        (O.WhetherPaid = 0 OR
                        O.ShippingStatus = 0)
                    """
        if DataDisplay == "1":
            WhereSQL = """
                   WHERE 
                        (O.WhetherPaid = 0 OR
                        O.WhetherPaid = 1)
                    """

        if Key is not None or Key == "":
            WhereSQL += """
                        AND (O.OrderID = '%{Key}%' OR
                        C.Name like '%{Key}%' OR
                        C.Phone like '%{Key}%' OR
                        I.Name like '%{Key}%')
                    """.format(Key=Key)

        SQL += WhereSQL + " ORDER BY -O.OrderID"

        # 獲得總數
        TotalCount = GetProductCount(WhereSQL)

        # 分頁
        Start = (int(page)-1)*int(limit)
        SQL += " LIMIT {Start},{limit}".format(Start=Start, limit=limit)

        cursor.execute(SQL)
        row = cursor.fetchall()

        OrderList = []
        for Data in row:
            OrderList.append(
                {
                    "OrderID": self.GetShowOrderID(Data[0]),
                    "Description": self.GetShowOrderID(Data[0]) + " " + Data[1] + " " + Data[4] + " " + Data[5],
                    "WhetherPaid": Data[2],
                    "ShippingStatus": Data[3]
                }
            )

        return OrderList, TotalCount

    @staticmethod
    def GetShowOrderID(OrderID: int):
        """
        返回顯示的訂單ID
        補0與加上#符號
        :param OrderID:
        :return:
        """
        OrderID = str(OrderID)

        if len(OrderID) < 5:
            OrderID = "#" + (5-len(OrderID)) * "0" + OrderID
        else:
            OrderID = "#" + OrderID
        return OrderID

    def GetNewOrderID(self):
        """
        傳回一個未開新單編碼
        :return:
        """
        cursor = connection.cursor()

        SQL = "select max(OrderID) from `Order`"

        cursor.execute(SQL)
        rst = cursor.fetchone()
        return self.GetShowOrderID(rst[0] + 1)

    @staticmethod
    def CreateNewOrder(OrderID: str, Date: str, Client: int):
        """
        創建新單
        :return:
        """
        cursor = connection.cursor()
        OrderID = int(OrderID[1:])

        SQL = """
                INSERT INTO 
                    `Order`(
                        `OrderID`, 
                        `Date`, 
                        `Client`, 
                        `WhetherPaid`, 
                        `PaymentRecordPhoto`, 
                        `PaymentMemo`,
                        `Memo`,
                        `ShippingStatus`,
                        `ShippingMemo`
                    ) 
                VALUES (
                    "{OrderID}",
                    "{Date}",
                    "{Client}", 
                    "0", 
                    "", 
                    "", 
                    "", 
                    0, 
                    "");
                """.format(OrderID=OrderID,
                           Date=Date,
                           Client=Client)

        cursor.execute(SQL)
        return

    def GetOrderInfo(self, OrderID: str):
        """
        獲得訂單資料
        :return:
        """
        cursor = connection.cursor()
        OrderID = int(OrderID[1:])

        SQL = """
                SELECT
                    O.Date,
                    O.WhetherPaid,
                    O.PaymentRecordPhoto,
                    O.Memo,
                    C.Name,
                    C.Phone,
                    C.Address,
                    O.PaymentMemo,
                    O.ShippingStatus,
                    O.ShippingMemo
                FROM `Order` AS O
                LEFT JOIN `Client` AS C
                ON O.Client = C.id
                WHERE O.OrderID = "{OrderID}";
                """.format(OrderID=OrderID)

        cursor.execute(SQL)
        row = cursor.fetchall()[0]

        OrderInfo = {
            "OrderID": self.GetShowOrderID(OrderID),
            "Date": row[0],
            "WhetherPaid": row[1],
            "PaymentRecordPhoto": row[2],
            "Memo": row[3],
            "Name": row[4],
            "Phone": row[5],
            "Address": row[6],
            "PaymentMemo": row[7],
            "ShippingStatus": row[8],
            "ShippingMemo": row[9],
        }

        return OrderInfo

    def SavePaymentVoucher(self, OrderID: str, ImgFile: str):
        """

        :param OrderID:
        :param ImgFile:
        :return:
        """
        OrderInfo = self.GetOrderInfo(OrderID)

        FileName = OrderInfo["OrderID"][1:] + "_"
        FileName += OrderInfo["Date"] + "_"
        FileName += OrderInfo["Name"] + "_"
        FileName += OrderInfo["Phone"] + "." + ImgFile.split(".")[-1]

        cursor = connection.cursor()

        SQL = """
                UPDATE 
                    `Order` 
                SET 
                    `PaymentRecordPhoto`='{FileName}'
                WHERE 
                    `OrderID`= {OrderID}
                """.format(FileName=FileName,
                           OrderID=int(OrderID[1:]))

        cursor.execute(SQL)
        return FileName

    @staticmethod
    def PaymentToChange(OrderID: str, Payment: int):
        """
        轉變付款狀態
        :param OrderID:
        :param Payment:
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                UPDATE 
                    `Order` 
                SET 
                    `WhetherPaid`='{Payment}'
                WHERE 
                    `OrderID`= {OrderID}
                """.format(Payment=Payment,
                           OrderID=int(OrderID[1:]))

        cursor.execute(SQL)
        return

    @staticmethod
    def ShippingStatusToChange(OrderID: str, ShippingStatus: int):
        """
        轉變出貨狀態
        :param OrderID:
        :param ShippingStatus:
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                   UPDATE 
                       `Order` 
                   SET 
                       `ShippingStatus`='{ShippingStatus}'
                   WHERE 
                       `OrderID`= {OrderID}
                   """.format(ShippingStatus=ShippingStatus,
                              OrderID=int(OrderID[1:]))

        cursor.execute(SQL)
        return

    @staticmethod
    def SaveMemo(OrderID: str, Memo: str, PaymentMemo: str, ShippingMemo: str):
        """
        保存備忘記錄
        :param OrderID:
        :param Memo:
        :param PaymentMemo:
        :param ShippingMemo:
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                UPDATE 
                    `Order` 
                SET 
                    `Memo`='{Memo}',
                    `PaymentMemo`='{PaymentMemo}',
                    `ShippingMemo`='{ShippingMemo}'
                WHERE 
                    `OrderID`= {OrderID}
                """.format(Memo=Memo,
                           PaymentMemo=PaymentMemo,
                           ShippingMemo=ShippingMemo,
                           OrderID=int(OrderID[1:]))

        cursor.execute(SQL)
        return
