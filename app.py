import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات المواد والأسعار (تلقائية وقابلة للتعديل)
HAKIM_PRICES = {
    "Boite encastré 3 M": 0.850,
    "Boite encastré 4 M": 1.200,
    "Boite encastré 6 M": 1.800,
    "Coffret 24 module Hager": 145.000,
    "Monture 3 modules sys43": 2.400,
    "Monture 4 modules sys43": 3.200,
    "Monture 6 modules sys43": 4.500,
    "Boite encastrement PT 5": 0.650,
    "Disjoncteur différentiel 32A": 85.000,
    "Disjoncteur DPN 20A": 9.500,
    "Disjoncteur DPN 16A": 9.500,
    "Disjoncteur DPN 10A": 10.500,
    "Interrupteur va et Vien Sys43": 6.800,
    "Bouche module Sys43": 1.200,
    "Prise 2p+terre Sys43": 7.500,
    "Cable distribution tv SAT (m)": 1.200,
    "Cable réseau Cat 6 (m)": 1.500,
    "Domino 50": 4.500,
    "Domino 35": 3.200,
    "Tolésolon": 1.500
}

# 3. اختيار اللغة
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Langue", list(lang_options.keys()))
L = lang_options[L_key]

# 4. نصوص الواجهة
texts = {
    "تونس": {
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "إنشاء فاتورة (Devis)"],
        "inv_title": "فاتورة تقديرية / DEVIS",
        "add": "إضافة المادة",
        "total_label": "المجموع الجملي الصافي (TTC):"
    },
    "Français": {
        "menu": ["Consultation AI", "Calculateur", "Créer Devis"],
        "inv_title": "DEVIS ESTIMATIF",
        "add": "Ajouter l'article",
        "total_label": "TOTAL GÉNÉRAL (TTC):"
    }
}
curr = texts.get(L, texts["تونس"])

# 5. القائمة الجانبية
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# القسم 1 و 2 (بدون تغيير)
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    st.write("قسم الذكاء الاصطناعي")
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    st.write("قسم الحاسبة")

# --- القسم 3: نموذج فاتورة المحلات التونسية (التعديل المطلوب) ---
elif choice == curr["menu"][2]:
    st.markdown(f"### 📋 {curr['inv_title']}")
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []

    # إطار إدخال البيانات (مثل الكاسة)
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            prod = st.selectbox("Désignation (المادة):", list(HAKIM_PRICES.keys()))
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=HAKIM_PRICES[prod], format="%.3f")
        
        if st.button(curr["add"], use_container_width=True):
            st.session_state.cart.append({
                "Désignation": prod,
                "Qté": qte,
                "Prix Unitaire": price,
                "Total": qte * price
            })
            st.rerun()

    # شكل الفاتورة النهائي (كما في المحلات)
    if st.session_state.cart:
        st.markdown("""---""")
        # رأس الفاتورة
        col_header1, col_header2 = st.columns(2)
        with col_header1:
            st.write(f"**التاريخ:** {datetime.now().strftime('%d/%m/%Y')}")
        with col_header2:
            client = st.text_input("اسم الزبون:", "السيد ....................")

        # جدول المواد (Tableau)
        st.markdown("#### قائمة المواد:")
        
        # إنشاء جدول حقيقي باستخدام Dataframe لتسهيل العرض
        df = pd.DataFrame(st.session_state.cart)
        df.index += 1  # ليبدأ الترقيم من 1
        
        # عرض الجدول بشكل احترافي
        st.table(df)

        # خلاصة الفاتورة في الأسفل
        total_sum = sum(it["Total"] for it in st.session_state.cart)
        
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 20px; border: 2px solid #dee2e6; border-radius: 10px; text-align: center;">
            <h2 style="margin: 0; color: #28a745;">{curr['total_label']} {total_sum:.3f} DT</h2>
        </div>
        """, unsafe_allow_html=True)

        # أزرار التحكم
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            if st.button("🗑️ مسح الفاتورة"):
                st.session_state.cart = []
                st.rerun()
        with col_f2:
             # زر تحميل بصيغة CSV أو نص (مؤقتاً)
             st.download_button("📥 تحميل الفاتورة", df.to_csv(), file_name=f"Devis_{client}.csv")
        with col_f3:
            st.write("إمضاء الفني: ............ ")
