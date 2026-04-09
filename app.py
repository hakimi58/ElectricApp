import streamlit as st
import pandas as pd
import requests

# 1. الإعدادات الأساسية
st.set_page_config(page_title="منصة الكهربائي المحترف 2026", page_icon="⚡", layout="wide")
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 2. الكاتالوج الشامل
CATALOGUE = {
    "🛠️ التأسيس (Gaines & Boites)": {
        "Foureau Orange 11mm (50m)": 28.500, "Foureau Orange 13mm (50m)": 32.800,
        "Foureau Orange 16mm (50m)": 38.000, "Foureau Orange 20mm (50m)": 48.500,
        "Foureau Noir (Béton) 16mm": 42.000, "Foureau Noir (Béton) 20mm": 52.000,
        "Boite Encastrement 1 Poste": 0.450, "Boite Encastrement 3 Postes": 1.250
    },
    "🔌 الأسلاك والكابلات (Câbles)": {
        "Tunisie Câbles 1.5mm² (100m)": 65.000, "Tunisie Câbles 2.5mm² (100m)": 105.000,
        "Tunisie Câbles 4mm² (100m)": 165.000, "Tunisie Câbles 6mm² (100m)": 240.000,
        "Câble Racle 4x10mm (1m)": 14.500, "Câble Souple 2x1.5mm (1m)": 2.200
    },
    "📟 لوحة القواطع (Hager)": {
        "Hager 10A (Eclairage)": 10.500, "Hager 16A (Prise)": 9.800,
        "Hager 20A (Clim/Four)": 9.800, "Différentiel Hager 40A 30mA": 95.000,
        "Coffret Hager 12M": 75.000, "Coffret Hager 24M": 145.000
    },
    "🏠 المفاتيح (Appareillage)": {
        "Prise 2P+T Valena": 11.200, "Interrupteur Simple": 8.500,
        "Va-et-Vient Simple": 10.200, "Plaque Valena 1 Poste": 1.800
    }
}

# 3. نظام اللغات
translations = {
    "🇹🇳 العربية/تونسية": {
        "menu": ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 قائمة المواد", "📏 دليل الخراطيم والألوان"],
        "prompt": "أنت خبير كهرباء تونسي محترف. أجب بالدارجة التقنية.",
        "calc_foureau": "📐 حاسبة سعة الفورو",
        "color_code": "🎨 دليل ألوان الأسلاك"
    },
    "🇫🇷 Français": {
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Catalogue", "📏 Guide Gaines & Couleurs"],
        "prompt": "Tu es un expert électricien. Réponds en français technique.",
        "calc_foureau": "📐 Capacité des Gaines",
        "color_code": "🎨 Code Couleurs"
    },
    "🇺🇸 English": {
        "menu": ["🤖 AI Consultation", "🧮 Calculator", "📄 Catalogue", "📏 Conduit & Color Guide"],
        "prompt": "You are a professional electrical engineer. Answer in technical English.",
        "calc_foureau": "📐 Conduit Capacity",
        "color_code": "🎨 Wire Color Codes"
    }
}

# اختيار اللغة
selected_lang = st.sidebar.selectbox("🌐 اللغة / Language", list(translations.keys()))
T = translations[selected_lang]
if 'invoice' not in st.session_state: st.session_state['invoice'] = []

choice = st.sidebar.radio("🛠️ الأدوات", T["menu"])

# --- 1. الخبير ---
if choice == T["menu"][0]:
    st.header(T["menu"][0])
    query = st.text_area("اسأل خبيرك:")
    if st.button("إرسال"):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
        payload = {"contents": [{"parts": [{"text": f"{T['prompt']} : {query}"}]}]}
        res = requests.post(url, json=payload)
        if res.status_code == 200: st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])

# --- 2. الحاسبة ---
elif choice == T["menu"][1]:
    st.header(T["menu"][1])
    watt = st.number_input("Watt:", value=2000)
    amp = watt / 220
    st.metric("Ampère", f"{amp:.2f} A")
    wire = "1.5mm²" if amp <= 11 else "2.5mm²" if amp <= 17 else "4mm²+"
    st.info(f"النتيجة: {wire}")

# --- 3. الفاتورة ---
elif choice == T["menu"][2]:
    st.header(T["menu"][2])
    cat = st.selectbox("الفئة", list(CATALOGUE.keys())); item = st.selectbox("المادة", list(CATALOGUE[cat].keys()))
    qte = st.number_input("الكمية", min_value=1, value=1)
    if st.button("إضافة"):
        st.session_state['invoice'].append({"المادة": item, "الكمية": qte, "الثمن": CATALOGUE[cat][item], "المجموع": qte * CATALOGUE[cat][item]})
    if st.session_state['invoice']:
        st.table(pd.DataFrame(st.session_state['invoice']))
        st.success(f"المجموع: {sum(i['المجموع'] for i in st.session_state['invoice']):.3f} DT")

# --- 4. الأداة الجديدة: دليل الخراطيم والألوان ---
elif choice == T["menu"][3]:
    st.header(T["calc_foureau"])
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(T["calc_foureau"])
        gaine_size = st.selectbox("قطر الفورو (mm):", [11, 13, 16, 20, 25])
        wire_type = st.selectbox("نوع السلك:", ["1.5 mm²", "2.5 mm²", "4 mm²", "6 mm²"])
        
        # قاعدة تقريبية للسعة (قاعدة 1/3 لسهولة السحب)
        capacities = {
            11: {"1.5 mm²": 3, "2.5 mm²": 2},
            13: {"1.5 mm²": 4, "2.5 mm²": 3},
            16: {"1.5 mm²": 5, "2.5 mm²": 4, "4 mm²": 3},
            20: {"1.5 mm²": 7, "2.5 mm²": 6, "4 mm²": 5, "6 mm²": 4},
            25: {"1.5 mm²": 10, "2.5 mm²": 9, "4 mm²": 7, "6 mm²": 6}
        }
        max_wires = capacities.get(gaine_size, {}).get(wire_type, "غير محدد")
        st.warning(f"⚠️ السعة القصوى المقترحة لسحب سهل: {max_wires} أسلاك.")

    with col2:
        st.subheader(T["color_code"])
        st.code("""
        🔵 Neutre (محايد)  --> Bleu
        🔴 Phase (فاز)     --> Rouge / Noir / Marron
        🟡🟢 Terre (أرضي)  --> Jaune & Vert
        🟣 Navettes       --> Violet / Orange
        """)
        st.info("💡 ملاحظة: الالتزام بالألوان يسهل عملية الصيانة ويحمي من الأخطار.")
