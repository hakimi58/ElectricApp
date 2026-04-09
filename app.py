import streamlit as st
import pandas as pd
import requests
import json

# 1. الإعدادات الأساسية (مبدأ الأمان والاستقرار)
st.set_page_config(page_title="Pro Electric Platform v28", page_icon="⚡", layout="wide")

# جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 2. الكاتالوج الشامل والمنظم (آخر تحديث)
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

# 3. نظام الترجمة الاحترافي لكل الواجهات
translations = {
    "🇹🇳 العربية/تونسية": {
        "menu": ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 قائمة المواد", "📏 دليل الخراطيم والألوان"],
        "ai_header": "🤖 خبير الكهرباء الذكي", "ai_placeholder": "اسأل بالدارجة التقنية (مثلاً: كيفاش نركب ديفيرونسيال؟)",
        "calc_header": "🧮 حاسبة مقاطع الأسلاك", "inv_header": "📄 تحرير فاتورة شاملة",
        "f_label": "قطر الفورو (مم):", "w_label": "نوع السلك:", "wires": "أسلاك",
        "res_label": "⚠️ السعة القصوى لسحب سهل:", "color_title": "🎨 دليل ألوان الأسلاك",
        "prompt": "أنت خبير كهرباء تونسي محترف جداً. أجب بالدارجة التونسية التقنية مع استعمال مصطلحات الصنايعية.",
        "btn_send": "إرسال 🚀", "add_btn": "إضافة للفاتورة", "total": "المجموع الجملي"
    },
    "🇫🇷 Français": {
        "menu": ["🤖 Consultation AI", "🧮 Calculateur", "📄 Catalogue", "📏 Guide Gaines & Couleurs"],
        "ai_header": "🤖 Expert AI", "ai_placeholder": "Posez votre question technique...",
        "calc_header": "🧮 Calculateur de Section", "inv_header": "📄 Devis Complet",
        "f_label": "Diamètre de gaine (mm):", "w_label": "Type de fil:", "wires": "fils",
        "res_label": "⚠️ Capacité max suggérée:", "color_title": "🎨 Code Couleurs des Fils",
        "prompt": "Tu es un expert électricien senior. Réponds en français technique précis.",
        "btn_send": "Analyser 🚀", "add_btn": "Ajouter au devis", "total": "Total Général"
    },
    "🇺🇸 English": {
        "menu": ["🤖 AI Consultation", "🧮 Calculator", "📄 Catalogue", "📏 Conduit & Color Guide"],
        "ai_header": "🤖 AI Electrical Expert", "ai_placeholder": "Ask your technical question...",
        "calc_header": "🧮 Cable Size Calculator", "inv_header": "📄 Material Quote",
        "f_label": "Conduit Diameter (mm):", "w_label": "Wire Type:", "wires": "wires",
        "res_label": "⚠️ Max capacity suggested:", "color_title": "🎨 Wire Color Codes",
        "prompt": "You are a professional electrical engineer. Provide technical advice in English.",
        "btn_send": "Ask Expert 🚀", "add_btn": "Add to Quote", "total": "Grand Total"
    }
}

# 4. إدارة الحالة واختيار اللغة
selected_lang = st.sidebar.selectbox("🌐 Choose Language / اختر اللغة", list(translations.keys()))
T = translations[selected_lang]
if 'invoice' not in st.session_state: st.session_state['invoice'] = []

choice = st.sidebar.radio("🛠️ الأدوات", T["menu"])

# --- القسم 1: الخبير (نظام المحاولات المتعددة لتفادي أخطاء السيرفر) ---
if choice == T["menu"][0]:
    st.header(T["ai_header"])
    query = st.text_area("", placeholder=T["ai_placeholder"], height=150)
    
    if st.button(T["btn_send"]):
        if query and API_KEY:
            with st.spinner("جاري الاتصال بالخبير..."):
                # محاولة الاتصال بعدة موديلات لضمان الاستجابة
                models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
                success = False
                for model in models:
                    if success: break
                    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={API_KEY}"
                    payload = {"contents": [{"parts": [{"text": f"{T['prompt']} : {query}"}]}]}
                    try:
                        res = requests.post(url, json=payload, timeout=15)
                        if res.status_code == 200:
                            st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
                            success = True
                        elif res.status_code == 429: continue # جرب الموديل التالي إذا كان الأول عليه ضغط
                    except: continue
                if not success:
                    st.error("⚠️ عذراً، سيرفرات جوجل مشغولة حالياً في منطقتك. حاول مرة أخرى بعد قليل.")

# --- القسم 2: الحاسبة ---
elif choice == T["menu"][1]:
    st.header(T["calc_header"])
    watt = st.number_input("Watt:", min_value=0, value=2000)
    amp = watt / 220
    st.metric("Ampère", f"{amp:.2f} A")
    wire = "1.5mm²" if amp <= 11 else "2.5mm²" if amp <= 17 else "4mm² أو أكثر"
    st.info(f"النتيجة المقترحة: {wire}")

# --- القسم 3: الفاتورة الشاملة ---
elif choice == T["menu"][2]:
    st.header(T["inv_header"])
    col1, col2 = st.columns(2)
    with col1:
        cat = st.selectbox("الفئة / Catégorie", list(CATALOGUE.keys()))
        item = st.selectbox("المادة / Article", list(CATALOGUE[cat].keys()))
    with col2:
        qte = st.number_input("الكمية / Qté", min_value=1, value=1)
        if st.button(T["add_btn"]):
            price = CATALOGUE[cat][item]
            st.session_state['invoice'].append({"المادة": item, "الكمية": qte, "المجموع": qte * price})
            st.rerun()

    if st.session_state['invoice']:
        st.table(pd.DataFrame(st.session_state['invoice']))
        total_val = sum(i['المجموع'] for i in st.session_state['invoice'])
        st.markdown(f"### {T['total']}: :green[{total_val:.3f} DT]")
        if st.button("🗑️ Reset"):
            st.session_state['invoice'] = []; st.rerun()

# --- القسم 4: دليل الخراطيم والألوان (مترجم بالكامل) ---
elif choice == T["menu"][3]:
    st.header(T["menu"][3])
    c1, c2 = st.columns(2)
    with c1:
        g_size = st.selectbox(T["f_label"], [11, 13, 16, 20, 25])
        w_type = st.selectbox(T["w_label"], ["1.5 mm²", "2.5 mm²", "4 mm²", "6 mm²"])
        caps = {11: {"1.5 mm²": 3, "2.5 mm²": 2}, 16: {"1.5 mm²": 5, "2.5 mm²": 4, "4 mm²": 3}, 20: {"1.5 mm²": 7, "2.5 mm²": 6, "4 mm²": 5, "6 mm²": 4}}
        max_v = caps.get(g_size, {}).get(w_type, "3-5")
        st.warning(f"{T['res_label']} {max_v} {T['wires']}")
    with c2:
        st.subheader(T["color_title"])
        color_data = "🔵 Neutre\n🔴 Phase\n🟡🟢 Terre" if selected_lang != "🇹🇳 العربية/تونسية" else "🔵 محايد (Neutre)\n🔴 فاز (Phase)\n🟡🟢 أرضي (Terre)"
        st.code(color_data)
