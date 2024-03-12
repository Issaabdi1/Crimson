document.getElementById("CreateTeamPopup").addEventListener("click", function () {
    document.getElementById("popupContainer").style.display = "block";
    // document.getElementById("sidebar").style.backgroundColor = "rgba(0, 0, 0, 0.5)";
    document.getElementById("sidebar").style.zIndex = "999";
    setTimeout(function() {
        document.getElementById("popupContainer").classList.add("active");
    }, 10);
});

document.getElementById("closePopup").addEventListener("click", function () {
    document.getElementById("popupContainer").classList.remove("active");
    setTimeout(function() {
        document.getElementById("popupContainer").style.display = "none";
    }, 300);
});

document.addEventListener("DOMContentLoaded", function () {
    const teams = document.querySelectorAll(".teams-list .team-item");
    let index = 0;
    const interval = setInterval(function() {
        if (index >= teams.length) {
            clearInterval(interval);
            return;
        }
        teams[index].style.opacity = "1";
        teams[index].style.transform = "translateY(0)";
        index++;
    }, 200);
});