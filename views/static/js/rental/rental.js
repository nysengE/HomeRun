document.addEventListener('DOMContentLoaded', function() {
    // URL 설정
    document.getElementById('mjCollege').querySelector('a').href = urls.mjCollege;
    document.getElementById('foreignUniversity').querySelector('a').href = urls.foreignUniversity;
    document.getElementById('hansungUniversity').querySelector('a').href = urls.hansungUniversity;
    document.getElementById('urbanBasketball').querySelector('a').href = urls.urbanBasketball;

    // 이미지 설정
    document.querySelectorAll('#mjCollege .slide')[0].src = images.mjCollege[0];
    document.querySelectorAll('#mjCollege .slide')[1].src = images.mjCollege[1];

    document.querySelectorAll('#foreignUniversity .slide')[0].src = images.foreignUniversity[0];
    document.querySelectorAll('#foreignUniversity .slide')[1].src = images.foreignUniversity[1];

    document.querySelectorAll('#hansungUniversity .slide')[0].src = images.hansungUniversity[0];
    document.querySelectorAll('#hansungUniversity .slide')[1].src = images.hansungUniversity[1];

    document.querySelectorAll('#urbanBasketball .slide')[0].src = images.urbanBasketball[0];
    document.querySelectorAll('#urbanBasketball .slide')[1].src = images.urbanBasketball[1];

    // 슬라이더 자동 전환 기능
    const sliders = document.querySelectorAll('.slider');
    sliders.forEach(slider => {
        const slides = slider.querySelectorAll('.slide');
        let currentSlide = 0;

        slides[currentSlide].classList.add('active');

        setInterval(() => {
            slides[currentSlide].classList.remove('active');
            currentSlide = (currentSlide + 1) % slides.length;
            slides[currentSlide].classList.add('active');
        }, 3000);
    });

    // 가격 및 인원 스크롤바 값 표시 기능 추가
    const priceRange = document.getElementById('priceRange');
    const priceOutput = priceRange.nextElementSibling;
    const peopleRange = document.getElementById('peopleRange');
    const peopleOutput = peopleRange.nextElementSibling;

    priceRange.addEventListener('input', function() {
        priceOutput.value = this.value + ' 원';
    });

    peopleRange.addEventListener('input', function() {
        peopleOutput.value = this.value + ' 명';
    });

    // 서울시 구 리스트 추가
    const seoulDistricts = [
        "모든 지역", //추가해야  지역 눌렀을때 다 보임
        "종로구", "중구", "용산구", "성동구", "광진구", "동대문구", "중랑구",
        "성북구", "강북구", "도봉구", "노원구", "은평구", "서대문구", "마포구",
        "양천구", "강서구", "구로구", "금천구", "영등포구", "동작구", "관악구",
        "서초구", "강남구", "송파구", "강동구"
    ];

    const regionSelect = document.getElementById('region');
    seoulDistricts.forEach(district => {
        const option = document.createElement('option');
        option.value = district;
        option.textContent = district;
        regionSelect.appendChild(option);
    });

    // 아이템 필터링 기능
    // 아이템 필터링 기능
    regionSelect.addEventListener('change', function() {
        const selectedRegion = this.value;
        const items = document.querySelectorAll('.item');

        items.forEach(item => {
            if (selectedRegion === "모든 지역" || selectedRegion === "" || item.dataset.region === selectedRegion) { // 수정된 부분
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });



});
