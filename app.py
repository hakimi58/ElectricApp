import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# 1. الإعدادات الأساسية
st.set_page_config(page_title="منصة الكهربائي المحترف v29", page_icon="⚡", layout="wide")
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 2. الكاتالوج الشامل للمواد الكهربائية في تونس
CATALOGUE = {
    "🛠️ التأسيس (Gaines & Boites)": {
        "Foureau Orange 11mm (50m)": 28.500, "Foureau Orange 13mm (50m)": 32.800,
        "Foureau Orange 16mm (50m)": 38.000, "Foureau Orange 20mm (50m)": 48.500,
        "Foureau Noir (Béton) 16mm": 42.000, "Foureau Noir (Béton) 20mm": 52.000,
        "Boite Encastrement 1 Poste": 0.450, "Boite Encastrement 3 Postes": 1.250,
        "Boite Dérivation Carrée 100x100": 2.800
    },
    "🔌 الأسلاك والكابلات (Câbles)": {
        "Tunisie Câbles 1.5mm² (100m)": 65.000, "Tunisie Câbles 2.5mm² (100m)": 105.000,
        "Tunisie Câbles 4mm² (100m)": 165.000, "Tunisie Câbles 6mm² (100m)": 240.000,
        "Câble Racle 4x10mm (1m)": 14.500, "Câble Souple 2x1.5mm (1m)": 2.200
    },
    "📟 لوحة القواطع (Tableau Hager)": {
        "Hager 10A (Eclairage)": 10.500, "Hager 16A (Prise)": 9.800,
        "Hager 20A (Clim/Four)": 9.800, "Différentiel Hager 40A 30mA": 95.000,
        "Coffret Hager 12M": 75.000, "Coffret Hager 24M": 145.000,
        "Peigne Phase/Neutre": 18.000
    },
    "🏠 المفاتيح (Appareillage Valena)": {
        "Prise 2P+T Valena": 11.200, "Interrupteur Simple": 8.500,
        "Va-et-Vient Simple": 10.200, "Bouton Poussoir": 11.500,
        "Plaque Valena 1 Poste": 1.800
    }
}

# 3. نظام الترجمة
translations = {
    "🇹🇳 العربية/تونسية": {
        "menu": ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 قائمة المواد", "📏 دليل الخراطيم والألوان"],
        "total": "المجموع الجملي", "add_btn": "إضافة للفاتورة", "download_btn": "📥 تحميل الفاتورة (Excel/CSV)"
    },
    "🇫🇷 Français": {
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Facture", "📏 Guide"],
        "total": "Total Général", "add_btn": "Ajouter au devis", "download_btn": "📥 Télécharger (Excel/CSV)"
    }
}

selected_lang = st.sidebar.selectbox("🌐 اللغة", list(translations.keys()))
T = translations[selected_lang]
if 'invoice' not in st.session_state: st.session_state['invoice'] = []

choice = st.sidebar.radio("🛠️ الأدوات", T["menu"])

# --- القسم 3: الفاتورة (النسخة 29 الأصلية) ---
if choice == T["menu"][2]:
    st.header(T["menu"][2])
    col1, col2 = st.columns(2)
    with col1:
        cat = st.selectbox("الفئة", list(CATALOGUE.keys()))
        item = st.selectbox("المادة", list(CATALOGUE[cat].keys()))
    with col2:
        qte = st.number_input("الكمية", min_value=1, value=1)
        if st.button(T["add_btn"]):
            st.session_state['invoice'].append({
                "المادة": item, "الكمية": qte, "الثمن": CATALOGUE[cat][item], "المجموع": qte * CATALOGUE[cat][item]
            })
            st.rerun()
            
    if st.session_state['invoice']:
        df = pd.DataFrame(st.session_state['invoice'])
        st.table(df)
        total_val = df["المجموع"].sum()
        st.success(f"{T['total']}: {total_val:.3f} DT")
        
        # ميزة التحميل كـ CSV (الموجودة في النسخة 29)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(label=T["download_btn"], data=csv, file_name=f"Devis_{datetime.now().strftime('%d_%m')}.csv", mime='text/csv')
        
        if st.button("🗑️ Reset"): st.session_state['invoice'] = []; st.rerun()

# --- بقية الأقسام (الخبير، الحاسبة، الدليل) تبقى كما هي في نسختك 29 ---
