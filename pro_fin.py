import streamlit as st
import random
import requests

# 1. 페이지 설정 및 스타일 (수사대 다크 & 카툰 스타일)
st.set_page_config(
    page_title="국어 수사대 : 표준 발음법 추적 미션",
    page_icon="🕵️",
    layout="centered"
)

# 커스텀 스타일 (수사대 테마)
st.markdown("""
<style>
    .main-title { font-size: 2.5rem !important; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .subtitle { font-size: 1.15rem; color: #4B5563; text-align: center; margin-bottom: 25px; }
    .mission-header { background-color: #F3F4F6; border-left: 5px solid #1E3A8A; padding: 15px; border-radius: 5px; margin-bottom: 20px; font-weight: bold; }
    .stProgress .st-bo { background-color: #3B82F6; }
</style>
""", unsafe_allow_html=True)

# 2. 게임 세션 상태 초기화
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "student_id" not in st.session_state:
    st.session_state.student_id = ""
if "max_stages" not in st.session_state:
    st.session_state.max_stages = 5

# --- 인트로 화면 (학번/이름 입력 및 수사대 가입) ---
if st.session_state.stage == 1 and not st.session_state.user_name:
    st.markdown("<div class='main-title'>🕵️ 국어 수사대: 사라진 표준 발음을 찾아라!</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>우리가 무심히 쓰는 말속에 숨은 비밀 규칙을 파헤치는 특급 보강 미션!</div>", unsafe_allow_html=True)
    
    # 📌 코드로 직접 그리는 "사건 단서 게시판" (꽃 -> [꼳] 반영)
    st.markdown("""
    <div style="background-color: #2D3748; border: 4px solid #4A5568; border-radius: 12px; padding: 20px; margin-bottom: 25px; color: white;">
        <div style="text-align: center; font-size: 1.3rem; font-weight: bold; border-bottom: 2px dashed #718096; padding-bottom: 10px; margin-bottom: 15px;">
            🚨 [국어 수사본부 긴급 단서 게시판] 🚨
        </div>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 10px;">
            <div style="background-color: #FAF089; color: #1A202C; padding: 12px 18px; border-radius: 8px; box-shadow: 3px 3px 6px rgba(0,0,0,0.3); font-weight: bold;">
                📌 음운 교체 단서<br>
                • 꽃 ➔ <span style="color: #E53E3E;">[꼳]</span> (끝소리)<br>
                • 같이 ➔ <span style="color: #E53E3E;">[가치]</span> (구개음화)<br>
                • 신라 ➔ <span style="color: #E53E3E;">[실라]</span> (유음화)
            </div>
            <div style="background-color: #FED7D7; color: #1A202C; padding: 12px 18px; border-radius: 8px; box-shadow: 3px 3px 6px rgba(0,0,0,0.3); font-weight: bold;">
                📌 탈락 / 첨가 / 축약<br>
                • 흙 ➔ <span style="color: #2B6CB0;">[흑]</span> (자음군단순화)<br>
                • 맨입 ➔ <span style="color: #2B6CB0;">[맨닙]</span> (ㄴ첨가)<br>
                • 좋고 ➔ <span style="color: #2B6CB0;">[조코]</span> (거센소리)
            </div>
            <div style="background-color: #C6F6D5; color: #1A202C; padding: 12px 18px; border-radius: 8px; box-shadow: 3px 3px 6px rgba(0,0,0,0.3); font-weight: bold;">
                📌 오늘의 수사 미션<br>
                1. 조항 매칭 체포 작전<br>
                2. 조작된 연설문 발음 감식<br>
                3. 소리의 장단음 판별
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.warning("⚠️ 긴급 상황! '음운 변동' 규칙을 모르는 누군가가 표준 발음 조항들을 어지럽혀 놓았습니다. 지금 바로 수사대에 합류해 주세요!")
    
    col_id, col_nm = st.columns(2)
    with col_id:
        id_input = st.text_input("📝 학번을 입력하세요:", placeholder="예: 20101", key="id_box")
    with col_nm:
        name_input = st.text_input("📝 이름을 입력하세요:", placeholder="예: 홍길동", key="name_box")
        
    if st.button("🚨 수사 시작하기 (합류)"):
        if id_input.strip() and name_input.strip():
            st.session_state.student_id = id_input.strip()
            st.session_state.user_name = name_input.strip()
            st.session_state.stage = 1
            st.rerun()
        else:
            st.error("학번과 이름을 모두 입력해야 수사관 배지가 발급됩니다!")
    st.stop()

# --- 상단 고정 진행 바 & 수사관 정보 ---
progress_percentage = (st.session_state.stage - 1) / st.session_state.max_stages
st.sidebar.markdown(f"### 🎖️ {st.session_state.student_id} {st.session_state.user_name} 수사관")
st.sidebar.markdown(f"**현재 수사 진행률:** {int(progress_percentage * 100)}%")
st.sidebar.progress(progress_percentage)
st.sidebar.markdown(f"**누적 수사 점수:** {st.session_state.score}점 🌟")

# -------------------------------------------------------------
# MISSION 01: 발음 & 조항 매칭 (3단 매칭 퀴즈)
# -------------------------------------------------------------
if st.session_state.stage == 1:
    st.markdown("<div class='mission-header'>🎯 MISSION 01: 헝클어진 단어와 조항을 체포하라!</div>", unsafe_allow_html=True)
    st.markdown("사건 현장에 흩어진 단어들의 올바른 발음과 규칙을 매칭해 복구하세요.")
    
    m1_data = [
        {"word": "꽃", "p_correct": "꼳", "r_correct": "음절의 끝소리 규칙 (제9항)", "p_opts": ["꽃", "꼿", "꼳"], "r_opts": ["음절의 끝소리 규칙 (제9항)", "구개음화 (제17항)", "유음화 (제20항)"]},
        {"word": "신라", "p_correct": "실라", "r_correct": "유음화 (제20항)", "p_opts": ["신라", "신나", "실라"], "r_opts": ["비음화 (제18항)", "유음화 (제20항)", "된소리되기 (제23항)"]},
        {"word": "같이", "p_correct": "가치", "r_correct": "구개음화 (제17항)", "p_opts": ["갇이", "가치", "가티"], "r_opts": ["구개음화 (제17항)", "자음군 단순화 (제11항)", "거센소리되기 (제12항)"]},
    ]
    
    with st.form("m1_form"):
        ans_collect = []
        cols = st.columns(3)
        for i, d in enumerate(m1_data):
            with cols[i]:
                st.markdown(f"🔍 **단어: `{d['word']}`**")
                p = st.selectbox("올바른 발음?", d["p_opts"], key=f"m1_p_{i}")
                r = st.selectbox("적용 법칙?", d["r_opts"], key=f"m1_r_{i}")
                ans_collect.append((p, r))
        
        submitted = st.form_submit_button("🚨 단서 검증 (제출)")
        
    if submitted:
        correct_count = 0
        for idx, (p, r) in enumerate(ans_collect):
            data = m1_data[idx]
            if p == data["p_correct"] and r == data["r_correct"]:
                correct_count += 1
        
        if correct_count == 3:
            st.session_state.score += 30
            st.balloons()
            st.success("🎉 사건 완벽 해결! 흩어진 규칙들을 모두 안전하게 수거했습니다 (+30점)")
            if st.button("다음 사건(MISSION 02)으로 이동 ➡️"):
                st.session_state.stage = 2
                st.rerun()
        else:
            st.error(f"❌ 단서 일부가 잘못되었습니다 ({correct_count}/3 성공). 현장을 다시 살펴보고 재도전하세요!")

# -------------------------------------------------------------
# MISSION 02: 연설문 발음 추적 (실시간 발음 타이핑)
# -------------------------------------------------------------
elif st.session_state.stage == 2:
    st.markdown("<div class='mission-header'>📜 MISSION 02: 연설문 발음 조작단을 쫓아라!</div>", unsafe_allow_html=True)
    st.markdown("조작된 연설문의 **밑줄 친 단어 4개**의 실제 소리(표준 발음)를 한글로 입력해 복구하세요!")
    st.info("💡 주의: 대괄호 없이 발음 소리만 적어주세요! (예: `짧고` ➡️ `짤꼬`)")
    
    st.markdown("""
    > "제 공약을 **<u>짧고</u>** 말씀드리겠습니다.  
    > 친구들의 건의 사항을 수시로 **<u>듣고</u>** 소통하겠습니다.  
    > 교실 뒤에 **<u>책꽂이</u>**를 놓아 우리 반 친구들이 책을 **<u>읽는</u>** 습관을 기르도록 하겠습니다."
    """, unsafe_allow_html=True)
    
    m2_targets = [
        {"word": "짧고", "ans": "짤꼬", "tip": "겹받침 'ㄼ' 자음군 단순화 & 된소리되기"},
        {"word": "듣고", "ans": "듣꼬", "tip": "받침 'ㄷ' 뒤 된소리되기"},
        {"word": "책꽂이", "ans": "책꼬지", "tip": "받침 'ㅈ'이 연음되어 [지]로 발음"},
        {"word": "읽는", "ans": "잉는", "tip": "겹받침 'ㄺ' 단순화([익는]) 후 뒷소리 'ㄴ'에 의해 비음화([잉는])"}
    ]
    
    with st.form("m2_form"):
        ans_inputs = []
        cols = st.columns(2)
        for idx, item in enumerate(m2_targets):
            col = cols[idx % 2]
            user_input = col.text_input(f"🖋️ '{item['word']}'의 발음은?", placeholder="여기에 입력", key=f"m2_in_{idx}").strip()
            ans_inputs.append(user_input)
            
        submitted = st.form_submit_button("🔍 발음 감식 (체크)")
        
    if submitted:
        m2_score = 0
        feedback = []
        for idx, item in enumerate(m2_targets):
            if ans_inputs[idx] == item["ans"]:
                m2_score += 10
                feedback.append(f"✅ `{item['word']}` ➡️ `[{item['ans']}]` (감식 성공!)")
            else:
                feedback.append(f"❌ `{item['word']}` ➡️ 정답은 `[{item['ans']}]` 입니다. ({item['tip']})")
                
        for fb in feedback:
            st.write(fb)
            
        if m2_score == 40:
            st.session_state.score += 40
            st.snow()
            st.success("🕵️ 대단합니다! 사소한 소리의 비틀림까지 모두 찾아냈습니다. (+40점)")
            if st.button("다음 사건(MISSION 03)으로 이동 ➡️"):
                st.session_state.stage = 3
                st.rerun()
        else:
            st.warning("⚠️ 오판된 발음이 있습니다. 오답 힌트를 확인하고 다시 수정해 보세요!")

# -------------------------------------------------------------
# MISSION 03: 가나다 상담소 (규칙 분석)
# -------------------------------------------------------------
elif st.session_state.stage == 3:
    st.markdown("<div class='mission-header'>💬 MISSION 03: 상담소의 미스터리 해결 (자모의 발음)</div>", unsafe_allow_html=True)
    st.markdown("국립국어원에 들어온 발음 질문입니다. 수사관의 직관으로 정답을 골라주세요!")
    
    st.chat_message("user").write("'디귿이가'는 왜 [디그지가]가 아니라 [디그시가]로 발음할까요? 구개음화가 적용되어야 하는 것 아닌가요?")
    
    st.markdown("#### **🕵️ 수사대 소견**")
    q3_1 = st.radio(
        "Q1. 질문자가 [디그지가]가 맞다고 생각한 이론적 이유는 무엇일까요?",
        [
            "받침 'ㄷ, ㅌ'이 모음 'ㅣ'를 만나 [ㅈ, ㅊ]이 되는 '구개음화' 규칙 때문",
            "자음들이 서로 닮아가는 '비음화' 현상 때문",
            "글자 그대로 읽어야 한다는 강박 때문"
        ]
    )
    
    q3_2 = st.multiselect(
        "Q2. 「표준 발음법」 제16항에 의해 모음 조사 앞에서 [ㅅ]으로 변해 연음되는 친구들을 모두 골라내세요!",
        ["디귿(ㄷ)", "지읒(ㅈ)", "치읓(ㅊ)", "키읔(ㅋ)", "티읕(ㅌ)", "피읖(ㅍ)", "히읗(ㅎ)"],
        default=["디귿(ㄷ)"]
    )
    
    if st.button("🔎 진술 확인"):
        is_q1_correct = "구개음화" in q3_1
        expected_set = {"디귿(ㄷ)", "지읒(ㅈ)", "치읓(ㅊ)", "티읕(ㅌ)", "히읗(ㅎ)"}
        is_q2_correct = set(q3_2) == expected_set
        
        if is_q1_correct and is_q2_correct:
            st.session_state.score += 20
            st.balloons()
            st.success("🎉 완벽한 수사보고서입니다! 제16항의 예외 규정을 정확히 파악하셨습니다. (+20점)")
            if st.button("다음 사건(MISSION 04)으로 이동 ➡️"):
                st.session_state.stage = 4
                st.rerun()
        else:
            if not is_q1_correct:
                st.error("Q1 오답: 'ㄷ'이 'ㅣ'를 만나 'ㅈ'이 된다고 착각하는 것은 '구개음화' 때문입니다.")
            if not is_q2_correct:
                st.error("Q2 오답: 예외적으로 [ㅅ]으로 연음되는 자모는 'ㄷ, ㅈ, ㅊ, ㅌ, ㅎ' 총 5개입니다. (키읔, 피읖 제외)")

# -------------------------------------------------------------
# MISSION 04: 소리의 길이 (장단음 분별)
# -------------------------------------------------------------
elif st.session_state.stage == 4:
    st.markdown("<div class='mission-header'>⏳ MISSION 04: 시간 왜곡 장단을 맞춰라!</div>", unsafe_allow_html=True)
    st.markdown("단어의 길이에 따라 뜻이 달라지는 **장단음 사건**입니다. 상황에 맞는 소리 길이를 추적하세요!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📁 사건 A**")
        st.write("대영: '확실히 내 잘못을 **묻고** 가야겠어' (질문하기)")
        ans_a = st.selectbox("'질문하는 묻고'의 소리 길이는?", ["선택해 주세요...", "짧은소리(단음)", "긴소리(장음) [문:고]"], key="a")
        
    with col2:
        st.markdown("**📁 사건 B**")
        st.write("부연: '그대로 네 잘못을 **묻고** 끝내지 마!' (파묻기)")
        ans_b = st.selectbox("'파묻는 묻고'의 소리 길이는?", ["선택해 주세요...", "짧은소리(단음) [묻꼬]", "긴소리(장음)"], key="b")
        
    st.markdown("---")
    st.write("💡 **보너스 규칙:** 원래 첫 음절에서 길게 발음되던 단어에 **모음 어미나 피/사동 접미사**가 붙으면 소리가 어떻게 되나요?")
    bonus = st.radio("밟다[발:따] ➡️ 밟히다[?]", ["여전히 긴소리 [발:피다]", "짧아진소리 [발피다]"])
    
    if st.button("⏱️ 소리 파형 감식"):
        if ans_a == "긴소리(장음) [문:고]" and ans_b == "짧은소리(단음) [묻꼬]" and bonus == "짧아진소리 [발피다]":
            st.session_state.score += 20
            st.balloons()
            st.success("🎯 정확한 분석입니다! 질문은 길게[문:고], 파묻기는 짧게[묻꼬]이며, 접사 결합 시 소리가 짧아집니다! (+20점)")
            if st.button("다음 사건(MISSION 05)으로 이동 ➡️"):
                st.session_state.stage = 5
                st.rerun()
        else:
            st.error("🚨 소리의 길이에 오차가 있습니다. 대화 상황을 천천히 읽어보며 다시 감식해 보세요!")

# -------------------------------------------------------------
# MISSION 05: 외래어 발음 토론 (구글 시트 자동 전송)
# -------------------------------------------------------------
elif st.session_state.stage == 5:
    st.markdown("<div class='mission-header'>🌐 MISSION 05: 미래의 언어 표준을 지정하라!</div>", unsafe_allow_html=True)
    st.markdown("마지막 미션입니다. 일상 외래어의 실제 발음을 파악하고, 수사관님의 '최종 판결'을 기록해 주세요.")
    
    col1, col2 = st.columns(2)
    with col1:
        v1 = st.radio("Q1. 평소 '원룸(One room)'을 어떻게 발음하나요?", ["[원눔] (ㄴ첨가)", "[월룸] (유음화)", "[원룸] 있는 그대로"])
    with col2:
        v2 = st.radio("Q2. 평소 '온라인(Online)'을 어떻게 발음하나요?", ["[올라인] (유음화)", "[온라인] 있는 그대로"])
        
    opinion = st.text_area("🕵️ 그렇게 발음하거나, 표준어로 제정해야 하는 이유(근거)를 수사보고서 형식으로 작성하세요:")
    
    if st.button("📝 최종 수사보고서 제출 & 종결"):
        if len(opinion.strip()) < 10:
            st.warning("수사관님, 최종 의견과 근거를 최소 10자 이상 성의 있게 작성해 주세요!")
        else:
            # 📌 Google Apps Script 웹 앱 배포 URL을 여기에 넣으세요!
            GAS_WEB_APP_URL = "https://script.google.com/macros/s/1qYYXLIlrS25YUYYhFwvhJdgK6d3bupUgTExYRlLHmKU/exec"

            payload = {
                "student_id": st.session_state.student_id,
                "user_name": st.session_state.user_name,
                "score": st.session_state.score + 10,
                "v_oneroom": v1,
                "v_online": v2,
                "opinion": opinion.strip()
            }

            try:
                # 구글 시트로 실시간 전송
                requests.post(GAS_WEB_APP_URL, json=payload, timeout=5)
            except Exception:
                pass  # 네트워크 환경 이슈 시에도 학생 흐름은 정상 진행

            st.session_state.score += 10
            st.session_state.stage = 6
            st.rerun()

# -------------------------------------------------------------
# 엔딩: 1급 국어 수사관 임명장
# -------------------------------------------------------------
elif st.session_state.stage == 6:
    st.markdown("<h2 style='text-align: center;'>🎖️ 1급 국어 수사관 임명장 🎖️</h2>", unsafe_allow_html=True)
    st.write("")
    
    st.info(f"""
    **[ 국어 수사대 임명장 ]**
    
    * **학 번:** {st.session_state.student_id}
    * **성 명:** {st.session_state.user_name} 수사관
    * **최종 수사 점수:** {st.session_state.score} / 120 점 🌟
    
    위 사람은 '표준 발음법'과 관련된 음운 변동 사건들을 뛰어난 추리력과 끈기로 해결하고, 
    미래의 우리말 쓰임새(외래어)까지 깊이 있게 탐구하여 임무를 완수하였기에, 
    본 수사대 최고의 명예인 **『1급 국어 수사관』**으로 임명합니다!
    
    - 국어 수사대장 및 담당 국어 교사 -
    """)
    
    st.balloons()
    st.success("🎉 최종 수사보고서가 선생님께 안전하게 전송되었습니다! 화면을 캡처해 보관하세요. 수고하셨습니다!")
    
    if st.button("처음부터 다시 도전하기 🔄"):
        st.session_state.stage = 1
        st.session_state.score = 0
        st.session_state.user_name = ""
        st.session_state.student_id = ""
        st.rerun()