import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="Pro Electric Platform", page_icon="⚡", layout="wide")

# 2. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. نظام الترجمة الكامل (عربي/تونسية، فرنسية، إنجليزية)
translations = {
    "🇹🇳 العربية/تونسية": {
        "title": "⚡ منصة الكهربائي المحترف",
        "sidebar_title": "🛠️ لوحة التحكم",
        "menu": ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 نظام الفواتير"],
        "ai_header": "🤖 خبير الكهرباء الذكي (تونس)",
        "ai_info": "اسأل الخبير بالدارجة التونسية أو العربية التقنية",
        "ai_placeholder": "مثلاً: كيفاش نركب لوحة قواطع (Tableau)؟",
        "btn_send": "تحليل وإجابة 🚀",
        "calc_header": "🧮 حاسبة مقاطع الأسلاك (Câbles)",
        "watt_label": "قوة الجهاز (Watt):",
        "invoice_header": "📄 تحرير فاتورة تقديرية (Devis)",
        "add_item": "إضافة مادة للفاتورة",
        "search_label": "🔍 ابحث عن مادة (فورو، كابل...):",
        "total_label": "المجموع الجملي",
        "table_cols": ["المادة", "الكمية", "الثمن", "المجموع"],
        "prompt": "أنت خبير كهرباء تونسي محترف جداً. أجب بمزيج من اللغة العربية الفصحى والدارجة التونسية التقنية (مثلاً استعمل كلمات: فورو، ديفيرونسيال، تيليريبتور). اجعل شرحك مفصلاً وسهلاً للصنايعية."
    },
    "🇫🇷 Français": {
        "title": "⚡ Plateforme Électricien Pro",
        "sidebar_title": "🛠️ Tableau de Bord",
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Système de Factures"],
        "ai_header": "🤖 Expert Électricien AI",
        "ai_info": "Posez vos questions techniques en Français",
        "ai_placeholder": "Ex: Comment brancher un va-et-vient ?",
        "btn_send": "Analyser 🚀",
        "calc_header": "🧮 Calcul de Section de Câble",
        "watt_label": "Puissance (Watt) :",
        "invoice_header": "📄 Créer un Devis Professionnel",
        "add_item": "Ajouter au devis",
        "search_label": "🔍 Chercher un article :",
        "total_label": "Total Général",
        "table_cols": ["Article", "Qté", "Prix U", "Total"],
        "prompt": "Tu es un expert électricien senior. Réponds en français technique précis, avec des conseils de sécurité et des normes (NF C 15-100)."
    },
    "🇺🇸 English": {
        "title": "⚡ Pro Electric Master",
        "sidebar_title": "🛠️ Control Panel",
        "menu": ["🤖 AI Consultation", "🧮 Cable Calculator", "📄 Invoice System"],
        "ai_header": "🤖 AI Electrical Expert",
        "ai_info": "Ask technical questions in English",
        "ai_placeholder": "Ex: How to calculate voltage drop?",
        "btn_send": "Ask Expert 🚀",
        "calc_header": "🧮 Cable Size Calculator",
        "watt_label": "Load Power (Watt):",
        "invoice_header": "📄 Generate Quote",
        "add_item": "Add to Quote",
        "search_label": "🔍 Search items:",
        "total_label": "Grand Total",
        "table_cols": ["Item", "Qty", "Price", "Total"],
        "prompt": "You are a professional electrical engineer. Provide technical answers in English, focusing on international standards and efficiency."
    }
}

# 4. اختيار اللغة
selected_lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", list(translations.keys()))
T = translations[selected_lang]

# 5. قاعدة البيانات التونسية
DB_MATERIELS = {
    "Foureau Orange 11mm": 28.500, "Foureau Orange 13mm": 32.800,
    "Foureau Orange 16mm": 38.000, "Foureau Orange 20mm": 48.500,
    "Hager: Disjoncteur 16A": 9.800, "Tunisie Câbles: 1.5mm": 65.000,
    "Legrand Valena: Prise": 11.200, "Hager: Diff 40A": 95.000
}

if 'invoice_data' not in st.session_state:
    st.session_state['invoice_data'] = []

# 6. بناء الواجهة حسب اللغة المختارة
st.sidebar.title(T["sidebar_title"])
choice = st.sidebar.radio("", T["menu"])

# --- القسم 1: استشارة الخبير (موديل 2.0 المستقر) ---
if choice == T["menu"][0]:
    st.header(T["ai_header"])
    st.info(T["ai_info"])
    query = st.text_area("", placeholder=T["ai_placeholder"], height=150)
    
    if st.button(T["btn_send"]):
        if query and API_KEY:
            with st.spinner("..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"{T['prompt']} : {query}"}]}]}
                try:
                    res = requests.post(url, json=payload, timeout=20)
                    if res.status_code == 200:
                        st.markdown("---")
                        st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
                    elif res.status_code == 429:
                        st.warning("⚠️ Quota Full! Please wait 30-60 seconds and retry.")
                except:
                    st.error("Connection Error.")

# --- القسم 2: حاسبة القياسات ---
elif choice == T["menu"][1]:
    st.header(T["calc_header"])
    watt = st.number_input(T["watt_label"], min_value=0, value=2000)
    amp = watt / 220
    st.metric("Current (A)", f"{amp:.2f} A")
    # منطق اختيار السلك
    wire = "1.5mm²" if amp <= 11 else "2.5mm²" if amp <= 17 else "4mm²+"
    st.info(f"Recommended: {wire}")

# --- القسم 3: نظام الفواتير ---
elif choice == T["menu"][2]:
    st.header(T["invoice_header"])
    search = st.text_input(T["search_label"])
    filtered = [k for k in DB_MATERIELS.keys() if search.lower() in k.lower()]
    
    col1, col2 = st.columns(2)
    with col1:
        prod = st.selectbox("Item:", filtered if filtered else list(DB_MATERIELS.keys()))
    with col2:
        qte = st.number_input("Qty:", min_value=1, value=1)
    
    if st.button(T["add_item"]):
        st.session_state['invoice_data'].append({
            T["table_cols"][0]: prod,
            T["table_cols"][1]: qte,
            T["table_cols"][2]: DB_MATERIELS[prod],
            T["table_cols"][3]: qte * DB_MATERIELS[prod]
        })
        st.rerun()

    if st.session_state['invoice_data']:
        df = pd.DataFrame(st.session_state['invoice_data'])
        st.table(df)
        total = df[T["table_cols"][3]].sum()
        st.markdown(f"### {T['total_label']}: :green[{total:.3f} DT]")
        if st.button("🗑️ Reset"):
            st.session_state['invoice_data'] = []
            st.rerun()
