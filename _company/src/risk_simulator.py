import time
import math

# ---------------------------------------------------------------------
# Z Risk Simulation Core Engine (Time-Series Accumulation)
# 이 모듈은 시간 경과에 따른 잠재적 최대 손실액(Z)의 누적 및 변화를 시뮬레이션합니다.
# 외부 API 연결 없이, 순수 논리 기반으로 작동하는 MVP 코어입니다.
# ---------------------------------------------------------------------

def calculate_z_risk(initial_risk: float, time_passed_days: int, response_delay_months: float, mitigation_effectiveness: float) -> dict:
    """
    시간 흐름과 대응 지연에 따른 잠재적 최대 손실액(Z)을 계산합니다.

    Args:
        initial_risk (float): 초기 규제/시장 리스크 수준 (기준값).
        time_passed_days (int): 위협 발생 후 경과된 시간 (일 단위).
        response_delay_months (float): 대응책 마련 및 실행까지 지연된 기간 (개월).
        mitigation_effectiveness (float): 도입될 솔루션의 예상 효과 (0.0 ~ 1.0).

    Returns:
        dict: 시뮬레이션 결과 (초기 Z, 최종 Z, 누적 증폭 계수 등)
    """

    if initial_risk <= 0:
        raise ValueError("Initial risk must be positive.")
    if not (0.0 <= mitigation_effectiveness <= 1.0):
        raise ValueError("Mitigation effectiveness must be between 0 and 1.")


    # --- 1. 시간 경과에 따른 기본 리스크 증폭 계수 (Temporal Decay/Inflation) ---
    # 시간이 지날수록 규제 변화, 시장 혼란 등으로 인해 위험이 기하급수적으로 증가한다고 가정합니다.
    temporal_multiplier = 1 + (time_passed_days / 30)**(0.25)

    # --- 2. 대응 지연에 따른 페널티 증폭 (Response Delay Penalty) ---
    # 대응이 지연될수록 리스크 회피 비용이 기하급수적으로 증가합니다.
    delay_multiplier = math.exp(response_delay_months * 0.5)

    # --- 3. 최종 잠재적 최대 손실액 (Z_final) 계산 ---
    # Z_final = 초기 리스크 * 시간 증폭 * 지연 페널티 * (1 - 완화 효과)
    z_before_mitigation = initial_risk * temporal_multiplier * delay_multiplier
    
    # 최종 위험 감소분은 솔루션 도입으로 '회피 가능한' 부분입니다.
    reduction_factor = mitigation_effectiveness
    final_z_loss = z_before_mitigation * (1 - reduction_factor)

    return {
        "initial_risk": round(initial_risk, 2),
        "temporal_multiplier": round(temporal_multiplier, 2),
        "delay_penalty": round(delay_multiplier, 2),
        "z_before_mitigation": round(z_before_mitigation, 2), # Red Alert 값
        "final_z_loss": round(final_z_loss, 2)                   # Relief 값
    }

def run_simulation_and_print(initial_risk: float, time_days: int, delay_months: float, mitigation: float):
    """시뮬레이션 결과와 극적인 출력을 콘솔에서 실행합니다. (데모용)"""
    try:
        results = calculate_z_risk(initial_risk, time_days, delay_months, mitigation)

        print("\n" + "="*70)
        print("🚨 RED ALERT SIMULATION START 🚨")
        print("="*70)
        print(f"[Input Parameters] Initial Risk: ${results['initial_risk']} | Time Passed: {time_days} days | Delay: {delay_months:.1f} months | Mitigation Eff.: {mitigation*100:.0f}%")
        print("-" * 70)

        # Red Alert (최대 위협) 출력 시퀀스
        print("\n>>> [STAGE 1: NO ACTION] - 시간이 지남에 따라 규제 리스크가 누적됩니다...")
        time.sleep(1)
        print("!!! 경고! 대응이 지연됨에 따라, 잠재적 최대 손실액($Z$)은 기하급수적으로 증가합니다 !!!")
        time.sleep(1.5)
        print(f"📈 [PRE-MITIGATION Z]: 최소 ${results['z_before_mitigation']:.2f} (위협 규모)")
        print("----------------------------------------------------------------------")

        # Narrative Pause 효과 연출
        input("\n[⏸️ Narrating... 잠시 멈춥니다. 이 수치에 주목하십시오.] [Enter를 누르세요]")
        time.sleep(1)

        # Relief (해결책 제시) 출력 시퀀스
        print("\n✅ [STAGE 2: SOLUTION] - hensam의 운영 지속성 전략 도입!")
        time.sleep(1)
        print("규제 리스크 감소분($\Delta Z$)을 계산하여, 위협 규모를 크게 낮춥니다.")
        time.sleep(1.5)
        print("-" * 70)
        print(f"📉 [FINAL $Z$ LOSS]: 최종 위험 손실액은 ${results['final_z_loss']:.2f}로 감소했습니다.")
        print("=====================================================================")


    except ValueError as e:
        print(f"\n[ERROR] 시뮬레이션 실패: {e}")

if __name__ == "__main__":
    # --- [데모 실행 예시] ---
    # 1. 초기 리스크 $Z$ = 5,000만 달러 (기준)
    initial_risk_val = 50.0  # 단위: 백만원
    
    # 2. 위협 발생 후 대응하지 않고 시간이 흐름 (365일 경과)
    time_passed_days_val = 365 

    # 3. 규제 변화에 대한 내부 대응 지연 기간 (8개월)
    delay_months_val = 8.0   

    # 4. hensam의 솔루션 도입으로 회피 가능한 리스크 비율 (70% 감소 효과)
    mitigation_effectiveness_val = 0.7

    run_simulation_and_print(
        initial_risk=initial_risk_val,
        time_days=time_passed_days_val,
        delay_months=delay_months_val,
        mitigation=mitigation_effectiveness_val
    )