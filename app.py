import streamlit as st
import pandas as pd
import requests

# 1. الإعدادات الأساسية (مبدأ الأمان)
st.set_page_config(page_title="منصة الكهربائي المحترف الشاملة", page_icon="⚡", layout="wide")
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 2. الكاتالوج الشامل للمواد الكهربائية في تونس
CATALOGUE = {
    "🛠️ التأسيس (Gaines & Boites)": {
        "Foureau Orange 11mm (50m)": 28.500,
        "Foureau Orange 13mm (50m)": 32.800,
        "Foureau Orange 16mm (50m)": 38.000,
        "Foureau Orange 20mm (50m)": 48.500,
        "Foureau Noir (Béton) 16mm": 42.000,
        "Foureau Noir (Béton) 20mm": 52.000,
        "Boite Encastrement 1 Poste": 0.450,
        "Boite Encastrement 2 Postes": 0.950,
        "Boite Encastrement 3 Postes": 1.250,
        "Boite Dérivation Carrée 100x100": 2.800,
        "Boite Dérivation Ronde": 0.900
    },
    "🔌 الأسلاك والكابلات (Câbles)": {
        "Tunisie Câbles 1.5mm² (100m)": 65.000,
        "Tunisie Câbles 2.5mm² (100m)": 105.000,
        "Tunisie Câbles 4mm² (100m)": 165.000,
        "Tunisie Câbles 6mm² (100m)": 240.000,
        "Câble Racle 4x10mm (1m)": 14.500,
        "Câble Racle 4x16mm (1m)": 19.800,
        "Câble Souple 2x1.5mm (1m)": 2.200,
        "Câble Téléphone 2 Paires (1m)": 0.850
    },
    "📟 لوحة القواطع (Tableau Hager)": {
        "Hager 10A (Eclairage)": 10.500,
        "Hager 16A (Prise)": 9.800,
        "Hager 20A (Clim/Four)": 9.800,
        "Hager 25A / 32A": 14.500,
        "Différentiel Hager 40A 30mA": 95.000,
        "Différentiel Hager 63A 30mA": 128.000,
        "Disjoncteur Branchement (Sonalge)": 115.000,
        "Coffret Hager 12M": 75.000,
        "Coffret Hager 24M": 145.000,
        "Coffret Hager 36M": 195.000,
        "Peigne Phase/Neutre (Barrette)": 18.000
    },
    "🏠 المفاتيح (Appareillage Valena)": {
        "Prise 2P+T (مع أرضي)": 11.200,
        "Interrupteur Simple": 8.500,
        "Interrupteur Double": 10.800,
        "Va-et-Vient Simple": 10.200,
        "Bouton Poussoir": 11.500,
        "Prise TV / Satellite": 14.500,
        "Prise Téléphone RJ11": 12.800,
        "Plaque Valena 1 Poste": 1.800,
        "Plaque Valena 2 Postes": 3.500
    },
    "💡 الإضاءة (Luminaires)": {
        "Spot LED 7W Encastré": 6.800,
        "Spot LED 12W Encastré": 9.500,
        "Dalle LED 60x60 (Bureau)": 65.000,
        "Hublot LED 18W (Etanche)": 19.500,
        "Projecteur LED 50W": 45.000,
        "Ruban LED 5m + Transfo": 48.000
    },
    "⚙️ الحماية والإكسسوارات": {
        "Scotch d'Electricien (Chatterton)": 1.200,
        "Barrette de connexion (Dominos)": 2.500,
        "Embouts de câbles (Lot)": 8.000,
        "Gaine ICTA 16mm (Vrac)": 0.800
    }
}

# 3. نظام اللغات
translations = {
    "🇹🇳 العربية/تونسية": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 قائمة المواد الكاملة"],
        "ai_header": "🤖 خبير الكهرباء الذكي",
        "btn_send": "إرسال 🚀",
        "calc_header": "🧮 حاسبة مقاطع الأسلاك",
        "inv_header": "📄 تحرير فاتورة شاملة",
        "add_btn": "إضافة للفاتورة",
        "total": "المجموع الجملي",
        "prompt": "أنت خبير كهرباء تونسي محترف. أجب بالدارجة التونسية التقنية بمصطلحات الصنايعية."
    },
    "🇫🇷 Français": {
        "title": "⚡ Plateforme Électricien Pro",
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Catalogue Complet"],
        "ai_header": "🤖 Expert Électricien AI",
        "btn_send": "Envoyer 🚀",
        "calc_header": "🧮 Calculateur de Section",
        "inv_header": "📄 Devis Complet",
        "add_btn": "Ajouter",
        "total": "Total Général",
        "prompt": "Tu es un expert électricien. Réponds en français technique précis."
    },
    "🇺🇸 English": {
        "title": "⚡ Pro Electric Master",
        "menu": ["🤖 AI Consultation", "🧮 Calculator", "📄 Full Catalogue"],
        "ai_header": "🤖 AI Electrical Expert",
        "btn_send": "Send 🚀",
        "calc_header": "🧮 Cable Size Calculator",
        "inv_header": "📄 Full Quote",
        "add_btn": "Add",
        "total": "Grand Total",
        "prompt": "You are a professional electrical engineer. Provide clear technical advice."
    }
}

# 4. واجهة التطبيق
selected_lang = st.sidebar.selectbox("🌐 اللغة / Language", list(translations.keys()))
T = translations[selected_lang]

if 'invoice' not in st.session_state: st.session_state['invoice'] = []

choice = st.sidebar.radio("🛠️ الأدوات", T["menu"])

# --- الخبير ---
if choice == T["menu"][0]:
    st.header(T["ai_header"])
    query = st.text_area("اسأل الخبير:")
    if st.button(T["btn_send"]):
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"{T['prompt']} : {query}"}]}]}
            res = requests.post(url, json=payload)
            if res.status_code == 200:
                st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])

# --- الحاسبة ---
elif choice == T["menu"][1]:
    st.header(T["calc_header"])
    watt = st.number_input("Watt:", value=2000)
    amp = watt / 220
    st.metric("Ampère", f"{amp:.2f} A")
    wire = "1.5mm²" if amp <= 11 else "2.5mm²" if amp <= 17 else "4mm²+"
    st.info(f"النتيجة: {wire}")

# --- الفاتورة الشاملة ---
elif choice == T["menu"][2]:
    st.header(T["inv_header"])
    col1, col2 = st.columns(2)
    with col1:
        cat = st.selectbox("الفئة (Catégorie)", list(CATALOGUE.keys()))
        item = st.selectbox("المادة (Article)", list(CATALOGUE[cat].keys()))
    with col2:
        qte = st.number_input("الكمية (Qté)", min_value=1, value=1)
        price = CATALOGUE[cat][item]
        if st.button(T["add_btn"]):
            st.session_state['invoice'].append({"المادة": item, "الكمية": qte, "الثمن": price, "المجموع": qte * price})
            st.rerun()

    if st.session_state['invoice']:
        st.write("---")
        df = pd.DataFrame(st.session_state['invoice'])
        st.table(df)
        st.markdown(f"### {T['total']}: :green[{sum(i['المجموع'] for i in st.session_state['invoice']):.3f} DT]")
        if st.button("🗑️ Reset"):
            st.session_state['invoice'] = []; st.rerun()
