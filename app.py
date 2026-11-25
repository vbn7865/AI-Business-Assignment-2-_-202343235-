import os
import base64
from io import BytesIO
import streamlit as st
from PIL import Image, ImageEnhance

# ==========================================
# 1. 페이지 기본 설정
# ==========================================
st.set_page_config(
    page_title="행운 거북이가 알려주는 K-현대인 찌뿌둥 레벨 테스트",
    page_icon="🍀",
    layout="centered"
)

# ==========================================
# 비밀번호 잠금 기능 (에러 방지 안전 버전)
# ==========================================
def check_password():
    if st.session_state.get("password_correct", False):
        return True

    st.markdown("### 🔒 접근 제한")
    st.write("비밀번호를 입력하면 **행운 거북이 찌뿌둥 레벨 테스트**를 시작할 수 있습니다.")
    pwd = st.text_input("비밀번호를 입력하세요", type="password")

    if st.button("확인"):
        try:
            correct_pw = st.secrets["APP_PASSWORD"]
        except Exception:
            correct_pw = "pnumis"

        if pwd == correct_pw:
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("비밀번호가 틀렸습니다. 다시 확인해 주세요.")
    return False

if not check_password():
    st.stop()

# 설문 화면('survey') <-> 결과 화면('result') 전환용 상태 관리 (수정사항 4)
if "view_mode" not in st.session_state:
    st.session_state.view_mode = "survey"
if "neck_score" not in st.session_state:
    st.session_state.neck_score = 4
if "eye_score" not in st.session_state:
    st.session_state.eye_score = 4

# ==========================================
# 2. 지마켓산스 웹폰트 & 지정 컬러 팔레트 CSS 스타일
# 팔레트: #67B446 / #42822E / #A8E635 / #EBE85A / #F4BD33 / #4E2A14 / #FFFFFF
# ==========================================
st.markdown("""
<style>
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

/* 전체 배경 및 일반 설명문 (GmarketSansMedium) */
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

/* 질문, 버튼, 제목, 강조 문구는 GmarketSansBold 자동 구분 */
h1, h2, h3, h4,
strong, b,
div[data-testid="stMarkdownContainer"] strong,
div[data-testid="stMarkdownContainer"] b,
div[data-testid="stMetricValue"] {
    font-family: 'GmarketSansBold', sans-serif !important;
    color: #4E2A14;
}

/* 수정사항 2: 행운 거북이가 말하는 듯한 말풍선 UI */
.intro-wrap {
    display: flex;
    align-items: center;
    gap: 18px;
    margin: 14px 0 26px 0;
}
.intro-mascot {
    flex-shrink: 0;
    width: 105px;
    text-align: center;
}
.intro-mascot img {
    width: 100px;
    height: auto;
    display: block;
    margin: 0 auto;
}
.speech-bubble {
    position: relative;
    background-color: #F9FDF3;
    border: 2.5px solid #A8E635;
    border-radius: 18px;
    padding: 18px 22px;
    flex: 1;
    box-shadow: 0 3px 10px rgba(103, 180, 70, 0.08);
}
/* 말풍선 왼쪽 꼬리 (테두리 + 내부 채움) */
.speech-bubble::before {
    content: '';
    position: absolute;
    left: -14px;
    top: 50%;
    transform: translateY(-50%);
    border-width: 11px 14px 11px 0;
    border-style: solid;
    border-color: transparent #A8E635 transparent transparent;
}
.speech-bubble::after {
    content: '';
    position: absolute;
    left: -10px;
    top: 50%;
    transform: translateY(-50%);
    border-width: 9px 12px 9px 0;
    border-style: solid;
    border-color: transparent #F9FDF3 transparent transparent;
}
.speech-title {
    font-family: 'GmarketSansBold', sans-serif !important;
    font-size: 1.08rem;
    color: #42822E;
    margin-bottom: 8px;
}
.speech-body {
    font-family: 'GmarketSansMedium', sans-serif !important;
    font-size: 0.97rem;
    color: #4E2A14;
    line-height: 1.75;
}

/* 수정사항 3: 원페이지 연속 설문용 Step 헤더 배지 */
.step-header {
    background-color: #F4FBE8;
    border-left: 6px solid #67B446;
    border-radius: 10px;
    padding: 12px 18px;
    margin: 24px 0 16px 0;
    font-family: 'GmarketSansBold', sans-serif !important;
    font-size: 1.15rem;
    color: #42822E;
}

/* 슬라이더 포인트 컬러 통일 */
div[data-testid="stSlider"] div[role="slider"] {
    background-color: #67B446 !important;
    border: 2px solid #42822E !important;
}
div[data-testid="stSliderThumbValue"] {
    font-family: 'GmarketSansBold', sans-serif !important;
    color: #42822E !important;
}

/* 버튼 스타일 (#67B446 기본 / #42822E 호버) */
div[data-testid="stButton"] button {
    background-color: #67B446 !important;
    border: 2px solid #42822E !important;
    border-radius: 14px !important;
    padding: 0.7rem 1.2rem !important;
    transition: all 0.2s ease;
}
div[data-testid="stButton"] button p {
    font-family: 'GmarketSansBold', sans-serif !important;
    color: #FFFFFF !important;
    font-size: 1.08rem !important;
}
div[data-testid="stButton"] button:hover {
    background-color: #42822E !important;
    border-color: #4E2A14 !important;
}
div[data-testid="stButton"] button:hover p {
    color: #EBE85A !important;
}

/* 요약 지표(Metric) 카드 */
div[data-testid="stMetric"] {
    background-color: #FFFFFF;
    border: 2px solid #A8E635;
    border-radius: 14px;
    padding: 12px 16px;
}

/* 수정사항 6 & 7: 글자 겹침 없는 스트레칭 섹션 헤더 & 가로 3단 카드 */
.section-title-box {
    background-color: #42822E;
    color: #FFFFFF !important;
    font-family: 'GmarketSansBold', sans-serif !important;
    font-size: 1.15rem;
    padding: 12px 20px;
    border-radius: 12px;
    margin: 26px 0 14px 0;
}

.banner-flex {
    display: flex;
    align-items: center;
    gap: 16px;
    background-color: #FEFBE8;
    border: 2px solid #F4BD33;
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 16px;
}
.banner-flex.green-theme {
    background-color: #F9FDF3;
    border: 2px solid #A8E635;
    margin-top: 16px;
    margin-bottom: 10px;
}
.banner-flex img {
    width: 68px;
    height: auto;
    flex-shrink: 0;
}

.step-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 14px 0;
}
.step-card {
    background-color: #F9FDF3;
    border: 2px solid #A8E635;
    border-top: 6px solid #67B446;
    border-radius: 14px;
    padding: 16px 14px;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
}
.step-badge {
    display: inline-block;
    background-color: #EBE85A;
    color: #4E2A14;
    font-family: 'GmarketSansBold', sans-serif !important;
    font-size: 0.85rem;
    padding: 4px 10px;
    border-radius: 999px;
    margin: 0 auto 8px auto;
}
.step-card-title {
    font-family: 'GmarketSansBold', sans-serif !important;
    font-size: 1.02rem;
    color: #42822E;
    margin-bottom: 10px;
}
.step-card-desc {
    font-family: 'GmarketSansMedium', sans-serif !important;
    font-size: 0.92rem;
    color: #4E2A14;
    line-height: 1.55;
    word-break: keep-all;
}

/* 모바일 화면 대응 */
@media (max-width: 640px) {
    .intro-wrap {
        flex-direction: column;
        text-align: center;
    }
    .speech-bubble::before, .speech-bubble::after {
        display: none;
    }
    .step-grid {
        grid-template-columns: 1fr;
    }
}

hr {
    border-color: #EBE85A !important;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 이미지 탐색 및 선명도 향상·180도 회전 처리 함수
# ==========================================
def resolve_image_path(candidates):
    """파일명 및 확장자 대소문자 차이를 모두 안전하게 탐색합니다."""
    if isinstance(candidates, str):
        candidates = [candidates]
    files_in_dir = os.listdir(".")
    for cand in candidates:
        if os.path.exists(cand):
            return cand
        cand_lower = cand.lower()
        for f in files_in_dir:
            if f.lower() == cand_lower:
                return f
    return None

def clean_white_background(img, threshold=244):
    """이미지 외곽의 불투명한 흰색 배경이 네모나게 뜨지 않도록 깔끔하게 투명화합니다."""
    img = img.convert("RGBA")
    datas = img.getdata()
    new_data = []
    for r, g, b, a in datas:
        if a > 0 and r >= threshold and g >= threshold and b >= threshold:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    # 투명 여백 자동 크롭으로 크기 균일화
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img

@st.cache_data
def get_image_base64(path, rotate_180=False, sharpen=False, clean_bg=True):
    """
    PIL 이미지를 처리(배경 정리, 180도 회전, 선명도 대폭 향상)한 뒤
    HTML 카드 내부에 깨짐 없이 삽입할 수 있도록 Base64 문자열로 변환합니다.
    """
    if not path:
        return None
    img = Image.open(path).convert("RGBA")
    if clean_bg:
        img = clean_white_background(img)
    if rotate_180:
        img = img.rotate(180, expand=True)
    if sharpen:
        # RGB 채널만 분리하여 선명도와 대비를 깔끔하게 강화 (투명 테두리 보존)
        r, g, b, a = img.split()
        rgb = Image.merge("RGB", (r, g, b))
        rgb = ImageEnhance.Contrast(rgb).enhance(1.12)
        rgb = ImageEnhance.Sharpness(rgb).enhance(2.2)
        r2, g2, b2 = rgb.split()
        img = Image.merge("RGBA", (r2, g2, b2, a))

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

# GitHub 저장소 이미지 경로 연결
path_title_banner = resolve_image_path(["앱 폰트 이미지.PNG", "앱 폰트 이미지.png", "앱 폰트 수정본.png"])
path_turtle_1 = resolve_image_path(["앱 행운거북이 1.PNG", "앱 행운거북이 1.png"])
path_turtle_green = resolve_image_path(["앱 행운거북이 초록.png", "앱 행운거북이 초록.PNG"])
path_turtle_yellow = resolve_image_path(["앱 행운거북이 노랑.png", "앱 행운거북이 노랑.PNG"])

# Base64 이미지 준비
b64_turtle_1 = get_image_base64(path_turtle_1, rotate_180=False, sharpen=False, clean_bg=True)
# 추가 요청사항: 초록/노랑 거북이는 180도 회전 + 선명도 향상 적용
b64_turtle_green = get_image_base64(path_turtle_green, rotate_180=True, sharpen=True, clean_bg=True)
b64_turtle_yellow = get_image_base64(path_turtle_yellow, rotate_180=True, sharpen=True, clean_bg=True)

# ==========================================
# 4. 최상단 고정 헤더 영역 ('앱 폰트 이미지.PNG' - 설문/결과 공통 유지)
# ==========================================
if path_title_banner:
    st.image(path_title_banner, use_container_width=True)
else:
    st.title("🍀 행운 거북이가 알려주는 K-현대인 찌뿌둥 레벨 테스트")

# ==========================================
# 5-A. [설문조사 화면] (수정사항 2, 3, 4 반영)
# ==========================================
def create_question_row(question_text, options, key_id):
    col1, col2 = st.columns([1.08, 1.12], vertical_alignment="center")
    with col1:
        st.markdown(f"**{question_text}**")
    with col2:
        choice = st.select_slider(
            question_text,
            options=options,
            label_visibility="collapsed",
            key=key_id
        )
    st.divider()
    return options.index(choice) + 1

if st.session_state.view_mode == "survey":
    # 수정사항 2: 거북이 말풍선 + 문장마다 명확한 줄 나눔
    mascot_img_html = f'<img src="data:image/png;base64,{b64_turtle_1}" alt="행운 거북이">' if b64_turtle_1 else "🍀"
    st.markdown(f"""
<div class="intro-wrap">
    <div class="intro-mascot">{mascot_img_html}</div>
    <div class="speech-bubble">
        <div class="speech-title">🍀 네잎클로버 행운 거북이가 찾아왔어요!</div>
        <div class="speech-body">
            스마트폰과 모니터 앞에서 굳어가는 내 목과 눈, 지금 몇 레벨일까요?<br>
            아래 8가지 문항에 솔직하게 답하고 나만의 3분 맞춤 스트레칭 루틴을 처방받아 보세요!
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    standard_options = ["전혀 없음 (1점)", "가끔 있음 (2점)", "자주 있음 (3점)"]

    # 수정사항 3: 탭 분리 없이 Step 1과 Step 2가 한 페이지에 쭉 이어지는 설문 구조
    st.markdown('<div class="step-header">🐢 Step 1. 목·어깨 뻐근함 체크</div>', unsafe_allow_html=True)
    n1 = create_question_row("1. 하루 평균 PC·스마트폰 사용 시간은?", ["4시간 미만 (1점)", "4~8시간 (2점)", "8시간 이상 (3점)"], "q_n1")
    n2 = create_question_row("2. 스마트폰을 볼 때 고개를 푹 숙이는 빈도는?", ["거의 없음 (1점)", "가끔 숙임 (2점)", "자주 숙임 (3점)"], "q_n2")
    n3 = create_question_row("3. 평소 목과 어깨의 뻐근함 정도는?", standard_options, "q_n3")
    n4 = create_question_row("4. 승모근이 딱딱하게 뭉쳐있는 느낌이 드나요?", ["전혀 없음 (1점)", "가끔 뭉침 (2점)", "항상 뭉침 (3점)"], "q_n4")

    st.markdown('<div class="step-header">👀 Step 2. 눈 피로·건조함 체크</div>', unsafe_allow_html=True)
    e1 = create_question_row("5. 모니터나 스마트폰을 볼 때 눈이 침침하거나 건조한가요?", ["거의 없음 (1점)", "가끔 느낌 (2점)", "자주 느낌 (3점)"], "q_e1")
    e2 = create_question_row("6. 어두운 곳에서 스마트폰을 사용하는 빈도는?", ["거의 없음 (1점)", "가끔 사용 (2점)", "자주 사용 (3점)"], "q_e2")
    e3 = create_question_row("7. 눈 주변이 묵직하고 피로한 느낌이 드나요?", standard_options, "q_e3")
    e4 = create_question_row("8. 먼 곳을 보다가 가까운 곳을 볼 때 초점 전환이 느린가요?", ["전혀 없음 (1점)", "가끔 느림 (2점)", "자주 느림 (3점)"], "q_e4")

    st.write("")
    # 수정사항 4: 버튼 클릭 시 설문 화면을 닫고 결과 화면으로 전환
    if st.button("🍀 나의 찌뿌둥 레벨 & 맞춤 스트레칭 확인하기", use_container_width=True):
        st.session_state.neck_score = n1 + n2 + n3 + n4
        st.session_state.eye_score = e1 + e2 + e3 + e4
        st.session_state.view_mode = "result"
        st.rerun()

# ==========================================
# 5-B. [진단 결과 및 맞춤 스트레칭 화면] (수정사항 4, 5, 6, 7, 8 반영)
# ==========================================
else:
    neck_score = st.session_state.neck_score
    eye_score = st.session_state.eye_score
    total_score = neck_score + eye_score

    st.write("")
    st.subheader("📊 행운 거북이의 찌뿌둥 레벨 판독 결과")

    # 레벨별 결과 판독 및 색상·거북이 매칭 (수정사항 8: 같은 디자인·다른 색상 거북이 활용)
    if total_score <= 12:
        level = 1
        bg_color = "#F2FBE9"
        border_color = "#67B446"
        title_color = "#42822E"
        result_title = "🟢 Lv.1 양호 : 바른 자세의 인간 거북이 탈출러"
        result_desc = "목과 눈 모두 컨디션이 아주 양호한 상태예요!<br>지금처럼 바른 자세와 휴식 습관을 꾸준히 유지해 주세요."
        result_turtle_b64 = b64_turtle_green
        coach_turtle_b64 = b64_turtle_yellow
    elif total_score <= 18:
        level = 2
        bg_color = "#FEFBE8"
        border_color = "#F4BD33"
        title_color = "#4E2A14"
        result_title = "🟡 Lv.2 주의 : 슬금슬금 목 내미는 예비 거북이"
        result_desc = "거북목과 안구 피로가 서서히 누적되고 있어요!<br>화면에서 고개를 살짝 뒤로 당기고 지금 바로 스트레칭이 필요합니다."
        result_turtle_b64 = b64_turtle_yellow
        coach_turtle_b64 = b64_turtle_green
    else:
        level = 3
        bg_color = "#FFF6EC"
        border_color = "#4E2A14"
        title_color = "#4E2A14"
        result_title = "🔴 Lv.3 위험 : 모니터 속으로 빨려 들어가는 만성 피로 거북왕"
        result_desc = "목·어깨 경직과 눈의 피로가 한계치에 도달했습니다!<br>지금 당장 기기를 내려놓고 아래 3분 집중 케어 루틴을 따라 해보세요."
        result_turtle_b64 = b64_turtle_yellow
        coach_turtle_b64 = b64_turtle_green

    res_turtle_html = (
        f'<img src="data:image/png;base64,{result_turtle_b64}" style="width:76px; height:auto; flex-shrink:0;" alt="결과 거북이">'
        if result_turtle_b64 else "🐢"
    )

    st.markdown(f"""
<div style="display:flex; align-items:center; gap:18px; background-color:{bg_color}; border:2px solid {border_color}; border-left:8px solid {border_color}; padding:18px 22px; border-radius:16px; margin-bottom:18px;">
    {res_turtle_html}
    <div>
        <div style="font-family:'GmarketSansBold',sans-serif; font-size:1.18rem; color:{title_color}; margin-bottom:6px;">{result_title}</div>
        <div style="font-family:'GmarketSansMedium',sans-serif; font-size:0.96rem; color:#4E2A14; line-height:1.6;">{result_desc}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    # 부위별 피로 점수 요약 지표 (수정사항 5에 따라 아래 막대그래프는 완전 삭제)
    m1, m2, m3 = st.columns(3)
    m1.metric(label="총점 (24점 만점)", value=f"{total_score}점")
    m2.metric(label="목·어깨 피로도 (12점)", value=f"{neck_score}점")
    m3.metric(label="눈 피로도 (12점)", value=f"{eye_score}점")

    # ==========================================
    # 수정사항 6, 7, 8 + 추가 요청사항:
    # 텍스트 겹침 없는 헤더 + 180도 회전·선명화 거북이 코치 + 가로 3단 STEP 카드
    # ==========================================
    st.markdown(
        '<div class="section-title-box">🧘‍♀️ 거북이 코치와 함께하는 초간단 3분 스트레칭 루틴</div>',
        unsafe_allow_html=True
    )

    # 레벨별 맞춤 3단계 스트레칭 문구 설정
    if level == 1:
        step1_desc = "고개를 좌우로 천천히<br><strong>5회씩 회전</strong>하며<br>목의 긴장을 가볍게 풀기"
        step2_desc = "어깨를 귀 쪽으로 으쓱 올린 뒤<br><strong>툭 떨구는 동작을</strong><br><strong>10회 반복</strong>하기"
        step3_desc = "눈을 감고 시계·반시계 방향으로<br><strong>각각 5바퀴씩</strong><br>천천히 굴려주기"
    elif level == 2:
        step1_desc = "한 손으로 반대쪽 머리를 잡고<br>옆으로 지그시 당겨<br><strong>좌우 15초씩 유지</strong>하기"
        step2_desc = "등 뒤로 양손 깍지를 끼고<br>가슴을 활짝 편 채로<br><strong>15초간 쭉 펴주기</strong>"
        step3_desc = "양손바닥을 비벼 따뜻하게 한 뒤<br>감은 눈 위에 올려<br><strong>20초간 온찜질</strong>하기"
    else:
        step1_desc = "뒤통수에 깍지를 끼고 턱을 당겨<br>뻣뻣한 뒷목 근육을<br><strong>20초간 깊게 늘리기</strong>"
        step2_desc = "양팔을 W자로 벌려 날개뼈를<br>모아 등 근육을 조인 채<br><strong>10초 유지 × 3회 반복</strong>"
        step3_desc = "눈썹 뼈 안쪽을 지그시 누르며<br>뭉친 혈을 풀어주고<br><strong>10분간 화면 멀리하기</strong>"

    # 상단 코치 한마디 배너 (180도 회전 + 선명도 향상된 초록/노랑 거북이 활용)
    # 코치 배너에는 초록·노랑 거북이를 함께 보여주어 통일감과 귀여움을 극대화
    coach_imgs_html = ""
    if b64_turtle_green:
        coach_imgs_html += f'<img src="data:image/png;base64,{b64_turtle_green}" alt="초록 거북이 코치">'
    if b64_turtle_yellow:
        coach_imgs_html += f'<img src="data:image/png;base64,{b64_turtle_yellow}" alt="노랑 거북이 코치">'

    st.markdown(f"""
<div class="banner-flex">
    <div style="display:flex; gap:6px; align-items:center; flex-shrink:0;">
        {coach_imgs_html}
    </div>
    <div>
        <strong style="color:#42822E; font-size:1.03rem;">🐢 코치 한마디 : 의자에 앉아서 딱 3분만 따라 해보세요!</strong><br>
        <span style="font-size:0.94rem;">뻣뻣하게 굳어있던 목·어깨와 뻑뻑한 눈이 한결 가벼워집니다.</span>
    </div>
</div>

<div class="step-grid">
    <div class="step-card">
        <div class="step-badge">⏱️ STEP 1 (1분)</div>
        <div class="step-card-title">[ 목 이완하기 ]</div>
        <div class="step-card-desc">{step1_desc}</div>
    </div>
    <div class="step-card">
        <div class="step-badge">⏱️ STEP 2 (1분)</div>
        <div class="step-card-title">[ 어깨 펴주기 ]</div>
        <div class="step-card-desc">{step2_desc}</div>
    </div>
    <div class="step-card">
        <div class="step-badge">⏱️ STEP 3 (1분)</div>
        <div class="step-card-title">[ 눈 휴식하기 ]</div>
        <div class="step-card-desc">{step3_desc}</div>
    </div>
</div>
""", unsafe_allow_html=True)

    # 하단 행운 거북이 응원 배너 ('앱 행운거북이 1.PNG' 활용)
    cheer_img_html = f'<img src="data:image/png;base64,{b64_turtle_1}" alt="행운 거북이">' if b64_turtle_1 else "🍀"
    st.markdown(f"""
<div class="banner-flex green-theme">
    {cheer_img_html}
    <div>
        <strong style="color:#42822E; font-size:1.04rem;">🍀 오늘도 바른 자세로 행운 가득한 하루 보내세요!</strong><br>
        <span style="font-size:0.93rem;">1시간마다 한 번씩 기지개를 켜면 거북목 예방 효과가 2배로 올라갑니다.</span>
    </div>
</div>
""", unsafe_allow_html=True)

    st.write("")
    if st.button("🔄 처음부터 다시 테스트하기", use_container_width=True):
        st.session_state.view_mode = "survey"
        st.rerun()
