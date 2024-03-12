document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("InvitePopup").addEventListener("click", function () {
        document.getElementById("popupInviteContainer").style.display = "block";
        document.getElementById("sidebar").style.zIndex = "999";
        setTimeout(function() {
            document.getElementById("popupInviteContainer").classList.add("active");
        }, 10);
    });

    document.getElementById("closeInvitePopup").addEventListener("click", function () {
        document.getElementById("popupInviteContainer").classList.remove("active");
        setTimeout(function() {
            document.getElementById("popupInviteContainer").style.display = "none";
        }, 300);
    });

    const elements = document.querySelectorAll('.fade-in');
    elements.forEach(function(element, index) {
        setTimeout(function() {
            element.classList.add('visible');
        }, index * 75);
    });
});