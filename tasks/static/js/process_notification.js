//<!--JavaScript to delete the notifications when their delete button is pressed-->

/* This function is run when the delete button or the dismiss all button is pressed
* Runs view to delete the relevant notifications, and then gets back the updated notification list  
*/ 
function reload_notifications(id, forTests = false){
    //pass parameters through url
    var parameters = "?notification_id=" + id + "&forTests=" + forTests;
    console.log(forTests);
    const xhttp = new XMLHttpRequest();
    //When the request has been dealt with, get the response
    xhttp.onreadystatechange = function() {
        if (this.readyState == XMLHttpRequest.DONE) {
            var response = JSON.parse(xhttp.response);
            //If there are no more notifications, disable the dismiss all button
            if(response['notifications'].length <=0){
              var element = document.querySelector('#dismiss-notifications');
              element.style.display = "none";
            }
        }
    };
    xhttp.open("GET", "/process_notification/" + parameters); 
    xhttp.send();
    return true; //Show the request has been sent successfully
  }

  //Add listener to every remove notification button to run the above method
  const btns = document.querySelectorAll('#remove-notification');

  btns.forEach(btn => {
    btn.addEventListener('click', event => {
        reload_notifications(btn.getAttribute("value"));
    });

  });