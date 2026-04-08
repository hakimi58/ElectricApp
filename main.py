import google.generativeai as genai

# 1. إعداد المفتاح (استبدل النص بالأسفل بمفتاحك الخاص)
genai.configure(api_key="ضع_هنا_مفتاح_API_الخاص_بك")

# 2. اختيار نموذج الذاء الاصطناعي
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. أمر برمجي لتجربة التشغيل
response = model.generate_content("أعطني نصيحة برمجية للمبتدئين")

# 4. طباعة النتيجة
print(response.text)
