from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from src.zrisk_engine import ZRiskEngine, InputData, ZRiskSimulationReport

# --- API 스키마 정의 (요청/응답) ---
class RiskInput(BaseModel):
    """API 요청 본문(Body)의 구조를 정의합니다."""
    industry_sector: str
    compliance_weakness_score: float
    market_dependency_index: float

app = FastAPI(
    title="hensam Z-Risk Simulation API",
    description="Z Risk PoC 시뮬레이터 백엔드 엔드포인트. 재무적 손실 예측 및 위험 감소 과정을 구조화된 JSON으로 반환합니다.",
)

@app.post("/api/v1/calculate_zrisk", response_model=ZRiskSimulationReport)
async def calculate_zrisk(input: RiskInput):
    """
    사용자가 제공한 데이터를 기반으로 Z Risk 시뮬레이션을 실행하고, 
    진단 전 위험($Z_{current}$)과 솔루션 적용 후 감소분($\Delta Z$)을 계산합니다.
    """
    try:
        # Pydantic 모델로 변환하여 엔진에 전달 (데이터 유효성 검사 보장)
        data_model = InputData(**input.model_dump())

        # 코어 엔진 실행
        report = ZRiskEngine.run_simulation(data_model)
        return report
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"데이터 처리 중 오류 발생: {e}")

@app.get("/health")
def health_check():
    """API 서버 상태 확인용 엔드포인트."""
    return {"status": "ok", "service": "ZRiskEngine API Operational"}


if __name__ == "__main__":
    # 로컬 테스트 실행 명령어 (uvicorn main_api:app --reload)
    print("=====================================================")
    print("✅ Z Risk PoC Simulator Backend Ready.")
    print("🚀 서버를 시작하려면 다음 명령어를 사용하세요:")
    print("   uvicorn main_api:app --reload")
    print("=====================================================")