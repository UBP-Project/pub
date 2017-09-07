function set_buttons() {
    $("#btn-follow").on('click', function() {
        $.ajax({
            'url': '{{ url_for('api.follow_user', to_follow_id=user["id"]) }}',
            'type': 'POST'
        }).done(function(data) {
            $("#btn-follow").remove();
            $("#profile-btns").append('<button id="btn-unfollow" class="btn btn-style-1" style="width: 100px">Following</button>');
            set_buttons();
        });
    });

    $("#btn-unfollow").on('click', function() {
        $.ajax({
            'url': '{{ url_for('api.unfollow_user', to_unfollow_id=user["id"]) }}',
            'type': 'DELETE'
        }).done(function(data) {
            $("#btn-unfollow").remove();
            $("#profile-btns").append('<button id="btn-follow" class="btn btn-style-2" style="width: 100px">Follow</button>');
            set_buttons();
        });
    });

    $("#btn-unfollow")
        .mouseover(function() {
            $(this).text("Unfollow");
        })
        .mouseout(function() {
            $(this).text("Following");
        });

}
// initialize buttons
set_buttons();