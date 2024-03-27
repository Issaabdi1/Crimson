//<!--JavaScript to delete the notifications when their delete button is pressed-->

/* This function is run when the delete button or the dismiss all button is pressed
* Runs view to delete the relevant notifications, and then gets back the updated notification list  
*/
function delete_notifications(id, forTests = false) {
    //pass parameters through url
    var parameters = "?notification_id=" + id + "&forTests=" + forTests;
    var notificationCards = document.querySelectorAll('.notification-card');
    
    //If there are no cards left, then hide the dismiss all button
    if (notificationCards.length <= 0) {
        var element = document.querySelector('#dismiss-notifications');
        element.style.display = "none";
    }

    //Send the request to delete the notification from the server
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/process_notification_delete/" + parameters);
    xhttp.send();
    return true; //Show the request has been sent successfully
}

//Add listener to every remove notification button to run the above method
const btns = document.querySelectorAll('#remove-notification');
btns.forEach(btn => {
    btn.addEventListener('click', event => {
        delete_notifications(btn.getAttribute("value"));
    });

});