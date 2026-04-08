import streamlit as st
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

st.markdown('<h1 style="text-align:center;">⚡ خبير الكهرباء التونسي Pro</h1>', unsafe_allow_html=True)

# القائمة الجانبية
menu = st.sidebar.radio("القائمة:", ["🤖 استشارة الذكاء الاصطناعي", "🧮 حاسبة الأحمال", "🎨 دليل الألوان"])

api_key = st.secrets.get("GOOGLE_API_KEY")

if menu == "🤖 استشارة الذكاء الاصطناعي":
    if api_key:
        try:
            genai.configure(api_key=api_key)
            
            # الحل السحري: تجربة الموديل بدون تحديد v1beta يدوياً
            # واستخدام اسم الموديل الأكثر استقراراً
            model = genai.GenerativeModel('gemini-1.5-flash-latest') 
            
            user_input = st.chat_input("اسأل خبيرك...")
            if user_input:
                with st.chat_message("user"): st.write(user_input)
                with st.spinner("جاري التحليل..."):
                    # إضافة تعليمات النظام لضمان اللهجة التونسية
                    res = model.generate_content(f"أجب كخبير كهرباء تونسي: {user_input}")
                    with st.chat_message("assistant"): st.write(res.text)
        except Exception as e:
            # إذا فشل الموديل الأول، نجرب الموديل الاحتياطي فوراً
            try:
                model = genai.GenerativeModel('gemini-pro')
                res = model.generate_content(user_input)
                st.write(res.text)
            except:
                st.error("جوجل قام بتحديث الموديلات. يرجى التأكد من تحديث مكتبة google-generativeai في ملف requirements.txt")
    else:
        st.warning("⚠️ يرجى إضافة المفتاح السري")

elif menu == "🧮 حاسبة الأحمال":
    v = st.number_input("الجهد (V)", value=220)
    i = st.number_input("التيار (A)", value=10)
    st.metric("القدرة", f"{v * i} Watt")

elif menu == "🎨 دليل الألوان":
    st.table({"السلك": ["Phase", "Neutre", "Terre"], "اللون": ["بني", "أزرق", "أخضر/أصفر"]})
