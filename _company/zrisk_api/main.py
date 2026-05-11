from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

# 로컬에서 핵심 비즈니스 로직을 가져옵니다.
from zrisk_api.services.zrisk_engine import calculate_z_risk, generate_report_json

app = FastAPI(title="Z Risk Simulator API", version="1.0")

# 요청 바디 구조 정의 (Pydantic Model 사용)
class SimulationInput(BaseModel):
    """
    /zrisk/simulate 엔드포인트로 전송될 데이터의 스키마를 정의합니다.
    이 구조는 openapi.yaml 명세서와 일치해야 합니다.
    """
    industry_type: str = Field(..., description="분석 대상 산업군 (예: Finance, Health)")
    regulatory_score: float = Field(..., ge=0.0, le=1.0, description="현재 규제 준수 점수 (0.0 ~ 1.0)")
    market_vulnerability_index: float = Field(..., ge=0.0, le=1.0, description="시장 취약성 지표 (0.0 ~ 1.0)")

@app.post("/zrisk/simulate")
async def simulate_z_risk(input_data: SimulationInput) -> dict:
    """
    주어진 변수들을 기반으로 Z Risk를 시뮬레이션하고 최종 보고서 JSON을 반환합니다.
    """
    try:
        # 1. Core Business Logic 호출 (Service Layer)
        z_data = calculate_z_risk(
            industry_type=input_data.industry_type,
            regulatory_score=input_data.regulatory_score,
            market_vulnerability_index=input_data.market_vulnerability_index
        )

        # 2. 최종 보고서 JSON 구조화 (Report Generation Layer)
        final_report = generate_report_json(
            industry=input_data.industry_type,
            z_data=z_data
        )

        return final_report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 예상치 못한 서버 오류 처리
        print(f"Error during simulation: {e}")
        raise HTTPException(status_code=500, detail="내부 서버 오류가 발생했습니다.")