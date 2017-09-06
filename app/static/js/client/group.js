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
            //console.log("Join Request Sent");
            console.log("success");
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
            viewMembers(group_id);
            //console.log("You left the group");
            console.log('success');
        })
        .fail(function() {
             console.log("error");
        });

    } // if(action == 'join')


}); // $('.grp-btn').bind('click', function(event)

/*
    GROUP DETAILS - Members & Activities
*/

$('.grp-icon').bind('click', function(event) {
    var group_id = event.currentTarget.id;  // group id
    viewLeaders(group_id);
    viewMembers(group_id);
    viewActivities(group_id);
});

function viewLeaders(group_id) {

    $.ajax({
        url: '/api/v1.0/interest_groups/'+ group_id + '/leaders',
        type: 'GET'
    })
    .done(function(data) {

        if(data.length){
            var users_list = "<b>Leader(s)</b><br/>";
            for (var i in data) {
                var name = data[i].firstname + " " + data[i].lastname;
                var user_id = data[i].id;
                users_list += "<div class='col-md-6 mini-container'><a href='/profile/" + user.id + "'><span>"+ name + "</span></a></div>";
            }

            document.getElementById('group-leaders-'+group_id).innerHTML = users_list;
        } else {
            document.getElementById('group-leaders-'+group_id).innerHTML = '<i>Group has no leaders</i>';   
        }

    })
    .fail(function() {
        console.log("error");
    });

}

function viewMembers(group_id) {

    $.ajax({
        url: '/api/v1.0/interest_groups/'+ group_id + '/members',
        type: 'GET'
    })
    .done(function(data) {

        if(data.length){
            var users_list = "<b>Member(s)</b><br/>";
            for (var i in data) {
                var name = data[i].firstname + " " + data[i].lastname;
                var user_id = data[i].id;
                users_list += "<div class='col-md-6 mini-container'><a href='/profile/" + user.id + "'><span>"+ name + "</span></a></div>";
            }
            document.getElementById('group-members-'+group_id).innerHTML = users_list;
        } else {
            document.getElementById('group-members-'+group_id).innerHTML = '<i>Group has no members</i>';   
        }

    })
    .fail(function() {
        console.log("error");
    });

}

function viewActivities(group_id) {

    $.ajax({
        url: '/api/v1.0/interest_groups/'+ group_id + '/activities',
        type: 'GET'
    })
    .done(function(data) {
        
        if(data){
            var activity_list = "";
            for(activity in data){
                var title = data[activity].title;
                /*var activity_id = data[activity].id;*/
                activity_list += title + '<br/>';
            }

            if(activity_list==""){
                document.getElementById('group-activities-'+group_id).innerHTML = "<i>Group has No Activity</i>"; 
            } else {
                document.getElementById('group-activities-'+group_id).innerHTML = activity_list;
                //console.log(activity_list);
            }
            
        } else {
            document.getElementById('group-activities-'+group_id).innerHTML = "<i>Group has No Activity</i>";
            console.log('Group has No Activity');
        }

    })
    .fail(function() {
        console.log("error");
    });

}