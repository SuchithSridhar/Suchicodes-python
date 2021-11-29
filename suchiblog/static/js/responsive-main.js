const outputElement = document.getElementById("info");
const smallDevice = window.matchMedia("(max-width: 1000px)");

smallDevice.addListener(handleDeviceChange);

function handleDeviceChange(e) {
  if (e.matches) {
      $("#tab-list").removeClass('col-sm-2');
      $("#tab-container").removeClass('col-sm-10');
  }
  else {
      $("#tab-list").addClass('col-sm-2');
      $("#tab-container").addClass('col-sm-10');
  }
}

handleDeviceChange(smallDevice);