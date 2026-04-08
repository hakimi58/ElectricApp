import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Tunisia Electric", layout="centered")

st.write("# ⚡ خبير الكهرباء التونسي")

key = st.secrets.get("GOOGLE_API_KEY")

if key:
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = st.chat_input("اسأل خبيرك...")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        with st.spinner("جاري التحضير..."):
            res = model.generate_content(f"أنت خبير كهرباء تونسي: {prompt}")
            with st.chat_message("assistant"):
                st.write(res.text)
else:
    st.error("المفتاح السري ناقص")
