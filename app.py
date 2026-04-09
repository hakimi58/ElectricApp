import streamlit as st
import pandas as pd
import requests
import json

# 1. إعدادات الصفحة (المبدأ الأساسي)
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. جلب المفتاح (السر في ثبات التطبيق)
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة بيانات المواد (التركيز على الكهرباء فقط)
CATALOGUE = {
    "الخراطيم (Foureau)": {
        "Foureau Orange 11mm (50m)": 28.500,
        "Foureau Orange 13mm (50m)": 32.800,
        "Foureau Orange 16mm (50m)": 38.000,
        "Foureau Orange 20mm (50m)": 48.500,
        "Foureau Noir (Béton) 16mm": 42.000,
        "Foureau Noir (Béton) 20mm": 52.000
    },
    "الأسلاك والكابلات (Câbles)": {
        "Tunisie Câbles 1.5mm² (100m)": 65.000,
        "Tunisie Câbles 2.5mm² (100m)": 105.000,
        "Tunisie Câbles 4mm² (100m)": 165.000,
        "Tunisie Câbles 6mm² (100m)": 240.000,
        "Câble Racle 4x10mm (1m)": 14.500
    },
    "قواطع هاجر (Hager)": {
        "Hager 10A (Eclairage)": 10.500,
        "Hager 16A (Prise)": 9.800,
        "Hager 20A (Cuisine/Clim)": 9.800,
        "Différentiel Hager 40A 30mA": 95.000,
        "Coffret Hager 12M": 75.000,
        "Coffret Hager 24M": 145.000
    },
    "المفاتيح والبرايز (Appareillage)": {
        "Legrand Valena: Prise 2P+T": 11.200,
        "Legrand Valena: Interrupteur": 8.500,
        "Legrand Valena: Va-et-Vient": 10.200,
        "Boite Encastrement 1 Poste": 0.450,
        "Boite Encastrement 3 Postes": 1.200
    }
}

# 4. نظام اللغات والواجهة (تغيير كامل حسب اللغة)
translations = {
    "🇹🇳 العربية/تونسية": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 قائمة المواد"],
        "ai_header": "🤖 خبير الكهرباء الذكي",
        "ai_placeholder": "اسأل بالدارجة التونسية التقنية...",
        "btn_send": "إرسال 🚀",
        "calc_header": "🧮 حاسبة مقاطع الأسلاك",
        "inv_header": "📄 كشف المواد (Devis)",
        "add_btn": "إضافة",
        "total": "المجموع الجملي",
        "prompt": "أنت خبير كهرباء تونسي محترف. أجب بالدارجة التونسية التقنية بمصطلحات الصنايعية."
    },
    "🇫🇷 Français": {
        "title": "⚡ Plateforme Électricien Pro",
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Catalogue Matériels"],
        "ai_header": "🤖 Expert Électricien AI",
        "ai_placeholder": "Posez votre question en français...",
        "btn_send": "Envoyer 🚀",
        "calc_header": "🧮 Calculateur de Section",
        "inv_header": "📄 Devis Matériels",
        "add_btn": "Ajouter",
        "total": "Total Général",
        "prompt": "Tu es un expert électricien. Réponds en français technique précis."
    },
    "🇺🇸 English": {
        "title": "⚡ Pro Electric Master",
        "menu": ["🤖 AI Consultation", "🧮 Calculator", "📄 Material List"],
        "ai_header": "🤖 AI Electrical Expert",
        "ai_placeholder": "Ask your technical question...",
        "btn_send": "Send 🚀",
        "calc_header": "🧮 Cable Size Calculator",
        "inv_header": "📄 Material Quote",
        "add_btn": "Add",
        "total": "Grand Total",
        "prompt": "You are a professional electrical engineer. Provide clear technical advice in English."
    }
}

# 5. اختيار اللغة
selected_lang = st.sidebar.selectbox("🌐 اللغة / Language", list(translations.keys()))
T = translations[selected_lang]

# 6. ذاكرة الفاتورة
if 'invoice' not in st.session_state: st.session_state['invoice'] = []

# 7. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", T["menu"])

# --- القسم 1: الخبير (بالموديل المستقر) ---
if choice == T["menu"][0]:
    st.header(T["ai_header"])
    query = st.text_area("", placeholder=T["ai_placeholder"], height=120)
    if st.button(T["btn_send"]):
        if query and API_KEY:
            with st.spinner("..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"{T['prompt']} : {query}"}]}]}
                res = requests.post(url, json=payload)
                if res.status_code == 200:
                    st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
                elif res.status_code == 429:
                    st.warning("الرجاء الانتظار 30 ثانية (Quota).")

# --- القسم 2: الحاسبة ---
elif choice == T["menu"][1]:
    st.header(T["calc_header"])
    watt = st.number_input("Watt:", value=2000)
    amp = watt / 220
    st.metric("Ampère", f"{amp:.2f} A")
    wire = "1.5mm²" if amp <= 11 else "2.5mm²" if amp <= 17 else "4mm²+"
    st.info(f"النتيجة: {wire}")

# --- القسم 3: الفاتورة العملية ---
elif choice == T["menu"][2]:
    st.header(T["inv_header"])
    col1, col2 = st.columns(2)
    with col1:
        cat = st.selectbox("الفئة / Catégorie", list(CATALOGUE.keys()))
        item = st.selectbox("المادة / Article", list(CATALOGUE[cat].keys()))
    with col2:
        qte = st.number_input("الكمية / Qté", min_value=1, value=1)
        price = CATALOGUE[cat][item]
        if st.button(T["add_btn"]):
            st.session_state['invoice'].append({"المادة": item, "الكمية": qte, "المجموع": qte * price})
            st.rerun()

    if st.session_state['invoice']:
        st.table(pd.DataFrame(st.session_state['invoice']))
        st.markdown(f"### {T['total']}: :green[{sum(i['المجموع'] for i in st.session_state['invoice']):.3f} DT]")
        if st.button("🗑️ Reset"):
            st.session_state['invoice'] = []; st.rerun()
