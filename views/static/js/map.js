document.addEventListener("DOMContentLoaded", function () {
    var spaceno = "{{ rent.spaceno }}";  // 서버에서 렌더링된 spaceno 변수 사용

    // AJAX를 사용하여 FastAPI 지오코딩 엔드포인트 호출
    fetch(`/geocode/${spaceno}`)
        .then(response => response.json())
        .then(data => {
            if (data.addresses && data.addresses.length > 0) {
                var result = data.addresses[0]; // 첫 번째 결과 사용
                var coords = new naver.maps.LatLng(result.y, result.x);

                // 지도 표시할 div 요소
                var mapContainer = document.getElementById('map');

                // 지도를 생성할 초기 위치와 확대 레벨 설정
                var mapOption = {
                    center: coords,
                    zoom: 15 // 확대 레벨
                };

                // 지도 생성
                var map = new naver.maps.Map(mapContainer, mapOption);

                // 결과값으로 받은 위치를 지도에 마커로 표시
                var marker = new naver.maps.Marker({
                    map: map,
                    position: coords
                });

                // 인포윈도우로 장소에 대한 정보 표시
                var infowindow = new naver.maps.InfoWindow({
                    content: '<div style="width:150px;text-align:center;padding:6px 0;">' + result.roadAddress + '</div>'
                });
                infowindow.open(map, marker);
            } else {
                alert('도로명 주소를 찾을 수 없습니다. 올바른 주소인지 확인해주세요.');
            }
        })
        .catch(error => {
            console.error('지오코딩 실패:', error);
            alert('지오코딩 중 오류가 발생했습니다.');
        });
});
