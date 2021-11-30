const chk = document.getElementById('chk');

function toggle_mode() {
    let light = getComputedStyle(document.documentElement).getPropertyValue('--color-background');
    let dark = getComputedStyle(document.documentElement).getPropertyValue('--color-foreground');
    let light_gray = getComputedStyle(document.documentElement).getPropertyValue('--color-light-gray');
    let dark_gray = getComputedStyle(document.documentElement).getPropertyValue('--color-dark-gray');

    document.documentElement.style.setProperty('--color-background', dark);
    document.documentElement.style.setProperty('--color-foreground', light);
    document.documentElement.style.setProperty('--color-light-gray', dark_gray);
    document.documentElement.style.setProperty('--color-dark-gray', light_gray);

    let mode = "light";
    if ($('nav').hasClass('navbar-light')) {
        $('nav').removeClass('navbar-light');
        $('nav').addClass('navbar-dark');

        let dots_dark = getComputedStyle(document.documentElement).getPropertyValue('--dots-image-dark');
        let hex_dark = getComputedStyle(document.documentElement).getPropertyValue('--hex-image-dark');
        document.documentElement.style.setProperty('--dots-image', dots_dark);
        document.documentElement.style.setProperty('--hex-image', hex_dark);

        mode = "dark";
    } else {
        $('nav').removeClass('navbar-dark');
        $('nav').addClass('navbar-light');

        let dots_light = getComputedStyle(document.documentElement).getPropertyValue('--dots-image-light');
        let hex_light = getComputedStyle(document.documentElement).getPropertyValue('--hex-image-light');
        document.documentElement.style.setProperty('--dots-image', dots_light);
        document.documentElement.style.setProperty('--hex-image', hex_light);
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
        if (result == "dark") {
            $(".dark-mode-div .ball").click();
        }
    }
}); 
