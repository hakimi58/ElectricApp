import streamlit as st
import requests

# 1. إعدادات الصفحة (نفس الواجهة الأصلية)
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="wide")

# 2. نظام اختيار اللغة بـ "قائمة منسدلة واحدة" في الأعلى لتوفير المساحة
lang_options = {
    "🇹🇳 تونسية": "تونس",
    "🇸🇦 فصحى": "الفصحى",
    "🇫🇷 Français": "Français",
    "🇺🇸 English": "English"
}

# وضع اختيار اللغة في الجانب بشكل أنيق ومختصر
L_key = st.sidebar.selectbox("🌐 اختر اللغة / Langue", list(lang_options.keys()))
L = lang_options[L_key]

# 3. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 4. قاموس النصوص لكل اللغات (للحفاظ على استقرار الواجهة)
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "sidebar_title": "🛠️ قائمة الأدوات",
        "menu": ["استشارة الخبير (AI)", "حاسبة الأسلاك والقواطع"],
        "query_label": "اشرح المشكلة هنا (بالدارجة):",
        "btn_label": "الحصول على الحل",
        "watt_label": "قوة الجهاز الكلية (Watt):",
        "calc_btn": "احسب القياسات",
        "prompt": "أنت خبير كهرباء تونسي، أجب بالدارجة التونسية التقنية وبشكل نقاط."
    },
    "الفصحى": {
        "title": "⚡ منصة خبير الكهرباء العربي",
        "sidebar_title": "🛠️ قائمة الأدوات",
        "menu": ["استشارة الخبير (AI)", "حاسبة الأسلاك والقواطع"],
        "query_label": "يرجى وصف المشكلة الفنية:",
        "btn_label": "الحصول على الحل",
        "watt_label": "القدرة الإجمالية (واط):",
        "calc_btn": "احسب القياسات",
        "prompt": "أنت مستشار هندسة كهربائية، أجب باللغة العربية الفصحى وبدقة تقنية."
    },
    "Français": {
        "title": "⚡ Tunisia Electric Pro",
        "sidebar_title": "🛠️ Menu des Outils",
        "menu": ["Consultation AI", "Calculateur Câbles"],
        "query_label": "Décrivez le problème ici :",
        "btn_label": "Obtenir la solution",
        "watt_label": "Puissance Totale (Watt) :",
        "calc_btn": "Calculer",
        "prompt": "Tu es un expert électricien. Réponds en français technique."
    },
    "English": {
        "title": "⚡ Electric Master Pro",
        "sidebar_title": "🛠️ Toolbox",
        "menu": ["AI Consultation", "Cable Calculator"],
        "query_label": "Describe the fault here:",
        "btn_label": "Get Solution",
        "watt_label": "Total Power (Watt):",
        "calc_btn": "Calculate",
        "prompt": "You are a professional electrical expert. Provide advice in English."
    }
}

# 5. عرض العنوان بناءً على اللغة
st.title(texts[L]["title"])

# 6. القائمة الجانبية (نفس التصميم الذي أعجبك)
st.sidebar.markdown("---")
choice = st.sidebar.radio(texts[L]["sidebar_title"], texts[L]["menu"])

# --- القسم الأول: خبير الذكاء الاصطناعي ---
if choice == texts[L]["menu"][0]:
    st.header(texts[L]["menu"][0])
    query = st.text_area(texts[L]["query_label"], height=150)
    
    if st.button(texts[L]["btn_label"]):
        if query and API_KEY:
            with st.spinner("..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"{texts[L]['prompt']} : {query}"}]}]}
                try:
                    response = requests.post(url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("✅ النتيجة / Result:")
                    st.text_area("", value=answer, height=300)
                except:
                    st.error("خطأ في الاتصال.")

# --- القسم الثاني: حاسبة الأحمال ---
elif choice == texts[L]["menu"][1]:
    st.header(texts[L]["menu"][1])
    watt = st.number_input(texts[L]["watt_label"], min_value=0, value=2000)
    
    if st.button(texts[L]["calc_btn"]):
        amp = watt / 220
        st.info(f"التيار المسحوب: {amp:.2f} A")
        
        if amp <= 11: res, wire = "10A", "1.5 مم²"
        elif amp <= 17: res, wire = "16A", "2.5 مم²"
        else: res, wire = "25A+", "4 مم²+"
        
        st.success(f"النتيجة: {wire} + {res}")
        
