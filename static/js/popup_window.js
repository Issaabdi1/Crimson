var profilePopup = document.getElementById("ProfilePopup");
if (profilePopup) {
    profilePopup.addEventListener("click", function () {
        document.getElementById("popupContainer").style.display = "block";
    });
}

var invitePopup = document.getElementById("InvitePopup");
if (invitePopup) {
    invitePopup.addEventListener("click", function () {
        document.getElementById("popupContainer").style.display = "block";
    });
}

var createTeamPopup = document.getElementById("CreateTeamPopup");
if (createTeamPopup) {
    createTeamPopup.addEventListener("click", function () {
        document.getElementById("popupContainer").style.display = "block";
        document.getElementById("sidebar").style.zIndex = "999";
    });
}

document.getElementById("closePopup").addEventListener("click", function () {
    document.getElementById("popupContainer").style.display = "none";
    if(document.getElementById("sidebar")) {
        document.getElementById("sidebar").style.zIndex = "0";
    }
});