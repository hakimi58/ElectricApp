import streamlit as st
import requests

# 1. إعدادات أساسية جداً
st.set_page_config(page_title="Tunisia Electric Fix")

st.title("⚡ تطبيق فني الكهرباء (النسخة المستقرة)")

# 2. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("المفتاح مفقود في Secrets!")
else:
    # 3. مدخلات المستخدم
    query = st.text_input("ادخل سؤالك التقني:")

    if st.button("تشغيل"):
        if query:
            # الرابط الذي أثبت نجاحه مع حسابك (2.5-flash)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            
            payload = {
                "contents": [{"parts": [{"text": f"أنت خبير كهرباء، أجب باللهجة التونسية التقنية باختصار: {query}"}]}]
            }

            try:
                response = requests.post(url, json=payload)
                res_json = response.json()
                
                if "candidates" in res_json:
                    output = res_json['candidates'][0]['content']['parts'][0]['text']
                    
                    st.success("تم الاستلام بنجاح:")
                    
                    # الحل النهائي لمشكلة الصفحة البيضاء:
                    # عرض النص داخل منطقة نصية (Text Area) لضمان رؤية اللون الأسود
                    st.text_area(label="الإجابة:", value=output, height=300)
                    
                else:
                    st.error("فشل في استخراج النص")
                    st.json(res_json)
            except Exception as e:
                st.error(f"خطأ اتصال: {e}")
