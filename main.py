import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 앱 제목
st.title("🔋 전기차 판매량 대시보드")

# 데이터 로드
df = pd.read_csv("IEA-EV-dataEV salesHistoricalCars - IEA-EV-dataEV salesHistoricalCars.csv")

# EV sales 데이터만 필터
df_sales = df[(df["parameter"] == "EV sales") & (df["unit"] == "Vehicles")]

# 국가 이름 표준화
country_mapping = {
    'USA': 'United States',
    'US': 'United States',
    'Korea': 'South Korea',
    'Republic of Korea': 'South Korea',
    'Russian Federation': 'Russia',
    'Czech Republic': 'Czechia',
    'Slovak Republic': 'Slovakia',
    'Türkiye': 'Turkey',
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

# 연돌 선택
min_year = int(df_sales["year"].min())
max_year = int(df_sales["year"].max())
year = st.slider("연돌 선택", min_year, max_year, max_year)

df_year = df_sales[df_sales["year"] == year]

# 개수로만 보여주는 각역방의 컬렉션
all_countries_df = pd.DataFrame({
    'region': df_sales['region'].unique()
})
all_countries_df['value'] = 0

# 보여주기위한 모든 국가 + 현재연돌 데이터 메지
df_year_complete = all_countries_df.merge(df_year[['region', 'value']], on='region', how='left', suffixes=('_default', '_actual'))
df_year_complete['value'] = df_year_complete['value_actual'].fillna(0)
df_year_complete = df_year_complete[['region', 'value']]
df_year_complete['log_value'] = df_year_complete['value'].apply(lambda x: np.log10(x + 1))

# 1. 그린: 그리조가로 기준
st.subheader("📈 전세계 EV 판매 수준")
global_sales = df_sales.groupby("year")["value"].sum().reset_index()
fig_line = px.line(global_sales, x="year", y="value", markers=True, title="기간\uubcc4 그린 전세계 EV 판매가")
st.plotly_chart(fig_line, use_container_width=True)

# 2. 바람과 컬렉션
st.subheader(f"🌍 {year}년 국가별 EV 판매")
fig_map = px.choropleth(
    df_year_complete,
    locations="region",
    locationmode="country names",
    color="log_value",
    color_continuous_scale=["#e0f3ff", "#86c5f7", "#1c64f2"],
    title=f"{year}년 EV 판매 (로그 스케일)",
    labels={"log_value": "판매량 (로그)"},
    hover_name="region",
    hover_data={"value": ":,.0f", "log_value": False}
)
fig_map.update_geos(showframe=False, showcoastlines=True)
st.plotly_chart(fig_map, use_container_width=True)

# 3. 개발율
st.subheader("📊 EV 업적 개발 율")
global_sales["growth_rate"] = global_sales["value"].pct_change() * 100
fig_growth = px.bar(
    global_sales[1:],
    x="year",
    y="growth_rate",
    color="growth_rate",
    color_continuous_scale=["#fef9e7", "#ffe08a", "#f7b731"],
    title="EV 업적 개발율 (YoY)"
)
st.plotly_chart(fig_growth, use_container_width=True)

# 4. 중요국가 5가면 동행형
st.subheader("📈 중요 국가 세대 EV 수준")
top_5 = df_sales.groupby("region")["value"].sum().nlargest(5).index
df_top = df_sales[df_sales["region"].isin(top_5)]
fig_top = px.line(df_top, x="year", y="value", color="region", markers=True, title="중요 5가국 EV 판매가")
st.plotly_chart(fig_top, use_container_width=True)

# 5. 연돌 기준 정보
st.subheader("🌐 요약 정보")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🚗 전체 판매", f"{int(df_year['value'].sum()):,} 대")
with col2:
    st.metric("🌍 개별 국가", f"{df_year[df_year['value'] > 0]['region'].nunique()} 공공")
with col3:
    top = df_year.sort_values("value", ascending=False).iloc[0]
    st.metric("🏆 보고 국가", top['region'])
with col4:
    growth = global_sales[global_sales['year'] == year]['growth_rate'].values
    if len(growth) > 0:
        st.metric("📊 업적율", f"{growth[0]:.1f}%")
    else:
        st.metric("📊 업적율", "N/A")
