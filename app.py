import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="Hakim Boughanmi Électricité", page_icon="⚡", layout="wide")

# تنسيق CSS مخصص ليشبه الفواتير المطبوعة
st.markdown("""
    <style>
    .reportview-container { background: #f0f2f6; }
    .invoice-box { 
        background-color: white; 
        border: 2px solid #2c3e50; 
        padding: 40px; 
        border-radius: 10px; 
        font-family: 'Courier New', Courier, monospace;
    }
    .header-style { color: #2c3e50; border-bottom: 3px solid #f39c12; padding-bottom: 10px; }
    .total-style { font-size: 28px; background-color: #2c3e50; color: #f39c12; padding: 15px; border-radius: 5px; text-align: center; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 2. قاعدة بيانات المواد المستخرجة من ملفك الخاص 
HAKIM_INVENTORY = [
    "Boite encastré 3 M", "Boite encastré 4 M", "Boite encastré 6 M",
    "Coffret 24 module Hager", "Monture 3 modules sys43", "Monture 4 modules sys43",
    "Monture 6 modules sys43", "Boite encastrement PT 5", "Disjoncteur différentiel 32 AMP 2 POLE",
    "Disjoncteur DPN 20 AMP", "Disjoncteur DPN 16 AMP", "Disjoncteur minuterie d’escalier 10 AMP",
    "Disjoncteur DPN 10 AMP 2 POLE", "Répartiteur", "Cable distribution tv SAT",
    "Peigne de connecteur", "Cable réseau Cat 6 - 4 pairs", "Cable téléphone 2 pairs",
    "Interrupteur va et Vien System 43", "Bouche module System 43", "Demi bouche module System 43",
    "Interrupteur simple System 43", "Prise 2p+terre System 43", "Bouton poussoir System 43",
    "Prise SAT System 43", "Prise internet cat 6 System 43", "Domino 50 Barrée",
    "Domino 35 Barrée", "Tolésolon"
]

# 3. القائمة الجانبية (الأدوات)
st.sidebar.image("https://via.placeholder.com/150?text=⚡", width=100) # يمكنك وضع لوغو حقيقي هنا
st.sidebar.markdown("### ⚙️ الإعدادات")
lang = st.sidebar.selectbox("🌐 اللغة", ["🇹🇳 تونسية", "🇫🇷 Français", "🇺🇸 English"])

st.sidebar.write("---")
menu = ["📄 إنشاء فاتورة (Devis)", "🤖 استشارة الخبير AI", "🧮 حاسبة القياسات"]
choice = st.sidebar.radio("🛠️ اختر الأداة:", menu)

# --- القسم الأول: نظام الفواتير المخصص (نموذج المحلات الكبرى) ---
if choice == menu[0]:
    st.markdown('<h2 class="header-style">HAKIM BOUGHANMI - Électricité bâtiment</h2>', unsafe_allow_html=True)
    st.write("📞 **Phone:** 97822678 | 📧 **Email:** hakimboughanmi58@gmail.com")
    
    if 'invoice_items' not in st.session_state: st.session_state.invoice_items = []

    with st.expander("➕ إضافة مادة جديدة للفاتورة", expanded=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1:
            # اختيار المادة من قائمة ملفك 
            selected_item = st.selectbox("Désignation / المادة", HAKIM_INVENTORY)
        with c2:
            qty = st.number_input("Quantité / الكمية", min_value=1, value=1)
        with c3:
            u_price = st.number_input("Prix Unitaire / الثمن (DT)", min_value=0.0, format="%.3f")
        
        if st.button("إضافة للفاتورة"):
            st.session_state.invoice_items.append({
                "Désignation": selected_item,
                "Quantité": qty,
                "Prix Unitaire": u_price,
                "Total (DT)": qty * u_price
            })
            st.rerun()

    # عرض الفاتورة بشكل رسمي
    if st.session_state.invoice_items:
        st.markdown("---")
        st.markdown('<div class="invoice-box">', unsafe_allow_html=True)
        st.write(f"**Date:** {datetime.now().strftime('%d/%m/%Y')}")
        client = st.text_input("اسم الزبون (Client):", "السيد ....................")
        
        df = pd.DataFrame(st.session_state.invoice_items)
        df.index = df.index + 1
        st.table(df)
        
        grand_total = df["Total (DT)"].sum()
        st.markdown(f'<div class="total-style">TOTAL: {grand_total:.3f} DT</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ مسح الفاتورة"):
                st.session_state.invoice_items = []
                st.rerun()
        with col2:
            st.download_button("📥 تحميل الفاتورة (CSV)", df.to_csv(), file_name=f"Facture_{client}.csv")

# --- القسم الثاني والثالث (AI والحاسبة) يظلان بنفس الكفاءة السابقة ---
