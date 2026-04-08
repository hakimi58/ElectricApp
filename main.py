 import os
import google.generativeai as genai
from dotenv import load_dotenv

# تحميل المتغيرات السرية من ملف .env أو إعدادات GitHub
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("خطأ: لم يتم العثور على مفتاح API. تأكد من ضبطه في Secrets!")
else:
    genai.configure(api_key=api_key)
    
    # اختيار النموذج
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    try:
        response = model.generate_content("اكتب كود بلغة بايثون لطباعة كلمة مرحبا")
        print(response.text)
    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال: {e}")
