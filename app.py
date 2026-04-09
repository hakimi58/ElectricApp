import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", layout="wide")

# 2. الأسعار التلقائية
HAKIM_PRICES = {
    "Boite encastré 3 M": 0.850, "Boite encastré 4 M": 1.200, "Boite encastré 6 M": 1.800,
    "Coffret 24 module Hager": 145.000, "Monture 3 modules sys43": 2.400, "Monture 4 modules sys43": 3.200,
    "Monture 6 modules sys43": 4.500, "Disjoncteur DPN 20A": 9.500, "Disjoncteur DPN 16A": 9.500,
    "Prise 2p+terre Sys43": 7.500, "Interrupteur va et Vien Sys43": 6.800
}

# 3. ذاكرة الجلسة
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 4. اختيار الوظيفة
choice = st.sidebar.radio("الأدوات:", ["نظام الفواتير", "استشارة الخبير", "الحاسبة"])

if choice == "نظام الفواتير":
    st.header("📋 تحرير فاتورة احترافية")

    # إضافة المواد
    with st.expander("➕ إضافة مادة جديدة", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            prod = st.selectbox("المادة:", list(HAKIM_PRICES.keys()))
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=HAKIM_PRICES[prod], format="%.3f")
        
        if st.button("إضافة ➕"):
            st.session_state['cart'].append({"المادة": prod, "الكمية": qte, "الثمن": price, "المجموع": qte * price})
            st.rerun()

    if st.session_state['cart']:
        df = pd.DataFrame(st.session_state['cart'])
        
        # جدول قابل للتعديل
        edited_df = st.data_editor(df, use_container_width=True, key="main_editor")
        
        # إعادة حساب المجاميع بعد التعديل اليدوي
        edited_df["المجموع"] = edited_df["الكمية"] * edited_df["الثمن"]
        total_final = edited_df["المجموع"].sum()
        
        st.success(f"### المجموع الجملي: {total_final:.3f} DT")

        # --- تحضير نص الفاتورة للوورد (Word Friendly) ---
        client_name = st.text_input("اسم الزبون:", "حريف محترم")
        
        # تنسيق النص ليكون جميلاً عند فتحه في Word
        out_txt = f"قائمة تقديرية للمواد الكهربائية (DEVIS)\n"
        out_txt += f"التاريخ: {datetime.now().strftime('%d/%m/%Y')}\n"
        out_txt += f"الزبون: {client_name}\n"
        out_txt += "="*50 + "\n"
        out_txt += f"{'المادة':<30} | {'الكمية':<5} | {'الثمن':<10} | {'المجموع':<10}\n"
        out_txt += "-"*50 + "\n"
        
        for _, row in edited_df.iterrows():
            out_txt += f"{row['المادة']:<30} | {row['الكمية']:<5} | {row['الثمن']:<10.3f} | {row['المجموع']:<10.3f}\n"
        
        out_txt += "="*50 + "\n"
        out_txt += f"المجموع الجملي الصافي: {total_final:.3f} دينار تونسي\n"
        out_txt += "="*50 + "\n\nإمضاء الفني:\n...................."

        col_del, col_down = st.columns(2)
        with col_del:
            if st.button("🗑️ مسح الكل"):
                st.session_state['cart'] = []
                st.rerun()
        with col_down:
            # التحميل بصيغة .txt يضمن بقاء العربية سليمة
            st.download_button(
                label="📥 تحميل الفاتورة للوورد",
                data=out_txt.encode('utf-8-sig'), # هذا التشفير يحل مشكلة الرموز الغريبة
                file_name=f"Devis_{client_name}.txt",
                mime="text/plain"
            )
