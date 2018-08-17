var data = source.data;
var commareplace = '|';
var filetext = 'DocumentTrackingNumber,OriginalDocumentID,MarketerDUNS,TDSP,PaymentDueDate,ESIID,Invoice Total Amount,Processed\n';
for (i=0; i < data['DocumentTrackingNumber'].length; i++) {
    var currRow = [data['DocumentTrackingNumber'][i].toString().replace(/,/g , commareplace),
                   data['OriginalDocumentID'][i].toString().replace(/,/g , commareplace),
                   data['MarketerDUNS'][i].toString().replace(/,/g , commareplace),
                   data['TDSP'][i].toString().replace(/,/g , commareplace),
                   data['PaymentDueDate'][i].toString().replace(/,/g , commareplace),
                   data['ESIID'][i].toString().replace(/,/g , commareplace),
                   data['InvoiceTotalAmount'][i].toString().replace(/,/g , commareplace),
                   data['Processed'][i].toString().replace(/,/g , commareplace).concat('\n')];
    var joined = currRow.join();
    filetext = filetext.concat(joined);
}

var filename = '820transactions.csv';
var blob = new Blob([filetext], { type: 'text/csv;charset=utf-8;' });

//addresses IE
if (navigator.msSaveBlob) {
    navigator.msSaveBlob(blob, filename);
}

else {
    var link = document.createElement("a");
    link = document.createElement('a')
    link.href = URL.createObjectURL(blob);
    link.download = filename
    link.target = "_blank";
    link.style.visibility = 'hidden';
    link.dispatchEvent(new MouseEvent('click'))
}
