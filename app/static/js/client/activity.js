/*
    ACTIVITY - Going & Interested
*/

function view_activity(activity_id) {
    console.log("ACT_ID = " + activity_id);
    interested_users(activity_id);
    going_users(activity_id);
}

function interested_users(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/interested',
        type: 'GET'
    })
    .done(function(data) {
        //console.log("success");
        if(data.length){
            var users_list = "";
            for (var i in data) {
                var name = data[i].firstname + " " + data[i].lastname;
                var user_id = data[i].id;
                users_list += "<a href='/profile/" + user_id + "'>" + name + "</a><br/>";
                /*console.log("NAME: " + name);
                console.log("USER_ID: " + user_id);*/
            }
            document.getElementById('interested-users-'+activity_id).innerHTML = users_list;
        } else {
            document.getElementById('interested-users-'+activity_id).innerHTML = 'No one is interested to this activity';   
        }
    })
    .fail(function() {
        console.log("error");
    });
}

function going_users(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/going',
        type: 'GET'
    })
    .done(function(data) {
         //console.log("success");
        if(data.length){
            var users_list = "";
            for (var i in data) {
                var name = data[i].firstname + " " + data[i].lastname;
                var user_id = data[i].id;
                users_list += "<a href='/profile/" + user_id + "'>" + name + "</a><br/>";
                /*console.log("NAME: " + name);
                console.log("USER_ID: " + user_id);*/
            }
            document.getElementById('going-users-'+activity_id).innerHTML = users_list;
        } else {
            document.getElementById('going-users-'+activity_id).innerHTML = 'No one is going to this activity';   
        }
    })
    .fail(function() {
        console.log("error");
    });
}




$('.activity-btn').bind('click', function(event) {

    var activity_id = event.currentTarget.id;  // activity id  
    var btn = event.currentTarget;
    console.log("ACT_ID = " + activity_id);
    console.log(btn);

});

function going(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/going',
        type: 'POST'
    })
    .done(function(data) {
        console.log('success going');
        console.log(data);
    })
    .fail(function() {
        console.log("error");
    });
}

function interested(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/interested',
        type: 'POST'
    })
    .done(function(data) {
        console.log('success interested');
        console.log(data);
    })
    .fail(function() {
        console.log("error");
    });
}