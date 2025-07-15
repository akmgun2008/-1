import streamlit as st
import pandas as pd
import plotly.express as px

# 앱 제목
st.title("🔋 Global EV Sales Dashboard")
st.write("데이터 출처: IEA EV Sales Historical Cars")

# 데이터 로드 (파일명을 꼭 확인!)
df = pd.read_csv("ev_sales.csv")

# EV sales 데이터만 필터
df_sales = df[(df["parameter"] == "EV sales") & (df["unit"] == "Vehicles")]

# 연도 선택 슬라이더
min_year = int(df_sales["year"].min())
max_year = int(df_sales["year"].max())
year = st.slider("연도 선택", min_year, max_year, max_year)

df_year = df_sales[df_sales["year"] == year]

# ---------------------------
# 1) 연도별 선 그래프 (글로벌)
# ---------------------------
global_sales = df_sales.groupby("year")["value"].sum().reset_index()

fig_line = px.line(
    global_sales,
    x="year",
    y="value",
    markers=True,
    title="📈 Global EV Sales Over Time",
    labels={"year": "Year", "value": "EV Sales (Vehicles)"},
)

st.plotly_chart(fig_line, use_container_width=True)

# ---------------------------
# 2) 선택한 연도 지도 (나라별)
# ---------------------------
fig_map = px.choropleth(
    df_year,
    locations="region",           # 지역 컬럼 (나라 이름)
    locationmode="country names", # 나라 이름을 Plotly에 매칭
    color="value",
    color_continuous_scale="Blues",
    title=f"🌍 {year} EV Sales by Country",
    labels={"value": "EV Sales (Vehicles)", "region": "Country"},
)

fig_map.update_geos(fitbounds="locations", visible=False)

st.plotly_chart(fig_map, use_container_width=True)

# ---------------------------
# 원본 데이터 (옵션)
# ---------------------------
with st.expander("🔍 원본 데이터 보기"):
    st.write(df.head())
