import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DataSabi", page_icon="📊", layout="centered")
PAYSTACK_LINK = "https://paystack.shop/pay/2jji7vgoln"

# AUTO-UNLOCK LOGIC - NO CHECKBOX
if st.query_params.get("paid") == "true":
    st.session_state.paid = True

if "paid" not in st.session_state:
    st.session_state.paid = False

st.title("📊 DataSabi")
st.caption("Upload Your Data, Get Insights 🇳🇬")

uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
df = None
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    except:
        df = pd.read_excel(uploaded_file)

if df is not None:
    st.success(f"Loaded {len(df)} rows")
    st.write(df.head(5).astype(str))

    if not st.session_state.paid:
        st.divider()
        st.subheader("🔒 Unlock Full Pro Report - ₦2,000")
        st.link_button("💳 PAY ₦2,000 - AUTO UNLOCK", PAYSTACK_LINK, type="primary", use_container_width=True)
        st.caption("After payment, you'll be sent back here and full report opens automatically. No checkbox needed.")
        st.stop()
    
    # --- FULL REPORT - AUTO OPENED ---
    st.balloons()
    st.success("✅ Payment verified! Full Pro Report unlocked")
    st.write(df.describe().astype(str))
    try:
        numeric_df = df.select_dtypes(include=['number'])
        if not numeric_df.empty:
            fig = px.line(numeric_df, y=numeric_df.columns[0], title="Trend")
            st.plotly_chart(fig, use_container_width=True)
    except:
        pass
    st.info("💡 Recommendation: Focus on your top products and run promos on slow days.")
else:
    st.info("👆 Upload a file to start")

if st.session_state.get("paid"):
    if st.button("Lock & Start Over"):
        st.session_state.paid = False
        st.query_params.clear()
        st.rerun()
