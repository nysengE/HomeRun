const checkpwdfrm = document.checkpwdfrm;

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
            // 여기서 추가로 비밀번호 수정 요청 등을 처리할 수 있습니다.
        } else {
            // 비밀번호가 일치하지 않으면 알림 표시
            alert('비밀번호가 일치하지 않습니다. 다시 시도해 주세요.');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('서버에 문제가 발생했습니다. 나중에 다시 시도해 주세요.');
    }
})