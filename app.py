import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة والألوان لضمان عدم وجود "شاشة سوداء"
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .invoice-box { background-color: #f9f9f9; border: 1px solid #ddd; padding: 20px; border-radius: 10px; font-family: 'Arial'; }
    .total-style { font-size: 24px; color: #27ae60; font-weight: bold; border-top: 2px solid #eee; padding-top: 10px; }
    .stButton>button { width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 2. قاعدة بيانات الأسعار
TUNISIA_PRICES = {
    "سلك 1.5 مم² (100م)": 95.000,
    "سلك 2.5 مم² (100م)": 145.000,
    "قاطع 10A/16A": 13.500,
    "قاطع 20A/32A": 16.800,
    "قاطع تفاضلي 30mA": 95.000,
    "صندوق 8 قواطع": 48.000,
    "مفتاح إنارة بسيط": 4.500,
    "مأخذ تيار (Prise)": 6.500,
    "يد عاملة (يومية)": 90.000
}

# 3. إعدادات اللغة والأدوات
lang_map = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Language", list(lang_map.keys()))
L = lang_map[L_key]

texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["🤖 استشارة الخبير (AI)", "🧮 حاسبة القياسات", "📄 نموذج الفاتورة المميز"],
        "ai_label": "اشرح المشكلة التقنية:",
        "calc_label": "قوة الجهاز (Watt):",
        "inv_header": "نموذج فاتورة احترافي"
    },
    "Français": {
        "title": "⚡ Tunisia Electric Pro",
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Facturation Pro"],
        "ai_label": "Décrivez le problème :",
        "calc_label": "Puissance (Watt) :",
        "inv_header": "Modèle de Facture Pro"
    }
}

# الحفاظ على الأدوات في الجانب
st.sidebar.write("---")
choice = st.sidebar.radio("🛠️ الأدوات", texts.get(L, texts["تونس"])["menu"])

# --- القسم 1: الذكاء الاصطناعي (موجود سابقاً) ---
if "الخبير" in choice or "AI" in choice:
    st.markdown(f"### {texts.get(L, texts['تونس'])['menu'][0]}")
    query = st.text_area(texts.get(L, texts['تونس'])['ai_label'])
    if st.button("تحليل"):
        API_KEY = st.secrets.get("GOOGLE_API_KEY")
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي: {query}"}]}]}
            res = requests.post(url, json=payload)
            st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])

# --- القسم 2: الحاسبة (موجود سابقاً) ---
elif "حاسبة" in choice or "Calcul" in choice:
    st.markdown(f"### {texts.get(L, texts['تونس'])['menu'][1]}")
    watt = st.number_input(texts.get(L, texts['تونس'])['calc_label'], value=2000)
    amp = watt / 220
    st.metric("Amperage", f"{amp:.2f} A")
    res, wire = ("10A", "1.5mm²") if amp <= 11 else ("16A", "2.5mm²") if amp <= 17 else ("25A", "4mm²")
    st.success(f"النتيجة: كابل {wire} وقاطع {res}")

# --- القسم 3: نموذج الفاتورة المميز (تصميم جديد) ---
elif "فاتورة" in choice or "Facture" in choice:
    st.markdown(f"### {texts.get(L, texts['تونس'])['inv_header']}")
    
    if 'cart' not in st.session_state: st.session_state.cart = []

    # شكل مدخلات الفاتورة
    with st.expander("➕ إضافة مواد للفاتورة", expanded=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1: prod = st.selectbox("المادة", list(TUNISIA_PRICES.keys()))
        with c2: qte = st.number_input("الكمية", min_value=1, value=1)
        with c3: 
            st.write("##")
            if st.button("إضافة"):
                st.session_state.cart.append({"Item": prod, "Qty": qte, "Price": TUNISIA_PRICES[prod], "Total": TUNISIA_PRICES[prod]*qte})
                st.rerun()

    # تصميم الفاتورة النهائي (النموذج المميز)
    if st.session_state.cart:
        st.markdown("---")
        st.markdown('<div class="invoice-box">', unsafe_allow_html=True)
        st.write(f"**تاريخ الفاتورة:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # عرض الجدول بشكل نظيف جداً
        df = pd.DataFrame(st.session_state.cart)
        df.index = df.index + 1 # ترقيم الأسطر
        st.table(df)
        
        grand_total = sum(item['Total'] for item in st.session_state.cart)
        st.markdown(f'<p class="total-style">المجموع الجملي: {grand_total:.3f} DT</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.button("🗑️ مسح الكل"):
                st.session_state.cart = []
                st.rerun()
        with col_f2:
            st.download_button("📥 تحميل الفاتورة", df.to_csv(), file_name="invoice.csv")
