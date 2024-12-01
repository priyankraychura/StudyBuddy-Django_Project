$(document).ready(function () {
    $('.enableBtn').click(function () {
        var $row = $(this).closest('tr');
        $row.find('.myInput').prop("disabled", false);
        $(this).hide();
        $row.find('.saveBtn').show();
        $row.find('.cancelBtn').show();

        $row.find('.viewBtn').hide();
        $row.find('.deleteBtn').hide();
    });

    $('.cancelBtn').click(function () {
        var $row = $(this).closest('tr');
        $row.find('.myInput').prop("disabled", true);
        $(this).hide();
        $row.find('.saveBtn').hide();
        $row.find('.enableBtn').show();

        $row.find('.viewBtn').show();
        $row.find('.deleteBtn').show();
    });
});