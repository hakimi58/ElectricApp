import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات المواد مع الأسعار التقريبية (بالدينار التونسي)
# ملاحظة: هذه أسعار تقريبية للسوق التونسية حالياً
HAKIM_PRICES = {
    "Boite encastré 3 M": 0.850,
    "Boite encastré 4 M": 1.200,
    "Boite encastré 6 M": 1.800,
    "Coffret 24 module Hager": 145.000,
    "Monture 3 modules sys43": 2.400,
    "Monture 4 modules sys43": 3.200,
    "Monture 6 modules sys43": 4.500,
    "Boite encastrement PT 5": 0.650,
    "Disjoncteur différentiel 32A": 85.000,
    "Disjoncteur DPN 20A": 9.500,
    "Disjoncteur DPN 16A": 9.500,
    "Disjoncteur DPN 10A": 10.500,
    "Interrupteur va et Vien Sys43": 6.800,
    "Bouche module Sys43": 1.200,
    "Prise 2p+terre Sys43": 7.500,
    "Cable distribution tv SAT (m)": 1.200,
    "Cable réseau Cat 6 (m)": 1.500,
    "Domino 50": 4.500,
    "Domino 35": 3.200,
    "Tolésolon": 1.500
}

# 3. اختيار اللغة
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_options.keys()))
L = lang_options[L_key]

texts = {
    "تونس": {
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "add": "إضافة للفاتورة", "total": "المجموع الجملي"
    },
    "Français": {
        "menu": ["Consultation AI", "Calculateur", "Facturation & Prix"],
        "add": "Ajouter", "total": "Total Global"
    }
}
curr = texts.get(L, texts["تونس"])

# 4. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# الأقسام 1 و 2 تظل كما هي في النسخة 8
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    st.write("قسم الذكاء الاصطناعي")
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    st.write("قسم الحاسبة")

# --- القسم 3: نظام الفواتير بالأسعار التلقائية ---
elif choice == curr["menu"][2]:
    st.subheader("📋 نظام الفواتير والأسعار التونسية")
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # واجهة الإدخال
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            prod = st.selectbox("اختر المادة:", list(HAKIM_PRICES.keys()))
        with col2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with col3:
            # السعر يظهر تلقائياً من القاعدة ولكن يمكن تعديله
            default_price = HAKIM_PRICES[prod]
            price = st.number_input("السعر (DT):", min_value=0.0, value=default_price, format="%.3f")
        
        if st.button(curr["add"], use_container_width=True):
            st.session_state.cart.append({"Désignation": prod, "Qty": qte, "Price": price, "Total": qte*price})
            st.rerun()

    # عرض الفاتورة والمسح السريع
    if st.session_state.cart:
        st.write("---")
        h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 0.5])
        h1.write("**Désignation**"); h2.write("**Qty**"); h3.write("**P.U**"); h4.write("**Total**"); h5.write("🗑️")

        for i, item in enumerate(st.session_state.cart):
            r1, r2, r3, r4, r5 = st.columns([3, 1, 1, 1, 0.5])
            r1.write(item["Désignation"])
            r2.write(str(item["Qty"]))
            r3.write(f"{item['Price']:.3f}")
            r4.write(f"**{item['Total']:.3f}**")
            if r5.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        grand_total = sum(it["Total"] for it in st.session_state.cart)
        st.success(f"### {curr['total']}: {grand_total:.3f} DT")
