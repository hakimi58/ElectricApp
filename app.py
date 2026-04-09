import streamlit as st
import requests
from PIL import Image
import io

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="Tunisia Electric Master - Vision", page_icon="⚡", layout="wide")

# تنسيق الألوان لإعطاء طابع احترافي
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #f1c40f; color: black; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #d4ac0d; color: white; }
    div[data-testid="stExpander"] { background-color: white; border: 1px solid #dfe6e9; border-radius: 10px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.title("⚡ منصة الكهربائي المحترف - تونس (النسخة الذكية)")
st.write("أدوات تقنية، حسابات دقيقة، وتحليل الصور بالذكاء الاصطناعي.")

# 2. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. القائمة الجانبية للتنقل (Toolbox)
st.sidebar.title("🛠️ حقيبة الفني")
st.sidebar.markdown("---")
choice = st.sidebar.radio("اختر الأداة:", [
    "🤖 خبير الأعطال (AI)", 
    "📸 مصور الأعطال (Vision)",
    "🧮 حاسبة الكابلات والقواطع",
    "📏 حاسبة هبوط الجهد",
    "📑 دليل الربط السريع"
])

# --- القسم الأول: خبير الأعطال النصي ---
if choice == "🤖 خبير الأعطال (AI)":
    st.header("🤖 مستشارك الفني النصي")
    query = st.text_area("اشرح العطل أو اطلب نصيحة:", height=120, placeholder="مثلاً: علاش الديجونكتور يطيح كي يخدم الكليماتيزور؟")
    
    if st.button("تحليل المشكلة"):
        if query and API_KEY:
            with st.spinner("جاري استشارة قاعدة البيانات..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي محترف. قدم حلاً تقنياً مفصلاً باللهجة التونسية التقنية وبشكل نقاط واضحة: {query}. ركز على الأسباب والحلول العملية."}]}]}
                try:
                    response = requests.post(url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("✅ تشخيص الخبير:")
                    st.text_area("الإجابة:", value=answer, height=350)
                except:
                    st.error("مشكلة في الاتصال بالسيرفر. تأكد من مفتاح الـ API.")
        else:
            st.warning("الرجاء كتابة تفاصيل العطل.")

# --- القسم الثاني: مصور الأعطال (الميزة الجديدة) ---
elif choice == "📸 مصور الأعطال (Vision)":
    st.header("📸 تحليل صور الأعطال الكهربائية")
    st.write("ارفع صورة للوحة، قطة إلكترونية، أو عطل مكشوف، وسيقوم الخبير بتحليلها.")
    
    # تحميل الصورة
    uploaded_file = st.file_uploader("اختر صورة العطل:", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # عرض الصورة المرفوعة
        image = Image.open(uploaded_file)
        st.image(image, caption="الصورة المرفوعة", use_column_width=True)
        
        # صندوق نصي لإضافة تفاصيل
        extra_info = st.text_input("إضافة تفاصيل (اختياري):مثلاً: الكومبريسور ما يخدمش.")
        
        if st.button("تحليل الصورة"):
            if API_KEY:
                with st.spinner("جاري تحليل الصورة بعين الخبير..."):
                    try:
                        # تحويل الصورة إلى بايتات (Bytes) لإرسالها
                        img_byte_arr = io.BytesIO()
                        image.save(img_byte_arr, format=image.format)
                        img_bytes = img_byte_arr.getvalue()
                        
                        # إعداد الطلب لموديل Gemini Vision
                        # ملحوظة: نستخدم موديل يدعم الرؤية مثل gemini-pro-vision أو gemini-1.5-flash
                        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
                        
                        # إعداد التلقين (Prompt)
                        prompt_text = f"أنت خبير كهرباء تونسي محترف. حلل هذه الصورة بدقة. ماذا ترى؟ هل هناك مشكلة أو خطر كهربائي؟ صف ما تراه باللهجة التونسية التقنية. التفاصيل الإضافية: {extra_info}"
                        
                        # إعداد الحمولة (Payload)
                        payload = {
                            "contents": [{
                                "parts": [
                                    {"text": prompt_text},
                                    {"inline_data": {
                                        "mime_type": f"image/{image.format.lower()}",
                                        "data": requests.utils.quote(img_bytes)
                                    }}
                                ]
                            }]
                        }
                        
                        # إرسال الطلب (Request)
                        response = requests.post(url, json=payload)
                        response.raise_for_status() # التأكد من عدم وجود خطأ
                        
                        result = response.json()
                        analysis = result['candidates'][0]['content']['parts'][0]['text']
                        
                        # عرض التحليل
                        st.success("✅ تحليل الخبير البصري:")
                        st.text_area("النتيجة:", value=analysis, height=350)
                        
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء تحليل الصورة: {e}")
            else:
                st.error("المفتاح ناقص.")

# --- القسم الثالث: حاسبة الكابلات ---
elif choice == "🧮 حاسبة الكابلات والقواطع":
    st.header("🧮 حاسبة القياسات الفنية (السلك والديجونكتور)")
    watt = st.number_input("قوة الجهاز (Watt):", min_value=0, value=2500, step=100)
    
    if st.button("احسب"):
        # حساب التيار (220V فاز ونوتر)
        amp = watt / 220
        # تحديد السلك والقاطع بناءً على المواصفات التونسية NF C 15-100
        if amp <= 11: res, wire = "10A", "1.5 مم²"
        elif amp <= 17: res, wire = "16A", "2.5 مم²"
        elif amp <= 24: res, wire = "25A", "4 مم²"
        elif amp <= 30: res, wire = "32A", "6 مم²"
        else: res, wire = "40A فأكثر", "10 مم² فأكثر"
        
        st.success(f"✅ النتيجة التقديرية:\n- التيار: {amp:.1f} أمبير\n- القاطع (Disjoncteur): {res}\n- مقطع السلك: {wire}")

# --- القسم الرابع: حاسبة هبوط الجهد ---
elif choice == "📏 حاسبة هبوط الجهد":
    st.header("📏 فحص ضياع الجهد في المسافات الطويلة")
    current = st.number_input("التيار (Ampere):", value=16)
    length = st.number_input("طول الكابل (متر):", value=30)
    section = st.selectbox("مقطع السلك (مم²):", [1.5, 2.5, 4, 6, 10, 16])
    
    if st.button("احسب الضياع"):
        drop = (2 * length * current) / (56 * section)
        percentage = (drop / 220) * 100
        st.metric("هبوط الجهد", f"{drop:.2f} Volt", f"{percentage:.1f}%")
        if percentage > 3:
            st.error("⚠️ الضياع كبير! يجب تكبير مقطع السلك.")
        else:
            st.success("✅ الضياع مقبول.")

# --- القسم الخامس: دليل الربط السريع ---
elif choice == "📑 دليل الربط السريع":
    st.header("📑 مخططات الربط الأساسية (مساعدة نصية)")
    item = st.selectbox("اختر الدارة:", ["الذهاب والإياب (Va-et-vient)", "المبدل (Télérupteur)", "المؤقت (Minuterie)"])
    
    if item == "الذهاب والإياب (Va-et-vient)":
        st.info("الربط: نحتاج مفتاحين Va-et-vient. الخيط الحامي (Phase) يدخل للـ 'Common' في المفتاح الأول، والـ 'Common' في المفتاح الثاني يذهب للمصباح. يربط المفتاحان ببعضهما عبر خيطي 'النافطة' (Navettes).")
    elif item == "المبدل (Télérupteur)":
        st.info("الربط: يحتاج أزرار ضاغطة (Boutons Poussoirs). يربط الفاز والنوتر للوشيعة (A1, A2) عبر الأزرار، والملامسات (1, 2) تقطع الفاز الذاهب للمصابيح.")
