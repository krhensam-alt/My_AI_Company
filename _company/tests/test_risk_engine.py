import unittest
from src.risk_engine import RiskEngineCore

class TestRiskEngine(unittest.TestCase):
    """
    RiskEngineCore 클래스의 핵심 로직(Z Risk 계산 및 상태 전환)을 테스트합니다.
    """
    
    def setUp(self):
        # 각 테스트 케이스 실행 전에 엔진 인스턴스를 초기화합니다.
        self.engine = RiskEngineCore()

    def test_high_risk_state_transition(self):
        """
        [High Risk Scenario] - 규제 준수 점수가 낮을 때, Z_Initial이 높게 산출되고 
        Delta_Z가 명확하게 계산되는지 검증합니다.
        """
        # 입력 변수 설정: 금융 (위험), 낮은 점수(위험), 높은 의존도(위험)
        industry = "금융 (은행)"
        compliance_score = 3.0
        market_index = 8.5

        report = self.engine.run_simulation(
            industry=industry,
            compliance_score=compliance_score,
            market_index=market_index
        )
        
        # 검증 1: 초기 상태가 'RED ALERT'인지 확인
        self.assertEqual(report['initial_risk']['status'], "RED ALERT")

        # 검증 2: Z_Initial 값이 충분히 높은지 (상대적 크기 체크)
        z_initial = report['initial_risk']['Z_Initial']
        self.assertGreater(z_initial, 15000, f"Expected high initial risk > 15000, got {z_initial}")

        # 검증 3: 상태 전환 로직이 작동하여 Z_Final과 Delta_Z가 양수인지 확인
        resilience = report['resilience_result']
        self.assertGreater(resilience['Delta_Z'], z_initial * 0.2, "Expected significant risk reduction.")
        self.assertLess(resilience['Z_Final'], z_initial * 0.9, "Z_Final should be significantly lower than Z_Initial.")

    def test_low_risk_state_transition(self):
        """
        [Low Risk Scenario] - 규제 준수 점수가 높을 때, 초기 위험이 낮고 
        필요한 개선 영역(Delta_Z)도 적절하게 산출되는지 검증합니다.
        """
        # 입력 변수 설정: IT (안전), 높은 점수(안전), 낮은 의존도(안전)
        industry = "IT (소프트웨어)"
        compliance_score = 9.5
        market_index = 2.0

        report = self.engine.run_simulation(
            industry=industry,
            compliance_score=compliance_score,
            market_index=market_index
        )
        
        # 검증 1: 초기 Z_Initial 값이 충분히 낮은지 (상대적 크기 체크)
        z_initial = report['initial_risk']['Z_Initial']
        self.assertLess(z_initial, 7000, f"Expected low initial risk < 7000, got {z_initial}")

        # 검증 2: Delta_Z가 적절한 범위 내에 있는지 (너무 크거나 작지 않아야 함)
        resilience = report['resilience_result']
        self.assertGreater(resilience['Delta_Z'], 500, "Expected some measurable improvement.")


if __name__ == '__main__':
    unittest.main()