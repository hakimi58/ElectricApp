import streamlit as st
import requests
from datetime import datetime

# 1. إعدادات الصفحة وتثبيت الألوان لمنع الشاشة السوداء
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات الأسعار التونسية
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

# 3. قاموس اللغات الشامل (تم ملء جميع اللغات لمنع KeyError)
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "prompt": "أنت خبير كهرباء تونسي، أجب بالدارجة التونسية التقنية.",
        "calc_res": "النتيجة: كابل {wire} وقاطع {res}"
    },
    "الفصحى": {
        "title": "⚡ خبير الكهرباء العربي",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "prompt": "أنت مستشار هندسة كهربائية، أجب باللغة العربية الفصحى.",
        "calc_res": "النتيجة: سلك {wire} وقاطع {res}"
    },
    "Français": {
        "title": "⚡ Tunisia Electric Pro",
        "menu": ["Consultation AI", "Calculateur", "Facturation & Prix"],
        "prompt": "Tu es un expert électricien. Réponds en français technique.",
        "calc_res": "Résultat: Câble {wire} et Disjoncteur {res}"
    },
    "English": {
        "title": "⚡ Electric Master Pro",
        "menu": ["AI Consultation", "Calculator", "Invoicing & Prices"],
        "prompt": "You are a professional electrical expert. Provide advice in English.",
        "calc_res": "Result: {wire} wire and {res} breaker"
    }
}

# 4. اختيار اللغة (في الجانب)
st.sidebar.subheader("⚙️ Settings / الإعدادات")
lang_map = {"🇹🇳 تونسية": "تونس", "🇸🇦 فصحى": "الفصحى", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 Choose Language", list(lang_map.keys()))
L = lang_map[L_key]

# 5. عرض العنوان (استخدام get لمنع الخطأ البرمجي)
current_text = texts.get(L, texts["تونس"])
st.markdown(f"### {current_text['title']}")

# 6. قائمة الأدوات
choice = st.sidebar.radio("🛠️ Tools", current_text["menu"])

API_KEY = st.secrets.get("GOOGLE_API_KEY")

# --- 1. استشارة الذكاء الاصطناعي ---
if choice == current_text["menu"][0]:
    st.subheader(choice)
    query = st.text_area("Question / السؤال:", height=100)
    if st.button("OK"):
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"{current_text['prompt']} : {query}"}]}]}
            try:
                res = requests.post(url, json=payload)
                st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
            except: st.error("Error!")

# --- 2. حاسبة القياسات ---
elif choice == current_text["menu"][1]:
    st.subheader(choice)
    watt = st.number_input("Watt:", value=2000)
    amp = watt / 220
    if amp <= 11: res, wire = "10A", "1.5mm²"
    elif amp <= 17: res, wire = "16A", "2.5mm²"
    else: res, wire = "25A+", "4mm²+"
    st.success(current_text["calc_res"].format(wire=wire, res=res))

# --- 3. الفواتير والأسعار ---
elif choice == current_text["menu"][2]:
    st.subheader(choice)
    if 'cart' not in st.session_state: st.session_state.cart = []
    
    col1, col2 = st.columns(2)
    with col1:
        item = st.selectbox("Product / المنتج:", list(TUNISIA_PRICES.keys()))
        qty = st.number_input("Qty / الكمية:", min_value=1, value=1)
        if st.button("Add / إضافة"):
            st.session_state.cart.append({"item": item, "qty": qty, "total": TUNISIA_PRICES[item]*qty})
            st.rerun()
    with col2:
        grand_total = 0
        for e in st.session_state.cart:
            st.write(f"- {e['qty']}x {e['item']} = {e['total']:.3f} DT")
            grand_total += e['total']
        st.warning(f"Total: {grand_total:.3f} DT")
        if st.button("Clear / مسح"): 
            st.session_state.cart = []
            st.rerun()
