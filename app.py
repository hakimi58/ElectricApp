import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة والتنسيق (النسخة 12.0)
st.set_page_config(page_title="Hakim Boughanmi Électricité", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .invoice-box { background-color: #f9f9f9; border: 1px solid #ddd; padding: 25px; border-radius: 10px; font-family: 'Arial'; }
    .total-style { font-size: 26px; color: #27ae60; font-weight: bold; border-top: 2px solid #eee; padding-top: 10px; text-align: center; }
    .stButton>button { width: 100%; border-radius: 5px; }
    .header-info { color: #2c3e50; margin-bottom: 20px; border-bottom: 2px solid #f39c12; padding-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 2. قائمة المواد الخاصة بك (من الملف المرفق) 
HAKIM_MATERIAUX = [
    "Boite encastré 3 M", "Boite encastré 4 M", "Boite encastré 6 M", [cite: 2]
    "Coffret 24 module Hager", "Monture 3 modules sys43", "Monture 4 modules sys43", [cite: 2]
    "Monture 6 modules sys43", "Boite encastrement PT 5", "Disjoncteur différentiel 32 AMP 2 POLE", [cite: 2]
    "Disjoncteur DPN 20 AMP", "Disjoncteur DPN 16 AMP", "Disjoncteur minuterie d’escalier 10 AMP", [cite: 2]
    "Disjoncteur DPN 10 AMP 2 POLE", "Répartiteur", "Cable distribution tv SAT", [cite: 2]
    "Peigne de connecteur", "Cable réseau Cat 6 - 4 pairs", "Cable téléphone 2 pairs", [cite: 2]
    "Interrupteur va et Vien System 43", "Bouche module System 43", "Demi bouche module System 43", [cite: 2]
    "Interrupteur simple System 43", "Prise 2p+terre System 43", "Bouton poussoir System 43", [cite: 2]
    "Prise SAT System 43", "Prise internet cat 6 System 43", "Domino 50 Barrée", [cite: 2]
    "Domino 35 Barrée", "Tolésolon" [cite: 2]
]

# 3. إعدادات اللغة والأدوات
lang_map = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Language", list(lang_map.keys()))
L = lang_map[L_key]

texts = {
    "تونس": {
        "menu": ["🤖 خبير الأعطال (AI)", "🧮 حاسبة القياسات", "📄 نظام الفواتير"],
        "inv_header": "نموذج الفاتورة والتقدير"
    },
    "Français": {
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Facturation Pro"],
        "inv_header": "Modèle de Facture / Devis"
    }
}
curr = texts.get(L, texts["تونس"])

# 4. القائمة الجانبية (نفس تصميم 12.0)
st.sidebar.write("---")
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# بيانات الهوية في الجانب
st.sidebar.markdown(f"""
**HAKIM BOUGHANMI**
📞 97822678
📧 hakimboughanmi58@gmail.com
""")

# --- القسم 1: الخبير (AI) ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    query = st.text_area("اشرح العطل هنا:")
    if st.button("تحليل"):
        # كود الربط بـ Gemini API يوضع هنا كما سبق
        st.info("الخبير جاهز لتحليل استفسارك.")

# --- القسم 2: الحاسبة ---
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    watt = st.number_input("القوة (Watt):", value=2000)
    amp = watt / 220
    st.success(f"التيار: {amp:.2f} أمبير")

# --- القسم 3: الفاتورة المميزة (تعديل 12.0 ببياناتك) ---
elif choice == curr["menu"][2]:
    st.markdown(f"### {curr['inv_header']}")
    
    if 'cart' not in st.session_state: st.session_state.cart = []

    with st.expander("➕ إضافة مواد من قائمتك الخاصة", expanded=True):
        c1, c2, c3 = st.columns([3, 1, 1])
        with c1: prod = st.selectbox("المادة (Désignation)", HAKIM_MATERIAUX) [cite: 2]
        with c2: qte = st.number_input("الكمية", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن الوحدوي", min_value=0.0, format="%.3f")
            if st.button("إضافة"):
                st.session_state.cart.append({"Désignation": prod, "Qty": qte, "Price": price, "Total": qte*price})
                st.rerun()

    if st.session_state.cart:
        st.markdown("---")
        st.markdown('<div class="invoice-box">', unsafe_allow_html=True)
        # رأس الفاتورة الاحترافي
        st.markdown(f"""
        <div class="header-info">
            <h2>HAKIM BOUGHANMI</h2>
            <p>Électricité bâtiment | 📞 97822678</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write(f"**التاريخ:** {datetime.now().strftime('%d/%m/%Y')}")
        client = st.text_input("اسم الزبون:", "....................")
        
        df = pd.DataFrame(st.session_state.cart)
        st.table(df)
        
        grand_total = df["Total"].sum()
        st.markdown(f'<p class="total-style">المجموع الجملي: {grand_total:.3f} DT</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            if st.button("🗑️ مسح الكل"):
                st.session_state.cart = []
                st.rerun()
        with col_f2:
            st.download_button("📥 تحميل الفاتورة", df.to_csv(), file_name=f"Devis_{client}.csv")
