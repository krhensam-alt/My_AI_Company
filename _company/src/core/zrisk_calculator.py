import json
from typing import Dict, Any, TypedDict

# --- [1] 데이터 구조 정의 (TypedDict를 사용하여 강한 타입 명시) ---

class ZRiskInputs(TypedDict):
    """
    Z Risk 계산을 위한 모든 입력 변수들. 
    이 모듈은 이 구조화된 입력을 받습니다.
    """
    industry_sector: str  # 예: '금융', '헬스케어'
    regulatory_compliance_score: float  # 0.0 ~ 1.0 (규제 준수 점수)
    operational_resilience_index: float  # 0.0 ~ 1.0 (운영 연속성 지표)
    market_dependency_factor: float  # 0.0 ~ 1.0 (시장 의존도 계수)

class ZRiskOutput(TypedDict):
    """
    API를 통해 반환되어야 하는 구조화된 최종 결과물.
    핵심 가치인 '재무적 손실 감소액'을 포함합니다.
    """
    z_current: float  # 현재 위험 수준 (Potential Maximum Loss)
    delta_z_avoided: float # 회피 가능한 재무적 손실 감소액 (Financial Aha Moment)
    risk_level_category: str # 위험 등급 (예: Red Alert, Green Relief)
    summary_report: Dict[str, Any] # 상세 보고서 요약

# --- [2] 핵심 Pure Function 모듈 구현 ---

def calculate_z_risk(inputs: ZRiskInputs) -> ZRiskOutput:
    """
    [Pure Function] 입력 변수만으로 최종 Z Risk와 Delta Z를 계산하는 코어 엔진.
    외부 API 호출, DB 접근 등 Side Effect가 전혀 없습니다. 
    테스트 용이성이 극대화됩니다.

    Args:
        inputs: ZRiskInputs 타입의 사전 정의된 위험 요소들.

    Returns:
        ZRiskOutput 타입의 구조화된 결과물.
    """
    print(f"--- [LOG] Z Risk 계산 시작: {inputs['industry_sector']} 분야 ---")
    
    # 1. 현재 최대 잠재 손실액 (Z_current) 계산 로직 (가중치 부여 예시)
    # Formula: Z = MaxLoss * (RegulatoryPenalty + OperationalRisk * DependencyFactor)
    regulatory_penalty = (1 - inputs['regulatory_compliance_score']) * 0.6
    operational_risk_factor = (1 - inputs['operational_resilience_index']) * inputs['market_dependency_factor']
    
    # 임시 최대 손실액(MaxLoss) 가정: 업종에 따라 기본 계수가 다름
    base_max_loss = 100.0 # 만약 API에서 받은 상수로 대체 가능
    
    z_current_value = base_max_loss * (regulatory_penalty + operational_risk_factor)
    
    # 2. 위험 등급 결정 로직
    if z_current_value >= 70:
        risk_level = "Red Alert" # 심각한 수준
        risk_color = "red"
    elif z_current_value >= 30:
        risk_level = "Amber Warning" # 주의 필요 수준
        risk_color = "orange"
    else:
        risk_level = "Green Relief" # 안전/완화 수준
        risk_color = "green"

    # 3. 회피 가능한 손실 감소액 (Delta Z) 계산 로직
    # Delta Z는 솔루션 도입을 통해 개선된 '효율성'에 비례한다고 가정합니다.
    delta_z_avoided = base_max_loss * inputs['regulatory_compliance_score'] * 0.8
    
    if delta_z_avoided < 1: # 최소한의 값을 보장
        delta_z_avoided = max(1.0, delta_z_avoided)

    # 4. 보고서 요약 구조화
    summary = {
        "risk_components": {
            "regulatory_score": f"{inputs['regulatory_compliance_score']:.2f}",
            "operational_index": f"{inputs['operational_resilience_index']:.2f}",
            "market_dependency": f"{inputs['market_dependency_factor']:.2f}"
        },
        "z_current_interpretation": "현행 시스템의 취약점을 기반으로 추정된 최대 재무적 손실액입니다.",
        "delta_z_interpretation": "hensam 솔루션 도입을 통해 방지할 수 있는 핵심 가치(재무적 회복)입니다."
    }

    # 5. 최종 결과 반환
    return ZRiskOutput(
        z_current=round(z_current_value, 2),
        delta_z_avoided=round(delta_z_avoided, 2),
        risk_level_category=risk_level,
        summary_report=summary
    )

# --- [3] 테스트 코드 예시 (사용자가 직접 실행하여 검증) ---

def run_example_test():
    """
    실제 환경에서 시뮬레이션하는 방법을 보여주는 예시 함수. 
    이 함수는 백엔드 스켈레톤의 사용법을 안내합니다.
    """
    print("\n=============================================")
    print("        ✅ Z Risk Calculator Test Run         ")
    print("=============================================\n")

    # Case 1: 매우 위험한 상황 (Red Alert 유도)
    bad_inputs = ZRiskInputs(
        industry_sector='금융',
        regulatory_compliance_score=0.2,  # 낮은 점수
        operational_resilience_index=0.3, # 낮은 안정성
        market_dependency_factor=0.9      # 높은 의존도
    )
    print(">>> [테스트 Case 1: High Risk Scenario (Red Alert 유도)]")
    result_bad = calculate_z_risk(bad_inputs)
    print("\n[결과 JSON 구조 예시]:")
    print(json.dumps(result_bad, indent=4))

    # Case 2: 안전하고 규제 준수도가 높은 상황 (Green Relief 유도)
    good_inputs = ZRiskInputs(
        industry_sector='통신',
        regulatory_compliance_score=0.95, # 매우 높은 점수
        operational_resilience_index=0.8, 
        market_dependency_factor=0.4      # 낮은 의존도
    )
    print("\n\n>>> [테스트 Case 2: Low Risk Scenario (Green Relief 유도)]")
    result_good = calculate_z_risk(good_inputs)
    print("\n[결과 JSON 구조 예시]:")
    print(json.dumps(result_good, indent=4))

if __name__ == "__main__":
    run_example_test()