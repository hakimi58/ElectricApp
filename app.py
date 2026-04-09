import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Master", page_icon="⚡")

# 2. جلب المفتاح السري
API_KEY = st.secrets.get("GOOGLE_API_KEY")

# 3. القائمة الجانبية للتنقل
st.sidebar.title("🛠️ حقيبة الفني")
choice = st.sidebar.radio("اختر الأداة:", [
    "🤖 خبير الأعطال (AI)", 
    "🧮 حاسبة الكابلات والقواطع",
    "📏 حاسبة هبوط الجهد (Voltage Drop)",
    "📑 دليل الربط السريع"
])

# --- القسم الأول: خبير الأعطال ---
if choice == "🤖 خبير الأعطال (AI)":
    st.header("🤖 مستشارك الفني الذكي")
    query = st.text_area("اشرح العطل أو اطلب نصيحة:", height=120, placeholder="مثلاً: علاش الديجونكتور يطيح كي يخدم الكليماتيزور؟")
    
    if st.button("تحليل المشكلة"):
        if query and API_KEY:
            with st.spinner("جاري استشارة قاعدة البيانات..."):
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
                payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء تونسي، أجب باللهجة التقنية التونسية وبشكل نقاط واضحة: {query}"}]}]}
                try:
                    response = requests.post(url, json=payload)
                    answer = response.json()['candidates'][0]['content']['parts'][0]['text']
                    st.success("✅ تشخيص الخبير:")
                    st.text_area("الإجابة:", value=answer, height=350)
                except:
                    st.error("مشكلة في الاتصال.")
        else:
            st.warning("اكتب سؤالك أولاً.")

# --- القسم الثاني: حاسبة الكابلات ---
elif choice == "🧮 حاسبة الكابلات والقواطع":
    st.header("🧮 تحديد المقاييس (Section & Disjoncteur)")
    watt = st.number_input("قوة الجهاز (Watt):", min_value=0, value=2500)
    
    if st.button("احسب"):
        amp = watt / 220
        if amp <= 11: res, wire = "10A", "1.5 مم²"
        elif amp <= 17: res, wire = "16A", "2.5 مم²"
        elif amp <= 24: res, wire = "25A", "4 مم²"
        else: res, wire = "32A+", "6 مم² فأكثر"
        
        st.success(f"النتيجة: تيار {amp:.1f}A ⬅️ استعمل قاطع {res} وخيط {wire}")

# --- القسم الثالث: حاسبة هبوط الجهد ---
elif choice == "📏 حاسبة هبوط الجهد (Voltage Drop)":
    st.header("📏 فحص ضياع الجهد في المسافات الطويلة")
    st.write("استخدمها لضمان وصول 220 فولت كاملة للأجهزة البعيدة.")
    
    current = st.number_input("التيار (Ampere):", value=16)
    length = st.number_input("طول الكابل (متر):", value=30)
    section = st.selectbox("مقطع السلك (مم²):", [1.5, 2.5, 4, 6, 10, 16])
    
    if st.button("احسب الضياع"):
        # معادلة تقريبية لهبوط الجهد: DeltaU = (2 * L * I) / (K * S) حيث K ناقلية النحاس
        drop = (2 * length * current) / (56 * section)
        percentage = (drop / 220) * 100
        
        st.metric("هبوط الجهد", f"{drop:.2f} Volt")
        if percentage > 3:
            st.error(f"⚠️ الضياع كبير ({percentage:.1f}%)! يجب تكبير مقطع السلك.")
        else:
            st.success(f"✅ الضياع مقبول ({percentage:.1f}%).")

# --- القسم الرابع: دليل الربط السريع ---
elif choice == "📑 دليل الربط السريع":
    st.header("📑 مخططات الربط الأساسية")
    item = st.selectbox("اختر الدارة:", ["الذهاب والإياب (Va-et-vient)", "المؤقت (Minuterie)", "المبدل (Télérupteur)"])
    
    if item == "الذهاب والإياب (Va-et-vient)":
        st.info("الربط: نحتاج مفتاحين Va-et-vient. الخيط الحامي (Phase) يدخل للـ 'Common' في المفتاح الأول، والـ 'Common' في المفتاح الثاني يذهب للمصباح. يربط المفتاحان ببعضهما عبر خيطي 'النافطة' (Navettes).")
    elif item == "المبدل (Télérupteur)":
        st.info("الربط: يحتاج أزرار ضاغطة (Boutons Poussoirs). يربط الفاز والنوتر للوشيعة (A1, A2) عبر الأزرار، والملامسات (1, 2) تقطع الفاز الذاهب للمصابيح.")
