import streamlit as st
import pandas as pd
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. جلب المفتاح
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة البيانات (الفورو والمواد التونسية)
DB_MATERIELS = {
    "Foureau Orange 11mm (Rouleau)": 28.500,
    "Foureau Orange 13mm (Rouleau)": 32.800,
    "Foureau Orange 16mm (Rouleau)": 38.000,
    "Foureau Orange 20mm (Rouleau)": 48.500,
    "Hager: Disjoncteur DPN 16A": 9.800,
    "Tunisie Câbles: 1.5mm² (100m)": 65.000,
    "Legrand Valena: Prise 2P+T": 11.200
}

# 4. اختيار الأداة
st.sidebar.title("القائمة")
choice = st.sidebar.radio("🛠️ الأدوات", ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"])

# --- القسم 1: استشارة الخبير (استخدام موديل 2.0 المستقر لتفادي زحمة 503) ---
if choice == "استشارة الخبير (AI)":
    st.subheader("🤖 خبير الكهرباء الذكي")
    query = st.text_area("اسأل الخبير (بالدارجة التونسية):")
    
    if st.button("تحليل السؤال"):
        if not API_KEY:
            st.error("المفتاح غير موجود!")
        elif query:
            with st.spinner("جاري الاتصال بالسيرفر (نسخة 2.0 المستقرة)..."):
                # غيرنا الموديل إلى 2.0-flash لأنه أقل زحمة وأكثر استقراراً
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
                
                payload = {
                    "contents": [{
                        "parts": [{"text": f"أنت خبير كهرباء تونسي محترف. أجب بالدارجة التونسية التقنية وبوضوح: {query}"}]
                    }]
                }
                
                try:
                    res = requests.post(url, json=payload, timeout=20)
                    if res.status_code == 200:
                        st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
                    elif res.status_code == 503:
                        st.warning("السيرفر مشغول حالياً (Overload). انتظر 10 ثواني واضغط على الزر مرة أخرى.")
                    else:
                        st.error(f"خطأ {res.status_code}: {res.text}")
                except:
                    st.error("مشكلة في الاتصال. حاول مرة أخرى.")

# --- الأقسام الأخرى ---
elif choice == "حاسبة القياسات":
    watt = st.number_input("قوة الجهاز (Watt):", value=2000)
    st.success(f"التيار: {watt/220:.2f} A")

elif choice == "نظام الفواتير":
    st.subheader("📄 الفواتير")
    prod = st.selectbox("المادة:", list(DB_MATERIELS.keys()))
    st.write(f"ثمن {prod} هو {DB_MATERIELS[prod]:.3f} DT")
