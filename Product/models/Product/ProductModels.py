"""
產品數據
Name = 名称
Label = 標籤後期使用
QuantityPerBox = 一箱數量
PurchasePrice = 成本價
Details = 詳情
"""
import os

from django.db import models, connection
from PConceptOpenOrderSystem.settings import BASE_DIR

ProductImgPath = os.path.join(BASE_DIR, "templates/static/images/Product")

class Product(models.Model):
    Name = models.CharField(max_length=128)
    Label = models.CharField(max_length=248)
    QuantityPerBox = models.CharField(max_length=248)
    PurchasePrice = models.CharField(max_length=248)
    Details = models.TextField()

    class Meta:
        db_table = "Product"
        unique_together = ["Name", "Label"]
        index_together = ["Name", "Label"]
        ordering = ['Name']

    @staticmethod
    def GetProductList(Key: str, SellPrice: float, page: str, limit: str, ShowAll: str):
        """
        回傳產品列表
        :param Key: 關鍵字查詢
        :param SellPrice:
        :param page:
        :param limit:
        :param ShowAll: 是否顯示全部
        :return:
        """

        def new_round(_float, _len):
            if isinstance(_float, float):
                if str(_float)[::-1].find('.') <= _len:
                    return _float
                if str(_float)[-1] == '5':
                    return round(float(str(_float)[:-1] + '6'), _len)
                else:
                    return round(_float, _len)
            else:
                return round(_float, _len)

        def GetProductCount(Where):
            cursor.execute("SELECT count(*) FROM `Product`" + Where)
            rst = cursor.fetchone()
            return rst[0]

        cursor = connection.cursor()

        SQL = """
                SELECT
                    id,
                    Name,
                    Label,
                    QuantityPerBox,
                    PurchasePrice
                FROM 
                    `Product`
                """

        WhereSQL = ""
        if Key is not None or Key == "":
            WhereSQL = """
                    WHERE
                        Name like '%{Key}%' OR
                        Label	like '%{Key}%'
                    """.format(Key=Key)

        SQL += WhereSQL + " ORDER BY `Name`"

        # 獲得總數
        TotalCount = GetProductCount(WhereSQL)

        # 分頁
        Start = (int(page)-1)*int(limit)

        if ShowAll != "1":
            SQL += " LIMIT {Start},{limit}".format(Start=Start, limit=limit)
        cursor.execute(SQL)
        row = cursor.fetchall()

        ProductList = []
        for Data in row:
            ProductList.append(
                {
                    "id": Data[0],
                    "Name": Data[1],
                    "Label": Data[2],
                    "QuantityPerBox": Data[3],
                    "PurchasePrice": Data[4],
                    "SellPrice": new_round(float(Data[4]) * SellPrice, 1),
                    "HavePhoto": os.path.exists(os.path.join(ProductImgPath, Data[1] + ".jpg"))
                }
            )

        return ProductList, TotalCount

    @staticmethod
    def GetProductInfo(SKU: str):
        """
        回傳產品資料
        包含圖片名稱
        和各個櫃的數量
        :param SKU: 公司產品內部ID
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                SELECT
                    IF(Photo is NULL,"NULL", Photo)
                FROM 
                    `Product`
                WHERE
                    SKU	= '{SKU}'
                """.format(SKU=SKU)

        cursor.execute(SQL)
        row = cursor.fetchall()

        ProductInfo = {
            "Photo": row[0][0],
            "Container": [{
                "ContainerNum": 1,
                "Total": 1,
                "Remainder": 1
            }]
        }

        return ProductInfo

    @staticmethod
    def GetProduct(ID: str):
        """
        回傳单个產品資料
        :param ID: 產品ID
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                SELECT
                    id,
                    Name,
                    Label,
                    QuantityPerBox,
                    PurchasePrice
                FROM 
                    `Product`
                WHERE
                    id	= '{ID}'
                """.format(ID=ID)

        cursor.execute(SQL)
        Data = cursor.fetchall()[0]
        ProductInfo = {
            "id": Data[0],
            "Name": Data[1],
            "Label": Data[2],
            "QuantityPerBox": Data[3],
            "PurchasePrice": Data[4],
            "HavePhoto": os.path.exists(os.path.join(ProductImgPath, Data[1] + ".jpg"))
        }

        return ProductInfo

    @staticmethod
    def GetLabelAndDetails(ID: str):
        """
        回傳单个產品的標籤和詳情
        :param ID: 產品ID
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                SELECT
                    id,
                    Label,
                    Details
                FROM 
                    `Product`
                WHERE
                    id	= '{ID}'
                """.format(ID=ID)

        cursor.execute(SQL)
        Data = cursor.fetchall()[0]
        ProductInfo = {
            "id": Data[0],
            "Label": Data[1],
            "Details": Data[2]
        }

        return ProductInfo

    @staticmethod
    def EditProduct(Name: str,
                    Label: str,
                    QuantityPerBox: str,
                    PurchasePrice: str,
                    ProductID: str):
        """
        修改单个產品資料
        :param Name:
        :param Label:
        :param QuantityPerBox:
        :param PurchasePrice:
        :param ProductID:
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                UPDATE 
                    `Product` 
                SET 
                    `Name`='{Name}',
                    `Label`='{Label}',
                    `QuantityPerBox`='{QuantityPerBox}',
                    `PurchasePrice`='{PurchasePrice}' 
                WHERE 
                    `id`='{ProductID}'
                """.format(Name=Name,
                           Label=Label,
                           QuantityPerBox=QuantityPerBox,
                           PurchasePrice=PurchasePrice,
                           ProductID=ProductID)

        cursor.execute(SQL)
        return True

    @staticmethod
    def EditProductDetails(Label: str,
                           Details: str,
                           ProductID: str):
        """
        修改单个產品資料
        :param Label:
        :param Details:
        :param ProductID:
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                    UPDATE 
                        `Product` 
                    SET 
                        `Label`='{Label}',
                        `Details`='{Details}'
                    WHERE 
                        `id`='{ProductID}'
                    """.format(Label=Label,
                               Details=Details,
                               ProductID=ProductID)

        cursor.execute(SQL)
        return True

    @staticmethod
    def AddProduct(Name: str,
                   Label: str,
                   QuantityPerBox: str,
                   PurchasePrice: str):
        """
        增加单个產品資料
        :param Name:
        :param Label:
        :param QuantityPerBox:
        :param PurchasePrice:
        :return:
        """
        cursor = connection.cursor()

        SQL = """
                INSERT INTO 
                    `Product`(`Name`, `Label`, `QuantityPerBox`, `PurchasePrice`, `Details`) 
                VALUES ("{Name}","{Label}","{QuantityPerBox}","{PurchasePrice}", "")
                """.format(Name=Name,
                           Label=Label,
                           QuantityPerBox=QuantityPerBox,
                           PurchasePrice=PurchasePrice)

        cursor.execute(SQL)
        return True

    @staticmethod
    def BatchAddProduct(dataList: list):
        """
        批量增加產品資料
        :param dataList:
        :return:
        """
        cursor = connection.cursor()
        ChangeScore = 0
        SaveNewProduct = 0

        for data in dataList:
            SQL = """
                    INSERT INTO 
                        `Product`(`Name`, `Label`, `QuantityPerBox`, `PurchasePrice`, `Details`) 
                    values 
                        ('{Name}', "{Label}", "{QuantityPerBox}", "{PurchasePrice}", "") 
                    ON DUPLICATE KEY UPDATE 
                        `Name`='{Name}', `Label`="{Label}", `QuantityPerBox`="{QuantityPerBox}", `PurchasePrice`="{PurchasePrice}";
                    """.format(Name=data['Name'],
                               Label=data['Label'],
                               QuantityPerBox=data['QuantityPerBox'],
                               PurchasePrice=data['PurchasePrice'])
            cursor.execute(SQL)
            if cursor.rowcount == 2:
                ChangeScore += 1
            elif cursor.rowcount == 1:
                SaveNewProduct += 1
        return ChangeScore, SaveNewProduct

    @staticmethod
    def DelProducts(DelList: list):
        """
        :param DelList:
        :return:
        """
        cursor = connection.cursor()

        SQL = "DELETE FROM Product WHERE"

        for ID in DelList:
            SQL += " id={id} OR".format(id=ID)
        SQL = SQL[:-3] + ";"
        print(SQL)
        cursor.execute(SQL)
        return
