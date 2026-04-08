import os
import google.generativeai as genai

# 1. جلب المفتاح السري من إعدادات النظام (GitHub Secrets)
# اسم المفتاح هنا يجب أن يكون مطابقاً تماماً لما سميته في GitHub
api_key = os.environ.get("GEMINI_API_KEY")

# 2. التحقق من وجود المفتاح قبل البدء
if not api_key:
    raise ValueError("خطأ: لم يتم العثور على 'GEMINI_API_KEY'. تأكد من إضافته في Secrets على GitHub.")

# 3. إعداد المكتبة بالمفتاح السري
genai.configure(api_key=api_key)

# 4. تشغيل النموذج
model = genai.GenerativeModel('gemini-1.5-flash')

try:
    response = model.generate_content("أهلاً، أنا مبرمج أستخدم GitHub Secrets الآن!")
    print(response.text)
except Exception as e:
    print(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
