import streamlit as st
import pandas as pd
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", layout="wide")

# 2. قاعدة البيانات الشاملة للمواد الكهربائية في تونس
# قمت بإضافة الأنواع والمصنعين (Marques) الأكثر تداولاً
DATABASE_MATERIELS = {
    # --- الحماية (Protection) ---
    "Hager: Disjoncteur DPN 10A": 10.500,
    "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800,
    "Hager: Disjoncteur DPN 25A": 11.200,
    "Hager: Interrupteur Différentiel 40A 30mA": 95.000,
    "Hager: Disjoncteur Différentiel 32A": 88.000,
    
    "Schneider: Disjoncteur DPN 16A": 11.500,
    "Schneider: Disjoncteur DPN 20A": 11.500,
    "Schneider: Interrupteur Différentiel 40A": 110.000,
    
    "Chint: Disjoncteur DPN 16A": 6.500,
    "Chint: Disjoncteur DPN 20A": 6.500,
    "Chint: Différentiel 40A": 55.000,
    
    "General: Disjoncteur DPN 16A": 7.800,
    "General: Disjoncteur DPN 20A": 7.800,

    # --- القواطع والبرايز (Appareillage) ---
    "Legrand (Valena): Interrupteur Simple": 8.500,
    "Legrand (Valena): Va et Vient": 9.800,
    "Legrand (Valena): Prise 2P+T": 10.500,
    
    "Générale (Système 45): Interrupteur Simple": 5.200,
    "Générale (Système 45): Va et Vient": 6.800,
    "Générale (Système 45): Prise 2P+T": 7.200,
    "Générale (Système 43): Interrupteur Simple": 4.500,
    
    "Ingellec (Tiziano): Interrupteur Simple": 4.200,
    "Ingellec (Tiziano): Prise 2P+T": 5.800,

    # --- الصناديق والعلب (Coffrets & Boites) ---
    "Hager: Coffret 12 Modules (Encastré)": 45.000,
    "Hager: Coffret 24 Modules (Encastré)": 145.000,
    "Hager: Coffret 36 Modules (Encastré)": 195.000,
    "Générale: Boite Encastrement 3M": 0.850,
    "Générale: Boite Encastrement 4M": 1.250,
    "Générale: Boite Encastrement 6M": 1.850,
    "Boite Dérivation 100x100": 2.200,
    "Boite Dérivation 150x150": 4.500,

    # --- الأسلاك والقنوات (Câbles & Conduits) ---
    "Câble (Tunisie Câbles): 1.5mm² (Rouge/Bleu) 100m": 65.000,
    "Câble (Tunisie Câbles): 2.5mm² (Rouge/Bleu) 100m": 105.000,
    "Câble (Tunisie Câbles): 4mm² 100m": 165.000,
    "Câble (Tunisie Câbles): 6mm² 100m": 240.000,
    "Câble TV (Teleco): Coaxial 100m": 85.000,
    "Câble Réseau: Cat6 UTP (mètre)": 1.500,
    "Tube Orange (ICTA) 16mm (Rouleau)": 35.000,
    "Tube Orange (ICTA) 20mm (Rouleau)": 45.000,
    "Tube Orange (ICTA) 25mm (Rouleau)": 58.000,

    # --- الإضاءة (Eclairage) ---
    "Spot LED 7W (Encastré)": 6.500,
    "Hublot LED 18W (Etanche)": 18.500,
    "Réglette LED 120cm": 15.000,
    "Projecteur LED 50W": 45.000
}

# 3. ذاكرة الجلسة
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 4. واجهة التطبيق
st.sidebar.title("🛠️ منصة الكهربائي")
choice = st.sidebar.radio("الأدوات:", ["نظام الفواتير", "استشارة الخبير", "الحاسبة"])

if choice == "نظام الفواتير":
    st.header("📋 تحرير فاتورة (جميع المواد والمصنعين)")

    # إدخال المواد
    with st.expander("➕ إضافة مادة من قاعدة البيانات", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            # قائمة البحث والفلترة
            search_query = st.text_input("ابحث عن مادة أو مصنع (مثال: Hager أو Prise):")
            filtered_items = [k for k in DATABASE_MATERIELS.keys() if search_query.lower() in k.lower()]
            prod = st.selectbox("اختر المادة:", filtered_items if filtered_items else list(DATABASE_MATERIELS.keys()))
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=DATABASE_MATERIELS[prod], format="%.3f")
        
        if st.button("إضافة للفاتورة ➕", use_container_width=True):
            st.session_state['cart'].append({"المادة": prod, "الكمية": qte, "الثمن": price, "المجموع": qte * price})
            st.rerun()

    # عرض الفاتورة والتحرير
    if st.session_state['cart']:
        df = pd.DataFrame(st.session_state['cart'])
        edited_df = st.data_editor(df, use_container_width=True, key="main_editor", num_rows="dynamic")
        
        # تحديث الحسابات
        edited_df["المجموع"] = edited_df["الكمية"] * edited_df["الثمن"]
        total_final = edited_df["المجموع"].sum()
        
        st.success(f"### المجموع الجملي الصافي: {total_final:.3f} DT")

        # تجهيز النص للتحميل (Word)
        client = st.text_input("اسم الزبون:", "السيد ....................")
        report = f"DEVIS ESTIMATIF\nالزبون: {client}\nتاريخ: {datetime.now().strftime('%d/%m/%Y')}\n" + "="*50 + "\n"
        for i, r in edited_df.iterrows():
            report += f"{i+1}. {r['المادة']} | ك: {r['الكمية']} | س: {r['الثمن']:.3f} | ج: {r['المجموع']:.3f}\n"
        report += "="*50 + f"\nالمجموع الجملي: {total_final:.3f} DT"

        c_del, c_down = st.columns(2)
        with c_del:
            if st.button("🗑️ مسح الكل"):
                st.session_state['cart'] = []
                st.rerun()
        with c_down:
            st.download_button("📥 تحميل الفاتورة للوورد", report.encode('utf-8-sig'), file_name=f"Devis_{client}.txt")
