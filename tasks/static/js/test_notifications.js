//Tests for notifications
QUnit.module('notifications', {
    beforeEach: function()
    {
        // Setup
        //get all the buttons
        delete_all_button = document.querySelector('button[type=submit]');
        delete_button = document.querySelector('button[type=button]');

        const btns = document.querySelectorAll('#remove-notification');
        received_response = false; //shows if a response has been sent by the javascript function
        btns.forEach(btn => {
          btn.addEventListener('click', event => {
            //pass true to the function to show it is being used for tests
            received_response = reload_notifications(btn.getAttribute("value"), true); 
          });
        });
    }});

    // Test delete notification button
    QUnit.test('delete notification button sends an xml response', function(assert) {
        delete_button.click();
        
        // Check that the function was run
        assert.equal(received_response, true);
    });

    // Test dismiss all button
    QUnit.test('dismiss all button triggers sends an xml response', function(assert) {
        delete_all_button.click();

        // Check that the function was run
        assert.equal(received_response, true);
    });

    // Test reload notifications function
    QUnit.test('dismiss all button disappears when there are no notifications', function(assert) {
        delete_all_button.click();
        display = document.getElementById('dismiss-notifications');

        var done = assert.async();
        //Wait for a time, and assert that the dismiss all button has disappeared
        setTimeout(function() {
            // Check that the dismiss all button is hidden
            assert.equal(display.style.display, "none");
    
            // Call done to signal that the test is complete
            done();
        }, 1000); // Wait for 1000 milliseconds (1 second)

    });


