# 필요한 패키지 설치: pip install sxtwl pytz
import sxtwl
from datetime import datetime
from pytz import timezone

# 십간, 십이지 리스트
GAN = ["갑", "을", "병", "정", "무", "기", "경", "신", "임", "계"]
ZHI = ["자", "축", "인", "묘", "진", "사", "오", "미", "신", "유", "술", "해"]

def get_ganzhi(gz):
    return GAN[gz.tg] + ZHI[gz.dz]

def get_sexagenary_info(birth_str, birth_time_str, gender="남자", is_lunar=False, is_leap=False):
    """
    생년월일과 시간 기준으로 사주 및 운세 출력
    - birth_str: "YYYYMMDD"
    - birth_time_str: "HHMM" or "모름"
    - gender: "남자" or "여자"
    - is_lunar: 음력 입력 여부
    - is_leap: 윤달 여부 (음력인 경우)
    """
    # 1. 입력 날짜 및 시간 처리
    birth_date = datetime.strptime(birth_str, "%Y%m%d")
    if birth_time_str != "모름":
        birth_time = datetime.strptime(birth_time_str, "%H%M").time()
        birth_date = datetime.combine(birth_date, birth_time)
    else:
        birth_date = datetime.combine(birth_date, datetime.min.time())

    # 2. 한국 시간대 적용
    birth_date = timezone("Asia/Seoul").localize(birth_date)
    y, m, d = birth_date.year, birth_date.month, birth_date.day

    # 3. 간지 계산용 날짜 객체 생성
    if not is_lunar:
        day = sxtwl.fromSolar(y, m, d)
    else:
        day = sxtwl.fromLunar(y, m, d, is_leap)

    # 4. 년주, 월주, 일주
    year_gz = day.getYearGZ(True)   # 입춘 기준
    month_gz = day.getMonthGZ()
    day_gz = day.getDayGZ()

    # 5. 시주 계산
    if birth_time_str != "모름":
        hour = birth_date.hour
        branch_index = ((hour + 1) // 2) % 12
        stem_index = (day_gz.tg * 2 + branch_index) % 10
        hour_gz = GAN[stem_index] + ZHI[branch_index]
    else:
        hour_gz = "모름"

    # 6. 현재 시점 기준 세운, 월운
    now = datetime.now(timezone("Asia/Seoul"))
    now_day = sxtwl.fromSolar(now.year, now.month, now.day)
    current_year_gz = get_ganzhi(now_day.getYearGZ(True))
    current_month_gz = get_ganzhi(now_day.getMonthGZ())

    # 7. 대운 계산 (단순화된 버전)
    is_male = gender == "남자"
    is_yang = year_gz.tg % 2 == 0
    forward = (is_male and is_yang) or (not is_male and not is_yang)

    base_index = (month_gz.tg * 10 + month_gz.dz) % 60
    current_age = now.year - y
    steps = current_age // 10

    if forward:
        du_index = (base_index + steps) % 60
    else:
        du_index = (base_index - steps) % 60

    du_gan = GAN[du_index % 10]
    du_zhi = ZHI[du_index % 12]
    current_daewoon = du_gan + du_zhi

    # 8. 결과 반환
    return {
        "년주": get_ganzhi(year_gz),
        "월주": get_ganzhi(month_gz),
        "일주": get_ganzhi(day_gz),
        "시주": hour_gz,
        # "대운": current_daewoon,
        # "세운": current_year_gz,
        # "월운": current_month_gz
    }
