// hook up script to DOM on document ready
$(function () {
    // form submission handler
    $('#ymmForm').on('submit', function (e) {
        e.preventDefault(); //suppress the default form submit behavior

        var theForm = $(this);

        $.getJSON('/carsearch', $(this).serialize(), function (data, status, jqXhr) {
            var results = data;

            $('#resultDiv .data-status').text(results.message);

            var rowContainer = $('#resultDiv .data-rows');
            rowContainer.empty();

            for (var i = 0; i < results.rows.length; i++) {
                var row = document.createElement('div');
                row.className = "row";

                for (key in results.rows[i]) {
                    var col = document.createElement('div');
                    col.className = "col-md";
                    col.textContent = results.rows[i][key];
                    row.appendChild(col);
                }

                rowContainer.append(row);
            }

        });
    });
});
