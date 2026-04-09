import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. الأسعار التقريبية (تلقائية)
HAKIM_PRICES = {
    "Boite encastré 3 M": 0.850, "Boite encastré 4 M": 1.200, "Boite encastré 6 M": 1.800,
    "Coffret 24 module Hager": 145.000, "Monture 3 modules sys43": 2.400, "Monture 4 modules sys43": 3.200,
    "Monture 6 modules sys43": 4.500, "Boite encastrement PT 5": 0.650, "Disjoncteur différentiel 32A": 85.000,
    "Disjoncteur DPN 20A": 9.500, "Disjoncteur DPN 16A": 9.500, "Disjoncteur DPN 10A": 10.500,
    "Interrupteur va et Vien Sys43": 6.800, "Bouche module Sys43": 1.200, "Prise 2p+terre Sys43": 7.500,
    "Cable distribution tv SAT (m)": 1.200, "Cable réseau Cat 6 (m)": 1.500, "Domino 50": 4.500,
    "Domino 35": 3.200, "Tolésolon": 1.500
}

# 3. تهيئة سلة المشتريات (هذا هو السّر لكي لا تختفي المواد)
if 'invoice_list' not in st.session_state:
    st.session_state.invoice_list = []

# 4. اختيار اللغة
L_key = st.sidebar.selectbox("🌐 اللغة", ["🇹🇳 تونسية", "🇫🇷 Français", "🇺🇸 English"])

# 5. القائمة الجانبية
menu = ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"]
choice = st.sidebar.radio("🛠️ الأدوات", menu)

if choice == menu[2]:
    st.markdown("### 📋 نموذج فاتورة احترافي")
    
    # واجهة الإضافة
    with st.form("add_form", clear_on_submit=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            prod = st.selectbox("Désignation (المادة):", list(HAKIM_PRICES.keys()))
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=HAKIM_PRICES[prod], format="%.3f")
        
        submit = st.form_submit_button("إضافة المادة ➕")
        
        if submit:
            # إضافة المادة للقائمة الموجودة مسبقاً
            st.session_state.invoice_list.append({
                "المادة": prod,
                "الكمية": qte,
                "الثمن الوحدوي": f"{price:.3f}",
                "المجموع": qte * price
            })
            st.rerun()

    # عرض الفاتورة الكاملة
    if st.session_state.invoice_list:
        st.markdown("---")
        st.markdown(f"**التاريخ:** {datetime.now().strftime('%d/%m/%Y')} | **الزبون:** السيد ....................")
        
        # تحويل القائمة إلى جدول عرض
        df = pd.DataFrame(st.session_state.invoice_list)
        df.index += 1
        
        # عرض الجدول بشكل المحلات (كل المواد تظهر هنا)
        st.table(df)

        # المجموع النهائي
        total_ttc = sum(float(item["المجموع"]) for item in st.session_state.invoice_list)
        
        st.markdown(f"""
        <div style="background-color: #2c3e50; padding: 15px; border-radius: 8px; text-align: center;">
            <h2 style="color: #f39c12; margin: 0;">المجموع الجملي: {total_ttc:.3f} DT</h2>
        </div>
        """, unsafe_allow_html=True)

        # أزرار الإدارة
        col_del, col_down = st.columns(2)
        with col_del:
            if st.button("🗑️ مسح الفاتورة والبدء من جديد"):
                st.session_state.invoice_list = []
                st.rerun()
        with col_down:
            st.download_button("📥 تحميل الفاتورة", df.to_csv(), file_name="devis.csv")
