function initMap(latitude, longitude) {
    var container = document.getElementById('map'); // 지도를 표시할 div
    var options = {
        center: new kakao.maps.LatLng(latitude, longitude), // 한성대학교 좌표
        level: 2 // 지도의 확대 레벨
    };

    var map = new kakao.maps.Map(container, options); // 지도 생성

    // 마커가 표시될 위치
    var markerPosition = new kakao.maps.LatLng(latitude, longitude);

    // 마커 생성
    var marker = new kakao.maps.Marker({
        position: markerPosition
    });

    // 마커가 지도 위에 표시되도록 설정
    marker.setMap(map);

}

// Kakao Maps API의 load 메서드를 이용하여 지도 초기화
kakao.maps.load(function() {
    var latitude = parseFloat(document.getElementById('map').dataset.latitude);
    var longitude = parseFloat(document.getElementById('map').dataset.longitude);
    initMap(latitude, longitude);
});