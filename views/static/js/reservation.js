document.addEventListener('DOMContentLoaded', function() {
    const monthYear = document.getElementById('reservationMonthYear');
    const daysContainer = document.querySelector('.reservation-days');
    const timeCanvas = document.getElementById('reservationTimeCanvas');
    const ctx = timeCanvas.getContext('2d');

    const timeSlots = {
        "2024-08-27": [],
        "2024-08-28": ["12:00 - 13:00", "14:00 - 15:00"],
        "2024-08-29": ["09:00 - 10:00", "15:00 - 16:00"],
        "2024-08-30": [],
        "2024-08-31": ["09:00 - 10:00", "11:00 - 12:00", "13:00 - 14:00"]
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

        updateClock(date);  // 시계 업데이트
    }

    function updateClock(date) {
        ctx.clearRect(0, 0, timeCanvas.width, timeCanvas.height); // 이전 캔버스 지우기
        drawClockFace(); // 시계의 원 바깥쪽에 시간 표시
        const times = timeSlots[date] || [];

        // 현재 시간 계산
        const now = new Date();
        const currentHours = now.getHours();
        const currentMinutes = now.getMinutes();
        const currentAngle = ((currentHours + currentMinutes / 60) / 24) * 360;

        // 지난 시간 표시 (회색)
        drawTimeSegment(-90, currentAngle - 90, '#e8e4e4');

        if (times.length === 0) return; // 예약 가능한 시간이 없을 경우 종료

        // 예약 가능한 시간 표시 (파란색) 및 클릭 이벤트 추가
        times.forEach(time => {
            const [start, end] = time.split(' - ').map(t => parseTimeToAngle(t));
            drawTimeSegment(start, end, '#007bff', function() {
                alert(`예약 가능한 시간: ${time}`); // 클릭 시 예약 가능 시간 알림
            });
        });
    }

    function parseTimeToAngle(time) {
        const [hours, minutes] = time.split(':').map(Number);
        return ((hours + minutes / 60) / 24) * 360; // 24시간 기준 각도를 360도로 변환
    }

    function drawTimeSegment(startAngle, endAngle, color, clickHandler) {
        ctx.beginPath();
        ctx.moveTo(100, 100);
        ctx.arc(100, 100, 80, (startAngle - 90) * Math.PI / 180, (endAngle - 90) * Math.PI / 180); // 90도 회전 조정
        ctx.closePath();
        ctx.fillStyle = color;
        ctx.fill();

        // 클릭 가능한 시간 영역 설정
        if (clickHandler) {
            timeCanvas.addEventListener('click', function(event) {
                const rect = timeCanvas.getBoundingClientRect();
                const x = event.clientX - rect.left - 100; // 캔버스 중심으로 좌표 조정
                const y = event.clientY - rect.top - 100;
                const angle = Math.atan2(y, x) * (180 / Math.PI) + 90;
                const normalizedAngle = (angle + 360) % 360;
                if (normalizedAngle >= startAngle && normalizedAngle <= endAngle) {
                    clickHandler();
                }
            });
        }
    }

    function drawClockFace() {
        ctx.clearRect(0, 0, timeCanvas.width, timeCanvas.height); // 이전 캔버스 지우기

        // 시계 원 그리기
        ctx.beginPath();
        ctx.arc(100, 100, 80, 0, 2 * Math.PI);
        ctx.strokeStyle = '#ded7d7'; // 선 색상 설정
        ctx.stroke();

        // 시계의 각 위치에 24시간 기준으로 시간 표시
        ctx.font = '14px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('24', 100, 20);   // 24시 위치 (위)
        ctx.fillText('6', 180, 100);   // 6시 위치 (오른쪽)
        ctx.fillText('12', 100, 180);  // 12시 위치 (아래)
        ctx.fillText('18', 20, 100);   // 18시 위치 (왼쪽)
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
    drawClockFace(); // 초기 시계 표시
});
