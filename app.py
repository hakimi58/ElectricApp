import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات المواد
DB_MATERIELS = {
    "Foureau Orange 11mm": 28.500, "Foureau Orange 13mm": 32.800,
    "Foureau Orange 16mm": 38.000, "Foureau Orange 20mm": 48.500,
    "Hager: Disjoncteur 16A": 9.800, "Tunisie Câbles: 1.5mm": 65.000
}

# 3. جلب المفتاح (نحاول جلب المفتاح بكل الطرق الممكنة)
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 4. اللغات
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_options.keys()))
L = lang_options[L_key]

# 5. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", ["استشارة الخبير (AI)", "حاسبة القياسات", "تحرير فاتورة"])

# --- القسم الأول: استشارة الخبير (مع كاشف الأخطاء) ---
if choice == "استشارة الخبير (AI)":
    st.subheader("🤖 استشارة الخبير")
    query = st.text_area("اشرح المشكلة هنا:")
    
    if st.button("تحليل"):
        if not API_KEY:
            st.error("❌ المفتاح غير موجود! تأكد من كتابة GOOGLE_API_KEY في الـ Secrets.")
        elif query:
            with st.spinner("جاري الاتصال بالسيرفر..."):
                # جربنا v1beta، الآن سنجرب v1 (أكثر استقراراً)
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي، أجب بالدارجة: {query}"}]}]}
                
                try:
                    res = requests.post(url, json=payload, timeout=15)
                    
                    if res.status_code == 200:
                        st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
                    elif res.status_code == 400:
                        st.error(f"خطأ 400: الطلب غير صحيح. (تأكد من نسخ المفتاح كاملاً)")
                    elif res.status_code == 403:
                        st.error(f"خطأ 403: المفتاح لا يملك صلاحية. (تأكد من تفعيل Gemini API في Google AI Studio)")
                    elif res.status_code == 404:
                        st.error(f"خطأ 404: الرابط غير موجود. جاري تجربة رابط بديل...")
                        # محاولة برابط آخر تلقائياً
                        url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                        res_alt = requests.post(url_alt, json=payload, timeout=15)
                        if res_alt.status_code == 200:
                            st.info(res_alt.json()['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"فشل الاتصال النهائي. كود الخطأ: {res_alt.status_code}")
                    else:
                        st.error(f"خطأ غير معروف: {res.status_code}")
                except Exception as e:
                    st.error(f"📡 فشل الاتصال بالانترنت: {e}")

# --- باقي الأقسام ---
elif choice == "حاسبة القياسات":
    watt = st.number_input("القدرة (Watt):", value=2000)
    st.success(f"التيار: {watt/220:.2f} A")

elif choice == "تحرير فاتورة":
    st.write("أضف المواد من القائمة...")
