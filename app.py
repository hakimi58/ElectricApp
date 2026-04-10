import streamlit as st
import pandas as pd
import requests

# 1. الإعدادات الأساسية
st.set_page_config(page_title="Pro Electric Platform", page_icon="⚡", layout="wide")

# استدعاء مفتاح API من الإعدادات السرية
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 2. الكاتالوج (قاعدة البيانات المصغرة)
CATALOGUE = {
    "🛠️ T تأسيس (Gaines)": {"Foureau Orange 16mm": 38.000, "Foureau Noir 20mm": 52.000, "Boite Encastrement": 0.450},
    "🔌 C كابلات (Câbles)": {"Tunisie Câbles 1.5mm": 65.000, "Tunisie Câbles 2.5mm": 105.000},
    "📟 T طابلو (Hager)": {"Hager 16A": 9.800, "Diff 40A": 95.000, "Coffret 24M": 145.000}
}

# 3. نظام اللغات
translations = {
    "🇹🇳 العربية/تونسية": {
        "menu": ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 قائمة المواد", "📏 دليل الخراطيم والألوان"],
        "f_label": "قطر الفورو (مم):",
        "w_label": "نوع السلك:",
        "res_label": "⚠️ السعة القصوى المقترحة لسحب سهل:",
        "wires": "أسلاك",
        "color_title": "🎨 دليل ألوان الأسلاك",
        "note": "💡 ملاحظة: الالتزام بالألوان يسهل عملية الصيانة.",
        "p": "أنت خبير كهرباء تونسي محترف. أجب بالدارجة التقنية وبوضوح.",
        "total": "الإجمالي الإجمالي:"
    },
    "🇫🇷 Français": {
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Catalogue", "📏 Guide Gaines & Couleurs"],
        "f_label": "Diamètre de gaine (mm):",
        "w_label": "Type de fil:",
        "res_label": "⚠️ Capacité max suggérée pour un tirage facile:",
        "wires": "fils",
        "color_title": "🎨 Code Couleurs des Fils",
        "note": "💡 Note: Le respect des couleurs facilite la maintenance.",
        "p": "Tu es un expert électricien. Réponds en français technique.",
        "total": "Total Global:"
    },
    "🇺🇸 English": {
        "menu": ["🤖 AI Consultation", "🧮 Calculator", "📄 Catalogue", "📏 Conduit & Color Guide"],
        "f_label": "Conduit Diameter (mm):",
        "w_label": "Wire Type:",
        "res_label": "⚠️ Suggested max capacity for easy pulling:",
        "wires": "wires",
        "color_title": "🎨 Wire Color Codes",
        "note": "💡 Note: Color compliance simplifies maintenance.",
        "p": "You are a professional electrical engineer. Answer in English.",
        "total": "Grand Total:"
    }
}

selected_lang = st.sidebar.selectbox("🌐 Choose Language", list(translations.keys()))
T = translations[selected_lang]

# إدارة حالة سلة المشتريات
if 'invoice' not in st.session_state: 
    st.session_state['invoice'] = []

choice = st.sidebar.radio("القائمة", T["menu"])

# --- القسم 1: استشارة الخبير (Gemini API) ---
if choice == T["menu"][0]:
    st.header(T["menu"][0])
    q = st.text_area("اسأل الخبير الكهربائي (AI):") 
    if st.button("إرسال السؤال"):
        if not API_KEY:
            st.error("API Key missing!")
        else:
            res = requests.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}", 
                json={"contents": [{"parts": [{"text": f"{T['p']} : {q}"}]}]}
            )
            if res.status_code == 200: 
                st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])

# --- القسم 2: حاسبة القدرة ---
elif choice == T["menu"][1]:
    st.header(T["menu"][1])
    w = st.number_input("Watt (الواط):", value=2000)
    st.metric("Ampère (الأمبير)", f"{w/220:.2f} A")

# --- القسم 3: قائمة المواد (الفاتورة) ---
elif choice == T["menu"][2]:
    st.header(T["menu"][2])
    cat = st.selectbox("الفئة (Catégorie)", list(CATALOGUE.keys()))
    it = st.selectbox("المنتج (Article)", list(CATALOGUE[cat].keys()))
    
    if st.button("إضافة إلى القائمة"):
        st.session_state['invoice'].append({"Item": it, "Price": CATALOGUE[cat][it]})
        st.toast(f"تمت إضافة {it}")

    if st.session_state['invoice']:
        df = pd.DataFrame(st.session_state['invoice'])
        st.table(df)
        total_price = df["Price"].sum()
        st.subheader(f"{T['total']} {total_price:.3f} TND")
        if st.button("مسح القائمة"):
            st.session_state['invoice'] = []
            st.rerun()

# --- القسم 4: دليل الخراطيم والألوان ---
elif choice == T["menu"][3]:
    st.header(T["menu"][3])
    col1, col2 = st.columns(2)
    
    with col1:
        g_size = st.selectbox(T["f_label"], [11, 13, 16, 20, 25])
        w_type = st.selectbox(T["w_label"], ["1.5 mm²", "2.5 mm²", "4 mm²", "6 mm²"])
        
        capacities = {
            11: {"1.5 mm²": 3, "2.5 mm²": 2}, 
            13: {"1.5 mm²": 4, "2.5 mm²": 3},
            16: {"1.5 mm²": 5, "2.5 mm²": 4, "4 mm²": 3},
            20: {"1.5 mm²": 7, "2.5 mm²": 6, "4 mm²": 5, "6 mm²": 4},
            25: {"1.5 mm²": 10, "2.5 mm²": 9, "4 mm²": 7, "6 mm²": 6}
        }
        max_w = capacities.get(g_size, {}).get(w_type, "N/A")
        st.warning(f"{T['res_label']} {max_w} {T['wires']}.")

    with col2:
        st.subheader(T["color_title"])
        if selected_lang == "🇫🇷 Français":
            st.code("🔵 Neutre --> Bleu\n🔴 Phase  --> Rouge/Noir\n🟡🟢 Terre --> Jaune/Vert")
        elif selected_lang == "🇺🇸 English":
            st.code("🔵 Neutral --> Blue\n🔴 Phase   --> Red/Black\n🟡🟢 Ground  --> Yellow/Green")
        else:
            # إكمال الجزء العربي الذي كان ناقصاً
            st.code("🔵 محايد (Neutre) --> أزرق\n🔴 فاز (Phase) --> أحمر/أسود\n🟡🟢 أرضي (Terre) --> أصفر مخضر")
        st.info(T["note"])
