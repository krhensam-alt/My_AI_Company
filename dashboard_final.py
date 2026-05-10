import streamlit as st
import pandas as pd
import numpy as np

# ==============================================================
# 🚩 [핵심 로직: RiskEngine - 외부 API 의존성을 제거한 시뮬레이션 모듈]
# 이 함수는 '잠재적 최대 손실액(Z)'을 계산하는 코어 엔진입니다.
# 입력 값에 따라 최종 $Z$ 값을 도출합니다. (단위: 백만 원)
def calculate_risk(industry, regulation_strength, market_dependency):
    """
    주어진 변수를 기반으로 최대 잠재 손실액 Z와 위험 회피분 Delta_Z를 계산합니다.

    Args:
        industry (str): 산업군 (예: 금융, 의료) - 리스크 기본값 결정
        regulation_strength (float): 규제 강도 계수 (0.1 ~ 1.0)
        market_dependency (float): 시장 의존성 지표 (0.1 ~ 1.0)

    Returns:
        tuple: (Z_current, Delta_Z)
    """
    # 1. 산업별 기본 위험 계수 정의 (가정적 데이터베이스 역할)
    base_risk = {
        "금융": 1200,  # 금융권은 구조적으로 높은 리스크를 가짐
        "의료": 850,   # 의료는 규제 변수가 복잡하여 중간 수준
        "IT/테크": 600, # 기술 변화가 빠르나 규제가 상대적으로 적음 (상대적)
        "소매": 400     # 소매업은 시장 변수에 민감하지만, 구조적 리스크는 낮음
    }

    base_z = base_risk.get(industry, 500) # 기본값 설정
    
    # 2. 핵심 손실 계산 로직 (가정: Z는 기본 위험에 규제와 의존성이 곱해져 증폭됨)
    # Danger: 변수들이 높을수록 Z 값이 기하급수적으로 증가함
    z_current = base_z * ((1 + regulation_strength)**2 * market_dependency)
    
    # 3. 해결책 도입 후 위험 감소분 (Delta_Z): 솔루션의 효과가 크다고 가정하고 계산
    # Delta Z는 규제 및 시장 변수의 제곱근에 비례하여 감소한다고 설정합니다.
    delta_z = np.sqrt(regulation_strength) * base_z * 0.8 + 150 # 최소한의 개선분 보장

    return round(z_current, 2), round(max(delta_z, 50), 2)

# ==============================================================
# 🖥️ Streamlit UI/UX 및 시연 로직
def main():
    st.set_page_config(layout="wide", page_title="Z Risk Audit Report Prototype")

    # --- [전체 레이아웃 정의: 재무 감사 보고서 스타일] ---
    st.markdown("""
        <style>
        /* 권위적이고 진지한 폰트 설정 */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;700&display=swap');
        body { font-family: 'Noto Sans KR', sans-serif; }
        /* 경고 섹션 스타일 */
        .danger-box { 
            background-color: #ffe6e6; /* 연한 빨간 배경 */
            border: 3px solid #CC0000; /* 강렬한 빨간색 테두리 */
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 10px;
        }
        .danger-box h2 { color: #CC0000; }
        /* 안도 섹션 스타일 */
        .relief-box { 
            background-color: #e6ffe6; /* 연한 녹색 배경 */
            border: 3px solid #008000; /* 강렬한 초록색 테두리 */
            padding: 20px;
            margin-top: 20px;
            border-radius: 10px;
        }
        .relief-box h2 { color: #006400; }
        /* 주요 지표 강조 스타일 */
        .metric-card {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("🚨 Z Risk Audit Report (Proto Type)")
    st.markdown("---")
    st.caption("본 보고서는 고객사의 잠재적 최대 손실액(Z)을 계량적으로 분석하는 시뮬레이션 결과입니다. 모든 수치는 가상 변수를 기반으로 합니다.")

    # --- [1단계: 사용자 입력 (좌측 컨트롤 영역)] ---
    with st.sidebar:
        st.header("🔍 리스크 진단 변수 입력")
        st.markdown("핵심 위험 요소를 3가지 차원에서 설정해주세요.")
        
        industry_input = st.selectbox(
            "1. 산업군 (Industry)",
            options=["금융", "의료", "IT/테크", "소매"],
            help="산업군은 기본 리스크 레벨을 결정합니다."
        )
        
        regulation_strength_input = st.slider(
            "2. 규제 강도 계수 (Regulation Strength, 0.1~1.0)",
            min_value=0.1, max_value=1.0, value=0.6, step=0.1,
            help="규제가 강화될수록 Z는 비선형적으로 증가합니다."
        )

        market_dependency_input = st.slider(
            "3. 시장 의존성 지표 (Market Dependency, 0.1~1.0)",
            min_value=0.1, max_value=1.0, value=0.7, step=0.1,
            help="외부 시장 변동에 대한 취약도를 나타냅니다."
        )

    # --- [2단계: 핵심 로직 실행 및 결과 도출] ---
    z_current, delta_z = calculate_risk(industry_input, regulation_strength_input, market_dependency_input)

    # --- [3단계: 시각적 임팩트 전달 (메인 영역)] ---
    col1, col2 = st.columns([0.65, 0.35]) # Z Current가 더 크게 보이도록 레이아웃 조정

    with col1:
        st.markdown("""
        <div class="danger-box">
            <h2>🔴 [STEP 1] 잠재적 최대 손실액 (Z_current) 분석</h2>
            <p>현재의 리스크 요인(규제, 시장 의존성 등)이 결합되었을 때, 회사가 직면할 수 있는 **최대 재무적 위험 규모**입니다. 이는 비용 절감 문제가 아닌 '존속 가능성'에 대한 문제입니다.</p>
        </div>
        """, unsafe_allow_html=True)

        # Z Current Display
        st.metric(label="현재 잠재 최대 손실액 (Z_current)", 
                  value=f"{z_current:,.0f} 만 원", 
                  delta=f"🚨 위험 경고! ({industry_input} 기준)")

        st.subheader("📊 리스크 지표 분포 시뮬레이션")
        # 그래프 출력 - 현재의 불안감(Danger)을 극대화
        fig = {
            'Data': [z_current, 0], # Z와 0을 비교하여 위험도를 부각
            'Labels': ['현재', '기준'],
            'Colors': ['#CC0000', '#AAAAAA']
        }
        st.markdown(f"""<div style="text-align: center; margin-top: 20px;">
            <h3 style="color: #CC0000;">⚠️ 위험 수준 지표</h3>
            <p>Z_current가 높을수록 그래프의 빨간색 면적이 커집니다.</p>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="relief-box">
            <h2>🟢 [STEP 2] 위험 회피 가치 (Delta Z) 제시</h2>
            <p>우리의 솔루션(Risk Hedge System)을 도입하여 잠재적 리스크를 관리했을 때, **회피 가능한 최소 손실액 감소분**입니다. 이는 곧 '안정성 확보 보험'의 가치를 의미합니다.</p>
        </div>
        """, unsafe_allow_html=True)

        # Delta Z Display (가장 눈에 띄게)
        st.metric(label="회피 가능한 위험 감소분 (ΔZ)", 
                  value=f"{delta_z:,.0f} 만 원", 
                  delta=f"✅ 안정성 확보! ({round((delta_z/z_current)*100, 1)}% 절감)")


    # --- [4단계: 결론 및 행동 유도] ---
    st.markdown("---")
    st.header("📈 최종 감사 보고서 요약 (Actionable Insight)")

    colA, colB = st.columns(2)

    with colA:
        st.subheader("🔬 핵심 진단 포인트:")
        st.info(f"**{industry_input} 산업군은 {z_current:,.0f} 만 원의 Z 리스크에 노출되어 있습니다.**")
        st.warning("현재는 규제 및 시장 변동성을 예측하고 선제적으로 대응할 '운영 안정성 확보'가 시급합니다.")

    with colB:
        st.subheader("💰 제안 가치 (Our Value Proposition):")
        st.success(f"당사의 솔루션을 통해 **최소 {delta_z:,.0f} 만 원**의 잠재적 손실을 회피할 수 있습니다.")

    # 사용법 안내
    st.markdown("---")
    st.caption("💡 **사용 방법:** 사이드바에서 3가지 변수를 조정하며, Z_current와 Delta_Z가 어떻게 논리적으로 변화하는지 실시간으로 확인하세요.")


if __name__ == "__main__":
    main()