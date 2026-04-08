 import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Tunisia Electric", page_icon="⚡")
st.title("⚡ خبير الكهرباء التونسي")

# جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        # هذا السطر يضمن الوصول للموديل حتى لو تغير اسمه
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
                # هنا التعديل: نحدد الموديل مباشرة عند الطلب لضمان عدم وجود NotFound
                response = model.generate_content(query)
                st.markdown("---")
                st.success(response.text)
            except Exception as e:
                # إذا لم يجد الموديل الأول، سيجرب الموديل الاحتياطي
                try:
                    alt_model = genai.GenerativeModel('gemini-pro')
                    response = alt_model.generate_content(query)
                    st.success(response.text)
                except:
                    st.error("جوجل يرفض الاتصال حالياً. تأكد أن المفتاح API Key نشط ومفعل من Google AI Studio.")
