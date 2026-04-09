import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة والتنسيق الاحترافي
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .invoice-box { background-color: #ffffff; border: 2px solid #34495e; padding: 20px; border-radius: 10px; }
    .total-style { font-size: 26px; color: #ffffff; background-color: #27ae60; padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; }
    .stButton>button { border-radius: 5px; height: 3em; }
    </style>
""", unsafe_allow_html=True)

# 2. قاعدة بيانات الأسعار الأساسية
BASE_PRICES = {
    "سلك 1.5 مم² (100م)": 95.000,
    "سلك 2.5 مم² (100م)": 145.000,
    "قاطع 10A/16A": 13.500,
    "قاطع تفاضلي 30mA": 95.000,
    "يد عاملة (يومية)": 90.000
}

# 3. نظام اللغات المتقاطع
lang_map = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Language", list(lang_map.keys()))
L = lang_map[L_key]

texts = {
    "تونس": {
        "menu": ["🤖 خبير الأعطال", "🧮 حاسبة القياسات", "📄 نظام الفواتير"],
        "add": "إضافة للفاتورة", "clear": "مسح الكل", "total": "المجموع الجملي:", 
        "qty": "الكمية", "item": "المادة", "custom": "🖋️ إضافة مادة غير موجودة في القائمة",
        "price": "السعر (DT)", "manual_name": "اسم القطعة (مثلاً: صندوق 24 قاطع)"
    },
    "Français": {
        "menu": ["🤖 Expert AI", "🧮 Calculateur", "📄 Facturation Pro"],
        "add": "Ajouter", "clear": "Effacer", "total": "Total Global:", 
        "qty": "Qté", "item": "Article", "custom": "🖋️ Ajouter article personnalisé",
        "price": "Prix (DT)", "manual_name": "Nom de l'article (Ex: Coffret 24 mod)"
    },
    "English": {
        "menu": ["🤖 AI Expert", "🧮 Calculator", "📄 Invoicing System"],
        "add": "Add", "clear": "Clear", "total": "Grand Total:", 
        "qty": "Qty", "item": "Item", "custom": "🖋️ Add custom item",
        "price": "Price (DT)", "manual_name": "Item Name (Ex: 24-way Box)"
    }
}
curr = texts[L]

# 4. القائمة الجانبية
st.sidebar.write("---")
choice = st.sidebar.radio("🛠️", curr["menu"])

# --- 1. خبير الأعطال و 2. الحاسبة (تعمل بكل اللغات) ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    # ... (كود AI السابق يظل كما هو)
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    # ... (كود الحاسبة السابق يظل كما هو)

# --- 3. نظام الفواتير المتطور والمرن ---
elif choice == curr["menu"][2]:
    st.subheader(curr["menu"][2])
    
    if 'cart' not in st.session_state: st.session_state.cart = []

    # خيارين: اختيار من القائمة أو كتابة يدوية
    mode = st.radio("إدخال المواد:", ["من القائمة الجاهزة", "كتابة يدوية (قطعة خاصة)"] if L=="تونس" else ["Liste", "Manuel"])

    with st.container():
        c1, c2, c3 = st.columns([3, 1, 1])
        if "القائمة" in mode or "Liste" in mode:
            with c1: prod_name = st.selectbox(curr["item"], list(BASE_PRICES.keys()))
            u_price = BASE_PRICES[prod_name]
        else:
            with c1: prod_name = st.text_input(curr["manual_name"])
            with c2: u_price = st.number_input(curr["price"], min_value=0.0, step=0.5)
            
        with c2 if "القائمة" in mode or "Liste" in mode else c3: 
            qte = st.number_input(curr["qty"], min_value=1, value=1, key="qte_input")
        
        with c3 if "القائمة" in mode or "Liste" in mode else c1:
            st.write("##")
            if st.button(curr["add"]):
                if prod_name:
                    st.session_state.cart.append({
                        curr["item"]: prod_name, 
                        curr["qty"]: qte, 
                        "Prix Unitaire": f"{u_price:.3f}", 
                        "Total DT": u_price * qte
                    })
                    st.rerun()

    # عرض الفاتورة
    if st.session_state.cart:
        st.markdown("---")
        st.markdown('<div class="invoice-box">', unsafe_allow_html=True)
        df = pd.DataFrame(st.session_state.cart)
        df.index = df.index + 1
        st.table(df)
        
        grand_total = sum(item['Total DT'] for item in st.session_state.cart)
        st.markdown(f'<p class="total-style">{curr["total"]} {grand_total:.3f} DT</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.button("🗑️ " + curr["clear"]):
                st.session_state.cart = []
                st.rerun()
        with col_f2:
            st.download_button("📥 Download PDF/CSV", df.to_csv(), file_name=f"Facture_{datetime.now().day}.csv")
