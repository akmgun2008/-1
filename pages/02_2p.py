import streamlit as st

# 페이지 설정
st.set_page_config(page_title="느낀점", layout="centered")

# CSS로 배경/폰트/디자인 커스터마이즈
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Noto Sans KR', sans-serif;
    }

    body {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    }

    .container {
        background: white;
        padding: 60px 40px;
        border-radius: 12px;
        max-width: 800px;
        margin: 80px auto;
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
    }

    .title {
        font-size: 4em;
        font-weight: 700;
        text-align: center;
        margin-bottom: 50px;
        color: #333333;
    }

    .content {
        font-size: 1.1em;
        line-height: 1.8em;
        color: #444444;
        white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)

# 컨테이너
st.markdown("<div class='container'>", unsafe_allow_html=True)

# 제목
st.markdown("<div class='title'>느낀점</div>", unsafe_allow_html=True)

# 본문 그대로
st.markdown("""
<div class='content'>
이태완:개발을 할때 ai사용이 매우 효율적이란 것을 깨달았다. 또한 깃허브와 스트림릿이라는 프로그램을 상용해봄으로서 개발이나 코딩에대한 지식을 많이 알아간것 같다.:

홍의찬:ai가 정말 빠르게 발전해서 몇년전에는 사이트를 만들려면 고등학생 수준으로는 불가능하였는데 할수있어서 놀랐다 이젠 코딩을 배우는것보다 ai활용을 배우는것이 맞는것같다
</div>
""", unsafe_allow_html=True)

# 닫기
st.markdown("</div>", unsafe_allow_html=True)
