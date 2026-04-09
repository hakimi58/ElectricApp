import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة (النسخة 8 الأصلية)
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. نظام اختيار اللغة (تونسية، فرنسية، إنجليزية فقط)
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Langue", list(lang_options.keys()))
L = lang_options[L_key]

# 3. جلب المفتاح السري للذكاء الاصطناعي
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 4. قاموس النصوص (النسخة 8 الأصلية بدون فصحى)
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "تحرير فاتورة (Devis)"],
        "ai_label": "اشرح المشكلة هنا:",
        "calc_label": "قوة الجهاز (Watt):",
        "invoice_header": "📄 إنشاء فاتورة تقديرية",
        "prompt": "أنت خبير كهرباء تونسي، أجب بالدارجة التونسية التقنية."
    },
    "Français": {
        "title": "⚡ Pro Electric Platform",
        "menu": ["Consultation AI", "Calculateur", "Établir Facture"],
        "ai_label": "Décrivez le problème :",
        "calc_label": "Puissance (Watt) :",
        "invoice_header": "📄 Créer un Devis",
        "prompt": "Tu es un expert électricien. Réponds en français technique."
    },
    "English": {
        "title": "⚡ Electric Master Pro",
        "menu": ["AI Consultation", "Calculator", "Create Invoice"],
        "ai_label": "Describe the fault:",
        "calc_label": "Power (Watt):",
        "invoice_header": "📄 Generate Invoice",
        "prompt": "You are a professional electrical expert. Provide advice in English."
    }
}

# 5. الواجهة الرئيسية
st.markdown(f"### {texts[L]['title']}")
st.write("---")

# 6. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", texts[L]["menu"])

# --- القسم الأول: استشارة الخبير (AI) ---
if choice == texts[L]["menu"][0]:
    st.subheader(texts[L]["menu"][0])
    query = st.text_area(texts[L]["ai_label"], height=100)
    if st.button("تحليل" if L == "تونس" else "Analyze"):
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"{texts[L]['prompt']} : {query}"}]}]}
            try:
                res = requests.post(url, json=payload)
                answer = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.info(answer)
            except:
                st.error("خطأ في الاتصال.")

# --- القسم الثاني: حاسبة القياسات ---
elif choice == texts[L]["menu"][1]:
    st.subheader(texts[L]["menu"][1])
    watt = st.number_input(texts[L]["calc_label"], value=2000)
    if st.button("احسب" if L == "تونس" else "Calculate"):
        amp = watt / 220
        wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
        st.success(f"I = {amp:.2f} A | Cable: {wire}")

# --- القسم الثالث: تحرير الفواتير (النسخة 8 الأصلية) ---
elif choice == texts[L]["menu"][2]:
    st.subheader(texts[L]["invoice_header"])
    c_name = st.text_input("اسم الزبون / Client Name:")
    items = st.text_area("المواد والخدمات / Items & Services:")
    price = st.number_input("المبلغ الإجمالي (DT):", min_value=0.0)
    
    if st.button("حفظ الفاتورة" if L == "تونس" else "Save Invoice"):
        invoice_content = f"""
        {texts[L]['title']}
        التاريخ: {datetime.now().strftime('%d/%m/%Y')}
        الزبون: {c_name}
        ---------------------------
        التفاصيل:
        {items}
        ---------------------------
        المبلغ الإجمالي: {price:.3f} دينار تونسي
        ---------------------------
        """
        st.code(invoice_content)
        st.download_button("تحميل (.txt)", invoice_content, file_name=f"Devis_{c_name}.txt")
