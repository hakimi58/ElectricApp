import streamlit as st
import requests
from PIL import Image
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="Pro Electric Master", page_icon="⚡", layout="wide")

# 2. نظام إدارة اللغات المتطور
if 'lang' not in st.session_state:
    st.session_state.lang = "تونس" # اللغة الافتراضية

def set_lang(lang_code):
    st.session_state.lang = lang_code

# أزرار اختيار اللغة في شريط جانبي أنيق
st.sidebar.markdown("### 🌐 اختر اللغة / Langue / Language")
col1, col2 = st.sidebar.columns(2)
with col1:
    if st.sidebar.button("🇹🇳 تونس"): set_lang("تونس")
    if st.sidebar.button("🇸🇦 الفصحى"): set_lang("الفصحى")
with col2:
    if st.sidebar.button("🇫🇷 Français"): set_lang("Français")
    if st.sidebar.button("🇺🇸 English"): set_lang("English")

L = st.session_state.lang

# 3. قاموس اللغات الشامل
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["🤖 خبير الأعطال", "📸 مصور الأعطال", "🧮 حاسبة الكابلات"],
        "query": "اشرح العطل التقني (بالدارجة):",
        "btn": "تحليل",
        "ai_prompt": "أنت خبير كهرباء تونسي، أجب باللهجة التونسية التقنية."
    },
    "الفصحى": {
        "title": "⚡ منصة خبير الكهرباء المحترف",
        "menu": ["🤖 خبير الأعطال", "📸 الفحص بالصور", "🧮 حاسبة الكابلات"],
        "query": "يرجى شرح العطل الفني بالتفصيل:",
        "btn": "بدء التحليل",
        "ai_prompt": "أنت مستشار هندسة كهربائية خبير، أجب باللغة العربية الفصحى وبصياغة فنية دقيقة."
    },
    "Français": {
        "title": "⚡ Tunisia Electric Pro",
        "menu": ["🤖 Expert AI", "📸 Diagnostic Vision", "🧮 Calcul de Câbles"],
        "query": "Décrivez la panne technique :",
        "btn": "Analyser",
        "ai_prompt": "Tu es un ingénieur électricien expert. Réponds en français technique."
    },
    "English": {
        "title": "⚡ Electric Master Pro",
        "menu": ["🤖 AI Expert", "📸 Vision Diagnosis", "🧮 Cable Calculator"],
        "query": "Describe the technical fault:",
        "btn": "Analyze",
        "ai_prompt": "You are a professional electrical engineer. Provide expert advice in English."
    }
}

# 4. واجهة التطبيق
st.title(texts[L]["title"])
st.caption(f"Language Mode: {L}")

API_KEY = st.secrets.get("GOOGLE_API_KEY")
choice = st.sidebar.radio("القائمة" if L in ["تونس", "الفصحى"] else "Menu", texts[L]["menu"])

# --- القسم الأول: خبير الأعطال (الذكاء الاصطناعي) ---
if choice == texts[L]["menu"][0]:
    st.header(texts[L]["menu"][0])
    query = st.text_area(texts[L]["query"], height=150)
    
    if st.button(texts[L]["btn"]):
        if query and API_KEY:
            with st.spinner("جاري المعالجة..." if L != "English" else "Processing..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"{texts[L]['ai_prompt']} : {query}"}]}]}
                try:
                    response = requests.post(url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("✅ النتيجة / Result:")
                    st.text_area("", value=answer, height=350)
                except:
                    st.error("خطأ في الاتصال بالسيرفر!")

# --- القسم الثاني: حاسبة الكابلات ---
elif choice == texts[L]["menu"][2]:
    st.header(texts[L]["menu"][2])
    watt = st.number_input("القدرة بالواط / Power (W):", value=2000, step=100)
    if st.button(texts[L]["btn"]):
        amp = watt / 220
        st.metric("Current (A)", f"{amp:.2f} A")
        if amp <= 11: wire = "1.5 mm²"
        elif amp <= 17: wire = "2.5 mm²"
        else: wire = "4 mm² +"
        st.success(f"Recommended Wire: {wire}")
