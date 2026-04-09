import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة (النسخة 8 المعتمدة)
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة بيانات المواد والمصنعين (الموسوعة التونسية)
DATABASE_MATERIELS = {
    "Hager: Disjoncteur DPN 10A": 10.500, "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800, "Hager: Disjoncteur Diff 32A": 88.000,
    "Hager: Coffret 24M": 145.000, "Legrand: Interrupteur Simple": 8.500,
    "Legrand: Va et Vient": 9.800, "Legrand: Prise 2P+T": 10.500,
    "Générale: Boite 3M": 0.850, "Générale: Boite 4M": 1.250,
    "Tunisie Câbles: 1.5mm² 100m": 65.000, "Tunisie Câbles: 2.5mm² 100m": 105.000,
    "Tube Orange ICTA 20mm": 45.000, "Spot LED 7W": 6.500
}

# 3. ذاكرة الجلسة للفاتورة
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 4. نظام اللغات (رجوع أداة تغيير اللغة)
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة / Langue", list(lang_options.keys()))
L = lang_options[L_key]

# 5. جلب المفتاح السري للذكاء الاصطناعي
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 6. قاموس النصوص (النسخة 8)
texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"],
        "ai_label": "اشرح المشكلة هنا:",
        "calc_label": "قوة الجهاز (Watt):",
        "inv_header": "📄 إنشاء فاتورة (Devis)",
        "prompt": "أنت خبير كهرباء تونسي، أجب بالدارجة التونسية التقنية."
    },
    "Français": {
        "title": "⚡ Pro Electric Platform",
        "menu": ["Consultation AI", "Calculateur", "Système de Facture"],
        "ai_label": "Décrivez le problème :",
        "calc_label": "Puissance (Watt) :",
        "inv_header": "📄 Créer un Devis",
        "prompt": "Tu es un expert électricien. Réponds en français technique."
    }
}
curr = texts.get(L, texts["تونس"])

# 7. الواجهة والقائمة الجانبية
st.markdown(f"### {curr['title']}")
st.write("---")
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- القسم الأول: استشارة الخبير (إصلاح الخبير) ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    query = st.text_area(curr["ai_label"], height=100)
    if st.button("تحليل"):
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"{curr['prompt']} : {query}"}]}]}
            try:
                res = requests.post(url, json=payload)
                answer = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.info(answer)
            except:
                st.error("خطأ في الاتصال بالخبير.")

# --- القسم الثاني: حاسبة القياسات (إصلاح الحاسبة) ---
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    watt = st.number_input(curr["calc_label"], value=2000)
    amp = watt / 220
    wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
    st.success(f"التيار: {amp:.2f} A | السلك المناسب: {wire}")

# --- القسم الثالث: نظام الفواتير (التطوير الجديد داخل النسخة 8) ---
elif choice == curr["menu"][2]:
    st.subheader(curr["inv_header"])
    
    with st.expander("➕ إضافة مادة (Hager, Legrand, etc.)", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search = st.text_input("بحث سريع:")
            filtered = [k for k in DATABASE_MATERIELS.keys() if search.lower() in k.lower()]
            prod = st.selectbox("المادة:", filtered if filtered else list(DATABASE_MATERIELS.keys()))
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=DATABASE_MATERIELS[prod], format="%.3f")
        
        if st.button("إضافة للفاتورة ➕"):
            st.session_state['cart'].append({"المادة": prod, "الكمية": qte, "الثمن": price, "المجموع": qte * price})
            st.rerun()

    if st.session_state['cart']:
        st.write("---")
        df = pd.DataFrame(st.session_state['cart'])
        # جدول تفاعلي قابل للتعديل
        edited_df = st.data_editor(df, use_container_width=True, key="inv_edit", num_rows="dynamic")
        
        edited_df["المجموع"] = edited_df["الكمية"] * edited_df["الثمن"]
        total_final = edited_df["المجموع"].sum()
        st.success(f"### المجموع الجملي: {total_final:.3f} DT")

        # زر التحميل بصيغة نصية واضحة للوورد
        report = f"DEVIS\nتاريخ: {datetime.now().strftime('%d/%m/%Y')}\n" + "-"*30 + "\n"
        for i, r in edited_df.iterrows():
            report += f"{r['المادة']} | ك: {r['الكمية']} | ج: {r['المجموع']:.3f}\n"
        report += "-"*30 + f"\nالمجموع: {total_final:.3f} DT"
        
        if st.button("🗑️ مسح الكل"):
            st.session_state['cart'] = []
            st.rerun()
        st.download_button("📥 تحميل الفاتورة للوورد", report.encode('utf-8-sig'), file_name="devis_hkim.txt")
