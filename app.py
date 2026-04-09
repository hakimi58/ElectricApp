import streamlit as st
import pandas as pd
import requests
import json

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة الكهربائي المحترف", layout="wide")

# 2. جلب المفتاح
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. قاعدة البيانات
DB_MATERIELS = {
    "Foureau Orange 11mm": 28.500, "Foureau Orange 13mm": 32.800,
    "Foureau Orange 16mm": 38.000, "Foureau Orange 20mm": 48.500,
    "Hager: Disjoncteur 16A": 9.800, "Tunisie Câbles: 1.5mm": 65.000
}

# 4. واجهة التطبيق
st.sidebar.title("القائمة")
choice = st.sidebar.radio("🛠️ الأدوات", ["استشارة الخبير (AI)", "حاسبة القياسات", "الفاتورة"])

# --- قسم الخبير (محاولات متعددة الروابط) ---
if choice == "استشارة الخبير (AI)":
    st.subheader("🤖 استشارة الخبير")
    query = st.text_area("اشرح المشكلة هنا:")
    
    if st.button("تحليل"):
        if not API_KEY:
            st.error("❌ المفتاح ناقص في Secrets.")
        elif query:
            # قائمة الروابط الممكنة (سنجربها واحداً تلو الآخر)
            endpoints = [
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}",
                f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}",
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
            ]
            
            success = False
            with st.spinner("جاري البحث عن رابط شغال..."):
                for url in endpoints:
                    try:
                        payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي، أجب بالدارجة: {query}"}]}]}
                        res = requests.post(url, json=payload, timeout=10)
                        
                        if res.status_code == 200:
                            st.info(res.json()['candidates'][0]['content']['parts'][0]['text'])
                            success = True
                            break # إذا نجح، توقف عن التجربة
                    except:
                        continue
                
                if not success:
                    st.error("⚠️ كل المحاولات فشلت بـ 404. يا سي حكيم، المفتاح اللي عندك فيه مشكلة في التفعيل من موقع Google AI Studio.")
                    st.info("💡 الحل: ادخل لموقع Google AI Studio واضغط على 'Create API Key in NEW Project' واستعمل المفتاح الجديد.")

# --- باقي الأقسام لضمان اشتغال التطبيق ---
elif choice == "حاسبة القياسات":
    watt = st.number_input("القدرة (Watt):", value=2000)
    st.success(f"التيار: {watt/220:.2f} A")
    
elif choice == "الفاتورة":
    st.write("الفاتورة تعمل")
