$(document).ready(function(){
$.fn.exists = function(){return this.length>0;}
if ($('#iso').exists()){
$('#iso').imagesLoaded(function(){
$('.isoImg').fadeIn(400);
$('#iso').isotope({
itemSelector : '.item'
});
});
}
$('html').fadeIn(200);
$('a').click(function(){
	$('html').fadeOut(200);
});
$('#fadeContent').fadeIn(800);
$('a').click(function(){
	$('#fadeContent').fadeOut(800);
});
});