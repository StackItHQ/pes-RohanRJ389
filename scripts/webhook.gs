function onEdit(e) {
  var webhookUrl = "your/backend/url/here";  // Update this

  var range = e.range;
  var row = range.getRow();
  var col = range.getColumn();
  var newValue = e.value;
  var oldValue = e.oldValue || ""; // Get the old value before the edit

  // Get the column name based on the header row (assuming it's the first row)
  var sheet = e.source.getActiveSheet();
  var column_name = sheet.getRange(1, col).getValue();

  // Get the entire row data
  var rowValues = sheet.getRange(row, 1, 1, sheet.getLastColumn()).getValues()[0];

  // Prepare data to send to the Flask app
  var data = {
    "row": row,
    "column_name": column_name,
    "new_value": newValue,
    "old_value": oldValue,  // Send old value to the backend
    "action": "update", // Default action
    "row_data": rowValues // All data from the row
  };

  // Check if the entire row is now empty
  var isEmptyRow = rowValues.every(cell => cell === "" || cell === null);

  if (isEmptyRow) {
    // Set action to delete
    data.new_value = "";
    data.action = "delete";
  }

  // Send a POST request to the Flask webhook
  var options = {
    'method': 'POST',
    'contentType': 'application/json',
    'payload': JSON.stringify(data)
  };

  // Trigger the webhook
  UrlFetchApp.fetch(webhookUrl, options);
}
