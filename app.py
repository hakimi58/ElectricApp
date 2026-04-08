import streamlit as st
import google.generativeai as genai

# إعدادات واجهة التطبيق
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

# تصميم CSS لجعله يشبه تطبيقات الأندرويد
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    h1 { color: #e67e22; text-align: center; font-family: 'Arial'; }
    .stChatInput { border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ خبير الكهرباء التونسي")

# جلب المفتاح السري من إعدادات Streamlit
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        # استخدام الموديل المستقر لعام 2026
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # نظام الدردشة
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("اسأل خبيرك الكهربائي هنا..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("👷 جاري التفكير في الحل..."):
                    # توجيه الموديل ليكون خبيراً تونسياً
                    full_query = f"أنت مهندس كهرباء تونسي خبير. أجب بلهجة تقنية واضحة ومبسطة: {prompt}"
                    response = model.generate_content(full_query)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                    
    except Exception as e:
        st.error(f"⚠️ حدث خطأ تقني: {e}")
else:
    st.warning("⚠️ يرجى التأكد من إضافة GOOGLE_API_KEY في Secrets.")
