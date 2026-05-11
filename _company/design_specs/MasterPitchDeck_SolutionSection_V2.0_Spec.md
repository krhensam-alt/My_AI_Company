# 💡 Master Pitch Deck: Solution Section Design & Animation Specification (V2.0)

**목표:** 최고 경영진(C-Level)에게 'Delay Cost'의 심각성을 인식시키고, hensam의 솔루션만이 유일한 탈출구임을 극적으로 각인시킨다.
**핵심 감정 플로우:** **[공포 (Fear)] $\rightarrow$ [깨달음 (Aha!)] $\rightarrow$ [안도감 (Relief)]**
**주요 트랜지션:** Red Alert ($Z_{\text{high}}$) $\xrightarrow{\text{Solution Logic Applied}}$ Green Zone ($Z_{\text{low}}$)

---

## 1. 전체 구조 및 레이아웃 원칙

*   **레이아웃 (Grid):** 좌측 (Problem/Input), 중앙 (Process/Action), 우측 (Result/Impact).
*   **배경:** 어둡고 무거운 톤을 유지하여 심각성을 강조합니다.
*   **폰트 사용:** 전문적이고 권위적인 산세리프 계열 (예: Source Sans Pro 또는 Noto Sans Bold).

## 2. 애니메이션 시퀀스 상세 설계 (The Three Acts)

### ACT I: 문제 제기 및 충격 유도 (The Problem - Red Alert State)

*   **트리거:** 슬라이드 진입 또는 '현재 위험 분석' 버튼 클릭.
*   **시각화 요소:** 대형 $Z$ Risk Gauge, 초기 Input 변수 목록.
*   **컬러 팔레트:** 배경색은 무채색/짙회색. $Z$ 값 관련 UI 요소는 **#C0392B (Danger Red)**로 지배됨.
*   **애니메이션 A: Z-Value 증폭:**
    1.  초기에는 $Z_{\text{current}}$ 값이 0에서 시작합니다.
    2.  개발자가 제공한 `initialInputs` 데이터(산업별 변수, 시장 의존도 등)가 차례로 화면에 입력되면서 (타이핑 애니메이션), **$Z$ 값 게이지 바늘이 기하급수적으로 증가**해야 합니다.
    3.  증폭 속도는 최고조에 달하며, 최대 $Z_{\text{high}}$ 값 도달 시 **'Critical Failure' 경고 사운드 및 화면 떨림 효과(Subtle Jitter)**를 부여합니다.
    4.  **Key Message Overlay:** "현재 구조적 리스크는 통제 불가능한 수준입니다."

### ACT II: 솔루션 적용 (The Turning Point - The Process)

*   **트리거:** 'vensam Solution Apply' 버튼 클릭 또는 발표자의 구두 개입 시점.
*   **시각화 요소:** OPRF Model Diagram, 로직 플로우 다이어그램.
*   **애니메이션 B: 로직 프로세싱:**
    1.  $Z_{\text{high}}$ 값이 정점에 도달했을 때, 화면 전체에 **'PROCESSING...'** 오버레이가 나타나며 시각적 멈춤(Pause)을 유도합니다.
    2.  OPRF 모델의 각 축(예: 운영 복원력 확보, 프로세스 최적화)이 차례로 빛나면서 (Spotlight Effect), 시스템이 작동하는 느낌을 줍니다.
    3.  **Key Visual:** $Z$ Risk Gauge가 갑자기 **'재계산 중...'** 상태로 전환되며, 데이터 변수들이 빠져나가는(Extracting/Filtering) 애니메이션을 보여줍니다.

### ACT III: 결과 제시 및 안도감 극대화 (The Relief - Green Zone State)

*   **트리거:** 로직 프로세싱이 완료됨과 동시에 자동 전환.
*   **시각화 요소:** 새로운 $Z$ Risk Gauge, 개선된 재무 예측 그래프.
*   **컬러 팔레트:** 모든 위험 경고색($#C0392B$)이 부드럽게 **#27AE60 (Safety Green)**으로 전환됩니다. 배경의 무거움이 걷히며 밝아지는 느낌을 연출합니다.
*   **애니메이션 C: Z-Value 감소:**
    1.  $Z$ 게이지 바늘이 극적으로 하락하며, 새로운 $Z_{\text{low}}$ 값이 명료하게 표시됩니다. 이 변화는 **급격하고 드라마틱한 '역방향' 애니메이션**이어야 합니다 (Falling Effect).
    2.  **핵심 효과:** 감소된 $\Delta Z$ 값 (회피 가치)에 해당하는 금액($\$$)을 가장 크게, 그리고 가장 명확하게 중앙에 띄웁니다. ("Potential Loss Reduction: $X Million")
    3.  **최종 메시지:** "hensam은 단순한 진단을 넘어, **구체적이고 실행 가능한 재무 회복 로드맵**을 제공합니다."

---
*   **기술 구현 참고 사항 (Developer):** 모든 상태 변화(State Change)는 `analysisResults`의 `z_current`와 `riskLevel` 필드를 트리거로 사용해야 합니다. $Z$ 값 감소율은 임의가 아닌, 정의된 모델 기반으로 '최소 X% 이상' 감축되는 수치를 보여주어야 신뢰도가 유지됩니다.