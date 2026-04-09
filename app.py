import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="wide")

# 2. قاعدة البيانات (محدثة)
TUNISIA_PRICES = {
    "سلك 1.5 مم² (100م)": 95.000,
    "سلك 2.5 مم² (100م)": 145.000,
    "قاطع 10A/16A": 13.500,
    "قاطع 20A/32A": 16.800,
    "قاطع تفاضلي 30mA": 95.000,
    "صندوق 8 قواطع": 48.000,
    "مفتاح إنارة بسيط": 4.500,
    "مأخذ تيار (Prise)": 6.500,
    "يد عاملة (يومية)": 90.000
}

# 3. اختيار اللغة
lang_map = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_map.keys()))
L = lang_map[L_key]

# 4. واجهة الفواتير المميزة
st.markdown(f"### 💰 نظام الفواتير والتقديرات الاحترافي")
st.write("---")

# تهيئة سلة المشتريات
if 'cart' not in st.session_state:
    st.session_state.cart = []

# إدخال بيانات الفني والزبون
col_info1, col_info2 = st.columns(2)
with col_info1:
    tech_name = st.text_input("اسم الفني (أنت):", value="المعلم للكهرباء")
    tech_phone = st.text_input("رقم الهاتف:")
with col_info2:
    client_name = st.text_input("اسم الزبون:")
    date_now = datetime.now().strftime('%d/%m/%Y')

st.write("---")

# إضافة المواد
col_add1, col_add2, col_add3 = st.columns([2, 1, 1])
with col_add1:
    selected_product = st.selectbox("اختر المادة من المخزن:", list(TUNISIA_PRICES.keys()))
with col_add2:
    quantity = st.number_input("الكمية:", min_value=1, value=1)
with col_add3:
    st.write("##")
    if st.button("➕ إضافة للفاتورة"):
        price_unit = TUNISIA_PRICES[selected_product]
        st.session_state.cart.append({
            "المادة": selected_product,
            "الكمية": quantity,
            "سعر الوحدة": f"{price_unit:.3f} DT",
            "المجموع": price_unit * quantity
        })

# عرض الفاتورة بشكل مميز (جدول)
if st.session_state.cart:
    st.markdown("#### 📄 معاينة الفاتورة")
    df = pd.DataFrame(st.session_state.cart)
    
    # تنسيق الجدول ليظهر بشكل احترافي
    st.table(df)
    
    grand_total = sum(item['المجموع'] for item in st.session_state.cart)
    
    # خلية المجموع النهائي
    st.markdown(f"""
    <div style="background-color:#f1c40f; padding:20px; border-radius:10px; text-align:center;">
        <h2 style="color:black; margin:0;">المبلغ الإجمالي: {grand_total:.3f} DT</h2>
    </div>
    """, unsafe_allow_html=True)

    # أزرار التحكم
    col_ctrl1, col_ctrl2 = st.columns(2)
    with col_ctrl1:
        if st.button("🗑️ مسح الفاتورة"):
            st.session_state.cart = []
            st.rerun()
    with col_ctrl2:
        # توليد النص النهائي للنسخ أو الطباعة
        invoice_header = f"⚡ {tech_name}\n📞 الهاتف: {tech_phone}\n📅 التاريخ: {date_now}\n👤 الزبون: {client_name}\n"
        invoice_body = "\n".join([f"- {i['المادة']} (x{i['الكمية']}): {i['المجموع']:.3f} DT" for i in st.session_state.cart])
        full_invoice = f"{invoice_header}\n{'-'*30}\n{invoice_body}\n{'-'*30}\nالإجمالي: {grand_total:.3f} DT"
        
        st.download_button("📩 تحميل الفاتورة للزبون", full_invoice, file_name=f"Facture_{client_name}.txt")

else:
    st.info("قم بإضافة المواد لإنشاء فاتورة جديدة.")
    
