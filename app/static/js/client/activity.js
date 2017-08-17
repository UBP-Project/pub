/*
    ACTIVITY - Going & Interested
*/

$('.actvivity-card').bind('click', function(event) {
    var activity_id = event.currentTarget.id;  // activity id  
    viewGoing(activity_id);
    viewInterested(activity_id);
});

function viewGoing(activity_id) {

    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/going',
        type: 'GET'
    })
    .done(function(data) {

        if(data){

            console.log(data);
            
        } else {
            console.log('No one is going in this Activity');
        }

    })
    .fail(function() {
        console.log("error");
    });

}

function viewInterested(activity_id) {

    $.ajax({
        url: '/api/v1.0/activities/'+ activity_id + '/interested',
        type: 'GET'
    })
    .done(function(data) {
        
        if(data){
            console.log(data);
            /*var activity_list = "";
            for(activity in data){
                var title = data[activity].title;
                activity_list += title + '<br/>';
            }

            if(activity_list==""){
                document.getElementById('group-activities-'+group_id).innerHTML = "Group has No Activity"; 
            } else {
                document.getElementById('group-activities-'+group_id).innerHTML = activity_list;
                console.log(activity_list);
            }*/
            
        } else {
            /*document.getElementById('group-activities-'+group_id).innerHTML = "Group has No Activity";*/
            console.log('No one is Iinterested in this Activity');
        }

    })
    .fail(function() {
        console.log("error");
    });

}