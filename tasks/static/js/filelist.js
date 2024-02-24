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

function openLink(url) {
    window.location.href = url;
}