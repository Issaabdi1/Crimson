// dashboard.js

/**
 * double click active
 */

$(document).ready(function () {
    // Add click event to each checkbox
    $('.row-checkbox').on('click', function () {
        // Toggle active class for the parent row
        $(this).closest('tr').toggleClass('table-active');
    });
});

/**
 * search bar
 */
$(document).ready(function () {
    $("#searchInput").on("input", function () {
        var searchText = $(this).val().trim();
        var regex = new RegExp(searchText, "i");
        $("#dataTable tbody tr").hide().filter(function () {
            return regex.test($(this).text());
        }).show();
    });
});
$(document).ready(function () {
    $('#selectAll').change(function () {
        if (this.checked) {
            $('.row-checkbox').prop('checked', true);
            $('tbody tr').addClass('table-active');
        } else {
            $('.row-checkbox').prop('checked', false);
            $('tbody tr').removeClass('table-active');
        }
    });

    $('.row-checkbox').change(function () {
        if (this.checked) {
            $(this).closest('tr').addClass('table-active');
            if ($('.row-checkbox:checked').length == $('.row-checkbox').length) {
                $('#selectAll').prop('checked', true);
            }
        } else {
            $(this).closest('tr').removeClass('table-active');
            $('#selectAll').prop('checked', false);
        }
    });

    $('tbody tr').dblclick(function () {
        var checkbox = $(this).find('.row-checkbox');
        if (checkbox.prop('checked')) {
            checkbox.prop('checked', false);
            $(this).removeClass('table-active');
        } else {
            checkbox.prop('checked', true);
            $(this).addClass('table-active');
        }
    });

    $('tbody tr').hover(function () {
        $(this).addClass('table-active');
    }, function () {
        $(this).removeClass('table-active');
    });
});


/**
 * sort function
 */

$(document).ready(function () {
// Function to sort the table data based on column index and order
    function sortTable(columnIndex, order) {
        const rows = $('#dataTable tbody tr').get();

        rows.sort(function (a, b) {
            const aValue = $(a).find('td').eq(columnIndex).text();
            const bValue = $(b).find('td').eq(columnIndex).text();

            if (columnIndex === 1 || columnIndex === 3) { // ID or Owner - sort as numbers
                return order === 'asc' ? (parseInt(aValue) - parseInt(bValue)) : (parseInt(bValue) - parseInt(aValue));
            } else if (columnIndex === 2) { // File Name - sort alphabetically
                return order === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
            } else if (columnIndex === 4) { // Uploaded At - sort chronologically
                return order === 'asc' ? (new Date(aValue) - new Date(bValue)) : (new Date(bValue) - new Date(aValue));
            } else if (columnIndex === 6) { // Size - sort as numbers
                const aSize = parseFloat(aValue.split(' ')[0]);
                const bSize = parseFloat(bValue.split(' ')[0]);
                return order === 'asc' ? (aSize - bSize) : (bSize - aSize);
            }
        });

        $.each(rows, function (index, row) {
            $('#dataTable tbody').append(row);
        });
    }

// Click event handler for the sort buttons
    $('.icon-btn').click(function () {
        const columnIndex = $(this).closest('th').index();
        const order = $(this).hasClass('asc') ? 'desc' : 'asc';

        // Remove 'asc' and 'desc' classes from all buttons
        $('.icon-btn').removeClass('asc desc');

        // Add 'asc' or 'desc' class to the clicked button
        $(this).addClass(order);

        // Call the sort function
        sortTable(columnIndex, order);
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const collapseSection = document.getElementById('collapseExample');
    const collapseButton = document.querySelector('[data-bs-target="#collapseExample"]');

    if (collapseButton) {
        collapseButton.addEventListener('click', function () {
            const isCollapsed = !collapseSection.classList.contains('show');
            localStorage.setItem('collapseState', isCollapsed);
            console.log("localstorage click!");
        });
    } else {
        console.log("Collapse button not found");
    }

    const storedState = localStorage.getItem('collapseState') === 'true';

    if (collapseSection) {
        if (storedState) {
            collapseSection.classList.add('show');
        } else {
            collapseSection.classList.remove('show');
        }
    }
});

/**
 * submit selected form handler
 */
$(document).ready(function () {
    // Function to submit forms of selected rows
    function submitSelectedForms() {
        if ($('.row-checkbox:checked').length < 1) {
            alert('Please select at least one file to delete.');
        } else {
            // Iterate over each checkbox
            $('.row-checkbox:checked').each(function () {
                // Find the closest 'tr' parent, then find the form within that row and submit it
                $(this).closest('tr').find('form').submit();
            });
        }
    }

    // Attach the function to the "View Selected" button click event
    $('#viewSelected').on('click', function () {
        submitSelectedForms();
    });
});

/**
 * download file handler
 */

$(document).ready(function () {
    $('#downloadSelected').on('click', function () {
        const selectedRows = $('.row-checkbox:checked');
        if (selectedRows.length === 1) {
            // Direct download for single file
            const uploadId = selectedRows.closest('tr').data('upload-id');
            window.location.href = `/download-single/${uploadId}`; // Update with your actual endpoint
        } else if (selectedRows.length > 1) {
            // Prepare data for zipped download
            let uploadIds = [];
            selectedRows.each(function () {
                uploadIds.push($(this).closest('tr').data('upload-id'));
            });

            // Assuming you're using a method to handle POST requests
            // You might need to adjust this to your specific backend handling
            fetch('/download_multiple/', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                },
                body: JSON.stringify({upload_ids: uploadIds}),
            }).then(response => {
                if (response.ok) return response.blob();
                throw new Error('Network response was not ok.');
            }).then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = "downloads.zip"; // Or any filename you wish to give
                document.body.appendChild(a); // Required for Firefox
                a.click();
                a.remove();
            }).catch(error => console.error('Error:', error));
        } else {
            // No selection made
            alert('Please select one or more files to download.');
        }
    });
});

$(document).ready(function () {
    $('#deleteSelected').on('click', function () {
        const selectedUploadIds = $('.row-checkbox:checked').map(function () {
            return $(this).closest('tr').data('upload-id');
        }).get();

        if (selectedUploadIds.length > 0) {
            if (!confirm('Are you sure you want to delete the selected files?')) {
                return;  // User canceled the action
            }

            // Send the IDs to the server for deletion
            fetch('/delete_selected_uploads/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(), // Ensure CSRF token is sent
                },
                body: JSON.stringify({upload_ids: selectedUploadIds}),
            })
                .then(response => {
                    if (response.ok) {
                        // Reload or update the page content
                        location.reload();  // Simple way to update the page content
                    } else {
                        throw new Error('Something went wrong');
                    }
                })
                .catch(error => console.error('Error:', error));
        } else {
            alert('Please select at least one file to delete.');
        }
    });
});

function getCsrfToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}
