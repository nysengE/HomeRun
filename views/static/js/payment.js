document.addEventListener('DOMContentLoaded', function() {
    var payButton = document.getElementById('payButton');
    if (payButton) {
        payButton.addEventListener('click', function() {
            var IMP = window.IMP; // 생략 가능
            IMP.init('imp77608186'); // 'iamport' 대신 발급받은 "가맹점 식별코드"를 사용

            // 결제 요청 데이터
            var paymentData = {
                pg: 'html5_inicis', // 예: 'html5_inicis'는 KG이니시스, 'kakaopay'는 카카오페이
                pay_method: 'card', // 결제 방식 (카드, 계좌이체, 가상계좌 등)
                merchant_uid: 'merchant_' + new Date().getTime(), // 주문번호
                name: payButton.dataset.itemName || '상품명', // 결제 이름
                amount: parseInt(payButton.dataset.amount) || 0, // 결제 금액
                buyer_email: 'user@example.com', // 구매자 이메일
                buyer_name: '홍길동', // 구매자 이름
                buyer_tel: '010-1234-5678', // 구매자 전화번호
                buyer_addr: '서울특별시 강남구 삼성동', // 구매자 주소
                buyer_postcode: '123-456', // 구매자 우편번호
                m_redirect_url: 'http://localhost:8000/pay/complete' // 결제 완료 후 리다이렉트 될 주소
            };

            IMP.request_pay(paymentData, function (rsp) {
                if (rsp.success) {
                    // 결제 성공 시 처리 로직
                    fetch('/pay/complete', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            imp_uid: rsp.imp_uid,
                            merchant_uid: rsp.merchant_uid
                        })
                    })
                        .then(response => response.json())
                        .then(data => {
                            alert('결제가 완료되었습니다.');
                        });
                } else {
                    // 결제 실패 시 처리 로직
                    alert('결제에 실패하였습니다. 에러 내용: ' + rsp.error_msg);
                }
            });
        });
    }
});
