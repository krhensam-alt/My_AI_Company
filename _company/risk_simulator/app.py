from flask import Flask, request, jsonify
import random

# --- 환경 설정 (Mocking) ---
app = Flask(__name__)

def calculate_z(data):
    """
    입력 데이터를 기반으로 Z 값을 계산하는 핵심 로직 시뮬레이션 함수.
    실제 복잡한 금융 모델을 단순화하여 구현함.
    """
    try:
        reg_strength = float(data['regulatory_strength_index'])
        market_dep = float(data['market_dependency_score'])
        industry = data['industry']

        # Z 계산 공식 시뮬레이션 (임의 가중치)
        base_risk = 10 * reg_strength * market_dep
        z_current = round(base_risk + random.uniform(5, 15), 2) # 현재 위험값
        delta_z = round(z_current * (reg_strength - 0.3), 2)   # 회피 가능 위험 감소분

        return z_current, delta_z
    except Exception:
        return None, None

@app.route('/api/v1/risk-simulation', methods=['POST'])
def simulate_risk():
    """
    실제 API 엔드포인트 모킹 함수. 
    JSON 입력 데이터를 받아 위험 분석을 수행하고 결과를 반환합니다.
    """
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "Invalid JSON payload."}), 400

    # 1. Z 값 계산
    z_current, delta_z = calculate_z(data)

    if z_current is None or delta_z is None:
         return jsonify({"success": False, "message": "Calculation failed due to invalid input types."}), 400


    # 2. Red Alert 상태 판별 (가장 중요한 애니메이션 트리거 정의 지점)
    # 예시 기준: Z 값이 임계치(30)를 넘거나, 규제 강도가 매우 높을 경우
    RED_ALERT_THRESHOLD = 30.0

    status = "NORMAL"
    summary = f"{data['industry']}의 운영 안정성은 현재 양호합니다."
    
    if z_current > RED_ALERT_THRESHOLD or data['regulatory_strength_index'] > 0.8:
        status = "RED_ALERT"
        summary = (f"🚨 CRITICAL WARNING! {data['industry']}는 잠재적 최대 손실액($Z$={z_current:.2f})이 임계치를 초과했습니다. 즉각적인 구조 개편이 필수입니다.")

    # 3. 결과 반환
    result = {
        "success": True,
        "status": status,  # <-- Designer가 이 값을 보고 애니메이션을 제어함
        "z_current": z_current,
        "delta_z": delta_z,
        "summary_text": summary,
        "explanation": f"규제 강도({data['regulatory_strength_index']:.2f})와 시장 의존성({data['market_dependency_score']:.2f})을 종합하여 $Z$를 계산했습니다."
    }

    return jsonify(result)

if __name__ == '__main__':
    # 로컬 테스트용 실행 명령어
    print("--- Risk Simulator Mockup API가 시작되었습니다. ---")
    print("테스트: http://127.0.0.1:5000/api/v1/risk-simulation (POST 요청 필요)")
    app.run(debug=True, port=5000)