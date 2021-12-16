$('#submit-btn').on('click', ()=>{
    $('#category-input').val($('#select-group').val());
    $('#create-form').submit();
});