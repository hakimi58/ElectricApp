import streamlit as st
import requests
import json

st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.write("# ⚡ خبير الكهرباء التونسي")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ المفتاح السري مفقود في إعدادات Secrets.")
else:
    prompt = st.chat_input("اسأل خبيرك (مثلاً: الفاتورة غالية، فمّا فويت...)")

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("جاري البحث عن أفضل مسار للاتصال بالخبير..."):
            # قائمة شاملة لكل الاحتمالات الممكنة لروابط Gemini في 2026
            urls = [
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
                f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}",
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}",
                f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
            ]
            
            success = False
            last_error = ""

            for url in urls:
                try:
                    payload = {
                        "contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي محترف، أجب باللهجة التونسية التقنية وبدقة على هذا السؤال: {prompt}"}]}]
                    }
                    response = requests.post(url, headers={'Content-Type': 'application/json'}, json=payload, timeout=10)
                    res_json = response.json()
                    
                    if "candidates" in res_json:
                        answer = res_json['candidates'][0]['content']['parts'][0]['text']
                        with st.chat_message("assistant"):
                            st.write(answer)
                        success = True
                        break 
                    else:
                        last_error = res_json
                except Exception as e:
                    last_error = str(e)
                    continue
            
            if not success:
                st.error("❌ فشلت جميع محاولات الاتصال.")
                with st.expander("اضغط هنا لرؤية تفاصيل العطل التقني"):
                    st.write("آخر رد من السيرفر:")
                    st.json(last_error)
                st.info("نصيحة: تأكد من أن مفتاح API الخاص بك مفعل (Enabled) في Google AI Studio.")

with st.sidebar:
    st.info("نصيحة الخبير: إذا كانت الفاتورة غالية، تثبت من 'الترموستا' متاع الشوفو (Chauffe-eau).")
