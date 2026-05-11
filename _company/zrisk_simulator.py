import streamlit as st
import numpy as np
import pandas as pd

# --- [핵심 상수 및 함수 정의] ---

def calculate_delay_cost(base_value, delay_days, regulatory_complexity):
    """시간 지연 비용($Z$)을 계산하는 핵심 비즈니스 로직."""
    # Z Risk = Base Loss * (1 + Delay Cost Factor)^Delay Days * Regulatory Multiplier
    delay_factor = 1.05 ** delay_days # 기하급수적 증가 (exponential growth)
    z_risk = base_value * delay_factor * (1 + regulatory_complexity / 10)
    return z_risk

def get_status_color(score):
    """점수에 따른 시각적 상태를 결정합니다."""
    if score < 50:
        return "#2ECC71", "Operational Resilience 확보됨." # Green (Relief)
    elif 50 <= score < 200:
        return "#F39C12", "주의 필요. 즉각적인 점검이 요구됩니다." # Yellow (Warning)
    else:
        return "#C0392B", "CRITICAL ALERT! 운영 연속성 확보가 위협받고 있습니다." # Red (Fear/Danger)

# --- [Streamlit UX 컴포넌트] ---

st.set_page_config(layout="wide")
st.title("🚨 Z Risk Audit Dashboard: Interactive Simulation Module")
st.markdown("""
**[사용자 안내]:** 아래 변수들을 조작하여 시간 경과에 따른 잠재적 최대 손실액($Z$ Risk)의 변화를 체험하십시오. 이 시뮬레이션은 귀사가 현재 놓치고 있는 '시간 지체 비용(Delay Cost)'을 보여줍니다.
""")

# 1. 사이드바: 변수 입력 (User Input Area - The Control Panel)
st.sidebar.header("⚙️ 환경 변수 조작")

initial_base_loss = st.sidebar.slider(
    "기초 손실액 추정치 ($L_{base}$)", 
    min_value=10, max_value=300, value=100, step=5
)

delay_days = st.sidebar.slider(
    "가정된 대응 지연 기간 (Delay Days)", 
    min_value=0, max_value=60, value=30, step=5
)

regulatory_complexity = st.sidebar.slider(
    "규제 변경 복잡성 가중치 (Regulatory Complexity)", 
    min_value=1, max_value=5, value=3, step=1
)

# 2. 계산 및 상태 업데이트 (The Engine)
z_risk_score = calculate_delay_cost(initial_base_loss, delay_days, regulatory_complexity)
status_color, status_message = get_status_color(z_risk_score)

# 3. 메인 콘텐츠: 시각화 및 스토리텔링 (The Narrative Arc Display)
st.markdown("---")
col1, col2 = st.columns([0.65, 0.35])

with col1:
    st.header(f"📊 현재 $Z$ Risk 지표: {z_risk_score:,.0f} (Potential Max Loss)")
    st.metric(label="재무 위험 수준", value=f"{status_message}", delta="🚨")
    
    # 핵심 시각화 - Gauge/Progress Bar 형태 권장
    st.progress(min(1, z_risk_score / 500), color=status_color)
    
    st.subheader("⏱️ 기술 분석: Delay Cost의 작용 원리")
    st.info(f"""
**[분석 결과]:** $Z$ Risk는 단순히 현재 손실액이 아닙니다. **{delay_days}일 동안 대응이 지연될 때마다, 복잡한 규제 변화({regulatory_complexity}배)와 결합하여 기하급수적으로 증가**합니다. 이는 시간 자체가 가장 큰 비용입니다.
""")

with col2:
    st.markdown("---")
    st.subheader("📝 내러티브 흐름 (The Story)")
    if z_risk_score > 300 and delay_days >= 15:
        # 공포 유발 메시지 (Red Alert Trigger)
        st.warning("""
🚨 **[RED ALERT]** 현재의 지연 기간은 치명적입니다. 지금 이대로 가시면, 예상 손실액을 훨씬 초과합니다. 시간을 '구매'해야 합니다.
""")
    else:
        # Setup/Relief 메시지 (Normal Operation)
        st.success("""
✅ **[STATUS OK]** 현재는 관리 가능 범위 내에 있습니다. 하지만 변수는 언제든 바뀝니다. 선제적 관리가 필요합니다.
""")

# 4. CTA 영역 - 사용자 유도 (The Funnel Close)
st.markdown("---")
st.header("✨ 해결책: Operational Resilience 확보의 재무적 필수 비용")

if z_risk_score > 250 or delay_days >= 30:
    # 공포가 극대화되었을 때, 가장 강력한 CTA를 노출
    st.markdown(f"""
**[CTA 1] 즉시 진단 (Loss Aversion Trigger):** $Z$ Risk의 원인을 정확히 파악해야 합니다. 저희는 귀사의 **'운영 안정성 점수(Operational Resilience Score)'**를 무료로 산정해 드립니다.
""")
    st.button("🔬 [무료 다운로드] Z Risk Audit Checklist 및 Preliminary Scoring Report 받기", key="cta1")
    st.markdown("""
*(이 보고서에는 귀사가 즉시 개선해야 할 Top 3 취약 영역과 그로 인한 예상 Delay Cost가 포함되어 있습니다.)*""")
else:
    # 낮은 위험도일 때, 교육적/점진적인 CTA 노출
    st.info("더 깊은 분석을 원하시면, 저희의 전문 컨설팅 서비스를 통해 맞춤형 'Delay Cost' 시뮬레이션을 경험하십시오.")