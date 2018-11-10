function test() {
	/* open the file explorer window */
	$("#fileupload").click();	
}

$(document).ready(function () {

	  /* initialize the file upload component */
	  $("#fileupload").fileupload({
	    dataType: 'json',
	    done: function (e, data) {
	  /* process the response from the server */
	      if (data.result.is_valid) {
	        $("#gallery tbody").prepend(
	          "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
	        )
	      }
	    }
	  });

});