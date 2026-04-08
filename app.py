import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

# 2. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. القائمة الجانبية (بسيطة وواضحة)
st.sidebar.title("🛠️ قائمة الأدوات")
choice = st.sidebar.radio("اختر ماذا تريد:", ["استشارة الخبير (AI)", "حاسبة الأسلاك والقواطع"])

# --- القسم الأول: خبير الذكاء الاصطناعي ---
if choice == "استشارة الخبير (AI)":
    st.header("🤖 خبير الكهرباء الذكي")
    st.write("اسأل عن أي عطل أو طريقة تركيب...")
    
    query = st.text_area("اشرح المشكلة هنا:", height=150)
    
    if st.button("الحصول على الحل"):
        if query and API_KEY:
            with st.spinner("جاري التفكير في الحل..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء، أجب باللهجة التونسية التقنية: {query}"}]}]}
                try:
                    response = requests.post(url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    st.success("✅ تشخيص الخبير:")
                    st.text_area("الإجابة:", value=answer, height=300)
                except:
                    st.error("فشل الاتصال بجوجل، تأكد من مفتاح الـ API.")
        else:
            st.warning("الرجاء كتابة سؤال أولاً.")

# --- القسم الثاني: حاسبة الأحمال (بدون تعقيد) ---
elif choice == "حاسبة الأسلاك والقواطع":
    st.header("🧮 حاسبة القياسات الفنية")
    st.write("أداة سريعة لاختيار السلك والديجونكتور المناسب.")
    
    watt = st.number_input("قوة الجهاز الكلية (Watt):", min_value=0, value=2000)
    
    if st.button("احسب القياسات"):
        amp = watt / 220
        st.info(f"التيار المسحوب: {amp:.2f} أمبير")
        
        if amp <= 10:
            res = "خيط 1.5 مم² + ديجونكتور 10A"
        elif amp <= 16:
            res = "خيط 2.5 مم² + ديجونكتور 16A"
        elif amp <= 25:
            res = "خيط 4 مم² + ديجونكتور 25A"
        else:
            res = "خيط 6 مم² فأكثر + ديجونكتور 32A"
            
        st.success(f"النتيجة المقترحة: {res}")
