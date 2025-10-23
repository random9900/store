let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;

function changeSlide(direction) {
    currentSlide = (currentSlide + direction + totalSlides) % totalSlides;
    document.querySelector('.slides').style.transform = `translateX(-${currentSlide * 100}%)`;
}

// Auto-slide every 5 seconds
setInterval(() => changeSlide(1), 5000);