// 목록으로 돌아가기
const prebtn = document.querySelector('#prebtn');

prebtn.addEventListener('click', () => {
    window.location.href='/club/1';
});

// 동호회 번호 (clubno) 가져오기
const clubno = parseInt(document.querySelector('#clubno').value);


// 회원 아이디 (userid) 가져오기
const userid = document.querySelector('#userid').value;

// 신청하기
const applybtn = document.querySelector('#applybtn');
applybtn.addEventListener('click', async (e) => {
    e.preventDefault();

    window.location.href=`/club/apply/${clubno}/${userid}`;

    // // post로 보낼 데이터 json 형식으로 만들기
    // const data = {
    //     userid: userid,
    //     clubno: clubno
    // };
    //
    // try {
    //     await fetch('/club/apply', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json',
    //         },
    //         body: JSON.stringify(data)
    //     }).then((res) => {
    //         alert('신청되었습니다.');
    //         if (res.redirected) {
    //             location.href = res.url;
    //         }
    //     })
    //
    // } catch (error) {
    //     console.error('Error:', error);
    // }

});

// 댓글창
let replyfrm = document.replyfrm;

replyfrm?.addEventListener('submit', (e) => {
    e.preventDefault();

    const formData = new FormData(replyfrm);

    let jsondata = {};
    formData.forEach((val, key) => {
        jsondata[key] = val;
    });

    // formData.forEach((val, key) => {
    //     console.log(key, val);
    // });

    fetch('/club/reply', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsondata),
        redirect: 'follow'
    }).then((res) => {
        if (res.redirected) location.href = res.url;
    });
});

// '추가'버튼 누르면 hidden 댓글번호(rpno) value 값 넣기
const addrreply = (rno) => {
    let rpno = document.querySelector('#rpno');
    rpno.value = rno;
};

// 대댓글창 등록
const rreplyfrm = document.rreplyfrm;

rreplyfrm.addEventListener('submit', (e, rpno) => {
    e.preventDefault();

    const formData = new FormData(rreplyfrm);

    let jsondata = {};
    formData.forEach((val, key) => {
        jsondata[key] = val;
    });

    // formData.forEach((val, key) => {
    //     console.log(key, val);
    // });

    fetch('/club/rreply', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(jsondata),
        redirect: 'follow'
    }).then((res) => {
        if (res.redirected) location.href = res.url;
    });
});


