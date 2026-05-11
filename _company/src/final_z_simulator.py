import json
from typing import Dict, Any

# ==============================================================================
# [CORE MODULE] Final Z Risk Simulation Engine (Keynote/Figma Optimized)
# 이 함수는 복잡한 백엔드 의존성을 제거하고, '상태 변화'와 '발표용 데이터 흐름'을 반환하는 데 초점을 맞춥니다.
# ==============================================================================

def run_z_risk_simulation(initial_state: Dict[str, Any], user_input: Dict[str, float]) -> Dict[str, Any]:
    """
    사용자 변수 조작에 따른 Z Risk 변화 과정을 시뮬레이션하고, 
    발표 자료 제작에 필요한 모든 상태 정보와 데이터를 구조적으로 반환합니다.

    Args:
        initial_state: 초기 규제 환경 및 시장 상황 (기준점).
        user_input: 사용자가 변경할 수 있는 핵심 변수들 (예: 대응 속도 계수, 신뢰 지표 등).

    Returns:
        상태 변화와 최종 결과를 포함하는 딕셔너리.
    """
    print("--- [Z Risk Simulation Engine] 초기 상태 로드 중 ---")
    
    # 1. Red Alert 구간 진입 (위협 증폭 단계)
    initial_z = initial_state.get("base_risk", 0.0)
    delay_cost = max(0, user_input.get('delay_period', 0)) * initial_state.get("base_severity_factor", 1.5)
    
    # 규제 강도 계수와 시장 의존성이 높아질수록 Z 값이 급격히 증가함을 반영
    red_alert_z = initial_z + delay_cost + (user_input.get('regulation_coeff', 0) * 100)
    
    # 최대 손실액($Z$)이 임계치를 넘었는지 확인하여 'Red Alert' 플래그 설정
    is_red_alert = red_alert_z > initial_state.get("critical_threshold", 500.0)
    
    simulation_step = {
        "status": "RED_ALERT" if is_red_alert else "NORMAL",
        "risk_value": round(red_alert_z, 2),
        "description": f"규제 지연 ({delay_cost:.2f})으로 인해 잠재적 최대 손실액이 임계치를 초과했습니다. 즉각적인 대응 필요.",
        "animation_trigger": "SCALE_UP_FAST", # Keynote/Figma 애니메이션 트리거 명시
        "data_point": {"Delay Cost": delay_cost}
    }

    # 2. Relief 구간 전환 (해결책 제시 및 위험 감소 단계)
    solution_efficacy = user_input.get('solution_efficacy', 0.7) # 솔루션 도입 효과율 (0~1)
    mitigation_factor = solution_efficacy * initial_state.get("base_risk", 0.0) * 0.8

    final_z = red_alert_z - mitigation_factor
    
    # 최종 상태 결정 및 메시지 생성
    simulation_step["status"] = "RELIEF"
    simulation_step["risk_value"] = round(max(0, final_z), 2)
    simulation_step["description"] = f"솔루션 도입으로 위험을 성공적으로 완화했습니다. 회피 가능액: {round(mitigation_factor, 2)}."
    simulation_step["animation_trigger"] = "SCALE_DOWN_SMOOTH" # Keynote/Figma 애니메이션 트리거 명시
    simulation_step["data_point"]["Mitigated Loss"] = round(mitigation_factor, 2)

    return {
        "initial_state": initial_state,
        "final_result": simulation_step
    }


# ==============================================================================
# [TESTING EXAMPLE] 이 코드는 Keynote/Figma의 로직 백엔드 역할을 합니다.
# 사용자는 이 함수를 호출하여 상태 변화에 따른 데이터를 받아 시각화합니다.
# ==============================================================================

if __name__ == "__main__":
    print("\n" + "="*50)
    print("        [실행 테스트] Z Risk Simulation Core Module")
    print("="*50)

    # 1. 초기 환경 설정 (가정된 기준값)
    initial_environment = {
        "base_risk": 300.0,
        "base_severity_factor": 1.5, # 기본 심각도 계수
        "critical_threshold": 450.0 # 경고 임계치
    }

    # --- 시나리오 A: Red Alert 유발 (사용자가 대응을 안 했을 때) ---
    print("\n--- [시나리오 A] 대응 실패 시뮬레이션 (Red Alert) ---")
    input_fail = {"delay_period": 3.0, "regulation_coeff": 2.5, "solution_efficacy": 0.0}
    result_fail = run_z_risk_simulation(initial_environment, input_fail)
    print("\n[결과 A (Red Alert)]")
    print(json.dumps(result_fail['final_result'], indent=4))

    # --- 시나리오 B: Relief 유발 (사용자가 솔루션을 적용했을 때) ---
    print("\n--- [시나리오 B] 성공적인 대응 시뮬레이션 (Relief) ---")
    input_success = {"delay_period": 1.0, "regulation_coeff": 1.0, "solution_efficacy": 0.8} # 높은 효능율 적용
    result_success = run_z_risk_simulation(initial_environment, input_success)
    print("\n[결과 B (Relief)]")
    print(json.dumps(result_success['final_result'], indent=4))