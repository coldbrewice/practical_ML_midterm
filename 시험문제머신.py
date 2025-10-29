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
# ===== 제05장 지식표현 (30문항) =====
{"q":"데이터→정보→지식→지혜의 관계를 가장 올바르게 나타낸 것은?", "options":["데이터→정보→지식→지혜","정보→데이터→지식→지혜","지식→정보→데이터→지혜","데이터→지식→정보→지혜"], "answer":1},
{"q":"의미망(semantic network)의 기본 구성 요소는?", "options":["노드와 간선","조건과 결론","객체와 속성","패턴과 규칙"], "answer":1},
{"q":"의미망에서 is-a 관계의 특징으로 옳은 것은?", "options":["상위 속성 상속","비추이적 관계","부분-전체 관계","시간 관계"], "answer":1},
{"q":"의미망에서 has-a는 무엇을 의미하는가?", "options":["전체-부분 관계","클래스-인스턴스","상속","동치"], "answer":1},
{"q":"프레임(frame)을 제안한 사람은?", "options":["Marvin Minsky","Lotfi Zadeh","Gottlob Frege","Tim Berners-Lee"], "answer":1},
{"q":"프레임에서 속성을 담는 요소는?", "options":["슬롯(slot)","노드(node)","리터럴(literal)","절(clause)"], "answer":1},
{"q":"프레임 슬롯에 부가 정보를 붙이는 요소는?", "options":["패싯(facet)","데몬(demon)","메소드(method)","트리플"], "answer":1},
{"q":"프레임의 if-needed 데몬은 언제 실행되는가?", "options":["슬롯 값을 사용할 때","값이 추가될 때","값이 삭제될 때","프레임 로드 시"], "answer":1},
{"q":"프레임의 class/instance 관계에서 하위 프레임이 상속받는 것은?", "options":["상위 슬롯과 기본값","하위의 전용 메소드","외부 함수","이벤트 큐"], "answer":1},
{"q":"의미망→프레임 변환 시 간선은 보통 무엇이 되는가?", "options":["슬롯","노드","데몬","패싯"], "answer":1},
{"q":"시맨틱 웹의 목표는?", "options":["기계가 의미를 이해하고 추론","네트워크 속도 향상","이미지 압축 향상","UI 일관성 개선"], "answer":1},
{"q":"시맨틱 웹 핵심 기술이 아닌 것은?", "options":["RDF","OWL","SPARQL","SMOTE"], "answer":4},
{"q":"명제(proposition)의 정의는?", "options":["참/거짓 판별 가능한 문장","주어-술어 구조","객체의 속성","추론 규칙"], "answer":1},
{"q":"명제논리에서 리터럴(literal)이란?", "options":["명제기호 혹은 그 부정","명제기호의 집합","절의 집합","CNF 전체"], "answer":1},
{"q":"CNF(논리곱 정규형)의 구조는?", "options":["논리합 절들의 논리곱","논리곱 절들의 논리합","단일 리터럴","항진식의 모음"], "answer":1},
{"q":"타당한 논리식(항진식)의 정의는?", "options":["모든 모델에서 참","일부 모델에서 참","모든 모델에서 거짓","해석 불가"], "answer":1},
{"q":"모더스 포넌스의 형식은?", "options":["A→B, A ⊢ B","A→B, ¬B ⊢ ¬A","A→B, B→C ⊢ A→C","A∨B, ¬A ⊢ A"], "answer":1},
{"q":"부정 논법(Modus Tollens)의 형식은?", "options":["A→B, ¬B ⊢ ¬A","A→B, A ⊢ B","A∨B, ¬A ⊢ B","A∧B ⊢ A∨B"], "answer":1},
{"q":"삼단논법(syllogism)의 전형적 형태는?", "options":["A→B, B→C ⊢ A→C","A→B, A ⊢ B","A∨B, ¬A ⊢ B","A∧B ⊢ A"], "answer":1},
{"q":"논리융합(resolution)이 다루는 것은?", "options":["상반 리터럴 제거해 새 절 생성","명제기호 수 줄이기","진리표 최소화","모형 이론 증명"], "answer":1},
{"q":"논리적 귀결 Δ⊨ω의 의미는?", "options":["Δ의 모든 모델에서 ω도 참","Δ가 거짓이면 ω가 참","ω가 Δ를 포함","Δ와 ω가 동치"], "answer":1},
{"q":"임의의 wff를 CNF로 바꾸는 이유는?", "options":["논리융합 적용을 위해","진리표 작성을 위해","모델 수 감소","항진식 검출"], "answer":1},
{"q":"다음 중 항위식(항상 거짓) 예시는?", "options":["P∧¬P","P∨¬P","(P→Q)∨P","P∨P"], "answer":1},
{"q":"다음 중 항진식 예시는?", "options":["P∨¬P","P∧¬P","P","¬P"], "answer":1},
{"q":"‘소크라테스는 사람이다, 사람은 죽는다’에서 결론은?", "options":["소크라테스는 죽는다","소크라테스는 불멸이다","사람은 불멸이다","결론 없음"], "answer":1},
{"q":"논리융합 반박(resolution refutation)의 핵심 절차는?", "options":["목표의 부정을 추가해 모순 유도","모든 명제를 나열","진리표 완전 탐색","휴리스틱 선택"], "answer":1},
{"q":"CNF 변환 순서 중 옳지 않은 것은?", "options":["함의 제거","이중부정 제거","변수표준화","전체한정사 추가"], "answer":4},
{"q":"정리증명에서 공리란?", "options":["참으로 주어지는 논리식","추론 결과식","항진식","무관식"], "answer":1},
{"q":"Prolog의 기본 절 형태에 해당하는 것은?", "options":["Horn 절","CNF 절만","DNF 절만","양화 논리만"], "answer":1},
{"q":"Prolog에서 백트래킹의 목적은?", "options":["해 탐색의 후퇴/대안 탐색","데이터 정렬","메모리 해제","동시성 제어"], "answer":1},

# ===== 제06장 퍼지논리 (20문항) =====
{"q":"퍼지논리를 처음 제안한 학자는?", "options":["Zadeh","Minsky","Frege","Shannon"], "answer":1},
{"q":"퍼지집합에서 소속함수 μ(x)는 무엇을 의미하는가?", "options":["집합에 속하는 정도","확률밀도","빈도수","오류율"], "answer":1},
{"q":"크리스프 집합과 퍼지집합의 가장 큰 차이는?", "options":["경계의 모호성 허용","원소 개수","정렬 가능성","집합 연산 부재"], "answer":1},
{"q":"퍼지집합의 교집합은 어떤 연산으로 계산하는가?", "options":["min","max","1-μ","곱"], "answer":1},
{"q":"퍼지집합의 합집합은 어떤 연산으로 계산하는가?", "options":["max","min","1-μ","곱"], "answer":1},
{"q":"퍼지집합의 여집합은 어떤 연산으로 계산하는가?", "options":["1-μ","μ1+μ2","min","max"], "answer":1},
{"q":"퍼지언어변수의 예로 적절한 것은?", "options":["온도={낮음,보통,높음}","온도={10,20,30}","온도={True,False}","온도={A,B,C}"], "answer":1},
{"q":"퍼지추론 단계의 올바른 순서는?", "options":["퍼지화→규칙적용→집계→역퍼지화","역퍼지화→퍼지화→집계→규칙","집계→규칙→퍼지화→역퍼지화","퍼지화→역퍼지화→규칙→집계"], "answer":1},
{"q":"max-min 퍼지추론에서 전제부 집계(OR)는 보통 무엇을 쓰는가?", "options":["max","min","곱","합"], "answer":1},
{"q":"max-min 퍼지추론에서 함축(THEN) 처리에 쓰이는 연산은?", "options":["min","max","곱","합"], "answer":1},
{"q":"여러 규칙 결과를 합성할 때(OR) 흔히 쓰는 연산은?", "options":["max","min","곱","나눗셈"], "answer":1},
{"q":"역퍼지화(defuzzification)에서 중심점(Centroid)법의 개념은?", "options":["DOM과 x의 가중평균","최대 DOM의 평균","최소값의 평균","중앙값 선택"], "answer":1},
{"q":"MOM(Mean of Maxima) 방식의 단점은?", "options":["최대부 외 정보 무시","계산량 과다","불연속만 처리","확률 필요"], "answer":1},
{"q":"삼각형 멤버십 함수의 대표값은 보통?", "options":["중간 꼭짓점 x","좌측 기울기","우측 기울기","기저 길이"], "answer":1},
{"q":"입력 온도=‘약간 높다’(0.6), 규칙: IF 온도 높음 THEN 팬 빠르게(0.8). 출력 확신도는?", "options":["0.48","0.14","0.68","0.6"], "answer":1},
{"q":"두 전제 AND의 전제 확신도가 0.7, 0.5이고 규칙 cf=0.9일 때 출력 확신도는?", "options":["min(0.7,0.5)×0.9=0.45","(0.7+0.5)/2×0.9=0.54","0.7×0.5×0.9=0.315","max×0.9=0.63"], "answer":1},
{"q":"두 전제 OR의 전제 확신도가 0.4, 0.8이고 규칙 cf=0.6일 때 출력 확신도는?", "options":["max(0.4,0.8)×0.6=0.48","min×0.6=0.24","평균×0.6=0.36","곱×0.6=0.192"], "answer":1},
{"q":"퍼지제어가 유리한 분야는?", "options":["모호한 언어 규칙 활용","정확한 미분방정식 필요","완전 결정론적 시스템","정수계획 전용"], "answer":1},
{"q":"퍼지논리는 ‘애매한 논리’가 아니라는 설명의 요지는?", "options":["모호함을 질서정연하게 다룬다","확률만 사용한다","수학적 근거 없다","블랙박스"], "answer":1},
{"q":"퍼지 집합 예: ‘키 큰 사람’={0.3/170, 0.6/178, 1.0/190}. 178의 소속도는?", "options":["0.6","0.3","1.0","0.0"], "answer":1},

# ===== 제07장 불확실성 (25문항) =====
{"q":"현실에서 불확실성이 발생하는 이유로 보기 어려운 것은?", "options":["완전한 측정","센서오차","지식 불완전성","전문가 의견 차이"], "answer":1},
{"q":"확률적 추론에서 명제의 값 범위는?", "options":["0~1 실수","정수","음수","복소"], "answer":1},
{"q":"상호 독립 사건 A,B의 결합확률은?", "options":["P(A)P(B)","P(A)+P(B)","P(A|B)","P(A)/P(B)"], "answer":1},
{"q":"조건부 확률 P(A|B)의 정의는?", "options":["B가 주어졌을 때 A의 확률","A와 B의 합","A만의 확률","B만의 확률"], "answer":1},
{"q":"베이즈 정리 기본식은?", "options":["P(H|E)=P(E|H)P(H)/P(E)","P(E|H)=P(H|E)/P(H)","P(H)=P(E|H)/P(E)","P(E)=P(H|E)/P(H)"], "answer":1},
{"q":"특이도(Specificity)는?", "options":["실제 음성 중 음성으로 맞춤","실제 양성 중 양성으로 맞춤","예측 양성 중 실제 양성","재현율"], "answer":1},
{"q":"정밀도(Precision)는?", "options":["예측 양성 중 실제 양성 비율","실제 음성 중 음성 비율","전체 정확도","특이도와 동일"], "answer":1},
{"q":"재현율(Recall, 민감도)은?", "options":["실제 양성 중 양성으로 맞춤","예측 양성 중 실제 양성","실제 음성 중 음성","오분류율"], "answer":1},
{"q":"F1 점수는 무엇의 조화평균인가?", "options":["정밀도와 재현율","정확도와 특이도","TP와 FP","민감도와 특이도"], "answer":1},
{"q":"사전확률이 0.1, P(양성|질병)=0.9, P(양성|비질병)=0.3일 때 양성 결과의 질병 사후확률은?", "options":["0.25","0.5","0.75","0.9"], "answer":1},
{"q":"바나나 선택 문제: 그릇1(사과10,바나나30), 그릇2(사과20,바나나20), 그릇 무작위 선택. 바나나가 나왔을 때 그릇1일 확률은?", "options":["(0.5×30/40)/(0.5×30/40+0.5×20/40)=0.6","0.5","0.4","0.3"], "answer":1},
{"q":"두 항아리: 1번(빨강50,파랑50), 2번(빨강30,파랑70). 빨강이 나왔다면 1번 항아리일 확률은?", "options":["(0.5×0.5)/(0.5×0.5+0.5×0.3)=5/8","1/2","3/5","5/6"], "answer":1},
{"q":"스팸필터: P(spam)=0.4, P(word|spam)=0.01, P(word|¬spam)=0.004. 제목에 word가 있을 때 스팸일 확률은?", "options":["(0.01×0.4)/(0.01×0.4+0.004×0.6)≈0.625","0.4","0.5","0.25"], "answer":1},
{"q":"경기침체 모델: P(recession)=0.2, 민감도 0.8, 위양성 0.1. 모델이 침체라고 할 때 실제 침체 확률은?", "options":["(0.8×0.2)/(0.8×0.2+0.1×0.8)=2/3","1/2","0.8","0.2"], "answer":1},
{"q":"몬티홀 문제에서 전략적으로 유리한 선택은?", "options":["바꾼다","유지한다","무관하다","동전 던진다"], "answer":1},
{"q":"베이즈 추론의 한계는?", "options":["사전확률 요구","검정 불가능","모순 발생","모델 없음"], "answer":1},
{"q":"확신도(CF)를 도입한 시스템은?", "options":["MYCIN","ELIZA","Watson","AlphaGo"], "answer":1},
{"q":"CF 기본식 cf[H,E]=MB−MD에서 MB 의미는?", "options":["믿음의 정도","불신의 정도","오차","확률밀도"], "answer":1},
{"q":"MB=0.8, MD=0.6일 때 수정식 cf=(MB−MD)/(1−min(MB,MD))의 값은?", "options":["0.5","0.2","0.3","0.6"], "answer":1},
{"q":"불확실한 증거 cf(E,e)=0.6, 규칙 cf(H,E)=0.8. cf(H,e)는?", "options":["0.48","0.14","0.68","0.6"], "answer":1},
{"q":"AND 전제 cf가 0.7, 0.5이고 규칙 cf=0.9이면 최종 cf는?", "options":["0.45","0.63","0.315","0.54"], "answer":1},
{"q":"OR 전제 cf가 0.4, 0.8이고 규칙 cf=0.6이면 최종 cf는?", "options":["0.48","0.24","0.36","0.192"], "answer":1},
{"q":"혼동행렬에서 특이도는 수식으로?", "options":["TN/(TN+FP)","TP/(TP+FN)","TP/(TP+FP)","(TP+TN)/(전체)"], "answer":1},
{"q":"혼동행렬에서 정밀도의 수식은?", "options":["TP/(TP+FP)","TN/(TN+FP)","TP/(TP+FN)","(TP+TN)/전체"], "answer":1},
{"q":"불확실성 처리의 목표에 가장 가까운 설명은?", "options":["불완전 정보에서도 합리적 의사결정","항상 100% 정확","추론 제거","결정적 규칙만 사용"], "answer":1},

# ===== 제08장 유전자 알고리즘 (25문항) =====
{"q":"유전자 알고리즘(GA)은 무엇을 모방했는가?", "options":["자연선택과 진화","뉴턴역학","푸리에해석","퍼지집합"], "answer":1},
{"q":"GA의 핵심 연산 3가지는?", "options":["선택, 교차, 돌연변이","추출, 분류, 회귀","정렬, 탐색, 해시","수집, 평균, 필터"], "answer":1},
{"q":"적합도(fitness)를 반환하는 함수는?", "options":["평가함수","활성함수","손실함수","소속함수"], "answer":1},
{"q":"룰렛 휠 선택의 원리는?", "options":["적합도 비례 확률 선택","무작위 균등 선택","최대값만 선택","최소값만 선택"], "answer":1},
{"q":"교차(crossover)의 목적은?", "options":["부모 유전 정보 재조합","새 개체 무작위 생성","적합도 측정","돌연변이 방지"], "answer":1},
{"q":"돌연변이(mutation)의 주요 효과는?", "options":["탐색 다양성 유지/국소해 탈출","적합도 고정","교차 억제","조기수렴 유도"], "answer":1},
{"q":"GA의 종료 조건으로 적절한 것은?", "options":["목표 적합도 도달 또는 반복 제한","난수=0 발생","모든 유전자 동일","세대=1"], "answer":1},
{"q":"0~31 5비트 이진 염색체에서 ‘11111’의 십진값은?", "options":["31","15","30","32"], "answer":1},
{"q":"교차확률 0.7, 돌연변이확률 0.001로 자주 설정하는 이유는?", "options":["재조합 중심+소량 탐색 유지","완전 무작위화","탐색 중단","수렴 보장"], "answer":1},
{"q":"지역최대점(local optimum) 탈출을 돕는 연산은?", "options":["돌연변이","선택","평가","정규화"], "answer":1},
{"q":"8-Queen 적합도 설계로 적절한 것은?", "options":["서로 공격하지 않는 쌍의 수","퀸 총합","대각선 길이합","보드 면적"], "answer":1},
{"q":"TSP에서 염색체는 보통 무엇을 나타내는가?", "options":["도시 방문 순열","거리 행렬","적합도 벡터","확률벡터"], "answer":1},
{"q":"유전자 프로그래밍(GP)의 표현은?", "options":["트리 구조 프로그램","이진 벡터","스칼라","인접행렬"], "answer":1},
{"q":"GP와 잘 맞는 언어는?", "options":["LISP","C","SQL","HTML"], "answer":1},
{"q":"선택 연산의 부작용으로 과도한 조기수렴을 막으려면?", "options":["엘리티즘+다양성 유지","선택 확률=0","교차 제거","평가함수 폐기"], "answer":1},
{"q":"다음 중 GA에 대한 서술로 옳지 않은 것은?", "options":["결정론적 최적 보장","확률적 탐색","전역 탐색 경향","휴리스틱과 결합 가능"], "answer":1},
{"q":"이진 인코딩에서 한 유전자의 값은?", "options":["0 또는 1","실수","문자열","행렬"], "answer":1},
{"q":"룰렛 휠에서 적합도가 0인 개체의 선택 확률은?", "options":["0","0.5","1/N","1"], "answer":1},
{"q":"세대 교체 후 보통 수행하는 단계는?", "options":["돌연변이 및 평가","역전파","규칙학습","퍼지화"], "answer":1},
{"q":"교차 지점 한 곳에서 절단/교환하는 방식은?", "options":["단일지점 교차","균일 교차","부분일치 교차","순서 교차"], "answer":1},
{"q":"정수 인코딩 TSP에서 순서 보존을 위한 교차는?", "options":["순서교차(OX) 등","단일지점 이진교차","균일교차만","비트반전"], "answer":1},
{"q":"적합도 스케일링을 하는 이유는?", "options":["선택 압력 조절","돌연변이 확률 증가","교차 확률 0으로","평가 제거"], "answer":1},
{"q":"엘리티즘(elitism)의 목적은?", "options":["최고 개체 보존","다양성 제거","무작위 초기화","평가 생략"], "answer":1},
{"q":"함수 최대화에서 적합도로 f(x)=6x−x^2를 쓴다면, x∈{0,…,31}의 최댓값은 대략 어느 근처인가?", "options":["x≈3 근방(정수화)","x≈6","x≈0","x≈31"], "answer":1},
{"q":"현대 GP의 활용으로 보기 어려운 것은?", "options":["웹 브라우징 자동화 일반해","심볼릭 회귀","신경망 구조 탐색","물리 기반 식 도출"], "answer":1}
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


