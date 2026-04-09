 import streamlit as st
import requests
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات الأسعار التونسية (تقديرية لعام 2026 - يمكن تحديثها من الإعدادات لاحقاً)
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

# 3. قائمة الإعدادات واختيار اللغة
st.sidebar.markdown("### ⚙️ الإعدادات / Settings")
lang_options = {"🇹🇳 تونسية": "تونس", "🇸🇦 فصحى": "الفصحى", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_options.keys()))
L = lang_options[L_key]

# 4. قاموس النصوص
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "invoice_header": "💰 حساب التكلفة الجملية (السلعة واليد العاملة)",
        "add_item": "أضف مواد إلى القائمة",
        "total": "المبلغ الجملي التقديري:"
    },
    "الفصحى": {
        "title": "⚡ خبير الكهرباء المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير والأسعار"],
        "invoice_header": "💰 نظام حساب التكاليف والمواد",
        "add_item": "أضف مادة للجدول",
        "total": "الإجمالي العام:"
    }
}

# 5. الواجهة الرئيسية
st.markdown(f"### {texts[L]['title']}")
st.write("---")

choice = st.sidebar.radio("🛠️ الأدوات", texts[L]["menu"])

# --- القسم الأول والثاني (الذكاء الاصطناعي والحاسبة) سيبقيان كما هما ---

# --- القسم الثالث: نظام الفواتير والأسعار (المطور) ---
if choice == texts[L]["menu"][2]:
    st.subheader(texts[L]["invoice_header"])
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🛒 اختيار السلعة")
        selected_product = st.selectbox("اختر المادة:", list(TUNISIA_PRICES.keys()))
        quantity = st.number_input("الكمية:", min_value=1, value=1)
        
        if st.button("إضافة إلى القائمة"):
            if 'cart' not in st.session_state:
                st.session_state.cart = []
            
            price_unit = TUNISIA_PRICES[selected_product]
            subtotal = price_unit * quantity
            st.session_state.cart.append({
                "item": selected_product,
                "qty": quantity,
                "unit": price_unit,
                "total": subtotal
            })
            st.toast("تمت الإضافة!")

    with col2:
        st.markdown("#### 💳 الملخص")
        if 'cart' in st.session_state and len(st.session_state.cart) > 0:
            grand_total = 0
            for i, entry in enumerate(st.session_state.cart):
                st.write(f"{entry['qty']}x {entry['item']} = {entry['total']:.3f} DT")
                grand_total += entry['total']
            
            st.divider()
            st.warning(f"**{texts[L]['total']} {grand_total:.3f} DT**")
            
            if st.button("تفريغ السلة"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.info("السلة فارغة حالياً")

    # توليد التقرير النهائي للتحميل
    if 'cart' in st.session_state and len(st.session_state.cart) > 0:
        st.write("---")
        client_name = st.text_input("اسم الزبون:")
        if st.button("تجهيز فاتورة PDF (نصية)"):
            invoice_txt = f"فاتورة تقديرية - {client_name}\nالتاريخ: {datetime.now()}\n"
            invoice_txt += "-"*30 + "\n"
            for e in st.session_state.cart:
                invoice_txt += f"{e['item']} | الكمية: {e['qty']} | الثمن: {e['total']:.3f} DT\n"
            invoice_txt += "-"*30 + f"\nالمجموع الجملي: {grand_total:.3f} DT"
            
            st.download_button("تحميل الفاتورة", invoice_txt, file_name=f"Devis_{client_name}.txt")
