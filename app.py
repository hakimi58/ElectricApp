import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة البيانات الكبرى للمواد الكهربائية في تونس (Électricité de Bâtiment)
# تشمل جميع الماركات والأسعار التقريبية بالدينار التونسي
DATABASE_PRO = {
    # --- قسم الحماية (Protection & Coupure) ---
    "Hager: Disjoncteur DPN 10A": 10.500, "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800, "Hager: Disjoncteur DPN 25A": 11.500,
    "Hager: Disjoncteur DPN 32A": 12.800, "Hager: Différentiel 40A 30mA": 95.000,
    "Schneider: Disjoncteur DPN 16A": 12.500, "Schneider: Disjoncteur DPN 20A": 12.500,
    "Schneider: Différentiel 40A 30mA": 115.000, "Chint: Disjoncteur DPN 16A": 6.800,
    "Chint: Disjoncteur DPN 20A": 6.800, "Chint: Différentiel 40A": 58.000,
    "Vynckier: Disjoncteur DPN 16A": 8.500, "General: Disjoncteur DPN 16A": 7.500,
    
    # --- قسم البرايز والقواطع (Appareillage) ---
    "Legrand Valena: Interrupteur Simple": 8.800, "Legrand Valena: Va et Vient": 10.500,
    "Legrand Valena: Prise 2P+T": 11.200, "Legrand Valena: Bouton Poussoir": 12.000,
    "Legrand Valena: Prise TV": 15.500, "Legrand Valena: Prise RJ45": 22.000,
    "Générale Sys45: Interrupteur Simple": 5.500, "Générale Sys45: Va et Vient": 6.800,
    "Générale Sys45: Prise 2P+T": 7.500, "Générale Sys43: Interrupteur Simple": 4.500,
    "Ingellec Tiziano: Interrupteur Simple": 4.500, "Ingellec Tiziano: Prise 2P+T": 5.800,

    # --- قسم الأسلاك والقنوات (Câbles & Conduits) ---
    "Tunisie Câbles: 1.5mm² (Rouleau 100m)": 65.000, "Tunisie Câbles: 2.5mm² (Rouleau 100m)": 105.000,
    "Tunisie Câbles: 4mm² (Rouleau 100m)": 165.000, "Tunisie Câbles: 6mm² (Rouleau 100m)": 240.000,
    "Câble TV Teleco: (Rouleau 100m)": 88.000, "Câble Réseau Cat6: (Mètre)": 1.600,
    "Tube Orange ICTA 16mm (Rouleau)": 38.000, "Tube Orange ICTA 20mm (Rouleau)": 48.000,
    "Tube Orange ICTA 25mm (Rouleau)": 62.000, "Tube Noir 16mm (Barre 3m)": 2.500,

    # --- قسم الصناديق والعلب (Coffrets & Boites) ---
    "Hager: Coffret Encastré 12M": 48.000, "Hager: Coffret Encastré 24M": 148.000,
    "Hager: Coffret Encastré 36M": 198.000, "Générale: Boite Encastrement 3M": 0.900,
    "Générale: Boite Encastrement 4M": 1.300, "Générale: Boite Encastrement 6M": 1.950,
    "Boite Dérivation 100x100": 2.400, "Boite Dérivation 150x150": 4.800, "Boite Dérivation 200x200": 8.500,

    # --- قسم الإضاءة (Luminaires) ---
    "Spot LED 7W Encastré": 6.800, "Hublot LED 18W Etanche": 19.500, 
    "Réglette LED 120cm": 14.500, "Projecteur LED 50W": 42.000,
    "Panneau LED 60x60 (48W)": 55.000
}

# 3. ذاكرة الجلسة
if 'cart' not in st.session_state: st.session_state['cart'] = []

# 4. نظام اللغات (النسخة 8 الأصلية)
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_options.keys()))
L = lang_options[L_key]
API_KEY = st.secrets.get("GOOGLE_API_KEY")

texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"],
        "ai_label": "اشرح المشكلة هنا:", "calc_label": "قوة الجهاز (Watt):",
        "inv_header": "📄 إنشاء فاتورة (Devis)", "prompt": "أنت خبير كهرباء تونسي، أجب بالدارجة التونسية."
    },
    "Français": {
        "title": "⚡ Pro Electric Platform",
        "menu": ["Consultation AI", "Calculateur", "Système de Facture"],
        "ai_label": "Décrivez le problème :", "calc_label": "Puissance (Watt) :",
        "inv_header": "📄 Créer un Devis", "prompt": "Tu es un expert électricien en français."
    }
}
curr = texts.get(L, texts["تونس"])

# 5. القائمة الجانبية والأدوات
st.markdown(f"### {curr['title']}")
st.write("---")
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- القسم الأول: الخبير ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    query = st.text_area(curr["ai_label"])
    if st.button("تحليل"):
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"{curr['prompt']} : {query}"}]}]}
            try:
                res = requests.post(url, json=payload); answer = res.json()['candidates'][0]['content']['parts'][0]['text']
                st.info(answer)
            except: st.error("خطأ في الاتصال.")

# --- القسم الثاني: الحاسبة ---
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    watt = st.number_input(curr["calc_label"], value=2000)
    amp = watt / 220
    wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
    st.success(f"التيار: {amp:.2f} A | السلك المناسب: {wire}")

# --- القسم الثالث: الفاتورة (كاملة مع نظام البحث) ---
elif choice == curr["menu"][2]:
    st.subheader(curr["inv_header"])
    
    with st.expander("➕ إضافة مادة (Hager, Legrand, Tunisie Câbles...)", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search = st.text_input("🔍 ابحث عن المادة أو الماركة (مثال: Legrand):")
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
        df = pd.DataFrame(st.session_state['cart'])
        # جدول احترافي قابل للتعديل
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="editor_v8")
        
        edited_df["المجموع"] = edited_df["الكمية"] * edited_df["الثمن"]
        total_final = edited_df["المجموع"].sum()
        st.markdown(f"### المجموع الجملي الصافي: :green[{total_final:.3f} DT]")

        # خيارات الحفظ والتحميل للوورد
        report = f"DEVIS ESTIMATIF\nتاريخ: {datetime.now().strftime('%d/%m/%Y')}\n" + "-"*40 + "\n"
        for i, r in edited_df.iterrows():
            report += f"{r['المادة']} | ك: {r['الكمية']} | ج: {r['المجموع']:.3f}\n"
        report += "-"*40 + f"\nالمجموع: {total_final:.3f} DT"

        c_del, c_down = st.columns(2)
        with c_del:
            if st.button("🗑️ مسح الكل"): st.session_state['cart'] = []; st.rerun()
        with c_down:
            st.download_button("📥 تحميل للوورد (Word)", report.encode('utf-8-sig'), file_name="devis.txt")
