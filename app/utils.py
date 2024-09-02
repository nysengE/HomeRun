
from datetime import datetime

def format_time(value, format='%H:%M'):
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%H:%M:%S')  # HH:MM:SS 형식의 문자열을 파싱
        except ValueError:
            return value  # 파싱 실패 시 원래 값을 반환
    return value.strftime(format)
