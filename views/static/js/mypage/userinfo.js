const checkpwdfrm = document.checkpwdfrm;
const modifyuserContainer = document.getElementById('modifyuser-container');
const checkpwdContainer = document.getElementById('checkpwd-container');

modifyuserContainer.style.display = 'none';
checkpwdContainer.style.display = 'block';

// 비밀번호 확인
checkpwdfrm.addEventListener('submit', async(e) => {
    e.preventDefault();

    const formData = new FormData(checkpwdfrm);

    const data ={};
    formData.forEach((value, key) => {
        data[key] = value;
    });

    try {
    const response = await fetch('/mypage/checkpwd', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    });

        const result = await response.json();

        if (result.success) {
            // 비밀번호가 맞으면 수정 작업 수행
            alert('비밀번호가 확인되었습니다.');
            // modifyuserfrm.style.display = 'block';
            // checkpwdfrm.style.display = 'none';
            modifyuserContainer.style.display = 'block';
            checkpwdContainer.style.display = 'none';
        } else {
            alert('비밀번호가 일치하지 않습니다. 다시 시도해 주세요.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('서버에 문제가 발생했습니다. 나중에 다시 시도해 주세요.');
    }
})

// 수정하기
const modifyuserfrm = document.modifyuserfrm;
modifyuserfrm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(modifyuserfrm);

    const passwd = formData.get('passwd');
    const ckpasswd = formData.get('ckpasswd');

    if (passwd && passwd !== ckpasswd) {
        alert('비밀번호가 일치하지 않습니다. 다시 시도해 주세요.');
        return;
    }

    formData.delete('ckpasswd');

    if (passwd === '') {
        formData.delete('passwd');
    }

    // const birth = formData.get('birth');
    // if (birth) {
    //     const date = new Date(birth);
    //     if (!isNaN(date.getTime())) {
    //         formData.set('birth', date.toISOString().split('T')[0]); // Format as 'YYYY-MM-DD'
    //     } else {
    //         console.error('Invalid date format');
    //     }
    // } else {
    //     formData.delete('birth'); // Remove birth field if it's empty
    // }

    formData.forEach((value, key) => {
        console.log(`${key}: ${value}`, typeof(value));
    });

    try {

        const response =await fetch('/mypage/userinfo', {
            method: 'PUT',
            body: formData,
            redirect: 'follow'
        });

        if(response.ok) {
            alert('수정되었습니다.');
            location.reload(true);
        } else {
            console.error('Update failed:', response.statusText);
        }

    } catch (error) {
        console.error(error);
    }

});