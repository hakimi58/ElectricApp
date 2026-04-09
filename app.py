import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قائمة المواد الكاملة (من ملفك)
HAKIM_LIST = [
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
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير (Professionnel)"],
        "header": "🛒 منظومة بيع المواد الكهربائية"
    },
    "Français": {
        "menu": ["Consultation AI", "Calculateur", "Système de Vente"],
        "header": "🛒 Système de Vente Pro"
    }
}
curr = texts.get(L, texts["تونس"])

# 5. القائمة الجانبية
st.sidebar.markdown("---")
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- الأقسام 1 و 2 (بدون تغيير) ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    st.write("قسم الذكاء الاصطناعي")
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    st.write("قسم الحاسبة")

# --- القسم 3: الفاتورة المطورة (التغيير الكبير هنا) ---
elif choice == curr["menu"][2]:
    st.markdown(f"## {curr['header']}")
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # إطار إضافة المواد
    st.markdown("### ➕ إضافة مادة للفاتورة")
    with st.container():
        col_item, col_qty, col_pr = st.columns([3, 1, 1])
        with col_item:
            item_selected = st.selectbox("اختر المادة من القائمة:", HAKIM_LIST)
        with col_qty:
            qty_input = st.number_input("الكمية:", min_value=1, value=1)
        with col_pr:
            price_input = st.number_input("الثمن الوحدوي (DT):", min_value=0.0, format="%.3f")
        
        if st.button("اضف للسلّة 🛒"):
            st.session_state.cart.append({
                "المادة": item_selected,
                "الكمية": qty_input,
                "الثمن": price_input,
                "المجموع": qty_input * price_input
            })
            st.rerun()

    # عرض الفاتورة (جدول حقيقي)
    if st.session_state.cart:
        st.markdown("---")
        st.markdown("### 📋 تفاصيل الفاتورة")
        
        # تحويل السلة إلى جدول بيانات DataFrame لعرضه بشكل احترافي
        df = pd.DataFrame(st.session_state.cart)
        
        # إضافة عمود للحذف السريع
        for i, row in df.iterrows():
            c1, c2, c3, c4, c5 = st.columns([3, 1, 1, 1, 0.5])
            c1.write(row["المادة"])
            c2.write(str(row["الكمية"]))
            c3.write(f"{row['الثمن']:.3f}")
            c4.write(f"**{row['المجموع']:.3f}**")
            if c5.button("❌", key=f"del_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()

        st.markdown("---")
        total_final = sum(item["المجموع"] for item in st.session_state.cart)
        st.success(f"### المجموع الجملي صافي: {total_final:.3f} DT")
        
        if st.button("🗑️ إفراغ الفاتورة"):
            st.session_state.cart = []
            st.rerun()
