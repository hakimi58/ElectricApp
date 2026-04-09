import streamlit as st
import pandas as pd
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", layout="wide")

# 2. جلب المفتاح
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة البيانات (الفورو والمواد)
DB = {
    "Foureau Orange 11mm": 28.500, "Foureau Orange 13mm": 32.800,
    "Foureau Orange 16mm": 38.000, "Foureau Orange 20mm": 48.500,
    "Hager 16A": 9.800, "Tunisie Câbles 1.5mm": 65.000
}

# 4. الواجهة
st.sidebar.title("الإعدادات")
choice = st.sidebar.radio("الأدوات", ["استشارة الخبير (AI)", "الفاتورة"])

if choice == "استشارة الخبير (AI)":
    st.subheader("🤖 استشارة الخبير")
    query = st.text_area("اسأل الخبير:")
    
    if st.button("تحليل"):
        if not API_KEY:
            st.error("المفتاح غير موجود في Secrets!")
        else:
            with st.spinner("جاري تجربة الاتصال..."):
                # محاولة الاتصال بموديل gemini-1.5-flash برابط v1 (أحدث نسخة)
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": f"أنت خبير كهرباء تونسي، أجب بالدارجة: {query}"}]
                    }]
                }
                
                try:
                    res = requests.post(url, json=payload, timeout=10)
                    if res.status_code == 200:
                        st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"فشل الاتصال بكود {res.status_code}")
                        # هنا السر: سنطلب من السيرفر إخبارنا ما هي الموديلات التي يقبلها مفتاحك
                        st.warning("🧐 جاري فحص الموديلات المتاحة لمفتاحك...")
                        diag_url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"
                        diag_res = requests.get(diag_url)
                        if diag_res.status_code == 200:
                            models = [m['name'] for m in diag_res.json().get('models', [])]
                            st.write("الموديلات التي يدعمها مفتاحك حالياً هي:", models)
                        else:
                            st.write("السيرفر يرفض حتى قائمة الموديلات. هذا يعني أن المفتاح يحتاج تفعيل من Google AI Studio.")
                except Exception as e:
                    st.error(f"خطأ: {e}")

elif choice == "الفاتورة":
    st.subheader("📄 نظام الفواتير (الفورو)")
    prod = st.selectbox("المادة:", list(DB.keys()))
    st.write(f"الثمن التقديري: {DB[prod]:.3f} DT")
