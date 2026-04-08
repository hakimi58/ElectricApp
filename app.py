import streamlit as st
import google.generativeai as genai

st.title("⚡ خبير الكهرباء التونسي")
key = st.secrets.get("GOOGLE_API_KEY")

if key:
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    query = st.text_input("اسأل خبيرك:")
    if st.button("إجابة"):
        st.write(model.generate_content(query).text)
else:
    st.error("المفتاح ناقص في Secrets!")
