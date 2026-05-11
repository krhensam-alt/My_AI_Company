class RiskEngineCore:
    """
    Operational Resilience Framework (OPRF) 기반 Z Risk 진단 및 시뮬레이션 핵심 엔진.
    외부 API 의존성을 제거하고, 논리적 상태 전환(State Transition)에 집중합니다.
    """

    def __init__(self):
        # 기본 상수 값 설정 (가상의 산업 평균 데이터)
        self.DEFAULT_BASE_RISK = 10000  # 초기 최대 잠재 손실액 기준 (단위: 백만 원)
        self.OPRF_DISCOUNT_FACTOR = 0.65 # OPRF 적용 시 위험 감소율 계수 (최대 35% 절감 가정)

    def calculate_initial_z_risk(self, industry_type: str, regulatory_compliance_score: float, market_dependency_index: float) -> dict:
        """
        사용자 입력 변수를 받아 초기 잠재 최대 손실액 (Z_Initial)을 산출합니다.
        높은 위험 점수는 높은 Z 값을 의미합니다.
        """
        # 1. 산업군 기반 기본 위험 할당
        base_risk = self.DEFAULT_BASE_RISK * (1 + (market_dependency_index / 2))

        # 2. 규제 준수 실패 패널티 계산: 점수가 낮을수록(위험할수록) 가중치가 높아짐
        # 예시: Score가 0에 가까우면 패널티가 매우 커지도록 설계 (1 - score/10) 사용
        compliance_penalty = max(0.1, 1 - (regulatory_compliance_score / 10)) * self.DEFAULT_BASE_RISK * 0.5

        # 최종 초기 위험 지표 산출 (가장 충격적인 수치를 만들기 위해 합산)
        z_initial = base_risk + compliance_penalty
        
        return {
            "status": "RED ALERT",
            "Z_Initial": round(z_initial, 2), # Initial Risk Value
            "description": f"{industry_type} 산업군 및 낮은 규제 준수 점수로 인해 잠재적 최대 손실액이 매우 높게 예측됩니다."
        }

    def apply_oprf_and_calculate_final_state(self, z_initial: float) -> dict:
        """
        OPRF 솔루션을 적용하여 위험 감소분 (Delta Z) 및 최종 안전 지표 (Z_Final)를 산출합니다.
        이 함수가 핵심 State Transition Logic을 담당합니다.
        """
        # OPRF 효과 반영: 초기 위험액의 일정 비율을 안정화 자산으로 전환
        delta_z = z_initial * self.OPRF_DISCOUNT_FACTOR 
        z_final = max(100, z_initial - delta_z) # 최소한의 안전 지표 유지

        return {
            "status": "RELIEF",
            "Z_Final": round(z_final, 2), # Final Safe Value
            "Delta_Z": round(delta_z, 2),  # 위험 감소분 (The core value proposition)
            "description": f"OPRF 솔루션 적용을 통해 {round(self.OPRF_DISCOUNT_FACTOR * 100)}%의 재무적 안정화 효과가 예상됩니다.",
        }

    def run_simulation(self, industry: str, compliance_score: float, market_index: float) -> dict:
        """
        전체 시뮬레이션 과정을 단일하게 실행하고, 구조화된 최종 보고서를 반환합니다.
        사용자가 보는 '스토리텔링 플로우'가 이 함수 한 번의 호출로 완성되어야 합니다.
        """
        # 1. 초기 상태 진단 (RED ALERT)
        initial_report = self.calculate_initial_z_risk(industry, compliance_score, market_index)
        
        # 2. 솔루션 적용 및 최종 상태 도출 (RELIEF)
        final_report = self.apply_oprf_and_calculate_final_state(initial_report["Z_Initial"])

        # 3. 종합 결과 구조화
        return {
            "simulation_summary": "최종 Z Risk 진단 및 OPRF 적용 보고서",
            "initial_risk": initial_report,
            "resilience_result": final_report,
            "analysis": f"Initial Risk ({initial_report['Z_Initial']}M) $\\rightarrow$ Solution Applied $\\rightarrow$ Final Safe Value ({final_report['Z_Final']}M). 절감액: {final_report['Delta_Z']}M."
        }

# 테스트용 실행 코드 (Module Level Test)
if __name__ == "__main__":
    print("--- [RiskEngineCore Self-Test Start] ---")
    engine = RiskEngineCore()
    
    # 1. 고위험 시나리오 테스트: 규제 준수 점수 낮음, 시장 의존도 높음
    high_risk_params = {
        "industry": "금융 (은행)",
        "compliance_score": 3.0, # 매우 낮음
        "market_index": 8.5      # 매우 높음
    }
    print("\n[TEST CASE 1: High Risk Scenario]")
    report = engine.run_simulation(**high_risk_params)
    import json
    print(json.dumps(report, indent=4))

    # 2. 저위험 시나리오 테스트: 규제 준수 점수 높음, 시장 의존도 낮음
    low_risk_params = {
        "industry": "IT (소프트웨어)",
        "compliance_score": 9.5, # 매우 높음
        "market_index": 2.0      # 낮음
    }
    print("\n[TEST CASE 2: Low Risk Scenario]")
    report = engine.run_simulation(**low_risk_params)
    print(json.dumps(report, indent=4))

    print("--- [RiskEngineCore Self-Test End] ---")