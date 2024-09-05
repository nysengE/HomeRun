const applyusers = document.querySelectorAll('.applyusers');

applyusers.forEach((applybtn) => {
    applybtn.addEventListener('click', async (e) => {
        const clubno = applybtn.querySelector('#applyclubno').value;

        try {
           let jsondata = {};
           jsondata['clubno'] = clubno;

           await fetch(`/mypage/clubwrite/apply`, {
            method: 'POST',
               headers: {
                   'Accept': 'application/json',
                   'Content-Type': 'application/json'
               },
               body: JSON.stringify(jsondata),
               redirect: 'follow'
           }).then((res) => {
               // if (res.redirected) location.href = res.url;
               return res.json();
           })
           .then((data) => {
               // console.log(data);
               if (data.applylist) {
                   // console.log('Apply List:', data.applylist);
                   // 추가적인 처리 로직을 여기에 추가
                   applylist = data.applylist;

                   const tableBody = document.getElementById('applyTableBody');
                   const table = document.getElementById('applyTable');
                   const noApplicants = document.getElementById('noApplicants');

                   tableBody.innerHTML = '';

                   if (applylist && applylist.length > 0) {
                       // 신청자 목록이 있을 때 테이블 표시
                       applylist.forEach(applicant => {
                           const row = document.createElement('tr');
                           // console.log('applicant: ', applicant);

                           // 버튼의 활성화 상태를 결정하는 조건
                           const buttonClass = applicant.status === '승인' ? 'btn-secondary' : 'btn-success';
                           const buttonDisabled = applicant.status === '승인' ? 'disabled' : '';

                           row.innerHTML = `
                            <td>${applicant.userid}</td>
                            <td>${applicant.regdate}</td>
                            <td>${applicant.status}</td>
                            <td>
                                <button type="button" class="btn ${buttonClass}" ${buttonDisabled} data-ano="${applicant.ano}">승인</button>
                            </td>
                        `;
                           tableBody.appendChild(row);
                       });
                       table.style.display = 'table';
                       noApplicants.style.display = 'none';
                   } else {
                       // 신청자 목록이 없을 때 메시지 표시
                       table.style.display = 'none';
                       noApplicants.style.display = 'block';
                   }

                   // 승인 버튼에 이벤트 추가
                   const approveButtons = document.querySelectorAll('.btn-success:not([disabled])');
                   approveButtons.forEach(button => {
                       button.addEventListener('click', async (e) => {
                           const ano = button.getAttribute('data-ano');

                           console.log('ano: ', ano);

                           try {
                               const response = await fetch('/mypage/clubwrite/approve', {
                                   method: 'POST',
                                   headers: {
                                       'Accept': 'application/json',
                                       'Content-Type': 'application/json'
                                   },
                                   body: JSON.stringify({ ano })
                               });

                               const result = await response.json();
                               if (result.success) {
                                   alert('승인되었습니다.');
                                   button.classList.replace('btn-success', 'btn-secondary');
                                   button.setAttribute('disabled', true);

                                   window.location.href = '/mypage/clubwrite';
                               } else {
                                   alert('승인 실패.');
                               }
                           } catch (error) {
                               console.error('승인 중 오류 발생:', error);
                           }
                       });
                   });

               }
            })


        } catch(error) {
            console.error('데이터 가져오기 실패:', error);
        }

    })
});

// 수정 페이지로 이동
const modifyclub = (clubno) => {
    console.log('clubno: ', clubno);
    window.location.href = '/mypage/clubwrite/modify/'+clubno;
}

// 삭제
const deleteclub = (clubno) => {
    if (confirm('정말 삭제하시겠습니까?')) {
        fetch(`/mypage/clubwrite/${clubno}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if(data.success){
                    alert('삭제되었습니다.');
                    location.reload();
                } else {
                    alert('삭제되지않았습니다.')
                }
        })
            .catch(error => {
                console.error('삭제 중 오류 발생: ', error);
                alert('오류가 발생했습니다.');
            })
    }
};

