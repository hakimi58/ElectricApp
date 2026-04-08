import google.generativeai as genai

# 1. إعداد المفتاح (استبدل النص بالأسفل بمفتاحك الخاص)
genai.configure(api_key="AIzaSyBVBqJeBslEfq81liIKXgtwu7YIXX_sCpA")

# 2. اختيار نموذج الذاء الاصطناعي
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. أمر برمجي لتجربة التشغيل
response = model.generate_content("أعطني نصيحة برمجية للمبتدئين")

# 4. طباعة النتيجة
print(response.text)
