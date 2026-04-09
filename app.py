import streamlit as st
import pandas as pd
import requests

# 1. الإعدادات الأساسية
st.set_page_config(page_title="Pro Electric v29", page_icon="⚡", layout="wide")
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 2. الكاتالوج (مختصر هنا للسرعة، ابقِ النسخة الكاملة عندك)
CATALOGUE = {
    "🛠️ التأسيس": {"Foureau 16mm": 38.000, "Boite Encastrement": 0.450},
    "🔌 الكابلات": {"Câble 1.5mm": 65.000, "Câble 2.5mm": 105.000},
    "📟 الطابلو": {"Hager 16A": 9.800, "Diff 40A": 95.000}
}

# 3. الترجمة
translations = {
    "🇹🇳 العربية/تونسية": {
        "menu": ["🤖 الخبير", "🧮 الحاسبة", "📄 الفاتورة", "📏 الخراطيم"],
        "inv_header": "📄 تحرير وتحميل الفاتورة",
        "download_csv": "📥 تحميل الفاتورة (Excel/CSV)",
        "download_txt": "📄 حفظ كملف نصي (للإرسال)",
        "total": "المجموع الجملي"
    },
    "🇫🇷 Français": {
        "menu": ["🤖 AI", "🧮 Calc", "📄 Facture", "📏 Gaines"],
        "inv_header": "📄 Créer et Télécharger le Devis",
        "download_csv": "📥 Télécharger (Excel/CSV)",
        "download_txt": "📄 Sauvegarder (Texte)",
        "total": "Total Général"
    }
}

selected_lang = st.sidebar.selectbox("🌐 اللغة", list(translations.keys()))
T = translations[selected_lang]
if 'invoice' not in st.session_state: st.session_state['invoice'] = []

choice = st.sidebar.radio("🛠️", T["menu"])

# --- قسم الفاتورة المطور (التحميل والحفظ) ---
if choice == T["menu"][2]:
    st.header(T["inv_header"])
    
    col1, col2 = st.columns(2)
    with col1:
        cat = st.selectbox("الفئة", list(CATALOGUE.keys()))
        item = st.selectbox("المادة", list(CATALOGUE[cat].keys()))
    with col2:
        qte = st.number_input("الكمية", min_value=1, value=1)
        if st.button("إضافة ➕"):
            price = CATALOGUE[cat][item]
            st.session_state['invoice'].append({"المادة/Article": item, "الكمية/Qty": qte, "الثمن/Price": price, "المجموع/Total": qte * price})
            st.rerun()

    if st.session_state['invoice']:
        st.write("---")
        df = pd.DataFrame(st.session_state['invoice'])
        st.table(df)
        
        total_val = df["المجموع/Total"].sum()
        st.markdown(f"### {T['total']}: :green[{total_val:.3f} DT]")
        
        # --- أزرار التحميل الجديدة ---
        st.write("### 💾 خيارات الحفظ والتحميل:")
        
        # 1. التحميل كـ CSV (يفتح في Excel)
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label=T["download_csv"],
            data=csv,
            file_name=f"Devis_Electricite_{datetime.now().strftime('%d_%m_%Y')}.csv",
            mime='text/csv',
        )
        
        # 2. التحميل كملف نصي بسيط (سهل للإرسال في الواتساب أو الإيميل)
        txt_content = f"--- Devis Électrique ---\nDate: {datetime.now()}\n\n"
        for i, row in df.iterrows():
            txt_content += f"- {row['المادة/Article']} x{row['الكمية/Qty']}: {row['المجموع/Total']:.3f} DT\n"
        txt_content += f"\nTotal: {total_val:.3f} DT"
        
        st.download_button(
            label=T["download_txt"],
            data=txt_content,
            file_name="Devis.txt",
            mime='text/plain',
        )

        if st.button("🗑️ مسح الكل"):
            st.session_state['invoice'] = []
            st.rerun()
