# quiz_app.py
# 웹 클릭형 Python 중간고사 퀴즈 (Streamlit)
# - 보기/문항 무작위
# - 즉시 채점/해설
# - 오답만 재도전
# - "출제 문항 수" 변경 후 [적용] 버튼으로 즉시 반영
import os, warnings, logging
os.environ.setdefault("PYTHONWARNINGS", "ignore")
warnings.filterwarnings("ignore")
logging.disable(logging.WARNING)
import random
import streamlit as st

st.set_page_config(page_title="인공지능 퀴즈 대비", layout="wide")
st.title("📘 인공지능 퀴즈 머신")

# =========================
# 1) 문제 데이터셋
#    → 여기만 네 100문항으로 교체
# =========================
QUESTIONS = [
{"q": "지식표현에서 데이터, 정보, 지식의 관계를 가장 올바르게 설명한 것은?", 
 "options": ["데이터→정보→지식→지혜", "정보→데이터→지식→지혜", "지식→정보→데이터→지혜", "데이터→지식→정보→지혜"], 
 "answer": 1},

{"q": "의미망(semantic network)의 기본 구성 요소는?", 
 "options": ["노드와 간선", "조건과 결론", "객체와 속성", "슬롯과 데몬"], 
 "answer": 1},

{"q": "프레임(frame)을 제안한 사람은?", 
 "options": ["Zadeh", "Minsky", "Frege", "Berners-Lee"], 
 "answer": 2},

{"q": "프레임의 속성을 나타내는 구성요소는?", 
 "options": ["슬롯(slot)", "노드(node)", "규칙(rule)", "패턴(pattern)"], 
 "answer": 1},

{"q": "슬롯에 부가 정보를 제공하는 구성요소는?", 
 "options": ["패싯(facet)", "데몬(demon)", "조건식", "속성(attribute)"], 
 "answer": 1},

{"q": "프레임에서 if-needed 조건은 언제 실행되는가?", 
 "options": ["슬롯 값이 필요할 때", "값이 추가될 때", "값이 삭제될 때", "프레임이 초기화될 때"], 
 "answer": 1},

{"q": "의미망에서 has-a 관계는 어떤 관계를 의미하는가?", 
 "options": ["전체-부분 관계", "상속 관계", "인스턴스 관계", "시간적 관계"], 
 "answer": 1},

{"q": "시맨틱 웹(Semantic Web)의 목적은?", 
 "options": ["웹 페이지의 시각화", "기계가 데이터의 의미를 이해하도록 함", "웹 검색 속도 향상", "데이터 압축 효율 향상"], 
 "answer": 2},

{"q": "시맨틱 웹에서 사용되는 기술이 아닌 것은?", 
 "options": ["RDF", "OWL", "SPARQL", "SMOTE"], 
 "answer": 4},

{"q": "명제논리에서 ‘참 또는 거짓’을 판정할 수 있는 문장을 무엇이라 하는가?", 
 "options": ["명제", "술어", "패싯", "절"], 
 "answer": 1},

{"q": "명제 P→Q에서 P를 무엇이라 하는가?", 
 "options": ["결론", "전제", "귀결", "리터럴"], 
 "answer": 2},

{"q": "모더스 포넌스(Modus Ponens)는 어떤 형태의 추론인가?", 
 "options": ["A→B, A ⊢ B", "A→B, ¬B ⊢ ¬A", "A→B, B→C ⊢ A→C", "A∨B, ¬A ⊢ B"], 
 "answer": 1},

{"q": "명제논리에서 타당한 논리식(항진식)이란?", 
 "options": ["모든 모델에서 참인 식", "모든 모델에서 거짓인 식", "특정 모델에서만 참인 식", "참과 거짓이 번갈아 나오는 식"], 
 "answer": 1},

{"q": "명제논리의 논리곱 정규형(CNF)은 어떤 형태인가?", 
 "options": ["논리합 절들의 논리곱", "논리곱 절들의 논리합", "단일 명제", "부정식의 합"], 
 "answer": 1},

{"q": "논리융합(resolution)에서 두 절이 상반되는 리터럴을 가질 때 생성되는 것은?", 
 "options": ["새로운 절", "항진식", "모순", "공리"], 
 "answer": 1},

{"q": "프레임의 장점으로 옳지 않은 것은?", 
 "options": ["개념 구조화", "지식 재사용 용이", "일관성 유지", "비구조적 표현"], 
 "answer": 4},

{"q": "프레임에서 슬롯의 절차적 지식 실행 메커니즘은?", 
 "options": ["데몬", "노드", "조건부", "리터럴"], 
 "answer": 1},

{"q": "‘소크라테스는 인간이다. 인간은 죽는다.’에서 ‘소크라테스는 죽는다’가 나오는 추론법은?", 
 "options": ["삼단논법", "부정논법", "모더스 포넌스", "논리융합"], 
 "answer": 1},

{"q": "논리적 귀결(entailment) Δ⊨ω의 의미는?", 
 "options": ["Δ가 ω를 참으로 만든다", "ω가 Δ를 거짓으로 만든다", "Δ가 ω보다 크다", "Δ가 ω를 대체한다"], 
 "answer": 1},

{"q": "시맨틱 웹의 핵심 아이디어는?", 
 "options": ["데이터의 의미적 구조화", "하이퍼링크 최적화", "데이터 압축", "그래픽 성능 향상"], 
 "answer": 1},

{"q": "퍼지논리는 누구에 의해 제안되었는가?", 
 "options": ["Zadeh", "Minsky", "Frege", "Russell"], 
 "answer": 1},

{"q": "퍼지논리에서 소속함수는 무엇을 나타내는가?", 
 "options": ["집합에 속하는 정도", "명제의 진리값", "패싯의 개수", "변수의 범위"], 
 "answer": 1},

{"q": "퍼지집합에서 교집합은 어떤 연산으로 계산되는가?", 
 "options": ["min", "max", "1-μ", "곱셈"], 
 "answer": 1},

{"q": "퍼지집합에서 여집합의 연산은?", 
 "options": ["1-μ", "μ1+μ2", "min", "max"], 
 "answer": 1},

{"q": "퍼지추론에서 입력값을 소속함수로 변환하는 과정은?", 
 "options": ["퍼지화(fuzzification)", "역퍼지화(defuzzification)", "가중합", "논리융합"], 
 "answer": 1},

{"q": "퍼지추론에서 출력값을 명확한 수치로 변환하는 과정은?", 
 "options": ["역퍼지화", "퍼지화", "정규화", "비퍼지화"], 
 "answer": 1},

{"q": "max-min 추론에서 결론부 함축 처리 시 사용하는 연산은?", 
 "options": ["min", "max", "곱셈", "합"], 
 "answer": 1},

{"q": "역퍼지화 방법 중 중심점(Centroid)법은 어떤 계산을 수행하는가?", 
 "options": ["DOM과 x값의 가중평균", "최대값의 평균", "최솟값의 평균", "합의 제곱평균"], 
 "answer": 1},

{"q": "퍼지언어 변수(fuzzy linguistic variable)의 예로 옳은 것은?", 
 "options": ["속도= {느림, 보통, 빠름}", "속도= {1,2,3}", "속도= {True, False}", "속도= {A,B,C}"], 
 "answer": 1},

{"q": "퍼지추론의 기본 구조로 옳은 것은?", 
 "options": ["입력→퍼지화→추론→역퍼지화→출력", "입력→정규화→분류→출력", "입력→추론→퍼지화→출력", "입력→비퍼지화→출력"], 
 "answer": 1},

{"q": "불확실성에서 참·거짓 대신 사용되는 것은?", 
 "options": ["믿음의 정도", "진리표", "조건식", "함의"], 
 "answer": 1},

{"q": "확률적 추론에서 명제의 진리값은 어떤 범위를 가지는가?", 
 "options": ["0~1 사이의 실수", "정수", "음수", "복소수"], 
 "answer": 1},

{"q": "상호 독립 사건 A, B의 결합 확률은?", 
 "options": ["P(A)×P(B)", "P(A)+P(B)", "P(A|B)", "P(A)/P(B)"], 
 "answer": 1},

{"q": "베이즈 정리의 기본 형태는?", 
 "options": ["P(H|E)=P(E|H)P(H)/P(E)", "P(E|H)=P(H|E)P(H)/P(E)", "P(H)=P(E)/P(E|H)", "P(E)=P(H)×P(E|H)"], 
 "answer": 1},

{"q": "특이도(Specificity)는 무엇을 의미하는가?", 
 "options": ["실제 음성 중 음성으로 맞춘 비율", "실제 양성 중 양성 비율", "예측이 참인 비율", "모델의 오류율"], 
 "answer": 1},

{"q": "정밀도(Precision)는?", 
 "options": ["예측 양성 중 실제 양성 비율", "실제 음성 중 음성 비율", "모델의 전체 정확도", "재현율과 동일"], 
 "answer": 1},

{"q": "F1 점수는 어떤 두 지표의 조화 평균인가?", 
 "options": ["정밀도와 재현율", "정확도와 특이도", "오차와 손실", "TP와 FP"], 
 "answer": 1},

{"q": "베이즈 추론의 단점으로 옳은 것은?", 
 "options": ["사전확률이 필요하다", "논리적 일관성이 없다", "데이터가 필요 없다", "결과가 항상 동일하다"], 
 "answer": 1},

{"q": "확신도(Certainty Factor)를 처음 사용한 시스템은?", 
 "options": ["MYCIN", "ELIZA", "Deep Blue", "Watson"], 
 "answer": 1},

{"q": "확신도 cf[H,E]=MB−MD에서 MB는?", 
 "options": ["믿음의 정도", "불신의 정도", "가중치", "확률"], 
 "answer": 1},

{"q": "MB=0.8, MD=0.6일 때 수정된 확신도는?", 
 "options": ["0.5", "0.2", "0.3", "0.6"], 
 "answer": 1},

{"q": "불확실한 증거에서 cf(H,e)=cf(E,e)×cf(H,E). cf(E,e)=0.6, cf(H,E)=0.8이면?", 
 "options": ["0.48", "0.14", "0.68", "0.6"], 
 "answer": 1},

{"q": "AND 연결 시 확신도 계산식은?", 
 "options": ["min(cf(E1),cf(E2))×cf(H,E)", "max(cf(E1),cf(E2))×cf(H,E)", "합×cf(H,E)", "곱/2"], 
 "answer": 1},

{"q": "OR 연결 시 확신도 계산식은?", 
 "options": ["max(cf(E1),cf(E2))×cf(H,E)", "min(cf(E1),cf(E2))×cf(H,E)", "합/2", "곱/2"], 
 "answer": 1},

{"q": "유전자 알고리즘은 어떤 원리를 모방한 것인가?", 
 "options": ["자연선택과 진화", "뉴턴역학", "양자역학", "퍼지집합"], 
 "answer": 1},

{"q": "유전자 알고리즘의 주요 연산이 아닌 것은?", 
 "options": ["선택", "교차", "돌연변이", "퍼지화"], 
 "answer": 4},

{"q": "유전자 알고리즘에서 개체의 적합도를 계산하는 함수는?", 
 "options": ["평가함수", "손실함수", "활성함수", "소속함수"], 
 "answer": 1},

{"q": "룰렛 휠 선택 방법의 핵심 원리는?", 
 "options": ["확률적 비례 선택", "무작위 균등 선택", "최대값 선택", "순차적 선택"], 
 "answer": 1},

{"q": "교차 연산의 목적은?", 
 "options": ["부모 유전자의 조합 생성", "무작위 돌연변이", "적합도 계산", "세대 초기화"], 
 "answer": 1},

{"q": "돌연변이 연산의 역할은?", 
 "options": ["탐색 다양성 유지", "적합도 최대화", "지역해 수렴 촉진", "무작위 초기화 방지"], 
 "answer": 1},

{"q": "유전자 알고리즘의 종료 조건으로 적절한 것은?", 
 "options": ["적합도가 충분히 높거나 반복 횟수 초과", "돌연변이 발생 시", "모든 유전자가 동일할 때", "난수값이 0일 때"], 
 "answer": 1},

{"q": "8-Queen 문제에서 적합도는 어떻게 정의되는가?", 
 "options": ["서로 공격하지 않는 Queen 쌍의 수", "Queen의 개수", "대각선 거리 합", "보드의 크기"], 
 "answer": 1},

{"q": "TSP 문제에서 염색체는 무엇을 나타내는가?", 
 "options": ["도시의 방문 순서", "각 도시의 거리", "적합도 값", "유전자 수"], 
 "answer": 1},

{"q": "유전자 프로그래밍(GP)은 어떤 구조를 다루는가?", 
 "options": ["트리 구조의 프로그램", "이진 벡터", "수치 행렬", "논리식"], 
 "answer": 1},

{"q": "GP가 주로 사용하는 언어로 적합한 것은?", 
 "options": ["LISP", "C", "Python", "SQL"], 
 "answer": 1},

{"q": "유전자 알고리즘의 장점으로 옳은 것은?", 
 "options": ["복잡한 최적화 문제에 적용 가능", "결정론적 결과 제공", "계산시간 일정", "데이터 필요 없음"], 
 "answer": 1},

{"q": "현대 GP의 활용 분야가 아닌 것은?", 
 "options": ["딥러닝 구조 탐색", "심볼릭 회귀", "웹 브라우징", "물리 기반 모델링"], 
 "answer": 3}
]




# =========================
# 2) 유틸: 보기 섞기 & 초기화 함수
# =========================
def shuffle_question(qobj):
    """보기를 섞고, 정답 인덱스를 재계산"""
    opts = qobj["options"]
    correct_idx_0based = qobj["answer"] - 1
    paired = list(enumerate(opts))  # (원래인덱스, 보기문자열)
    random.shuffle(paired)
    new_options = [t for _, t in paired]
    new_answer = None
    for new_i, (orig_i, _) in enumerate(paired):
        if orig_i == correct_idx_0based:
            new_answer = new_i + 1  # 1-based
            break
    return {
        "q": qobj["q"],
        "options": new_options,
        "answer": new_answer,
        "exp": qobj.get("exp", "")
    }

def init_quiz(num, shuffle_opt):
    pool = random.sample(QUESTIONS, k=num)
    if shuffle_opt:
        pool = [shuffle_question(q) for q in pool]
    st.session_state.quiz = pool
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.finished = False
    st.session_state.history = []
    st.session_state.config_num_select = num
    st.session_state.config_shuffle_opt = shuffle_opt

# =========================
# 3) 사이드바 설정 + 적용 버튼
# =========================
with st.sidebar:
    st.markdown("### 설정")
    total_pool = len(QUESTIONS)
    # 초기 기본값(세션 없을 때만 사용)
    default_num = min(20, total_pool)

    # 현재 세션에 설정값이 있으면 그걸 기본으로 보여주기
    cur_num = st.session_state.get("config_num_select", default_num)
    cur_shuffle = st.session_state.get("config_shuffle_opt", True)

    num_select = st.number_input(
        "출제 문항 수", min_value=1, max_value=total_pool, value=cur_num, step=1
    )
    shuffle_opt = st.checkbox("보기 순서 섞기", value=cur_shuffle)

    # 적용 버튼: 현재 퀴즈를 즉시 재초기화
    apply_clicked = st.button("적용(재설정)")

# =========================
# 4) 최초 실행 / 적용 처리
# =========================
# 세션에 퀴즈가 없으면 최초 초기화
if "quiz" not in st.session_state:
    init_quiz(int(num_select), bool(shuffle_opt))

# 사용자가 적용을 눌렀다면 즉시 재초기화
if apply_clicked:
    init_quiz(int(num_select), bool(shuffle_opt))
    st.rerun()

quiz = st.session_state.quiz
current = st.session_state.current
total = len(quiz)

# 진행상태 표시
st.progress((current / total) if total > 0 else 0)
st.caption(f"문항 진행: {current}/{total}")

# =========================
# 5) 퀴즈 진행
# =========================
if not st.session_state.finished:
    q = quiz[current]
    st.subheader(f"문제 {current+1} / {total}")
    st.write(q["q"])
    choice = st.radio("정답을 선택하세요:", q["options"], key=f"opt_{current}", index=0)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("제출하기", use_container_width=True):
            correct_txt = q["options"][q["answer"] - 1]
            is_correct = (choice == correct_txt)
            if is_correct:
                st.success("✅ 정답입니다!")
                st.session_state.score += 1
            else:
                st.error(f"❌ 오답! 정답은 '{correct_txt}' 입니다.")
                if q.get("exp"):
                    st.info(f"해설: {q['exp']}")

            # 기록 저장
            st.session_state.history.append({
                "q": q["q"],
                "choice": choice,
                "correct": is_correct,
                "answer": correct_txt,
                "exp": q.get("exp", "")
            })

            # 다음 문항으로
            st.session_state.current += 1
            if st.session_state.current >= total:
                st.session_state.finished = True
            st.rerun()

    with col2:
        if st.button("건너뛰기", use_container_width=True):
            st.session_state.history.append({
                "q": q["q"],
                "choice": None,
                "correct": False,
                "answer": q["options"][q["answer"] - 1],
                "exp": q.get("exp", "")
            })
            st.session_state.current += 1
            if st.session_state.current >= total:
                st.session_state.finished = True
            st.rerun()

# =========================
# 6) 결과 요약
# =========================
else:
    st.subheader("📊 결과 요약")
    score = st.session_state.score
    st.write(f"총 점수: {score} / {total} (정답률: {score/total*100:.1f}%)")
    if score == total:
        st.balloons()
        st.success("완벽합니다!")
    elif score >= total * 0.8:
        st.info("매우 우수합니다!")
    elif score >= total * 0.5:
        st.warning("절반 이상 이해했습니다. 복습을 이어가세요!")
    else:
        st.error("복습이 더 필요합니다.")

    wrong_items = [h for h in st.session_state.history if not h["correct"]]
    if wrong_items:
        st.markdown("---")
        st.subheader("📌 오답 리뷰")
        for i, h in enumerate(wrong_items, start=1):
            st.markdown(f"**{i}. {h['q']}**")
            if h["choice"] is None:
                st.write("내 선택: (건너뜀)")
            else:
                st.write(f"내 선택: {h['choice']}")
            st.write(f"정답: {h['answer']}")
            if h["exp"]:
                st.caption(f"해설: {h['exp']}")

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        if wrong_items and st.button("오답만 재도전", use_container_width=True):
            # 현재 세팅 유지한 채 오답만 다시
            wrong_q_objs = []
            for h in wrong_items:
                for q in quiz:
                    if q["q"] == h["q"]:
                        wrong_q_objs.append(q)
                        break
            random.shuffle(wrong_q_objs)
            # 보기 섞기 여부는 현재 설정 유지
            if st.session_state.get("config_shuffle_opt", True):
                wrong_q_objs = [shuffle_question(q) for q in wrong_q_objs]
            st.session_state.quiz = wrong_q_objs
            st.session_state.current = 0
            st.session_state.score = 0
            st.session_state.finished = False
            st.session_state.history = []
            st.rerun()

    with c2:
        if st.button("처음부터 다시", use_container_width=True):
            # 현재 사이드바 설정값 유지한 채 전체 재설정
            n = st.session_state.get("config_num_select", min(20, len(QUESTIONS)))
            shuf = st.session_state.get("config_shuffle_opt", True)
            init_quiz(int(n), bool(shuf))
            st.rerun()

