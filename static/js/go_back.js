go_back.addEventListener("click", function () {
    const urlParams = new URLSearchParams(window.location.search);
    urlParams.set("no_search", "true");
    window.location.search = urlParams;
});
