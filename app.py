import streamlit as st
import requests
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Business", page_icon="💰", layout="wide")

# تنسيق واجهة احترافية
st.markdown("""
    <style>
    .stHeader { background-color: #2c3e50; color: white; padding: 10px; border-radius: 10px; }
    .stButton>button { background-color: #27ae60; color: white; border-radius: 20px; }
    .report-box { background-color: #ffffff; border: 2px solid #ecf0f1; padding: 20px; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# العنوان
st.title("⚡ منصة الكهربائي المحترف (النسخة التجارية)")

# القائمة الجانبية للتنقل
menu = st.sidebar.radio("اختر الأداة:", ["الرئيسية", "إنشاء فاتورة تقديرية (Devis)", "حاسبة الأحمال", "خبير الذكاء الاصطناعي"])

API_KEY = st.secrets.get("GOOGLE_API_KEY")

# --- الخيار 1: إنشاء فاتورة تقديرية (هذه هي ميزة جني المال) ---
if menu == "إنشاء فاتورة تقديرية (Devis)":
    st.header("📋 منشئ التقديرات المالية (Devis)")
    with st.form("devis_form"):
        client_name = st.text_input("اسم الزبون:")
        project_type = st.selectbox("نوع العمل:", ["تركيب منزل جديد", "إصلاح عطل", "صيانة مكيف", "تركيب كاميرات"])
        
        st.write("--- تفاصيل المواد والعمل ---")
        items = st.text_area("أدخل المواد والخدمات (مثلاً: 5 قواطع، 2 لفات خيط، يد عاملة...):")
        total_price = st.number_input("المبلغ الإجمالي التقديري (DT):", min_value=0)
        
        submit_devis = st.form_submit_button("إنشاء مسودة الفاتورة")
        
        if submit_devis:
            st.success("تم إنشاء التقدير بنجاح!")
            devis_text = f"""
            === تقدير كلفة عمل كهربائي ===
            التاريخ: {datetime.now().strftime('%Y-%m-%d')}
            الزبون: {client_name}
            نوع المهمة: {project_type}
            ---------------------------
            التفاصيل:
            {items}
            ---------------------------
            المبلغ الجملي: {total_price} دينار تونس
            ---------------------------
            شكراً لثقتكم - فني كهرباء محترف
            """
            st.code(devis_text, language="text")
            st.download_button("تحميل الفاتورة كملف نصي", devis_text, file_name=f"Devis_{client_name}.txt")

# --- الخيار 2: حاسبة الأحمال (أداة ميدانية) ---
elif menu == "حاسبة الأحمال":
    st.header("🧮 حسابات السلك والقاطع")
    col1, col2 = st.columns(2)
    with col1:
        watt = st.number_input("القوة بالواط (W):", value=2000)
        dist = st.number_input("المسافة (متر):", value=10)
    with col2:
        amp = watt / 220
        st.metric("التيار (Ampere)", f"{amp:.2f} A")
        
        if amp <= 10: rec = "خيط 1.5 مم² + ديجونكتور 10A"
        elif amp <= 16: rec = "خيط 2.5 مم² + ديجونكتور 16A"
        else: rec = "خيط 4 مم² أو أكثر + ديجونكتور 25A"
        st.info(f"النتيجة المقترحة: {rec}")

# --- الخيار 3: الذكاء الاصطناعي (الدعم الفني) ---
elif menu == "خبير الذكاء الاصطناعي":
    st.header("🤖 استشارة تقنية فورية")
    problem = st.text_area("اشرح العطل التقني:")
    if st.button("تحليل العطل"):
        if problem and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء، أجب باللهجة التونسية التقنية: {problem}"}]}]}
            res = requests.post(url, json=payload)
            st.text_area("رد الخبير:", value=res.json()['candidates'][0]['content']['parts'][0]['text'], height=200)

# --- الصفحة الرئيسية ---
else:
    st.write("### مرحباً بك في رفيقك المهني اليومي")
    st.info("استخدم القائمة الجانبية للوصول إلى الأدوات.")
    
    st.subheader("📌 مرجع سريع للألوان (المواصفات التونسية)")
    st.table({
        "السلك": ["Phase (حامي)", "Neutre (بارد)", "Terre (أرضي)"],
        "اللون": ["أحمر / بني / أسود", "أزرق", "أخضر وأصفر"]
    })
