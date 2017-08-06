$(document).ready(function() {
    $("#reveal").click(function() {
        if($(".password").attr("type") == "password") {
            $(".password").attr("type", "text");
            $("#reveal-icon").attr("class", "fa fa-eye");
        } else {
            $(".password").attr("type", "password");
            $("#reveal-icon").attr("class", "fa fa-eye-slash");
        }
    });
});