var resize = false;
$('#id_content').hover(function(e){
	e.preventDefault();
	resize = false;
});
$('#grippie').mousemove(function(e){
	if(resize == true){
      $('#id_content').height(e.pageY-18);
   }
});

$('#grippie').mousedown(function(e){
	resize = false;
   resize = true;
});
$(window).mouseup(function(e){
   resize = false;
});
