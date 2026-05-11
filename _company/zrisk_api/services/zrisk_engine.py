from typing import Dict

# [Developer Notes] Z Risk 계산 엔진의 순수 모듈화 (API 레이어와 분리)
# 이 함수는 외부 의존성 없이 오직 입력 변수를 받아 재무적 손실을 도출하는 핵심 비즈니스 로직입니다.

def calculate_z_risk(industry_type: str, regulatory_score: float, market_vulnerability_index: float) -> Dict[str, float]:
    """
    Z Risk (Potential Maximum Loss)를 계산하고 위험 감소분(Delta Z)을 예측합니다.
    - industry_type: 산업군 문자열 (예: 'Finance', 'Health')
    - regulatory_score: 현재 규제 준수 점수 (0.0 ~ 1.0)
    - market_vulnerability_index: 시장 취약성 지표 (0.0 ~ 1.0)

    반환값은 {Z_current: 현재 위험, Delta_Z: 감소 가능한 위험} 형태의 Dictionary입니다.
    """
    if not (0.0 <= regulatory_score <= 1.0 and 0.0 <= market_vulnerability_index <= 1.0):
        raise ValueError("모든 입력 변수는 0.0에서 1.0 사이여야 합니다.")

    # 1. 규제 준수 실패 패널티 (Regulatory Failure Penalty, R) 계산:
    # 규제가 낮을수록(score가 작을수록) 위험은 기하급수적으로 증가한다고 가정합니다.
    R = 1 - regulatory_score # 간소화된 변환 로직

    # 2. 시장 취약성 기반 최대 잠재 손실 (Z_current) 계산:
    # Z = f(R, MVI) -> R * (1 + MVI^2) * MaxScaleFactor
    MAX_SCALE_FACTOR = 100.0 # 임의의 재무적 규모 스케일링 계수
    z_current = round(R * (1 + market_vulnerability_index**2) * MAX_SCALE_FACTOR, 2)

    # 3. 위험 회피 가능 분 (Delta Z) 계산:
    # 솔루션 도입을 통해 규제 준수 점수를 일정 비율(예: 0.75) 향상시킬 수 있다고 가정합니다.
    # 이 개선이 재무적 손실 예측에 기여하는 만큼을 Delta_Z로 잡습니다.
    # (1 - regulatory_score * 0.25)가 감소 가능한 위험의 비율이라고 가정합니다.
    delta_z = round(z_current * 0.3, 2)

    if delta_z > z_current: # 논리 오류 방지
        delta_z = z_current * 0.9

    return {
        "Z_current": z_current,  # 현재 예측되는 최대 재무 손실액 (Potential Max Loss)
        "Delta_Z": delta_z,     # 솔루션 도입으로 회피 가능한 위험 감소분 (Financial Aha Moment)
        "Operational_Resilience_Score": round(regulatory_score * 1.2 + 0.3, 2) # 추가 지표
    }

def generate_report_json(industry: str, z_data: Dict[str, float]) -> dict:
    """
    최종 보고서 JSON 구조를 완성하는 함수입니다. (API 응답 표준화 목적)
    """
    return {
        "metadata": {
            "source": "hensam_zrisk_api",
            "version": "V1.0",
            "timestamp": "2026-05-12T12:00:00Z" # 실제 구현 시 datetime 사용 필요
        },
        "input_parameters": {
            "industry_type": industry,
            # ... 나머지 입력 변수 포함
        },
        "risk_assessment": {
            "z_current": z_data["Z_current"],
            "delta_z": z_data["Delta_Z"],
            "operational_resilience_score": z_data["Operational_Resilience_Score"]
        },
        "recommendation": "운영 복원력(OPRF) 모델 기반의 즉각적인 PoC 도입을 강력히 권고합니다."
    }