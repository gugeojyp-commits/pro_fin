import streamlit as st
import requests

# 1. 페이지 설정 및 스타일
st.set_page_config(
    page_title="국어 수사대 : 표준 발음법 전면 수사",
    page_icon="🕵️",
    layout="wide"
)

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

st.markdown("""
<style>
    .main-title { font-size: 2.2rem !important; font-weight: 800; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .subtitle { font-size: 1.1rem; color: #4B5563; text-align: center; margin-bottom: 25px; }
    .mission-header { background-color: #F1F5F9; border-left: 6px solid #1E3A8A; padding: 15px; border-radius: 6px; margin-bottom: 20px; font-weight: bold; font-size: 1.2rem; }
    .stTextInput>div>div>input { font-weight: bold; }
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

# --- 인트로 화면 ---
if st.session_state.stage == 1 and not st.session_state.user_name:
    st.markdown("<div class='main-title'>🕵️ 국어 수사대: 사라진 표준 발음을 찾아라!</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>교과서 속 모든 음운 변동과 표준 발음법 조항을 완전 정복하는 최종 수사 작전!</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background-color: #1E293B; border-radius: 12px; padding: 20px; margin-bottom: 25px; color: white;">
        <div style="text-align: center; font-size: 1.25rem; font-weight: bold; border-bottom: 1px dashed #64748B; padding-bottom: 10px; margin-bottom: 15px;">
            🚨 [국어 수사본부 긴급 단서 게시판] 🚨
        </div>
        <div style="display: flex; justify-content: space-around; flex-wrap: wrap; gap: 15px;">
            <div style="background-color: #FEF08A; color: #1E293B; padding: 12px 18px; border-radius: 8px; font-weight: bold;">
                📌 음운의 교체<br>
                • 꽃 ➔ [꼳] (음절 끝소리)<br>
                • 같이 ➔ [가치] (구개음화)<br>
                • 신라 ➔ [실라] (유음화)<br>
                • 국물 ➔ [궁물] (비음화)
            </div>
            <div style="background-color: #FECACA; color: #1E293B; padding: 12px 18px; border-radius: 8px; font-weight: bold;">
                📌 탈락 / 첨가 / 축약<br>
                • 흙 ➔ [흑] (자음군 단순화)<br>
                • 맨입 ➔ [맨닙] (ㄴ 첨가)<br>
                • 좋고 ➔ [조코] (거센소리되기)<br>
                • 다쳐서 ➔ [다처서] (반모음 j 탈락)
            </div>
            <div style="background-color: #BBF7D0; color: #1E293B; padding: 12px 18px; border-radius: 8px; font-weight: bold;">
                📌 오늘의 수사 미션<br>
                Mission 01. 10개 단어 & 조항 매칭<br>
                Mission 02. 연설문 20개 단어 발음 감식<br>
                Mission 03. 한글 자모 발음 특례<br>
                Mission 04. 소리의 길이(장단음) 수사<br>
                Mission 05. 외래어 표준 판결
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        id_in = st.text_input("📝 학번을 입력하세요 (예: 20101):", key="in_id")
    with col2:
        nm_in = st.text_input("📝 이름을 입력하세요 (예: 홍길동):", key="in_nm")
        
    if st.button("🚨 수사 본부 출동 (수사관 등록)", key="btn_start"):
        if id_in.strip() and nm_in.strip():
            st.session_state.student_id = id_in.strip()
            st.session_state.user_name = nm_in.strip()
            st.session_state.stage = 1
            safe_rerun()
        else:
            st.error("학번과 이름을 모두 입력해야 수사관 배지가 발급됩니다!")
    st.stop()

# --- 사이드바 ---
progress_pct = (st.session_state.stage - 1) / st.session_state.max_stages
st.sidebar.markdown(f"### 🎖️ {st.session_state.student_id} {st.session_state.user_name} 수사관")
st.sidebar.markdown(f"**현재 수사 진행률:** {int(progress_pct * 100)}%")
st.sidebar.progress(progress_pct)
st.sidebar.markdown(f"**누적 수사 점수:** {st.session_state.score}점 🌟")

# -------------------------------------------------------------
# MISSION 01: 1번 활동 10개 단어 전체 조항 매칭
# -------------------------------------------------------------
if st.session_state.stage == 1:
    st.markdown("<div class='mission-header'>🎯 MISSION 01: 10개 단어의 표준 발음과 조항을 검거하라!</div>", unsafe_allow_html=True)
    st.info("교과서 1번 활동에 제시된 10개 단어의 올바른 발음과 해당 표준 발음법 조항을 빠짐없이 선택하세요.")

    m1_list = [
        {"w": "꽃", "p_ans": "꼳", "p_opts": ["꽃", "꼿", "꼳"], "r_ans": "제9항(음절끝소리)", "r_opts": ["제9항(음절끝소리)", "제17항(구개음화)", "제18항(비음화)"]},
        {"w": "국물", "p_ans": "궁물", "p_opts": ["궁물", "국물", "군물"], "r_ans": "제18항(비음화)", "r_opts": ["제18항(비음화)", "제20항(유음화)", "제23항(된소리)"]},
        {"w": "신라", "p_ans": "실라", "p_opts": ["신나", "신라", "실라"], "r_ans": "제20항(유음화)", "r_opts": ["제20항(유음화)", "제18항(비음화)", "제17항(구개음화)"]},
        {"w": "숙제", "p_ans": "숙 crappy".replace("crappy", "private"), "p_ans": "숙private".replace("private", "쩨"), "p_opts": ["숙제", "숙쩨", "수쩨"], "r_ans": "제23항(된소리되기)", "r_opts": ["제23항(된소리되기)", "제9항(음절끝소리)", "제12항(거센소리)"]},
        {"w": "같이", "p_ans": "가치", "p_opts": ["가티", "갇이", "가치"], "r_ans": "제17항(구개음화)", "r_opts": ["제17항(구개음화)", "제11항(자음군단순화)", "제15항(연음/탈락)"]},
        {"w": "맨입", "p_ans": "맨닙", "p_opts": ["매닙", "맨입", "맨닙"], "r_ans": "제29항(ㄴ첨가)", "r_opts": ["제29항(ㄴ첨가)", "제22항(반모음첨가)", "제9항(음절끝소리)"]},
        {"w": "흙", "p_ans": "흑", "p_opts": ["흘", "흑", "흟"], "r_ans": "제11항(자음군단순화)", "r_opts": ["제11항(자음군단순화)", "제12항(거센소리)", "제23항(된소리)"]},
        {"w": "좋고", "p_ans": "조코", "p_opts": ["졷고", "조코", "좋고"], "r_ans": "제12항(거센소리되기)", "r_opts": ["제12항(거센소리되기)", "제11항(자음군단순화)", "제23항(된소리)"]},
        {"w": "다쳐서", "p_ans": "다처서", "p_opts": ["다쳐서", "다처서", "닫쳐서"], "r_ans": "제15항(반모음'j'탈락)", "r_opts": ["제15항(반모음'j'탈락)", "제22항(반모음'j'첨가)", "제17항(구개음화)"]},
        {"w": "뛰어", "p_ans": "뛰어 / 뛰여", "p_opts": ["뛰어만 허용", "뛰여만 허용", "뛰어 / 뛰여"], "r_ans": "제22항(반모음'j'첨가허용)", "r_opts": ["제22항(반모음'j'첨가허용)", "제15항(반모음탈락)", "제29항(ㄴ첨가)"]}
    ]

    cols = st.columns(2)
    user_m1 = []
    for idx, item in enumerate(m1_list):
        c = cols[idx % 2]
        with c:
            st.markdown(f"**단어 {idx+1}. `{item['w']}`**")
            p_val = st.selectbox(f"'{item['w']}'의 표준 발음", item["p_opts"], key=f"m1_p_{idx}")
            r_val = st.selectbox(f"'{item['w']}'의 적용 조항", item["r_opts"], key=f"m1_r_{idx}")
            user_m1.append((p_val, r_val))

    st.write("")
    if st.button("🚨 10개 단어 감식 결과 제출 및 다음 미션으로 (클릭)", key="btn_m1"):
        correct_cnt = 0
        wrongs = []
        for idx, (p_v, r_v) in enumerate(user_m1):
            target = m1_list[idx]
            if p_v == target["p_ans"] and r_v == target["r_ans"]:
                correct_cnt += 1
            else:
                wrongs.append(f"{target['w']} (정답: [{target['p_ans']}], {target['r_ans']})")
        
        if correct_cnt == 10:
            st.session_state.score += 30
            st.session_state.stage = 2
            safe_rerun()
        else:
            st.error(f"❌ 총 10개 중 {correct_cnt}개만 일치합니다. 잘못된 항목을 확인하고 수정해 주세요:\n- " + "\n- ".join(wrongs))

# -------------------------------------------------------------
# MISSION 02: 2번 활동 연설문 밑줄 친 20개 단어 전체
# -------------------------------------------------------------
elif st.session_state.stage == 2:
    st.markdown("<div class='mission-header'>📜 MISSION 02: 회장 선거 연설문 20개 단어 전면 감식!</div>", unsafe_allow_html=True)
    st.info("교과서 2번 활동의 밑줄 친 20개 단어 발음을 대괄호 없이 소리대로 정확히 적어주세요! (복수 표준발음은 하나만 적어도 인정)")

    st.markdown("""
    > "안녕하세요. 우리 반 회장 선거에 출마한 강태양입니다. 제 공약을 **<u>짧고</u>** **<u>굵게</u>** 말씀드리겠습니다.  
    > 첫째, **<u>의견란</u>**을 설치하겠습니다. 친구들의 **<u>건의</u>** 사항을 수시로 **<u>듣고</u>** **<u>폭넓게</u>** 소통하겠습니다.  
    > 둘째, 교실을 아름답게 가꾸겠습니다. 교실 **<u>곳곳에</u>** **<u>꽃을</u>** 두어 **<u>삭막한</u>** **<u>실내</u>** 분위기를 화사하게 바꾸겠습니다.  
    > 셋째, **<u>학급</u>** 문고를 만들겠습니다. 교실 뒤에 **<u>책꽂이</u>**를 놓아 우리 반 친구들이 책을 **<u>읽는</u>** 습관을 **<u>기를 수</u>** 있도록 하겠습니다.  
    > **<u>끝으로</u>**, **<u>궂은일</u>**도 마다하지 않는 회장이 **<u>되어</u>**, 친구들과 **<u>같이</u>** **<u>행복한</u>** 우리 반을 만들겠습니다."
    """, unsafe_allow_html=True)

    words_20 = [
        {"w": "짧고", "ans": ["짤꼬"]}, {"w": "굵게", "ans": ["국께"]}, {"w": "의견란", "ans": ["의견난"]}, {"w": "건의", "ans": ["거늬", "거니"]},
        {"w": "듣고", "ans": ["듣꼬"]}, {"w": "폭넓게", "ans": ["퐁널께"]}, {"w": "곳곳에", "ans": ["고꼬세"]}, {"w": "꽃을", "ans": ["꼬츨"]},
        {"w": "삭막한", "ans": ["상마칸"]}, {"w": "실내", "ans": ["실래"]}, {"w": "학급", "ans": ["학끕"]}, {"w": "책꽂이", "ans": ["책꼬지"]},
        {"w": "놓아", "ans": ["노아"]}, {"w": "읽는", "ans": ["잉는"]}, {"w": "기를 수", "ans": ["기를쑤", "기를 수"]}, {"w": "끝으로", "ans": ["끄트로"]},
        {"w": "궂은일", "ans": ["구즌닐"]}, {"w": "되어", "ans": ["되어", "되여"]}, {"w": "같이", "ans": ["가치"]}, {"w": "행복한", "ans": ["행보칸"]}
    ]

    cols = st.columns(4)
    u_ans_20 = {}
    for idx, item in enumerate(words_20):
        c = cols[idx % 4]
        u_ans_20[item["w"]] = c.text_input(f"{idx+1}. {item['w']}", key=f"m2_in_{idx}").strip()

    st.write("")
    if st.button("🔍 20개 단어 발음 감식 및 다음 미션으로 (클릭)", key="btn_m2"):
        pass_cnt = 0
        wrongs = []
        for item in words_20:
            val = u_ans_20[item["w"]]
            if val in item["ans"]:
                pass_cnt += 1
            else:
                wrongs.append(f"'{item['w']}' (입력값: '{val}' ➡️ 정답: {item['ans']})")

        if pass_cnt == 20:
            st.session_state.score += 40
            st.session_state.stage = 3
            safe_rerun()
        else:
            st.error(f"⚠️ 20개 중 {pass_cnt}개 일치! 틀린 항목을 다시 확인해 보세요:\n- " + "\n- ".join(wrongs))

# -------------------------------------------------------------
# MISSION 03: 3번 활동 국어원 상담소 & 7개 자모 21개 조사 결합형 전체
# -------------------------------------------------------------
elif st.session_state.stage == 3:
    st.markdown("<div class='mission-header'>💬 MISSION 03: 가나다 상담소 & 자모 발음 특례 (제16항)</div>", unsafe_allow_html=True)
    st.markdown("교과서 3번 활동입니다. 자모 뒤에 조사가 결합할 때의 발음 원리를 탐구하세요.")

    st.markdown("#### (1) 질문자가 해당 발음이 맞다고 생각한 까닭 추측")
    q3_reason = st.selectbox(
        "질문자가 [디그진가], [티으친가]가 맞다고 생각한 문법적 까닭은?",
        [
            "선택하세요...",
            "받침 'ㄷ, ㅌ'이 모음 'ㅣ'로 시작하는 형식 형태소 앞에서 [ㅈ, ㅊ]으로 바뀌는 '구개음화' 규칙 때문",
            "자음이 'ㄴ, ㅁ'을 만나 비음으로 바뀌는 '비음화' 규칙 때문",
            "모음 뒤에서 예외 없이 소리가 탈락하기 때문"
        ],
        key="q3_reason"
    )

    st.markdown("---")
    st.markdown("#### (2) 다음 말들의 표준 발음을 정확하게 완성해 보세요 (제16항 적용)")
    st.info("💡 주의: '디귿, 지읒, 치읓, 티읕, 히읗'은 모음 조사 앞에서 [ㅅ]으로 소리 납니다! (예: 디귿이 ➡️ 디그시)")

    jamo_list = [
        {"j": "디귿", "ans_i": "디그시", "ans_ul": "디그슬", "ans_e": "디그세"},
        {"j": "지읒", "ans_i": "지으시", "ans_ul": "지으슬", "ans_e": "지으세"},
        {"j": "치읓", "ans_i": "치으시", "ans_ul": "치으슬", "ans_e": "치으세"},
        {"j": "키읔", "ans_i": "키으기", "ans_ul": "키으글", "ans_e": "키으게"},
        {"j": "티읕", "ans_i": "티으시", "ans_ul": "티으슬", "ans_e": "티으세"},
        {"j": "피읖", "ans_i": "피으비", "ans_ul": "피으블", "ans_e": "피으베"},
        {"j": "히읗", "ans_i": "히으시", "ans_ul": "히으슬", "ans_e": "히으세"},
    ]

    cols = st.columns(3)
    u_jamo = {}
    for idx, item in enumerate(jamo_list):
        j = item["j"]
        st.markdown(f"**📌 자모: `{j}`**")
        c1, c2, c3 = st.columns(3)
        with c1:
            u_jamo[f"{j}이"] = c1.text_input(f"{j}이 [?]", key=f"j_{idx}_i").strip()
        with c2:
            u_jamo[f"{j}을"] = c2.text_input(f"{j}을 [?]", key=f"j_{idx}_ul").strip()
        with c3:
            u_jamo[f"{j}에"] = c3.text_input(f"{j}에 [?]", key=f"j_{idx}_e").strip()

    st.write("")
    if st.button("🔎 자모 발음 검증 및 다음 미션으로 (클릭)", key="btn_m3"):
        reason_ok = ("구개음화" in q3_reason)
        jamo_all_ok = True
        jamo_wrongs = []

        for item in jamo_list:
            j = item["j"]
            if u_jamo[f"{j}이"] != item["ans_i"]:
                jamo_all_ok = False; jamo_wrongs.append(f"{j}이 ➡️ [{item['ans_i']}]")
            if u_jamo[f"{j}을"] != item["ans_ul"]:
                jamo_all_ok = False; jamo_wrongs.append(f"{j}을 ➡️ [{item['ans_ul']}]")
            if u_jamo[f"{j}에"] != item["ans_e"]:
                jamo_all_ok = False; jamo_wrongs.append(f"{j}에 ➡️ [{item['ans_e']}]")

        if reason_ok and jamo_all_ok:
            st.session_state.score += 25
            st.session_state.stage = 4
            safe_rerun()
        else:
            err_msg = []
            if not reason_ok:
                err_msg.append("질문자의 까닭 추측에서 '구개음화 규칙 때문'을 선택해 주세요.")
            if not jamo_all_ok:
                err_msg.append(f"자모 발음 오답 목록: {', '.join(jamo_wrongs)}")
            st.error("❌ 수정이 필요합니다:\n- " + "\n- ".join(err_msg))

# -------------------------------------------------------------
# MISSION 04: 4번 활동 소리의 길이 (대화 분석 + 제7항 12개 단어 전체)
# -------------------------------------------------------------
elif st.session_state.stage == 4:
    st.markdown("<div class='mission-header'>⏳ MISSION 04: 소리의 길이 (장단음 탐구 & 제7항)</div>", unsafe_allow_html=True)
    st.markdown("교과서 4번 활동의 대화 탐구와 제6·7항 규정에 따른 소리의 길이를 판별하세요.")

    st.markdown("#### (1)~(3) 대영과 부연의 대화 분석")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**대영이 의도한 '묻다' (질문)**")
        ans_ask_mean = st.text_input("뜻 (예: 질문하다/물어보다):", key="m4_ask_m").strip()
        ans_ask_sound = st.selectbox("표준 발음 (소리의 길이):", ["선택...", "짧은소리 [묻따]", "긴소리 [문:따]"], key="m4_ask_s")
    with col2:
        st.markdown("**부연이 이해한 '묻다' (매몰/은폐)**")
        ans_bury_mean = st.text_input("뜻 (예: 파묻다/덮어두다):", key="m4_bury_m").strip()
        ans_bury_sound = st.selectbox("표준 발음 (소리의 길이):", ["선택...", "짧은소리 [묻따]", "긴소리 [문:따]"], key="m4_bury_s")

    st.markdown("**대영의 마지막 말에 쓰인 '묻는'의 발음 채점**")
    st.write("“그러니까 잘못을 묻는[ 1 ] 게 아니라 묻는[ 2 ]다고!”")
    cm1, cm2 = st.columns(2)
    with cm1:
        ans_mun1 = cm1.text_input("첫 번째 묻는 (파묻다) 발음:", key="m4_mun1").strip()
    with cm2:
        ans_mun2 = cm2.text_input("두 번째 묻는 (질문하다) 발음 (장음 표시는 : ):", key="m4_mun2").strip()

    st.markdown("---")
    st.markdown("#### (4) 「표준 발음법」 제6항·제7항에 따른 12개 단어 소리의 길이")
    st.info("💡 제7항: 긴소리를 가진 음절이라도 단음절 용언 어간에 모음 어미나 피/사동 접미사가 결합하면 **짧게** 발음합니다.")

    # 교과서 하단 12개 단어 전체
    length_quiz = [
        {"w": "눈보라", "ans": "긴소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "첫눈", "ans": "짧은소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "말씀", "ans": "긴소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "혼잣말", "ans": "짧은소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "벌리다", "ans": "긴소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "떠벌리다", "ans": "짧은소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "감다", "ans": "긴소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "감으니", "ans": "짧은소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "감기다", "ans": "짧은소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "밟다", "ans": "긴소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "밟으면", "ans": "짧은소리", "opts": ["긴소리", "짧은소리"]},
        {"w": "밝히다", "ans": "짧은소리", "opts": ["긴소리", "짧은소리"]}
    ]

    cols = st.columns(4)
    u_len = {}
    for idx, item in enumerate(length_quiz):
        c = cols[idx % 4]
        u_len[item["w"]] = c.selectbox(f"{item['w']}", item["opts"], key=f"len_{idx}")

    st.write("")
    if st.button("⏱️ 소리의 길이 판정 및 다음 미션으로 (클릭)", key="btn_m4"):
        part1_ok = (
            len(ans_ask_mean) >= 2 and "긴소리" in ans_ask_sound and
            len(ans_bury_mean) >= 2 and "짧은소리" in ans_bury_sound and
            ans_mun1 == "문는" and (ans_mun2 in ["문:는", "문ː는"])
        )

        part2_ok = True
        wrongs = []
        for item in length_quiz:
            if u_len[item["w"]] != item["ans"]:
                part2_ok = False
                wrongs.append(f"{item['w']} (정답: {item['ans']})")

        if part1_ok and part2_ok:
            st.session_state.score += 25
            st.session_state.stage = 5
            safe_rerun()
        else:
            errs = []
            if not part1_ok:
                errs.append("대화 분석(뜻 2글자 이상 입력, 질문=긴소리, 파묻다=짧은소리, 묻는=[문는]과 [문:는])을 확인하세요.")
            if not part2_ok:
                errs.append(f"장단음 판별 오답: {', '.join(wrongs)}")
            st.error("❌ 오차가 발견되었습니다:\n- " + "\n- ".join(errs))

# -------------------------------------------------------------
# MISSION 05: 5번 활동 외래어 발음 토론 & 구글 시트 전송
# -------------------------------------------------------------
elif st.session_state.stage == 5:
    st.markdown("<div class='mission-header'>🌐 MISSION 05: 외래어 발음 조사 & 나만의 표준 발음 제정</div>", unsafe_allow_html=True)
    st.markdown("교과서 5번 활동입니다. 표준 발음이 아직 정해지지 않은 외래어에 대해 나만의 표준 발음과 근거를 제시해 주세요.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**1. '원룸(One room)' 발음 선택**")
        v1 = st.radio("평소 어떻게 발음하시나요?", ["[원눔] (ㄴ첨가)", "[월룸] (유음화)", "[원룸] 표기 그대로"], key="m5_v1")
    with col2:
        st.markdown("**2. '온라인(Online)' 발음 선택**")
        v2 = st.radio("평소 어떻게 발음하시나요?", ["[올라인] (유음화)", "[온라인] 표기 그대로"], key="m5_v2")

    opinion = st.text_area(
        "🕵️ (3)~(4) '원룸'과 '온라인'의 표준 발음을 그렇게 정해야 하는 이유와 근거를 적어보세요 (15자 이상):",
        placeholder="예시: 외래어라도 한국어 화자들의 실제 발음 습관과 유음화/자음동화 규칙의 합리성을 고려하여...",
        key="m5_opinion"
    )

    st.write("")
    if st.button("📝 최종 수사보고서 제출 & 종결 (클릭)", key="btn_m5"):
        if len(opinion.strip()) < 15:
            st.warning("수사관님, 타당한 근거와 이유를 최소 15자 이상 성의 있게 서술해 주세요!")
        else:
            # 📌 여기에 발급받으신 Apps Script 웹 앱 URL(AKfycb.../exec)을 입력하세요.
            GAS_WEB_APP_URL = "https://script.google.com/macros/s/AKfycbw9W3FvLg_SAMPLE_REPLACE_ME/exec"

            payload = {
                "sheet_name": "3차시",
                "student_id": st.session_state.student_id,
                "user_name": st.session_state.user_name,
                "score": st.session_state.score + 10,
                "v_oneroom": v1,
                "v_online": v2,
                "opinion": opinion.strip()
            }

            if GAS_WEB_APP_URL.startswith("http") and "SAMPLE_REPLACE_ME" not in GAS_WEB_APP_URL:
                try:
                    requests.post(GAS_WEB_APP_URL, json=payload, timeout=5)
                except Exception:
                    pass

            st.session_state.score += 10
            st.session_state.stage = 6
            safe_rerun()

# -------------------------------------------------------------
# 엔딩: 1급 국어 수사관 임명장
# -------------------------------------------------------------
elif st.session_state.stage == 6:
    st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🎖️ 1급 국어 수사관 임명장 🎖️</h2>", unsafe_allow_html=True)
    st.write("")
    
    st.info(f"""
    **[ 국어 수사대 공식 임명장 ]**
    
    * **학 번:** {st.session_state.student_id}
    * **성 명:** {st.session_state.user_name} 수사관
    * **최종 수사 점수:** {st.session_state.score} / 130 점 🌟
    
    위 학생은 음운의 교체, 탈락, 첨가, 축약은 물론 한글 자모의 발음 특례와 소리의 장단음까지
    교과서의 모든 표준 발음 사건을 완벽한 논리와 추리력으로 해결하였으므로, 
    본 수사대 최고의 명예인 **『1급 국어 수사관』**으로 임명합니다!
    
    - 국어 수사대장 및 담당 국어 교사 일동 -
    """)
    
    st.success("🎉 모든 수사 미션을 완료하고 결과가 전송되었습니다! 위 임명장을 캡처해 과제방에 인증해 주세요.")
    
    if st.button("처음부터 다시 도전하기 🔄", key="btn_reset"):
        st.session_state.stage = 1
        st.session_state.score = 0
        st.session_state.user_name = ""
        st.session_state.student_id = ""
        safe_rerun()
