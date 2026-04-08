 import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Tunisia Electric", page_icon="⚡")
st.title("⚡ خبير الكهرباء التونسي")

# جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"خطأ في الإعدادات: {e}")
else:
    st.warning("⚠️ يرجى إضافة المفتاح في Secrets")
    st.stop()

query = st.text_input("اسأل خبيرك التقني:")

if st.button("إجابة"):
    if query:
        with st.spinner('👷 جاري الاتصال بالخبير...'):
            try:
                response = model.generate_content(query)
                st.markdown("---")
                st.success(response.text)
            except Exception as e:
                st.error(f"حدث خطأ أثناء جلب الإجابة: {e}")
