# 글로벌 규제 및 공급망 리스크 기반 Z Risk 시나리오 라이브러리 (최종안)

**작성 목적:** B2B 영업 자산의 'Audit Evidence Exhibit' 페이지를 위한 핵심 근거 자료. 단순한 위험 목록이 아닌, 재무적 손실액($Z$)을 정량화하여 고객의 운영 지속성 위협 인지를 극대화하는 것을 목표로 함.

## 🔍 리스크 시나리오 데이터 구조 (4가지 핵심 주제)

| 구분 | 주제 (Focus Area) | 주요 위험 원인 | $Z$ Risk 측정 변수 | 예상 피해 규모 ($Z$) 제시 방식 |
| :--- | :--- | :--- | :--- | :--- |
| **1** | AI 거버넌스 실패 | 국경 간 데이터 이동 제한, 규제 미준수 | 법적 패널티 (L), 지연 비용 ($\text{Delay Cost}$) | $Z = (L \times I) + (\text{매출} \times \Delta T / 365)$ (I: 위반 건수, $\Delta T$: 예상 중단 기간) |
| **2** | 공급망 병목 현상 | 핵심 광물 단일 소스 의존, 지정학적 리스크 | 필수 부품 단가 폭등 $(\text{Cost}_{spike})$, 재고 부족 비용 ($\text{Stockout Cost}$) | $Z = (\text{원가} \times (1+\text{Inflation})) + (\text{생산량} \times \text{단가})$ |
| **3** | OT/IT 사이버 보안 실패 | 레거시 시스템의 외부 노출, 제어 장치 마비 | MTTR 증가 비용 ($\text{Loss Rate}_{\uparrow}$), 데이터 무결성 손실액 | $Z = (\text{시간당 운영 중단 비용} \times \text{MTTR}_{new}) + \text{데이터 복구 비용}$ |
| **4** | ESG/지속가능성 의무 미준수 | 탄소 추적 실패, 비재무 보고의 투명성 부족 | 시장 접근 제한세 ($\text{Tariff}_{ESG}$), 자본 조달 기회비용($\text{Opportunity Cost}$) | $Z = \text{매출} \times (1 + \frac{\text{탄소세}}{\text{원가}})$ |

## 💡 시나리오 활용 가이드라인
*   **전환 논리:** 위협 $\rightarrow$ $Z$ Risk 제시(공포) $\rightarrow$ [hensam 솔루션] 적용 후 $Z'$ (안도) 비교.
*   **데이터 근거 확보 필수:** 각 수식에 사용된 변수 값($L, \text{Cost}_{spike}, \text{Tariff}_{ESG}$ 등)은 반드시 '출처(Source)'를 명시한 보고서로 뒷받침되어야 함.