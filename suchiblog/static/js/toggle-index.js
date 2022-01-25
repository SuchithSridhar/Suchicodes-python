$('.arrow').on('click', function(e){
    if ($(".arrow").hasClass('open')) {
        $(".arrow").removeClass('open');
        $(".index-container").removeClass('open');

        $(".arrow").addClass('close');
        $(".index-container").addClass('close');
        $(".arrow").html('&#8250;');
    } else {
        $(".arrow").removeClass('close');
        $(".index-container").removeClass('close');

        $(".arrow").addClass('open');
        $(".index-container").addClass('open');
        $(".arrow").html('&#8249;');
    }
})
