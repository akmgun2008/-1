import streamlit as st

# 페이지 설정
st.set_page_config(page_title="느낀점", layout="centered")

# CSS로 배경색 + 약간의 꾸밈
st.markdown("""
    <style>
    body {
        background-color: #f5f5f5;
    }
    .container {
        background-color: white;
        padding: 50px;
        border-radius: 10px;
        max-width: 800px;
        margin: auto;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
    }
    .title {
        font-size: 4em;
        font-weight: normal;
        text-align: center;
        margin-bottom: 50px;
    }
    .content {
        font-size: 1em;
        white-space: pre-wrap;
    }
    </style>
""", unsafe_allow_html=True)

# 컨테이너 박스
st.markdown("<div class='container'>", unsafe_allow_html=True)

# 제목
st.markdown("<div class='title'>느낀점</div>", unsafe_allow_html=True)

# 본문 (사용자 글 그대로)
st.markdown("""
<div class='content'>
이태완:개발을 할때 ai사용이 매우 효율적이란 것을 깨달았다. 또한 깃허브와 스트림릿이라는 프로그램을 상용해봄으로서 개발이나 코딩에대한 지식을 많이 알아간것 같다.:
<br><br>
홍의찬:ai가 정말 빠르게 발전해서 몇년전에는 사이트를 만들려면 고등학생 수준으로는 불가능하였는데 할수있어서 놀랐다 이젠 코딩을 배우는것보다 ai활용을 배우는것이 맞는것같다
</div>
""", unsafe_allow_html=True)

# 컨테이너 박스 닫기
st.markdown("</div>", unsafe_allow_html=True)
