import streamlit as st
import calendar
from datetime import datetime
from streamlit_calendar import calendar as cal

# 색상 매핑
COLOR_MAP = {
    "D": "#FDBA74",    # Day - 주황
    "N": "#A78BFA",    # Night - 보라
    "E": "#F9A8D4",    # Evening - 핑크
    "X": "#F87171",    # Off - 빨강
    "P": "#60A5FA",    # 교육 - 파랑
}

# 범례 HTML + 스타일
LEGEND = """
<style>
.legend-item {
    display: inline-flex;
    align-items: center;
    margin-right: 15px;
    font-weight: 600;
    font-size: 0.95rem;
    user-select: none;
}
.legend-color {
    width: 14px;
    height: 14px;
    display: inline-block;
    margin-right: 6px;
    border-radius: 3px;
}
</style>
<div>
  <div class="legend-item"><span class="legend-color" style="background-color:#FDBA74"></span>Day</div>
  <div class="legend-item"><span class="legend-color" style="background-color:#A78BFA"></span>Night</div>
  <div class="legend-item"><span class="legend-color" style="background-color:#F9A8D4"></span>Evening</div>
  <div class="legend-item"><span class="legend-color" style="background-color:#F87171"></span>Off</div>
  <div class="legend-item"><span class="legend-color" style="background-color:#60A5FA"></span>교육</div>
</div>
"""

# 페이지 기본 설정 및 스타일
st.set_page_config(page_title="근무표 생성기", page_icon="🩺", layout="wide")

st.markdown("""
<style>
            
    .block-container {
        max-width: 900px;
        padding: 1.5rem 2rem;
        margin: auto;
    }
    h1 {
        text-align: center;
        font-weight: 700;
    }
    label {
        font-weight: 600;
        margin-bottom: 0.25rem;
        display: block;
    }
    .stTextInput>div>input, .stNumberInput>div>input {
        font-size: 1rem;
        padding: 0.4rem 0.6rem;
        margin-bottom: 1rem;
    }
    .stButton button {
        font-size: 1.1rem;
        padding: 0.6rem 1.2rem;
    }
    /* 모바일 대응 */
    @media (max-width: 600px) {
        .block-container {
            padding: 1rem;
        }
        h1 {
            font-size: 1.5rem;
        }
        .stButton button {
            width: 100%;
        }
        div[data-testid="stVerticalBlock"] > div > iframe {
            width: 100% !important;
            min-height: 650px !important;
        }
    }
    /* 달력 범례 스타일 */
    .legend-item {
        display: inline-flex;
        align-items: center;
        margin-right: 15px;
        font-weight: 600;
        font-size: 0.95rem;
        user-select: none;
    }
    .legend-color {
        width: 14px;
        height: 14px;
        display: inline-block;
        margin-right: 6px;
        border-radius: 3px;
    }
            
    /* 이벤트 텍스트 중앙 정렬 (가로 + 세로) */
    .fc-event-main {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        height: 100% !important;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0 !important;
        text-align: center;
    }
    .fc-event-title {
        width: 100%;
        text-align: center;
    }
            /* 이벤트 박스 중앙 정렬 */
    .fc-event {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        height: 100% !important;
        font-weight: 600;
        font-size: 0.95rem;
        padding: 0 !important;
        text-align: center;
    }


</style>
""", unsafe_allow_html=True)

# 제목 및 구분선
st.title("📅 근무표 생성기")
st.markdown("<hr style='border: 1px solid #ddd'>", unsafe_allow_html=True)

# 입력폼
name = st.text_input("이름을 입력하세요:")

# 년도와 월을 selectbox로 선택
col1, col2 = st.columns(2)
with col1:
    year = st.selectbox("년도를 선택하세요:", 
                       options=list(range(2020, 2101)), 
                       index=list(range(2020, 2101)).index(datetime.now().year))
with col2:
    month_names = ["1월", "2월", "3월", "4월", "5월", "6월", 
                   "7월", "8월", "9월", "10월", "11월", "12월"]
    month_selection = st.selectbox("월을 선택하세요:", 
                                  options=month_names, 
                                  index=0)
    month = month_names.index(month_selection) + 1
code = st.text_input("근무코드를 입력하세요 (D: Day, N: Night, E: Evening, X: Off, P: 교육)", max_chars=31)

# 버튼 클릭 시 달력 생성 여부 저장할 상태 초기화
if "show_calendar" not in st.session_state:
    st.session_state.show_calendar = False

if st.button("근무표 달력 생성") and code:
    days_in_month = calendar.monthrange(year, month)[1]
    if len(code) != days_in_month:
        st.error(f"입력한 근무코드 길이가 {days_in_month}일과 다릅니다.")
        st.session_state.show_calendar = False
    else:
        st.session_state.show_calendar = True

if st.session_state.show_calendar:
    st.success(f"{year}년 {month}월 {name}님의 근무 달력")

    events = []
    days_in_month = calendar.monthrange(year, month)[1]

    for day in range(1, days_in_month + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        work_type = code[day - 1]
        color = COLOR_MAP.get(work_type, "#E5E7EB")

        label = "OFF" if work_type == "X" else (work_type if work_type in COLOR_MAP else "기타")

        events.append({
            "title": label,
            "start": date_str,
            "end": date_str,
            "color": color,
        })

    cal_options = {
        "initialView": "dayGridMonth",
        "initialDate": f"{year}-{month:02d}-01",
        "locale": "ko",
        "headerToolbar": {
            "left": "",
            "center": "title",
            "right": ""
        },
        "eventDisplay": "block",
        "height": 500,
        "contentHeight": 500,
        "aspectRatio": 1.2,
        "fixedWeekCount": False
    }

    cal(events=events, options=cal_options)

    # 📌 달력 바로 아래 범례 출력
    st.markdown(LEGEND, unsafe_allow_html=True)


st.markdown("<hr style='border: 1px solid #ddd'>", unsafe_allow_html=True)
st.info("근무코드는 정확한 날짜 수에 맞게 D/N/E/X/P 로 입력해주세요.")

st.expander("예시 보기").markdown("""
**7월 31일 기준 근무코드 예시:**  
`DDNEXXPPDDNEXXPPDDNEXXPPDDNEXXP`

**설명:**  
- D = Day 근무  
- N = Night 근무  
- E = Evening 근무  
- X = 비번 (Off)  
- P = 교육
""")
