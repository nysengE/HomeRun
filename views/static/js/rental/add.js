// 주소 검색 함수
function searchAddress() {
    var address = document.getElementById('address').value.trim();
    if (address) {
        var geocoder = new kakao.maps.services.Geocoder();
        geocoder.addressSearch(address, function(result, status) {
            if (status === kakao.maps.services.Status.OK) {
                var latitude = result[0].y;
                var longitude = result[0].x;
                document.getElementById('latitude').value = latitude;
                document.getElementById('longitude').value = longitude;
            } else {
                alert('올바른 도로명 주소를 입력하세요.');
            }
        });
    } else {
        alert('주소를 입력해주세요.');
    }
}

// 가격 필드 포맷팅 및 유효성 검사
document.getElementById('price').addEventListener('input', function(e) {
    let value = e.target.value.replace(/[^0-9]/g, '');
    let numberValue = parseInt(value, 10);

    if (!isNaN(numberValue)) {
        if (numberValue > 10000000) {
            numberValue = 10000000;
        }
        e.target.value = new Intl.NumberFormat().format(numberValue);
    } else {
        e.target.value = '';
    }
});

document.getElementById('price').addEventListener('blur', function(e) {
    let value = e.target.value.replace(/[^0-9]/g, '');
    let numberValue = parseInt(value, 10);

    if (!isNaN(numberValue) && numberValue < 10000) {
        e.target.value = '10,000'; // 최소값 1만으로 설정
    }
});

// 폼 제출 시 유효성 검사
document.querySelector('form[name="addfrm"]').addEventListener('submit', function(e) {
    const availableDates = document.getElementById('available_dates').value;
    const file1 = document.getElementById('file1');
    const priceInput = document.getElementById('price');
    const latitude = document.getElementById('latitude').value;
    const longitude = document.getElementById('longitude').value;

    // 가격 필드에서 쉼표 제거
    priceInput.value = priceInput.value.replace(/,/g, '');

    // 첨부파일 필수 확인
    if (!file1.value) {
        e.preventDefault(); // 폼 제출 방지
        alert('첨부파일을 최소 1개 이상 선택하세요.');
        file1.focus();
        return;
    }

    // 지오코딩 확인
    if (!latitude || !longitude) {
        e.preventDefault();
        alert('주소확인을 눌러 정확한 주소인지 확인하세요.');
    }

    // 사용 가능 날짜 확인
    if (!availableDates) {
        e.preventDefault();
        alert('사용 가능 날짜를 선택하세요.');
        return;
    }
});
