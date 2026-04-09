import streamlit as st
import pandas as pd
from datetime import datetime
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="Pro Electric Platform", layout="wide")
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 2. الكاتالوج (تأكد من وجود الكاتالوج الكامل الذي وضعناه سابقاً)
CATALOGUE = {
    "🛠️ التأسيس": {"Foureau 16mm": 38.000, "Boite Encastrement": 0.450},
    "🔌 الكابلات": {"Câble 1.5mm": 65.000, "Câble 2.5mm": 105.000},
    "📟 الطابلو": {"Hager 16A": 9.800, "Diff 40A": 95.000}
}

if 'invoice' not in st.session_state: st.session_state['invoice'] = []

# 3. واجهة الفاتورة
st.header("📄 تحرير واستخراج الفاتورة")

col1, col2 = st.columns(2)
with col1:
    cat = st.selectbox("الفئة", list(CATALOGUE.keys()))
    item = st.selectbox("المادة", list(CATALOGUE[cat].keys()))
with col2:
    qte = st.number_input("الكمية", min_value=1, value=1)
    if st.button("إضافة للمسودة ➕"):
        price = CATALOGUE[cat][item]
        st.session_state['invoice'].append({
            "Désignation": item,
            "Qté": qte,
            "Prix Unitaire": price,
            "Total HT": qte * price
        })
        st.rerun()

if st.session_state['invoice']:
    df = pd.DataFrame(st.session_state['invoice'])
    st.table(df)
    total_ttc = df["Total HT"].sum()
    st.markdown(f"### المجموع الجملي: :green[{total_ttc:.3f} DT]")

    st.write("---")
    st.subheader("📥 خيارات التحميل الاحترافية")

    # --- الخيار 1: تحميل ملف Excel (يفتح في Word أيضاً) ---
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Devis')
        # إضافة المجموع في الملف
        workbook  = writer.book
        worksheet = writer.sheets['Devis']
        worksheet.write(len(df) + 1, 2, "TOTAL")
        worksheet.write(len(df) + 1, 3, total_ttc)
        
    st.download_button(
        label="📥 تحميل كملف Excel (للكمبيوتر والطباعة)",
        data=buffer.getvalue(),
        file_name=f"Devis_{datetime.now().strftime('%d_%m_%Y')}.xlsx",
        mime="application/vnd.ms-excel"
    )

    # --- الخيار 2: نسخة نصية احترافية (للوورد والواتساب) ---
    devis_text = f"⚡ فاتورة كهرباء تقديرية ⚡\n"
    devis_text += f"التاريخ: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    devis_text += "-"*30 + "\n"
    for i, row in df.iterrows():
        devis_text += f"{row['Désignation']} | {row['Qté']} x {row['Prix Unitaire']:.3f} = {row['Total HT']:.3f} DT\n"
    devis_text += "-"*30 + "\n"
    devis_text += f"المجموع الجملي: {total_ttc:.3f} DT\n"
    devis_text += "شكراً لثقتكم!"

    st.download_button(
        label="📄 تحميل نسخة وورد نصية (.doc)",
        data=devis_text,
        file_name="Devis_Pro.doc",
        mime="application/msword"
    )

    if st.button("🗑️ مسح الفاتورة"):
        st.session_state['invoice'] = []; st.rerun()
