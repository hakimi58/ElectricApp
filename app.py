import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Pro Electric Master", page_icon="⚡", layout="wide")

# 2. نظام اللغة بـ "قائمة واحدة" توفر المساحة
# نضع اختيار اللغة في شريط الجانب لكن بشكل مدمج جداً
lang_options = {
    "🇹🇳 تونسية": "تونس",
    "🇸🇦 فصحى": "الفصحى",
    "🇫🇷 Français": "Français",
    "🇺🇸 English": "English"
}

# اختيار اللغة بلمسة واحدة
selected_lang_name = st.sidebar.selectbox("🌐 اختر اللغة / Langue", list(lang_options.keys()))
L = lang_options[selected_lang_name]

# 3. قاموس اللغات (نفس البيانات السابقة لكن منظمة)
texts = {
    "تونس": {
        "title": "⚡ خبير الكهرباء التونسي",
        "menu": ["🤖 خبير الأعطال", "📸 مصور الأعطال", "🧮 حاسبة الكابلات"],
        "query": "شنوة المشكل التقني اللي عندك؟",
        "btn": "تحليل العطل",
        "prompt": "أنت خبير كهرباء تونسي، أجب بالدارجة التونسية التقنية."
    },
    "الفصحى": {
        "title": "⚡ منصة خبير الكهرباء العالمي",
        "menu": ["🤖 خبير الأعطال", "📸 الفحص بالصور", "🧮 حاسبة الكابلات"],
        "query": "يرجى وصف العطل الفني بالتفصيل:",
        "btn": "بدء التشخيص",
        "prompt": "أنت مستشار هندسة كهربائية، أجب باللغة العربية الفصحى."
    },
    "Français": {
        "title": "⚡ Tunisia Electric Pro",
        "menu": ["🤖 Expert AI", "📸 Diagnostic Vision", "🧮 Calcul de Câbles"],
        "query": "Décrivez la panne technique :",
        "btn": "Analyser",
        "prompt": "Tu es un ingénieur électricien expert. Réponds en français technique."
    },
    "English": {
        "title": "⚡ Electric Master Pro",
        "menu": ["🤖 AI Expert", "📸 Vision Diagnosis", "🧮 Cable Calculator"],
        "query": "Describe the technical fault:",
        "btn": "Analyze",
        "prompt": "You are a professional electrical engineer. Provide expert advice in English."
    }
}

# 4. تنسيق الواجهة الرئيسية
st.title(texts[L]["title"])
st.markdown("---")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

# اختيار الأداة من القائمة الجانبية (بشكل نظيف)
choice = st.sidebar.radio("🛠️ الأدوات" if L in ["تونس", "الفصحى"] else "🛠️ Tools", texts[L]["menu"])

# --- تنفيذ الأداة المختارة ---
if choice == texts[L]["menu"][0]:
    st.header(texts[L]["menu"][0])
    query = st.text_area(texts[L]["query"], height=150)
    
    if st.button(texts[L]["btn"]):
        if query and API_KEY:
            with st.spinner("جاري العمل..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"{texts[L]['prompt']} : {query}"}]}]}
                try:
                    response = requests.post(url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("✅ النتيجة:")
                    # استخدام صندوق نصي أسود لضمان الرؤية
                    st.text_area("", value=answer, height=350)
                except:
                    st.error("خطأ في الاتصال.")

elif choice == texts[L]["menu"][2]:
    st.header(texts[L]["menu"][2])
    watt = st.number_input("القدرة (W):", value=2000)
    if st.button(texts[L]["btn"]):
        amp = watt / 220
        st.metric("Ampere", f"{amp:.2f} A")
        # قانون تقريبي (نفس الذي نخدم به في تونس)
        wire = "1.5 mm²" if amp <= 11 else "2.5 mm²" if amp <= 17 else "4 mm² +"
        st.success(f"Cable: {wire}")
