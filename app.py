import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", layout="wide")

# 2. قاعدة البيانات والأسعار
HAKIM_PRICES = {
    "Boite encastré 3 M": 0.850, "Boite encastré 4 M": 1.200, "Boite encastré 6 M": 1.800,
    "Coffret 24 module Hager": 145.000, "Monture 3 modules sys43": 2.400, "Monture 4 modules sys43": 3.200,
    "Monture 6 modules sys43": 4.500, "Disjoncteur DPN 20A": 9.500, "Disjoncteur DPN 16A": 9.500,
    "Prise 2p+terre Sys43": 7.500, "Interrupteur va et Vien Sys43": 6.800
}

# 3. التأكد من حفظ البيانات في ذاكرة المتصفح (مهم جداً)
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 4. القائمة الجانبية
st.sidebar.title("🛠️ الأدوات")
menu = ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"]
choice = st.sidebar.radio("اختر الوظيفة:", menu)

# --- نظام الفواتير (Professionnel) ---
if choice == "نظام الفواتير":
    st.header("📋 فاتورة محل كهرباء")

    # واجهة إضافة المواد
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            prod = st.selectbox("المادة:", list(HAKIM_PRICES.keys()))
        with col2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with col3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=HAKIM_PRICES[prod], format="%.3f")
        
        if st.button("إضافة السلعة ➕", use_container_width=True):
            # إضافة المادة للقائمة الحالية
            st.session_state['cart'].append({
                "Désignation": prod,
                "Qté": qte,
                "P.U": price,
                "Total": qte * price
            })
            st.rerun()

    # عرض الفاتورة بشكل جدول (إذا كانت السلة غير فارغة)
    if st.session_state['cart']:
        st.write("---")
        df = pd.DataFrame(st.session_state['cart'])
        df.index += 1
        
        # عرض الجدول
        st.table(df.style.format({"P.U": "{:.3f}", "Total": "{:.3f}"}))

        # حساب المجموع
        total_final = sum(item["Total"] for item in st.session_state['cart'])
        st.markdown(f"### المجموع الجملي: :green[{total_final:.3f} DT]")

        if st.button("🗑️ مسح الفاتورة"):
            st.session_state['cart'] = []
            st.rerun()
