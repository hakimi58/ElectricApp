import streamlit as st
import google.generativeai as genai

# إعداد الصفحة لتناسب شكل تطبيقات الهاتف
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="centered")

# إضافة لمسات جمالية (CSS)
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #e67e22; text-align: center; font-size: 26px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #e67e22; color: white; height: 3em; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">⚡ خبير الكهرباء التونسي Pro</p>', unsafe_allow_html=True)

# القائمة الجانبية للتنقل (مثل التطبيقات الحقيقية)
st.sidebar.header("⚙️ القائمة")
menu = st.sidebar.radio("اختر الوظيفة:", ["🤖 استشارة الذكاء الاصطناعي", "🧮 حاسبة الأحمال", "🎨 دليل الألوان"])

# جلب المفتاح من Secrets
api_key = st.secrets.get("GOOGLE_API_KEY")

if menu == "🤖 استشارة الذكاء الاصطناعي":
    st.info("مرحباً بك! اسألني عن أي مشكل كهربائي.")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            user_input = st.chat_input("اكتب سؤالك هنا...")
            if user_input:
                with st.chat_message("user"): st.write(user_input)
                with st.spinner("جاري التفكير..."):
                    res = model.generate_content(f"أنت خبير كهرباء تونسي محترف: {user_input}")
                    with st.chat_message("assistant"): st.write(res.text)
        except Exception as e:
            st.error(f"خطأ: {e}")
    else:
        st.warning("⚠️ يرجى إضافة المفتاح السري في إعدادات Streamlit")

elif menu == "🧮 حاسبة الأحمال":
    st.subheader("💡 حساب القدرة والشدة")
    v = st.number_input("الجهد (Volt)", value=220)
    i = st.number_input("التيار (Ampere)", value=10)
    st.metric("القدرة الإجمالية", f"{v * i} Watt")

elif menu == "🎨 دليل الألوان":
    st.subheader("📋 المعايير التونسية")
    st.table({
        "السلك": ["الطور (Phase)", "المحايد (Neutre)", "الأرضي (Terre)"],
        "اللون": ["بني / أسود", "أزرق", "أخضر وأصفر"]
    })
