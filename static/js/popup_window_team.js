var createTeamPopup = document.getElementById("CreateTeamPopup");
var joinTeamPopup = document.getElementById("JoinTeamPopup");

document.addEventListener("DOMContentLoaded", function () {
    createTeamPopup.addEventListener("click", function () {
        document.getElementById("popupContainerCreate").style.display = "block";
        document.getElementById("sidebar").style.zIndex = "999";
        setTimeout(function () {
            document.getElementById("popupContainerCreate").classList.add("active");
        }, 10);
    });

    joinTeamPopup.addEventListener("click", function () {
        document.getElementById("popupContainerJoin").style.display = "block";
        document.getElementById("sidebar").style.zIndex = "999";
        setTimeout(function () {
            document.getElementById("popupContainerJoin").classList.add("active");
        }, 10);
    });

    document.getElementById("closePopupCreate").addEventListener("click", function () {
        document.getElementById("popupContainerCreate").classList.remove("active");
        setTimeout(function () {
            document.getElementById("popupContainerCreate").style.display = "none";
        }, 300);
    });
    document.getElementById("closePopupJoin").addEventListener("click", function () {
        document.getElementById("popupContainerJoin").classList.remove("active");
        setTimeout(function () {
            document.getElementById("popupContainerJoin").style.display = "none";
        }, 300);
    });

    const teams = document.querySelectorAll(".teams-list .team-item");
    let index = 0;
    const interval = setInterval(function () {
        if (index >= teams.length) {
            clearInterval(interval);
            return;
        }
        teams[index].style.opacity = "1";
        teams[index].style.transform = "translateY(0)";
        index++;
    }, 200);
});

