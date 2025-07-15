import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="프로젝트 동기",
    page_icon="🚗",
    layout="wide"
)

# 제목
st.title("📘 프로젝트 동기")
st.markdown("---")

# 본문 출력 (원문 그대로, HTML 카드 스타일 적용)
st.markdown("""
<div style="
    background-color: #f4f4f4;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    font-size: 18px;
    line-height: 1.8;
    color: #333;">
    요즘 자동차 시장의 주요 목표 중 하나는 전체 생산량의 대부분을 전기자동차로 전환하는 것입니다.<br><br>
    전기자동차는 탄소 배출이 없어 환경에 더 친화적이기 때문에, 각국 정부에서도 전기자동차 사용을 적극 장려하고 있습니다.<br><br>
    이는 많은 국가들이 실제로 추진 중인 정책이기도 하며, 이러한 점에서 전기자동차는 지속가능한 발전이라는 주제와 관련이 있다고 생각되어 선택하게되었습니다.
</div>
""", unsafe_allow_html=True)

# 하단 여백
st.markdown(" ")
st.markdown("---")
st.caption("Made with Streamlit 🚀")
