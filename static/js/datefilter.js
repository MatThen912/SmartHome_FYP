let minDate, maxDate;
 
// Custom filtering function which will search data in column four between two values
$.fn.dataTable.ext.search.push(
    function( settings, data, dataIndex ) {
        let min = minDate.val();
        let max = maxDate.val();
        let date = new Date( data[0] );
 
        if (
            ( min === null && max === null ) ||
            ( min === null && date <= max ) ||
            ( min <= date   && max === null ) ||
            ( min <= date   && date <= max )
        ) {
            return true;
        }
        return false;
    }
);

$(document).ready(function() {
    // Create date inputs
    minDate = new DateTime($('#min'), {
        format: 'MMM DD, YYYY'
    });
    maxDate = new DateTime($('#max'), {
        format: 'MMM DD, YYYY'
    });
 
    // DataTables initialisation
    const table = $('#dataTable').DataTable({
        language: {
          oPaginate: {
            sNext: '<i class="fa fa-angle-right"></i>',
            sPrevious: '<i class="fa fa-angle-left"></i>',
          }
        }  
    })
 
    // Refilter the table
    $('#min, #max').on('change', function () {
        table.draw();
    });
});