(function ($) {
    "use strict";
    // Auto-scroll
    $('#myCarousel').carousel({
        interval: false,
    });
  
    // Control buttons
    $('.next').click(function () {
      $('.carousel').carousel('next');
      return false;
    });
    $('.prev').click(function () {
      $('.carousel').carousel('prev');
      return false;
    });
  
    // On carousel scroll
    $("#myCarousel").on("slide.bs.carousel", function (e) {

      var $e = $(e.relatedTarget);
      var idx = $e.index();
      var itemsPerSlide = 3;
      var totalItems = $(".carousel-item").length;
      if (idx >= totalItems - (itemsPerSlide - 1)) {
        var it = itemsPerSlide -
            (totalItems - idx);
        for (var i = 0; i < it; i++) {
          // append slides to end 
          if (e.direction == "left") {
            $(
              ".carousel-item").eq(i).appendTo(".carousel-inner");
          } else {
            $(".carousel-item").eq(0).appendTo(".carousel-inner");
          }
        }
      }
    });
  })
(jQuery);

var slideIndex = 1;
showSlides(slideIndex);

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}

window.alert = function() {};