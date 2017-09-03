/*
    ACTIVITY - Going & Interested
*/

$('.modal-footer .activity-btn').bind('click', function(event) {

    var activity_id = event.currentTarget.id;  // activity id  
    var btn = event.currentTarget;
    var val = event.currentTarget.value;
    console.log("ACT_ID fr bind= " + activity_id + ", value = " + val);
    //console.log(btn);

    if(val=="going"){
        going(activity_id);
        $(btn).removeClass('ngoing-btn');
        $(btn).addClass('going-btn');
        event.currentTarget.value = 'cgoing';
    } else if(val=="interested") {
        interested(activity_id);
        $(btn).removeClass('ninterested-btn');
        $(btn).addClass('interested-btn');
        event.currentTarget.value = 'cinterested';
    } else if(val=="cgoing") {
        cancel_going(activity_id);
        $(btn).removeClass('going-btn');
        $(btn).addClass('ngoing-btn');
        event.currentTarget.value = 'going';
    } else if(val=="cinterested") {
        cancel_interested(activity_id);
        $(btn).removeClass('interested-btn');
        $(btn).addClass('ninterested-btn');
        event.currentTarget.value = 'interested';
    }

    //init_status(activity_id);

});

function view_activity(activity_id) {
    //console.log("ACT_ID = " + activity_id);
    init_status(activity_id);
    interested_users(activity_id);
    going_users(activity_id);
}

function init_status(activity_id) {

    $('.modal-footer .interested-btn').hide();
    $('.modal-footer .ninterested-btn').hide();
    $('.modal-footer .going-btn').hide();
    $('.modal-footer .ngoing-btn').hide();

    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/participation',
        type: 'GET'
    })
    .done(function(data) {

        var interested = data.interested;
        var going = data.going;

        if(interested) {
            $('.modal-footer .interested-btn').show();
            $('.modal-footer .ninterested-btn').hide();
        } else {
            $('modal-footer .interested-btn').hide();
            $('.modal-footer .ninterested-btn').show();
        }

        if(going) {
            $('.modal-footer .going-btn').show();
            $('.modal-footer .ngoing-btn').hide();
        } else {
            $('.modal-footer .going-btn').hide();
            $('.modal-footer .ngoing-btn').show();
        }


    })
    .fail(function() {
        console.log("error");
    });
}

function going(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/participants/going',
        type: 'POST'
    })
    .done(function(data) {
        going_users(activity_id);
        //console.log('success going');
    })
    .fail(function() {
        console.log("error");
    });
}

function interested(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/participants/interested',
        type: 'POST'
    })
    .done(function(data) {
        interested_users(activity_id);
        //console.log('success interested');
    })
    .fail(function() {
        console.log("error");
    });
}

function cancel_going(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/participants/going',
        type: 'DELETE'
    })
    .done(function(data) {
        going_users(activity_id);
        //console.log('cancel going');
    })
    .fail(function() {
        console.log("error");
    });
}

function cancel_interested(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/participants/interested',
        type: 'DELETE'
    })
    .done(function(data) {
        interested_users(activity_id);
        //console.log('cancel interested');
    })
    .fail(function() {
        console.log("error");
    });
}

function interested_users(activity_id) {
    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/participants/interested',
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
        url: '/api/v1.0/activities/'+ activity_id + '/participants/going',
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