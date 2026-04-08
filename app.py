  import streamlit as st
import google.generativeai as genai

# 1. إعدادات مظهر التطبيق ليكون مثل تطبيقات الهاتف
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

# تصميم احترافي بـ CSS
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .main-title { color: #e67e22; text-align: center; font-size: 28px; font-weight: bold; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #e67e22; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">⚡ خبير الكهرباء التونسي Pro</p>', unsafe_allow_html=True)

# 2. القائمة الجانبية (Navigation)
menu = st.sidebar.selectbox("القائمة الرئيسية", ["الذكاء الاصطناعي", "حاسبة الأحمال", "دليل الألوان"])

# جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# --- القسم الأول: الذكاء الاصطناعي ---
if menu == "الذكاء الاصطناعي":
    st.info("🤖 اسأل الخبير عن أي عطل أو طريقة ربط")
    if API_KEY:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        user_input = st.chat_input("اكتب سؤالك هنا (مثلاً: ربط محرك 380v)")
        if user_input:
            with st.chat_message("user"): st.write(user_input)
            with st.spinner("جاري التحليل..."):
                res = model.generate_content(f"أنت خبير كهرباء تونسي. أجب بدقة: {user_input}")
                with st.chat_message("assistant"): st.write(res.text)
    else:
        st.error("المفتاح السري ناقص!")

# --- القسم الثاني: حاسبة الأحمال ---
elif menu == "حاسبة الأحمال":
    st.subheader("🧮 حاسبة قانون أوم والقدرة")
    col1, col2 = st.columns(2)
    with col1:
        v = st.number_input("الجهد (Volt)", value=220)
        i = st.number_input("التيار (Amper)", value=10)
    with col2:
        power = v * i
        st.metric("القدرة (Watt)", f"{power} W")
    st.help("استخدم هذه الحاسبة لتحديد سلك القاطع المناسب.")

# --- القسم الثالث: دليل الألوان ---
elif menu == "دليل الألوان":
    st.subheader("🎨 دليل ألوان الأسلاك (تونس/أوروبا)")
    st.table({
        "السلك": ["الطور (Phase)", "المحايد (Neutre)", "الأرضي (Terre)"],
        "اللون": ["بني أو أسود (Marron/Noir)", "أزرق (Bleu)", "أخضر/أصفر (Vert/Jaune)"]
    })
