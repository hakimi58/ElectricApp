import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.write("# ⚡ خبير الكهرباء التونسي")

# إعداد المفتاح
key = st.secrets.get("GOOGLE_API_KEY")

if key:
    try:
        # إجبار المكتبة على استخدام الإصدار المستقر v1 وليس v1beta
        genai.configure(api_key=key, transport='grpc') 
        
        # استخدام الموديل بدون أي إضافات في الاسم لضمان التوافق
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = st.chat_input("اسأل خبيرك...")
        if prompt:
            with st.chat_message("user"):
                st.write(prompt)
            
            # الطلب مع تحديد الإعدادات لضمان عدم حدوث خطأ 404
            response = model.generate_content(
                f"أنت خبير كهرباء تونسي، أجب بدقة على: {prompt}",
                generation_config=genai.types.GenerationConfig(
                    candidate_count=1,
                    max_output_tokens=1000,
                    temperature=0.7
                )
            )
            
            with st.chat_message("assistant"):
                st.write(response.text)
                
    except Exception as e:
        # إذا استمر الخطأ، سنعرضه هنا لنفهمه بدقة
        st.error(f"⚠️ تنبيه تقني: {str(e)}")
        if "404" in str(e):
            st.info("جوجل تطلب تحديث الرابط. جاري المحاولة بطريقة احتياطية...")
            # محاولة أخيرة بموديل مختلف تماماً
            try:
                backup_model = genai.GenerativeModel('gemini-pro')
                res = backup_model.generate_content(prompt)
                st.write(res.text)
            except:
                st.warning("يرجى مراجعة ملف requirements.txt والتأكد أنه يحتوي على google-generativeai فقط بدون تحديد إصدار قديم.")
else:
    st.error("المفتاح السري ناقص")
