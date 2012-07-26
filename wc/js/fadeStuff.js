$(document).ready(function(){
$.fn.exists = function(){return this.length>0;}
if ($('#iso').exists()){
$('#iso').imagesLoaded(function(){
$('.isoImg').fadeIn(600);
$('#iso').isotope({
itemSelector : '.item'
});
});
}
$('html').fadeIn(200);
$('#fadeContent').fadeIn(800);
$('a').not('.lightview').click(function(){
	$('html').fadeOut(200);
	$('#fadeContent').fadeOut(800);
});
});
