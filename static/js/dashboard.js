// dashboard.js

/**
 * double click active
 */
$(document).ready(function(){
    $('#selectAll').change(function(){
        if(this.checked){
            $('.row-checkbox').prop('checked', true);
            $('tbody tr').addClass('table-active');
        } else {
            $('.row-checkbox').prop('checked', false);
            $('tbody tr').removeClass('table-active');
        }
    });

    $('.row-checkbox').change(function(){
        if(this.checked){
            $(this).closest('tr').addClass('table-active');
            if($('.row-checkbox:checked').length == $('.row-checkbox').length){
                $('#selectAll').prop('checked', true);
            }
        } else {
            $(this).closest('tr').removeClass('table-active');
            $('#selectAll').prop('checked', false);
        }
    });

    $('tbody tr').dblclick(function(){
        var checkbox = $(this).find('.row-checkbox');
        if (checkbox.prop('checked')) {
            checkbox.prop('checked', false);
            $(this).removeClass('table-active');
        } else {
            checkbox.prop('checked', true);
            $(this).addClass('table-active');
        }
    });

    $('tbody tr').hover(function(){
        $(this).addClass('table-active');
    }, function(){
        $(this).removeClass('table-active');
    });
});


/**
 * sort function
 */

$(document).ready(function() {
    // Function to sort the table data based on column index and order
    function sortTable(columnIndex, order) {
        const rows = $('#dataTable tbody tr').get();

        rows.sort(function(a, b) {
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

        $.each(rows, function(index, row) {
            $('#dataTable tbody').append(row);
        });
    }

    // Click event handler for the sort buttons
    $('.icon-btn').click(function() {
        var columnIndex = $(this).closest('th').index();
        var order = $(this).hasClass('asc') ? 'desc' : 'asc';

        // Remove 'asc' and 'desc' classes from all buttons
        $('.icon-btn').removeClass('asc desc');

        // Add 'asc' or 'desc' class to the clicked button
        $(this).addClass(order);

        // Call the sort function
        sortTable(columnIndex, order);
    });
});
