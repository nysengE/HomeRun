// 현재 페이지 링크 활성화
document.addEventListener('DOMContentLoaded', function() {
    console.log('hello');
    const currentPath = window.location.hash || 'mypage/user'; // 기본값 설정
    // console.log(currentPath)
    const activeLink = document.querySelector(`.nav-link[href="/${currentPath}"]`);
    console.log(activeLink)
    if (activeLink) {
        activeLink.classList.add('active');
        // 드롭다운 메뉴 항목 활성화
        if (activeLink.classList.contains('dropdown-toggle')) {
            const dropdownMenu = document.querySelector(`#${activeLink.getAttribute('aria-controls')} .dropdown-menu`);
            if (dropdownMenu) {
                dropdownMenu.classList.add('show');
            }
        }
        console.log(currentPath)
        // 해당 콘텐츠 보이기
        // document.querySelector(currentPath)?.classList.add('show', 'active');
    }
});