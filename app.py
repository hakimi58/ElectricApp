import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Hakim Boughanmi Électricité", page_icon="⚡", layout="wide")

# تنسيق CSS احترافي يتماشى مع لوغو الكهرباء
st.markdown("""
    <style>
    .header-box { background-color: #f8f9fa; border-left: 5px solid #0077b6; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
    .invoice-card { background-color: white; border: 1px solid #ddd; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .total-banner { background-color: #f39c12; color: white; padding: 15px; border-radius: 8px; text-align: center; font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. قاعدة بيانات المواد (مستخرجة من ملفك الخاص)
# ملاحظة: يمكنك إضافة الأسعار التقريبية هنا لاحقاً
HAKIM_MATERIAUX = [
    "Boite encastré 3 M", "Boite encastré 4 M", "Boite encastré 6 M",
    "Coffret 24 module Hager", "Monture 3 modules sys43", "Monture 4 modules sys43",
    "Monture 6 modules sys43", "Boite encastrement PT 5", "Disjoncteur différentiel 32A 2P",
    "Disjoncteur DPN 20 AMP", "Disjoncteur DPN 16 AMP", "Minuterie d'escalier 10A",
    "Disjoncteur DPN 10A 2P", "Répartiteur", "Cable distribution tv SAT",
    "Peigne de connecteur", "Cable réseau Cat 6", "Cable téléphone 2 pairs",
    "Interrupteur va et Vien Sys43", "Bouche module Sys43", "Interrupteur simple Sys43",
    "Prise 2p+terre Sys43", "Bouton poussoir Sys43", "Prise SAT Sys43",
    "Prise internet cat 6 Sys43", "Domino 50", "Domino 35", "Tolésolon"
]

# 3. واجهة الهوية (Header)
st.markdown(f"""
<div class="header-box">
    <h2 style="color:#0077b6; margin:0;">HAKIM BOUGHANMI</h2>
    <p style="margin:5px 0;"><b>Électricité bâtiment</b></p>
    <p style="margin:0;">📞 Phone: 97822678 | 📧 E-mail: hakimboughanmi58@gmail.com</p>
</div>
""", unsafe_allow_html=True)

# 4. نظام الفواتير
if 'cart' not in st.session_state: st.session_state.cart = []

tab1, tab2 = st.tabs(["📝 إنشاء فاتورة", "🤖 خبير الأعطال (AI)"])

with tab1:
    st.subheader("إضافة السلعة من القائمة")
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        prod = st.selectbox("المادة (Désignation):", HAKIM_MATERIAUX)
    with c2:
        qte = st.number_input("الكمية (Quantité):", min_value=1, value=1)
    with c3:
        price = st.number_input("السعر الوحدوي (DT):", min_value=0.0, step=0.5)
    
    if st.button("➕ إضافة للفاتورة"):
        st.session_state.cart.append({
            "Désignation": prod,
            "Quantité": qte,
            "Prix Unitaire": f"{price:.3f}",
            "Total": price * qte
        })
        st.success("تمت الإضافة")

    if st.session_state.cart:
        st.write("---")
        st.markdown('<div class="invoice-card">', unsafe_allow_html=True)
        st.markdown(f"<h4>DEVIS / FACTURE</h4>", unsafe_allow_html=True)
        st.write(f"**Date:** {datetime.now().strftime('%d/%m/%Y')}")
        st.write(f"**Client:** {st.text_input('اسم الزبون:', '....................')}")
        
        df = pd.DataFrame(st.session_state.cart)
        st.table(df)
        
        grand_total = sum(item['Total'] for item in st.session_state.cart)
        st.markdown(f'<div class="total-banner">TOTAL: {grand_total:.3f} DT</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🗑️ مسح الفاتورة"):
            st.session_state.cart = []
            st.rerun()

with tab2:
    st.info("هنا يمكنك استشارة الذكاء الاصطناعي في أي عطل كهربائي تواجهه.")
    # كود الـ AI يوضع هنا كما فعلنا سابقاً
