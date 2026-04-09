import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. جلب المفتاح من Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة البيانات (الفورو والمواد التونسية)
DB_MATERIELS = {
    "Foureau Orange 11mm": 28.500,
    "Foureau Orange 13mm": 32.800,
    "Foureau Orange 16mm": 38.000,
    "Foureau Orange 20mm": 48.500,
    "Hager: Disjoncteur 16A": 9.800,
    "Tunisie Câbles: 1.5mm": 65.000,
    "Legrand Valena: Prise": 11.200
}

# 4. ذاكرة الفاتورة
if 'invoice' not in st.session_state:
    st.session_state['invoice'] = []

# 5. اللغات
lang = st.sidebar.selectbox("🌐 اللغة", ["🇹🇳 تونسية", "🇫🇷 Français"])

# 6. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"])

# --- القسم 1: استشارة الخبير (تم إصلاح الرابط والموديل) ---
if choice == "استشارة الخبير (AI)":
    st.subheader("🤖 خبير الكهرباء الذكي")
    query = st.text_area("اسأل الخبير (بالدارجة):", placeholder="مثلاً: كيفاش نركب لوحة قواطع؟")
    
    if st.button("تحليل السؤال"):
        if not API_KEY:
            st.error("❌ المفتاح غير موجود في Secrets!")
        elif query:
            with st.spinner("جاري الاتصال بالخبير..."):
                # هذا هو الرابط الذي سيحل مشكلة 404 نهائياً
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"أنت خبير كهرباء تونسي محترف، أجب بالدارجة التونسية التقنية: {query}"}]
                    }]
                }
                
                try:
                    res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
                    if res.status_code == 200:
                        ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                        st.info(ans)
                    else:
                        st.error(f"خطأ {res.status_code}: السيرفر لا يستجيب. جرب مفتاحاً جديداً.")
                except Exception as e:
                    st.error(f"📡 مشكلة اتصال: {e}")

# --- القسم 2: حاسبة القياسات ---
elif choice == "حاسبة القياسات":
    st.subheader("🧮 حاسبة مقاطع الأسلاك")
    watt = st.number_input("قوة الجهاز (Watt):", value=2000)
    amp = watt / 220
    wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
    st.success(f"التيار المقدر: {amp:.2f} A | السلك المناسب: {wire}")

# --- القسم 3: نظام الفواتير (الفورو) ---
elif choice == "نظام الفواتير":
    st.subheader("📄 إنشاء فاتورة")
    prod = st.selectbox("اختر المادة:", list(DB_MATERIELS.keys()))
    qte = st.number_input("الكمية:", min_value=1, value=1)
    
    if st.button("إضافة للفاتورة"):
        st.session_state['invoice'].append({"المادة": prod, "الكمية": qte, "المجموع": qte * DB_MATERIELS[prod]})
        st.rerun()

    if st.session_state['invoice']:
        df = pd.DataFrame(st.session_state['invoice'])
        st.table(df)
        st.markdown(f"### المجموع: {df['المجموع'].sum():.3f} DT")
        if st.button("🗑️ مسح"):
            st.session_state['invoice'] = []
            st.rerun()
