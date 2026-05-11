import streamlit as st
import numpy as np
import pandas as pd

# ==============================================================
# 🚨 Z Risk Audit Dashboard V3 - Prototype Core Engine
# 이 모듈은 실제 외부 API와 연결되지 않으며, 시연 효과 극대화에 초점을 맞춥니다.
# ==============================================================

def calculate_z_risk(industry: str, regulatory_score: float, market_dependency: float):
    """
    Z 리스크를 계산하는 코어 엔진 (모킹 버전).
    규제 준수 실패 패널티와 시장 의존성을 핵심 변수로 사용합니다.
    """
    # 1. 기본 위험 점수 산출 (가정: 산업군별 베이스 라인)
    base_risk = {
        "금융": 0.85,  # 금융은 규제 리스크가 높음
        "헬스케어": 0.60,
        "에너지": 0.75,
        "기타": 0.50
    }.get(industry, 0.50)

    # 2. 패널티 가중치 적용 (Regulatory Gap = 핵심 위협)
    regulatory_penalty = base_risk * regulatory_score * 1.5 # 규제 점수가 높을수록 페널티 극대화
    
    # 3. 시장 의존성 및 복합 리스크 결합
    complex_risk = (base_risk + regulatory_penalty) * market_dependency

    # 최종 잠재 최대 손실액 Z (0부터 1 사이의 값으로 정규화하여 사용)
    Z_current = min(1.0, complex_risk / 2.5) # 최대치를 1로 제한

    # 개선된 솔루션 도입 후 회피 가능한 위험 감소분 Delta Z 계산
    Delta_Z = (Z_current * 0.6) + np.random.uniform(0.1, 0.3) # 최소한의 개선효과 보장

    return Z_current, Delta_Z, base_risk


def display_red_alert_overlay(z_current: float):
    """L2 단계에서 작동하는 'Red Alert Overlay' 시뮬레이션 함수."""
    if z_current > 0.75:
        st.markdown("""
        <div style="background-color: #8B0000; color: white; padding: 15px; border-radius: 10px; text-align: center;">
            <h1>🚨 CRITICAL WARNING: RED ALERT TRIGGERED! 🚨</h1>
            <p style="font-size: 1.2em;">현재 잠재 최대 손실액($Z$)이 임계치(0.75)를 초과했습니다.</p>
            <p style="margin-top: 10px; font-weight: bold;">즉각적인 리스크 점검 및 대응책 수립이 필수적입니다.</p>
        </div>
        """, unsafe_allow_html=True)

def narrative_pause(z_current: float):
    """L2 단계에서 발생하는 'Narrative Pause' 시뮬레이션 함수."""
    st.markdown("---")
    st.warning("""
    ⚠️ **[NARRATIVE PAUSE]** ⚠️<br>
    잠시, 청중의 집중을 극대화해야 합니다. 데이터를 보여주기 전에, *이 위험이 실제로 어떤 결과를 초래할지*에 대한 감정적 공포감을 조성하는 것이 중요합니다.<br><br>
    (여기서 잠시 침묵하며 다음 슬라이드로 넘어갑니다...)
    """)

def main():
    st.set_page_config(layout="wide", page_title="Z Risk Audit Dashboard V3 Prototype")
    st.title("🛡️ Z Risk Audit Dashboard V3: Interactive Simulation")
    st.markdown("""
        *본 프로토타입은 규제 리스크 회피 가치($\text{Potential Maximum Loss}$)를 시뮬레이션하며, 최고의 데모 임팩트를 위해 설계되었습니다.*
    """)

    # -------------------- INPUTS (L1: Danger Zone 설정) --------------------
    st.sidebar.header("🔍 진단 입력 변수 (L1)")
    industry = st.sidebar.selectbox(
        "산업군 선택", 
        options=["금융", "헬스케어", "에너지", "기타"],
        help="가장 규제 변화가 활발한 산업을 선택하세요."
    )
    regulatory_score = st.sidebar.slider(
        "규제 준수 미준수 위험 지표 (0.0 ~ 1.0)", 
        min_value=0.0, max_value=1.0, value=0.8, step=0.05,
        help="최근 규제 변화의 강도를 나타냅니다. 높을수록 리스크가 커집니다."
    )
    market_dependency = st.sidebar.slider(
        "시장 의존성 및 투명성 지표 (0.0 ~ 1.0)", 
        min_value=0.0, max_value=1.0, value=0.7, step=0.05,
        help="외부 시장 변수에 대한 의존도가 높을수록 리스크가 커집니다."
    )

    # -------------------- CORE CALCULATION (L2: Red Alert Trigger) --------------------
    Z_current, Delta_Z, base_risk = calculate_z_risk(industry, regulatory_score, market_dependency)

    st.header("📊 규제 리스크 진단 결과")
    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        # Red Alert Overlay 시뮬레이션 호출 (가장 먼저 실행되어야 함)
        display_red_alert_overlay(Z_current)
        
        st.subheader("❌ 현재 잠재 최대 손실액 ($Z_{Current}$)")
        st.metric(label="잠재적 최대 재무 손실액", value=f"{Z_current*100:.1f}%", delta=f"[{base_risk*100:.1f}% Base]")

    with col2:
        # Narrative Pause 시뮬레이션 호출 (시각적 효과 후 작동)
        narrative_pause(Z_current) 
        
        st.subheader("✅ 회피 가능 리스크 감소분 ($\Delta Z$)")
        st.success(f"{Delta_Z*100:.1f}% 감소 예상", icon="📈")

    # -------------------- CONCLUSION (L3: Relief & CTA) --------------------
    st.markdown("""
    ***<br>***
    **[CONCLUSION - L3]** 현 분석 결과, 귀사의 핵심 취약점은 **'규제 시스템의 구조적 불투명성'** 입니다. hensam 솔루션 도입 시, 이 리스크를 체계적으로 모니터링하고 사전에 경고함으로써 최대 손실액을 효과적으로 회피할 수 있습니다.
    """)

if __name__ == "__main__":
    main()