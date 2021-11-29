const chk = document.getElementById('chk');

function toggle_mode() {
    let light = getComputedStyle(document.documentElement).getPropertyValue('--color-background');
    let dark = getComputedStyle(document.documentElement).getPropertyValue('--color-foreground');

    document.documentElement.style.setProperty('--color-background', dark);
    document.documentElement.style.setProperty('--color-foreground', light);

    let mode = "light";
    if ($('nav').hasClass('navbar-light')) {
        $('nav').removeClass('navbar-light');
        $('nav').addClass('navbar-dark');

        let dots_dark = getComputedStyle(document.documentElement).getPropertyValue('--dots-image-dark');
        document.documentElement.style.setProperty('--dots-image', dots_dark);

        mode = "dark";
    } else {
        $('nav').removeClass('navbar-dark');
        $('nav').addClass('navbar-light');

        let dots_light = getComputedStyle(document.documentElement).getPropertyValue('--dots-image-light');
        document.documentElement.style.setProperty('--dots-image', dots_light);
    }

    $.ajax({
        url: `/session/set/${mode}`,
    }); 
}

chk.addEventListener('change', () => {
	document.body.classList.toggle('chk');
    let label = document.querySelector(".label");
    let label_color = document.querySelector(".label").style.backgroundColor;
    if (label_color == 'white') label.style.backgroundColor = 'black';
    else label.style.backgroundColor = 'white';
    toggle_mode();
});

$.ajax({
    url: "/session/get",
    success: function(result){
        console.log(result);
        if (result == "dark") {
            $(".dark-mode-div .ball").click();
        }
    }
}); 
