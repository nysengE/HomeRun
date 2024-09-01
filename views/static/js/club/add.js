let addfrm = document.addfrm;
let prebtn = document.getElementById('prebtn');

// 목록버튼 click
prebtn.addEventListener('click', () => {
    console.log('hello')
    window.location.href = '/club';
});


// 제출버튼 click
addfrm.addEventListener('submit', async (e) => {
    e.preventDefault();
    // userid 숨겨진 input
    // const userid_text = document.getElementById('author').textContent;
    // document.getElementById('userid').value=userid_text;
    // console.log('type: ', typeof(parseInt(document.querySelector('#sports').value)));

    const formData = new FormData(addfrm);

    // formData.forEach((value, key) => {
    //     console.log(`${key}: ${value}`, typeof(value));
    // });

    try {
        await fetch('/club/add', {
            method: 'POST',
            body: formData,
            redirect: 'follow'
        })
            .then((res) => {
                if (res.redirected) {
                    location.href = res.url;
                }
            })
            .then(result => console.log(result))
            .catch(error => console.error('Error:', error));
        // .then(response => response.json())
        // .then(data => console.log(data))
        // .catch(error => console.error('Error: ', error));
    } catch (error) {
        console.error(error);
    }
});