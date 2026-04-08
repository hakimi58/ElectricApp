 import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.markdown('<h1 style="text-align:center; color:#e67e22;">⚡ خبير الكهرباء التونسي</h1>', unsafe_allow_html=True)

# الربط مع API
api_key = st.secrets.get("GOOGLE_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    # استخدام التسمية العالمية والمستقرة لعام 2026
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # واجهة الدردشة
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input("اسأل خبيرك التقني..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        try:
            # صياغة الطلب بلهجة تونسية
            response = model.generate_content(f"أنت مهندس كهرباء تونسي، أجب بدقة على: {prompt}")
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.chat_message("assistant").write(response.text)
        except Exception as e:
            st.error(f"خطأ في الاتصال: {e}")
else:
    st.warning("يرجى إضافة المفتاح السري GOOGLE_API_KEY")
