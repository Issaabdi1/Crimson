var profilePopup = document.getElementById("ProfilePopup");
if (profilePopup) {
    profilePopup.addEventListener("click", function () {
        document.getElementById("popupContainer").style.display = "block";
    });
}

document.getElementById("closePopup").addEventListener("click", function () {
    document.getElementById("popupContainer").style.display = "none";
});

