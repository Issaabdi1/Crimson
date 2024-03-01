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
