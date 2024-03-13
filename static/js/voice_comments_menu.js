document.addEventListener("DOMContentLoaded", function() {
    const collapseButton = document.getElementById("collapseButton");
    const collapseMenu = document.getElementById("collapseMenu");

    collapseButton.addEventListener("click", function() {
        if (collapseMenu.style.display == "none" || collapseMenu.style.display == "") {
            collapseMenu.style.display = "block";
            collapseButton.classList.add("rotate-down");
        } else {
            collapseMenu.style.display = "none";
            collapseButton.classList.remove("rotate-down");
        }
    });
});