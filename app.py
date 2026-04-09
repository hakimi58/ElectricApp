import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Pro Electric Master", page_icon="⚡", layout="wide")

# 2. نظام اللغة (المدمج)
lang_options = {
    "🇹🇳 تونسية": "تونس",
    "🇸🇦 فصحى": "الفصحى",
    "🇫🇷 Français": "Français",
    "🇺🇸 English": "English"
}
selected_lang_name = st.sidebar.selectbox("🌐 اللغة / Langue", list(lang_options.keys()))
L = lang_options[selected_lang_name]

# 3. القاموس (إضافة ميزة التقرير)
texts = {
    "تونس": {
        "menu": ["🤖 خبير الأعطال", "📝 تقرير معاينة", "🛡️ دليل الحماية IP", "🧮 حاسبة الكابلات"],
        "rep_header": "📝 إنشاء تقرير عطل لحريف",
        "rep_btn": "توليد نص التقرير"
    },
    "الفصحى": {
        "menu": ["🤖 خبير الأعطال", "📝 تقرير معاينة", "🛡️ دليل الحماية IP", "🧮 حاسبة الكابلات"],
        "rep_header": "📝 إنشاء تقرير فني رسمي",
        "rep_btn": "إنشاء التقرير"
    }
    # (الفرنسية والإنجليزية يتبعون نفس النمط)
}

choice = st.sidebar.radio("القائمة", texts[L]["menu"])

# --- ميزة تقرير المعاينة (الجديدة) ---
if "تقرير" in choice or "Rapport" in choice:
    st.header(texts[L]["rep_header"])
    client = st.text_input("اسم الحريف:")
    problem_desc = st.text_area("وصف العطل:")
    parts_needed = st.text_area("القطع اللازم شراؤها:")
    
    if st.button(texts[L]["rep_btn"]):
        report = f"""
        *تقرير فني كهرباء*
        -----------------
        الحريف: {client}
        التشخيص: {problem_desc}
        المواد المطلوبة: {parts_needed}
        -----------------
        نصيحة: يرجى عدم ترك الأسلاك مكشوفة.
        """
        st.code(report) # يظهر بشكل سهل للنسخ
        st.info("انسخ النص وابعثو في WhatsApp للحريف")

# --- ميزة دليل الحماية IP (الجديدة) ---
elif "IP" in choice:
    st.header("🛡️ دليل رموز الحماية العالمية (IP Rating)")
    ip_code = st.selectbox("اختر الرمز:", ["IP20", "IP44", "IP65", "IP67", "IP68"])
    
    ip_data = {
        "IP20": "للاستعمال الداخلي فقط (داخل الدار)، لا يحمي من الماء.",
        "IP44": "محمي من رذاذ الماء (يصلح للحمام أو تحت سقف لبرة).",
        "IP65": "محمي من خراطيم الماء (يصلح للشارع والمطر).",
        "IP67": "يتحمل الغطس المؤقت في الماء.",
        "IP68": "مقاوم للماء تماماً (للمسابح والآبار)."
    }
    st.success(ip_data[ip_code])

# --- باقي الأقسام (الذكاء الاصطناعي والحاسبة) تبقى كما هي ---
