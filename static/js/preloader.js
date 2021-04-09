var hellopreloader = document.getElementById("hellopreloader");
var hellopreloader_preload = document.getElementById("hellopreloader_preload");
var button_loader = document.getElementById("button_loader");
function fadeOutnojquery(el) {
    el.style.opacity = 1;
    var interhellopreloader = setInterval(function () {
        el.style.opacity = el.style.opacity - 0.05;
        if (el.style.opacity <= 0.05) {
            clearInterval(interhellopreloader);
            hellopreloader_preload.style.display = "none";
        }
    }, 16);
}
button_loader.addEventListener("click", function() {
    hellopreloader.style.opacity = 1;
    hellopreloader_preload.style.opacity = 1;
    hellopreloader.style.display = "block";
    hellopreloader_preload.style.display = "block";
});
