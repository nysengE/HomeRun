document.addEventListener('DOMContentLoaded', function() {
    // 전역 변수 선언
    var maxPeople = parseInt("{{ rent.people }}", 10);
    var selectedPeople = 1;
    var selectedDate = null;
    var selectedTime = null;

    // 예약 페이지에서 사용 가능 날짜 불러오기 및 표시
    var calendarEl = document.getElementById('calendar');
    var spaceno = "{{ rent.spaceno }}";  // 이 부분은 서버 템플릿 엔진에서 치환되어야 함

    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
            initialView: 'dayGridMonth',
            locale: 'ko',
            themeSystem: 'bootstrap',
            headerToolbar: {
                left: 'prev,next today',
                center: 'title',
                right: 'dayGridMonth,timeGridWeek,timeGridDay'
            },
            events: function(fetchInfo, successCallback, failureCallback) {
                fetch(`/api/rental/${spaceno}/avail_dates`)
                    .then(response => response.json())
                    .then(data => {
                        if (Array.isArray(data)) {
                            var events = data.map(date => ({
                                title: '예약 가능',
                                start: date,
                                display: 'background'
                            }));
                            successCallback(events);
                        } else {
                            console.error('Unexpected data format:', data);
                            failureCallback('Unexpected data format');
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching available dates:', error);
                        failureCallback(error);
                    });
            },
            buttonText: {
                today: '오늘',
                month: '월',
                week: '주',
                day: '일'
            },
            dateClick: function(info) {
                // 날짜 선택 시 처리 로직
                console.log('Selected date:', info.dateStr);
                selectedDate = info.dateStr;
                updateSelectedInfo();
            }
        });

        calendar.render();
    }

    // 시간 슬롯 생성 코드
    var morningSlots = ['09:00', '11:00'];
    var afternoonSlots = ['13:00', '15:00', '17:00', '19:00', '21:00'];

    function generateTimeSlots() {
        var morningSlotsEl = document.getElementById('morningSlots');
        var afternoonSlotsEl = document.getElementById('afternoonSlots');

        morningSlots.forEach(function(time) {
            var button = document.createElement('button');
            button.className = 'btn btn-outline-secondary time-slot';
            button.textContent = time;
            button.addEventListener('click', function() {
                selectedTime = time;
                updateSelectedInfo();
            });
            morningSlotsEl.appendChild(button);
        });

        afternoonSlots.forEach(function(time) {
            var button = document.createElement('button');
            button.className = 'btn btn-outline-secondary time-slot';
            button.textContent = time;
            button.addEventListener('click', function() {
                selectedTime = time;
                updateSelectedInfo();
            });
            afternoonSlotsEl.appendChild(button);
        });
    }

    generateTimeSlots();

    // 선택된 날짜와 시간을 업데이트하는 함수
    function updateSelectedInfo() {
        document.getElementById('selectedDateDisplay').innerText = selectedDate || '선택되지 않음';
        document.getElementById('selectedTimeDisplay').innerText = selectedTime || '선택되지 않음';
    }

    // 인원 수 증가/감소 버튼 이벤트
    document.getElementById('increasePeople').addEventListener('click', function() {
        if (selectedPeople < maxPeople) {
            selectedPeople++;
            document.getElementById('selectedPeople').innerText = selectedPeople;
        }
    });

    document.getElementById('decreasePeople').addEventListener('click', function() {
        if (selectedPeople > 1) {
            selectedPeople--;
            document.getElementById('selectedPeople').innerText = selectedPeople;
        }
    });

    // 토글 스위치 로직
    document.getElementById('confirmSelection').addEventListener('change', function() {
        document.getElementById('makeReservation').disabled = !this.checked;
    });

    // 예약하기 버튼 클릭 이벤트
    document.getElementById('makeReservation').addEventListener('click', function() {
        if (!selectedDate || !selectedTime) {
            alert('날짜와 시간을 선택해주세요.');
            return;
        }

        var reservationData = {
            spaceno: "{{ rent.spaceno }}",
            resdate: selectedDate,
            restime: selectedTime,
            people: selectedPeople,
            price: "{{ rent.price }}"
        };

        fetch('/api/reservation', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(reservationData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/payment?resno=' + data.resno;
                } else {
                    alert('예약에 실패했습니다. 다시 시도해주세요.');
                }
            })
            .catch(error => {
                console.error('예약 처리 중 오류 발생:', error);
                alert('예약 처리 중 오류가 발생했습니다. 다시 시도해주세요.');
            });
    });
});
