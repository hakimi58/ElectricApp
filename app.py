import streamlit as st
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

st.write("# ⚡ خبير الكهرباء التونسي")
st.caption("مساعدك التقني للأعطال الكهربائية في تونس")

# 2. جلب مفتاح API من إعدادات Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ خطأ: المفتاح السري (GOOGLE_API_KEY) مفقود في إعدادات Secrets.")
else:
    # 3. واجهة إدخال السؤال
    prompt = st.chat_input("اسأل خبيرك (مثلاً: الفاتورة غالية، القاطع يسقط...)")

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("جاري استشارة الخبير التونسي..."):
            # تم تغيير الرابط والموديل إلى gemini-pro لضمان التوافق التام واختفاء خطأ 404
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
            
            headers = {'Content-Type': 'application/json'}
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"أنت خبير كهرباء تونسي محترف. أجب بدقة، بوضوح، وباللهجة التقنية التونسية (استخدم كلمات مثل: منقذ، فويت، كونتور، ديجونكتور، خيوط) على السؤال التالي: {prompt}"
                    }]
                }]
            }

            try:
                response = requests.post(url, headers=headers, json=payload)
                response_json = response.json()
                
                # التحقق من وجود إجابة في القائمة
                if "candidates" in response_json and len(response_json["candidates"]) > 0:
                    answer = response_json['candidates'][0]['content']['parts'][0]['text']
                    with st.chat_message("assistant"):
                        st.write(answer)
                else:
                    st.error("❌ حدثت مشكلة في العثور على الموديل المناسب.")
                    with st.expander("رؤية تفاصيل الخطأ التقني"):
                        st.json(response_json)
                        
            except Exception as e:
                st.error(f"⚠️ خطأ في الاتصال: {str(e)}")

# 4. قائمة جانبية
with st.sidebar:
    st.title("حول المشروع")
    st.warning("⚠️ تنبيه: الكهرباء خطيرة، استشر مختصاً دائماً.")
