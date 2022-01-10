document.write("<script type='text/javascript' src='/static/js/PrintOrder/jspdf.umd.js'></script>");
document.write("<script type='text/javascript' src='/static/js/PrintOrder/jspdf.plugin.autotable.js'></script>");
document.write("<script type='text/javascript' src='/static/js/PrintOrder/source-han-sans-normal.js'></script>");

function PrintOrder() {
	this.doc = new jspdf.jsPDF();
	this.doc.addFont('SourceHanSans-Normal.ttf', 'SourceHanSans-Normal', 'normal');
	this.doc.setFont('SourceHanSans-Normal');

	this.OrderPageMixItem = 15;
}

PrintOrder.prototype.SetCompany = function(Name, Address, Phone) {
	// 公司名称/Logo
	this.doc.setFontSize(40);
	this.doc.text(Name, 14, 22);
	
	// 公司地址&公司电话
	this.doc.setFontSize(10);
	this.doc.text("地址: " + Address + "\r電話: " + Phone, 14, 35);
};

PrintOrder.prototype.SetTransferInformation = function(TransferInformation){
	this.doc.text(TransferInformation, 14, 200);
};

PrintOrder.prototype.SetMemo = function(Memo){
	this.doc.text(Memo, 14, 230);
};

PrintOrder.prototype.SetCustomerInformation = function(OrderID, Date, Name, Address, Phone){
	//客戶資料
	let text = "顧客姓名: " + Name + "\r";
	text += "顧客地址: " + Address + "\r";
	text += "顧客電話: " + Phone;
	this.doc.setFontSize(10);
	this.doc.text(text, 14, 50);
	
	//訂單日期/訂單編號
	text = "日期： "+ Date +"\r";
	text += "訂單編號： "+ OrderID;
	this.doc.setFontSize(10);
	this.doc.text(text, 150, 50);
};

PrintOrder.prototype.SetItem = function(Data, fillColor) {
	//表格列头
	let columns = ["No.", "商品名稱", "數量", "單價", ""];
	if(Data.length <= this.OrderPageMixItem){
		let rows = [];

		for(let x in Data) {
			let rowData = [];
			rowData.push(Data[x]['No']);
			rowData.push(Data[x]['Name']);
			rowData.push(Data[x]['Num']);
			rowData.push(Data[x]['Price']);
			rowData.push(Data[x]['TotalPrice']);
			rows.push(rowData);
		}
		rows.pop();
		if(rows.length !== this.OrderPageMixItem){
			for(let x = rows.length+1; x < this.OrderPageMixItem; x++){
				rows.push([x]);
			}
		}

		rows.push(["","","", "總金額: ", Data[Data.length-1]["AllPrice"]]);

		this.doc.autoTable(columns, rows,
		{
			startY: 65,
			showHead: 'firstPage',
			styles: { font: "SourceHanSans-Normal"},
			headerStyles: {
     			fillColor: fillColor
   			}
		});
	}
};

PrintOrder.prototype.Save = function(Name) {
  	this.doc.save(Name + ".pdf");
};

