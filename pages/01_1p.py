import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="EV Future Outlook Dashboard", layout="centered")

st.title("🔮 Future Outlook: Global EV Market")
st.write("💡 실제 판매량 + 미래 전망 시나리오 비교")

# 실제 데이터
actual_df = pd.read_csv("ev_sales.csv")
actual_sales = actual_df[
    (actual_df["parameter"] == "EV sales") & (actual_df["unit"] == "Vehicles")
]
actual_by_year = actual_sales.groupby("year")["value"].sum().reset_index()
actual_by_year["scenario"] = "Actual"

# 미래 시나리오 데이터
future_df = pd.read_csv("future_projection.csv")

# 하나로 합치기
combined_df = pd.concat([
    actual_by_year.rename(columns={"value": "Sales"}),
    future_df.rename(columns={"value": "Sales"})
])

# Plotly 그래프
fig = px.line(
    combined_df,
    x="year",
    y="Sales",
    color="scenario",
    markers=True,
    title="📈 Actual vs Future Projections",
    labels={"year": "Year", "Sales": "EV Sales (Vehicles)", "scenario": "Scenario"}
)

fig.update_traces(mode="lines+markers")

st.plotly_chart(fig, use_container_width=True)

with st.expander("🔍 원본 데이터 보기"):
    st.write(combined_df)
