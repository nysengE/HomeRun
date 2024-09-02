const checkpwdfrm = document.checkpwdfrm;
const modifyuserfrm = document.getElementById('modifyuser-container');
const checkpwdContainer = document.getElementById('checkpwd-container');

modifyuserfrm.style.display = 'none';
checkpwdContainer.style.display = 'block';

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
            modifyuserfrm.style.display = 'block';
            checkpwdContainer.style.display = 'none';
        } else {
            alert('비밀번호가 일치하지 않습니다. 다시 시도해 주세요.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('서버에 문제가 발생했습니다. 나중에 다시 시도해 주세요.');
    }
})