const chk = document.getElementById('chk');

function toggle_mode() {
    let light = getComputedStyle(document.documentElement).getPropertyValue('--color-light');
    let dark = getComputedStyle(document.documentElement).getPropertyValue('--color-dark');

    document.documentElement.style.setProperty('--color-light', dark);
    document.documentElement.style.setProperty('--color-dark', light);

    if ($('nav').hasClass('navbar-light')) {
        $('nav').removeClass('navbar-light');
        $('nav').addClass('navbar-dark');
    } else {
        $('nav').removeClass('navbar-dark');
        $('nav').addClass('navbar-light');
    }
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
