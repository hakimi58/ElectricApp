import streamlit as st
import requests

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tunisia Electric Pro - Devis", page_icon="📈")

# 2. قاعدة بيانات الأسعار (أسعار تقريبية قابلة للتعديل)
PRICES = {
    "سلك 1.5 مم² (لفة 100م)": 85.000,
    "سلك 2.5 مم² (لفة 100م)": 135.000,
    "ديجونكتور 10A/16A (نوع جيد)": 12.500,
    "ديجونكتور 20A/32A": 15.000,
    "لوحة توزيع (8 قواطع)": 45.000,
    "منقذ فرعي (Interrupteur Diff)": 85.000,
    "علبة تفرع (Boite de dérivation)": 1.500,
    "يومية فني كهرباء (يد عاملة)": 80.000,
    "يومية مساعد (Aide)": 40.000
}

st.title("⚡ نظام إدارة الفواتير والأرباح")
st.markdown("---")

# القائمة الجانبية
choice = st.sidebar.selectbox("اختر المهمة:", ["حساب كلفة مشروع", "استشارة فنية (AI)"])

if choice == "حساب كلفة مشروع":
    st.header("📋 تقدير ميزانية العمل (Devis)")
    
    # اختيار المواد
    st.subheader("1. اختر المواد اللازمة:")
    selected_items = {}
    
    col1, col2 = st.columns(2)
    with col1:
        for item in list(PRICES.keys())[:4]:
            qty = st.number_input(f"كمية {item}:", min_value=0, step=1, key=item)
            if qty > 0:
                selected_items[item] = qty
    
    with col2:
        for item in list(PRICES.keys())[4:]:
            qty = st.number_input(f"كمية {item}:", min_value=0, step=1, key=item)
            if qty > 0:
                selected_items[item] = qty

    # عرض الفاتورة
    if st.button("توليد الفاتورة النهائية"):
        st.markdown("### 📝 تفاصيل الفاتورة التقديرية")
        total_sum = 0
        invoice_text = "المادة | الكمية | الثمن\n---|---|---\n"
        
        for item, qty in selected_items.items():
            subtotal = qty * PRICES[item]
            total_sum += subtotal
            invoice_text += f"{item} | {qty} | {subtotal:.3f} DT\n"
        
        st.markdown(invoice_text)
        st.warning(f"### 💰 المبلغ الإجمالي: {total_sum:.3f} دينار تونسي")
        
        # ميزة حفظ البيانات
        st.download_button("تحميل الفاتورة للزبون (Text)", 
                           f"فاتورة تقديرية\n\n{invoice_text}\nالمجموع: {total_sum:.3f} DT", 
                           file_name="Devis_Tunisia_Electric.txt")

elif choice == "استشارة فنية (AI)":
    st.header("🤖 مساعدك الذكي في الميدان")
    API_KEY = st.secrets.get("GOOGLE_API_KEY")
    query = st.text_area("اشرح المشكل (مثلاً: طريقة ربط Télérupteur):")
    
    if st.button("اسأل الخبير"):
        if query and API_KEY:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
            payload = {"contents": [{"parts": [{"text": f"أنت خبير كهرباء، أجب باللهجة التونسية: {query}"}]}]}
            res = requests.post(url, json=payload)
            st.code(res.json()['candidates'][0]['content']['parts'][0]['text'], language="text")
