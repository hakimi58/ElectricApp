import streamlit as st
import requests
from datetime import datetime

# 1. حل مشكلة الشاشة السوداء عبر فرض تنسيق ألوان فاتح وواضح
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    /* فرض خلفية بيضاء ونصوص سوداء لمنع الشاشة السوداء */
    .stApp { background-color: #FFFFFF; color: #000000; }
    .stHeader { background-color: #f8f9fa; }
    h1, h2, h3, h4, p { color: #1e272e !important; }
    .stButton>button { background-color: #2ecc71; color: white; border-radius: 5px; border: none; }
    .stTextInput>div>div>input { color: #000000; }
    </style>
""", unsafe_allow_html=True)

# 2. قاعدة بيانات الأسعار التونسية 2026
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

# 3. إعدادات اللغة (قائمة منسدلة صغيرة في الجانب)
st.sidebar.subheader("⚙️ الإعدادات / Settings")
lang_options = {"🇹🇳 تونسية": "تونس", "🇸🇦 فصحى": "الفصحى", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اختر اللغة", list(lang_options.keys()))
L = lang_options[L_key]

# 4. قاموس النصوص
texts = {
    "تونس": {
        "title": "### ⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "prompt": "أنت خبير كهرباء تونسي، أجب بالدارجة التونسية التقنية."
    },
    "الفصحى": {
        "title": "### ⚡ خبير الكهرباء العربي",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "prompt": "أنت مستشار هندسة كهربائية، أجب باللغة العربية الفصحى."
    }
}

# 5. عرض العنوان (حجم متوسط لمنع الزحمة)
st.markdown(texts[L if L in texts else "تونس"]["title"])

API_KEY = st.secrets.get("GOOGLE_API_KEY")
choice = st.sidebar.radio("🛠️ الأدوات", texts[L if L in texts else "تونس"]["menu"])

# --- القسم الأول: الذكاء الاصطناعي ---
if "استشارة" in choice or "AI" in choice:
    st.subheader(choice)
    query = st.text_area("اشرح العطل هنا:", height=100)
    if st.button("تحليل المشكلة"):
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"{texts[L if L in texts else 'تونس']['prompt']} : {query}"}]}]}
            try:
                res = requests.post(url, json=payload)
                st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
            except: st.error("خطأ في الاتصال")

# --- القسم الثاني: الحاسبة ---
elif "حاسبة" in choice or "Calcul" in choice:
    st.subheader(choice)
    watt = st.number_input("القوة (Watt):", value=2000)
    amp = watt / 220
    wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
    st.success(f"I = {amp:.2f} A | الكابل: {wire}")

# --- القسم الثالث: الفواتير والأسعار ---
elif "الفواتير" in choice or "Invoice" in choice:
    st.subheader("💰 حساب التكلفة والسلعة")
    
    if 'cart' not in st.session_state: st.session_state.cart = []
    
    col1, col2 = st.columns(2)
    with col1:
        item = st.selectbox("اختر المادة:", list(TUNISIA_PRICES.keys()))
        qty = st.number_input("الكمية:", min_value=1, value=1)
        if st.button("إضافة للسلّة"):
            st.session_state.cart.append({"item": item, "qty": qty, "total": TUNISIA_PRICES[item]*qty})
            st.rerun()

    with col2:
        st.markdown("#### الفاتورة الحالية")
        grand_total = 0
        for e in st.session_state.cart:
            st.write(f"- {e['qty']}x {e['item']} = {e['total']:.3f} DT")
            grand_total += e['total']
        st.write(f"**الإجمالي: {grand_total:.3f} DT**")
        if st.button("مسح السلة"): 
            st.session_state.cart = []
            st.rerun()
