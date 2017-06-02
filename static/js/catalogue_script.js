$(document).ready(function () {
        $('#rating_form select').change(function (e) {
        e.preventDefault();
        $('#rating_form').submit();
    })
});