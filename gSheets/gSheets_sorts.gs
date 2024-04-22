function onOpen() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var entries = [{
    name: "Sort by Amount (Asc) | Донатики",
    functionName: "sortAmountAsc"
  }, {
    name: "Sort by Amount (Desc) | Донатики",
    functionName: "sortAmountDesc"
  }, {
    name: "Sort by Date (Asc) | Донатики + Список пожеланий",
    functionName: "sortDateAsc"
  }, {
    name: "Sort by Date (Desc) | Донатики + Список пожеланий",
    functionName: "sortDateDesc"
  }];
  sheet.addMenu("Sort", entries);
}

function sortAmountAsc() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getRange("A2:D");
  range.sort([{column: 3, ascending: true}]);
}

function sortAmountDesc() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getRange("A2:D");
  range.sort([{column: 3, ascending: false}]);
}

function sortDateAsc() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getRange("A2:D");
  range.sort([{column: 4, ascending: true}]);
}

function sortDateDesc() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  var range = sheet.getRange("A2:D");
  range.sort([{column: 4, ascending: false}]);
}
