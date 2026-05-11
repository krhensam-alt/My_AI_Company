from flask import Flask, request, jsonify
import uuid
from pydantic import BaseModel
# ReportLab은 PDF 생성을 위해 사용한다고 가정합니다. 실제 환경에서는 설치 후 임포트해야 함.
# from reportlab.pdfgen import canvas 

app = Flask(__name__)

# --- 데이터 구조 정의 (Input Validation) ---
class RiskData(BaseModel):
    """API 입력으로 받는 핵심 리스크 데이터 구조."""
    industry_sector: str  # 예: 금융, 제조
    regulatory_compliance_score: float # 규제 준수 점수 (0.0 ~ 1.0)
    market_dependency_index: float # 시장 의존성 지표
    initial_risk_estimate: float # 초기 추정 손실액 Z_initial

# --- 핵심 상태 관리 로직 ---
def calculate_z_risk(data: RiskData, stage: str):
    """입력된 데이터와 현재 단계를 기반으로 잠재적 최대 손실액(Z)을 계산합니다."""
    base_loss = data.initial_risk_estimate * (1 + data.market_dependency_index * 0.5)
    
    if stage == "DANGER":
        # 규제 미준수 시나리오: 점수가 낮을수록 Z가 기하급수적으로 증가합니다.
        compliance_penalty = (1 - data.regulatory_compliance_score) ** 2 * 1000
        z_current = base_loss + compliance_penalty
        delta_z = z_current # 초기 대비 최대 손실액으로 설정
        return {"status": "ALERT", "Z_value": round(z_current, 2), "Delta_Z": round(delta_z, 2)}
    
    elif stage == "RELIEF":
        # 솔루션 도입 시나리오: Z 값을 일정 비율로 감소시킵니다. (예: 40% 감소)
        reduction_factor = 0.6 # 60% 위험 회피
        z_final = base_loss * reduction_factor
        delta_z = round(base_loss - z_final, 2) # 회피 가능액 계산
        return {"status": "SAFE", "Z_value": round(z_final, 2), "Delta_Z": round(delta_z, 2)}

    else: # NARRATIVE PAUSE 또는 초기 상태
        return {"status": "PENDING", "Z_value": base_loss}


@app.route('/api/v3/audit_flow', methods=['POST'])
def audit_flow_endpoint():
    """
    Z Risk Audit Dashboard의 핵심 내러티브 흐름을 제어하는 API 게이트웨이.
    (Red Alert -> Narrative Pause -> Relief 시퀀스 강제)
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON data missing"}), 400

        # Pydantic을 이용한 입력 유효성 검사 및 객체화
        risk_input = RiskData(**data)

    except Exception as e:
        return jsonify({"error": f"Invalid input data format or missing fields. {e}"}), 400


    # --- 1단계: Danger (위험 인지 극대화) ---
    danger_result = calculate_z_risk(risk_input, "DANGER")
    if danger_result['status'] != 'ALERT':
        return jsonify({"error": "Failed to enter Danger stage."}), 500

    # --- 2단계: Narrative Pause (문제 제기 및 질문 유도) ---
    pause_data = {
        "stage": "NARRATIVE_PAUSE",
        "message": f"현재 규제 미준수 리스크(Z={danger_result['Z_value']})가 확인되었습니다. 이 격차를 어떻게 메울 것입니까?",
        "required_input": ["SOLUTION_PLAN"] # 다음 액션을 요구하는 지점
    }

    # --- 3단계: Relief (해결책 제시) ---
    relief_result = calculate_z_risk(risk_input, "RELIEF")

    # API 응답 구조 설계: 프론트엔드가 이 순서대로 데이터를 소비하며 시각적 변화를 일으키도록 합니다.
    response = {
        "success": True,
        "sequence": [
            {"stage": "DANGER", "data": danger_result, "visual_hint": "Red Alert Overlay Activated"},
            {"stage": "PAUSE", "data": pause_data, "visual_hint": "Focus on Questioning (Gap Analysis)"},
            {"stage": "RELIEF", "data": relief_result, "visual_hint": "Green Relief Gradient Applied"}
        ],
        "metadata": {
            "session_id": str(uuid.uuid4()), # 시연마다 고유 세션 ID 부여 (추적 및 기록용)
            "audit_timestamp": "2026-05-11T12:30:00Z"
        }
    }

    return jsonify(response)


@app.route('/api/v3/generate_evidence', methods=['POST'])
def generate_evidence():
    """
    데모의 가장 충격적인 결과물(Audit Evidence)을 PDF 형태로 즉시 생성합니다. 
    이는 기술적 시연 효과를 극대화하기 위한 핵심 기능입니다.
    """
    data = request.get_json()
    if not data or 'final_z' not in data:
        return jsonify({"error": "Missing final Z value for evidence generation."}), 400

    # 실제 ReportLab 로직이 들어가야 하지만, 여기서는 성공적인 엔드포인트 존재를 증명하는 Mockup으로 대체합니다.
    evidence_id = f"audit_evidence_{uuid.uuid4().hex[:8]}.pdf"
    
    print(f"[SYSTEM] Generating High-Fidelity Audit Evidence: {evidence_id}")
    # 실제로는 PDF 파일 스트림을 반환해야 함 (response(stream=...) 사용)
    return jsonify({
        "success": True, 
        "message": f"Audit Evidence '{evidence_id}'가 성공적으로 생성되었습니다. (진정한 감사의 기록)",
        "file_path": f"/temp/assets/{evidence_id}"
    })


if __name__ == '__main__':
    # 이 API는 실제 데모 시연 환경에서 호출될 것입니다.
    print("--- Z Risk Audit Dashboard V3 Narrative API 가동 ---")
    app.run(debug=True, port=5001)