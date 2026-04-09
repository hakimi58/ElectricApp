import streamlit as st
import pandas as pd
from datetime import datetime
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", page_icon="⚡", layout="wide")

# 2. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة بيانات المواد التونسية (الأسعار تقديرية بالدينار)
DB_MATERIELS = {
    "Foureau Orange 11mm (Rouleau)": 28.500,
    "Foureau Orange 13mm (Rouleau)": 32.800,
    "Foureau Orange 16mm (Rouleau)": 38.000,
    "Foureau Orange 20mm (Rouleau)": 48.500,
    "Foureau Noir (Béton) 16mm": 42.000,
    "Hager: Disjoncteur DPN 10A": 10.500,
    "Hager: Disjoncteur DPN 16A": 9.800,
    "Hager: Disjoncteur DPN 20A": 9.800,
    "Hager: Différentiel 40A 30mA": 95.000,
    "Hager: Coffret Encastré 24M": 145.000,
    "Tunisie Câbles: 1.5mm² (100m)": 65.000,
    "Tunisie Câbles: 2.5mm² (100m)": 105.000,
    "Legrand Valena: Prise 2P+T": 11.200,
    "Générale: Boite Encastrement 3M": 0.900,
    "Spot LED 7W Encastré": 6.800
}

# 4. ذاكرة الجلسة للفاتورة
if 'invoice_items' not in st.session_state:
    st.session_state['invoice_items'] = []

# 5. القائمة الجانبية (Sidebar)
st.sidebar.title("🛠️ لوحة التحكم")
lang = st.sidebar.selectbox("🌐 اللغة", ["🇹🇳 تونسية", "🇫🇷 Français"])
choice = st.sidebar.radio("القائمة الرئيسية", ["🤖 استشارة الخبير", "🧮 حاسبة القياسات", "📄 نظام الفواتير"])

# --- القسم 1: استشارة الخبير (النسخة المستقرة 2.0) ---
if choice == "🤖 استشارة الخبير":
    st.header("🤖 خبير الكهرباء الذكي")
    st.info("اسأل الخبير على أي مشكلة تقنية (تكلم بالدارجة التونسية)")
    
    query = st.text_area("اشرح المشكلة هنا:", height=150, placeholder="مثلاً: كيفاش نركب تيليريبتور (Télérupteur)؟")
    
    if st.button("تحليل وإجابة 🚀"):
        if not API_KEY:
            st.error("❌ المفتاح ناقص في الإعدادات!")
        elif query:
            with st.spinner("الخبير يفكر..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي محترف. أجب بالدارجة التونسية التقنية: {query}"}]}]}
                try:
                    res = requests.post(url, json=payload, timeout=15)
                    if res.status_code == 200:
                        st.markdown("### 💡 نصيحة الخبير:")
                        st.success(res.json()['candidates'][0]['content']['parts'][0]['text'])
                    elif res.status_code == 429:
                        st.warning("⚠️ السيرفر مشغول (كثير من الطلبات). انتظر 30 ثانية وعاود اضغط.")
                    else:
                        st.error(f"خطأ من السيرفر: {res.status_code}")
                except:
                    st.error("📡 فشل الاتصال بالانترنت.")

# --- القسم 2: حاسبة القياسات ---
elif choice == "🧮 حاسبة القياسات":
    st.header("🧮 حاسبة مقاطع الأسلاك")
    col1, col2 = st.columns(2)
    with col1:
        watt = st.number_input("قوة الجهاز (Watt):", min_value=0, value=2000, step=100)
    with col2:
        volt = 220
        amp = watt / volt
        st.metric("التيار (Ampère)", f"{amp:.2f} A")
    
    st.write("---")
    if amp <= 11:
        st.success("✅ السلك المناسب: 1.5 مم² | Disjoncteur: 10A")
    elif amp <= 17:
        st.success("✅ السلك المناسب: 2.5 مم² | Disjoncteur: 16A أو 20A")
    elif amp <= 24:
        st.warning("⚠️ السلك المناسب: 4 مم² | Disjoncteur: 25A")
    else:
        st.error("🚨 حمل كبير! تحتاج سلك 6 مم² فما فوق.")

# --- القسم 3: نظام الفواتير المطور ---
elif choice == "📄 نظام الفواتير":
    st.header("📄 تحرير فاتورة تقديرية (Devis)")
    
    with st.expander("➕ إضافة سلعة للفاتورة", expanded=True):
        search = st.text_input("🔍 ابحث عن مادة (فورو، كابل، هاجر...):")
        filtered_items = [k for k in DB_MATERIELS.keys() if search.lower() in k.lower()]
        
        selected_prod = st.selectbox("المادة:", filtered_items if filtered_items else list(DB_MATERIELS.keys()))
        qte = st.number_input("الكمية:", min_value=1, value=1)
        price = st.number_input("ثمن الوحدة (DT):", value=DB_MATERIELS[selected_prod], format="%.3f")
        
        if st.button("إضافة للفاتورة ➕"):
            st.session_state['invoice_items'].append({
                "المادة": selected_prod,
                "الكمية": qte,
                "الثمن": price,
                "المجموع": qte * price
            })
            st.rerun()

    if st.session_state['invoice_items']:
        st.write("---")
        df = pd.DataFrame(st.session_state['invoice_items'])
        st.table(df)
        
        total = df["المجموع"].sum()
        st.markdown(f"## المجموع الجملي: :green[{total:.3f} DT]")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🗑️ مسح الفاتورة"):
                st.session_state['invoice_items'] = []
                st.rerun()
        with c2:
            st.download_button("📥 تحميل الفاتورة (CSV)", df.to_csv(index=False), "devis.csv")
