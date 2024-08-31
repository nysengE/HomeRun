document.addEventListener('DOMContentLoaded', function() {
    const monthYear = document.getElementById('reservationMonthYear');
    const daysContainer = document.querySelector('.reservation-days');
    // const timeCanvas = document.getElementById('reservationTimeCanvas');
    // const ctx = timeCanvas.getContext('2d');

    // timeCanvas와 관련된 모든 코드를 주석 처리 또는 삭제

    let currentMonthIndex = 0;  // 현재 달의 인덱스 (0: 현재 달, 1: 다음 달, 2: 다다음 달)
    const currentDate = new Date();  // 현재 날짜
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();  // 현재 달 (0부터 시작)

    function generateCalendar(year, month) {
        daysContainer.innerHTML = '';
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        monthYear.textContent = `${year}년 ${month + 1}월`;

        // 이전 달의 빈 칸 채우기
        for (let i = 0; i < firstDay.getDay(); i++) {
            const emptyDay = document.createElement('span');
            daysContainer.appendChild(emptyDay);
        }

        for (let i = 1; i <= lastDay.getDate(); i++) {
            const dayElement = document.createElement('span');
            dayElement.textContent = i;

            const isPast = new Date(year, month, i) < currentDate;
            dayElement.classList.add(isPast ? 'past' : 'available');

            if (!isPast) {
                dayElement.addEventListener('click', function() {
                    selectDate(`${year}-${(month + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`);
                });
            }

            daysContainer.appendChild(dayElement);
        }
    }

    function selectDate(date) {
        const allDays = document.querySelectorAll('.reservation-days span');
        allDays.forEach(day => day.classList.remove('active'));

        const [year, month, day] = date.split('-').map(Number);
        const selectedDay = document.querySelector(`.reservation-days span:nth-child(${day + new Date(year, month - 1, 1).getDay()})`);
        if (selectedDay) selectedDay.classList.add('active');
    }

    document.getElementById('prevMonth').addEventListener('click', function() {
        if (currentMonthIndex > 0) {
            currentMonthIndex--;
            generateCalendar(currentYear, currentMonth + currentMonthIndex);
        }
    });

    document.getElementById('nextMonth').addEventListener('click', function() {
        if (currentMonthIndex < 2) {
            currentMonthIndex++;
            generateCalendar(currentYear, currentMonth + currentMonthIndex);
        }
    });

    // 초기 달력 생성
    generateCalendar(currentYear, currentMonth);
});


document.addEventListener('DOMContentLoaded', function() {
    const monthYear = document.getElementById('reservationMonthYear');
    const daysContainer = document.querySelector('.reservation-days');

    const holidays = {
        "2024-01-01": "New Year's Day",
        "2024-03-01": "Independence Movement Day",
        "2024-05-05": "Children's Day",
        "2024-06-06": "Memorial Day",
        "2024-08-15": "Liberation Day",
        "2024-09-16": "Chuseok", // 추석 추가
        "2024-09-17": "Chuseok", // 추석 추가
        "2024-09-18": "Chuseok", // 추석 추가
        "2024-10-03": "National Foundation Day",
        "2024-10-09": "Hangeul Day",
        "2024-12-25": "Christmas Day"
    };

    let currentMonthIndex = 0;  // 현재 달의 인덱스 (0: 현재 달, 1: 다음 달, 2: 다다음 달)
    const currentDate = new Date();  // 현재 날짜
    const currentYear = currentDate.getFullYear();
    const currentMonth = currentDate.getMonth();  // 현재 달 (0부터 시작)

    function generateCalendar(year, month) {
        daysContainer.innerHTML = '';
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        monthYear.textContent = `${year}년 ${month + 1}월`;

        // 이전 달의 빈 칸 채우기
        for (let i = 0; i < firstDay.getDay(); i++) {
            const emptyDay = document.createElement('span');
            daysContainer.appendChild(emptyDay);
        }

        for (let i = 1; i <= lastDay.getDate(); i++) {
            const dayElement = document.createElement('span');
            dayElement.textContent = i;

            const date = new Date(year, month, i);
            const isPast = date < currentDate;

            const dayString = `${year}-${(month + 1).toString().padStart(2, '0')}-${i.toString().padStart(2, '0')}`;
            if (holidays[dayString]) {
                dayElement.classList.add('holiday');
                if (isPast) {
                    dayElement.classList.add('past');
                }
            } else if (date.getDay() === 0) {
                dayElement.classList.add('sunday');
                if (isPast) {
                    dayElement.classList.add('past');
                }
            } else if (!isPast) {
                dayElement.classList.add('available');
                dayElement.addEventListener('click', function() {
                    selectDate(dayString);
                });
            } else {
                dayElement.classList.add('past');
            }

            daysContainer.appendChild(dayElement);
        }
    }

    function selectDate(date) {
        const allDays = document.querySelectorAll('.reservation-days span');
        allDays.forEach(day => day.classList.remove('active'));

        const [year, month, day] = date.split('-').map(Number);
        const selectedDay = document.querySelector(`.reservation-days span:nth-child(${day + new Date(year, month - 1, 1).getDay()})`);
        if (selectedDay) selectedDay.classList.add('active');
    }

    document.getElementById('prevMonth').addEventListener('click', function() {
        if (currentMonthIndex > 0) {
            currentMonthIndex--;
            generateCalendar(currentYear, currentMonth + currentMonthIndex);
        }
    });

    document.getElementById('nextMonth').addEventListener('click', function() {
        if (currentMonthIndex < 2) {
            currentMonthIndex++;
            generateCalendar(currentYear, currentMonth + currentMonthIndex);
        }
    });

    // 초기 달력 생성
    generateCalendar(currentYear, currentMonth);
});

