// JavaScript to handle click events and display the value
document.querySelectorAll('.list-group-item').forEach(item => {
    item.addEventListener('click', () => {
        const value = item.getAttribute('data-value');
        console.log(value);
    });
});

$(document).ready(function() {
    let sliding = $('.sliding');
    let clubBtn = $('#clubBtn');
    let rentalBtn = $('#rentalBtn');

    // 버튼 너비 계산
    let buttonWidth = clubBtn.outerWidth();

    // 현재 페이지 경로 확인
    let currentPath = window.location.pathname;

    // 현재 경로가 '/club' 또는 '/club/'인 경우
    if (currentPath === '/club' || currentPath === '/club/') {
        sliding.css('left', '0');
        clubBtn.addClass('active');
    }
    // 현재 경로가 '/rental' 또는 '/rental/'인 경우
    else if (currentPath === '/rental' || currentPath === '/rental/') {
        sliding.css('left', `${buttonWidth}px`);
        rentalBtn.addClass('active');
    }

    // 버튼 클릭 시 슬라이더 이동
    clubBtn.click(function() {
        sliding.animate({left: '0'}, 300);
        clubBtn.addClass('active');
        rentalBtn.removeClass('active');
    });

    rentalBtn.click(function() {
        sliding.animate({left: `${buttonWidth}px`}, 300);
        rentalBtn.addClass('active');
        clubBtn.removeClass('active');
    });

    // 슬라이더 드래그 가능 설정 (jQuery UI 필요)
    sliding.draggable({
        axis: 'x', // x축 방향으로만 드래그 가능
        containment: '.btn-group', // 드래그 가능 영역 제한
        stop: function(event, ui) {
            let slidingPosition = ui.position.left;
            if (slidingPosition < buttonWidth / 2) {
                clubBtn.trigger('click');
            } else {
                rentalBtn.trigger('click');
            }
        }
    });
});
