  document.addEventListener("scroll", function() {
    // if(window.matchMedia("(min-width: 64em)").matches) {
      if (window.pageYOffset > 2000) {
        document.getElementById("nav-display").style.display = "block";

      }
      else {
        document.getElementById("nav-display").style.display = "none";
      }
    //}
});
//}
particlesJS.load('particles-js', 'public/assets/particles.json', function() {
  console.log('callback - particles.js config loaded');
});