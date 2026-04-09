import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. قاعدة البيانات الشاملة (مع الفورو والمواد التونسية)
DATABASE_PRO = {
    "Foureau Orange 11mm (Rouleau)": 28.500, "Foureau Orange 13mm (Rouleau)": 32.800,
    "Foureau Orange 16mm (Rouleau)": 38.000, "Foureau Orange 20mm (Rouleau)": 48.500,
    "Hager: Disjoncteur DPN 10A": 10.500, "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800, "Hager: Différentiel 40A 30mA": 95.000,
    "Hager: Coffret Encastré 24M": 145.000, "Legrand Valena: Prise 2P+T": 11.200,
    "Tunisie Câbles: 1.5mm² (100m)": 65.000, "Tunisie Câbles: 2.5mm² (100m)": 105.000,
    "Générale: Boite Encastrement 3M": 0.900, "Spot LED 7W Encastré": 6.800
}

# 3. ذاكرة الجلسة
if 'cart' not in st.session_state:
    st.session_state['cart'] = []

# 4. نظام اللغات والمفتاح السري
lang_options = {"🇹🇳 تونسية": "تونس", "🇫🇷 Français": "Français", "🇺🇸 English": "English"}
L_key = st.sidebar.selectbox("🌐 اللغة", list(lang_options.keys()))
L = lang_options[L_key]

# جلب المفتاح السري من الإعدادات
API_KEY = st.secrets.get("GOOGLE_API_KEY")

texts = {
    "تونس": {
        "title": "⚡ منصة الكهربائي المحترف",
        "menu": ["استشارة الخبير (AI)", "حاسبة القياسات", "نظام الفواتير"],
        "ai_label": "اشرح المشكلة هنا (بالدارجة):",
        "calc_label": "قوة الجهاز (Watt):",
        "inv_header": "📄 إنشاء فاتورة (Devis)",
        "prompt": "أنت خبير كهرباء تونسي محترف، أجب بالدارجة التونسية التقنية وبسرعة."
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

# 5. القائمة الجانبية
st.markdown(f"### {curr['title']}")
st.write("---")
choice = st.sidebar.radio("🛠️ الأدوات", curr["menu"])

# --- القسم 1: استشارة الخبير (إصلاح الاتصال) ---
if choice == curr["menu"][0]:
    st.subheader(curr["menu"][0])
    query = st.text_area(curr["ai_label"], height=120, placeholder="مثلاً: عندي بريز يتحرق ديما، شنوة السبب؟")
    
    if st.button("تحليل السؤال 🤖"):
        if not API_KEY:
            st.error("❌ خطأ: مفتاح API غير موجود في إعدادات Secrets.")
        elif query:
            with st.spinner("الخبير يفكر..."):
                try:
                    # رابط Google Gemini API
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                    payload = {"contents": [{"parts": [{"text": f"{curr['prompt']} : {query}"}]}]}
                    response = requests.post(url, json=payload, timeout=10)
                    
                    if response.status_code == 200:
                        result = response.json()
                        answer = result['candidates'][0]['content']['parts'][0]['text']
                        st.info(answer)
                    else:
                        st.error(f"خطأ في الرد من جوجل (كود {response.status_code}). تأكد من صحة المفتاح.")
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {str(e)}")
        else:
            st.warning("الرجاء كتابة سؤال أولاً.")

# --- القسم 2: حاسبة القياسات ---
elif choice == curr["menu"][1]:
    st.subheader(curr["menu"][1])
    watt = st.number_input(curr["calc_label"], value=2000)
    amp = watt / 220
    wire = "1.5 مم²" if amp <= 11 else "2.5 مم²" if amp <= 17 else "4 مم²+"
    st.success(f"التيار: {amp:.2f} A | السلك المناسب: {wire}")

# --- القسم 3: نظام الفواتير (المطور والمؤمن) ---
elif choice == curr["menu"][2]:
    st.subheader(curr["inv_header"])
    
    with st.expander("➕ إضافة مادة (بحث سريع)", expanded=True):
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search = st.text_input("🔍 اكتب اسم المادة (مثلاً: Foureau):")
            filtered = [k for k in DATABASE_PRO.keys() if search.lower() in k.lower()]
            prod = st.selectbox("المادة:", filtered if filtered else list(DATABASE_PRO.keys()))
        with c2:
            qte = st.number_input("الكمية:", min_value=1, value=1)
        with c3:
            price = st.number_input("الثمن (DT):", min_value=0.0, value=DATABASE_PRO[prod], format="%.3f")
        
        if st.button("إضافة ➕", use_container_width=True):
            st.session_state['cart'].append({"المادة": prod, "الكمية": qte, "الثمن": price, "المجموع": qte * price})
            st.rerun()

    if st.session_state['cart']:
        st.write("---")
        df = pd.DataFrame(st.session_state['cart'])
        edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic", key="editor_v8_final")
        
        edited_df["المجموع"] = edited_df["الكمية"] * edited_df["الثمن"]
        total_final = edited_df["المجموع"].sum()
        st.markdown(f"### المجموع الجملي: :green[{total_final:.3f} DT]")

        if st.button("🗑️ مسح الفاتورة"):
            st.session_state['cart'] = []
            st.rerun()
