// // upload_file.js

/**
 * close button
 * @type {NodeListOf<Element>}
 */
var closeButtons = document.querySelectorAll('.btn-close');

// Loop through each close button
closeButtons.forEach(function (button) {
    // Add click event listener
    button.addEventListener('click', function () {
        // Find the parent div and remove it
        var parentDiv = button.closest('.uploaded-file');
        if (parentDiv) {
            parentDiv.remove();
        }
    });
});

/**
 *  form upload listener
 */
document.addEventListener('DOMContentLoaded', function () {
    var fileIcon = document.getElementById('file-icon');
    var successIcon = document.getElementById('success-icon');
    var uploadInstruction = document.getElementById('upload-instruction');
    var successAlert = document.getElementById('success-alert');
    var fileName = document.getElementById('file-name')
    var fileInput = document.querySelector('input[type="file"]');
    var uploadButton = document.getElementById('upload-btn');

    successIcon.style.display = 'none';
    successAlert.style.display = 'none';
    fileInput.addEventListener('change', function () {
        if (fileInput.files.length > 0) {
            fileIcon.style.display = 'none';
            successIcon.style.display = 'block';
            uploadInstruction.style.display = 'none';
            successAlert.style.display = 'block';
            fileName.textContent = event.target.files[0].name;
        }
    });

    document.getElementById('upload-form').addEventListener('submit', function (event) {
        if (fileInput.files.length === 0) {
            alert('Please select a file!');
            event.preventDefault();
        } else {
            // Disable the upload button to prevent multiple submissions
            uploadButton.disabled = true;
        }
    });
});

// Function to enable the upload button after successful upload
function enableUploadButton() {
    var uploadButton = document.querySelector('button[type="submit"]');
    uploadButton.disabled = false;
}

document.addEventListener('DOMContentLoaded', function () {
    /*Drop and drag zone handler*/
    let dropArea = document.getElementById('drop_zone')

    dropArea.addEventListener('dragenter', preventDefaults, false)
    dropArea.addEventListener('dragover', preventDefaults, false)
    dropArea.addEventListener('dragleave', preventDefaults, false)
    dropArea.addEventListener('drop', preventDefaults, false)

    function preventDefaults(e) {
        e.preventDefault()
        e.stopPropagation()
    }

    dropArea.addEventListener('drop', handleDrop, false)

    function handleDrop(e) {
        e.preventDefault(); // Prevent default browser behavior (opening the file)

        const dt = e.dataTransfer;
        const files = dt.files;

        if (files.length > 1) {
            console.warn('Multiple file uploads are not supported yet.');
            return;
        }

        const fileInput = document.getElementById('file-input');

        // Assuming the file input has a single child element (the actual input)
        fileInput.children[0].files = files; // Assign the dropped file(s) to the file input

        var fileIcon = document.getElementById('file-icon');
        var successIcon = document.getElementById('success-icon');
        var uploadInstruction = document.getElementById('upload-instruction');
        var successAlert = document.getElementById('success-alert');
        var fileName = document.getElementById('file-name')

        if (fileInput.children[0].files.length > 0) {
            fileIcon.style.display = 'none';
            successIcon.style.display = 'block';
            uploadInstruction.style.display = 'none';
            successAlert.style.display = 'block';
            fileName.textContent = files[0].name;
        }
        console.log(`File dropped: ${fileName}`);
    }

    /*Progress bar handler*/
    document.getElementById('upload-form').addEventListener('submit', function (event) {
        var progressBar = document.getElementById("success-bar");
        var status = document.getElementById("status");

        progressBar.style.width = "0%";
        status.innerHTML = "0%";

        var duration = 800;
        var interval = 20;

        var startTime = new Date().getTime();

        function updateProgress() {
            var currentTime = new Date().getTime();
            var elapsedTime = currentTime - startTime;
            var percentComplete = (elapsedTime / duration) * 100;

            if (percentComplete > 100) {
                percentComplete = 100;
            }

            progressBar.style.width = Math.round(percentComplete) + "%";
            status.innerHTML = Math.round(percentComplete) + "%";

            if (percentComplete < 100) {
                setTimeout(updateProgress, interval);
            }
        }

        updateProgress();

    });
});