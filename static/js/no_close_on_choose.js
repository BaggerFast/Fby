document.querySelectorAll(".no-close-on-choose").forEach(element => {
	element.addEventListener("hide.bs.dropdown", function (e) {
		if (e.clickEvent && e.clickEvent.target.closest(".no-close-on-choose")) {
		  e.preventDefault();
		}
	});
});
