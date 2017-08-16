/*
    JOIN GROUP - CANCEL JOIN REQUEST - LEAVE GROUP
*/

$('.grp-btn').bind('click', function(event) {

    var btn = event.currentTarget;
    var group_id = event.currentTarget.id;  // group id  
    var action = event.currentTarget.value; // [ join, cancel, leave ]

    if(action == 'join') {

        $.ajax({
            url: '/api/v1.0/interest_groups/'+ group_id + '/join',
            type: 'POST'
        })
        .done(function(data) {
            $(btn).removeClass('btn-style-1');
            $(btn).addClass('btn-warning');
            $(btn).text('CANCEL JOIN REQUEST');
            event.currentTarget.value = 'cancel';
            console.log("Join Request Sent");
        })
        .fail(function() {
             console.log("error");
        });

    } else {

        $.ajax({
            url: '/api/v1.0/interest_groups/'+ group_id + '/leave',
            type: 'DELETE'
        })
        .done(function(data) {
            $(btn).removeClass('btn-warning');
            $(btn).removeClass('btn-danger');
            $(btn).addClass('btn-style-1');
            $(btn).text('JOIN GROUP');
            event.currentTarget.value = 'join';
            console.log("You left the group");
        })
        .fail(function() {
             console.log("error");
        });

    } // if(action == 'join')


}); // $('.grp-btn').bind('click', function(event)

/*
    GROUP DETAILS - Members & Activities
*/

/*$('grp-modal').bind('load', function(event) {
    var group_id = event.currentTarget.id;  // group id  
    console.log('Add additional info for group here (members,activities) - ' + group_id);
});*/