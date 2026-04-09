import streamlit as st
import requests
from PIL import Image
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Master", page_icon="⚡", layout="wide")

# 2. نظام إدارة اللغات (AR, FR, EN)
if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"

def set_lang(lang_name):
    st.session_state.lang = lang_name

# أزرار اختيار اللغة في أعلى الصفحة
col_l1, col_l2, col_l3 = st.columns([0.8, 0.1, 0.1])
with col_l2:
    if st.button("🌐 FR/EN"):
        set_lang("Français" if st.session_state.lang != "Français" else "English")
with col_l3:
    if st.button("🇹🇳 AR"):
        set_lang("العربية")

L = st.session_state.lang

# 3. قاموس اللغات
texts = {
    "العربية": {
        "title": "⚡ منصة الكهربائي المحترف",
        "sidebar": "🛠️ حقيبة الفني",
        "menu": ["🤖 خبير الأعطال", "📸 مصور الأعطال", "🧮 حاسبة الكابلات"],
        "query_label": "اشرح العطل التقني:",
        "analyze_btn": "تحليل",
        "watt_label": "القوة (Watt):",
        "result_label": "✅ النتيجة:",
        "ai_prompt": "أنت خبير كهرباء تونسي، أجب باللهجة التونسية والفرنسية والإنجليزية التقنية حسب الحاجة."
    },
    "Français": {
        "title": "⚡ Tunisia Electric Pro",
        "sidebar": "🛠️ Boîte à outils",
        "menu": ["🤖 Expert AI", "📸 Diagnostic Vision", "🧮 Calcul de Câbles"],
        "query_label": "Décrivez la panne :",
        "analyze_btn": "Analyser",
        "watt_label": "Puissance (Watt) :",
        "result_label": "✅ Résultat :",
        "ai_prompt": "Tu es un expert électricien. Réponds en français technique."
    },
    "English": {
        "title": "⚡ Electric Master Pro",
        "sidebar": "🛠️ Technician Toolbox",
        "menu": ["🤖 AI Expert", "📸 Vision Diagnosis", "🧮 Cable Calculator"],
        "query_label": "Describe the fault:",
        "analyze_btn": "Analyze",
        "watt_label": "Power (Watt):",
        "result_label": "✅ Result:",
        "ai_prompt": "You are a professional electrical expert. Provide technical advice in English."
    }
}

# 4. واجهة التطبيق
st.title(texts[L]["title"])
st.write(f"**Language:** {L}")

API_KEY = st.secrets.get("GOOGLE_API_KEY")
choice = st.sidebar.radio(texts[L]["sidebar"], texts[L]["menu"])

# --- القسم الأول: خبير الأعطال ---
if choice in [texts[lang]["menu"][0] for lang in texts]:
    st.header(texts[L]["menu"][0])
    query = st.text_area(texts[L]["query_label"], height=100)
    
    if st.button(texts[L]["analyze_btn"]):
        if query and API_KEY:
            with st.spinner("Processing..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"{texts[L]['ai_prompt']} : {query}"}]}]}
                try:
                    response = requests.post(url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.text_area("Response:", value=answer, height=300)
                except:
                    st.error("Connection Error!")

# --- القسم الثاني: حاسبة الكابلات (مثال) ---
elif choice in [texts[lang]["menu"][2] for lang in texts]:
    st.header(texts[L]["menu"][2])
    watt = st.number_input(texts[L]["watt_label"], value=2000)
    if st.button(texts[L]["analyze_btn"]):
        amp = watt / 220
        st.success(f"{texts[L]['result_label']} {amp:.2f} A")
