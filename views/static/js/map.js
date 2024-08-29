async function geocodeAddress(address) {
    return new Promise((resolve, reject) => {
        if (!kakao || !kakao.maps) {
            reject('Kakao Maps API가 로드되지 않았습니다.');
            return;
        }

        const geocoder = new kakao.maps.services.Geocoder();

        geocoder.addressSearch(address, (result, status) => {
            if (status === kakao.maps.services.Status.OK) {
                resolve({
                    latitude: parseFloat(result[0].y),
                    longitude: parseFloat(result[0].x),
                });
            } else {
                reject(`지오코딩에 실패했습니다: ${status}`);
            }
        });
    });
}

// 페이지 로드 후 지도 초기화
document.addEventListener('DOMContentLoaded', async function () {
    try {
        const address = "{{ rent.district_name }} {{ rent.zipcode }}"; // 서버로부터 받은 주소 정보
        const geocodeResult = await geocodeAddress(address); // 지오코딩 결과 가져오기

        if (geocodeResult) {
            initializeMap(geocodeResult.latitude, geocodeResult.longitude); // 지도를 초기화
        } else {
            // 지오코딩 실패 시 기본 좌표로 지도 표시
            console.warn("기본 좌표로 지도를 초기화합니다.");
            initializeMap(37.5665, 126.9780); // 서울시청 좌표
        }
    } catch (error) {
        console.error('지도를 초기화하는 동안 오류가 발생했습니다:', error);
    }
});
