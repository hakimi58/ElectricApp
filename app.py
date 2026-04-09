import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات المواد الكهربائية التونسية (من ملفك)
HAKIM_ITEMS = [
    "Boite encastré 3 M", "Boite encastré 4 M", "Boite encastré 6 M",
    "Coffret 24 module Hager", "Monture 3 modules sys43", "Monture 4 modules sys43",
    "Monture 6 modules sys43", "Boite encastrement PT 5", "Disjoncteur différentiel 32A",
    "Disjoncteur DPN 20A", "Disjoncteur DPN 16A", "Disjoncteur DPN 10A",
    "Interrupteur va et Vien System 43", "Bouche module System 43", "Prise 2p+terre System 43",
    "Cable distribution tv SAT", "Cable réseau Cat 6", "Tolésolon", "Domino 50", "Domino 35"
]

# 3. اختيار اللغة (تونسية، فرنسية، إنجليزية)
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Langue", list(lang_options.keys()))
L = lang_options[L_key]

# 4. جلب المفتاح السري للذكاء الاصطناعي
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 5. قاموس النصوص الاحترافي
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير (Pro)"],
        "inv_header": "🛒 إدارة المبيعات والفواتير",
        "add_item": "إضافة المادة",
        "manual_add": "🖋️ إضافة مادة يدوياً",
        "total": "المجموع الجملي",
        "clear": "إفراغ السلة"
    },
    "Français": {
        "title": "⚡ Pro Electric Platform",
        "menu": ["Consultation AI", "Calculateur", "Facturation (Pro)"],
        "inv_header": "🛒 Gestion de Facturation",
        "add_item": "Ajouter",
        "manual_add": "🖋️ Article manuel",
        "total": "Total Global",
        "clear": "Vider le panier"
    }
}
curr = texts.get(L, texts["تونس"])

# 6. الواجهة والقائمة الجانبية
st.markdown(f"### {curr['title']}")
st.write("---")
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- الأقسام 1 و 2 (AI وحاسبة) ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    query = st.text_area("اشرح العطل هنا:")
    if st.button("تحليل"): st.info("جاري التحليل...")

elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    watt = st.number_input("القدرة (Watt):", value=2000)
    st.success(f"التيار المقدر: {watt/220:.2f} A")

# --- القسم 3: نظام الفواتير الاحترافي (المطور) ---
elif choice == curr["menu"][2]:
    st.markdown(f"## {curr['inv_header']}")
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # 1. واجهة الإدخال الذكية
    with st.container():
        st.markdown("#### ➕ إضافة سلعة")
        c1, c2, c3 = st.columns([2, 1, 1])
        
        with c1:
            item_type = st.radio("نوع الإدخال:", ["من القائمة", "يدوي"], horizontal=True)
            if item_type == "من القائمة":
                prod_name = st.selectbox("اختر المادة:", HAKIM_ITEMS)
            else:
                prod_name = st.text_input("اسم المادة الجديدة:")
        
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        
        with c3:
            price = st.number_input("الثمن الوحدوي (DT):", min_value=0.0, step=0.1, format="%.3f")

        if st.button(curr["add_item"], use_container_width=True):
            if prod_name:
                st.session_state.cart.append({
                    "Désignation": prod_name,
                    "Qté": qte,
                    "P.U": price,
                    "Total": qte * price
                })
                st.rerun()

    # 2. عرض الجدول والتحكم (المسح السريع)
    if st.session_state.cart:
        st.markdown("---")
        st.markdown("### 📋 قائمة المشتريات")
        
        # ترويسة الجدول
        h1, h2, h3, h4, h5 = st.columns([3, 1, 1, 1, 0.5])
        h1.write("**Désignation**")
        h2.write("**Qté**")
        h3.write("**P.U (DT)**")
        h4.write("**Total**")
        h5.write("🗑️")

        for i, item in enumerate(st.session_state.cart):
            r1, r2, r3, r4, r5 = st.columns([3, 1, 1, 1, 0.5])
            r1.write(item["Désignation"])
            r2.write(str(item["Qté"]))
            r3.write(f"{item['P.U']:.3f}")
            r4.write(f"**{item['Total']:.3f}**")
            
            # زر المسح السريع (🗑️)
            if r5.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        # 3. المجموع الجملي
        total_sum = sum(it["Total"] for it in st.session_state.cart)
        st.markdown("---")
        st.success(f"### {curr['total']}: {total_sum:.3f} DT")
        
        if st.button(curr["clear"]):
            st.session_state.cart = []
            st.rerun()
