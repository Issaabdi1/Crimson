//<!--JavaScript to delete the notifications when their delete button is pressed-->

/* This function is run when the delete button or the dismiss all button is pressed
* Runs view to delete the relevant notifications, and then gets back the updated notification list  
*/
function delete_notifications(id, forTests = false) {
    //pass parameters through url
    var parameters = "?notification_id=" + id + "&forTests=" + forTests;
    console.log(forTests);
    var notificationCards = document.querySelectorAll('.notification-card');
    notificationCards.forEach(card => {
        if (card.getAttribute("data-id") === id) {
            card.remove();
        }
    });
    console.log(id)
    if (notificationCards.length <= 1) {
        var element = document.querySelector('#dismiss-notifications');
        element.style.display = "none";
    } else {
        // Add a notification placeholder.
        const newNotificationCard = document.createElement('div');
        newNotificationCard.classList.add('card', 'card-body', 'mb-3', 'notification-card');
        newNotificationCard.id = 'closeable-card';
        newNotificationCard.style.display = 'none';
        newNotificationCard.dataset.id = '99999';
        const notificationCardsContainer = notificationCards[0].parentElement;
        notificationCardsContainer.insertBefore(newNotificationCard, notificationCards[0]);
    }
    //Send the deletion request asynchronously
    // fetch(`/process_notification_delete/` + parameters)
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log("Notification deletion request processed:", data);
    //     })
    //     .catch(error => {
    //         console.error("Error deleting notification:", error);
    //     });
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