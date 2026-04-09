import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. الأسعار التلقائية
HAKIM_PRICES = {
    "Boite encastré 3 M": 0.850, "Boite encastré 4 M": 1.200, "Boite encastré 6 M": 1.800,
    "Coffret 24 module Hager": 145.000, "Monture 3 modules sys43": 2.400, "Monture 4 modules sys43": 3.200,
    "Monture 6 modules sys43": 4.500, "Boite encastrement PT 5": 0.650, "Disjoncteur différentiel 32A": 85.000,
    "Disjoncteur DPN 20A": 9.500, "Disjoncteur DPN 16A": 9.500, "Disjoncteur DPN 10A": 10.500,
    "Interrupteur va et Vien Sys43": 6.800, "Bouche module Sys43": 1.200, "Prise 2p+terre Sys43": 7.500,
    "Cable distribution tv SAT (m)": 1.200, "Cable réseau Cat 6 (m)": 1.500, "Domino 50": 4.500,
    "Domino 35": 3.200, "Tolésolon": 1.500
}

# 3. التأكد من وجود "المخزن" (session_state) لجمع المواد
if 'invoice_list' not in st.session_state:
    st.session_state['invoice_list'] = []

# 4. اختيار اللغة والقائمة الجانبية
L_key = st.sidebar.selectbox("🌐 اللغة", ["🇹🇳 تونسية", "🇫🇷 Français"])
menu = ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"]
choice = st.sidebar.radio("🛠️ الأدوات", menu)

# --- نظام الفواتير (المطور ليجمع المواد) ---
if choice == menu[2]:
    st.markdown("### 📋 نموذج فاتورة المحلات التونسية")
    
    # واجهة الإضافة
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            prod = st.selectbox("المادة (Désignation):", list(HAKIM_PRICES.keys()))
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=HAKIM_PRICES[prod], format="%.3f")
        
        if st.button("إضافة المادة للجدول ➕", use_container_width=True):
            # إضافة السطر الجديد للمخزن
            new_item = {
                "المادة": prod,
                "الكمية": qte,
                "الثمن الوحدوي": price,
                "المجموع": qte * price
            }
            st.session_state['invoice_list'].append(new_item)
            st.rerun()

    # عرض الجدول الكامل (الذي يحتوي على كل المواد المضافة)
    if st.session_state['invoice_list']:
        st.write("---")
        st.markdown(f"**التاريخ:** {datetime.now().strftime('%d/%m/%Y')}")
        
        # تحويل المخزن إلى جدول
        df = pd.DataFrame(st.session_state['invoice_list'])
        df.index += 1 # ترقيم الأسطر
        
        # عرض الجدول (كما في المحلات)
        st.table(df.style.format({"الثمن الوحدوي": "{:.3f}", "المجموع": "{:.3f}"}))

        # المجموع الجملي في الأسفل
        total_ttc = sum(item["المجموع"] for item in st.session_state['invoice_list'])
        
        st.markdown(f"""
        <div style="background-color: #f1f3f4; padding: 20px; border: 2px solid #2c3e50; border-radius: 10px; text-align: center;">
            <h2 style="color: #2c3e50; margin: 0;">المجموع الجملي الصافي: {total_ttc:.3f} DT</h2>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑️ مسح الفاتورة بالكامل"):
            st.session_state['invoice_list'] = []
            st.rerun()
