import streamlit as st
import pandas as pd

# ==========================================
# 1. 페이지 초기 설정 및 UI 테마 적용
# ==========================================
st.set_page_config(page_title="거북목·눈 피로 자가진단", page_icon="🐢", layout="centered")

# 눈이 편안한 세이지 그린 계열 포인트 컬러 CSS 적용 (더 안정적인 방식 적용)
st.markdown("""
    <style>
    div[data-testid="stButton"] button {
        background-color: #9CA986 !important; 
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    div[data-testid="stButton"] button:hover {
        background-color: #829070 !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 메인 타이틀
st.title("🐢 거북목·눈 피로 자가진단 및 스트레칭 추천기")
st.markdown("현대인들의 고질적인 신체 문제인 **목·어깨 뭉침**과 **눈 피로도**를 간단히 점검하고 맞춤형 스트레칭 루틴을 처방받아 보세요!")
st.divider()

# ==========================================
# 2. 설문 문항 및 레이아웃 구성 (Tabs & Columns)
# ==========================================
# 사용자 응답 진행을 영역별로 나누기 위해 탭(Tabs) 사용
tab1, tab2 = st.tabs(["Step 1. 목·어깨 집중 체크 💆‍♂️", "Step 2. 눈 피로 집중 체크 👁️"])

# 질문과 슬라이더를 2단으로 배치하는 헬퍼 함수
def create_question_row(question_text, options):
    col1, col2 = st.columns([1, 1.2]) # 좌측은 질문, 우측은 슬라이더 배치
    with col1:
        st.markdown(f"**{question_text}**")
    with col2:
        # 오류 방지를 위해 명시적인 key 값(question_text) 부여
        choice = st.select_slider(
            question_text, 
            options=options, 
            label_visibility="collapsed",
            key=question_text 
        )
    st.divider() # 문항 간 가로 구분선
    # 선택한 옵션의 인덱스 + 1을 점수로 반환 (1점 ~ 3점)
    return options.index(choice) + 1 

# 일반적인 3점 척도 라벨
standard_options = ["전혀 없음 (1점)", "가끔 있음 (2점)", "자주 있음 (3점)"]

# --- [Tab 1] 목·어깨 피로도 문항 ---
with tab1:
    st.subheader("목·어깨 컨디션 체크")
    n1 = create_question_row("하루 평균 PC·스마트폰 사용 시간은?", ["4시간 미만 (1점)", "4~8시간 (2점)", "8시간 이상 (3점)"])
    n2 = create_question_row("스마트폰을 볼 때 고개를 푹 숙이는 빈도는?", ["거의 없음 (1점)", "가끔 숙임 (2점)", "자주 숙임 (3점)"])
    n3 = create_question_row("평소 목과 어깨의 뻐근함 정도는?", standard_options)
    n4 = create_question_row("승모근이 딱딱하게 뭉쳐있는 느낌이 드나요?", ["전혀 없음 (1점)", "가끔 뭉침 (2점)", "항상 뭉침 (3점)"])

# --- [Tab 2] 눈 피로도 문항 ---
with tab2:
    st.subheader("안구 피로도 체크")
    e1 = create_question_row("모니터나 스마트폰을 볼 때 눈이 침침하거나 건조한가요?", ["거의 없음 (1점)", "가끔 느낌 (2점)", "자주 느낌 (3점)"])
    e2 = create_question_row("어두운 곳에서 스마트폰을 사용하는 빈도는?", ["거의 없음 (1점)", "가끔 사용 (2점)", "자주 사용 (3점)"])
    e3 = create_question_row("눈 주변이 묵직하고 피로한 느낌이 드나요?", standard_options)
    e4 = create_question_row("먼 곳을 보다가 가까운 곳을 볼 때 초점 전환이 느린가요?", ["전혀 없음 (1점)", "가끔 느림 (2점)", "자주 느림 (3점)"])

# ==========================================
# 3. 진단 결과 계산 및 시각화 (Metrics & Chart)
# ==========================================
st.write("") # 여백
# 버튼 전체 너비 사용(use_container_width) 적용
if st.button("🔍 진단 결과 확인하기", use_container_width=True):
    # 점수 합산
    neck_score = n1 + n2 + n3 + n4
    eye_score = e1 + e2 + e3 + e4
    total_score = neck_score + eye_score
    
    st.markdown("---")
    st.header("📊 나의 피로도 진단 결과")
    
    # 3단계 진단 결과 판별 및 신호등 배너 출력
    if total_score <= 12:
        st.success("### 🟢 양호 : 바른 자세의 인간 거북이 탈출러\n목과 눈 모두 컨디션이 양호한 상태! 현재의 바른 생활 습관을 꾸준히 유지하면 되는 건강 관리 모범생입니다.")
        level = 1
    elif total_score <= 18:
        st.warning("### 🟡 주의 : 슬금슬금 목 내미는 예비 거북이\n거북목과 안구 피로가 서서히 누적되는 경고 단계! 틈틈이 자세를 고쳐 앉고 스트레칭이 시급한 상태입니다.")
        level = 2
    else:
        st.error("### 🔴 위험 : 모니터 속으로 빨려 들어가는 만성 피로 거북왕\n목·어깨 경직과 눈의 피로가 한계치에 도달한 상태! 즉각적인 휴식과 집중 스트레칭 케어가 필수인 상태입니다.")
        level = 3

    # 핵심 수치 요약 (st.metric)
    st.write("#### 요약 지표")
    m1, m2, m3 = st.columns(3)
    m1.metric(label="총점 (24점 만점)", value=f"{total_score}점")
    m2.metric(label="목·어깨 피로도 (12점 만점)", value=f"{neck_score}점")
    m3.metric(label="눈 피로도 (12점 만점)", value=f"{eye_score}점")
    
    # 부위별 비교를 위한 막대그래프 (디자인 테마에 맞춰 컬러 지정)
    st.write("#### 부위별 피로도 비교")
    chart_data = pd.DataFrame(
        {"피로 점수": [neck_score, eye_score]},
        index=["목·어깨", "눈"]
    )
    st.bar_chart(chart_data, color="#9CA986")

    # ==========================================
    # 4. 단계별 맞춤형 스트레칭 가이드 (Expander)
    # ==========================================
    with st.expander("🧘‍♀️ 나를 위한 3분 초간단 스트레칭 & 눈 휴식 루틴 펼쳐보기", expanded=True):
        st.markdown("자리에서 바로 따라 할 수 있는 3분 루틴입니다. 지금 바로 시작해 보세요!")
        
        if level == 1:
            st.markdown("""
            - **[1분 목 이완]**: 좌우로 천천히 고개를 5회씩 돌려주며 가볍게 목의 긴장을 풀어줍니다.
            - **[1분 어깨 회전]**: 어깨를 귀 쪽으로 으쓱 올렸다가 툭 떨어뜨리는 동작을 10회 반복합니다.
            - **[1분 안구 휴식]**: 눈을 감고 시계 방향으로 크게 5바퀴, 반시계 방향으로 5바퀴 굴려줍니다.
            """)
        elif level == 2:
            st.markdown("""
            - **[1분 목 이완]**: 오른손으로 왼쪽 귀 윗부분을 잡고 오른쪽으로 지그시 15초간 당겨줍니다. (반대쪽도 동일하게 진행)
            - **[1분 어깨 회전]**: 양손을 등 뒤로 깍지 끼고 가슴을 활짝 펴면서 팔을 위로 살짝 들어 올린 채 15초 유지합니다.
            - **[1분 안구 휴식]**: 양손바닥을 10초간 빠르게 비벼 따뜻하게 만든 뒤, 감은 눈 위에 살포시 올려 찜질해 줍니다.
            """)
        else: # level == 3
            st.markdown("""
            - **[1분 목 이완]**: 양손 깍지를 끼고 뒤통수에 댄 후, 턱이 쇄골에 닿을 만큼 지그시 눌러 뒷목을 깊게 20초간 스트레칭합니다.
            - **[1분 어깨 회전]**: W자 형태로 팔을 벌리고, 날개뼈(견갑골)가 서로 맞닿는다는 느낌으로 등 근육을 꽉 조여 10초간 유지합니다. (3회 반복)
            - **[1분 안구 휴식]**: 엄지손가락으로 눈썹 뼈 안쪽(눈 앞머리 위쪽)을 지그시 꾹꾹 눌러주며 눈 주변의 뭉친 혈을 풀어줍니다. 스마트폰은 10분간 엎어두세요!
            """)
