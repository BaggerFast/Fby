reset_filters.addEventListener("click", function () {
    checkboxes = document.querySelectorAll(".dropdown-item-no-active input[type=\"checkbox\"]");
    for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = false;
    }
});
