import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.colors import sequential
import numpy as np

# 앱 제목
st.title("🔋 Global EV Sales Dashboard")
st.write("데이터 출처: IEA EV Sales Historical Cars")

# 데이터 로드 (파일명을 꼭 확인!)
df = pd.read_csv("IEA-EV-dataEV salesHistoricalCars - IEA-EV-dataEV salesHistoricalCars.csv")

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
# 2) 개선된 세계지도 (모든 국가 표시)
# ---------------------------
# 모든 국가 리스트 (ISO 3166-1 alpha-3 코드 기준)
all_countries = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda',
    'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
    'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bhutan',
    'Bolivia', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'Brunei', 'Bulgaria',
    'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde',
    'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Comoros',
    'Congo', 'Costa Rica', 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark',
    'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Fiji', 'Finland',
    'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Grenada',
    'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Honduras', 'Hungary',
    'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy',
    'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait',
    'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya',
    'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia',
    'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius',
    'Mexico', 'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco',
    'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Zealand',
    'Nicaragua', 'Niger', 'Nigeria', 'North Korea', 'North Macedonia', 'Norway',
    'Oman', 'Pakistan', 'Palau', 'Palestine', 'Panama', 'Papua New Guinea', 'Paraguay',
    'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia',
    'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines',
    'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal',
    'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 'Slovenia',
    'Solomon Islands', 'Somalia', 'South Africa', 'South Korea', 'South Sudan',
    'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria',
    'Taiwan', 'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga',
    'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda',
    'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay',
    'Uzbekistan', 'Vanuatu', 'Vatican City', 'Venezuela', 'Vietnam', 'Yemen',
    'Zambia', 'Zimbabwe'
]

# 모든 국가를 포함하는 기본 데이터프레임 생성
all_countries_df = pd.DataFrame({
    'region': all_countries,
    'value': 0  # 기본값은 0
})

# 실제 데이터와 병합
df_year_complete = all_countries_df.merge(
    df_year[['region', 'value']], 
    on='region', 
    how='left', 
    suffixes=('_default', '_actual')
)

# 실제 값이 있으면 사용하고, 없으면 0 사용
df_year_complete['value'] = df_year_complete['value_actual'].fillna(0)
df_year_complete = df_year_complete[['region', 'value']]

# 더 간단한 방법으로 지도 생성
fig_map = px.choropleth(
    df_year_complete,
    locations="region",
    color="value",
    locationmode="country names",
    color_continuous_scale=[
        [0, 'white'],           # 판매량 0 (흰색)
        [0.001, '#f0f8ff'],     # 매우 적은 판매량 (매우 연한 파란색)
        [0.2, '#add8e6'],       # 적은 판매량 (연한 파란색)
        [0.4, '#87ceeb'],       # 보통 판매량 (하늘색)
        [0.6, '#4169e1'],       # 많은 판매량 (파란색)
        [0.8, '#0000cd'],       # 매우 많은 판매량 (진한 파란색)
        [1.0, '#000080']        # 최대 판매량 (가장 진한 파란색)
    ],
    title=f"🌍 {year} EV Sales by Country",
    labels={"value": "EV Sales (Vehicles)", "region": "Country"},
    hover_name="region",
    hover_data={"value": ":,.0f"},
    range_color=[0, None]  # 0부터 최대값까지 색상 범위 설정
)

# 지도 스타일 업데이트
fig_map.update_geos(
    showframe=False,
    showcoastlines=True,
    projection_type='natural earth'
)

# 색상 바 설정
fig_map.update_coloraxes(
    colorbar_title="EV Sales (Vehicles)",
    colorbar_title_side="right"
)

fig_map.update_layout(
    height=600
)

st.plotly_chart(fig_map, use_container_width=True)

# ---------------------------
# 3) 상위 국가 막대 그래프 추가
# ---------------------------
top_countries = df_year[df_year['value'] > 0].nlargest(10, 'value')
if not top_countries.empty:
    fig_bar = px.bar(
        top_countries,
        x='value',
        y='region',
        orientation='h',
        title=f"🏆 Top 10 Countries - {year} EV Sales",
        labels={'value': 'EV Sales (Vehicles)', 'region': 'Country'}
    )
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------------------------
# 통계 정보
# ---------------------------
col1, col2, col3 = st.columns(3)
with col1:
    total_sales = df_year['value'].sum()
    st.metric("총 판매량", f"{total_sales:,.0f}")
with col2:
    countries_with_sales = len(df_year[df_year['value'] > 0])
    st.metric("판매 국가 수", f"{countries_with_sales}")
with col3:
    if not df_year.empty:
        avg_sales = df_year[df_year['value'] > 0]['value'].mean()
        st.metric("평균 판매량", f"{avg_sales:,.0f}")

# ---------------------------
# 원본 데이터 (옵션)
# ---------------------------
with st.expander("🔍 원본 데이터 보기"):
    st.write(df.head())
