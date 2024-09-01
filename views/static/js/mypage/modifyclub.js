document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('file');
    const currentImage = document.getElementById('current-image');
    const fileContainer = document.getElementById('file-container');
    const filePreview = document.querySelector('.file-preview');

    const prebtn = document.querySelector('#prebtn');

    // 목록 페이지로 돌아가기
    prebtn.addEventListener('click', (e) => {
        e.preventDefault();

        window.location.href='/mypage/clubwrite';
    });


    // 파일 선택 시 기존 이미지 제거
    fileInput.addEventListener('change', () => {
        try {
            // 이미지 삭제 요청 보내기
            const response = fetch('/mypage/clubwrite/deletefile', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    image_url: currentImage.src
                })
            });

            if (response.ok) {
                // 서버에서 이미지 삭제 성공
                filePreview.remove(); // 이미지와 삭제 버튼 제거
                fileInput.style.display = 'block'; // 파일 입력 필드 보이기
            } else {
                alert('이미지 삭제에 실패했습니다.');
            }

            if (fileInput.files.length > 0) {
                if (currentImage) {
                    currentImage.remove();
                }
            }
        } catch (error) {
            console.error('이미지 삭제 중 오류 발생:', error);
        }

    });

    // 수정하기
    let modifyfrm = document.modifyfrm;
    modifyfrm.addEventListener('submit', async (e) => {
       e.preventDefault();

       const formData = new FormData(modifyfrm);

        // formData.forEach((value, key) => {
        //     console.log(`${key}: ${value}`, typeof(value));
        // });

        try {

            await fetch('/mypage/modify', {
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
        } catch (error) {
            console.error(error);
        }

    });

});
