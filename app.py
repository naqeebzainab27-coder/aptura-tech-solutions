import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from modules.data_processor import load_data, clean_data, get_kpis, get_summary_stats
from modules.ml_models import forecast_sales, customer_segmentation, top_products, growth_rate
from modules.visualizations import (
    plot_sales_trend, plot_forecast, plot_category_pie, 
    plot_region_bar, plot_heatmap, plot_top_products, plot_monthly_sales
)
from modules.insights import generate_insights

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="Aptura Tech Solutions",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== LOAD CUSTOM CSS =====
try:
    with open('assets/style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("CSS file not found. Continuing with default style.")

# ===== HEADER =====
st.markdown('<h1 class="main-title"> APTURA TECH SOLUTIONS </h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle"> AI-Powered Business Intelligence & Sales Forecasting Platform </p>', unsafe_allow_html=True)
st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🎛️ CONTROL PANEL")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "📁 Upload Sales CSV", 
        type=['csv'],
        help="Upload your sales data file"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Forecast Settings")
    forecast_days = st.slider("🔮 Forecast Period (Days)", 7, 90, 30)
    
    st.markdown("---")
    st.markdown("### 📋 Required CSV Columns:")
    st.code("date, category, region,\nproduct, quantity, price, sales")
    
    st.markdown("---")
    st.markdown("### 🏢 About")
    st.info("**Aptura Tech Solutions** delivers enterprise-grade AI analytics for modern businesses.")

# ===== MAIN CONTENT =====
if uploaded_file:
    try:
        # Load & Clean
        with st.spinner("🔄 Processing data with AI engine..."):
            df = load_data(uploaded_file)
            df = clean_data(df)
        
        st.success(f"✅ Successfully loaded {len(df):,} records!")
        
        # ===== KPI SECTION =====
        st.markdown("## 📊 KEY PERFORMANCE INDICATORS")
        kpis = get_kpis(df)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(" Total Sales", f"${kpis['total_sales']:,.0f}")
        col2.metric(" Average Sales", f"${kpis['avg_sales']:,.2f}")
        col3.metric(" Max Sale", f"${kpis['max_sales']:,.0f}")
        col4.metric(" Total Orders", f"{kpis['total_orders']:,}")
        
        col5, col6, col7, col8 = st.columns(4)
        col5.metric(" Products", f"{kpis['unique_products']:,}")
        col6.metric(" Regions", f"{kpis['unique_regions']:,}")
        col7.metric(" Categories", f"{kpis['unique_categories']:,}")
        growth = growth_rate(df)
        col8.metric(" Growth Rate", f"{growth:+.1f}%")
        
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        
        # ===== FORECAST =====
        with st.spinner(" AI is generating forecast..."):
            forecast, daily = forecast_sales(df, periods=forecast_days)
        
        # ===== AI INSIGHTS =====
        st.markdown("## AI INSIGHT ENGINE")
        insights = generate_insights(df, forecast)
        
        cols = st.columns(min(len(insights), 3))
        for i, (title, msg, level) in enumerate(insights):
            with cols[i % 3]:
                if level == "success":
                    st.success(f"**{title}**\n\n{msg}")
                elif level == "warning":
                    st.warning(f"**{title}**\n\n{msg}")
                else:
                    st.info(f"**{title}**\n\n{msg}")
        
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        
        # ===== ANALYTICS DASHBOARD =====
        st.markdown("##  INTERACTIVE ANALYTICS DASHBOARD")
        
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
            " Trend", " Forecast", " Category", 
            " Region", " Heatmap", " Top Products", " Monthly"
        ])
        
        with tab1:
            st.plotly_chart(plot_sales_trend(daily), use_container_width=True)
        
        with tab2:
            st.plotly_chart(plot_forecast(daily, forecast), use_container_width=True)
        
        with tab3:
            if 'category' in df.columns:
                st.plotly_chart(plot_category_pie(df), use_container_width=True)
            else:
                st.info("No 'category' column found in your data.")
        
        with tab4:
            if 'region' in df.columns:
                st.plotly_chart(plot_region_bar(df), use_container_width=True)
            else:
                st.info("No 'region' column found in your data.")
        
        with tab5:
            st.plotly_chart(plot_heatmap(df), use_container_width=True)
        
        with tab6:
            if 'product' in df.columns:
                st.plotly_chart(plot_top_products(df, n=10), use_container_width=True)
            else:
                st.info("No 'product' column found in your data.")
        
        with tab7:
            st.plotly_chart(plot_monthly_sales(df), use_container_width=True)
        
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        
        # ===== DATA TABLES =====
        st.markdown("##  DETAILED REPORTS")
        
        rep1, rep2 = st.tabs([" Forecast Data", " Raw Data"])
        
        with rep1:
            st.dataframe(forecast, use_container_width=True, height=300)
            csv_forecast = forecast.to_csv(index=False)
            st.download_button(
                "📥 Download Forecast CSV",
                csv_forecast,
                f"aptura_forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
        
        with rep2:
            st.dataframe(df, use_container_width=True, height=300)
            csv_raw = df.to_csv(index=False)
            st.download_button(
                "📥 Download Cleaned Data",
                csv_raw,
                f"aptura_cleaned_data_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv"
            )
    
    except Exception as e:
        st.error(f"❌ Error processing file: {str(e)}")
        st.info("Make sure your CSV has the required columns: date, category, region, product, quantity, price, sales")

else:
    # ===== WELCOME SCREEN =====
    st.markdown("## 👋 WELCOME TO APTURA TECH SOLUTIONS")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ###  AI-Powered
        - Machine Learning forecasting
        - Smart insight generation
        - Automated trend detection
        """)
    
    with col2:
        st.markdown("""
        ###  Advanced Analytics
        - Interactive dashboards
        - Multi-dimensional analysis
        - Real-time visualizations
        """)
    
    with col3:
        st.markdown("""
        ###  Enterprise Ready
        - Scalable architecture
        - Export capabilities
        - Beautiful UI/UX
        """)
    
    st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
    
    st.info(" **Upload your sales CSV file from the sidebar to get started!**")
    
    st.markdown("### 📝 Sample CSV Format:")
    sample_data = pd.DataFrame({
        'date': ['2025-01-01', '2025-01-02', '2025-01-03'],
        'category': ['Electronics', 'Clothing', 'Beauty'],
        'region': ['Karachi', 'Lahore', 'Islamabad'],
        'product': ['Laptop', 'Shirt', 'Lipstick'],
        'quantity': [5, 10, 20],
        'price': [50000, 2000, 1500],
        'sales': [250000, 20000, 30000]
    })
    st.dataframe(sample_data, use_container_width=True)

# ===== FOOTER =====
st.markdown("""
<div class="custom-footer">
    Built by <span>APTURA TECH SOLUTIONS</span>
</div>
""", unsafe_allow_html=True)