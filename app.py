import streamlit as st
import random
import time # time.sleep()을 위해 import

# ✅ 세션 상태 초기화 함수
def initialize_session_state():
    """Streamlit 세션 상태를 초기화하거나 재설정합니다."""
    # 모든 세션 키를 정의하여 초기화 및 재설정을 명확히 관리
    defaults = {
        "step": 0,
        "industry": "",
        "industry_confirmed": False,
        "company_name": "",
        "situation": "",
        "options": [],
        "selected_strategy_feedback": "", # 이전 단계의 선택된 전략 피드백용 (덮어쓰기 방지)
        "score": 0,
        "crisis_situation": "",
        "crisis_options": [],
        "effective_strategies_map": {}, # Step 3의 정답 전략 매핑 (이름 변경)
        "best_crisis_strategies_map": {}, # Step 5의 정답 전략 매핑 (이름 변경)
        "random_events_data": {}, # Step 8의 이벤트 데이터
        "step3_score_earned": 0, # Step 3에서 획득 점수
        "step5_score_earned": 0, # Step 5에서 획득 점수
        "step7_score_earned": 0, # Step 7에서 획득 점수
        "step8_score_earned": 0, # Step 8에서 획득 점수
        "step3_strategy_selected": "", # Step 3 선택 전략 기록
        "step5_strategy_selected": "", # Step 5 선택 전략 기록
        "step7_strategy_selected": "", # Step 7 선택 전략 기록
        "step8_strategy_selected": "", # Step 8 선택 전략 기록
        "current_event_name": None, # Step 8 현재 이벤트 이름
        "current_event_options": [], # Step 8 현재 이벤트 옵션
        "current_event_best_strategy": "", # Step 8 현재 이벤트 최적 전략
        "step7_state": "pending", # Step 7 진행 상태 관리
        "step8_state": "pending", # Step 8 진행 상태 관리
    }

    # 게임 재시작 시 기존 세션 상태를 모두 삭제하고 재초기화
    if st.session_state.get("reset_game", False):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.reset_game = False # 재설정 플래그 초기화

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# ---
# ✅ 공통 CSS 스타일 (한 번만 정의)
st.markdown("""
<style>
/* 전체 배경 및 텍스트 색상 */
body {
    background-color: #1a1a1a;
    color: #ffffff;
}

/* 기본 텍스트 요소 */
h1, h2, h3, h4, h5, h6, label, p, span, div {
    color: inherit;
}

/* selectbox 영역 - 흰 배경 + 검정 텍스트 */
div[data-baseweb="select"] {
    background-color: #ffffff;
    color: #000000;
}
div[data-baseweb="select"] * {
    color: #000000;
    fill: #000000;
}

/* 버튼 안 텍스트 */
button p {
    color: #000000;
    font-weight: bold;
}

/* 전체 컨테이너와 배경 이미지 */
.container {
    position: relative;
    width: 100%;
    height: 100vh;
    overflow: hidden;
    margin: 0;
    padding: 0;
    background-color: #1a1a1a;
}
.bg-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100vh;
    object-fit: cover;
    z-index: 0;
}

/* 말풍선 스타일 */
.speech-bubble {
    position: absolute;
    bottom: 8vh;
    left: 50%;
    transform: translateX(-50%);
    width: 90%;
    max-width: 500px;
    background: rgba(255, 255, 255, 0.1);
    padding: 20px 25px;
    border-radius: 25px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
    text-align: center;
    z-index: 1;
    backdrop-filter: blur(8px);
}

/* 말풍선 내 제목/본문 */
.speech-title {
    font-size: 1.4rem;
    font-weight: bold;
    color: #ffffff;
}
.speech-sub {
    margin-top: 10px;
    font-size: 1rem;
    color: #f0f0f0;
}
</style>
""", unsafe_allow_html=True)


# ✅ 말풍선 출력 함수
def show_speech(title: str, subtitle: str, image_url: str):
    """말풍선과 배경 이미지를 포함한 UI를 렌더링합니다."""
    st.markdown(f"""
    <div class="container">
        <img src="{image_url}" class="bg-image">
        <div class="speech-bubble">
            <div class="speech-title">{title}</div>
            <div class="speech-sub">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---
## Step 0: 시작 안내
if st.session_state.step == 0:
    show_speech("“환영합니다!”", "게임 플레이에 앞서 다크모드를 적용중이시라면 라이트모드로 전환해주시길 바랍니다.", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    st.markdown("### 경영 시뮬레이션 게임에 오신 것을 환영합니다!")
    st.markdown("이 게임에서는 회사를 창업하고 성장시키는 과정에서 다양한 결정을 내려야 합니다. 회사를 성공적으로 운영해보세요!")
    if st.button("게임 시작 ▶️"):
        st.session_state.step = 1
        st.rerun()

# ---
## Step 1: 업종 선택
elif st.session_state.step == 1:
    if not st.session_state.industry_confirmed:
        show_speech("“좋아, 이제 우리가 어떤 산업에 뛰어들지 결정할 시간이군.”", "어떤 분야에서 승부할지, 네 선택을 보여줘.", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    else:
        show_speech(f"“{st.session_state.industry}... 흥미로운 선택이군.”", "다음 단계로 가볼까?", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")

    st.markdown("### Step 1: 회사 분야 선택")
    industries = ["💻 IT 스타트업", "🌱 친환경 제품", "🎮 게임 개발사", "👗 패션 브랜드", "🍔 푸드테크", "🛒 글로벌 전자상거래"]

    if not st.session_state.industry_confirmed:
        selected = st.selectbox("회사 업종을 선택해주세요", industries)
        if st.button("업종 확정"):
            st.session_state.industry = selected
            st.session_state.industry_confirmed = True
            st.session_state.step = 2
            st.rerun()
    else:
        st.success(f"✅ 선택된 업종: **{st.session_state.industry}**")
        if st.button("다음 ▶️"):
            st.session_state.step = 2
            st.rerun()

# ---
## Step 2: 회사 이름 입력
elif st.session_state.step == 2:
    if not st.session_state.company_name:
        show_speech("“이제 회사를 설립할 시간이야.”", "멋진 회사 이름을 지어보자!", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    else:
        show_speech(f"“{st.session_state.company_name}... 멋진 이름이군!”", "이제 다음 단계로 넘어가자.", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")

    st.markdown("### Step 2: 회사 이름 입력")
    name_input = st.text_input("당신의 회사 이름은?", max_chars=20)

    if st.button("회사 이름 확정"):
        if name_input.strip():
            st.session_state.company_name = name_input.strip()
            st.success("✅ 회사 이름이 등록되었습니다!")
        else:
            st.warning("⚠️ 회사 이름을 입력해주세요.")

    if st.session_state.company_name and st.button("다음 ▶️"):
        st.session_state.step = 3
        st.rerun()

# ---
## Step 3: 전략 선택
elif st.session_state.step == 3:
    show_speech("“예기치 못한 사건 발생!”", "상황에 적절한 전략을 선택해 회사를 지켜내자.", "https://raw.githubusercontent.com/dddowobbb/simulator1/main/badevent.png")

    # Step 3 관련 데이터 정의 및 세션에 저장
    situations = {
        "⚠️ 대규모 고객 데이터 유출 발생": ["보안 시스템 전면 재구축", "PR 대응", "사과문 발표", "외부 컨설턴트 투입", "서비스 일시 중단"],
        "📈 갑작스러운 수요 폭증": ["생산 라인 확장", "기술 투자", "임시 고용 확대", "외주 활용", "품질 단가 조정"],
        "💸 원자재 가격 급등": ["공급처 다변화", "대체 소재 도입", "장기 계약", "수입 조정", "원가 절감"],
        "🔥 경쟁사 파산": ["인재 채용 강화", "기술 인수", "시장 확대", "기술 유출 방지", "법적 검토"],
        "📉 주요 제품 매출 급감": ["제품 리뉴얼", "광고 캠페인", "신제품 출시", "할인 행사", "시장 조사"],
        "🏆 대기업으로부터 투자 제안": ["지분 일부 매각", "전략적 제휴", "거절", "조건 재협상", "지분 공동 소유"],
        "🌍 글로벌 시장 진출 기회": ["현지화 전략", "글로벌 광고 캠페인", "온라인 직판", "외국 파트너와 제휴", "해외 공장 설립"]
    }
    effective_strategies_map_data = { # 이름 변경: effective_strategies_map_data
        "⚠️ 대규모 고객 데이터 유출 발생": "보안 시스템 전면 재구축",
        "📈 갑작스러운 수요 폭증": "생산 라인 확장",
        "💸 원자재 가격 급등": "공급처 다변화",
        "🔥 경쟁사 파산": "인재 채용 강화",
        "📉 주요 제품 매출 급감": "제품 리뉴얼",
        "🏆 대기업으로부터 투자 제안": "지분 일부 매각",
        "🌍 글로벌 시장 진출 기회": "현지화 전략"
    }
    st.session_state.effective_strategies_map = effective_strategies_map_data # 세션에 저장

    if not st.session_state.situation:
        st.session_state.situation, st.session_state.options = random.choice(list(situations.items()))

    st.markdown("### Step 3: 전략 선택")
    st.markdown(f"📍 **상황:** {st.session_state.situation}")
    strategy = st.radio("🧠 당신의 전략은?", st.session_state.options)

    if st.button("전략 확정"):
        st.session_state.step3_strategy_selected = strategy # 단계별 전략 기록
        
        # 점수 계산 및 저장 (로컬 변수 사용 없이 직접 세션 상태에 접근)
        if strategy == st.session_state.effective_strategies_map.get(st.session_state.situation):
            st.session_state.score += 10
            st.session_state.step3_score_earned = 10
            st.session_state.selected_strategy_feedback = f"선택한 전략: **{strategy}** (획득 점수: 10점)"
        else:
            st.session_state.score += 5
            st.session_state.step3_score_earned = 5
            st.session_state.selected_strategy_feedback = f"선택한 전략: **{strategy}** (획득 점수: 5점)"

        st.session_state.step = 4
        st.rerun()

# ---
## Step 4: 결과 분석 및 피드백
elif st.session_state.step == 4:
    # Step 3에서 저장된 정보를 활용하여 피드백
    score_earned_this_step = st.session_state.get("step3_score_earned", 0)
    selected_strategy_for_feedback = st.session_state.get("step3_strategy_selected", "선택 없음")

    if score_earned_this_step == 10:
        title = "“훌륭한 판단이었어!”"
        subtitle = st.session_state.selected_strategy_feedback
    else:
        title = "“음... 더 나은 전략도 있었을 거야.”"
        subtitle = st.session_state.selected_strategy_feedback

    show_speech(title, subtitle, "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")

    st.markdown("### Step 4: 결과 분석")
    st.success(f"당신의 전략: **{selected_strategy_for_feedback}**")
    st.info(f"현재 점수: **{st.session_state.score}점**")

    # Step 3 관련 세션 상태 정리
    if "step3_score_earned" in st.session_state:
        del st.session_state.step3_score_earned
    if "step3_strategy_selected" in st.session_state:
        del st.session_state.step3_strategy_selected
    st.session_state.situation = ""
    st.session_state.options = []
    st.session_state.selected_strategy_feedback = "" # 피드백 메시지 초기화

    # 사용자 제어권 보장 (다음 버튼)
    if st.button("다음 이벤트 ▶️"):
        st.session_state.step = 5
        st.rerun()

# ---
## Step 5: 국가적 위기 대응
elif st.session_state.step == 5:
    show_speech("“국가적 위기 발생!”", "경제, 정치, 국제 환경이 급변하고 있어. 대응 전략이 필요해.", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")

    # Step 5 관련 데이터 정의
    crisis_situations = {
        "📉 한국 외환시장 급변 (원화 가치 급락)": ["환 헤지 강화", "수출 확대", "정부와 협력", "외환 보유 확대", "위기 커뮤니케이션"],
        "🇺🇸 미 연준의 기준금리 인상": ["대출 축소", "내수 집중 전략", "고금리 대비 자산 조정", "비용 구조 개선", "긴축 경영"],
        "🗳️ 정치적 불확실성 증가": ["리스크 분산 경영", "정치 모니터링 강화", "내부 의사결정 체계 정비", "단기 전략 전환", "위기 대비 태스크포스 운영"],
        "🇺🇸 트럼프 대통령 재취임": ["미국 중심 전략 강화", "공급망 재편", "관세 대비 물류 최적화", "현지 생산 강화", "미국 투자 확대"],
        "🛃 주요 국가의 관세 인상 정책": ["무역 파트너 다변화", "현지 생산 확대", "비관세 수출 전략", "신시장 개척", "가격 재설정"]
    }
    
    # 🚨 중요: best_strategies_map_data를 Step 5 진입 시 한 번만 정의하여 세션에 저장
    if "best_crisis_strategies_map" not in st.session_state or not st.session_state.best_crisis_strategies_map:
        best_strategies_map_data = { # 이름 변경: best_strategies_map_data
            "📉 한국 외환시장 급변 (원화 가치 급락)": "환 헤지 강화",
            "🇺🇸 미 연준의 기준금리 인상": "고금리 대비 자산 조정",
            "🗳️ 정치적 불확실성 증가": "리스크 분산 경영",
            "🇺🇸 트럼프 대통령 재취임": "공급망 재편", # 트럼프 재취임 시 '공급망 재편'이 가장 적절한 대응 전략으로 판단
            "🛃 주요 국가의 관세 인상 정책": "무역 파트너 다변화"
        }
        st.session_state.best_crisis_strategies_map = best_strategies_map_data # 세션에 저장

    if not st.session_state.crisis_situation:
        st.session_state.crisis_situation, st.session_state.crisis_options = random.choice(list(crisis_situations.items()))

    st.markdown("### Step 5: 국가적 위기 대응")
    st.markdown(f"**상황:** {st.session_state.crisis_situation}")
    crisis_strategy = st.radio("🧠 대응 전략을 선택하세요:", st.session_state.crisis_options)

    if st.button("전략 확정"):
        st.session_state.step5_strategy_selected = crisis_strategy # ✅ 단계별 전략 기록

        # 세션 상태에 저장된 best_crisis_strategies_map을 사용하여 점수 계산
        if crisis_strategy == st.session_state.best_crisis_strategies_map.get(st.session_state.crisis_situation):
            st.session_state.score += 10
            st.session_state.step5_score_earned = 10
            st.session_state.selected_strategy_feedback = f"국가적 위기 속 **{crisis_strategy}** 전략은 뛰어난 선택이었어. (획득 점수: 10점)"
        else:
            st.session_state.score += 5
            st.session_state.step5_score_earned = 5
            st.session_state.selected_strategy_feedback = f"국가적 위기 속 **{crisis_strategy}** 전략도 나쁘지 않았어. (획득 점수: 5점)"

        # Step 6으로 이동. Step 6에서 다음 버튼이 있음.
        st.session_state.step = 6
        st.rerun()

# ---
## Step 6: 중간 평가
elif st.session_state.step == 6:
    # Step 5에서 저장된 정보 활용
    score_earned_this_step = st.session_state.get("step5_score_earned", 0)
    selected_strategy_for_feedback = st.session_state.get("step5_strategy_selected", "선택 없음")

    if score_earned_this_step == 10:
        title = "“최고의 경영자군!”"
        # subtitle은 Step 5에서 이미 세션에 저장된 feedback 메시지를 사용
        subtitle = st.session_state.selected_strategy_feedback + f" 총 점수: {st.session_state.score}점"
    else:
        title = "“괜찮은 성과지만 아직 성장 가능성이 보여.”"
        subtitle = st.session_state.selected_strategy_feedback + f" 총 점수: {st.session_state.score}점"

    show_speech(title, subtitle, "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
    st.markdown("### Step 6: 중간 평가")
    st.success(f"당신의 전략: **{selected_strategy_for_feedback}**")
    st.info(f"현재 점수: **{st.session_state.score}점**")

    # Step 5 관련 세션 상태 정리
    if "step5_score_earned" in st.session_state:
        del st.session_state.step5_score_earned
    if "step5_strategy_selected" in st.session_state:
        del st.session_state.step5_strategy_selected
    # crisis_situation, crisis_options는 Step 5에서 전략 확정 시 이미 초기화됨
    st.session_state.selected_strategy_feedback = "" # 피드백 메시지 초기화

    # 사용자 제어권 보장 (다음 버튼)
    if st.button("다음 이벤트 ▶️"):
        st.session_state.step = 7
        st.rerun()

# ---
## Step 7: 내부 문제 해결
elif st.session_state.step == 7:
    org_issues = {
        "🧠 조직문화 혁신": 10,
        "💰 복지 강화": 8,
        "🔁 리더십 교체": 6,
        "📚 교육 강화": 7,
        "🧘 그냥 기다린다": 2
    }

    # Step 7의 상태를 별도로 관리하여 중복 실행 방지
    # initialize_session_state()에서 기본값 "pending"으로 설정됨
    if st.session_state.step7_state == "pending":
        show_speech("“요즘 직원들 분위기가 심상치 않아...”", "사기 저하, 인사 갈등, 생산성 저하 문제가 보고됐어. 어떻게 대응할까?", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
        st.markdown("### Step 7: 내부 문제 해결 전략 선택")

        selected_org_strategy = st.radio("내부 문제를 해결할 전략을 선택하세요:", list(org_issues.keys()))

        if st.button("전략 확정"):
            st.session_state.step7_strategy_selected = selected_org_strategy # 단계별 전략 기록
            st.session_state.score += org_issues[selected_org_strategy]
            st.session_state.step7_score_earned = org_issues[selected_org_strategy]

            if st.session_state.step7_score_earned >= 8:
                title = "“탁월한 내부 결정이었어!”"
            elif st.session_state.step7_score_earned >= 5:
                title = "“무난한 선택이었군.”"
            else:
                title = "“기다리는 건 항상 좋은 선택은 아니지...”"
            st.session_state.selected_strategy_feedback = f"{selected_org_strategy} 전략에 따른 점수: {st.session_state.step7_score_earned}점"

            st.session_state.step7_state = "done" # 상태 변경
            st.rerun()
    elif st.session_state.step7_state == "done":
        # 피드백 표시
        title = st.session_state.selected_strategy_feedback.split('(')[0].strip() + "!" # 제목 추출
        subtitle = st.session_state.selected_strategy_feedback + f" (누적 점수: {st.session_state.score}점)"
        show_speech(title, subtitle, "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")

        st.success(f"전략: **{st.session_state.step7_strategy_selected}**")
        st.info(f"누적 점수: **{st.session_state.score}점**")

        # Step 7 관련 세션 상태 정리
        if "step7_score_earned" in st.session_state:
            del st.session_state.step7_score_earned
        if "step7_strategy_selected" in st.session_state:
            del st.session_state.step7_strategy_selected
        st.session_state.selected_strategy_feedback = ""
        st.session_state.step7_state = "pending" # 다음 게임을 위해 초기화

        # 사용자 제어권 보장 (다음 버튼)
        if st.button("다음 이벤트 ▶️"):
            st.session_state.step = 8
            st.rerun()

# ---
## Step 8: 돌발 변수 등장
elif st.session_state.step == 8:
    # Step 8 관련 데이터 정의 및 세션에 저장
    if not st.session_state.random_events_data: # 한 번만 정의하도록 체크
        st.session_state.random_events_data = {
            "📉 글로벌 경제 불황": {
                "options": ["비용 절감", "내수 시장 집중", "긴축 재정 운영", "신사업 보류", "시장 철수"],
                "best": "내수 시장 집중"
            },
            "🚀 경쟁사의 혁신 제품 발표": {
                "options": ["기술 개발 가속", "브랜드 리뉴얼", "마케팅 강화", "가격 인하", "특허 소송"],
                "best": "기술 개발 가속"
            },
            "📜 정부 규제 강화": {
                "options": ["법무팀 확대", "규제 준수 시스템 강화", "비즈니스 모델 전환", "로비 활동 강화", "해외 진출 모색"],
                "best": "규제 준수 시스템 강화"
            }
        }

    # Step 8의 상태를 별도로 관리하여 중복 실행 방지
    # initialize_session_state()에서 기본값 "pending"으로 설정됨
    if st.session_state.step8_state == "pending":
        show_speech("“뜻밖의 일이 벌어졌어!”", "외부 변수로 인해 경영환경이 크게 흔들리고 있어.", "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")
        st.markdown("### Step 8: 돌발 변수 등장")

        if st.session_state.current_event_name is None: # 이벤트가 아직 선택되지 않았다면 새로 선택
            event_name, event_info = random.choice(list(st.session_state.random_events_data.items()))
            st.session_state.current_event_name = event_name
            st.session_state.current_event_options = event_info["options"]
            st.session_state.current_event_best_strategy = event_info["best"]

        st.markdown(f"**🌀 이벤트:** {st.session_state.current_event_name}")
        selected_event_strategy = st.radio("✅ 어떤 전략으로 대응할까요?", st.session_state.current_event_options)

        if st.button("전략 확정"):
            st.session_state.step8_strategy_selected = selected_event_strategy # 단계별 전략 기록

            if selected_event_strategy == st.session_state.current_event_best_strategy:
                st.session_state.score += 10
                st.session_state.step8_score_earned = 10
                title = "“이번에도 잘 대처했군.”"
                st.session_state.selected_strategy_feedback = f"{selected_event_strategy} 전략으로 10점 획득!"
            else:
                st.session_state.score += 5
                st.session_state.step8_score_earned = 5
                title = "“나쁘지 않은 대응이었어.”"
                st.session_state.selected_strategy_feedback = f"{selected_event_strategy} 전략으로 5점 획득!"

            st.session_state.step8_state = "done" # 상태 변경
            st.rerun()
    elif st.session_state.step8_state == "done":
        # 피드백 표시
        title = st.session_state.selected_strategy_feedback.split('으로')[0].strip() + "!" # 제목 추출
        subtitle = st.session_state.selected_strategy_feedback + f" (총 점수: {st.session_state.score}점)"
        show_speech(title, subtitle, "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png")

        st.success(f"전략: **{st.session_state.step8_strategy_selected}**")
        st.info(f"총 점수: **{st.session_state.score}점**")

        # Step 8 관련 세션 상태 정리
        if "step8_score_earned" in st.session_state:
            del st.session_state.step8_score_earned
        if "step8_strategy_selected" in st.session_state:
            del st.session_state.step8_strategy_selected
        st.session_state.current_event_name = None
        st.session_state.current_event_options = []
        st.session_state.current_event_best_strategy = ""
        st.session_state.selected_strategy_feedback = ""
        st.session_state.step8_state = "pending" # 다음 게임을 위해 초기화

        # 사용자 제어권 보장 (다음 버튼)
        if st.button("최종 결과 확인 ▶️"):
            st.session_state.step = 9
            st.rerun()

# ---
## Step 9: 게임 종료 또는 최종 결과
elif st.session_state.step == 9:
    final_score = st.session_state.score
    final_message = ""
    image_url = "https://raw.githubusercontent.com/dddowobbb/16-1/main/talking%20ceo.png" # 기본 이미지

    if final_score >= 40: # 임의의 기준, 게임의 난이도에 따라 조정
        final_message = "“축하한다! 너는 최고의 경영자야. 우리 회사는 네 덕분에 크게 번창했어!”"
        title_bubble = "“위대한 성공!”"
    elif final_score >= 20:
        final_message = "“나쁘지 않은 결과였어. 하지만 더 성장할 여지가 많아 보이는군.”"
        title_bubble = "“괜찮은 성과!”"
    else:
        final_message = "“아쉽지만, 다음번엔 더 나은 결과를 기대해 볼게.”"
        title_bubble = "“재정비의 시간!”"
        image_url = "https://raw.githubusercontent.com/dddowobbb/16-1/main/sad_ceo.png" # 실패 시 다른 이미지 예시

    show_speech(title_bubble, final_message, image_url)
    st.markdown("### Step 9: 게임 결과")
    st.markdown(f"**수고하셨습니다, {st.session_state.company_name}의 CEO!**")
    st.success(f"당신의 최종 점수: **{final_score}점**")

    if st.button("다시 시작하기"):
        st.session_state.reset_game = True # 재설정 플래그 설정
        st.rerun()
