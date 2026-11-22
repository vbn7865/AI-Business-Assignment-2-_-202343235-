import os
import streamlit as st
import pandas as pd
from PIL import Image, ImageOps

# ==========================================
# 1. 페이지 초기 설정 (브라우저 탭 제목 포함)
# ==========================================
st.set_page_config(
    page_title="행운 거북이가 알려주는 K-현대인 찌뿌둥 레벨 테스트",
    page_icon="🍀",
    layout="centered"
)

# ==========================================
# 2. 지마켓산스 웹폰트 & 컬러 팔레트 스타일 적용
# 팔레트: #67B446 / #42822E / #A8E635 / #EBE85A / #F4BD33 / #4E2A14 / #FFFFFF
# ==========================================
st.markdown("""
<style>
/* 지마켓산스 Medium & Bold 웹폰트 불러오기 */
@font-face {
    font-family: 'GmarketSansMedium';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansMedium.woff') format('woff');
    font-weight: 500;
    font-style: normal;
}
@font-face {
    font-family: 'GmarketSansBold';
    src: url('https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_2001@1.1/GmarketSansBold.woff') format('woff');
    font-weight: 700;
    font-style: normal;
}

/* 전체 앱 기본 배경(#FFFFFF) 및 일반 설명문(GmarketSansMedium, #4E2A14) */
.stApp {
    background-color: #FFFFFF;
    color: #4E2A14;
    font-family: 'GmarketSansMedium', sans-serif;
}

p, li, span, div[data-testid="stMarkdownContainer"] {
    font-family: 'GmarketSansMedium', sans-serif !important;
    color: #4E2A14;
    line-height: 1.65;
}

/* 질문, 강조 문구(strong/b), 제목, 버튼은 GmarketSansBold 자동 적용 */
h1, h2, h3, h4,
strong, b,
div[data-testid="stMarkdownContainer"] strong,
div[data-testid="stMarkdownContainer"] b,
div[data-testid="stMetricValue"],
button[data-baseweb="tab"] p,
details summary p {
    font-family: 'GmarketSansBold', sans-serif !important;
    color: #4E2A14;
}

/* 페이지 메인 타이틀 배지 */
.main-subtitle-badge {
    background-color: #67B446;
    color: #FFFFFF !important;
    font-family: 'GmarketSansBold', sans-serif !important;
    text-align: center;
    padding: 10px 18px;
    border-radius: 999px;
    font-size: 1.05rem;
    border: 2px solid #42822E;
    margin: 6px 0 18px 0;
}

/* 상단 인트로 마스코트 카드 */
.intro-card {
    background-color: #F9FDF3;
    border: 2px solid #A8E635;
    border-radius: 16px;
    padding: 16px 20px;
}

/* 탭(Tabs) 포인트 컬러 통일 (#67B446 / #42822E) */
div[data-baseweb="tab-highlight"] {
    background-color: #67B446 !important;
}
button[data-baseweb="tab"][aria-selected="true"] p {
    color: #42822E !important;
}

/* 슬라이더(Slider) 핸들 컬러 통일 (#67B446 / #42822E) */
div[data-testid="stSlider"] div[role="slider"] {
    background-color: #67B446 !important;
    border: 2px solid #42822E !important;
}
div[data-testid="stSliderThumbValue"] {
    font-family: 'GmarketSansBold', sans-serif !important;
    color: #42822E !important;
}

/* 메인 진단 버튼 스타일 (#67B446 기본 / #42822E 호버) */
div[data-testid="stButton"] button {
    background-color: #67B446 !important;
    border: 2px solid #42822E !important;
    border-radius: 14px !important;
    padding: 0.65rem 1.2rem !important;
    transition: all 0.2s ease;
}
div[data-testid="stButton"] button p {
    font-family: 'GmarketSansBold', sans-serif !important;
    color: #FFFFFF !important;
    font-size: 1.1rem !important;
}
div[data-testid="stButton"] button:hover {
    background-color: #42822E !important;
    border-color: #4E2A14 !important;
}
div[data-testid="stButton"] button:hover p {
    color: #EBE85A !important;
}

/* 요약 지표(Metric) 카드 테두리 */
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 2px solid #A8E635;
    border-radius: 14px;
    padding: 12px 16px;
}

/* 스트레칭 개별 루틴 카드 */
.routine-box {
    background-color: #F9FDF3;
    border: 1.5px solid #A8E635;
    border-left: 5px solid #67B446;
    border-radius: 12px;
    padding: 12px 16px;
    margin-bottom: 10px;
}

/* 구분선 색상 */
hr {
    border-color: #EBE85A !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 이미지 로드 및 '앱 행운거북이 5.PNG' 색감 변환 함수
# ==========================================
def resolve_image_path(filename):
    """지정된 파일명을 우선 찾고, 확장자 대소문자 차이까지 안전하게 탐색합니다."""
    if os.path.exists(filename):
        return filename
    target_lower = filename.lower()
    for f in os.listdir("."):
        if f.lower() == target_lower:
            return f
    return None

def recolor_turtle_5(image_path, tone="green"):
    """
    '앱 행운거북이 5.PNG'의 형태와 투명 배경은 그대로 유지하고,
    앱의 지정 컬러 팔레트(#4E2A14, #42822E, #67B446, #A8E635, #EBE85A, #F4BD33)로 색감만 변경합니다.
    """
    img = Image.open(image_path).convert("RGBA")
    r, g, b, alpha = img.split()
    gray = ImageOps.grayscale(Image.merge("RGB", (r, g, b)))
    if tone == "green":
        # 클로버 그린 톤 (외곽선 #4E2A14 / 몸통 #67B446 / 하이라이트 #EBE85A)
        colored = ImageOps.colorize(gray, black="#4E2A14", mid="#67B446", white="#EBE85A")
    else:
        # 햇살 옐로우-그린 톤 (외곽선 #4E2A14 / 몸통 #F4BD33 / 하이라이트 #FFFFFF)
        colored = ImageOps.colorize(gray, black="#4E2A14", mid="#F4BD33", white="#FFFFFF")
    colored.putalpha(alpha)
    return colored

path_title_img = resolve_image_path("앱 폰트.png")
path_turtle_1 = resolve_image_path("앱 행운거북이 1.PNG")
path_turtle_5 = resolve_image_path("앱 행운거북이 5.PNG")

# ==========================================
# 4. 최상단 제목('앱 폰트.png') & 페이지 타이틀 & '앱 행운거북이 1.PNG'
# ==========================================
if path_title_img:
    st.image(path_title_img, use_container_width=True)
else:
    st.title("🍀 행운 거북이가 알려주는 K-현대인 찌뿌둥 레벨 테스트")

# 앱 및 페이지 공식 제목 배너
st.markdown(
    '<div class="main-subtitle-badge">🍀 행운 거북이가 알려주는 K-현대인 찌뿌둥 레벨 테스트</div>',
    unsafe_allow_html=True
)

# '앱 행운거북이 1.PNG' 원본 이미지 그대로 배치한 환영 안내 영역
col_mascot, col_intro = st.columns([1, 3.3], vertical_alignment="center")
with col_mascot:
    if path_turtle_1:
        st.image(path_turtle_1, width=115)

with col_intro:
    st.markdown("""
<div class="intro-card">
    <strong>🍀 네잎클로버 행운 거북이가 찾아왔어요!</strong><br>
    스마트폰과 모니터 앞에서 굳어가는 내 목과 눈, 지금 몇 레벨일까요?
    아래 8가지 문항에 솔직하게 답하고 <strong>나만의 3분 맞춤 스트레칭 루틴</strong>을 처방받아 보세요!
</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# 5. 설문 문항 및 2단 분할 레이아웃 (Tabs & Columns)
# ==========================================
tab1, tab2 = st.tabs(["Step 1. 목·어깨 뻐근함 체크 🐢", "Step 2. 눈 피로·건조함 체크 👀"])

def create_question_row(question_text, options):
    col1, col2 = st.columns([1.05, 1.15], vertical_alignment="center")
    with col1:
        # 질문 문구는 ** 강조를 통해 자동으로 GmarketSansBold 적용
        st.markdown(f"**{question_text}**")
    with col2:
        choice = st.select_slider(
            question_text,
            options=options,
            label_visibility="collapsed",
            key=question_text
        )
    st.divider()
    return options.index(choice) + 1

standard_options = ["전혀 없음 (1점)", "가끔 있음 (2점)", "자주 있음 (3점)"]

with tab1:
    st.subheader("목·어깨 컨디션 체크")
    n1 = create_question_row("하루 평균 PC·스마트폰 사용 시간은?", ["4시간 미만 (1점)", "4~8시간 (2점)", "8시간 이상 (3점)"])
    n2 = create_question_row("스마트폰을 볼 때 고개를 푹 숙이는 빈도는?", ["거의 없음 (1점)", "가끔 숙임 (2점)", "자주 숙임 (3점)"])
    n3 = create_question_row("평소 목과 어깨의 뻐근함 정도는?", standard_options)
    n4 = create_question_row("승모근이 딱딱하게 뭉쳐있는 느낌이 드나요?", ["전혀 없음 (1점)", "가끔 뭉침 (2점)", "항상 뭉침 (3점)"])

with tab2:
    st.subheader("안구 피로도 체크")
    e1 = create_question_row("모니터나 스마트폰을 볼 때 눈이 침침하거나 건조한가요?", ["거의 없음 (1점)", "가끔 느낌 (2점)", "자주 느낌 (3점)"])
    e2 = create_question_row("어두운 곳에서 스마트폰을 사용하는 빈도는?", ["거의 없음 (1점)", "가끔 사용 (2점)", "자주 사용 (3점)"])
    e3 = create_question_row("눈 주변이 묵직하고 피로한 느낌이 드나요?", standard_options)
    e4 = create_question_row("먼 곳을 보다가 가까운 곳을 볼 때 초점 전환이 느린가요?", ["전혀 없음 (1점)", "가끔 느림 (2점)", "자주 느림 (3점)"])

# ==========================================
# 6. 진단 결과 계산 및 시각화 (행운거북이 이미지 다채롭게 활용)
# ==========================================
st.write("")
if st.button("🍀 나의 찌뿌둥 레벨 & 맞춤 스트레칭 확인하기", use_container_width=True):
    neck_score = n1 + n2 + n3 + n4
    eye_score = e1 + e2 + e3 + e4
    total_score = neck_score + eye_score

    st.markdown("---")
    st.header("📊 행운 거북이의 찌뿌둥 레벨 판독 결과")

    # 단계별 컬러 배너 설정 (#67B446 / #F4BD33 / #4E2A14)
    if total_score <= 12:
        level = 1
        bg_color = "#F2FBE9"
        border_color = "#67B446"
        title_color = "#42822E"
        result_title = "🟢 Lv.1 양호 : 바른 자세의 인간 거북이 탈출러"
        result_desc = "목과 눈 모두 컨디션이 아주 양호한 상태예요! 지금처럼 바른 자세와 휴식 습관을 꾸준히 유지해 주세요."
    elif total_score <= 18:
        level = 2
        bg_color = "#FEFBE8"
        border_color = "#F4BD33"
        title_color = "#4E2A14"
        result_title = "🟡 Lv.2 주의 : 슬금슬금 목 내미는 예비 거북이"
        result_desc = "거북목과 안구 피로가 서서히 누적되고 있어요! 화면에서 고개를 살짝 뒤로 당기고 지금 바로 스트레칭이 필요합니다."
    else:
        level = 3
        bg_color = "#FFF6EC"
        border_color = "#4E2A14"
        title_color = "#4E2A14"
        result_title = "🔴 Lv.3 위험 : 모니터 속으로 빨려 들어가는 만성 피로 거북왕"
        result_desc = "목·어깨 경직과 눈의 피로가 한계치에 도달했습니다! 지금 당장 기기를 내려놓고 집중 케어 루틴을 따라 해보세요."

    # 결과 배너 옆에 '앱 행운거북이 1.PNG' (원본) 배치
    res_col1, res_col2 = st.columns([1, 3.6], vertical_alignment="center")
    with res_col1:
        if path_turtle_1:
            st.image(path_turtle_1, width=105)
    with res_col2:
        st.markdown(f"""
<div style="background-color:{bg_color}; border:2px solid {border_color}; border-left:8px solid {border_color}; padding:16px 20px; border-radius:14px;">
    <h3 style="margin:0 0 6px 0; color:{title_color};">{result_title}</h3>
    <p style="margin:0;">{result_desc}</p>
</div>
""", unsafe_allow_html=True)

    st.write("")

    # 핵심 수치 요약 (st.metric)
    st.subheader("부위별 피로 점수 요약")
    m1, m2, m3 = st.columns(3)
    m1.metric(label="총점 (24점 만점)", value=f"{total_score}점")
    m2.metric(label="목·어깨 피로도 (12점)", value=f"{neck_score}점")
    m3.metric(label="눈 피로도 (12점)", value=f"{eye_score}점")

    st.write("")

    # 부위별 비교 막대그래프 (#67B446 클로버 그린 적용)
    st.subheader("어느 부위가 더 찌뿌둥할까?")
    chart_data = pd.DataFrame(
        {"피로 점수": [neck_score, eye_score]},
        index=["목·어깨", "눈"]
    )
    st.bar_chart(chart_data, color="#67B446")

    # ==========================================
    # 7. 맞춤형 스트레칭 가이드 (색감 변경된 '앱 행운거북이 5.PNG' & '앱 행운거북이 1.PNG' 활용)
    # ==========================================
    with st.expander("🧘‍♀️ 거북이 코치와 함께하는 3분 초간단 스트레칭 루틴", expanded=True):
        # 스트레칭 코치 소개 영역: 클로버 그린으로 색감 변경한 '앱 행운거북이 5.PNG' 배치
        coach_col1, coach_col2 = st.columns([1, 4], vertical_alignment="center")
        with coach_col1:
            if path_turtle_5:
                turtle_5_green = recolor_turtle_5(path_turtle_5, tone="green")
                st.image(turtle_5_green, width=90)
        with coach_col2:
            st.markdown("""
<div style="background-color:#FEFBE8; border:1.5px solid #F4BD33; border-radius:12px; padding:12px 16px;">
    <strong>🐢 스트레칭 코치 거북이의 한마디</strong><br>
    의자에 앉은 채로 딱 3분만 투자해 보세요! 뻣뻣했던 목과 뻑뻑한 눈이 한결 가벼워집니다.
</div>
""", unsafe_allow_html=True)

        st.write("")

        if level == 1:
            neck_tip = "좌우로 천천히 고개를 5회씩 돌려주며 가볍게 목의 긴장을 풀어줍니다."
            shoulder_tip = "어깨를 귀 쪽으로 으쓱 올렸다가 툭 떨어뜨리는 동작을 10회 반복합니다."
            eye_tip = "눈을 감고 시계 방향으로 크게 5바퀴, 반시계 방향으로 5바퀴 굴려줍니다."
        elif level == 2:
            neck_tip = "오른손으로 왼쪽 귀 윗부분을 잡고 오른쪽으로 지그시 15초간 당겨줍니다. (반대쪽도 동일하게 진행)"
            shoulder_tip = "양손을 등 뒤로 깍지 끼고 가슴을 활짝 펴면서 팔을 위로 살짝 들어 올린 채 15초 유지합니다."
            eye_tip = "양손바닥을 10초간 빠르게 비벼 따뜻하게 만든 뒤, 감은 눈 위에 살포시 올려 찜질해 줍니다."
        else:
            neck_tip = "양손 깍지를 끼고 뒤통수에 댄 후, 턱이 쇄골에 닿을 만큼 지그시 눌러 뒷목을 깊게 20초간 스트레칭합니다."
            shoulder_tip = "W자 형태로 팔을 벌리고, 날개뼈(견갑골)가 서로 맞닿는다는 느낌으로 등 근육을 꽉 조여 10초간 유지합니다. (3회 반복)"
            eye_tip = "엄지손가락으로 눈썹 뼈 안쪽(눈 앞머리 위쪽)을 지그시 꾹꾹 눌러주며 눈 주변의 뭉친 혈을 풀어줍니다. 스마트폰은 10분간 엎어두세요!"

        # [1분 목 & 어깨 루틴] 카드 + 클로버 그린 톤 '앱 행운거북이 5.PNG'
        r1_col1, r1_col2 = st.columns([4.2, 1], vertical_alignment="center")
        with r1_col1:
            st.markdown(f"""
<div class="routine-box">
    <strong>⏱️ [1분 목 이완 루틴]</strong><br>{neck_tip}
</div>
<div class="routine-box">
    <strong>⏱️ [1분 어깨 회전 루틴]</strong><br>{shoulder_tip}
</div>
""", unsafe_allow_html=True)
        with r1_col2:
            if path_turtle_5:
                turtle_5_yellow = recolor_turtle_5(path_turtle_5, tone="yellow")
                st.image(turtle_5_yellow, width=85)

        # [1분 안구 휴식 루틴] & 마지막 행운 응원 배너 ('앱 행운거북이 1.PNG' 원본 활용)
        r2_col1, r2_col2 = st.columns([1, 4.2], vertical_alignment="center")
        with r2_col1:
            if path_turtle_1:
                st.image(path_turtle_1, width=85)
        with r2_col2:
            st.markdown(f"""
<div class="routine-box" style="border-left-color:#F4BD33; background-color:#FEFBE8;">
    <strong>⏱️ [1분 안구 휴식 & 행운 거북이의 응원]</strong><br>{eye_tip}<br>
    <strong>🍀 오늘도 바른 자세로 행운 가득한 하루 보내세요!</strong>
</div>
""", unsafe_allow_html=True)
