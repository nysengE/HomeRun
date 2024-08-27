document.addEventListener('DOMContentLoaded', function() {
    const monthYear = document.getElementById('reservationMonthYear');
    const daysContainer = document.querySelector('.reservation-days');
    const timeCanvas = document.getElementById('reservationTimeCanvas');
    const ctx = timeCanvas.getContext('2d');  // timeCanvas가 존재하는지 확인 후 사용

    const timeSlots = {
        "2024-08-27": [],
        "2024-08-28": ["12:00 - 13:00", "14:00 - 15:00"],
        "2024-08-29": ["09:00 - 10:00", "15:00 - 16:00"],
        "2024-08-30": [],
        "2024-08-31": ["09:00 - 10:00", "11:00 - 12:00", "13:00 - 14:00"]
    };

    function generateCalendar() {
        daysContainer.innerHTML = '';
        for (let i = 27; i <= 31; i++) {
            const dayElement = document.createElement('span');
            dayElement.textContent = i;
            dayElement.addEventListener('click', function() {
                selectDate(`2024-08-${i.toString().padStart(2, '0')}`);
            });
            daysContainer.appendChild(dayElement);
        }
    }

    function selectDate(date) {
        const allDays = document.querySelectorAll('.reservation-days span');
        allDays.forEach(day => day.classList.remove('active'));

        const dayNumber = parseInt(date.split('-')[2]);
        const selectedDay = document.querySelector(`.reservation-days span:nth-child(${dayNumber - 26})`);
        if (selectedDay) selectedDay.classList.add('active');

        updateClock(date);
    }

    function updateClock(date) {
        ctx.clearRect(0, 0, timeCanvas.width, timeCanvas.height); // 이전 캔버스 지우기
        const times = timeSlots[date] || [];

        // 시계 원 그리기
        ctx.beginPath();
        ctx.arc(100, 100, 80, 0, 2 * Math.PI);
        ctx.stroke();

        if (times.length === 0) return; // 예약 가능한 시간이 없을 경우 종료

        times.forEach(time => {
            const [start, end] = time.split(' - ').map(t => parseTimeToAngle(t));
            drawTimeSegment(start, end);
        });
    }

    function parseTimeToAngle(time) {
        const [hours, minutes] = time.split(':').map(Number);
        return ((hours % 12) + minutes / 60) * 30 - 90; // 각도를 도 단위로 변환하고 시계 방향으로 조정
    }

    function drawTimeSegment(startAngle, endAngle) {
        ctx.beginPath();
        ctx.moveTo(100, 100);
        ctx.arc(100, 100, 80, startAngle * Math.PI / 180, endAngle * Math.PI / 180);
        ctx.closePath();
        ctx.fillStyle = '#007bff';
        ctx.fill();
    }

    generateCalendar();
    selectDate('2024-08-27'); // 초기 선택 날짜
});
