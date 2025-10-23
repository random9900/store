function scrollSlider(sliderId, direction) {
    const slider = document.getElementById(sliderId);
    const cardWidth = slider.querySelector('.card').offsetWidth + 20;
    const scrollAmount = cardWidth * 2;
    slider.scrollLeft += direction * scrollAmount;
}

document.querySelectorAll('.card-slider').forEach(slider => {
    let startX, scrollLeft;
    slider.addEventListener('touchstart', e => {
        startX = e.touches[0].pageX;
        scrollLeft = slider.scrollLeft;
    });
    slider.addEventListener('touchmove', e => {
        const x = e.touches[0].pageX;
        const walk = (x - startX) * 2;
        slider.scrollLeft = scrollLeft - walk;
    });
});