//<!--JavaScript to delete the notifications when their delete button is pressed-->

/* This function is run when the delete button or the dismiss all button is pressed
* Runs view to delete the relevant notifications, and then gets back the updated notification list  
*/ 
function process_notification_delete(id){
    var parameters = "?notification_id=" + id; //the parameters to send to the view
    const xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        //When the request has been received and the code has completed
        if (this.readyState == XMLHttpRequest.DONE) {
            var response = JSON.parse(xhttp.response);
            //If there are no notifications, hide the dismiss all button
            if(response['notifications'].length <=0){
                var element = document.querySelector('#dismiss-notifications');
                element.style.display = "none";
            }
        }   
    };
    //Send a request to the view
    xhttp.open("GET", "{% url 'process_notification'%}" + parameters); 
    xhttp.send();
}

console.log("SSS");
//Gets all the buttons that can delete notifications
const btns = document.querySelectorAll('#remove-notification');

console.log(btns);
//Add an event listener for every button to run the process_notification_delete method
//Pass in the "value" attribute of the btn which holds the id of the notification it is deleting
btns.forEach(btn => {
btn.addEventListener('click', event => {
    process_notification_delete(btn.getAttribute("value"));
});

});
  