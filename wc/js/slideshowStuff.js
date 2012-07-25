$(document).ready(function(){
	var maximgheight = 0;
	$('img').each(function(){
var thisImg = $(this);
if (thisImg.attr('src') == $('body').attr('background')) thisImg.parent().remove();
$(window).load(function(){
	if (thisImg.height() > maximgheight) maximgheight = thisImg.height();
	$('.slideshow').css('min-height', maximgheight);
	});
});
if (!$('#imageCell').length) $('#imagesRow').remove();
$('.slideshow').cycle({fx: 'fade'});
});