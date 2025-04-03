# app.py
import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# إعداد المسارات
sys.path.append(str(Path(__file__).parent.parent))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# استيراد مدير التكوين
from config_manager import ConfigManager

# استيراد الوحدات
from modules.document_analysis.document_app import DocumentAnalysisApp
from modules.pricing.pricing_app import PricingApp
from modules.resources.resources_app import ResourcesApp
from modules.risk_analysis.risk_analyzer import RiskAnalysisApp
from modules.project_management.project_management_app import ProjectsApp
from modules.maps.maps_app import MapsApp
from modules.notifications.notifications_app import NotificationsApp
from modules.document_comparison.document_comparison_app import DocumentComparisonApp
from modules.translation.translation_app import TranslationApp
from modules.ai_assistant.ai_app import AIAssistantApp
from modules.data_analysis.data_analysis_app import DataAnalysisApp
from pricing_system.modules.pricing_strategies.pricing_strategies import PricingStrategies #added import
from pricing_system.integrated_app import IntegratedApp #added import
from styling.enhanced_ui import UIEnhancer

# تهيئة مدير التكوين
config_manager = ConfigManager()

# تكوين الصفحة
config_manager.set_page_config_if_needed(
    page_title="نظام تحليل المناقصات",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.example.com/help',
        'Report a bug': "https://www.example.com/bug",
        'About': "### نظام تحليل المناقصات\nالإصدار 2.0.0"
    }
)

# تطبيق التنسيق العام
ui_enhancer = UIEnhancer(page_title="نظام تحليل المناقصات", page_icon="📊")
ui_enhancer.apply_global_styles()

# تطبيق الأنماط الموحدة المخصصة للنظام
with open("pricing_system/static/css/unified_style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# إنشاء قائمة العناصر
menu_items = [
    {"name": "لوحة المعلومات", "icon": "house"},
    {"name": "المناقصات والعقود", "icon": "file-text"},
    {"name": "تحليل المستندات", "icon": "file-earmark-text"},
    {"name": "نظام التسعير", "icon": "calculator"},
    {"name": "حاسبة تكاليف البناء", "icon": "building"},
    {"name": "الموارد والتكاليف", "icon": "people"},
    {"name": "تحليل المخاطر", "icon": "exclamation-triangle"},
    {"name": "إدارة المشاريع", "icon": "kanban"},
    {"name": "الخرائط والمواقع", "icon": "geo-alt"},
    {"name": "الجدول الزمني", "icon": "calendar3"},
    {"name": "الإشعارات", "icon": "bell"},
    {"name": "مقارنة المستندات", "icon": "files"},
    {"name": "الترجمة", "icon": "translate"},
    {"name": "المساعد الذكي", "icon": "robot"},
    {"name": "تحليل البيانات", "icon": "bar-chart"},
    {"name": "الإعدادات", "icon": "gear"}
]

# إنشاء الشريط الجانبي
selected = ui_enhancer.create_sidebar(menu_items)

# تحديد الوحدة المطلوبة بناءً على اختيار المستخدم
if selected == "لوحة المعلومات":
    ui_enhancer.create_header("لوحة المعلومات", "نظرة عامة على المناقصات والمشاريع")

    col1, col2, col3 = st.columns(3)

    with col1:
        ui_enhancer.create_metric_card("المناقصات النشطة", "12", "+3", ui_enhancer.COLORS['primary'])

    with col2:
        ui_enhancer.create_metric_card("المشاريع قيد التنفيذ", "8", "+1", ui_enhancer.COLORS['success'])

    with col3:
        ui_enhancer.create_metric_card("المناقصات المقدمة", "24", "+5", ui_enhancer.COLORS['info'])

    st.markdown("### الإشعارات الأخيرة")
    notifications = [
        {"title": "موعد تقديم مناقصة", "project": "إنشاء مبنى مستشفى الولادة والأطفال", "date": "2025-04-05", "priority": "عالية"},
        {"title": "تحديث مستندات", "project": "صيانة وتطوير طريق الملك عبدالله", "date": "2025-03-28", "priority": "متوسطة"},
        {"title": "اجتماع مراجعة التسعير", "project": "إنشاء محطة معالجة مياه الصرف الصحي", "date": "2025-03-25", "priority": "عالية"}
    ]

    for notification in notifications:
        with st.container():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{notification['title']}** - {notification['project']}")
                st.caption(f"التاريخ: {notification['date']} | الأولوية: {notification['priority']}")
            with col2:
                st.button("عرض", key=f"view_{notification['title']}")
            st.divider()

elif selected == "تحليل المستندات":
    document_app = DocumentAnalysisApp()
    document_app.run()

elif selected == "نظام التسعير":
    import streamlit as st
    from pricing_system.integrated_app import IntegratedApp

    # تهيئة النظام المتكامل
    integrated_pricing = IntegratedApp()

    # إعداد التكوين مرة واحدة في بداية التطبيق
    config_manager.set_page_config_if_needed(
        page_title="نظام التسعير المتكامل",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # عرض الشعار وعنوان النظام
    st.markdown("""
        <style>
            .title-container {
                display: flex;
                align-items: center;
                padding: 1rem;
                background-color: #f0f2f6;
                border-radius: 0.5rem;
                margin-bottom: 2rem;
            }
            .main-title {
                color: #1f77b4;
                font-size: 1.8rem;
                margin: 0;
                padding: 0;
            }
        </style>
        <div class="title-container">
            <h1 class="main-title">نظام التسعير المتكامل</h1>
        </div>
    """, unsafe_allow_html=True)

    # تشغيل النظام المتكامل
    integrated_pricing.run()


elif selected == "الموارد والتكاليف":
    resources_app = ResourcesApp()
    resources_app.run()

elif selected == "تحليل المخاطر":
    risk_app = RiskAnalysisApp()
    risk_app.run()

elif selected == "إدارة المشاريع":
    projects_app = ProjectsApp()
    projects_app.run()

elif selected == "الخرائط والمواقع":
    maps_app = MapsApp()
    maps_app.run()

elif selected == "الإشعارات":
    notifications_app = NotificationsApp()
    notifications_app.run()

elif selected == "مقارنة المستندات":
    document_comparison_app = DocumentComparisonApp()
    document_comparison_app.run()

elif selected == "الترجمة":
    translation_app = TranslationApp()
    translation_app.run()

elif selected == "المساعد الذكي":
    ai_app = AIAssistantApp()
    ai_app.run()

elif selected == "تحليل البيانات":
    data_analysis_app = DataAnalysisApp()
    data_analysis_app.run()

elif selected == "الجدول الزمني":
    from modules.scheduling.schedule_app import ScheduleApp
    schedule_app = ScheduleApp()
    schedule_app.run()

elif selected == "الإعدادات":
    ui_enhancer.create_header("الإعدادات", "إعدادات النظام والحساب")
    st.markdown("### إعدادات النظام")
    tabs = st.tabs(["إعدادات عامة", "الواجهة", "الأمان", "مفاتيح API"])

    with tabs[0]:
        st.checkbox("تفعيل الإشعارات", value=True)
        st.checkbox("حفظ تلقائي للبيانات", value=True)
        st.selectbox("اللغة", ["العربية", "English"])
        st.selectbox("المنطقة الزمنية", ["توقيت الرياض (GMT+3)", "توقيت جرينتش (GMT)"])

    with tabs[1]:
        st.radio("النمط", ["فاتح", "داكن", "تلقائي (حسب نظام التشغيل)"])
        st.slider("حجم الخط", 12, 20, 16)
        st.color_picker("لون التمييز", "#1E88E5")

    with tabs[2]:
        st.checkbox("تفعيل المصادقة الثنائية", value=False)
        st.number_input("مدة الجلسة (دقائق)", min_value=5, max_value=120, value=30)
        st.button("تغيير كلمة المرور")

    with tabs[3]:
        st.text_input("مفتاح OpenAI API", type="password")
        st.text_input("مفتاح Google Maps API", type="password")
        st.button("حفظ مفاتيح API")