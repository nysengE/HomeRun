document.addEventListener('DOMContentLoaded', function() {
    const priceRange = document.getElementById('priceRange');
    const priceOutput = priceRange.nextElementSibling;
    const peopleRange = document.getElementById('peopleRange');
    const peopleOutput = peopleRange.nextElementSibling;
    const regionSelect = document.getElementById('region');

    // 가격 및 인원 스크롤바 값 표시 기능 추가
    priceRange.addEventListener('input', function() {
        priceOutput.value = this.value + ' 원';
    });

    peopleRange.addEventListener('input', function() {
        peopleOutput.value = this.value + ' 명';
    });

    // 지역 필터링 기능
    regionSelect.addEventListener('change', function() {
        const selectedRegion = this.value;
        const items = document.querySelectorAll('.item');

        items.forEach(item => {
            if (selectedRegion === "모든 지역" || item.dataset.region === selectedRegion) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });

    // 슬라이더 기능 추가
    const sliders = document.querySelectorAll('.slider');
    sliders.forEach(slider => {
        const slides = slider.querySelectorAll('.slide');
        let currentSlide = 0;

        if (slides.length > 1) {
            slides[currentSlide].classList.add('active');

            setInterval(() => {
                slides[currentSlide].classList.remove('active');
                currentSlide = (currentSlide + 1) % slides.length;
                slides[currentSlide].classList.add('active');
            }, 3000);
        }
    });
});
