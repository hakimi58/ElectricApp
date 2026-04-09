import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة البيانات الشاملة للمواد الكهربائية في تونس
DATABASE_PRO = {
    # الفورو (Foureaux)
    "Foureau Orange 11mm (Rouleau)": 28.500,
    "Foureau Orange 13mm (Rouleau)": 32.800,
    "Foureau Orange 16mm (Rouleau)": 38.000,
    "Foureau Orange 20mm (Rouleau)": 48.500,
    "Foureau Noir (Béton) 16mm": 42.000,
    "Foureau Noir (Béton) 20mm": 52.000,
    
    # الحماية (Hager)
    "Hager: Disjoncteur DPN 10A": 10.500,
    "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800,
    "Hager: Disjoncteur DPN 32A": 12.800,
    "Hager: Différentiel 40A 30mA": 95.000,
    "Hager: Coffret Encastré 12M": 48.000,
    "Hager: Coffret Encastré 24M": 145.000,
    
    # الحماية (ماركات أخرى)
    "Schneider: Disjoncteur DPN 16A": 12.500,
    "Chint: Disjoncteur DPN 16A": 6.800,
    "Vynckier: Disjoncteur DPN 16A": 8.500,

    # الأجهزة (Legrand Valena)
    "Legrand Valena: Interrupteur Simple": 8.800,
    "Legrand Valena: Va et Vient": 10.500,
    "Legrand Valena: Prise 2P+T": 11.200,
    
    # الأجهزة (Générale)
    "Générale Sys45: Interrupteur Simple": 5.500,
    "Générale Sys45: Va et Vient": 6.800,
    "Générale Sys45: Prise 2P+T": 7.500,
    "Générale: Boite Encastrement 3M": 0.900,
    "Générale: Boite Encastrement 4M": 1.300,
    "Générale: Boite Encastrement 6M": 1.950,

    # الأسلاك (Tunisie Câbles)
    "Tunisie Câbles: 1.5mm² (100m)": 65.000,
    "Tunisie Câbles: 2.5mm² (100m)": 105.000,
    "Tunisie Câbles: 4mm² (100m)": 165.000,
    "Tunisie Câbles: 6mm² (100m)": 240.000,

    # الإضاءة
    "Spot LED 7W Encastré": 6.800,
    "Hublot LED 18W Etanche": 19.500,
    "Projecteur LED 50W": 42.000
}

# 3. ذاكرة الجلسة
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 4. نظام اللغات
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_options.keys()))
L = lang_options[L_key]
API_KEY = st.secrets.get("GOOGLE_API_KEY")

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

# 5. الواجهة الرئيسية
st.markdown(f"### {curr['title']}")
st.write("---")
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- القسم 1: استشارة الخبير ---
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

# --- القسم 2: حاسبة القياسات ---
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    watt = st.number_input(curr["calc_label"], value=2000)
    amp = watt / 220
    wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
    st.success(f"التيار المقدر: {amp:.2f} A | السلك المناسب: {wire}")

# --- القسم 3: نظام الفواتير ---
elif choice == curr["menu"][2]:
    st.subheader(curr["inv_header"])
    
    with st.expander("➕ إضافة مادة", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search = st.text_input("🔍 بحث سريع عن المادة:")
            filtered = [k for k in DATABASE_PRO.keys() if search.lower() in k.lower()]
            prod = st.selectbox("اختر المادة:", filtered if filtered else list(DATABASE_PRO.keys()))
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=DATABASE_PRO[prod], format="%.3f")
        
        if st.button("إضافة للفاتورة ➕", use_container_width=True):
            st.session_state['cart'].append({"المادة": prod, "الكمية": qte, "الثمن": price, "المجموع": qte * price})
            st.rerun()

    if st.session_state['cart']:
        st.write("---")
        df = pd.DataFrame(st.session_state['cart'])
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="editor_final_fix")
        
        edited_df["المجموع"] = edited_df["الكمية"] * edited_df["الثمن"]
        total_final = edited_df["المجموع"].sum()
        st.markdown(f"### المجموع الجملي الصافي: :green[{total_final:.3f} DT]")

        report = f"DEVIS ESTIMATIF\nتاريخ: {datetime.now().strftime('%d/%m/%Y')}\n" + "="*40 + "\n"
        for i, r in edited_df.iterrows():
            report += f"{r['المادة']} | ك: {r['الكمية']} | ج: {r['المجموع']:.3f}\n"
        report += "="*40 + f"\nالمجموع الجملي: {total_final:.3f} DT"

        cdel, cdown = st.columns(2)
        with cdel:
            if st.button("🗑️ مسح الكل"):
                st.session_state['cart'] = []
                st.rerun()
        with cdown:
            st.download_button("📥 تحميل للوورد", report.encode('utf-8-sig'), file_name="devis_hkim.txt")
