
$(document).ready(function() {
    $('#store').change(function() {
        var store = $(this).val();
        if (store) {
            $.ajax({
                type: 'POST',
                url: '/get_dates',
                data: {store: store},
                success: function(dates) {
                    $('#date').empty();
                    $('#date').append('<option value="">Select Date</option>');
                    $.each(dates, function(index, date) {
                        $('#date').append('<option value="'+ date +'">'+ date +'</option>');
                    });
                }
            });
        }
    });

    $('#salesForm').submit(function(e) {
        e.preventDefault();
        var store = $('#store').val();
        var date = $('#date').val();
        if (store && date) {
            $.ajax({
                type: 'POST',
                url: '/get_sales',
                data: {store: store, date: date},
                success: function(sales) {
                    $('#salesValue').text('Sales: ' + sales);
                }
            });
        }
    });
});