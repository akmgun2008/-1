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

# 모든 국가를 포함하는 완전한 데이터셋 생성
all_countries = [
    'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Argentina', 'Armenia', 'Australia', 
    'Austria', 'Azerbaijan', 'Bahrain', 'Bangladesh', 'Belarus', 'Belgium', 'Bolivia', 'Bosnia and Herzegovina', 
    'Botswana', 'Brazil', 'Bulgaria', 'Cambodia', 'Cameroon', 'Canada', 'Chile', 'China', 'Colombia', 
    'Costa Rica', 'Croatia', 'Cyprus', 'Czechia', 'Denmark', 'Ecuador', 'Egypt', 'Estonia', 'Ethiopia', 
    'Finland', 'France', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Hungary', 'Iceland', 'India', 
    'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 
    'Kazakhstan', 'Kenya', 'Kuwait', 'Latvia', 'Lebanon', 'Lithuania', 'Luxembourg', 'Malaysia', 
    'Malta', 'Mexico', 'Moldova', 'Morocco', 'Netherlands', 'New Zealand', 'Nigeria', 'North Macedonia', 
    'Norway', 'Pakistan', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 
    'Romania', 'Russia', 'Saudi Arabia', 'Serbia', 'Singapore', 'Slovakia', 'Slovenia', 'South Africa', 
    'South Korea', 'Spain', 'Sri Lanka', 'Sweden', 'Switzerland', 'Thailand', 'Tunisia', 'Turkey', 
    'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'Uruguay', 'Venezuela', 
    'Vietnam', 'Yemen', 'Zimbabwe'
]

# 모든 국가에 기본값 0 설정
all_countries_df = pd.DataFrame({'region': all_countries, 'value': 0})

# 실제 데이터와 병합
df_year_complete = all_countries_df.merge(df_year[['region', 'value']], on='region', how='left', suffixes=('_default', '_actual'))
df_year_complete['value'] = df_year_complete['value_actual'].fillna(0)
df_year_complete = df_year_complete[['region', 'value']]

# 로그 스케일 적용으로 색상 차이 강화
df_year_complete['log_value'] = df_year_complete['value'].apply(lambda x: np.log10(x + 1))

# 세분화된 색상 스케일 적용
fig_map = px.choropleth(
    df_year_complete,
    locations="region",
    color="log_value",
    locationmode="country names",
    color_continuous_scale=[
        [0.0, '#ffffff'],    # 0 (흰색)
        [0.1, '#f0f8ff'],    # 극소량 (거의 흰색)
        [0.2, '#e0f0ff'],    # 매우 적음 (매우 연한 파란색)
        [0.3, '#c0e0ff'],    # 적음 (연한 파란색)
        [0.4, '#90c0ff'],    # 보통 하위 (연한 하늘색)
        [0.5, '#6090ff'],    # 보통 (하늘색)
        [0.6, '#3060ff'],    # 보통 상위 (밝은 파란색)
        [0.7, '#0040ff'],    # 많음 하위 (파란색)
        [0.8, '#0030cc'],    # 많음 (진한 파란색)
        [0.9, '#002099'],    # 매우 많음 (진한 남색)
        [1.0, '#001066']     # 최대 (가장 진한 남색)
    ],
    title=f"{year}년 국가별 전기차 판매량 (로그 스케일)",
    labels={"log_value": "판매량 (로그 스케일)", "region": "국가"},
    hover_name="region",
    hover_data={"value": ":,.0f", "log_value": False}
)

fig_map.update_geos(
    showframe=False,
    showcoastlines=True,
    projection_type='natural earth'
)

# 색상 바 설정
fig_map.update_coloraxes(
    colorbar_title="판매량<br>(로그 스케일)",
    colorbar_title_side="right",
    colorbar_thickness=20,
    colorbar_len=0.8,
    colorbar_tickmode='linear',
    colorbar_tick0=0,
    colorbar_dtick=1
)

fig_map.update_layout(height=500)
st.plotly_chart(fig_map, use_container_width=True)

# 색상 구분 설명
st.info("💡 **색상 구분**: 판매량의 차이를 더 명확하게 보기 위해 로그 스케일을 적용했습니다. 흰색(판매량 0) → 연한 파란색(소량) → 진한 파란색(대량)")

# 4. EV 성장률 분석
st.subheader("📊 EV 성장률 분석")

# 연도별 성장률 계산 (글로벌)
global_sales_growth = global_sales.copy()
global_sales_growth['growth_rate'] = global_sales_growth['value'].pct_change() * 100

# 글로벌 성장률 그래프
fig_growth = px.bar(
    global_sales_growth[1:],  # 첫 번째 연도는 성장률 계산 불가
    x='year',
    y='growth_rate',
    title='글로벌 EV 판매량 연도별 성장률',
    labels={'year': '연도', 'growth_rate': '성장률 (%)'},
    color='growth_rate',
    color_continuous_scale='RdYlGn'
)
fig_growth.update_layout(height=400)
st.plotly_chart(fig_growth, use_container_width=True)

# 국가별 성장률 계산 (전년 대비)
if year > min_year:
    prev_year = year - 1
    df_prev_year = df_sales[df_sales["year"] == prev_year]
    
    # 현재 연도와 전년도 데이터 병합
    growth_data = df_year.merge(df_prev_year, on='region', how='outer', suffixes=('_current', '_prev'))
    growth_data['value_current'] = growth_data['value_current'].fillna(0)
    growth_data['value_prev'] = growth_data['value_prev'].fillna(0)
    
    # 성장률 계산 (전년도 판매량이 0이 아닌 경우만)
    growth_data['growth_rate'] = growth_data.apply(
        lambda row: ((row['value_current'] - row['value_prev']) / row['value_prev'] * 100) 
        if row['value_prev'] > 0 else (100 if row['value_current'] > 0 else 0), axis=1
    )
    
    # 무한대 값 처리
    growth_data = growth_data[growth_data['growth_rate'] != float('inf')]
    
    # 성장률 상위 10개국
    st.subheader(f"🚀 {prev_year}년 대비 {year}년 성장률 상위 10개국")
    
    # 의미있는 성장률만 표시 (전년도 판매량이 있거나 신규 진입)
    meaningful_growth = growth_data[
        (growth_data['value_current'] > 0) & 
        (growth_data['growth_rate'] > 0)
    ].nlargest(10, 'growth_rate')
    
    if not meaningful_growth.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**🔥 1위 ~ 5위**")
            for idx, row in meaningful_growth.head(5).iterrows():
                growth_rate = row['growth_rate']
                current_sales = row['value_current']
                prev_sales = row['value_prev']
                
                if prev_sales == 0:
                    st.write(f"{len(meaningful_growth[meaningful_growth['growth_rate'] >= growth_rate])}. **{row['region']}**: 신규 진입 ({current_sales:,.0f}대)")
                else:
                    st.write(f"{len(meaningful_growth[meaningful_growth['growth_rate'] >= growth_rate])}. **{row['region']}**: +{growth_rate:.1f}% ({current_sales:,.0f}대)")
        
        with col2:
            st.write("**📈 6위 ~ 10위**")
            for idx, row in meaningful_growth.tail(5).iterrows():
                growth_rate = row['growth_rate']
                current_sales = row['value_current']
                prev_sales = row['value_prev']
                
                if prev_sales == 0:
                    st.write(f"{len(meaningful_growth[meaningful_growth['growth_rate'] >= growth_rate])}. **{row['region']}**: 신규 진입 ({current_sales:,.0f}대)")
                else:
                    st.write(f"{len(meaningful_growth[meaningful_growth['growth_rate'] >= growth_rate])}. **{row['region']}**: +{growth_rate:.1f}% ({current_sales:,.0f}대)")
        
        # 성장률 막대 그래프
        fig_growth_countries = px.bar(
            meaningful_growth,
            x='growth_rate',
            y='region',
            orientation='h',
            title=f"{prev_year}년 대비 {year}년 성장률 상위 10개국",
            labels={'growth_rate': '성장률 (%)', 'region': '국가'},
            color='growth_rate',
            color_continuous_scale='Viridis'
        )
        fig_growth_countries.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=400
        )
        st.plotly_chart(fig_growth_countries, use_container_width=True)
    else:
        st.write("성장률 데이터가 없습니다.")

# 5. 주요 국가 성장 추이
st.subheader("📈 주요 국가별 EV 판매량 추이")

# 상위 5개국 선택
top_5_overall = df_sales.groupby('region')['value'].sum().nlargest(5).index.tolist()

# 주요 국가들의 연도별 데이터
major_countries_data = df_sales[df_sales['region'].isin(top_5_overall)]

fig_trends = px.line(
    major_countries_data,
    x='year',
    y='value',
    color='region',
    markers=True,
    title='주요 5개국 EV 판매량 추이',
    labels={'year': '연도', 'value': '판매량 (대)', 'region': '국가'}
)
fig_trends.update_layout(height=400)
st.plotly_chart(fig_trends, use_container_width=True)

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
col1, col2, col3, col4 = st.columns(4)
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
with col4:
    # 글로벌 성장률 표시
    if year > min_year and len(global_sales_growth) > 1:
        current_growth = global_sales_growth[global_sales_growth['year'] == year]['growth_rate'].iloc[0]
        st.metric("📊 글로벌 성장률", f"{current_growth:.1f}%")
    else:
        st.metric("📊 글로벌 성장률", "N/A")
import streamlit as st

st.set_page_config(page_title="EV Opinion", layout="centered")

# 제목 - 글씨 3배, 단일 폰트, 굵기 없음
st.markdown(
    "<h1 style='font-size: 3em; font-weight: normal;'>내가 생각하는 전기차 전망</h1>",
    unsafe_allow_html=True
)

# 본문 - 사용자 의견 그대로
st.write("""
전기차에 대한 전망은 앞으로도 우상향을 그릴것을 예상한다. 왜냐하면 전기차에대한 고질적인 문제들이 점점 해결되고 있기때문이다. 너무 조용하다던가 연료효율이 안 좋다던가 혹은 주유소가 적다던가 이러한 문제들이 기술발전과 함께 개선 되었고 정부도 전기차에대한 보조금도 주고 있어 기업들도 투자를 할 경향이 높다
""")
