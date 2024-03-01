// upload_file.js

/**
 * form file utility
 */
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('pdf-upload-area').addEventListener('click', function() {
        document.querySelector('.input-file input[type=file]').click();
    });

    document.querySelector('.input-file input[type=file]').addEventListener('change', function() {
        document.getElementById('pdf-upload-form').submit();
    });
});

    document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('pdf-upload-area').addEventListener('click', function() {
        document.getElementById('pdf-file-input').click();
    });

    document.getElementById('pdf-upload-area').addEventListener('change', function() {
        document.getElementById('pdf-upload-form').submit();
    });
});