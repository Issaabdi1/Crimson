var profilePopup = document.getElementById("ProfilePopup");
var invitePopup = document.getElementById("InvitePopup");

if (invitePopup) {
    document.addEventListener("DOMContentLoaded", function () {
        invitePopup.addEventListener("click", function () {
                document.getElementById("popupContainer").style.display = "block";
                document.getElementById("sidebar").style.zIndex = "999";
                setTimeout(function () {
                    document.getElementById("popupContainer").classList.add("active");
                }, 10);
            }
        );

        const elements = document.querySelectorAll('.fade-in');
        elements.forEach(function (element, index) {
            setTimeout(function () {
                element.classList.add('visible');
            }, index * 75);
        });
    });
}

if (profilePopup) {
    document.addEventListener("DOMContentLoaded", function () {
        profilePopup.addEventListener("click", function () {
            document.getElementById("popupContainer").style.display = "block";
            setTimeout(function () {
                document.getElementById("popupContainer").classList.add("active");
            }, 10);
        });
    });
}

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("closePopup").addEventListener("click", function () {
        document.getElementById("popupContainer").classList.remove("active");
        setTimeout(function () {
            document.getElementById("popupContainer").style.display = "none";
        }, 300);
    });
});