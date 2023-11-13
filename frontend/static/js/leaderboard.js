
// var tbody_main = document.querySelector("#table-body-main");
var tbody_exam = document.querySelector("#table-body-exam");


// 循环遍历数据并将数据填入到表格中
// for (var i = 0; i < main_model_data.length; i++) {
//     var rowData = main_model_data[i];
//     var row = document.createElement("tr");

//     // 循环遍历属性并将数据填入到表格单元格中
//     for (var j = 0; j < Object.keys(rowData).length; j++) {
//         var cell = document.createElement("td");
//         cell.textContent = rowData[Object.keys(rowData)[j]];
//         row.appendChild(cell);
//     }

//     tbody_main.appendChild(row);
// }

// 循环遍历数据并将数据填入到表格中
for (var i = 0; i < exam_model_data.length; i++) {
    var rowData = exam_model_data[i];
    var row = document.createElement("tr");

    // 循环遍历属性并将数据填入到表格单元格中
    for (var j = 0; j < Object.keys(rowData).length; j++) {
        var cell = document.createElement("td");
        cell.textContent = rowData[Object.keys(rowData)[j]];
        row.appendChild(cell);
    }

    tbody_exam.appendChild(row);
}