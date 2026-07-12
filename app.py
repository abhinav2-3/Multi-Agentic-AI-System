import streamlit as st
from main2 import app as support_app

st.set_page_config(page_title="Customer Support AI", page_icon="🤖", layout="centered")

st.title("🤖 Customer Support AI")
st.caption("Powered by Multi-Agent AI System")

query = st.text_area(
    "Describe your issue",
    placeholder="e.g. I was charged twice this month...",
    height=120,
)

if st.button("Submit", use_container_width=True):
    if query.strip():
        with st.spinner("Agents working..."):
            result = support_app.invoke(
                {"query": query, "category": "", "resolution": "", "final_response": ""}
            )

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Category", result["category"].upper())

        st.divider()
        st.subheader("Final Response")
        st.success(result["final_response"])

        with st.expander("Internal Resolution"):
            st.write(result["resolution"])
    else:
        st.warning("Please enter a query.")
