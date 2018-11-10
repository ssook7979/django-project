function comment_Ajax(ajax_url, item){
	var queryset = $(item).closest('form').serialize();

	$.ajax({
		type:"POST",
		url: ajax_url,
		data: queryset,
		//async: false,
		headers : {'X-CSRFToken': getCookie('csrftoken')},
		success: function (response) {
		    $("#comment_list").load(" #comment_list");
		}
	});
}

function get_comment(load_url) {
	$("#comment_list").load(load_url + " #comment_list")
}

function load_comment_form(item, url) {
	$(item).load(url + " #comment_form");
}

function close_form(item){
	$(item).closest('form').empty();
}

function delete_check(url) {
    if (confirm("정말 삭제하시겠습니까?")) {
        location.href = url;
    } else {}
}
