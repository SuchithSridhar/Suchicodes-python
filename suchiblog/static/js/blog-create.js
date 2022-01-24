// how to use function:
// addTabListner(document.getElementById('textbox'))
// This converts all tabs to 4 spaces
function tabListner (input_field) {
    input_field.addEventListener('keydown', function(e){
        if (e.key == 'Tab') {
            convertValue = "    ";
            e.preventDefault();
            var start = this.selectionStart;
            var end = this.selectionEnd;

            // set textarea value to: text before caret + tab + text after caret
            this.value = this.value.substring(0, start) +
              convertValue + this.value.substring(end);

            // put caret at right position again
            this.selectionStart =
            this.selectionEnd = start + 1;
        }
    });
}

function make_id(length) {
  var result           = '';
  var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * 
    charactersLength));
  }
  return result;
};

function get_uuid(table, filename){
  rows = table.find('tr');
  for (let i=0; i<rows.length; i++){
      row = $(rows[i]);
      if ($(row.find('.data-filename')[0]).text() == filename) return($(row.find('.data-uuid')[0]).text());
  };
};

tabListner(document.getElementById('markdown-input'));

$('#submit-btn').on('click', ()=>{
    $('#category-input').val($('#select-group').val());
    let data = "";
    let tbody = $("#table-body");
    let rows = tbody.find('tr');
    for(let r=0; r<rows.length; r++){
      data+= $(rows[r]).find('.data-filename').text();
      data+= "###";
      data+= $(rows[r]).find('.data-uuid').text();
      data+= ",";
    };
    data = data.slice(0, -1);
    $('#uuids-input').val(data);
    $('#create-form').submit();
});

$('#process-btn').on('click', (e)=>{
  e.preventDefault();
  let files = $('#fileinput').prop('files');
  let tbody = $('#table-body');
  let content = tbody.html();
  let html = "";
  for(let i=0; i<files.length; i++){
    html += `<tr><td class='data-filename'>${files[i].name}</td>`;
    if (content.includes(files[i].name)) html += `<td class='data-uuid'>${get_uuid(tbody, files[i].name)}</td></tr>`; 
    else html += `<td class='data-uuid'>${make_id(8)}</td></tr>`; 
  };
  tbody.html(html);
});
