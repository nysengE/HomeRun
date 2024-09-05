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

    function updateButtonWidth() {
        return clubBtn.outerWidth(); // 항상 최신의 버튼 너비를 계산
    }

    function setActiveButton() {
        let currentPath = window.location.pathname;
        let buttonWidth = updateButtonWidth();

        if (currentPath === '/club' || currentPath === '/club/') {
            sliding.css('left', '0');
            clubBtn.addClass('active');
            rentalBtn.removeClass('active');
        } else if (currentPath === '/rental' || currentPath === '/rental/') {
            sliding.css('left', `${buttonWidth}px`);
            rentalBtn.addClass('active');
            clubBtn.removeClass('active');
        }
    }

    setActiveButton();

    clubBtn.click(function() {
        let buttonWidth = updateButtonWidth();
        sliding.animate({left: '0'}, 300);
        clubBtn.addClass('active');
        rentalBtn.removeClass('active');
    });

    rentalBtn.click(function() {
        let buttonWidth = updateButtonWidth();
        sliding.animate({left: `${buttonWidth}px`}, 300);
        rentalBtn.addClass('active');
        clubBtn.removeClass('active');
    });
});
