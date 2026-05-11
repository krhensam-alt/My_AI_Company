from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/zrisk/simulate', methods=['POST'])
def zrisk_simulate():
    """
    Z Risk 시뮬레이터의 가짜(Mock) 백엔드 엔드포인트입니다.
    프론트엔드의 통합 테스트 및 에러 핸들링 검증에 사용됩니다.
    """
    data = request.get_json()

    # 1. 필수 입력값 유효성 검사 (400 Bad Request 시나리오)
    if not data:
        return jsonify({
            "status": "error",
            "code": 400,
            "message": "요청 본문(Request Body)이 비어 있습니다. JSON 데이터를 전송해주세요.",
            "details": ["'operational_resilience'와 'regulatory_risk_score' 필드가 필수입니다."]
        }), 400

    required_fields = ['operational_resilience', 'regulatory_risk_score']
    if not all(field in data for field in required_fields):
         return jsonify({
            "status": "error",
            "code": 400,
            "message": f"필수 입력 필드가 누락되었습니다. 다음 중 빠진 값이 있습니다: {', '.join([f'"{f}"' for f in required_fields])}",
        }), 400

    # 2. 시나리오 분기 로직 (실제 비즈니스 로직 대신 테스트 구조만 구현)
    try:
        op_res = data['operational_resilience']
        reg_risk = data['regulatory_risk_score']

        # A. 정상 케이스 (Success Scenario - 200 OK)
        if op_res > 0.7 and reg_risk < 30:
            return jsonify({
                "status": "success",
                "code": 200,
                "message": "Z Risk 시뮬레이션이 성공적으로 완료되었습니다.",
                "data": {
                    "z_current": round(op_res * reg_risk / 10 + 50, 2), # 초기 손실액 (예시)
                    "delta_z": round((op_res - 0.3) * 10 + 40, 2),   # 회피 가치 (예시)
                    "risk_level": "Green Relief",
                    "report_summary": f"운영 연속성 및 규제 리스크 모두 양호합니다. $\Delta Z$는 {round((op_res - 0.3) * 10 + 40, 2)}로 예측됩니다.",
                    "simulation_timestamp": "2026-05-12T10:00:00Z"
                }
            }), 200

        # B. 경고 케이스 (Warning Scenario - 200 OK, 하지만 낮은 점수)
        elif op_res < 0.4 or reg_risk > 60:
             return jsonify({
                "status": "warning",
                "code": 200,
                "message": "경고: 주요 리스크 영역이 감지되었습니다. 추가 분석이 필요합니다.",
                "data": {
                    "z_current": round(op_res * reg_risk / 10 + 50, 2),
                    "delta_z": 0.0, # 회피 가치 없음 (추가 조치가 필요함을 암시)
                    "risk_level": "Red Alert",
                    "report_summary": "현재 운영 연속성 및 규제 리스크의 조합으로 인해 높은 잠재 손실액이 예상됩니다.",
                }
            }), 200

        # C. 내부 오류 시뮬레이션 (500 Internal Error Scenario)
        else:
             return jsonify({
                "status": "error",
                "code": 500,
                "message": "서버 측에서 예상치 못한 오류가 발생했습니다.",
                "details": ["데이터 포맷 또는 내부 로직 처리 중 예외가 발생함. 관리자에게 문의해주세요."]
            }), 500


    except Exception as e:
        # 최종적으로 포착되지 않은 시스템 오류 (예: JSON 파싱 실패 등)
        return jsonify({
            "status": "error",
            "code": 500,
            "message": f"시스템 처리 중 치명적인 오류 발생: {str(e)}",
            "details": ["클라이언트 측에서 전송한 데이터 형식을 확인해 주세요."]
        }), 500

if __name__ == '__main__':
    # 개발 및 테스트용으로 디버그 모드를 활성화합니다.
    app.run(debug=True, port=5001) # 포트를 명시하여 충돌 방지