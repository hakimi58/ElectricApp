import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة (النسخة 8 الأصلية)
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات المواد (حسب ملفك وبأسعار افتراضية يمكنك تعديلها)
HAKIM_DATABASE = [
    "Boite encastré 3 M", "Boite encastré 4 M", "Boite encastré 6 M",
    "Coffret 24 module Hager", "Monture 3 modules sys43", "Monture 4 modules sys43",
    "Monture 6 modules sys43", "Boite encastrement PT 5", "Disjoncteur différentiel 32A",
    "Disjoncteur DPN 20A", "Disjoncteur DPN 16A", "Disjoncteur DPN 10A",
    "Interrupteur va et Vien System 43", "Bouche module System 43", "Prise 2p+terre System 43",
    "Cable distribution tv SAT", "Cable réseau Cat 6", "Tolésolon", "Domino 50", "Domino 35"
]

# 3. نظام اختيار اللغة (تونسية، فرنسية، إنجليزية)
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Langue", list(lang_options.keys()))
L = lang_options[L_key]

# 4. جلب المفتاح السري للذكاء الاصطناعي
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 5. قاموس النصوص
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "inv_header": "📄 إنشاء فاتورة / Devis",
        "add_item": "إضافة المادة",
        "item_col": "المادة", "qty_col": "الكمية", "price_col": "الثمن الوحدوي", "total_col": "المجموع",
        "grand_total": "المجموع الجملي:"
    },
    "Français": {
        "title": "⚡ Pro Electric Platform",
        "menu": ["Consultation AI", "Calculateur", "Système de Facturation"],
        "inv_header": "📄 Créer une Facture / Devis",
        "add_item": "Ajouter l'article",
        "item_col": "Désignation", "qty_col": "Qté", "price_col": "Prix Unitaire", "total_col": "Total",
        "grand_total": "Total Global:"
    }
}
curr = texts.get(L, texts["تونس"])

# 6. الواجهة الرئيسية والقائمة الجانبية
st.markdown(f"### {curr['title']}")
st.write("---")
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- القسم الأول والثاني (AI والحاسبة) ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    query = st.text_area("اشرح المشكلة هنا:", height=100)
    if st.button("تحليل"):
        if query and API_KEY:
            # كود الذكاء الاصطناعي هنا
            st.info("الخبير يقوم بالتحليل...")

elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    watt = st.number_input("قوة الجهاز (Watt):", value=2000)
    amp = watt / 220
    st.success(f"التيار: {amp:.2f} A")

# --- القسم الثالث: نظام الفواتير المتطور (شغل المحلات) ---
elif choice == curr["menu"][2]:
    st.subheader(curr["inv_header"])
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # واجهة الإدخال السريع
    with st.expander("➕ إضافة مادة جديدة", expanded=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            # اختيار المادة من قاعدة البيانات
            prod = st.selectbox(curr["item_col"], HAKIM_DATABASE)
        with c2:
            qte = st.number_input(curr["qty_col"], min_value=1, value=1)
        with c3:
            price = st.number_input(curr["price_col"], min_value=0.0, step=0.1, format="%.3f")
        
        if st.button(curr["add_item"]):
            st.session_state.cart.append({
                "Désignation": prod, 
                "Qty": qte, 
                "Price": price, 
                "Total": qte * price
            })
            st.rerun()

    # عرض الفاتورة بشكل احترافي
    if st.session_state.cart:
        st.write("---")
        # تصميم الجدول
        col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 0.5])
        col1.write(f"**{curr['item_col']}**")
        col2.write(f"**{curr['qty_col']}**")
        col3.write(f"**{curr['price_col']}**")
        col4.write(f"**{curr['total_col']}**")
        col5.write("🗑️")

        for i, item in enumerate(st.session_state.cart):
            r1, r2, r3, r4, r5 = st.columns([3, 1, 1, 1, 0.5])
            r1.write(item["Désignation"])
            r2.write(str(item["Qty"]))
            r3.write(f"{item['Price']:.3f}")
            r4.write(f"{item['Total']:.3f}")
            
            # زر المسح السريع ❌
            if r5.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        # حساب المجموع النهائي
        total_sum = sum(it["Total"] for it in st.session_state.cart)
        st.markdown(f"### {curr['grand_total']} : {total_sum:.3f} DT")
        
        # خيارات إضافية
        if st.button("🗑️ مسح الفاتورة كاملة"):
            st.session_state.cart = []
            st.rerun()
