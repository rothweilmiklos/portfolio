$(document).ready(function(){
    $('form').on('submit', function(event) {
        // disable to avoid double submission
        $(':button').prop('disabled', true);
    });
});