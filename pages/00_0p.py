import streamlit as st
import time

# 페이지 설정
st.set_page_config(
    page_title="전기차의 전망",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사이드바 네비게이션
st.sidebar.title("📋 목차")
st.sidebar.markdown("""
- 🏠 **메인 페이지**
- 📊 데이터 분석
- 📈 시장 동향
- 🔮 미래 전망
- 📝 결론
""")

# 메인 타이틀
st.markdown("""
<div style="text-align: center; padding: 50px 0;">
    <h1 style="font-size: 4rem; color: #2E86AB; margin-bottom: 30px;">
        ⚡ 전기차의 전망 🚗
    </h1>
    <h2 style="color: #A23B72; margin-bottom: 40px;">
        Electric Vehicle Market Outlook
    </h2>
</div>
""", unsafe_allow_html=True)

# 구분선
st.markdown("---")

# 발표자 정보
st.markdown("""
<div style="text-align: center; padding: 30px 0;">
    <h3 style="color: #F18F01; margin-bottom: 30px;">👥 발표자</h3>
    <div style="display: flex; justify-content: center; gap: 100px; flex-wrap: wrap;">
        <div style="text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 15px; color: white; min-width: 200px;">
            <h4 style="margin: 0; font-size: 1.5rem;">20729</h4>
            <h3 style="margin: 10px 0; font-size: 2rem;">홍의찬</h3>
        </div>
        <div style="text-align: center; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 15px; color: white; min-width: 200px;">
            <h4 style="margin: 0; font-size: 1.5rem;">20722</h4>
            <h3 style="margin: 10px 0; font-size: 2rem;">이태완</h3>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 구분선
st.markdown("---")

# 발표 개요
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f0f8ff; border-radius: 10px;">
        <h3 style="color: #1f4e79;">🎯 발표 목적</h3>
        <p style="font-size: 1.1rem;">전기차 시장의 현재와 미래를 데이터 기반으로 분석하여 시장 전망을 제시</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #f0fff0; border-radius: 10px;">
        <h3 style="color: #2d5a27;">📊 분석 범위</h3>
        <p style="font-size: 1.1rem;">글로벌 전기차 판매 데이터, 시장 동향, 기술 발전 현황 분석</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 20px; background-color: #fff5f5; border-radius: 10px;">
        <h3 style="color: #8b0000;">🔍 주요 내용</h3>
        <p style="font-size: 1.1rem;">시장 성장률, 지역별 현황, 미래 예측 및 투자 전략 제안</p>
    </div>
    """, unsafe_allow_html=True)

# 공백
st.markdown("<br><br>", unsafe_allow_html=True)

# 시작 버튼
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🚀 발표 시작하기", key="start_presentation"):
        st.balloons()
        time.sleep(1)
        st.success("✅ 발표를 시작합니다!")
        st.info("👈 사이드바에서 다음 페이지로 이동하세요!")

# 푸터
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>📅 발표 일시: 2025년 7월 15일</p>
    <p>🛠️ 개발 도구: Streamlit, Python, GitHub</p>
    <p>📧 문의: 발표자 이메일</p>
</div>
""", unsafe_allow_html=True)
