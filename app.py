import streamlit as st
import pandas as pd
import requests

# 1. الإعدادات الأساسية
st.set_page_config(page_title="Pro Electric Platform", page_icon="⚡", layout="wide")
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 2. الكاتالوج
CATALOGUE = {
    "🛠️ T تأسيس (Gaines)": {"Foureau Orange 16mm": 38.000, "Foureau Noir 20mm": 52.000, "Boite Encastrement": 0.450},
    "🔌 C كابلات (Câbles)": {"Tunisie Câbles 1.5mm": 65.000, "Tunisie Câbles 2.5mm": 105.000},
    "📟 T طابلو (Hager)": {"Hager 16A": 9.800, "Diff 40A": 95.000, "Coffret 24M": 145.000}
}

# 3. نظام اللغات الاحترافي (تعريب وترجمة كل شيء)
translations = {
    "🇹🇳 العربية/تونسية": {
        "menu": ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 قائمة المواد", "📏 دليل الخراطيم والألوان"],
        "f_label": "قطر الفورو (مم):",
        "w_label": "نوع السلك:",
        "res_label": "⚠️ السعة القصوى المقترحة لسحب سهل:",
        "wires": "أسلاك",
        "color_title": "🎨 دليل ألوان الأسلاك",
        "note": "💡 ملاحظة: الالتزام بالألوان يسهل عملية الصيانة.",
        "p": "أنت خبير كهرباء تونسي محترف. أجب بالدارجة التقنية."
    },
    "🇫🇷 Français": {
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Catalogue", "📏 Guide Gaines & Couleurs"],
        "f_label": "Diamètre de gaine (mm):",
        "w_label": "Type de fil:",
        "res_label": "⚠️ Capacité max suggérée pour un tirage facile:",
        "wires": "fils",
        "color_title": "🎨 Code Couleurs des Fils",
        "note": "💡 Note: Le respect des couleurs facilite la maintenance.",
        "p": "Tu es un expert électricien. Réponds en français technique."
    },
    "🇺🇸 English": {
        "menu": ["🤖 AI Consultation", "🧮 Calculator", "📄 Catalogue", "📏 Conduit & Color Guide"],
        "f_label": "Conduit Diameter (mm):",
        "w_label": "Wire Type:",
        "res_label": "⚠️ Suggested max capacity for easy pulling:",
        "wires": "wires",
        "color_title": "🎨 Wire Color Codes",
        "note": "💡 Note: Color compliance simplifies maintenance.",
        "p": "You are a professional electrical engineer. Answer in English."
    }
}

selected_lang = st.sidebar.selectbox("🌐 Choose Language", list(translations.keys()))
T = translations[selected_lang]
if 'invoice' not in st.session_state: st.session_state['invoice'] = []
choice = st.sidebar.radio("🛠️", T["menu"])

# --- القسم 1 و 2 و 3 (مختصرة لضمان عمل الرابط) ---
if choice == T["menu"][0]:
    q = st.text_area(T["menu"][0]); 
    if st.button("OK"):
        res = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}", json={"contents": [{"parts": [{"text": f"{T['p']} : {q}"}]}]})
        if res.status_code == 200: st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])

elif choice == T["menu"][1]:
    w = st.number_input("Watt:", value=2000); st.metric("Ampère", f"{w/220:.2f} A")

elif choice == T["menu"][2]:
    st.header(T["menu"][2]); cat = st.selectbox("Cat", list(CATALOGUE.keys())); it = st.selectbox("Item", list(CATALOGUE[cat].keys()))
    if st.button("+"): st.session_state['invoice'].append({"Item": it, "Total": CATALOGUE[cat][it]})
    if st.session_state['invoice']: st.table(pd.DataFrame(st.session_state['invoice']))

# --- القسم 4: المصحح لغوياً بالكامل ---
elif choice == T["menu"][3]:
    st.header(T["menu"][3])
    col1, col2 = st.columns(2)
    
    with col1:
        g_size = st.selectbox(T["f_label"], [11, 13, 16, 20, 25])
        w_type = st.selectbox(T["w_label"], ["1.5 mm²", "2.5 mm²", "4 mm²", "6 mm²"])
        
        capacities = {
            11: {"1.5 mm²": 3, "2.5 mm²": 2}, 13: {"1.5 mm²": 4, "2.5 mm²": 3},
            16: {"1.5 mm²": 5, "2.5 mm²": 4, "4 mm²": 3},
            20: {"1.5 mm²": 7, "2.5 mm²": 6, "4 mm²": 5, "6 mm²": 4},
            25: {"1.5 mm²": 10, "2.5 mm²": 9, "4 mm²": 7, "6 mm²": 6}
        }
        max_w = capacities.get(g_size, {}).get(w_type, "?")
        st.warning(f"{T['res_label']} {max_w} {T['wires']}.")

    with col2:
        st.subheader(T["color_title"])
        if selected_lang == "🇫🇷 Français":
            st.code("🔵 Neutre --> Bleu\n🔴 Phase  --> Rouge/Noir\n🟡🟢 Terre --> Jaune/Vert")
        elif selected_lang == "🇺🇸 English":
            st.code("🔵 Neutral --> Blue\n🔴 Phase   --> Red/Black\n🟡🟢 Ground  --> Yellow/Green")
        else:
            st.code("🔵 محايد (Neutre) --> أزرق\n🔴 فاز (Phase) --> أحمر/أسود\n🟡🟢 أرضي (Terre) --> أصفر/أخضر")
        st.info(T["note"])
