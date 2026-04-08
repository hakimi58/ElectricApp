import streamlit as st
import requests
import json

st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.write("# ⚡ خبير الكهرباء التونسي")

# جلب المفتاح الجديد الذي أنشأته
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ المفتاح غير موجود في Secrets.")
else:
    prompt = st.chat_input("اسأل خبيرك...")

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("جاري الاتصال بخبير الكهرباء..."):
            # هذا هو الرابط الصحيح والمؤكد لعام 2026 لموديل Flash
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": f"أنت خبير كهرباء تونسي. أجب باللهجة التونسية: {prompt}"}]
                }]
            }
            
            try:
                response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
                res_json = response.json()
                
                if "candidates" in res_json:
                    answer = res_json['candidates'][0]['content']['parts'][0]['text']
                    with st.chat_message("assistant"):
                        st.write(answer)
                else:
                    st.error("❌ السيرفر استلم الطلب لكنه رفض الإجابة.")
                    st.json(res_json) # هذا سيظهر لنا السبب الحقيقي داخل الـ JSON
            except Exception as e:
                st.error(f"⚠️ خطأ في الاتصال: {str(e)}")
