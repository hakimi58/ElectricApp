import streamlit as st
import requests
from PIL import Image
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Master", page_icon="⚡", layout="wide")

# 2. نظام تغيير اللغة
if 'lang' not in st.session_state:
    st.session_state.lang = "العربية"

def toggle_lang():
    if st.session_state.lang == "العربية":
        st.session_state.lang = "Français"
    else:
        st.session_state.lang = "العربية"

# أزرار اللغة في أعلى الصفحة
col_l1, col_l2 = st.columns([0.9, 0.1])
with col_l2:
    st.button("🌐 FR/AR", on_click=toggle_lang)

L = st.session_state.lang

# 3. النصوص المترجمة
texts = {
    "العربية": {
        "title": "⚡ منصة الكهربائي المحترف",
        "sidebar": "🛠️ حقيبة الفني",
        "menu": ["🤖 خبير الأعطال (AI)", "📸 مصور الأعطال (Vision)", "🧮 حاسبة الكابلات", "📏 هبوط الجهد"],
        "query_label": "اشرح العطل أو اطلب نصيحة:",
        "analyze_btn": "تحليل المشكلة",
        "calc_btn": "احسب الآن",
        "watt_label": "قوة الجهاز (Watt):",
        "result_label": "✅ النتيجة التقديرية:",
        "vision_label": "📸 تحليل صور الأعطال",
        "upload_label": "اختر صورة العطل:",
        "ai_prompt": "أنت خبير كهرباء تونسي محترف. أجب باللهجة التونسية والفرنسية التقنية."
    },
    "Français": {
        "title": "⚡ Tunisia Electric Pro",
        "sidebar": "🛠️ Boîte à outils",
        "menu": ["🤖 Expert AI (Chat)", "📸 Diagnostic Vision", "🧮 Calcul de Câbles", "📏 Chute de Tension"],
        "query_label": "Décrivez la panne ou demandez conseil :",
        "analyze_btn": "Analyser le problème",
        "calc_btn": "Calculer maintenant",
        "watt_label": "Puissance de l'appareil (Watt) :",
        "result_label": "✅ Résultat estimé :",
        "vision_label": "📸 Analyse d'images",
        "upload_label": "Choisir une image de la panne :",
        "ai_prompt": "Tu es un expert électricien tunisien. Réponds en français technique avec quelques termes tunisiens."
    }
}

# 4. التطبيق الفعلي بناءً على اللغة المختارة
st.title(texts[L]["title"])

API_KEY = st.secrets.get("GOOGLE_API_KEY")

choice = st.sidebar.radio(texts[L]["sidebar"], texts[L]["menu"])

# --- القسم الأول: خبير الأعطال ---
if choice in [texts["العربية"]["menu"][0], texts["Français"]["menu"][0]]:
    st.header(texts[L]["menu"][0])
    query = st.text_area(texts[L]["query_label"], height=120)
    
    if st.button(texts[L]["analyze_btn"]):
        if query and API_KEY:
            with st.spinner("..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"{texts[L]['ai_prompt']} : {query}"}]}]}
                try:
                    response = requests.post(url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("✅ Solution :")
                    st.text_area("", value=answer, height=350)
                except:
                    st.error("Error/خطأ")

# --- القسم الثاني: مصور الأعطال ---
elif choice in [texts["العربية"]["menu"][1], texts["Français"]["menu"][1]]:
    st.header(texts[L]["vision_label"])
    uploaded_file = st.file_uploader(texts[L]["upload_label"], type=["jpg", "png", "jpeg"])
    
    if uploaded_file and st.button(texts[L]["analyze_btn"]):
        image = Image.open(uploaded_file)
        st.image(image, width=300)
        # هنا يتم استدعاء موديل الرؤية بنفس طريقة الكود السابق مع استخدام نصوص اللغة المختارة

# --- القسم الثالث: حاسبة الكابلات ---
elif choice in [texts["العربية"]["menu"][2], texts["Français"]["menu"][2]]:
    st.header(texts[L]["menu"][2])
    watt = st.number_input(texts[L]["watt_label"], min_value=0, value=2500)
    if st.button(texts[L]["calc_btn"]):
        amp = watt / 220
        # معايير تونسية
        if amp <= 11: res, wire = "10A", "1.5 mm²"
        elif amp <= 17: res, wire = "16A", "2.5 mm²"
        else: res, wire = "25A+", "4 mm²+"
        st.success(f"{texts[L]['result_label']} \n I = {amp:.1f}A | Breaker: {res} | Cable: {wire}")
