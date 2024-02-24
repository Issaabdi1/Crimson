/* This function is run when the notifications popup is pressed
* Runs view to set all the notifications of the current to read 
*/ 
function set_notifications_as_read(){
    const xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/set_notifications_as_read/");
    xhttp.send();
    //Clear alert on notification symbol
    var alert = document.getElementById("notification-alert");
    if(alert!=null){
        document.getElementById("notification-alert").setAttribute("hidden", true);
    }
    return true; //Show the request has been sent successfully
}