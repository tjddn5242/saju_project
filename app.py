import streamlit as st
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from saju import get_sexagenary_info
from mbti import get_personality_analysis

# 페이지 설정
st.set_page_config(
    page_title="내면 동물 테스트",
    page_icon="🦁",
    layout="wide"
)

# CSS 스타일 적용
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #fafafa;
    }
    .stRadio > label {
        font-weight: bold;
        color: #2d2d2d;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF9B50;
        color: white;
        border-radius: 10px;
        padding: 0.5rem;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF7B54;
        transform: translateY(-2px);
    }
    .css-1d391kg {
        padding: 2rem;
        border-radius: 15px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# 헤더 섹션
st.title("🦁 나의 내면 동물 찾기")
st.markdown("당신의 생년월일과 MBTI를 통해 내면의 동물을 찾아보세요!")
st.markdown("---")

# 입력 섹션을 카드 형태로 구성
with st.container():
    st.markdown("### 🌟 기본 정보 입력")
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        birth_date = st.date_input(
            "생년월일을 선택하세요",
            min_value=datetime(1900, 1, 1),
            max_value=datetime.now(),
            help="태어난 날짜를 선택해주세요"
        )
    
    with col2:
        calendar_type = st.selectbox(
            "양력/음력",
            options=["양력", "음력"],
            help="생년월일의 양력/음력을 선택하세요"
        )
    
    with col3:
        time_option = st.selectbox(
            "시간 입력",
            ["입력", "모름"],
            help="출생 시간을 아는 경우 '입력'을 선택하세요"
        )
    
    if time_option == "입력":
        with col4:
            birth_time = st.time_input(
                "시간",
                help="출생 시간을 입력하세요"
            )

# MBTI 섹션
st.markdown("### 🎯 나의 성격 유형 선택")

mbti_descriptions = {
    "E/I": ["E (활동적)", "I (신중한)"],
    "N/S": ["N (상상적)", "S (현실적)"],
    "T/F": ["T (이성적)", "F (감성적)"],
    "J/P": ["J (계획적)", "P (즉흥적)"]
}

selected_mbti = []
cols = st.columns(4)

for idx, (category, options) in enumerate(mbti_descriptions.items()):
    with cols[idx]:
        st.markdown(f"**{category}**")
        selected = st.radio(
            category,
            options,
            horizontal=True,
            key=f"mbti_{category}",
            help=f"{category} 유형을 선택하세요"
        )
        selected_mbti.append(selected[0])  # 첫 글자만 저장

mbti = "".join(selected_mbti)
st.markdown(f"#### 선택된 MBTI: `{mbti}`")

# 분석 버튼
st.markdown("---")
if st.button("🔍 내면의 동물 찾기", help="입력한 정보를 바탕으로 당신의 내면 동물을 찾아드립니다"):
    with st.spinner('당신의 내면 동물을 찾고 있어요...'):
        # 사주 계산을 위한 데이터 준비
        birth_str = birth_date.strftime("%Y%m%d")
        birth_time_str = "모름" if time_option == "모름" else birth_time.strftime("%H%M")
        is_lunar = calendar_type == "음력"
        
        # 데이터 로드
        gapja_df = pd.read_csv("data/gapja.csv")
        mbti_df = pd.read_csv("data/mbti.csv")
        
        # 사주 정보 가져오기
        saju_info = get_sexagenary_info(birth_str, birth_time_str, is_lunar=is_lunar)
        
        # MBTI와 일주를 기반으로 성격 분석 정보 가져오기
        personality_info = get_personality_analysis(saju_info["일주"], mbti)
        
        # 일주에 대한 표현과 이모지 매핑
        ilju_info = gapja_df[gapja_df['60갑자'] == saju_info["일주"]].iloc[0]
        ilju_expression = ilju_info['표현']
        ilju_emoji = ilju_info['이모지']
        
        # MBTI 형용사 매핑
        mbti_info = mbti_df[mbti_df['MBTI'] == mbti]
        if len(mbti_info) > 0:
            mbti_expression = mbti_info.iloc[0]['표현']
        else:
            mbti_expression = "정보 없음"
    
    # 결과 표시
    st.markdown("## 🎉 당신의 내면 동물을 찾았어요!")
    
    # 기본 정보와 성격 유형을 카드 형태로 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("##### 📋 기본 정보")
        st.markdown(f"""
        - **생년월일**: {birth_date.strftime('%Y년 %m월 %d일')}
        - **시간**: {'모름' if time_option == '모름' else birth_time.strftime('%H시 %M분')}
        - **{calendar_type}** 기준
        """)
    
    with col2:
        st.success("##### 🐾 성격 특성")
        st.markdown(f"""
        - **MBTI**: {mbti} - *{mbti_expression}*
        - **내면 동물**: {saju_info['일주']} - *{ilju_expression}* {ilju_emoji}
        """)
    
    # 레이더 차트 생성
    st.markdown("### 📊 동물 특성 분석")
    
    # mbti.py의 파라미터 이름과 일치하도록 수정
    categories = ['외향성', '안정성', '개방성', '책임감', '친화성', '자기주도성', '이성적', '도전성']
    values = [personality_info[cat] for cat in categories]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name='동물 특성',
        line_color='#FF9B50'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickfont_size=10
            ),
            bgcolor='rgba(255,155,80,0.05)'
        ),
        showlegend=False,
        height=500,
        margin=dict(t=30)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # 직업 추천 및 키워드
    st.markdown("### 🌈 추천 진로 및 특성")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.error("##### MBTI 기반 추천")
        st.markdown(personality_info["MBIT기반 직업"])
    
    with col2:
        st.warning("##### 내면 동물 기반 추천")
        st.markdown(personality_info["사주기반 직업"])
    
    with col3:
        st.success("##### 최종 추천")
        st.markdown(personality_info["최종 직업"])
    
    # 성격 키워드
    st.markdown("#### ✨ 당신의 특별한 매력")
    st.info(personality_info["성격 키워드"])
