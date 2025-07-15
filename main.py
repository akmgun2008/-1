import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 앱 제목
st.title("🔋 전기차 판매량 대시보드")

# 데이터 로드
df = pd.read_csv("IEA-EV-dataEV salesHistoricalCars - IEA-EV-dataEV salesHistoricalCars.csv")

# EV sales 데이터만 필터
df_sales = df[(df["parameter"] == "EV sales") & (df["unit"] == "Vehicles")]

# 국가 이름 표준화
country_mapping = {
    'United States': 'United States',
    'USA': 'United States',
    'US': 'United States',
    'Korea': 'South Korea',
    'Republic of Korea': 'South Korea',
    'Russian Federation': 'Russia',
    'Czech Republic': 'Czechia',
    'Slovak Republic': 'Slovakia',
    'Türkiye': 'Turkey',
    'United Kingdom': 'United Kingdom',
    'UK': 'United Kingdom',
    'Iran (Islamic Republic of)': 'Iran',
    'Venezuela (Bolivarian Republic of)': 'Venezuela',
    'Bolivia (Plurinational State of)': 'Bolivia',
    'Tanzania (United Republic of)': 'Tanzania',
    'Moldova (Republic of)': 'Moldova',
    'Macedonia (the former Yugoslav Republic of)': 'North Macedonia',
    'Congo (Democratic Republic of the)': 'Democratic Republic of the Congo',
    'Côte d\'Ivoire': 'Ivory Coast',
    'Lao People\'s Democratic Republic': 'Laos',
    'Syrian Arab Republic': 'Syria',
    'Viet Nam': 'Vietnam',
    'Republic of China (Taiwan)': 'Taiwan',
    'Hong Kong SAR, China': 'Hong Kong',
    'Macao SAR, China': 'Macao'
}

df_sales['region'] = df_sales['region'].replace(country_mapping)

# 연도 선택
min_year = int(df_sales["year"].min())
max_year = int(df_sales["year"].max())
year = st.slider("연도 선택", min_year, max_year, max_year)

# 선택된 연도 데이터
df_year = df_sales[df_sales["year"] == year]

# 1. 글로벌 판매량 연도별 그래프
st.subheader("📈 연도별 글로벌 전기차 판매량")
global_sales = df_sales.groupby("year")["value"].sum().reset_index()
fig_line = px.line(
    global_sales,
    x="year",
    y="value",
    markers=True,
    title="글로벌 전기차 판매량 추이",
    labels={"year": "연도", "value": "판매량 (대)"}
)
st.plotly_chart(fig_line, use_container_width=True)

# 2. 세계지도 (판매량에 따른 색상)
st.subheader(f"🌍 {year}년 국가별 전기차 판매량")

# 지도 생성
fig_map = px.choropleth(
    df_year,
    locations="region",
    color="value",
    locationmode="country names",
    color_continuous_scale="Blues",
    title=f"{year}년 국가별 전기차 판매량",
    labels={"value": "판매량 (대)", "region": "국가"},
    hover_name="region",
    hover_data={"value": ":,.0f"}
)

fig_map.update_geos(
    showframe=False,
    showcoastlines=True,
    projection_type='natural earth'
)

fig_map.update_layout(height=500)
st.plotly_chart(fig_map, use_container_width=True)

# 3. 상위 10개국 순위
st.subheader("🏆 상위 10개국 순위")

top_10 = df_year.nlargest(10, 'value').reset_index(drop=True)
if not top_10.empty:
    # 순위 표시
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🥇 1위 ~ 5위**")
        for idx, row in top_10.head(5).iterrows():
            st.write(f"{idx+1}. **{row['region']}**: {row['value']:,.0f}대")
    
    with col2:
        st.write("**🥈 6위 ~ 10위**")
        for idx, row in top_10.tail(5).iterrows():
            st.write(f"{idx+1}. **{row['region']}**: {row['value']:,.0f}대")
    
    # 막대 그래프로도 표시
    fig_bar = px.bar(
        top_10,
        x='value',
        y='region',
        orientation='h',
        title=f"{year}년 상위 10개국 판매량",
        labels={'value': '판매량 (대)', 'region': '국가'},
        color='value',
        color_continuous_scale='Blues'
    )
    fig_bar.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=400
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.write("해당 연도에 판매 데이터가 없습니다.")

# 요약 정보
col1, col2, col3 = st.columns(3)
with col1:
    total_sales = df_year['value'].sum()
    st.metric("🚗 총 판매량", f"{total_sales:,.0f}대")
with col2:
    countries_with_sales = len(df_year[df_year['value'] > 0])
    st.metric("🌍 판매 국가 수", f"{countries_with_sales}개국")
with col3:
    if not df_year.empty and len(df_year[df_year['value'] > 0]) > 0:
        max_sales = df_year['value'].max()
        max_country = df_year[df_year['value'] == max_sales]['region'].iloc[0]
        st.metric("🏆 최고 판매국", f"{max_country}")
    else:
        st.metric("🏆 최고 판매국", "없음")
