import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.write("# ⚡ خبير الكهرباء التونسي")

# جلب المفتاح من Secrets
key = st.secrets.get("GOOGLE_API_KEY")

if key:
    try:
        # الإعداد الأساسي
        genai.configure(api_key=key)
        
        # --- التعديل الجذري هنا ---
        # استخدام الاسم الكامل للموديل يحل مشكلة الـ 404 في معظم المناطق
        # بدلاً من استخدام الاسم المختصر، نستخدم المسار الكامل
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        prompt = st.chat_input("اسأل خبيرك في الكهرباء...")
        
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            
            with st.spinner("جاري الاتصال بالخبير..."):
                # محاولة طلب المحتوى
                response = model.generate_content(
                    f"أنت خبير كهرباء تونسي محترف. أجب بدقة وباللهجة التقنية التونسية: {prompt}"
                )
                
                with st.chat_message("assistant"):
                    st.write(response.text)
                
    except Exception as e:
        st.error(f"⚠️ حدث خطأ تقني: {str(e)}")
        # إذا فشل الفلاش، نحاول تشغيل النسخة المستقرة الأخرى تلقائياً
        if "404" in str(e) or "not found" in str(e).lower():
            st.info("جاري محاولة الاتصال بموديل احتياطي...")
            try:
                backup_model = genai.GenerativeModel('gemini-pro')
                res = backup_model.generate_content(prompt)
                st.write(res.text)
            except:
                st.warning("تأكد من تحديث ملف requirements.txt إلى أحدث إصدار.")
else:
    st.error("المفتاح السري (GOOGLE_API_KEY) ناقص في إعدادات Streamlit.")
