import streamlit as st
import requests
import json

# 1. إعدادات الصفحة والواجهة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stChatMessage {
        border-radius: 15px;
    }
    </style>
""", unsafe_allow_html=True)

st.write("# ⚡ خبير الكهرباء التونسي")
st.caption("مساعدك الذكي لتشخيص الأعطال الكهربائية في تونس")

# 2. جلب المفتاح السري من إعدادات Streamlit
# تأكد من إضافة GOOGLE_API_KEY في Secrets على منصة Streamlit
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ خطأ: المفتاح السري GOOGLE_API_KEY مفقود. يرجى إضافته في إعدادات التطبيق.")
else:
    # 3. واجهة الدردشة
    prompt = st.chat_input("اسأل خبيرك (مثلاً: الفاتورة غالية، القاطع يسقط...)")

    if prompt:
        # عرض سؤال المستخدم
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("جاري استشارة الخبير..."):
            # رابط API المباشر لـ Gemini 1.5 Flash
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            
            headers = {'Content-Type': 'application/json'}
            
            # صياغة الطلب مع توجيه الشخصية (System Prompt)
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"أنت خبير كهرباء تونسي محترف ومتمكن. أجب بدقة، بوضوح، وباللهجة التقنية التونسية (استخدم مصطلحات مثل: فويت، منقذ، كونتور، ديجونكتور) على السؤال التالي: {prompt}"
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.7,
                    "maxOutputTokens": 1000
                }
            }

            try:
                # إرسال الطلب
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response_json = response.json()
                
                # استخراج النص من استجابة جوجل
                if "candidates" in response_json:
                    answer = response_json['candidates'][0]['content']['parts'][0]['text']
                    with st.chat_message("assistant"):
                        st.write(answer)
                else:
                    st.error("حدث خطأ في استجابة الذكاء الاصطناعي. تأكد من صحة المفتاح.")
                    # عرض تفاصيل الخطأ للمبرمج (أنت) لتسهيل الإصلاح
                    with st.expander("تفاصيل الخطأ التقني"):
                        st.write(response_json)
                        
            except Exception as e:
                st.error(f"⚠️ فشل الاتصال بالسيرفر: {str(e)}")

# 4. قائمة جانبية بسيطة
with st.sidebar:
    st.title("حول التطبيق")
    st.info("هذا التطبيق يستخدم الذكاء الاصطناعي لتقديم نصائح كهربائية عامة. استشر دائماً فني مختص للأمور الخطيرة.")
