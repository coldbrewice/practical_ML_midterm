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

st.set_page_config(page_title="Practical ML 중간고사 대비", layout="wide")
st.title("📘 Practical ML 퀴즈 머신")

# =========================
# 1) 문제 데이터셋
#    → 여기만 네 100문항으로 교체
# =========================
QUESTIONS = [
    # 1~25: 머신러닝 기본/평가
    {"q": "머신러닝의 핵심 아이디어는 무엇인가?", "options": ["규칙 암기", "입력-출력 매핑 함수 학습", "데이터 저장", "그래픽 처리"], "answer": 2},
    {"q": "지도학습의 입력 데이터 특징은?", "options": ["라벨 없음", "라벨 있음", "시간정보만 있음", "이미지 전용"], "answer": 2},
    {"q": "비지도학습의 대표 과업은?", "options": ["분류", "군집화", "회귀", "강화학습"], "answer": 2},
    {"q": "강화학습은 무엇을 통해 학습하는가?", "options": ["보상", "정답라벨", "교사 데이터", "군집 중심"], "answer": 1},
    {"q": "Y가 연속형이면 어떤 문제인가?", "options": ["분류", "회귀", "군집화", "차원축소"], "answer": 2},
    {"q": "Y가 범주형이면 어떤 문제인가?", "options": ["회귀", "분류", "시계열", "강화학습"], "answer": 2},
    {"q": "정형 데이터의 예시는?", "options": ["스프레드시트", "자연어 텍스트", "이미지", "오디오"], "answer": 1},
    {"q": "비정형 데이터가 아닌 것은?", "options": ["이미지", "CSV 테이블", "자연어", "영상"], "answer": 2},
    {"q": "MLP의 기본 구조는?", "options": ["입력-출력", "입력-은닉-출력", "은닉-출력", "출력-입력"], "answer": 2},
    {"q": "은닉층의 주된 역할은?", "options": ["데이터 저장", "비선형 관계 학습", "라벨 생성", "정규화"], "answer": 2},
    {"q": "활성화 함수의 목적은?", "options": ["비선형성 부여", "가중치 초기화", "라벨 인코딩", "정규화"], "answer": 1},
    {"q": "손실함수는 무엇을 측정하는가?", "options": ["모델 복잡도", "오차 크기", "메모리 사용량", "데이터 크기"], "answer": 2},
    {"q": "학습/검증/테스트 분할의 주목적은?", "options": ["속도향상", "일반화 성능 평가", "라벨 정제", "시각화"], "answer": 2},
    {"q": "과적합의 전형적 징후는?", "options": ["훈련↑ 테스트↓", "훈련↓ 테스트↑", "둘 다↓", "둘 다↑"], "answer": 1},
    {"q": "언더피팅이 발생하는 이유는?", "options": ["모델 과복잡", "모델 과단순", "데이터 과다", "정규화 과소"], "answer": 2},
    {"q": "혼동행렬은 주로 어떤 모델 평가에 쓰이는가?", "options": ["회귀", "분류", "차원축소", "군집"], "answer": 2},
    {"q": "TP는 무엇을 의미하는가?", "options": ["정상→정상", "이상→이상", "이상→정상", "정상→이상"], "answer": 2},
    {"q": "TN은 무엇을 의미하는가?", "options": ["정상→정상", "이상→정상", "정상→이상", "이상→이상"], "answer": 1},
    {"q": "FP는 어떤 경우인가?", "options": ["정상을 이상으로 예측", "이상을 정상으로 예측", "정상을 정상으로 예측", "이상을 이상으로 예측"], "answer": 1},
    {"q": "FN은 어떤 경우인가?", "options": ["이상을 정상으로 예측", "정상을 이상으로 예측", "이상을 이상으로 예측", "정상을 정상으로 예측"], "answer": 1},
    {"q": "Accuracy가 부적절할 수 있는 상황은?", "options": ["클래스 균형", "클래스 불균형 심함", "피처가 적음", "라벨이 없음"], "answer": 2},
    {"q": "Precision의 정의는?", "options": ["실제 양성 중 맞춘 비율", "예측 양성 중 실제 양성 비율", "실제 음성 중 맞춘 비율", "전체 정확도"], "answer": 2},
    {"q": "Recall의 정의는?", "options": ["예측 양성 중 실제 양성", "실제 양성 중 맞춘 비율", "정확도", "오차율"], "answer": 2},
    {"q": "F1-score는 어떤 평균인가?", "options": ["산술평균", "조화평균", "기하평균", "가중평균"], "answer": 2},
    {"q": "불균형 상황에서 더 유용한 곡선은?", "options": ["ROC", "PR 커브", "히스토그램", "QQ-plot"], "answer": 2},

    # 26~50: 불균형 개념/언더샘플링
    {"q": "데이터 불균형의 정의는?", "options": ["클래스 표본 수가 비슷함", "한 클래스 표본이 매우 적음", "라벨이 없음", "결측이 많음"], "answer": 2},
    {"q": "소수 클래스(minority class)는?", "options": ["표본이 많은 클래스", "표본이 적은 클래스", "항상 정상 클래스", "항상 이상 클래스"], "answer": 2},
    {"q": "다수 클래스(majority class)는?", "options": ["표본이 많은 클래스", "표본이 적은 클래스", "항상 이상 클래스", "항상 정상 클래스"], "answer": 1},
    {"q": "불균형에서 Accuracy가 왜 위험한가?", "options": ["항상 낮음", "소수 클래스를 무시해도 높을 수 있음", "정의 불가", "계산 복잡"], "answer": 2},
    {"q": "불균형 대응의 데이터 수준 접근은?", "options": ["샘플링", "로스 변경", "모델 구조 변경", "최적화 변경"], "answer": 1},
    {"q": "모델 수준 접근의 예는?", "options": ["Cost-sensitive 학습", "샘플링", "정규화", "스케일링"], "answer": 1},
    {"q": "언더샘플링의 핵심은?", "options": ["소수 클래스 증가", "다수 클래스 감소", "라벨 제거", "특징 삭제"], "answer": 2},
    {"q": "오버샘플링의 핵심은?", "options": ["다수 클래스 감소", "소수 클래스 증가", "결측치 제거", "정규화"], "answer": 2},
    {"q": "언더샘플링의 장점은?", "options": ["계산량 감소", "정보 손실 없음", "항상 정확도↑", "노이즈 제거 보장"], "answer": 1},
    {"q": "언더샘플링의 단점은?", "options": ["정보 손실 위험", "과적합 증가", "데이터 폭증", "학습 불가"], "answer": 1},
    {"q": "Random Undersampling은 무엇을 제거하는가?", "options": ["소수 클래스", "다수 클래스 일부", "라벨", "결측치"], "answer": 2},
    {"q": "Tomek Links의 목적은?", "options": ["경계 근처 다수 클래스 제거", "소수 복제", "라벨 정정", "결측 대체"], "answer": 1},
    {"q": "Tomek Links가 집중하는 영역은?", "options": ["클래스 중심", "클래스 경계", "무작위", "고밀도 영역"], "answer": 2},
    {"q": "CNN(Condensed NN) 규칙은 어떤 샘플을 제거하는가?", "options": ["1-NN으로 잘 분류되는 샘플", "무작위 샘플", "소수 클래스만", "결측 행"], "answer": 1},
    {"q": "One-Sided Selection(OSS)은 무엇의 결합인가?", "options": ["Tomek Links + CNN", "SMOTE + ADASYN", "LOF + DBSCAN", "SVM + PCA"], "answer": 1},
    {"q": "언더샘플링 시 특히 주의해야 할 것은?", "options": ["다수 정보 손실", "소수 정보 손실", "라벨 손상", "스케일 손실"], "answer": 1},
    {"q": "언더샘플링의 목표는?", "options": ["클래스 비율 균형", "라벨 생성", "피처 감소", "정규화"], "answer": 1},
    {"q": "언더샘플링 후 기대 효과가 아닌 것은?", "options": ["학습 속도 향상", "경계 명확화 가능", "데이터 증가", "불균형 완화"], "answer": 3},
    {"q": "불균형 시 주로 강조하는 지표는?", "options": ["Recall/F1", "RMSE", "MAPE", "R²"], "answer": 1},
    {"q": "소수 클래스 검출력이 중요한 경우 중시할 지표는?", "options": ["Precision만", "Recall", "MAE", "AUC만"], "answer": 2},
    {"q": "언더샘플링이 특히 위험한 데이터 상황은?", "options": ["표본이 매우 적음", "표본이 매우 많음", "클래스 균형", "결측 없음"], "answer": 1},
    {"q": "언더/오버샘플링의 공통 목적은?", "options": ["결측 제거", "클래스 비율 개선", "정규화", "라벨링"], "answer": 2},
    {"q": "OSS의 기대 효과는?", "options": ["경계 정제", "소수 복제", "라벨 제거", "차원축소"], "answer": 1},
    {"q": "Tomek Links는 주로 어떤 오류를 줄이는가?", "options": ["과소적합", "경계혼합으로 인한 분류 오류", "라벨오류", "결측치 오류"], "answer": 2},
    {"q": "언더샘플링 선택 기준으로 적절한 것은?", "options": ["무작위만", "경계정보/1-NN 등 규칙 기반", "라벨삭제", "정규화만"], "answer": 2},

    # 51~75: 오버샘플링 (Resampling/SMOTE/Borderline/ADASYN)
    {"q": "Random Oversampling의 방법은?", "options": ["소수 복제", "다수 삭제", "경계 제거", "라벨 재배열"], "answer": 1},
    {"q": "Random Oversampling의 단점은?", "options": ["과적합 위험", "정보 손실", "속도 저하 없음", "경계 악화"], "answer": 1},
    {"q": "SMOTE의 핵심 아이디어는?", "options": ["보간으로 가상 샘플 생성", "복제", "경계 샘플 삭제", "클러스터 평균 생성"], "answer": 1},
    {"q": "SMOTE에서 새 샘플은 어디에 위치하는가?", "options": ["원점", "두 소수 이웃 사이 선분 상", "다수 중심", "무작위"], "answer": 2},
    {"q": "SMOTE에서 k는 무엇을 의미하는가?", "options": ["이웃 수", "클래스 수", "배치 크기", "특징 수"], "answer": 1},
    {"q": "SMOTE의 기대 효과는?", "options": ["경계 개선", "속도 저하", "정보 손실", "라벨 변경"], "answer": 1},
    {"q": "Borderline-SMOTE가 집중하는 영역은?", "options": ["안전영역", "경계 인근", "무작위", "다수 중심"], "answer": 2},
    {"q": "Borderline-SMOTE의 장점은?", "options": ["결정경계 학습 강화", "데이터 축소", "라벨 정규화", "정확도 하락"], "answer": 1},
    {"q": "Borderline-SMOTE에서 ‘Danger’ 샘플은?", "options": ["주변이 대부분 다수 클래스", "완전 안전", "노이즈 확정", "다수 중심"], "answer": 1},
    {"q": "ADASYN의 철학은?", "options": ["균일 생성", "난이도 가중 생성", "다수 축소", "라벨 변경"], "answer": 2},
    {"q": "ADASYN의 r_i는 무엇을 뜻하는가?", "options": ["분산", "주변 다수 비율", "거리합", "정확도"], "answer": 2},
    {"q": "ADASYN은 어느 영역에 더 많이 생성하는가?", "options": ["안전영역", "경계/어려운 영역", "무작위", "중심영역"], "answer": 2},
    {"q": "SMOTE와 ADASYN의 공통점은?", "options": ["가상샘플 생성 기반", "다수 축소", "라벨 정정", "차원축소"], "answer": 1},
    {"q": "오버샘플링의 장점은?", "options": ["정보 보존", "데이터 축소", "항상 과적합 감소", "라벨 정제"], "answer": 1},
    {"q": "오버샘플링의 단점은?", "options": ["과적합/계산 증가", "정보 손실", "라벨 손상", "항상 정확도↓"], "answer": 1},
    {"q": "Random Oversampling 대비 SMOTE의 이점은?", "options": ["복제 최소화로 과적합 완화", "속도 향상", "결측 제거", "클래스 축소"], "answer": 1},
    {"q": "Borderline-SMOTE의 적용 목적은?", "options": ["경계에서 분류 성능 향상", "라벨 변경", "결측 대체", "피처 선택"], "answer": 1},
    {"q": "SMOTE의 생성 수를 조절하는 주 요소는?", "options": ["샘플 가중치", "이웃 수와 증강 비율", "배치 크기", "러닝레이트"], "answer": 2},
    {"q": "오버샘플링 시 민감한 데이터 유형은?", "options": ["노이즈/이상치 포함 데이터", "완전 정규 데이터", "정형 테이블 없음", "라벨 없는 데이터"], "answer": 1},
    {"q": "SMOTE가 잘 작동하기 어려운 상황은?", "options": ["선형 경계", "복잡한 다중 모드 경계/노이즈", "클래스 균형", "표본 많음"], "answer": 2},
    {"q": "ADASYN의 총 생성량 G 분배 기준은?", "options": ["균등", "정규분포", "정규화된 r_i 비율", "무작위"], "answer": 3},
    {"q": "오버샘플링 후 평가 시 주로 확인할 요소는?", "options": ["Recall/F1 변화", "RMSE", "AIC", "BIC"], "answer": 1},
    {"q": "경계 근처에서 소수 샘플을 더 생성하는 이유는?", "options": ["정확도 감소 유도", "결정경계 학습 강화", "피처 수 증가", "속도 개선"], "answer": 2},
    {"q": "오버샘플링 적용 순서는 보통?", "options": ["학습 후 적용", "학습 전 훈련 데이터에만 적용", "테스트에도 동일 적용", "배포 단계 적용"], "answer": 2},
    {"q": "샘플링 전처리의 공통 목표는?", "options": ["모델 일반화 향상", "모델 복잡화", "라벨 변경", "피처 제거"], "answer": 1},

    # 76~101: 이상탐지(24p까지: 개념/확률기반/거리기반)
    {"q": "이상탐지의 목적은?", "options": ["정상 패턴 강화", "비정상 패턴 탐지", "라벨링", "정규화"], "answer": 2},
    {"q": "Outlier와 Noise의 구분으로 옳은 것은?", "options": ["동일 개념", "Noise는 무작위 오차, Outlier는 생성 메커니즘 이탈", "Outlier=오류 데이터만", "Noise=항상 이상"], "answer": 2},
    {"q": "Global/Contextual/Collective는 무엇의 유형인가?", "options": ["샘플링 방법", "이상치 유형", "평가 지표", "손실함수"], "answer": 2},
    {"q": "Contextual Outlier의 예시는?", "options": ["전체 분포에서 벗어남", "특정 맥락(예: 계절)에서만 비정상", "집합 패턴 이상", "노이즈"], "answer": 2},
    {"q": "Collective Outlier는?", "options": ["단일 점 이상", "여러 점이 함께 비정상 패턴", "노이즈", "라벨 오류"], "answer": 2},
    {"q": "확률밀도 기반 이상탐지의 원리는?", "options": ["거리 최솟값", "밀도가 낮으면 이상", "라벨 빈도", "회귀선과 거리"], "answer": 2},
    {"q": "정상 데이터만으로 분포를 추정한 뒤 p(x) 임계값으로 판단하는 방식은?", "options": ["지도학습", "준지도/비지도 방식", "강화학습", "클러스터만"], "answer": 2},
    {"q": "단변량 정규분포 기준 이상 판단에 흔히 쓰는 값은?", "options": ["평균±3σ", "평균±0.5σ", "평균±0.1σ", "평균±10σ"], "answer": 1},
    {"q": "z-score가 큰 양수/음수이면 보통 무엇을 의미하는가?", "options": ["중앙값 근처", "평균 근처", "이상 가능성 증가", "항상 정상"], "answer": 3},
    {"q": "다변량에서 스케일/상관을 고려한 거리는?", "options": ["유클리드", "맨해튼", "마할라노비스", "코사인"], "answer": 3},
    {"q": "Mahalanobis 거리 계산에 필요한 행렬은?", "options": ["상관행렬 역행렬", "공분산행렬 역행렬", "단위행렬", "영행렬"], "answer": 2},
    {"q": "임계값 α=0.05의 일반적 해석은?", "options": ["상위 5% 이상치", "하위 5%를 이상으로 간주", "50% 이상치", "임계값 미사용"], "answer": 2},
    {"q": "정상 분포 추정 시 무엇을 먼저 구하는가?", "options": ["평균과 분산(또는 공분산)", "중앙값만", "최빈값만", "사분위수만"], "answer": 1},
    {"q": "밀도기반 접근에서 로그우도(log-likelihood)를 쓰는 이유는?", "options": ["값을 키우기 위해", "수치 안정성/곱을 합으로 변환", "라벨 생성", "정규화"], "answer": 2},
    {"q": "거리기반 이상탐지의 핵심은?", "options": ["밀도추정", "근접도/거리 임계", "라벨빈도", "회귀계수"], "answer": 2},
    {"q": "k-NN 거리기반 이상도에서 k를 크게 하면?", "options": ["지역성 감소", "지역성 증가", "항상 정확도↑", "라벨 필요"], "answer": 1},
    {"q": "이상탐지에서 임계값 설정이 너무 엄격하면?", "options": ["거짓양성↑", "거짓음성↑", "정확도 항상↑", "변동성↓"], "answer": 2},
    {"q": "임계값 설정이 너무 느슨하면?", "options": ["거짓양성↑", "거짓음성↑", "둘 다 0", "영향 없음"], "answer": 1},
    {"q": "Context를 반영하지 않으면 생길 수 있는 문제는?", "options": ["Global만 탐지", "맥락적 이상 탐지 실패", "Collective만 탐지", "정상만 표기"], "answer": 2},
    {"q": "이상탐지에서 정상 데이터만 풍부할 때 적합한 설정은?", "options": ["이진 지도학습", "일류(one-class) 기반", "강화학습", "전처리만"], "answer": 2},
    {"q": "확률 기반/거리 기반 공통의 중요한 요소는?", "options": ["라벨 품질", "임계값/문턱값 설정", "배치 크기", "학습률"], "answer": 2},
    {"q": "밀도기반 방식의 장점은?", "options": ["분포 형태를 반영 가능", "라벨 불필요 없음", "항상 선형", "차원 영향 無"], "answer": 1},
    {"q": "거리기반 방식의 단점은?", "options": ["스케일/상관 민감", "분포 반영", "라벨 필요", "항상 최적"], "answer": 1},
    {"q": "마할라노비스 거리를 사용하면 개선되는 점은?", "options": ["상관/스케일 반영", "라벨 생성", "속도 항상↑", "임계 자동"], "answer": 1},
    {"q": "이상탐지 파이프라인에서 마지막 단계는?", "options": ["특징학습", "임계 적용 및 이상 판정", "스케일링", "라벨링"], "answer": 2}
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
