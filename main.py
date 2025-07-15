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

# 더 포괄적인 국가 이름 표준화 (데이터의 국가명을 Plotly가 인식할 수 있도록 매핑)
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
    'Great Britain': 'United Kingdom',
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

# 국가명 표준화 적용
df_sales['region'] = df_sales['region'].replace(country_mapping)

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

# 더 간단한 방법으로 지도 생성 - 세분화된 색상 농도
# 최대값을 기준으로 더 명확한 색상 구분
max_value = df_year_complete['value'].max()
if max_value > 0:
    # 로그 스케일을 고려한 색상 단계 설정
    fig_map = px.choropleth(
        df_year_complete,
        locations="region",
        color="value",
        locationmode="country names",
        color_continuous_scale=[
            [0.0, '#ffffff'],      # 판매량 0 (순백색)
            [0.01, '#f8f9ff'],     # 극소량 (거의 흰색)
            [0.05, '#e6f2ff'],     # 매우 적음 (매우 연한 파란색)
            [0.1, '#ccddff'],      # 적음 (연한 파란색)
            [0.2, '#99bbff'],      # 보통 하위 (연한 하늘색)
            [0.3, '#6699ff'],      # 보통 (하늘색)
            [0.4, '#3377ff'],      # 보통 상위 (밝은 파란색)
            [0.5, '#0055ff'],      # 많음 하위 (파란색)
            [0.6, '#0044dd'],      # 많음 (진한 파란색)
            [0.7, '#0033bb'],      # 많음 상위 (더 진한 파란색)
            [0.8, '#002299'],      # 매우 많음 (진한 남색)
            [0.9, '#001177'],      # 최상위 (매우 진한 남색)
            [1.0, '#000055']       # 최대 (가장 진한 남색)
        ],
        title=f"🌍 {year} 전 세계 전기차 판매량 (판매량에 따른 색상 농도)",
        labels={"value": "전기차 판매량 (대)", "region": "국가"},
        hover_name="region",
        hover_data={"value": ":,.0f"},
        range_color=[0, max_value]
    )
else:
    fig_map = px.choropleth(
        df_year_complete,
        locations="region",
        color="value",
        locationmode="country names",
        color_continuous_scale="Blues",
        title=f"🌍 {year} 전 세계 전기차 판매량",
        labels={"value": "전기차 판매량 (대)", "region": "국가"},
        hover_name="region",
        hover_data={"value": ":,.0f"}
    )

# 지도 스타일 업데이트
fig_map.update_geos(
    showframe=False,
    showcoastlines=True,
    projection_type='natural earth'
)

# 색상 바 설정 - 더 명확한 구분
fig_map.update_coloraxes(
    colorbar_title="전기차 판매량 (대)",
    colorbar_title_side="right",
    colorbar_thickness=20,
    colorbar_len=0.7
)

fig_map.update_layout(
    height=600
)

st.plotly_chart(fig_map, use_container_width=True)

# ---------------------------
# 3) 전체 판매량 순위 테이블 (모든 국가)
# ---------------------------
st.subheader("🏆 전체 국가 전기차 판매량 순위")

# 판매량이 있는 모든 국가 정렬
all_countries_ranked = df_year[df_year['value'] > 0].sort_values('value', ascending=False).reset_index(drop=True)
all_countries_ranked.index = all_countries_ranked.index + 1  # 순위는 1부터 시작

if not all_countries_ranked.empty:
    # 3개 컬럼으로 나누어 표시
    col1, col2, col3 = st.columns(3)
    
    total_countries = len(all_countries_ranked)
    countries_per_col = (total_countries + 2) // 3  # 올림 나눗셈
    
    with col1:
        st.write("**🥇 1위 ~ {}위**".format(min(countries_per_col, total_countries)))
        top_1 = all_countries_ranked.iloc[:countries_per_col]
        for idx, row in top_1.iterrows():
            st.write(f"{idx}. **{row['region']}**: {row['value']:,.0f}대")
    
    with col2:
        if countries_per_col < total_countries:
            st.write("**🥈 {}위 ~ {}위**".format(countries_per_col + 1, min(countries_per_col * 2, total_countries)))
            top_2 = all_countries_ranked.iloc[countries_per_col:countries_per_col * 2]
            for idx, row in top_2.iterrows():
                st.write(f"{idx}. **{row['region']}**: {row['value']:,.0f}대")
    
    with col3:
        if countries_per_col * 2 < total_countries:
            st.write("**🥉 {}위 ~ {}위**".format(countries_per_col * 2 + 1, total_countries))
            top_3 = all_countries_ranked.iloc[countries_per_col * 2:]
            for idx, row in top_3.iterrows():
                st.write(f"{idx}. **{row['region']}**: {row['value']:,.0f}대")

# ---------------------------
# 4) 상위 20개국 막대 그래프
# ---------------------------
st.subheader("📊 상위 20개국 전기차 판매량")
top_20_countries = df_year[df_year['value'] > 0].nlargest(20, 'value')
if not top_20_countries.empty:
    fig_bar = px.bar(
        top_20_countries,
        x='value',
        y='region',
        orientation='h',
        title=f"🏆 상위 20개국 - {year}년 전기차 판매량",
        labels={'value': '전기차 판매량 (대)', 'region': '국가'},
        color='value',
        color_continuous_scale='Blues'
    )
    fig_bar.update_layout(
        yaxis={'categoryorder': 'total ascending'},
        height=600
    )
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.write("해당 연도에 판매 데이터가 없습니다.")

# 디버깅을 위한 정보 표시
st.sidebar.title("📊 데이터 정보")
st.sidebar.write(f"**선택된 연도**: {year}")
st.sidebar.write(f"**데이터가 있는 국가 수**: {len(df_year[df_year['value'] > 0])}")

# 실제 데이터에 있는 국가들 표시
if not df_year.empty:
    st.sidebar.write("**데이터가 있는 주요 국가:**")
    top_5_countries = df_year.nlargest(5, 'value')[['region', 'value']]
    for _, row in top_5_countries.iterrows():
        st.sidebar.write(f"- {row['region']}: {row['value']:,.0f}")

# 원본 데이터에서 미국 관련 데이터 확인
us_data = df_sales[df_sales['region'].str.contains('United States|USA|US', case=False, na=False)]
if not us_data.empty:
    st.sidebar.write("**미국 데이터 확인:**")
    st.sidebar.write(us_data[['region', 'year', 'value']].tail())
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_sales = df_year['value'].sum()
    st.metric("🚗 총 판매량", f"{total_sales:,.0f}대")
with col2:
    countries_with_sales = len(df_year[df_year['value'] > 0])
    st.metric("🌍 판매 국가 수", f"{countries_with_sales}개국")
with col3:
    if not df_year.empty and len(df_year[df_year['value'] > 0]) > 0:
        avg_sales = df_year[df_year['value'] > 0]['value'].mean()
        st.metric("📊 평균 판매량", f"{avg_sales:,.0f}대")
    else:
        st.metric("📊 평균 판매량", "0대")
with col4:
    if not df_year.empty and len(df_year[df_year['value'] > 0]) > 0:
        max_sales = df_year['value'].max()
        max_country = df_year[df_year['value'] == max_sales]['region'].iloc[0]
        st.metric("🏆 최고 판매국", f"{max_country}")
    else:
        st.metric("🏆 최고 판매국", "없음")

# ---------------------------
# 원본 데이터 (옵션)
# ---------------------------
with st.expander("🔍 원본 데이터 보기"):
    st.write("**전체 데이터 샘플:**")
    st.write(df.head())
    st.write("**EV Sales 데이터 샘플:**")
    st.write(df_sales.head())
    st.write("**선택된 연도 데이터:**")
    st.write(df_year.head())

# 디버깅을 위한 정보 표시
st.sidebar.title("📊 데이터 분석")
st.sidebar.write(f"**선택된 연도**: {year}")
st.sidebar.write(f"**전체 국가 수**: {len(df_year_complete)}")
st.sidebar.write(f"**판매 데이터가 있는 국가**: {len(df_year[df_year['value'] > 0])}")

# 실제 데이터에 있는 상위 국가들 표시
if not df_year.empty and len(df_year[df_year['value'] > 0]) > 0:
    st.sidebar.write("**상위 10개국:**")
    top_10_countries = df_year.nlargest(10, 'value')[['region', 'value']]
    for idx, (_, row) in enumerate(top_10_countries.iterrows(), 1):
        st.sidebar.write(f"{idx}. {row['region']}: {row['value']:,.0f}대")

# 색상 구분 범례
st.sidebar.write("**색상 구분 기준:**")
st.sidebar.write("- 🤍 흰색: 판매량 0")
st.sidebar.write("- 🔵 연한 파란색: 소량 판매")
st.sidebar.write("- 🔷 파란색: 보통 판매")
st.sidebar.write("- 🔹 진한 파란색: 많은 판매")
st.sidebar.write("- 🟦 가장 진한 파란색: 최대 판매")
