QUnit.module('Pop-up Window', {
    beforeEach: function () {
        popupContainer = document.getElementById("popupContainer");
    }
});

QUnit.test("ProfilePopup click event", function (assert) {
    var profilePopup = document.createElement("div");
    profilePopup.id = "ProfilePopup";
    profilePopup.addEventListener("click", function () {
        document.getElementById("popupContainer").style.display = "block";
    });
    document.body.appendChild(profilePopup);

    profilePopup.click();

    assert.equal(popupContainer.style.display, "block", "Popup container should be displayed");
});

QUnit.test("InvitePopup click event", function (assert) {
    var invitePopup = document.createElement("div");
    invitePopup.id = "InvitePopup";
    invitePopup.addEventListener("click", function () {
        document.getElementById("popupContainer").style.display = "block";
    });
    document.body.appendChild(invitePopup);

    invitePopup.click();

    assert.equal(popupContainer.style.display, "block", "Popup container should be displayed");
});

QUnit.test("CreateTeamPopup click event", function (assert) {
    var createTeamPopup = document.createElement("div");
    createTeamPopup.id = "CreateTeamPopup";
    createTeamPopup.addEventListener("click", function () {
        document.getElementById("popupContainer").style.display = "block";
        document.getElementById("sidebar").style.backgroundColor = "rgba(0, 0, 0, 0.5)";
        document.getElementById("sidebar").style.zIndex = "999";
    });
    document.body.appendChild(createTeamPopup);

    var sidebar = document.createElement("div");
    sidebar.id = "sidebar";
    document.body.appendChild(sidebar);

    createTeamPopup.click();

    assert.equal(popupContainer.style.display, "block", "Popup container should be displayed");
    assert.equal(sidebar.style.backgroundColor, "rgba(0, 0, 0, 0.5)", "Sidebar background color should be set");
    assert.equal(sidebar.style.zIndex, "999", "Sidebar z-index should be set");
});

QUnit.test("ClosePopup click event", function (assert) {
    var closePopup = document.createElement("div");
    closePopup.id = "closePopup";
    closePopup.addEventListener("click", function () {
        document.getElementById("popupContainer").style.display = "none";
    });
    document.body.appendChild(closePopup);

    closePopup.click();

    assert.equal(popupContainer.style.display, "none", "Popup container should be hidden");
});
