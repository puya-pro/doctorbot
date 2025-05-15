# Libraries
import streamlit as st
from dotenv import load_dotenv
import os
import requests

# Load API key from .env
load_dotenv()
api_key = os.getenv("NEW_API_KEY")

# استایل تاریک با فونت فارسی یکپارچه
st.set_page_config(
        page_title="Doctor Bot",
        page_icon="",
        layout="centered",
    )

st.markdown("""
<style>
    /* بارگذاری و تنظیم فونت وزیر برای تمام عناصر */
    @font-face {
        font-family: 'Vazirmatn';
        font-style: normal;
        font-weight: 100 900;
        src: url('https://cdn.jsdelivr.net/gh/rastikerdar/vazirmatn@v33.003/fonts/webfonts/Vazirmatn-Regular.woff2') format('woff2');
        font-display: swap;
    }
    
    /* اعمال فونت فارسی به تمام عناصر */
    * {
        font-family: 'Vazirmatn', sans-serif !important;
    }
    
    /* تنظیمات پایه */
    html, body, [class*="css"] {
        direction: rtl !important;
        text-align: right !important;
        background-color: #121212 !important;
        color: #ffffff !important;
    }
    
    /* استایل دکمه‌ها */
    button, .stButton>button, .stDownloadButton>button {
        background-color: #1E88E5 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5em 1em !important;
        font-weight: 500 !important;
    }
    
    /* استایل ورودی‌ها */
    .stTextInput input, 
    .stNumberInput input,
    .stTextArea textarea,
    .stSelectbox select,
    .stSlider span {
        background-color: #1E1E1E !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
    }
    
    /* استایل عناصر خاص */
    .stAlert, .stWarning, .stError, .stSuccess {
        font-family: 'Vazirmatn' !important;
        border-radius: 8px !important;
    }
    
    /* استایل عنوان‌ها */
    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #1E88E5 !important;
        text-align: right !important;
        font-weight: 700 !important;
    }
    
    /* استایل متن‌های معمولی */
    p, div, span, label {
        font-family: 'Vazirmatn' !important;
    }
    
    /* استایل پاپ آپ‌ها و منوها */
    .st-b7, .st-c0, .st-c1, .st-c2 {
        font-family: 'Vazirmatn' !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖دکتر بات")

# گرفتن ورودی‌ها از کاربر
name = st.text_input("نام و نام خانوادگی:")
age = st.number_input("سن:", min_value=1, max_value=120, step=1)
gender = st.selectbox("جنسیت:", ["مرد", "زن"])
weight = st.number_input("وزن (کیلوگرم):", min_value=1, max_value=300, step=1)
height = st.number_input("قد (سانتی‌متر):", min_value=50, max_value=250, step=1)
symptoms = st.text_area("علائم بیماری:", placeholder="مثال: سردرد، تب، گلودرد")
pain_location = st.text_input("محل درد:")
severity = st.text_input("شدت درد: ")
duration = st.text_input("مدت زمان شروع علائم:")
allergies = st.text_input("آلرژی دارویی:")
medications = st.text_input("داروهای مصرفی فعلی:")
user_guess = st.text_input("حدس خود بیمار:")

if st.button("ارسال برای تشخیص"):
    if not symptoms:
        st.warning("لطفاً علائم را وارد کنید.")
    else:
        with st.spinner("در حال ارسال اطلاعات به مدل هوش مصنوعی..."):
            headers = {
                "Authorization": f"Bearer {api_key}"
            }
            user_message = f"""
            نام: {name}
            سن: {age}
            جنسیت: {gender}
            وزن: {weight} کیلوگرم
            قد: {height} سانتی‌متر
            علائم: {symptoms}
            محل درد: {pain_location}
            شدت درد : {severity}
            مدت زمان شروع علائم: {duration}
            آلرژی دارویی: {allergies}
            داروهای مصرفی فعلی: {medications}
            حدس خود بیمار: {user_guess}
            
            لطفاً یک تشخیص دقیق پزشکی، دارو، برنامه درمانی و جدول زمان‌بندی دارو ارائه بده.
            """

            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": "deepseek/deepseek-chat:free",
                    "messages": [
                        {"role": "user", "content": user_message}
                    ]
                }
            )

            if response.status_code == 200:
                result = response.json()["choices"][0]["message"]["content"]
                st.success("✅ پاسخ مدل هوش مصنوعی:")
                st.markdown(f'<div style="background-color:#1E1E1E; padding:15px; border-radius:8px; line-height: 1.8;">{result}</div>', unsafe_allow_html=True)
            else:
                st.error("❌ خطا در دریافت پاسخ از مدل. لطفاً API یا اتصال را بررسی کنید.")