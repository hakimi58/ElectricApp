import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. جلب المفتاح من Secrets
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة البيانات (المواد التونسية)
DATABASE_PRO = {
    "Foureau Orange 11mm": 28.500, "Foureau Orange 13mm": 32.800,
    "Foureau Orange 16mm": 38.000, "Foureau Orange 20mm": 48.500,
    "Hager: Disjoncteur 16A": 9.800, "Hager: Diff 40A": 95.000,
    "Legrand Valena: Prise": 11.200, "Tunisie Câbles: 1.5mm": 65.000
}

if 'cart' not in st.session_state: st.session_state['cart'] = []

# 4. نظام اللغات
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_options.keys()))
L = lang_options[L_key]

texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"],
        "ai_label": "اسأل الخبير (بالدارجة التونسية):",
        "prompt": "أنت خبير كهرباء بناء تونسي. أجب بالدارجة التونسية التقنية."
    },
    "Français": {
        "title": "⚡ Pro Electric Platform",
        "menu": ["Consultation AI", "Calculateur", "Factures"],
        "ai_label": "Demander à l'expert :",
        "prompt": "Tu es un expert électricien. Réponds en français technique."
    }
}
curr = texts.get(L, texts["تونس"])

# 5. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- القسم 1: استشارة الخبير (الربط المطور لتفادي 404) ---
if choice == curr["menu"][0]:
    st.subheader("🤖 خبير الكهرباء الذكي")
    query = st.text_area(curr["ai_label"], placeholder="اكتب سؤالك هنا...")
    
    if st.button("تحليل السؤال 🤖"):
        if not API_KEY:
            st.error("❌ المفتاح GOOGLE_API_KEY غير موجود في Secrets.")
        elif query:
            with st.spinner("جاري الاتصال بالسيرفر..."):
                # الطريقة الجديدة للرابط لضمان العمل
                url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
                headers = {'Content-Type': 'application/json'}
                data = {
                    "contents": [{
                        "parts": [{"text": f"{curr['prompt']} : {query}"}]
                    }]
                }
                
                try:
                    # قمنا بتغيير الموديل إلى gemini-pro لضمان التوافق
                    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=15)
                    
                    if response.status_code == 200:
                        res_json = response.json()
                        answer = res_json['candidates'][0]['content']['parts'][0]['text']
                        st.info(answer)
                    elif response.status_code == 404:
                        st.error("خطأ 404: السيرفر لم يجد هذا الرابط. جاري تجربة رابط بديل...")
                        # محاولة ثانية برابط مختلف تلقائياً
                        url_alt = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                        res_alt = requests.post(url_alt, headers=headers, data=json.dumps(data), timeout=15)
                        if res_alt.status_code == 200:
                            st.info(res_alt.json()['candidates'][0]['content']['parts'][0]['text'])
                        else:
                            st.error(f"فشل الاتصال النهائي (كود: {res_alt.status_code}). تأكد من أن الـ API Key مفعل.")
                    else:
                        st.error(f"فشل الاتصال. الكود: {response.status_code}")
                except Exception as e:
                    st.error(f"خطأ غير متوقع: {str(e)}")

# --- الأقسام الأخرى ---
elif choice == curr["menu"][1]:
    st.subheader("🧮 حاسبة القياسات")
    watt = st.number_input("القدرة (Watt):", value=2000)
    st.success(f"التيار: {watt/220:.2f} A")

elif choice == curr["menu"][2]:
    st.subheader("📄 نظام الفواتير")
    st.write("أضف المواد من القائمة")
