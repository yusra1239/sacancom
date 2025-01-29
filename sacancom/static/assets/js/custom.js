$(document).ready(function(){
	"use strict";
    
        /*==================================
* Author        : "ThemeSine"
* Template Name : Listrace directory HTML Template
* Version       : 1.0
==================================== */




/*=========== TABLE OF CONTENTS ===========
1. Scroll To Top 
2. slick carousel
3. welcome animation support
4. feather icon
5. counter
======================================*/

    // 1. Scroll To Top 
		$(window).on('scroll',function () {
			if ($(this).scrollTop() > 600) {
				$('.return-to-top').fadeIn();
			} else {
				$('.return-to-top').fadeOut();
			}
		});
		$('.return-to-top').on('click',function(){
				$('html, body').animate({
				scrollTop: 0
			}, 1500);
			return false;
		});
	
	// Initialize Feather Icons
	feather.replace();

	function addToFavorites(event, adId) {
		event.preventDefault(); // Prevent the default anchor behavior

		// Change the heart icon color to red
		const heartIcon = document.querySelector('.heart-icon');
		heartIcon.style.color = 'red';

		// Send a request to save the ad to favorites
		fetch('/add_to_favorites/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken') // Get CSRF token for Django
			},
			body: JSON.stringify({ ad_id: adId }) // Send the ad ID
		})
		.then(response => {
			if (response.ok) {
				console.log('Ad added to favorites!');
			} else {
				console.error('Failed to add ad to favorites.');
			}
		})
		.catch(error => console.error('Error:', error));
	}

	// Function to get CSRF token
	function getCookie(name) {
		let cookieValue = null;
		if (document.cookie && document.cookie !== '') {
			const cookies = document.cookie.split(';');
			for (let i = 0; i < cookies.length; i++) {
				const cookie = cookies[i].trim();
				// Check if this cookie string begins with the name we want
				if (cookie.substring(0, name.length + 1) === (name + '=')) {
					cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
					break;
				}
			}
		}
		return cookieValue;
	}
	// 2. slick carousel

	    $(".testimonial-carousel").slick({
	        infinite: true,
	        centerMode: true,
	        autoplay:true,
	        slidesToShow: 5,
	        slidesToScroll: 3,
	        autoplaySpeed:1500,
	        // the magic
			responsive: [
				{

					breakpoint:1440,
					settings: {
					slidesToShow:3
					}

				},
				{

					breakpoint: 1024,
					settings: {
					slidesToShow:2,
					
					}

				}, 
				{

					breakpoint:991,
					settings: {
					slidesToShow:2,
					centerMode:false,
					}

				},
				{

					breakpoint:767,
					settings: {
					slidesToShow:1,
					}

				}
			]
	    });



    // 3. welcome animation support

        $(window).load(function(){
        	$(".welcome-hero-txt h2,.welcome-hero-txt p").removeClass("animated fadeInUp").css({'opacity':'0'});
            $(".welcome-hero-serch-box").removeClass("animated fadeInDown").css({'opacity':'0'});
        });

        $(window).load(function(){
        	$(".welcome-hero-txt h2,.welcome-hero-txt p").addClass("animated fadeInUp").css({'opacity':'0'});
            $(".welcome-hero-serch-box").addClass("animated fadeInDown").css({'opacity':'0'});
        });

	// 4. feather icon

		feather.replace();

	// 5. counter
		$(window).on('load', function(){	
			$('.counter').counterUp({
				delay: 10,
				time: 3000
			});	
		});

});