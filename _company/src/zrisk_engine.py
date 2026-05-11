from pydantic import BaseModel, Field
from typing import Dict, Any

# --- 데이터 스키마 정의 (Pydantic 사용) ---
class InputData(BaseModel):
    """사용자 입력 데이터를 구조화합니다."""
    industry_sector: str = Field(description="진단 대상 산업군 (예: 금융, 헬스케어)")
    compliance_weakness_score: float = Field(description="규제 준수 약점 점수 (0.0 ~ 1.0). 높을수록 위험함.")
    market_dependency_index: float = Field(description="시장 의존성 지표 (0.0 ~ 1.0). 외부 변수에 대한 민감도.")

class ZRiskResult(BaseModel):
    """계산된 최종 결과를 구조화합니다."""
    z_current: float = Field(description="'진단 전'의 잠재 최대 손실액 (Red Alert, $Z_{current}$)")
    delta_z_potential: float = Field(description="솔루션 적용 시 회피 가능한 위험 감소분 ($\Delta Z$).")
    final_risk_level: str = Field(description="최종 권고 수준 (예: Managed, Low Risk).")

class ZRiskSimulationReport(BaseModel):
    """프런트엔드에 전달될 최종 JSON 구조화 보고서입니다."""
    input_data: InputData
    z_current_details: Dict[str, Any] = Field(description="Z Current 계산의 세부 근거.")
    solution_impact: Dict[str, float] = Field(description="솔루션 적용으로 개선되는 각 리스크 요소별 감소율.")
    z_result: ZRiskResult

# --- 핵심 엔진 클래스 ---
class ZRiskEngine:
    """
    Z Risk (Potential Maximum Loss) 계산 및 시뮬레이션을 담당하는 코어 모듈.
    외부 API 호출 없이 순수 로직으로만 작동합니다.
    """
    
    @staticmethod
    def _calculate_z_current(data: InputData) -> float:
        """
        Z Risk의 현재 수준을 계산합니다. 
        [가정된 복잡한 공식]: Z = (규제 약점 * 시장 의존성 계수) * 산업군 가중치 + 기본 패널티
        실제로는 수많은 변수가 들어가지만, 여기서는 구조를 보여줍니다.
        """
        # 1. 기본 위험 점수 산출 (Compliance Weakness가 가장 큰 영향 요소임을 가정)
        base_risk = data.compliance_weakness_score * 0.6 
        
        # 2. 시장 의존성 가중치 적용
        dependency_factor = data.market_dependency_index * 1.3
        
        # 3. 산업군별 패널티 (가상의 매핑)
        sector_weight = 1.0 # 실제 구현 시: if data.industry_sector == "Finance": return 1.5 ...
        
        z_current = base_risk * dependency_factor * sector_weight + 5.0 # 최소한의 기본 리스크 값 추가
        return round(z_current, 2)

    @staticmethod
    def simulate_solution_impact(data: InputData, z_current: float) -> tuple[float, Dict[str, float]]:
        """
        솔루션 적용으로 인해 Z Risk가 감소하는 정도를 계산합니다.
        감소분은 '규제 약점'을 해결하는 솔루션의 가치에 비례합니다.
        """
        # 가정: 솔루션이 규제 약점 점수의 70%까지 완화한다고 정의
        reduction_factor = 0.7 * data.compliance_weakness_score
        delta_z = z_current * reduction_factor
        
        # 각 요소별 감소율 매핑 (프런트엔드 시각화를 위한 데이터)
        impact_details = {
            "Compliance Improvement": round(delta_z * 0.5, 2), # 가장 큰 기여분
            "Operational Resilience": round(delta_z * 0.3, 2),
            "Process Automation": round(delta_z * 0.2, 2)
        }
        return delta_z, impact_details

    @staticmethod
    def run_simulation(data: InputData) -> ZRiskSimulationReport:
        """
        Z Risk 시뮬레이션의 전체 플로우를 실행하고 최종 보고서를 생성합니다.
        """
        # Step 1: 현재 위험 진단 (Red Alert)
        z_current = ZRiskEngine._calculate_z_current(data)

        # Step 2: 솔루션 적용 가능성 계산 (Green Relief 준비)
        delta_z, impact_details = ZRiskEngine.simulate_solution_impact(data, z_current)
        
        # Step 3: 최종 결과 산출 및 레벨 판정
        final_risk = round(max(0.0, z_current - delta_z), 2)

        if final_risk <= 10.0 and data.compliance_weakness_score < 0.4:
            level = "Low Risk (Sustainable)"
        elif final_risk > 50.0:
            level = "Extreme Risk (Immediate Intervention Required!)"
        else:
            level = "Moderate Risk (Strategic Improvement Recommended)"

        z_result = ZRiskResult(
            z_current=z_current,
            delta_z_potential=round(delta_z, 2),
            final_risk_level=level
        )

        report = ZRiskSimulationReport(
            input_data=data,
            z_current_details={
                "Formula": "Z = (Compliance Weakness * 0.6) * (Market Dependency * 1.3) * Sector Weight + Base Penalty",
                "Raw_Score": z_current,
                "Interpretation": f"현재 {data.industry_sector} 산업군은 약점({data.compliance_weakness_score:.2f})으로 인해 높은 잠재적 손실을 안고 있습니다."
            },
            solution_impact=impact_details,
            z_result=z_result
        )
        return report

# --- 테스트 예시 (이 코드는 실행 시 주석 처리하거나 별도 파일에서 실행해야 합니다.) ---
if __name__ == "__main__":
    # 예제 1: 위험도가 높은 금융사 케이스
    high_risk_data = InputData(
        industry_sector="Finance", 
        compliance_weakness_score=0.9, 
        market_dependency_index=0.8
    )
    report_high = ZRiskEngine.run_simulation(high_risk_data)
    print("--- [HIGH RISK SIMULATION REPORT] ---")
    print(report_high.model_dump_json(indent=2))

    # 예제 2: 위험도가 낮은 산업군 케이스
    low_risk_data = InputData(
        industry_sector="Consumer Goods", 
        compliance_weakness_score=0.2, 
        market_dependency_index=0.3
    )
    report_low = ZRiskEngine.run_simulation(low_risk_data)
    print("\n--- [LOW RISK SIMULATION REPORT] ---")
    print(report_low.model_dump_json(indent=2))