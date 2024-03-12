// filelist.js
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

function hideRenameField(button) {
    const renameForm = button.parentElement;
    const uploadId = renameForm.getAttribute('data-upload-id');
    const renameButton = document.querySelector(`#renameButton_${uploadId}`);

    if (renameButton) {
        renameForm.style.display = 'none';
        renameButton.style.display = 'inline-block';
    } else {
        console.error("Unable to find the Rename button.");
    }
}

function confirmRename(form) {
    const cardTitle = form.parentElement.querySelector('.card-title');
    if (cardTitle) {
        const currentName = cardTitle.textContent.trim();
        const newName = form.new_name.value.trim();
        if (newName && newName !== currentName) {
            form.submit();
        } else if (newName === currentName) {
            alert("The new name must be different from the current name.");
        } else {
            alert("The new name cannot be empty.");
        }
    } else {
        console.error("Unable to find .card-title element");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById('flexCheckDefault');
    const deleteAllForm = document.getElementById('delete-all');
    selectAllCheckbox.addEventListener('change', function() {
        if (this.checked) {
            deleteAllForm.style.display = 'block';
        } else {
            deleteAllForm.style.display = 'none';
        }
    });
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

document.addEventListener("DOMContentLoaded", function () {
    const selectAllCheckbox = document.getElementById('flexCheckDefault');
    const deleteAllForm = document.getElementById('delete-all');
    selectAllCheckbox.addEventListener('change', function() {
        if (this.checked) {
            deleteAllForm.style.display = 'block';
        } else {
            deleteAllForm.style.display = 'none';
        }
    });
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
