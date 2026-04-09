import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات المواد التونسية (الموسوعة المصغرة)
DB_MATERIELS = {
    "Foureau Orange 11mm (Rouleau)": 28.500,
    "Foureau Orange 13mm (Rouleau)": 32.800,
    "Foureau Orange 16mm (Rouleau)": 38.000,
    "Foureau Orange 20mm (Rouleau)": 48.500,
    "Hager: Disjoncteur DPN 10A": 10.500,
    "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800,
    "Hager: Différentiel 40A 30mA": 95.000,
    "Tunisie Câbles: 1.5mm² (100m)": 65.000,
    "Tunisie Câbles: 2.5mm² (100m)": 105.000,
    "Legrand Valena: Prise 2P+T": 11.200,
    "Générale: Boite Encastrement 3M": 0.900,
    "Spot LED 7W Encastré": 6.800
}

# 3. نظام اختيار اللغة
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Langue", list(lang_options.keys()))
L = lang_options[L_key]

# 4. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 5. قاموس النصوص
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

# 6. الواجهة الرئيسية
st.markdown(f"### {texts[L]['title']}")
st.write("---")

# 7. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", texts[L]["menu"])

# --- القسم الأول: استشارة الخبير (AI) ---
if choice == texts[L]["menu"][0]:
    st.subheader(texts[L]["menu"][0])
    query = st.text_area(texts[L]["ai_label"], height=100)
    if st.button("تحليل"):
        if query and API_KEY:
            # الرابط المحدث لضمان العمل
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"{texts[L]['prompt']} : {query}"}]}]}
            try:
                res = requests.post(url, json=payload)
                answer = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.info(answer)
            except:
                st.error("خطأ في الاتصال بالسيرفر. تأكد من الـ API KEY.")

# --- القسم الثاني: حاسبة القياسات ---
elif choice == texts[L]["menu"][1]:
    st.subheader(texts[L]["menu"][1])
    watt = st.number_input(texts[L]["calc_label"], value=2000)
    if st.button("احسب"):
        amp = watt / 220
        wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
        st.success(f"التيار: {amp:.2f} A | السلك المناسب: {wire}")

# --- القسم الثالث: تحرير الفواتير (تطوير مع قائمة المواد) ---
elif choice == texts[L]["menu"][2]:
    st.subheader(texts[L]["invoice_header"])
    
    # اختيار المادة من القائمة
    search = st.text_input("🔍 ابحث عن مادة (فورو، هاجر...):")
    filtered = [k for k in DB_MATERIELS.keys() if search.lower() in k.lower()]
    prod = st.selectbox("اختر المادة:", filtered if filtered else list(DB_MATERIELS.keys()))
    
    qte = st.number_input("الكمية:", min_value=1, value=1)
    unit_price = st.number_input("الثمن الواحد (DT):", value=DB_MATERIELS[prod], format="%.3f")
    
    if st.button("إضافة مادة للفاتورة"):
        if 'invoice_list' not in st.session_state:
            st.session_state['invoice_list'] = []
        st.session_state['invoice_list'].append({"item": prod, "qte": qte, "total": qte * unit_price})
        st.success("تمت الإضافة!")

    # عرض الفاتورة الحالية
    if 'invoice_list' in st.session_state and st.session_state['invoice_list']:
        df = pd.DataFrame(st.session_state['invoice_list'])
        st.table(df)
        grand_total = df['total'].sum()
        st.markdown(f"### المجموع الجملي: {grand_total:.3f} DT")
        
        if st.button("🗑️ مسح الكل"):
            st.session_state['invoice_list'] = []
            st.rerun()
