 
# --- دالة جلب الموديل المطورة لتجنب خطأ 404 ---
@st.cache_resource
def load_model():
    # قائمة بجميع الأسماء المحتملة للموديل حسب تحديثات جوجل
    potential_names = [
        'models/gemini-1.5-flash-latest', 
        'models/gemini-1.5-flash', 
        'gemini-1.5-flash',
        'models/gemini-pro'
    ]
    
    for name in potential_names:
        try:
            m = genai.GenerativeModel(name)
            # تجربة فحص سريعة جداً للتأكد أن الموديل شغال
            m.generate_content("hi", generation_config={"max_output_tokens": 1})
            return m
        except Exception:
            # إذا فشل هذا الاسم، ينتقل للاسم الذي يليه في القائمة
            continue
    
    # محاولة أخيرة: البحث في قائمة الموديلات المتاحة في حسابك فعلياً
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                return genai.GenerativeModel(m.name)
    except:
        pass
    
    return None

# استدعاء الموديل
model = load_model()
