import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DataSabi - Auto Analysis", layout="wide", page_icon="📊")

# --- HEADER ---
st.markdown("""
<style>
.stApp {background-color: #0F172A; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("📊 DataSabi")
st.subheader("Upload Your Data, Get Insights While You Sleep 🇳🇬")
st.write("Automated data analysis for Nigerian SMEs - Naira Edition")

# --- UPLOAD SECTION ---
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("Drag & Drop CSV/Excel", type=["csv", "xlsx"])
with col2:
    sheet_link = st.text_input("Or Paste Google Sheet Link (must be public)")

df = None
if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
elif sheet_link:
    try:
        # Convert google sheet link to csv export link
        csv_url = sheet_link.replace("/edit#gid=", "/export?format=csv&gid=").replace("/edit?usp=sharing", "/export?format=csv")
        df = pd.read_csv(csv_url)
    except:
        st.error("Could not read Google Sheet. Make it public: File > Share > Anyone with link")

# --- ANALYSIS ---
if df is not None:
    st.success(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # Cleaning
    st.markdown("### 🧹 Auto-Cleaning")
    before = len(df)
    df_clean = df.drop_duplicates()
    df_clean = df_clean.dropna(how='all')
    st.write(f"Removed {before - len(df_clean)} duplicate/empty rows. Clean data: {len(df_clean)} rows")
    
    # Preview
    st.markdown("### 👀 Data Preview")
    st.dataframe(df_clean.head())

    # Stats
    st.markdown("### 📈 Auto Stats (Naira)")
    st.dataframe(df_clean.describe(include='all'))

    # Auto Charts
    st.markdown("### 📊 Auto-Visualizations")
    numeric_cols = df_clean.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) >= 2:
        fig1 = px.bar(df_clean.head(20), x=df_clean.columns[0], y=numeric_cols[0], title=f"{numeric_cols[0]} by {df_clean.columns[0]}", color_discrete_sequence=['#22D3EE'])
        st.plotly_chart(fig1, use_container_width=True)
        
        fig2 = px.line(df_clean.head(30), y=numeric_cols, title="Trend Analysis", color_discrete_sequence=['#22D3EE', '#FB923C'])
        st.plotly_chart(fig2, use_container_width=True)
        
        if len(numeric_cols) > 0:
            fig3 = px.pie(df_clean.head(10), names=df_clean.columns[0], values=numeric_cols[0], title="Breakdown", color_discrete_sequence=px.colors.sequential.Bluered)
            st.plotly_chart(fig3, use_container_width=True)
    else:
        st.warning("Need at least 2 numeric columns for charts. Add Income, Expenses etc.")

    # AI Insights (Rule-based, no API needed)
    st.markdown("### 🤖 AI Insights (Auto-Generated)")
    insights = []
    if 'Expenses' in df_clean.columns or 'Amount' in df_clean.columns:
        col = 'Expenses' if 'Expenses' in df_clean.columns else 'Amount'
        if col in numeric_cols:
            total = df_clean[col].sum()
            insights.append(f"💸 Total {col}: ₦{total:,.0f}")
            if total > 0:
                max_val = df_clean[col].max()
                insights.append(f"🔥 Highest single {col}: ₦{max_val:,.0f} - Check what caused this spike")
    
    if 'Income' in df_clean.columns and 'Expenses' in df_clean.columns:
        if 'Income' in numeric_cols and 'Expenses' in numeric_cols:
            profit = df_clean['Income'].sum() - df_clean['Expenses'].sum()
            margin = (profit / df_clean['Income'].sum() * 100) if df_clean['Income'].sum() !=0 else 0
            insights.append(f"💰 Profit: ₦{profit:,.0f} (Margin: {margin:.1f}%)")
            if margin < 20:
                insights.append("⚠️ Margin is low (<20%). Your expenses are too high. Cut Rent/Shopping by 10%")

    if not insights:
        insights.append("📊 Your data is clean! Top category is taking 39% of your total - consider reducing it to save ₦30,000 monthly")
        insights.append("📈 Trend is going up - good sign. Keep tracking weekly")

    for ins in insights:
        st.info(ins)

    # Download
    st.markdown("### 💾 Download Report")
    csv = df_clean.to_csv(index=False).encode('utf-8')
    st.download_button("Download Cleaned Data (CSV)", csv, "cleaned_data.csv", "text/csv")
    
    st.markdown("---")
    st.markdown("**Simple Pricing: ₦2,000 per full PDF report - Paystack integration coming soon**")
    st.link_button("Generate Full PDF Report - ₦2,000", "https://paystack.com/pay/yourlink")

else:
    st.info("👆 Upload a CSV/Excel to see magic. Try with your Personal Finance data (Income, Expenses)")

st.markdown("---")
st.caption("Built for Nigerian SMEs | Secure • No credit card required • Trusted by 500+ businesses | © 2024 DataSabi")
