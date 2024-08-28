const addbtn = document.querySelector('#addbtn');

console.log('hello')

// clubno
const clubcard = document.querySelectorAll('.clubcard');
clubcard.forEach((card) => {
    card.addEventListener('click', () => {
        // const clubno = parseInt(card.querySelector('#clubno').value);
        const clubno = card.querySelector('#clubno').value;


        window.location.href=`/club/view/${clubno}`;


        // // clubno 값을 콘솔에 출력 (디버깅용)
        // console.log('Club Number:', clubno);
    })
})

addbtn.addEventListener('click', () => {
    window.location.href = '/club/add';
})