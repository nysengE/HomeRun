document.addEventListener('DOMContentLoaded', function() {
    var paymentButton = document.getElementById('confirmPaymentButton');
    paymentButton.addEventListener('click', function(event) {
        event.preventDefault();

        // 사용자 입력 유효성 검사
        var form = document.getElementById('customerInfoForm');
        if (!form.checkValidity()) {
            alert('예약자 정보를 정확히 입력해주세요.');
            return;
        }

        // 아임포트 결제 시작
        var IMP = window.IMP;
        IMP.init('imp77608186'); // 본인의 가맹점 식별코드로 변경해야 합니다.

        // 결제 금액 가져오기
        var amount = parseInt(document.getElementById('totalPrice').innerText.replace(',', '').replace('원', ''), 10);

        // 결제 요청
        IMP.request_pay({
            pg: 'html5_inicis', // 결제 창에 표시할 PG사
            pay_method: 'card', // 결제 방법
            merchant_uid: 'merchant_' + new Date().getTime(), // 주문 번호
            name: '{{ rent.title }}', // 주문명
            amount: amount, // 결제 금액
            buyer_email: document.getElementById('email').value,
            buyer_name: document.getElementById('name').value,
            buyer_tel: document.getElementById('contact').value
        }, function(rsp) {
            if (rsp.success) {
                // 결제 성공 시 서버로 imp_uid 전송
                fetch('/pay/complete', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': '{{ csrf_token }}' // 만약 CSRF 토큰이 필요하다면 추가
                    },
                    body: JSON.stringify({ imp_uid: rsp.imp_uid })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.message === "결제가 완료되었습니다.") {
                            alert('결제가 완료되었습니다.');
                            window.location.href = '/confirmation'; // 결제 확인 페이지로 이동
                        } else {
                            alert('결제 검증에 실패했습니다.');
                        }
                    })
                    .catch(error => {
                        console.error('결제 처리 중 오류 발생:', error);
                        alert('결제 처리 중 오류가 발생했습니다. 다시 시도해주세요.');
                    });
            } else {
                // 결제 실패 시 로직
                alert('결제에 실패하였습니다. 다시 시도해주세요.');
            }
        });
    });
});
