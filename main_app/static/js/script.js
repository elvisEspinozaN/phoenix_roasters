// variables
const searchBtn = $("#search-button");
const overlay = $("#overlay");
//
// $(document).ready(function () {
//   $("#search-close").click(function () {
//     $("#search-overlay").fadeOut();
//     $("#search-button").show();
//   });
//   $("#search-button").click(function () {
//     $(this).hide();
//     $("#search-overlay").fadeIn();
//   });
// });
searchBtn.on("click", function () {
  $(".search").removeClass("search_low");
  overlay.addClass("overlay_show");
});

$(".navbar-toggler").on("click", function () {
  overlay.addClass("overlay_show");
  $("html").addClass("open-nav");
});

overlay.on("click", function () {
  $("search").addClass("search_low");
  overlay.removeClass("overlay_show");
});

$(".home_fav__products__slick").slick({
  infinite: true,
  slidesToShow: 4,
  slidesToScroll: 1,
  arrows: false,
  dots: false,
  autoplay: true,
  autoplaySpeed: 550,
  responsive: [
    {
      breakpoint: 600,
      settings: {
        slidesToShow: 2,
        slidesToScroll: 1,
      },
    },
    {
      breakpoint: 750,
      settings: {
        slidesToShow: 3,
        slidesToScroll: 1,
      },
    },
    {
      breakpoint: 985,
      settings: {
        slidesToShow: 4,
        slidesToScroll: 1,
      },
    },
  ],
});
