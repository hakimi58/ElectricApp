import streamlit as st
import requests

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="Tunisia Electric Pro", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #ffc107; color: black; font-weight: bold; }
    div[data-testid="stExpander"] { background-color: white; border: 1px solid #ddd; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ منصة الكهربائي المحترف - تونس")
st.write("أدوات تقنية، حسابات دقيقة، واستشارات بالذكاء الاصطناعي")

API_KEY = st.secrets.get("GOOGLE_API_KEY")

# --- القائمة الجانبية (لجني المال مستقبلاً عبر الإعلانات أو الاشتراكات) ---
with st.sidebar:
    st.header("💰 خدمات بريميوم")
    st.info("قريباً: الحصول على شهادة مطابقة للمواصفات")
    st.write("---")
    st.subheader("إعدادات الحساب")
    if st.button("تفعيل النسخة الكاملة"):
        st.write("اتصل بالدعم لتفعيل الاشتراك")

# --- القسم الأول: الحاسبة التقنية (هذه تعطي قيمة للتطبيق) ---
st.header("🧮 حاسبة القواطع والأسلاك")
with st.expander("اضغط هنا لحساب القاطع وسلك التوصيل"):
    col1, col2 = st.columns(2)
    with col1:
        power = st.number_input("قوة الجهاز (Watt):", min_value=0, value=2000)
        voltage = st.selectbox("الجهد (Volt):", [220, 380])
    with col2:
        distance = st.number_input("طول الكابل (متر):", min_value=1, value=10)
    
    if st.button("احسب الآن"):
        # حساب التيار: I = P / V
        current = power / voltage
        # تقدير السلك (تقريبي للمواصفات التونسية)
        if current <= 10: wire = "1.5 مم²"; breaker = "10A"
        elif current <= 16: wire = "2.5 مم²"; breaker = "16A"
        elif current <= 25: wire = "4 مم²"; breaker = "25A"
        elif current <= 32: wire = "6 مم²"; breaker = "32A"
        else: wire = "10 مم² فأكثر"; breaker = "40A+"
        
        st.success(f"✅ النتائج المقترحة:\n- التيار: {current:.2f} أمبير\n- سلك التوصيل: {wire}\n- القاطع (Disjoncteur): {breaker}")

# --- القسم الثاني: خبير الذكاء الاصطناعي ---
st.header("🤖 استشارة الخبير (الذكاء الاصطناعي)")
query = st.text_area("اشرح العطل أو اطلب نصيحة فنية (باللهجة التونسية):", height=100)

if st.button("إرسال الاستشارة"):
    if query and API_KEY:
        with st.spinner("جاري تحليل العطل..."):
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي، ساعد فني زميل في حل هذا المشكل التقني باحترافية: {query}"}]}]
            }
            try:
                response = requests.post(url, json=payload)
                ans = response.json()['candidates'][0]['content']['parts'][0]['text']
                st.text_area("رد الخبير التقني:", value=ans, height=250)
            except:
                st.error("خطأ في الاتصال.")
    else:
        st.warning("الرجاء كتابة السؤال.")

# --- القسم الثالث: دليل أعطال المكيفات ---
st.header("❄️ دليل أكواد أعطال المكيفات")
brand = st.selectbox("اختر نوع المكيف:", ["LG", "Samsung", "Gree", "Midea", "General"])
code = st.text_input("ادخل رمز الخطأ (مثلاً: E1, CH05):")
if st.button("بحث عن الخطأ"):
    st.info(f"جاري البحث عن رمز {code} لمكيف {brand}... (يمكنك سؤال الخبير أعلاه أيضاً)")
