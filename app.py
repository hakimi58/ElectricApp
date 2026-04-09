import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قائمة موادك (بدون أسعار ثابتة لترك الحرية لك)
HAKIM_DATABASE = [
    "Boite encastré 3 M", "Boite encastré 4 M", "Boite encastré 6 M",
    "Coffret 24 module Hager", "Monture 3 modules sys43", "Monture 4 modules sys43",
    "Monture 6 modules sys43", "Boite encastrement PT 5", "Disjoncteur différentiel 32A",
    "Disjoncteur DPN 20A", "Disjoncteur DPN 16A", "Disjoncteur DPN 10A",
    "Interrupteur va et Vien System 43", "Bouche module System 43", "Prise 2p+terre System 43",
    "Cable distribution tv SAT", "Cable réseau Cat 6", "Tolésolon", "Domino 50", "Domino 35"
]

# 3. اختيار اللغة
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_options.keys()))
L = lang_options[L_key]

# 4. نصوص الواجهة
texts = {
    "تونس": {
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "inv_header": "📄 إنشاء فاتورة / Devis",
        "add_item": "إضافة للفاتورة",
        "total": "المجموع الجملي"
    },
    "Français": {
        "menu": ["Consultation AI", "Calculateur", "Système de Facturation"],
        "inv_header": "📄 Créer un Devis",
        "add_item": "Ajouter",
        "total": "Total Global"
    }
}
curr = texts.get(L, texts["تونس"])

# 5. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- القسم 1 و 2 (AI وحاسبة) ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    st.write("قسم الذكاء الاصطناعي جاهز")
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    st.write("قسم الحاسبة التقنية")

# --- القسم 3: نظام الفواتير (التحكم في الأسعار) ---
elif choice == curr["menu"][2]:
    st.markdown(f"### {curr['inv_header']}")
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # خانة الإدخال مع التحكم في السعر
    with st.form("price_form"):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            prod = st.selectbox("اختر السلعة:", HAKIM_DATABASE)
        with col2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with col3:
            # هنا تضع السعر يدوياً حسب سعر السوق اليوم
            price = st.number_input("السعر الحالي (DT):", min_value=0.0, step=0.1, format="%.3f")
        
        submit = st.form_submit_button(curr["add_item"])
        if submit:
            st.session_state.cart.append({"Désignation": prod, "Qty": qte, "Price": price, "Total": qte*price})
            st.rerun()

    # عرض الفاتورة والتحكم في الحذف
    if st.session_state.cart:
        st.write("---")
        df = pd.DataFrame(st.session_state.cart)
        
        # عرض البيانات مع زر حذف سريع ❌
        for i, item in enumerate(st.session_state.cart):
            c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 0.5])
            c1.write(item["Désignation"])
            c2.write(str(item["Qty"]))
            c3.write(f"{item['Price']:.3f}")
            c4.write(f"**{item['Total']:.3f}**")
            if c5.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        st.markdown("---")
        grand_total = sum(it["Total"] for it in st.session_state.cart)
        st.success(f"### {curr['total']}: {grand_total:.3f} DT")
