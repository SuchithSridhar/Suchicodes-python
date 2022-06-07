$('.arrow').on('click', function(e){
    arrow_open = "&#8250;INDEX"
    arrow_close = "&#8249;INDEX"
    if ($(".arrow").hasClass('open')) {
        $(".arrow").removeClass('open');
        $(".index-container").removeClass('open');

        $(".arrow").addClass('close');
        $(".index-container").addClass('close');
        $(".arrow").html(arrow_open);
    } else {
        $(".arrow").removeClass('close');
        $(".index-container").removeClass('close');

        $(".arrow").addClass('open');
        $(".index-container").addClass('open');
        $(".arrow").html(arrow_close);
    }
})
