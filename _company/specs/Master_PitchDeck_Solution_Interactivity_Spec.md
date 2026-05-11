# 📐 Master Pitch Deck: Solution Section (Interactive Spec)
**목표:** Z Risk 진단 $\rightarrow$ OPRF 적용 $\rightarrow$ 위험 회피 가치($\Delta Z$) 발견의 과정을 극적으로 시뮬레이션하여, 청중에게 '재무적 깨달음(Financial Aha Moment)'을 제공한다.
**타깃 환경:** Figma/Keynote 인터랙티브 프로토타이핑 (개발자 테스트 기준)
**핵심 원칙:** 모든 변화는 *데이터*에 의해 트리거되어야 한다.

---

## 💡 I. 시뮬레이션 플로우 및 데이터 흐름 정의

| 단계 | 사용자 액션 (Trigger) | 백엔드 연동 로직 (Developer Input) | 비주얼 상태 변화 (Designer Output) |
| :--- | :--- | :--- | :--- |
| **1. 문제 제기** (Initial State) | 1. 산업군 선택 ($\text{V}_{industry}$) <br>2. 기간 설정 ($\text{V}_{period}$) <br>3. 변수 입력 (예: 규제 준수 노력 $\text{V}_{effort}$) | **`services/risk_engine.py`** 호출 및 초기 $Z_{initial}$ 값 반환. | 전체 화면이 어둡고, 경고성(Warning)의 붉은 계열 톤을 지배적으로 사용한다. $|$
| **2. 위험 증폭 (Red Alert)** | *사용자가 $\text{V}_{effort}$를 낮추거나* 임계치 초과 변수 입력 시. | `RiskEngineCore`가 계산한 $Z_{current} > \text{RED\_ALERT\_THRESHOLD}$ 조건 만족 시, 강제로 $Z$ 값을 증폭(Exaggerate)하여 반환. | **Red Alert Trigger:** 전체 화면의 붉은색 오버레이 증가. Z-Gauge 수치가 폭발하듯 상승하는 애니메이션 필수. (Fear/Anxiety 극대화). |
| **3. 솔루션 적용 (Intervention)** | *'OPRF 시뮬레이터 실행'* 버튼 클릭. (강제 전환) | `RiskEngineCore`가 OPRF 모델을 통해 위험 감소분($\Delta Z$) 계산 및 $Z_{final}$ 반환. | 화면 중앙에 'Solution Applied' 모듈 활성화. 애니메이션 시작 지점. **(핵심 구간)** |
| **4. 결과 제시 (Relief/Aha Moment)** | - (자동 전환) | $Z_{initial} \rightarrow Z_{final}$ 비교 데이터와 $\Delta Z$ 값 출력. | **Green Relief:** 붉은색 오버레이가 부드럽게 녹색으로 변환(Color Shift Animation). Z-Gauge 수치가 급격히 하강하는 애니메이션 필수. (Relief/안도감 극대화). |

---

## ✨ II. 핵심 상호작용 요소 상세 스펙 (Interaction & Animation Specs)

### 1. Z-Risk Gauge 컴포넌트 ($\text{Z}_{Gauge}$)
*   **데이터 바인딩:** 현재 계산된 $Z$ 값을 실시간으로 표시해야 하며, 이 값이 모든 시각적 변화의 *단 하나의 진실 공급원(Single Source of Truth)*이 되어야 함.
*   **애니메이션 1: Red Alert 증폭 (Transition to High Risk):**
    *   **트리거:** $\text{V}_{effort}$가 임계치 이하로 떨어지는 순간.
    *   **효과:** Z-Gauge 수치가 **물리학적 힘을 받는 것처럼(Physics-based)**, 빠르고 불규칙하게 최고점까지 솟구쳐야 함. (단순 선형 증가 X).
    *   **시각화:** 배경색이 `#C0392B` (짙은 경고 레드)로 변하고, 전체 화면에 미세한 노이즈(Glitch Effect)가 추가되어 긴장감을 고조시켜야 함.

### 2. 색상 전환 애니메이션 (The Color Shift: The Core Magic)
*   **목표:** '위험' $\rightarrow$ '안도감'의 감정적 여정을 컬러로 표현.
*   **애니메이션 2: Relief Transition:**
    *   **트리거:** OPRF 솔루션이 적용되어 $Z_{final}$ 값이 반환되는 순간.
    *   **효과:** 화면 전체를 뒤덮고 있던 `#C0392B` 계열의 어두운 오버레이가, 1~2초에 걸쳐 부드럽게(Easing Curve: Out-Quad) `#27AE60` (안정적인 녹색)으로 점진적으로 **변이(Morphing)**해야 함.
    *   **데이터 매핑:** 이 변이는 $Z$ 값이 감소하는 비율($\Delta Z / Z_{initial}$)에 비례하여 진행되어야 합니다. ($\Delta Z$가 클수록, 전환 속도가 빠르고 강렬함).

### 3. $\Delta Z$ 값 하이라이팅 (The Financial Aha Moment)
*   **위치:** 결과 섹션 중앙의 별도 카드 컴포넌트.
*   **표현 방식:** 단순한 숫자가 아니라, '사라진 위험'을 상징하는 시각적 요소가 필요함.
    *   `[Visualization]` 영역에 초기 $Z$ 값 크기의 빨간색 막대(Bar)를 배치합니다.
    *   솔루션 적용 후 $\Delta Z$ 만큼의 길이만큼, 해당 빨간색 막대가 **'사라지면서(Fade Out)'** 녹색 빛을 내며 회피 가치($\Delta Z$)라는 텍스트와 함께 축소되어야 합니다. (Loss/Gain 시각화).

---
## 🛠️ III. 개발자 테스트 명세서 (Developer Checklist)
*   [ ] **API Endpoint Mocking:** `risk_engine.py`의 모든 출력 값을 성공적으로 수신할 수 있도록 프론트엔드 스켈레톤을 준비할 것.
*   [ ] **State Management:** $Z_{initial}$, $\text{Red Alert State}$, $\Delta Z$, $Z_{final}$ 네 가지 상태 값이 명확히 정의되고 관리되어야 함.
*   [ ] **Animation Hook:** 모든 애니메이션(특히 색상 변이)은 백엔드에서 전달된 `is_red_alert` 플래그와 최종 $Z$ 값의 차이를 기준으로 트리거 되어야 합니다.