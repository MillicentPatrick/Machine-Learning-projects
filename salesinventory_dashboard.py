import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.plot import plot_plotly
import plotly.express as px
from scipy.stats import zscore

# Page Configuration
st.set_page_config(page_title="KHEN SALES & INVENTORY DASHBOARD", layout="wide")
st.title(" Khen Enterprises Sales & Inventory Dashboard")

# Load data
@st.cache_data

def load_data(uploaded_file):
    df = pd.read_excel(uploaded_file)
    df['ORDERDATE'] = pd.to_datetime(df['ORDERDATE'])
    df['YearMonth'] = df['ORDERDATE'].dt.to_period('M')
    df['Day'] = df['ORDERDATE'].dt.date
    return df

uploaded_file = st.file_uploader("Upload your merged Excel file", type=["xlsx"])
if uploaded_file:
    merged_data = load_data(uploaded_file)

    # Filters
    st.subheader("🎛 Filtered Sales Explorer")
    with st.expander("Apply Filters"):
        col1, col2, col3 = st.columns(3)
        date_range = col1.date_input("Select Date Range", [merged_data['ORDERDATE'].min(), merged_data['ORDERDATE'].max()])
        product_line = col2.multiselect("Select Product Line", merged_data['PRODUCTLINE'].unique())
        country = col3.multiselect("Select Country", merged_data['COUNTRY'].unique())

    filtered_data = merged_data.copy()
    if date_range:
        filtered_data = filtered_data[(filtered_data['ORDERDATE'] >= pd.to_datetime(date_range[0])) & (filtered_data['ORDERDATE'] <= pd.to_datetime(date_range[1]))]
    if product_line:
        filtered_data = filtered_data[filtered_data['PRODUCTLINE'].isin(product_line)]
    if country:
        filtered_data = filtered_data[filtered_data['COUNTRY'].isin(country)]

    st.write(f"Filtered Rows: {filtered_data.shape[0]}")
    st.dataframe(filtered_data.head(50))

    # Key Metrics
    st.subheader(" Key Metrics")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Sales", f"${filtered_data['SALES'].sum():,.0f}")
    kpi2.metric("Total Orders", filtered_data['ORDERNUMBER'].nunique())
    kpi3.metric("Unique Products", filtered_data['PRODUCTCODE'].nunique())

    # Top 5 Products by Sales
    st.subheader(" Top 5 Products by Sales")
    top5 = filtered_data.groupby('PRODUCTLINE')['SALES'].sum().sort_values(ascending=False).head(5)
    fig1, ax1 = plt.subplots()
    top5.plot(kind='bar', color='skyblue', ax=ax1)
    ax1.set_ylabel('Total Sales')
    st.pyplot(fig1)

    # Sales Trends
    st.subheader(" Sales Trends by Day, Month, and Year")
    trend_option = st.selectbox("View sales trend by:", ["Daily", "Monthly", "Yearly"])

    if trend_option == "Daily":
        trend_data = filtered_data.groupby('Day')['SALES'].sum().reset_index()
    elif trend_option == "Monthly":
        trend_data = filtered_data.groupby('YearMonth')['SALES'].sum().reset_index()
        trend_data['YearMonth'] = trend_data['YearMonth'].astype(str)
    else:
        trend_data = filtered_data.groupby(filtered_data['ORDERDATE'].dt.year)['SALES'].sum().reset_index()
        trend_data.columns = ['Year', 'SALES']

    fig2 = px.line(trend_data, x=trend_data.columns[0], y='SALES', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

    # Revenue Trends
    st.subheader(" Revenue Trends by Product Line")
    rev_trend = filtered_data.groupby(['YearMonth', 'PRODUCTLINE'])['SALES'].sum().reset_index()
    rev_trend['YearMonth'] = rev_trend['YearMonth'].astype(str)
    figrev = px.line(rev_trend, x='YearMonth', y='SALES', color='PRODUCTLINE', markers=True)
    st.plotly_chart(figrev, use_container_width=True)

    # Anomaly Detection
    st.subheader(" Anomaly Detection (Monthly Sales)")
    monthly_sales = filtered_data.groupby('YearMonth')['SALES'].sum().reset_index()
    monthly_sales['YearMonth'] = monthly_sales['YearMonth'].astype(str)  # Convert Period to string
    monthly_sales['zscore'] = zscore(monthly_sales['SALES'])
    monthly_sales['Anomaly'] = monthly_sales['zscore'].apply(lambda x: 'High' if x > 2 else ('Low' if x < -2 else 'Normal'))
    fig3 = px.bar(monthly_sales, x='YearMonth', y='SALES', color='Anomaly', color_discrete_map={"High": "red", "Low": "blue", "Normal": "green"})
    st.plotly_chart(fig3, use_container_width=True)

    # Forecasting with Prophet
    st.subheader(" Sales Forecast (6 Months)")
    forecast_data = filtered_data.groupby('ORDERDATE')['SALES'].sum().reset_index()
    forecast_data = forecast_data.rename(columns={'ORDERDATE': 'ds', 'SALES': 'y'})
    model = Prophet()
    model.fit(forecast_data)
    future = model.make_future_dataframe(periods=180)
    forecast = model.predict(future)
    st.plotly_chart(plot_plotly(model, forecast), use_container_width=True)

    # Inventory vs. Sales Comparison
    st.subheader(" Inventory vs Sales by Product Line")
    if 'QUANTITYORDERED' in filtered_data.columns:
        inv_sales = filtered_data.groupby('PRODUCTLINE').agg({
            'QUANTITYORDERED': 'sum',
            'SALES': 'sum'
        }).reset_index()
        fig4 = px.bar(inv_sales, x='PRODUCTLINE', y=['QUANTITYORDERED', 'SALES'], barmode='group')
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.warning("QUANTITYORDERED column not available in dataset.")

    #  Summary Section
    st.markdown("---")
    st.subheader(" Automated Business Summary")
    total_sales = filtered_data['SALES'].sum()
    total_orders = filtered_data['ORDERNUMBER'].nunique()
    top_month = filtered_data.groupby(filtered_data['ORDERDATE'].dt.strftime('%B'))['SALES'].sum().idxmax()
    top_product = filtered_data.groupby('PRODUCTLINE')['SALES'].sum().idxmax()

    st.markdown(f" **Total Sales:** ${total_sales:,.0f}<br>"
                f" **Total Orders:** {total_orders}<br>"
                f" **Best Sales Month:** {top_month}<br>"
                f" **Top Product Line:** {top_product}", unsafe_allow_html=True)
else:
    st.warning("Please upload a merged Excel file to get started.")
