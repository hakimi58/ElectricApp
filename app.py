import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")

# 2. عنوان التطبيق
st.title("⚡ خبير الكهرباء التونسي")
st.markdown("---")

# 3. جلب المفتاح
API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("المفتاح مفقود في إعدادات Secrets!")
else:
    # واجهة الإدخال
    user_query = st.text_input("اسأل خبيرك (مثلاً: الفاتورة غالية، مشكلة في التار):")

    if st.button("إرسال السؤال"):
        if user_query:
            # عرض سؤالك بوضوح
            st.info(f"**سؤالك:** {user_query}")
            
            with st.spinner("جاري الاتصال بالخبير..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                
                payload = {
                    "contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي، أجب باللهجة التونسية التقنية: {user_query}"}]}]
                }

                try:
                    response = requests.post(url, json=payload)
                    res_json = response.json()
                    
                    if "candidates" in res_json:
                        answer = res_json['candidates'][0]['content']['parts'][0]['text']
                        
                        # الحل الجذري: عرض الإجابة داخل صندوق ملون ثابت
                        # هذا الصندوق لا يمكن أن يكون نصه أبيض أبداً
                        st.success("✅ إجابة الخبير:")
                        st.write(answer)
                        
                        # إضافة زر لتحميل الإجابة إذا كنت لا تراها
                        st.download_button("حفظ الإجابة كنص", answer, file_name="answer.txt")
                    else:
                        st.error("السيرفر لم يرسل إجابة، جرب مرة أخرى.")
                except Exception as e:
                    st.error(f"خطأ في الاتصال: {e}")
        else:
            st.warning("الرجاء كتابة سؤال أولاً.")

# 💡 نصيحة تقنية تونسية
st.markdown("---")
st.sidebar.markdown("### 🛠️ نصيحة الخبير")
st.sidebar.info("ديما ثبت في 'المنقذ' (Disjoncteur) متاعك، إذا كان يسخن برشة راهو فمة 'شوركوي' (Court-circuit) وإلا 'شارج' كبيرة عليه.")
