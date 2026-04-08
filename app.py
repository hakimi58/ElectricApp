  import streamlit as st
import google.generativeai as genai

# 1. إعدادات مظهر التطبيق ليكون مثل تطبيقات الهاتف
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="centered")

# تصميم احترافي
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #e67e22; text-align: center; font-size: 28px; font-weight: bold; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 12px; background-color: #e67e22; color: white; height: 3em; font-size: 18px; }
    .stSelectbox { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">⚡ خبير الكهرباء التونسي Pro</p>', unsafe_allow_html=True)

# 2. القائمة الجانبية للتنقل
st.sidebar.header("⚙️ الإعدادات")
menu = st.sidebar.radio("انتقل إلى:", ["🤖 استشارة الذكاء الاصطناعي", "🧮 حاسبة الأحمال", "🎨 دليل ألوان الأسلاك"])

# جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# --- القسم الأول: الذكاء الاصطناعي ---
if menu == "🤖 استشارة الذكاء الاصطناعي":
    st.info("مرحباً بك! أنا مساعدك الذكي، اسألني عن أي عطل أو مخطط كهربائي.")
    if API_KEY:
        try:
            genai.configure(api_key=API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            user_input = st.chat_input("اكتب سؤالك هنا (مثلاً: كيفية ربط دجونكتير)...")
            if user_input:
                with st.chat_message("user"): st.write(user_input)
                with st.spinner("جاري التفكير..."):
                    res = model.generate_content(f"أنت خبير كهرباء تونسي محترف. أجب بوضوح: {user_input}")
                    with st.chat_message("assistant"): st.write(res.text)
        except Exception as e:
            st.error(f"حدث خطأ في الاتصال: {e}")
    else:
        st.warning("⚠️ يرجى إضافة GOOGLE_API_KEY في إعدادات Secrets")

# --- القسم الثاني: حاسبة الأحمال ---
elif menu == "🧮 حاسبة الأحمال":
    st.subheader("💡 حساب القدرة الكهربائية")
    col1, col2 = st.columns(2)
    with col1:
        v = st.number_input("الجهد (ولت - Volt)", value=220)
    with col2:
        i = st.number_input("التيار (أمبير - Ampere)", value=10)
    
    power = v * i
    st.metric("القدرة الإجمالية", f"{power} واط (Watt)")
    st.success(f"تحتاج إلى سلك بقطر مناسب لـ {i} أمبير.")

# --- القسم الثالث: دليل الألوان ---
elif menu == "🎨 دليل ألوان الأسلاك":
    st.subheader("📋 المعايير المعتمدة في تونس")
    st.table({
        "نوع السلك": ["الطور (Phase)", "المحايد (Neutre)", "الأرضي (Terre)"],
        "اللون المتفق عليه": ["بني أو أسود", "أزرق سماوي", "أخضر مع أصفر"]
    })
    st.warning("تنبيه: دائماً تأكد من قطع التيار قبل فحص الأسلاك!")
