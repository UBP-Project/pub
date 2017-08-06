function join_group(group_id){
	        $.ajax({
	            url: '/api/v1.0/interest_groups/'+ group_id + '/join',
	            type: 'POST'
	        })
	        .done(function(data) {
	            /*console.log(data);*/
	            console.log("success");
	            $(".modal-item .modal-footer button").text("LEAVE GROUP");
	        })
	        .fail(function() {
	            console.log("error");
	        });
        }

        function leave_group(group_id){
	        $.ajax({
	            url: '/api/v1.0/interest_groups/'+ group_id + '/leave',
	            type: 'DELETE'
	        })
	        .done(function(data) {
	            /*console.log(data);*/
	            console.log("success");
	        })
	        .fail(function() {
	            console.log("error");
	        });
        }