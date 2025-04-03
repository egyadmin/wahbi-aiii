"""
وحدة تحليل البيانات - التطبيق الرئيسي
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time
import io
import os
import json
import base64
from pathlib import Path

class DataAnalysisApp:
    """وحدة تحليل البيانات"""
    
    def __init__(self):
        """تهيئة وحدة تحليل البيانات"""
        
        # تهيئة حالة الجلسة
        if 'uploaded_data' not in st.session_state:
            st.session_state.uploaded_data = None
        
        if 'data_sources' not in st.session_state:
            st.session_state.data_sources = [
                {
                    'id': 1,
                    'name': 'بيانات المناقصات السابقة',
                    'type': 'CSV',
                    'rows': 250,
                    'columns': 15,
                    'last_updated': '2024-03-01',
                    'description': 'بيانات المناقصات السابقة للشركة خلال الثلاث سنوات الماضية'
                },
                {
                    'id': 2,
                    'name': 'بيانات المنافسين',
                    'type': 'Excel',
                    'rows': 120,
                    'columns': 10,
                    'last_updated': '2024-02-15',
                    'description': 'بيانات المنافسين الرئيسيين في السوق وأسعارهم التنافسية'
                },
                {
                    'id': 3,
                    'name': 'بيانات أسعار المواد',
                    'type': 'CSV',
                    'rows': 500,
                    'columns': 8,
                    'last_updated': '2024-03-10',
                    'description': 'بيانات أسعار المواد الرئيسية المستخدمة في المشاريع'
                },
                {
                    'id': 4,
                    'name': 'بيانات الموردين',
                    'type': 'Excel',
                    'rows': 80,
                    'columns': 12,
                    'last_updated': '2024-02-20',
                    'description': 'بيانات الموردين الرئيسيين وأسعارهم وجودة منتجاتهم'
                },
                {
                    'id': 5,
                    'name': 'بيانات المشاريع المنجزة',
                    'type': 'CSV',
                    'rows': 150,
                    'columns': 20,
                    'last_updated': '2024-03-15',
                    'description': 'بيانات المشاريع المنجزة وتكاليفها الفعلية ومدة تنفيذها'
                }
            ]
        
        if 'sample_data' not in st.session_state:
            # إنشاء بيانات افتراضية للمناقصات السابقة
            np.random.seed(42)
            
            # إنشاء بيانات المناقصات السابقة
            n_tenders = 50
            tender_ids = [f"T-{2021 + i//20}-{i%20 + 1:03d}" for i in range(n_tenders)]
            tender_types = np.random.choice(["مبنى إداري", "مبنى سكني", "مدرسة", "مستشفى", "طرق", "جسور", "بنية تحتية"], n_tenders)
            tender_locations = np.random.choice(["الرياض", "جدة", "الدمام", "مكة", "المدينة", "أبها", "تبوك"], n_tenders)
            tender_areas = np.random.randint(1000, 10000, n_tenders)
            tender_durations = np.random.randint(6, 36, n_tenders)
            tender_budgets = np.random.randint(1000000, 50000000, n_tenders)
            tender_costs = np.array([budget * np.random.uniform(0.8, 1.1) for budget in tender_budgets])
            tender_profits = tender_budgets - tender_costs
            tender_profit_margins = tender_profits / tender_budgets * 100
            tender_statuses = np.random.choice(["فائز", "خاسر", "قيد التنفيذ", "منجز"], n_tenders)
            tender_dates = [f"202{1 + i//20}-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}" for i in range(n_tenders)]
            
            # إنشاء DataFrame للمناقصات السابقة
            tenders_data = {
                "رقم المناقصة": tender_ids,
                "نوع المشروع": tender_types,
                "الموقع": tender_locations,
                "المساحة (م2)": tender_areas,
                "المدة (شهر)": tender_durations,
                "الميزانية (ريال)": tender_budgets,
                "التكلفة (ريال)": tender_costs,
                "الربح (ريال)": tender_profits,
                "هامش الربح (%)": tender_profit_margins,
                "الحالة": tender_statuses,
                "تاريخ التقديم": tender_dates
            }
            
            st.session_state.sample_data = {
                "tenders": pd.DataFrame(tenders_data)
            }
            
            # إنشاء بيانات أسعار المواد
            n_materials = 30
            material_ids = [f"M-{i+1:03d}" for i in range(n_materials)]
            material_names = [
                "خرسانة جاهزة", "حديد تسليح", "طابوق", "أسمنت", "رمل", "بحص", "خشب", "ألمنيوم", "زجاج", "دهان",
                "سيراميك", "رخام", "جبس", "عازل مائي", "عازل حراري", "أنابيب PVC", "أسلاك كهربائية", "مفاتيح كهربائية",
                "إنارة", "تكييف", "مصاعد", "أبواب خشبية", "أبواب حديدية", "نوافذ ألمنيوم", "نوافذ زجاجية",
                "أرضيات خشبية", "أرضيات بلاط", "أرضيات رخام", "أرضيات سيراميك", "أرضيات بورسلين"
            ]
            material_units = np.random.choice(["م3", "طن", "م2", "كجم", "لتر", "قطعة", "متر"], n_materials)
            material_prices_2021 = np.random.randint(50, 5000, n_materials)
            material_prices_2022 = np.array([price * np.random.uniform(1.0, 1.2) for price in material_prices_2021])
            material_prices_2023 = np.array([price * np.random.uniform(1.0, 1.15) for price in material_prices_2022])
            material_prices_2024 = np.array([price * np.random.uniform(0.95, 1.1) for price in material_prices_2023])
            
            # إنشاء DataFrame لأسعار المواد
            materials_data = {
                "رمز المادة": material_ids,
                "اسم المادة": material_names,
                "الوحدة": material_units,
                "سعر 2021 (ريال)": material_prices_2021,
                "سعر 2022 (ريال)": material_prices_2022,
                "سعر 2023 (ريال)": material_prices_2023,
                "سعر 2024 (ريال)": material_prices_2024,
                "نسبة التغير 2021-2024 (%)": (material_prices_2024 - material_prices_2021) / material_prices_2021 * 100
            }
            
            st.session_state.sample_data["materials"] = pd.DataFrame(materials_data)
            
            # إنشاء بيانات المنافسين
            n_competitors = 10
            competitor_ids = [f"C-{i+1:02d}" for i in range(n_competitors)]
            competitor_names = [
                "شركة الإنشاءات المتطورة", "شركة البناء الحديث", "شركة التطوير العمراني", "شركة الإعمار الدولية",
                "شركة البنية التحتية المتكاملة", "شركة المقاولات العامة", "شركة التشييد والبناء", "شركة الهندسة والإنشاءات",
                "شركة المشاريع الكبرى", "شركة التطوير العقاري"
            ]
            competitor_specialties = np.random.choice(["مباني", "طرق", "جسور", "بنية تحتية", "متعددة"], n_competitors)
            competitor_sizes = np.random.choice(["صغيرة", "متوسطة", "كبيرة"], n_competitors)
            competitor_market_shares = np.random.uniform(1, 15, n_competitors)
            competitor_win_rates = np.random.uniform(10, 60, n_competitors)
            competitor_avg_margins = np.random.uniform(5, 20, n_competitors)
            
            # إنشاء DataFrame للمنافسين
            competitors_data = {
                "رمز المنافس": competitor_ids,
                "اسم المنافس": competitor_names,
                "التخصص": competitor_specialties,
                "الحجم": competitor_sizes,
                "حصة السوق (%)": competitor_market_shares,
                "معدل الفوز (%)": competitor_win_rates,
                "متوسط هامش الربح (%)": competitor_avg_margins
            }
            
            st.session_state.sample_data["competitors"] = pd.DataFrame(competitors_data)
    
    def run(self):
        """
        تشغيل وحدة تحليل البيانات

        هذه الدالة هي نقطة الدخول الرئيسية لوحدة تحليل البيانات.
        تقوم بتهيئة واجهة المستخدم وعرض البيانات والتحليلات.
        """
        try:
            # استخدام مدير التكوين لضبط إعدادات الصفحة
            from config_manager import ConfigManager
            config_manager = ConfigManager()
            config_manager.set_page_config_if_needed(
                page_title="وحدة تحليل البيانات - نظام المناقصات",
                page_icon="📊",
                layout="wide",
                initial_sidebar_state="expanded"
            )
            
            # تطبيق التنسيق المخصص
            st.markdown("""
            <style>
            .module-title {
                color: #2c3e50;
                text-align: center;
                font-size: 2.5rem;
                margin-bottom: 1rem;
                padding-bottom: 1rem;
                border-bottom: 2px solid #3498db;
            }
            .stTabs [data-baseweb="tab-list"] {
                gap: 10px;
            }
            .stTabs [data-baseweb="tab"] {
                height: 50px;
                white-space: pre-wrap;
                background-color: #f8f9fa;
                border-radius: 4px 4px 0px 0px;
                gap: 1px;
                padding-top: 10px;
                padding-bottom: 10px;
            }
            .stTabs [aria-selected="true"] {
                background-color: #3498db;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # عرض الشريط الجانبي
            with st.sidebar:
                st.image("assets/images/logo.png", width=200)
                st.markdown("## نظام تحليل المناقصات")
                st.markdown("### وحدة تحليل البيانات")
                
                st.markdown("---")
                
                # إضافة خيارات التصفية العامة
                st.markdown("### خيارات التصفية العامة")
                
                # إضافة مزيد من الخيارات حسب الحاجة
                st.markdown("---")
                
                # إضافة معلومات المستخدم
                st.markdown("### معلومات المستخدم")
                st.markdown("**المستخدم:** مهندس تامر الجوهري")
                st.markdown("**الدور:** محلل بيانات")
                st.markdown("**تاريخ آخر دخول:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))
            
            # عرض واجهة وحدة تحليل البيانات
            self.render()
            
            # إضافة معلومات في أسفل الصفحة
            st.markdown("---")
            st.markdown("### نظام تحليل المناقصات - وحدة تحليل البيانات")
            st.markdown("**الإصدار:** 2.0.0")
            st.markdown("**تاريخ التحديث:** 2024-03-31")
            st.markdown("**جميع الحقوق محفوظة © 2024**")
            
            return True
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء تشغيل وحدة تحليل البيانات: {str(e)}")
            return False
    
    def render(self):
        """عرض واجهة وحدة تحليل البيانات"""
        
        st.markdown("<h1 class='module-title'>وحدة تحليل البيانات</h1>", unsafe_allow_html=True)
        
        tabs = st.tabs([
            "لوحة المعلومات", 
            "تحليل المناقصات",
            "تحليل الأسعار",
            "تحليل المنافسين",
            "استيراد وتصدير البيانات"
        ])
        
        with tabs[0]:
            self._render_dashboard_tab()
        
        with tabs[1]:
            self._render_tenders_analysis_tab()
        
        with tabs[2]:
            self._render_price_analysis_tab()
        
        with tabs[3]:
            self._render_competitors_analysis_tab()
        
        with tabs[4]:
            self._render_import_export_tab()
    
    def _render_dashboard_tab(self):
        """عرض تبويب لوحة المعلومات"""
        
        st.markdown("### لوحة المعلومات")
        
        # عرض مؤشرات الأداء الرئيسية
        st.markdown("#### مؤشرات الأداء الرئيسية")
        
        # استخراج البيانات اللازمة للمؤشرات
        tenders_df = st.session_state.sample_data["tenders"]
        
        # حساب المؤشرات
        total_tenders = len(tenders_df)
        won_tenders = len(tenders_df[tenders_df["الحالة"] == "فائز"])
        win_rate = won_tenders / total_tenders * 100
        avg_profit_margin = tenders_df["هامش الربح (%)"].mean()
        total_profit = tenders_df["الربح (ريال)"].sum()
        
        # عرض المؤشرات
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("إجمالي المناقصات", f"{total_tenders}")
        
        with col2:
            st.metric("معدل الفوز", f"{win_rate:.1f}%")
        
        with col3:
            st.metric("متوسط هامش الربح", f"{avg_profit_margin:.1f}%")
        
        with col4:
            st.metric("إجمالي الربح", f"{total_profit:,.0f} ريال")
        
        # عرض توزيع المناقصات حسب الحالة
        st.markdown("#### توزيع المناقصات حسب الحالة")
        
        status_counts = tenders_df["الحالة"].value_counts().reset_index()
        status_counts.columns = ["الحالة", "العدد"]
        
        fig = px.pie(
            status_counts,
            values="العدد",
            names="الحالة",
            title="توزيع المناقصات حسب الحالة",
            color="الحالة",
            color_discrete_map={
                "فائز": "#2ecc71",
                "خاسر": "#e74c3c",
                "قيد التنفيذ": "#3498db",
                "منجز": "#f39c12"
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض توزيع المناقصات حسب نوع المشروع
        st.markdown("#### توزيع المناقصات حسب نوع المشروع")
        
        type_counts = tenders_df["نوع المشروع"].value_counts().reset_index()
        type_counts.columns = ["نوع المشروع", "العدد"]
        
        fig = px.bar(
            type_counts,
            x="نوع المشروع",
            y="العدد",
            title="توزيع المناقصات حسب نوع المشروع",
            color="نوع المشروع",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض تطور هامش الربح عبر الزمن
        st.markdown("#### تطور هامش الربح عبر الزمن")
        
        # إضافة عمود السنة
        tenders_df["السنة"] = tenders_df["تاريخ التقديم"].str[:4]
        
        # حساب متوسط هامش الربح لكل سنة
        profit_margin_by_year = tenders_df.groupby("السنة")["هامش الربح (%)"].mean().reset_index()
        
        fig = px.line(
            profit_margin_by_year,
            x="السنة",
            y="هامش الربح (%)",
            title="تطور متوسط هامش الربح عبر السنوات",
            markers=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض توزيع المناقصات حسب الموقع
        st.markdown("#### توزيع المناقصات حسب الموقع")
        
        location_counts = tenders_df["الموقع"].value_counts().reset_index()
        location_counts.columns = ["الموقع", "العدد"]
        
        fig = px.bar(
            location_counts,
            x="الموقع",
            y="العدد",
            title="توزيع المناقصات حسب الموقع",
            color="الموقع",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض العلاقة بين الميزانية والتكلفة
        st.markdown("#### العلاقة بين الميزانية والتكلفة")
        
        fig = px.scatter(
            tenders_df,
            x="الميزانية (ريال)",
            y="التكلفة (ريال)",
            color="الحالة",
            size="المساحة (م2)",
            hover_name="رقم المناقصة",
            hover_data=["نوع المشروع", "الموقع", "هامش الربح (%)"],
            title="العلاقة بين الميزانية والتكلفة",
            color_discrete_map={
                "فائز": "#2ecc71",
                "خاسر": "#e74c3c",
                "قيد التنفيذ": "#3498db",
                "منجز": "#f39c12"
            }
        )
        
        # إضافة خط الميزانية = التكلفة
        max_value = max(tenders_df["الميزانية (ريال)"].max(), tenders_df["التكلفة (ريال)"].max())
        fig.add_trace(
            go.Scatter(
                x=[0, max_value],
                y=[0, max_value],
                mode="lines",
                line=dict(color="gray", dash="dash"),
                name="الميزانية = التكلفة"
            )
        )
        st.plotly_chart(fig, use_container_width=True)

    def _render_tenders_analysis_tab(self):
        """عرض تبويب تحليل المناقصات"""
        st.markdown("### تحليل المناقصات")
        
    def _render_price_analysis_tab(self):
        """عرض تبويب تحليل الأسعار"""
        st.markdown("### تحليل الأسعار")
        
    def _render_competitors_analysis_tab(self):
        """عرض تبويب تحليل المنافسين"""
        st.markdown("### تحليل المنافسين")
        
    def _render_import_export_tab(self):
        """عرض تبويب استيراد وتصدير البيانات"""
        st.markdown("### استيراد وتصدير البيانات")

DocumentAnalysisApp = DataAnalysisApp