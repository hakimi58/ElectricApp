import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.write("# ⚡ خبير الكهرباء التونسي")

# 1. جلب المفتاح السري من Streamlit Secrets
# تأكد أنك وضعته في GitHub أو Streamlit Cloud باسم GOOGLE_API_KEY
key = st.secrets.get("GOOGLE_API_KEY")

if key:
    try:
        # تهيئة المكتبة
        genai.configure(api_key=key) 
        
        # 2. تحديث استدعاء الموديل (تم إزالة الإعدادات المعقدة لضمان التوافق)
        # نستخدم gemini-1.5-flash مباشرة
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = st.chat_input("اسأل خبيرك في الكهرباء...")
        
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.spinner("جاري استشارة الخبير..."):
                # محاولة توليد المحتوى
                response = model.generate_content(
                    f"أنت خبير كهرباء تونسي محترف. أجب باللغة العربية (ويمكنك استخدام مصطلحات تونسية تقنية) على السؤال التالي بدقة: {prompt}"
                )
                
                with st.chat_message("assistant"):
                    if response.text:
                        st.write(response.text)
                    else:
                        st.error("تعذر الحصول على إجابة، حاول صياغة السؤال بشكل مختلف.")
                
    except Exception as e:
        # معالجة ذكية للأخطاء
        error_msg = str(e)
        if "404" in error_msg:
            st.error("⚠️ الموديل gemini-1.5-flash غير متاح حالياً في منطقتك أو يحتاج لتحديث المكتبة.")
            st.info("نصيحة: تأكد من تحديث ملف requirements.txt")
        else:
            st.error(f"⚠️ خطأ تقني: {error_msg}")
else:
    st.warning("⚠️ المفتاح السري (GOOGLE_API_KEY) مفقود. يرجى إضافته في إعدادات Secrets.")
