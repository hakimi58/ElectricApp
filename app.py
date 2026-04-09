import streamlit as st
import requests
from datetime import datetime

# 1. إعدادات الصفحة والألوان
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

# 3. قاموس اللغات (تم حذف الفصحى وبقاء 3 لغات فقط)
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["🤖 استشارة الخبير (AI)", "🧮 حاسبة القياسات", "💰 الفواتير والأسعار"],
        "prompt": "أنت خبير كهرباء تونسي محترف، أجب بالدارجة التونسية التقنية الواضحة وبشكل نقاط.",
        "calc_res": "النتيجة: كابل {wire} وقاطع {res}",
        "ai_label": "اشرح المشكلة التقنية هنا:"
    },
    "Français": {
        "title": "⚡ Tunisia Electric Pro",
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "💰 Facturation & Prix"],
        "prompt": "Tu es un expert électricien tunisien. Réponds en français technique.",
        "calc_res": "Résultat: Câble {wire} et Disjoncteur {res}",
        "ai_label": "Décrivez le problème ici :"
    },
    "English": {
        "title": "⚡ Electric Master Pro",
        "menu": ["🤖 AI Expert", "🧮 Calculator", "💰 Invoicing & Prices"],
        "prompt": "You are a professional electrical expert. Provide advice in English.",
        "calc_res": "Result: {wire} wire and {res} breaker",
        "ai_label": "Describe the fault here:"
    }
}

# 4. إعدادات اللغة في الجانب (3 خيارات فقط)
st.sidebar.subheader("⚙️ Settings / الإعدادات")
lang_map = {
    "🇹🇳 تونسية": "تونس", 
    "🇫🇷 Français": "Français", 
    "🇺🇸 English": "English"
}
L_key = st.sidebar.selectbox("🌐 اختر اللغة / Langue", list(lang_map.keys()))
L = lang_map[L_key]

# 5. عرض الواجهة
current_text = texts[L]
st.markdown(f"### {current_text['title']}")

API_KEY = st.secrets.get("GOOGLE_API_KEY")
choice = st.sidebar.radio("🛠️ الأدوات", current_text["menu"])

# --- 1. استشارة الذكاء الاصطناعي ---
if choice == current_text["menu"][0]:
    st.subheader(current_text["menu"][0])
    query = st.text_area(current_text["ai_label"], height=100)
    if st.button("تحليل / Analyze"):
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"{current_text['prompt']} : {query}"}]}]}
            try:
                res = requests.post(url, json=payload)
                st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
            except: st.error("Error/خطأ")

# --- 2. حاسبة القياسات ---
elif choice == current_text["menu"][1]:
    st.subheader(current_text["menu"][1])
    watt = st.number_input("Watt:", value=2000)
    amp = watt / 220
    if amp <= 11: res, wire = "10A", "1.5mm²"
    elif amp <= 17: res, wire = "16A", "2.5mm²"
    else: res, wire = "25A+", "4mm²+"
    st.success(current_text["calc_res"].format(wire=wire, res=res))

# --- 3. الفواتير والأسعار ---
elif choice == current_text["menu"][2]:
    st.subheader(current_text["menu"][2])
    if 'cart' not in st.session_state: st.session_state.cart = []
    
    col1, col2 = st.columns(2)
    with col1:
        item = st.selectbox("المنتج / Product:", list(TUNISIA_PRICES.keys()))
        qty = st.number_input("الكمية / Qty:", min_value=1, value=1)
        if st.button("إضافة / Add"):
            st.session_state.cart.append({"item": item, "qty": qty, "total": TUNISIA_PRICES[item]*qty})
            st.rerun()
    with col2:
        grand_total = 0
        for e in st.session_state.cart:
            st.write(f"- {e['qty']}x {e['item']} = {e['total']:.3f} DT")
            grand_total += e['total']
        st.warning(f"Total: {grand_total:.3f} DT")
        if st.button("مسح / Clear"): 
            st.session_state.cart = []
            st.rerun()
