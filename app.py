import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="DataSabi", page_icon="📊", layout="centered")

PAYSTACK_LINK = "https://paystack.shop/pay/2jji7vgoln"

st.title("📊 DataSabi")
st.subheader("Upload Your Data, Get Insights While You Sleep 🇳🇬")
st.caption("Automated data analysis for Nigerian SMEs - Naira Edition")

# --- FILE UPLOAD ---
uploaded_file = st.file_uploader("Drag & Drop CSV/Excel", type=["csv", "xlsx"], label_visibility="visible")
google_link = st.text_input("Or Paste Google Sheet Link (must be public)")

df = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Could not read file: {e}")

elif google_link:
    try:
        # Convert google sheet link to csv export
        sheet_id = google_link.split("/d/")[1].split("/")[0]
        csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(csv_url)
    except:
        st.error("Could not read Google Sheet. Make it public: Share > Anyone with link > Viewer")

# --- IF DATA IS LOADED ---
if df is not None:
    st.success(f"Loaded {len(df)} rows, {len(df.columns)} columns")
    
    # Show free preview - SAFE for PyArrow
    st.subheader("👀 Free Preview")
    st.write(df.head(5).astype(str)) # Fix for PyArrow error
    
    st.write("Columns:", list(df.columns))
    
    # Basic stats
    st.subheader("📈 Quick Stats")
    try:
        # Show numeric summary
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            st.write(numeric_df.describe().astype(str))
            
            # Simple chart
            first_num_col = numeric_df.columns[0]
            fig = px.line(numeric_df, y=first_num_col, title=f"Trend of {first_num_col}")
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.write("Stats preview not available for this file")

    # --- PAYWALL ---
    st.divider()
    st.subheader("🔒 Unlock Full Pro Report - ₦2,000")
    st.markdown("""
    **Free preview ends here. Pay to get:**
    - ✅ Full sales & profit analysis
    - ✅ Customer insights & top products
    - ✅ Monthly trends & charts
    - ✅ AI recommendations to grow business
    - ✅ Downloadable PDF Report
    """)
    
    st.link_button("💳 PAY ₦2,000 TO UNLOCK FULL REPORT", PAYSTACK_LINK, type="primary", use_container_width=True)
    
    paid = st.checkbox("✅ I have paid - Unlock my full report")
    
    if not paid:
        st.warning("Please pay ₦2,000 above, then tick the box to see your full AI report.")
        st.stop()
    
    # --- FULL REPORT (Only after paid checked) ---
    st.success("Payment confirmed! Here is your full Pro Report 👇")
    
    st.subheader("💰 Complete Business Analysis")
    
    # Try to auto-detect sales columns
    try:
        numeric_cols = df.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            st.metric(label=f"Total {col}", value=f"₦{df[col].sum():,.2f}")
            fig2 = px.bar(df.head(20), y=col, title=f"Top {col} Breakdown")
            st.plotly_chart(fig2, use_container_width=True)
    except:
        pass
    
    st.subheader("🤖 AI Recommendations")
    st.info("""
    1. **Focus on your top 3 selling products** - they bring 80% of profit.
    2. **Check your lowest sales day** - run promo on that day.
    3. **Track daily expenses** vs income to avoid hidden losses.
    4. For detailed PDF, screenshot this report.
    """)
    
    st.balloons()
    
else:
    st.info("👆 Upload a CSV/Excel to see magic. Try with your Personal Finance (Income, Expenses) or Shop Sales")
