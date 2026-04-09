import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف 2026", page_icon="⚡", layout="wide")

# 2. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة البيانات (الفورو والمواد التونسية)
DB_MATERIELS = {
    "Foureau Orange 11mm (Rouleau)": 28.500,
    "Foureau Orange 13mm (Rouleau)": 32.800,
    "Foureau Orange 16mm (Rouleau)": 38.000,
    "Foureau Orange 20mm (Rouleau)": 48.500,
    "Hager: Disjoncteur DPN 16A": 9.800,
    "Tunisie Câbles: 1.5mm² (100m)": 65.000,
    "Legrand Valena: Prise 2P+T": 11.200,
    "Spot LED 7W Encastré": 6.800
}

if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 4. اللغات
lang = st.sidebar.selectbox("🌐 اللغة", ["🇹🇳 تونسية", "🇫🇷 Français"])

# 5. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"])

# --- القسم 1: استشارة الخبير (استخدام الموديل الجديد 2.5 Flash) ---
if choice == "استشارة الخبير (AI)":
    st.subheader("🤖 خبير الكهرباء الذكي (Gemini 2.5)")
    query = st.text_area("اسأل الخبير (بالدارجة التونسية):", placeholder="مثلاً: كيفاش نحمي الدار من السيرشارج؟")
    
    if st.button("تحليل السؤال"):
        if not API_KEY:
            st.error("❌ المفتاح غير موجود في Secrets!")
        elif query:
            with st.spinner("جاري الاتصال بأحدث موديل 2.5..."):
                # تم تحديث الرابط والموديل بناءً على تشخيصك
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                headers = {'Content-Type': 'application/json'}
                payload = {
                    "contents": [{
                        "parts": [{"text": f"أنت خبير كهرباء تونسي محترف. أجب بالدارجة التونسية التقنية: {query}"}]
                    }]
                }
                
                try:
                    res = requests.post(url, headers=headers, data=json.dumps(payload), timeout=15)
                    if res.status_code == 200:
                        ans = res.json()['candidates'][0]['content']['parts'][0]['text']
                        st.info(ans)
                    else:
                        st.error(f"خطأ {res.status_code}: السيرفر لم يقبل الطلب. التفاصيل: {res.text}")
                except Exception as e:
                    st.error(f"📡 مشكلة اتصال: {e}")

# --- القسم 2: حاسبة القياسات ---
elif choice == "حاسبة القياسات":
    st.subheader("🧮 حاسبة مقاطع الأسلاك")
    watt = st.number_input("قوة الجهاز (Watt):", value=2000)
    amp = watt / 220
    wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
    st.success(f"التيار: {amp:.2f} A | السلك: {wire}")

# --- القسم 3: نظام الفواتير (الفورو) ---
elif choice == "نظام الفواتير":
    st.subheader("📄 إنشاء فاتورة")
    prod = st.selectbox("اختر المادة:", list(DB_MATERIELS.keys()))
    qte = st.number_input("الكمية:", min_value=1, value=1)
    
    if st.button("إضافة للفاتورة"):
        st.session_state['cart'].append({"المادة": prod, "الكمية": qte, "المجموع": qte * DB_MATERIELS[prod]})
        st.rerun()

    if st.session_state['cart']:
        df = pd.DataFrame(st.session_state['cart'])
        st.table(df)
        st.markdown(f"### المجموع الجملي: :green[{df['المجموع'].sum():.3f} DT]")
        if st.button("🗑️ مسح"):
            st.session_state['cart'] = []
            st.rerun()
