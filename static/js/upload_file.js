// // upload_file.js

/**
 * close button
 * @type {NodeListOf<Element>}
 */
var closeButtons = document.querySelectorAll('.btn-close');

// Loop through each close button
closeButtons.forEach(function(button) {
    // Add click event listener
    button.addEventListener('click', function() {
        // Find the parent div and remove it
        var parentDiv = button.closest('.uploaded-file');
        if (parentDiv) {
            parentDiv.remove();
        }
    });
});