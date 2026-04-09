import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. جلب المفتاح من الـ Secrets
# تأكد أن الاسم في الإعدادات هو GOOGLE_API_KEY
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة البيانات الشاملة
DATABASE_PRO = {
    "Foureau Orange 11mm (Rouleau)": 28.500, "Foureau Orange 13mm (Rouleau)": 32.800,
    "Foureau Orange 16mm (Rouleau)": 38.000, "Foureau Orange 20mm (Rouleau)": 48.500,
    "Foureau Noir (Béton) 16mm": 42.000, "Foureau Noir (Béton) 20mm": 52.000,
    "Hager: Disjoncteur DPN 10A": 10.500, "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800, "Hager: Différentiel 40A 30mA": 95.000,
    "Hager: Coffret Encastré 24M": 145.000, "Legrand Valena: Prise 2P+T": 11.200,
    "Tunisie Câbles: 1.5mm² (100m)": 65.000, "Tunisie Câbles: 2.5mm² (100m)": 105.000,
    "Générale: Boite Encastrement 3M": 0.900, "Spot LED 7W Encastré": 6.800
}

if 'cart' not in st.session_state:
    st.session_state['cart'] = []

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

# 5. الواجهة
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- القسم 1: استشارة الخبير (تصحيح خطأ 404) ---
if choice == curr["menu"][0]:
    st.subheader("🤖 خبير الكهرباء الذكي")
    query = st.text_area(curr["ai_label"], placeholder="اكتب سؤالك هنا...")
    
    if st.button("تحليل السؤال"):
        if not API_KEY:
            st.error("❌ المفتاح غير موجود في Secrets.")
        elif query:
            with st.spinner("جاري الاتصال..."):
                # تحديث الرابط لضمان عدم حدوث خطأ 404
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                headers = {'Content-Type': 'application/json'}
                payload = {"contents": [{"parts": [{"text": f"{curr['prompt']} : {query}"}]}]}
                
                try:
                    res = requests.post(url, json=payload, headers=headers, timeout=15)
                    if res.status_code == 200:
                        st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
                    else:
                        st.error(f"فشل الاتصال. الكود: {res.status_code}. ثبت من إعدادات الـ API في جوجل.")
                except Exception as e:
                    st.error(f"خطأ غير متوقع: {str(e)}")

# --- القسم 2: الحاسبة ---
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    watt = st.number_input("القدرة (Watt):", value=2000)
    amp = watt / 220
    st.success(f"التيار: {amp:.2f} A")

# --- القسم 3: الفاتورة ---
elif choice == curr["menu"][2]:
    st.subheader("📄 نظام الفواتير")
    with st.expander("➕ إضافة مواد"):
        search = st.text_input("🔍 بحث:")
        filtered = [k for k in DATABASE_PRO.keys() if search.lower() in k.lower()]
        prod = st.selectbox("المادة:", filtered if filtered else list(DATABASE_PRO.keys()))
        qte = st.number_input("الكمية:", min_value=1, value=1)
        if st.button("إضافة ➕"):
            st.session_state['cart'].append({"المادة": prod, "الكمية": qte, "الثمن": DATABASE_PRO[prod], "المجموع": qte * DATABASE_PRO[prod]})
            st.rerun()

    if st.session_state['cart']:
        df = pd.DataFrame(st.session_state['cart'])
        edited_df = st.data_editor(df, use_container_width=True)
        st.markdown(f"### المجموع: {edited_df['المجموع'].sum():.3f} DT")
