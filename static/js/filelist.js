function showRenameField(button) {
    if (button) {
        const renameForm = button.nextElementSibling;
        if (renameForm && renameForm.classList.contains('rename-form')) {
            button.style.display = 'none';
            renameForm.style.display = 'block';
            const inputField = renameForm.querySelector('input[name="new_name"]');
            if (inputField) {
                inputField.focus();
            } else {
                console.error("Input field not found in the rename form.");
            }
        } else {
            console.error("Rename form not found or incorrect structure.");
        }
    } else {
        console.error("Button element is null or undefined.");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById('flexCheckDefault');
    const deleteAllForm = document.getElementById('delete-all');
    if (selectAllCheckbox) {
        selectAllCheckbox.addEventListener('change', function() {
            if (this.checked) {
                deleteAllForm.style.display = 'block';
            } else {
                deleteAllForm.style.display = 'none';
            }
        });
    }

    const items = document.querySelectorAll("#fileList .list-item");
    let index = 0;
    const interval = setInterval(function () {
        if (index >= items.length) {
            clearInterval(interval);
            return;
        }
        items[index].style.opacity = "1";
        items[index].style.transform = "translateY(0)";
        index++;
    }, 200);
});

/**
 *  comment controller
 */
$('.open-modal').click(function(){
    var uploadId = $(this).data('upload-id');
    var modalId = '#exampleModal_' + uploadId;
    $(modalId).modal('show');
});

$('.save-button').click(function(){
    var uploadId = $(this).data('upload-id');
    var formId = '#commentForm_' + uploadId;
    $(formId).submit();

});
