import streamlit as st
import requests
import json

# 1. إعدادات الواجهة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; background-color: #f0f2f6; }
    </style>
""", unsafe_allow_html=True)

st.write("# ⚡ خبير الكهرباء التونسي")
st.caption("مساعدك الذكي للأعطال والتركيبات الكهربائية في تونس")

# 2. جلب المفتاح
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ المفتاح مفقود في إعدادات Secrets.")
else:
    # 3. واجهة الدردشة
    prompt = st.chat_input("اسأل خبيرك (مثلاً: الفاتورة غالية، مشكلة في التار، توزيع المنقذ...)")

    if prompt:
        with st.chat_message("user"):
            st.write(prompt)

        with st.spinner("جاري استشارة الخبير..."):
            # الرابط الذي أثبت نجاحه مع حسابك
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": f"أنت خبير كهرباء تونسي محترف. أجب بدقة وباللهجة التقنية التونسية (استخدم مصطلحات: فويت، منقذ، ديجونكتور، كونتور، خيوط، جعبة). السؤال: {prompt}"
                    }]
                }],
                "generationConfig": { "temperature": 0.7 }
            }

            try:
                response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
                res_json = response.json()
                
                if "candidates" in res_json:
                    answer = res_json['candidates'][0]['content']['parts'][0]['text']
                    with st.chat_message("assistant"):
                        st.write(answer)
                else:
                    st.error("حدث خطأ مفاجئ في استلام الإجابة.")
            except Exception as e:
                st.error(f"⚠️ خطأ في الاتصال: {e}")

# 4. معلومات جانبية
with st.sidebar:
    st.title("نصائح السلامة")
    st.info("تذكر دائماً: 'الضو ما فيهش لعب'. ديما قص المنقذ قبل ما تخدم أي حاجة.")
