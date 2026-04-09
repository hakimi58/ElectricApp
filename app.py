import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", layout="wide")

# 2. قاعدة البيانات والأسعار التلقائية
HAKIM_PRICES = {
    "Boite encastré 3 M": 0.850, "Boite encastré 4 M": 1.200, "Boite encastré 6 M": 1.800,
    "Coffret 24 module Hager": 145.000, "Monture 3 modules sys43": 2.400, "Monture 4 modules sys43": 3.200,
    "Monture 6 modules sys43": 4.500, "Disjoncteur DPN 20A": 9.500, "Disjoncteur DPN 16A": 9.500,
    "Prise 2p+terre Sys43": 7.500, "Interrupteur va et Vien Sys43": 6.800
}

# 3. ذاكرة الجلسة
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 4. القائمة الجانبية
st.sidebar.title("🛠️ الأدوات")
choice = st.sidebar.radio("اختر الوظيفة:", ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"])

# --- نظام الفواتير القابل للتعديل ---
if choice == "نظام الفواتير":
    st.header("📋 فاتورة قابلة للتعديل المباشر")

    # واجهة إضافة المواد
    with st.expander("➕ إضافة مادة جديدة", expanded=True):
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            prod = st.selectbox("المادة:", list(HAKIM_PRICES.keys()))
        with col2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with col3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=HAKIM_PRICES[prod], format="%.3f")
        
        if st.button("إضافة السلعة ➕", use_container_width=True):
            st.session_state['cart'].append({
                "المادة": prod,
                "الكمية": qte,
                "الثمن الوحدوي": price,
                "المجموع": qte * price
            })
            st.rerun()

    # عرض وتحرير الفاتورة
    if st.session_state['cart']:
        st.write("---")
        st.info("💡 يمكنك الضغط على أي خانة في الجدول (الكمية أو الثمن) لتغييرها مباشرة!")
        
        # تحويل السلة إلى DataFrame
        df = pd.DataFrame(st.session_state['cart'])
        
        # استخدام data_editor للسماح بالتعديل اليدوي داخل الجدول
        edited_df = st.data_editor(
            df,
            column_config={
                "الكمية": st.column_config.NumberColumn(min_value=1),
                "الثمن الوحدوي": st.column_config.NumberColumn(format="%.3f"),
                "المجموع": st.column_config.NumberColumn(disabled=True, format="%.3f"), # المجموع يحسب آلياً
            },
            num_rows="dynamic", # يسمح لك بحذف أسطر بالضغط على زر Del في لوحة المفاتيح
            use_container_width=True,
            key="bill_editor"
        )

        # تحديث المجموع بعد التعديل (إعادة الحساب)
        edited_df["المجموع"] = edited_df["الكمية"] * edited_df["الثمن الوحدوي"]
        
        # حفظ التعديلات في الذاكرة
        if not edited_df.equals(df):
            st.session_state['cart'] = edited_df.to_dict('records')
            st.rerun()

        # حساب المجموع النهائي
        total_final = edited_df["المجموع"].sum()
        st.markdown(f"### المجموع الجملي الصافي: :green[{total_final:.3f} DT]")

        if st.button("🗑️ مسح الفاتورة"):
            st.session_state['cart'] = []
            st.rerun()
