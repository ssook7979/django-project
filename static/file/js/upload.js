$(document).ready(function () {
	  /* open the file explorer window */
	  $(".js-upload-photos").click(function () {
	    $("#fileupload").click();
	  });

	  /* initialize the file upload component */
	  $("#fileupload").fileupload({
	    dataType: 'json',
	    sequentialUploads: true, // send file one by one
	    start: function (e) {
	        $("#modal-progress").modal("show");
	      },

	      stop: function (e) {
	        $("#modal-progress").modal("hide");
	      },

	      progressall: function (e, data) {
	        var progress = parseInt(data.loaded / data.total * 100, 10);
	        var strProgress = progress + "%";
	        $(".progress-bar").css({"width": strProgress});
	        $(".progress-bar").text(strProgress);
	      },
	    done: function (e, data) {
	  /* process the response from the server */
	      if (data.result.is_valid) {
	        $("#gallery").load(" #gallery")
	      }
	    }
	  });

});

function file_delete(url) {
	$.ajax({
		type: 'POST',
		url: url,
		success: function (response) {
			$("#gallery").load(" #gallery")
	     }
	});
}