import streamlit as st

# 페이지 설정
st.set_page_config(page_title="느낀점", layout="centered")

# 컬러풀 + 폰트 + 배경 CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
    }

    body {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
    }

    .container {
        background: rgba(255, 255, 255, 0.9);
        padding: 60px 40px;
        border-radius: 15px;
        max-width: 800px;
        margin: 80px auto;
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
        border: 4px solid #ffb347;
    }

    .title {
        font-size: 4em;
        font-weight: 900;
        text-align: center;
        margin-bottom: 50px;
        color: #ff6f61;
    }

    .content {
        font-size: 1.2em;
        line-height: 1.8em;
        color: #333333;
        white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)

# 컨테이너 시작
st.markdown("<div class='container'>", unsafe_allow_html=True)

# 제목
st.markdown("<div class='title'>느낀점</div>", unsafe_allow_html=True)

# 본문 - 그대로
st.markdown("""
<div class='content'>
이태완:개발을 할때 ai사용이 매우 효율적이란 것을 깨달았다. 또한 깃허브와 스트림릿이라는 프로그램을 상용해봄으로서 개발이나 코딩에대한 지식을 많이 알아간것 같다.:

홍의찬:ai가 정말 빠르게 발전해서 몇년전에는 사이트를 만들려면 고등학생 수준으로는 불가능하였는데 할수있어서 놀랐다 이젠 코딩을 배우는것보다 ai활용을 배우는것이 맞는것같다
</div>
""", unsafe_allow_html=True)

# 컨테이너 닫기
st.markdown("</div>", unsafe_allow_html=True)
