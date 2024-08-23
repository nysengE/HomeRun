// JavaScript to handle click events and display the value
document.querySelectorAll('.list-group-item').forEach(item => {
    item.addEventListener('click', () => {
        const value = item.getAttribute('data-value');
        console.log(value);
    });
});

// header switch버튼
$(document).ready(function() {
    // 현재 페이지 경로에 따라 활성화 상태 설정
    let currentPath = window.location.pathname;

    if (currentPath.includes('/club')) {
        $('#clubBtn').addClass('active');
    } else if (currentPath.includes('/rental')) {
        $('#rentalBtn').addClass('active');
    }

    $('#clubBtn').click(function() {
        $(this).addClass('active');
        $('#rentalBtn').removeClass('active');
    });

    $('#rentalBtn').click(function() {
        $(this).addClass('active');
        $('#clubBtn').removeClass('active');
    });
});
