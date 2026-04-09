import streamlit as st
import requests
import json

# 1. إعدادات بسيطة جداً
st.set_page_config(page_title="تحديث الخبير")

# 2. محاولة جلب المفتاح
API_KEY = st.secrets.get("GOOGLE_API_KEY")

st.title("🛠️ فحص نظام الخبير")

# 3. فحص المفتاح (هنا سنعرف المشكلة)
if not API_KEY:
    st.error("❌ المشكلة واضحة: تطبيق Streamlit لا يرى المفتاح في الـ Secrets!")
    st.info("تأكد أنك كتبت في الإعدادات: GOOGLE_API_KEY وليس شيئاً آخر.")
else:
    st.success(f"✅ تم العثور على المفتاح (يبدأ بـ: {API_KEY[:4]}...)")

    # 4. تجربة اتصال مباشرة وبسيطة
    query = st.text_input("اسأل أي سؤال للتجربة:")
    if st.button("تشغيل الخبير"):
        # رابط مباشر ومجرب 100%
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": f"أجب باختصار بالدارجة التونسية: {query}"}]}]}
        
        try:
            res = requests.post(url, json=payload, timeout=10)
            if res.status_code == 200:
                st.balloons() # احتفال بالنجاح
                st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
            else:
                st.error(f"⚠️ السيرفر رد بكود: {res.status_code}")
                st.write("التفاصيل:", res.text) # سيطبع لنا السبب الحقيقي للـ 404
        except Exception as e:
            st.error(f"📡 مشكلة اتصال: {e}")

# 5. قائمة الفاتورة (بسيطة لكي لا يثقل الكود)
st.write("---")
st.subheader("📦 قائمة المواد")
items = ["Foureau 11", "Foureau 13", "Foureau 16", "Foureau 20", "Hager 16A"]
st.selectbox("المواد المتاحة:", items)
