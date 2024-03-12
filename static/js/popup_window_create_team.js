document.getElementById("CreateTeamPopup").addEventListener("click", function () {
    document.getElementById("popupContainer").style.display = "block";
    document.getElementById("sidebar").style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    document.getElementById("sidebar").style.zIndex = "999";
});

document.getElementById("closePopup").addEventListener("click", function () {
    document.getElementById("popupContainer").style.display = "none";
});