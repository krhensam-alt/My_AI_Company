import json
from typing import Dict, Any

class ZRiskBinder:
    """
    Z Risk Audit Dashboard V3의 논리 흐름 제어기 (Simulation Orchestrator).
    실제 API 게이트웨이와의 바인딩 로직을 시뮬레이션하며, 발표 환경에 최적화된 
    단계별(Red Alert -> Narrative Pause -> Relief) 데이터를 구조화하여 출력합니다.
    """

    def __init__(self, initial_inputs: Dict[str, Any]):
        """초기 입력값 (사용자/업종 변수 등)을 받아 초기 상태를 설정합니다."""
        self.inputs = initial_inputs
        print("=============================================")
        print("[INFO] Z Risk Binder Initialized.")
        print(f"[DEBUG] Inputs received: {json.dumps(initial_inputs, indent=2)}")

    def run_simulation(self) -> Dict[str, Any]:
        """전체 시뮬레이션 플로우를 순차적으로 실행하고 최종 결과를 반환합니다."""
        results = {}
        
        # 1단계: Red Alert (위험 인지 극대화) - 가장 충격적인 데이터를 먼저 노출
        red_alert_data = self._generate_red_alert(self.inputs)
        results['RedAlert'] = red_alert_data

        # 2단계: Narrative Pause (질문 던지기, 위협의 본질 탐구) - 시각적 여유 제공 및 질문 유도
        pause_data = self._generate_narrative_pause(red_alert_data)
        results['NarrativePause'] = pause_data

        # 3단계: Relief (솔루션 제시, 위험 회피 가치 증명) - 해결책과 감축 효과 강조
        relief_data = self._generate_relief(self.inputs, red_alert_data)
        results['Relief'] = relief_data
        
        return results

    def _calculate_risk_score(self, inputs: Dict[str, Any]) -> float:
        """규제 리스크 계산의 핵심 로직을 시뮬레이션합니다."""
        # 예시: 규제 강도 계수 * 시장 의존성 지표 * 기본 위험 값
        return (inputs.get('regulation_intensity', 0.5) * 
                inputs.get('market_dependency', 1.2) * 
                self.inputs.get('base_risk_factor', 100))

    def _generate_red_alert(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Red Alert 상태의 데이터를 생성합니다. (Z_current 최대 강조)"""
        z_current = self._calculate_risk_score(inputs) * 1.5 # 충격 효과를 위해 과장
        
        return {
            "state": "🚨 RED ALERT: CRITICAL VULNERABILITY DETECTED",
            "visual_impact": "HIGH (Dominant Red Color Scheme)",
            "core_metric": f"{z_current:,.0f} USD (Potential Maximum Loss)",
            "summary_text": (
                f"현재 {inputs.get('industry', 'Industry')}의 규제 준수 시스템은 심각한 구조적 취약점을 안고 있습니다. "
                f"예상되는 잠재 최대 손실액($Z$)는 최소 {z_current:,.0f} USD에 달하며, 즉각적인 개입이 필요합니다."
            ),
            "visual_props": ["Red Warning Banner", "Declining Trend Graph"]
        }

    def _generate_narrative_pause(self, red_alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Narrative Pause 상태의 데이터를 생성합니다. (질문 유도 및 긴장 완화)"""
        # Red Alert 이후 청중이 숨을 고르고 질문에 집중하는 순간을 연출합니다.
        return {
            "state": "⏸️ NARRATIVE PAUSE: THE CORE QUESTION",
            "visual_impact": "MEDIUM (Focus Shift to Text/Question)",
            "question_title": "진정한 리스크는 무엇입니까?",
            "key_points": [
                "문제는 '규제가 존재하는가'가 아니라, '규제에 어떻게 대응하는가'입니다.",
                "현재의 프로세스는 법적 강제성만 충족할 뿐, 재무적 안정성을 보장하지 못합니다.",
                "진정한 가치는 사후 처벌 회피를 넘어선, 선제적 운영 탄력성에 있습니다."
            ],
            "visual_props": ["Audit Checklist Mockup", "Question Marks Animation"]
        }

    def _generate_relief(self, inputs: Dict[str, Any], red_alert_data: Dict[str, Any]) -> Dict[str, Any]:
        """Relief 상태의 데이터를 생성합니다. (솔루션 제시 및 감축 효과 강조)"""
        # 솔루션을 도입했을 때 회피 가능한 위험 감소분 ($\Delta Z$)을 계산합니다.
        delta_z = red_alert_data['RedAlert'] * 0.4 # 임의로 40% 감소 가정
        
        return {
            "state": "✅ RELIEF: THE PATH TO OPERATIONAL RESILIENCE",
            "visual_impact": "HIGH (Green/Blue Color Scheme, Rising Trend)",
            "solution_metric": f"{delta_z:,.0f} USD ($\Delta Z$: Risk Avoidance Value)",
            "summary_text": (
                f"hensam의 시스템은 규제 공백을 실시간으로 진단하여 최대 잠재 손실액 {red_alert_data['RedAlert']['core_metric']}에서 "
                f"최소한 {delta_z:,.0f} USD를 회피할 수 있게 합니다. 이는 단순 비용이 아닌 생존 의무입니다."
            ),
            "visual_props": ["Before/After Comparison Graph", "Green Checkmark Animation"]
        }

# =======================================================
# 테스트 실행 예시 (Mock Data 사용)
if __name__ == "__main__":
    print("="*60)
    print("⚡️ Z Risk Binding Script Test Simulation Start ⚡️")
    print("="*60)
    
    # Mock 데이터: 가상의 입력 변수 설정
    mock_inputs = {
        "industry": "Global Financial Services",
        "base_risk_factor": 100, # 기본 위험 지표
        "regulation_intensity": 0.8, # 규제 강도 (높을수록 높은 값)
        "market_dependency": 1.5 # 시장 의존성 (클수록 높은 값)
    }

    binder = ZRiskBinder(mock_inputs)
    final_output = binder.run_simulation()
    
    print("\n\n=============================================")
    print("🚀 SIMULATION COMPLETE: STAGED OUTPUT DATA")
    print("=============================================")
    print("이 JSON 구조를 각 슬라이드의 데이터 소스로 사용하세요.")
    print(json.dumps(final_output, indent=4))