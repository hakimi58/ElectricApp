import streamlit as st
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

# تنسيق CSS بسيط لجعل المحادثة تبدو أفضل
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.write("# ⚡ خبير الكهرباء التونسي")
st.caption("مساعدك التقني للأعطال الكهربائية في تونس")

# 2. جلب مفتاح API من إعدادات Streamlit Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ خطأ: المفتاح السري (GOOGLE_API_KEY) مفقود في إعدادات Secrets.")
else:
    # 3. واجهة إدخال السؤال
    prompt = st.chat_input("اسأل خبيرك (مثلاً: الفاتورة غالية، فمّا فويت، ديجونكتور يطيح...)")

    if prompt:
        # عرض سؤال المستخدم
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("جاري استشارة الخبير التونسي..."):
            # الرابط المحدث لعام 2026 (استخدام v1 لضمان التوافق)
            url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            headers = {'Content-Type': 'application/json'}
            
            # صياغة الطلب (Payload)
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"أنت خبير كهرباء تونسي محترف. أجب بدقة، بوضوح، وباللهجة التقنية التونسية (استخدم كلمات مثل: منقذ، فويت، كونتور، ديجونكتور، خيوط) على السؤال التالي: {prompt}"
                    }]
                }]
            }

            try:
                # إرسال الطلب عبر requests
                response = requests.post(url, headers=headers, json=payload)
                response_json = response.json()
                
                # استخراج الإجابة
                if "candidates" in response_json:
                    answer = response_json['candidates'][0]['content']['parts'][0]['text']
                    with st.chat_message("assistant"):
                        st.write(answer)
                else:
                    # في حال وجود خطأ في المفتاح أو الموديل
                    st.error("❌ عذراً، لم أتمكن من الحصول على إجابة.")
                    with st.expander("رؤية تفاصيل الخطأ"):
                        st.json(response_json)
                        
            except Exception as e:
                st.error(f"⚠️ خطأ في الاتصال: {str(e)}")

# 4. معلومات إضافية في القائمة الجانبية
with st.sidebar:
    st.title("حول المشروع")
    st.write("تطبيق ذكاء اصطناعي مخصص للفنيين والمواطنين في تونس.")
    st.warning("⚠️ تنبيه: الكهرباء خطيرة، لا تلمس الأسلاك إذا لم تكن مختصاً.")
