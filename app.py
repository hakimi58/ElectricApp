import streamlit as st
import requests
import json

st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.write("# ⚡ خبير الكهرباء التونسي")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ المفتاح السري مفقود في إعدادات Secrets.")
else:
    prompt = st.chat_input("اسأل خبيرك...")

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("جاري الاتصال بالخبير..."):
            # سنقوم بتجربة الروابط الأكثر شيوعاً والتي تعمل حالياً في 2026
            urls = [
                f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}",
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
                f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
            ]
            
            success = False
            for url in urls:
                try:
                    payload = {
                        "contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي، أجب باللهجة التونسية التقنية: {prompt}"}]}]
                    }
                    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload)
                    res_json = response.json()
                    
                    if "candidates" in res_json:
                        answer = res_json['candidates'][0]['content']['parts'][0]['text']
                        with st.chat_message("assistant"):
                            st.write(answer)
                        success = True
                        break # إذا نجح أحد الروابط، توقف عن المحاولة
                except:
                    continue
            
            if not success:
                st.error("❌ تعذر الاتصال بجميع نسخ الموديل. تأكد من تفعيل Gemini API في حسابك.")
                with st.expander("تفاصيل الخطأ الأخير"):
                    st.json(res_json)
