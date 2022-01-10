#查詢訂單列表
SELECT 
	O.OrderID,
	O.Date,
	O.WhetherPaid,
	C.Name,
	C.Phone	
FROM `Order` AS O
LEFT JOIN `Client` AS C
ON O.Client = C.id


#获得訂單資料
SELECT
	O.OrderID,
	O.Date,
	O.WhetherPaid,
	O.PaymentRecordPhoto,
	O.Memo,
	C.Name,
	C.Phone,
	C.Address
FROM `Order` AS O
LEFT JOIN `Client` AS C
ON O.Client = C.id
WHERE O.OrderID = "";