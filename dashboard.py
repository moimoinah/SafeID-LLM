import streamlit as st
import requests

st.set_page_config(page_title="SafeID-LLM", layout="wide")

st.title("🔐 SafeID-LLM Risk Analysis Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.header("How to use")
st.sidebar.info("""
1. Click **Create DID**
2. Try **Wrong Verify** 3 times (different IP)
3. Risk score will be **90+**!
4. Use **Correct Verify** to return to normal
""")

# Main area - 2 columns
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1️⃣ Create DID")

    endpoint = st.text_input("Service Endpoint", "https://example.com")
    source_ip = st.text_input("Source IP", "1.2.3.4")

    if st.button("🚀 Create DID", type="primary"):
        try:
            response = requests.post("http://127.0.0.1:8000/did/create",
                                     json={"service_endpoint": endpoint, "source_ip": source_ip})
            result = response.json()

            st.success("✅ DID Created!")
            st.json(result)

            st.session_state.did = result["did"]
            st.session_state.pubkey = result["public_key"]

        except Exception as e:
            st.error(f"❌ Error: {e}")

with col2:
    st.header("2️⃣ Verify DID")

    did = st.text_input("DID", value=st.session_state.get('did', ''))
    pubkey = st.text_input("Public Key", value=st.session_state.get('pubkey', ''))
    verify_ip = st.text_input("Source IP", "5.6.7.8")

    col_btn1, col_btn2 = st.columns(2)

    if col_btn1.button("🚨 Wrong Verify (Attack Simulation)"):
        response = requests.post("http://127.0.0.1:8000/did/verify",
                                 json={"did": did, "presented_public_key": "WRONG_KEY", "source_ip": verify_ip})
        result = response.json()
        st.markdown(f"**Risk Score: {result['risk_score']}**")
        st.json(result)

    if col_btn2.button("✅ Correct Verify"):
        response = requests.post("http://127.0.0.1:8000/did/verify",
                                 json={"did": did, "presented_public_key": pubkey, "source_ip": verify_ip})
        result = response.json()
        st.markdown(f"**Risk Score: {result['risk_score']}**")
        st.json(result)

