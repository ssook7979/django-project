

//signup ajax
function signupAjax(){
	var queryset = $('#signupForm').serialize();
	$.ajax({
		type:"POST",
		url: "/members/signup/",
		data: queryset,
		datatype: 'json',
		headers : {'X-CSRFToken': getCookie('csrftoken')},
		success: function (response) {
			if (!response.error) {
				$('.modal-content').empty().load('/members/send_email/ .container');;
			}
			else {
				$(".errorMessage").empty();
				for (var x in response.error) {
					for (var i in response.error[x]) {
						$("#id_" + x).next().empty().html(response.error[x][i]);
					}
				}		
			}
		},
		error : function(request,status,error) {
			alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
		}
	});
}

function send_again(){
	$.ajax({
		type:"POST",
		url:"/members/send_email_again/",
		datatype: 'json',
		headers : {'X-CSRFToken': getCookie('csrftoken')},
		beforeSend: function () {
		},
		success: function(response){
			
			$('#send_alarm').fadeTo("slow",0.1).fadeTo("fast",1);

		},
		error: function(request,status,error) {
			alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
		}
	});
}

/*
function test(){
	$("div.container").remove();
	jQuery.removeData( div, "test1" );
	$("form.modal-content").load('/members/signup/ .container');
}
if ($("#id_panel").length == 0){
	$('.container').prepend(
			"<div id='id_panel' class='w3-panel w3-pale-red'>" + 
			"<p>입력하신 메일주소 " + email + "로 메일이 다시 전송되었습니다.</p>" +
			"</div>"
	);				
}
*/
/*
function signupPopup() {
    $modal = $('#signup-modal');
    $modal.find('form')[0].reset();
	document.getElementById('signup-modal').style.display='block';

}
 */