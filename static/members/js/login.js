function loginAjax(){
	var queryset = $('#loginForm').serialize();
	console.log(window.location.href);
	//var next = window.location.href.split('next=')[1];
	$.ajax({
		type: "POST",
		url: '/members/login/',
		data: queryset,
		datatype: 'json',
		headers : {'X-CSRFToken': getCookie('csrftoken')},
		beforeSend: function () {
		},
		success: function (response) {
			if (response.result) {
				var next = window.location.href.split('next=')
				if (next.length == 1) {
					window.location.reload(true);					
				}
				else {
					location.href = next[1]					
				}
			}
			else {
				if ($('#id_panel-login').css('display') == "none") {
					$('#id_panel-login').show();					
				}
			}
		},
		error: function(request,status,error) {
			alert("code:" + request.status + "\n" + "message:" + request.responseText + "\n" + "error:" + error);
		}
	});
}

