import streamlit as st
import requests
import json

st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.write("# ⚡ خبير الكهرباء التونسي")

# جلب المفتاح
key = st.secrets.get("GOOGLE_API_KEY")

if key:
    prompt = st.chat_input("اسأل خبيرك...")
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        
        with st.spinner("جاري استشارة الخبير عبر الرابط المباشر..."):
            # رابط API المباشر لجوجل (بدون الحاجة لمكتبة genai)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
            
            headers = {'Content-Type': 'application/json'}
            data = {
                "contents": [{
                    "parts": [{"text": f"أنت خبير كهرباء تونسي محترف. أجب بدقة وباللهجة التقنية التونسية على السؤال التالي: {prompt}"}]
                }]
            }
            
            try:
                response = requests.post(url, headers=headers, data=json.dumps(data))
                result = response.json()
                
                # استخراج النص من النتيجة
                answer = result['candidates'][0]['content']['parts'][0]['text']
                
                with st.chat_message("assistant"):
                    st.write(answer)
            except Exception as e:
                st.error(f"⚠️ عطل فني: {str(e)}")
else:
    st.error("المفتاح السري ناقص")
