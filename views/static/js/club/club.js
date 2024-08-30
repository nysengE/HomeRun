
// // dropdown 데이터 넣기
// const sports = document.querySelector('.sports');
// const regions = document.querySelector('.regions');
//
// console.log(sports);
// const li = document.createElement('li');
// li.textContent = '축구';
// li.classList.add('dropdown-item');
// li.dataset.value = 1;
//
// sports.append(li);

// 검색하기
let findbtn = document.querySelector('#findbtn');

findbtn.addEventListener('click', (e) => {
   e.preventDefault();

    let sports = parseInt(document.querySelector('#sports').value);
    let regions = parseInt(document.querySelector('#regions').value);
    let title = (document.querySelector('#findtext').value) || '#';


    // console.log(
    //     `sports: ${sports},
    //     regions: ${typeof (regions)},
    //     findtext: ${findtext}`
    // );

    let params = `/${sports}/${regions}/${title}/1`;
    let findurl = '/club'+params;

    location.href = findurl;

});





// clubno card 클릭시 상세보기 view
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

// 글 등록하기
const addbtn = document.querySelector('#addbtn');

addbtn.addEventListener('click', () => {
    window.location.href = '/club/add';
})