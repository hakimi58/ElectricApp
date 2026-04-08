import streamlit as st
import requests

st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡")
st.write("# ⚡ خبير الكهرباء التونسي")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ المفتاح مفقود في Secrets.")
else:
    # خطوة 1: البحث عن الموديلات المتاحة في حسابك
    with st.spinner("جاري فحص الموديلات المتاحة في حسابك..."):
        list_models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
        try:
            res = requests.get(list_models_url)
            models_data = res.json()
            # نبحث عن أي موديل يدعم توليد المحتوى
            available_models = [m['name'] for m in models_data.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
            
            if not available_models:
                st.error("❌ لا يوجد أي موديل متاح لهذا المفتاح. تأكد من تفعيل Gemini API.")
            else:
                # نختار أول موديل متاح (غالباً سيكون gemini-1.5-flash أو gemini-pro)
                selected_model = available_models[0]
                st.success(f"✅ تم الاتصال بنجاح عبر الموديل: {selected_model.split('/')[-1]}")
                
                prompt = st.chat_input("اسأل خبير الكهرباء الآن...")
                if prompt:
                    with st.chat_message("user"):
                        st.write(prompt)
                    
                    # خطوة 2: إرسال السؤال للموديل الذي وجدناه
                    gen_url = f"https://generativelanguage.googleapis.com/v1beta/{selected_model}:generateContent?key={API_KEY}"
                    payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي، أجب باللهجة التونسية التقنية: {prompt}"}]}]}
                    
                    response = requests.post(gen_url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    
                    with st.chat_message("assistant"):
                        st.write(answer)
        except Exception as e:
            st.error(f"⚠️ فشل الفحص: {e}")

with st.sidebar:
    st.info("نصيحة: إذا كنت في تونس، تأكد أن حساب جوجل الخاص بك ليس مربوطاً بدولة محظورة.")
