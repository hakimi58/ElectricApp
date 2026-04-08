import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Tunisia Electric", layout="centered")
st.write("# ⚡ خبير الكهرباء التونسي")

# جلب المفتاح السري
key = st.secrets.get("GOOGLE_API_KEY")

if key:
    try:
        genai.configure(api_key=key)
        # التعديل الجوهري: استخدام الإصدار المستقر والمتاح حالياً
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input("اسأل خبيرك..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            
            # محاولة جلب الإجابة
            response = model.generate_content(f"أنت خبير كهرباء تونسي. أجب بدقة على: {prompt}")
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.chat_message("assistant").write(response.text)
            
    except Exception as e:
        st.error(f"حدث خطأ في الموديل: {e}")
        st.info("نصيحة: تأكد من تحديث مكتبة google-generativeai في ملف requirements.txt")
else:
    st.error("المفتاح السري GOOGLE_API_KEY غير موجود في Secrets")
