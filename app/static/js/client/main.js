/*
    MAIN - Navigation
*/

$(function () {

	var nav = $('.nav-container');
	var content = $('.content-wrap');
	var side = $('.side');

	$(window).scroll(function () {
		if ($(this).scrollTop() > 45) {
			nav.addClass("fixed-nav");
			content.css('margin-top','75px');
			side.css('margin-top','75px');
		} else {
			nav.removeClass("fixed-nav");
			content.css('margin-top','0px');
			side.css('margin-top','0px');
		}
	});

	$(document).click(function (event) {
		$('.navbar-collapse').collapse('hide');
	});

});