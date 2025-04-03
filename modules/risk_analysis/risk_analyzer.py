"""
وحدة تحليل المخاطر لنظام إدارة المناقصات - Hybrid Face
"""

import os
import logging
import threading
import datetime
import json
import math
import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import plotly.express as px

# إضافة مسار المشروع للنظام
sys.path.append(str(Path(__file__).parent.parent))

# استيراد محسن واجهة المستخدم
from styling.enhanced_ui import UIEnhancer

# تهيئة السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('risk_analysis')

"""
محلل المخاطر المتقدم للمشاريع
"""

class RiskAnalyzer:
    def __init__(self):
        self.risk_categories = [
            "مخاطر السوق",
            "مخاطر التنفيذ",
            "مخاطر العقود",
            "مخاطر التمويل",
            "مخاطر الموارد"
        ]

        self.impact_levels = {
            "منخفض": 1,
            "متوسط": 2,
            "عالي": 3,
            "حرج": 4
        }

        self.probability_levels = {
            "نادر": 1,
            "محتمل": 2,
            "مرجح": 3,
            "شبه مؤكد": 4
        }

    def analyze_risks(self, project_data):
        """تحليل المخاطر للمشروع"""
        risks = []

        # تحليل مخاطر السوق
        market_risks = self._analyze_market_risks(project_data)
        risks.extend(market_risks)

        # تحليل مخاطر التنفيذ
        execution_risks = self._analyze_execution_risks(project_data)
        risks.extend(execution_risks)

        # تحليل المخاطر المالية
        financial_risks = self._analyze_financial_risks(project_data)
        risks.extend(financial_risks)

        return pd.DataFrame(risks)

    def calculate_risk_score(self, probability, impact):
        """حساب درجة الخطر"""
        return self.probability_levels[probability] * self.impact_levels[impact]

    def render_risk_analysis(self, project_data):
        """عرض تحليل المخاطر"""
        st.header("تحليل المخاطر")

        # تحليل المخاطر
        risks_df = self.analyze_risks(project_data)

        # عرض مصفوفة المخاطر
        self._render_risk_matrix(risks_df)

        # عرض تفاصيل المخاطر
        self._render_risk_details(risks_df)

        # عرض خطة الاستجابة للمخاطر
        self._render_risk_response_plan(risks_df)

    def _render_risk_matrix(self, risks_df):
        """عرض مصفوفة المخاطر"""
        st.subheader("مصفوفة المخاطر")

        # إنشاء مصفوفة المخاطر
        matrix_data = np.zeros((4, 4))
        for _, risk in risks_df.iterrows():
            prob_idx = self.probability_levels[risk['probability']] - 1
            impact_idx = self.impact_levels[risk['impact']] - 1
            matrix_data[prob_idx, impact_idx] += 1

        fig = px.imshow(
            matrix_data,
            labels=dict(x="التأثير", y="الاحتمالية"),
            x=list(self.impact_levels.keys()),
            y=list(self.probability_levels.keys())
        )
        st.plotly_chart(fig)

    def _render_risk_details(self, risks_df):
        """عرض تفاصيل المخاطر"""
        st.subheader("تفاصيل المخاطر")

        # تصنيف المخاطر حسب درجة الخطورة
        risks_df['risk_score'] = risks_df.apply(
            lambda x: self.calculate_risk_score(x['probability'], x['impact']),
            axis=1
        )

        # عرض المخاطر مرتبة حسب درجة الخطورة
        st.dataframe(
            risks_df.sort_values('risk_score', ascending=False),
            use_container_width=True
        )

    def _render_risk_response_plan(self, risks_df):
        """عرض خطة الاستجابة للمخاطر"""
        st.subheader("خطة الاستجابة للمخاطر")

        # عرض استراتيجيات الاستجابة للمخاطر العالية
        high_risks = risks_df[risks_df['risk_score'] >= 9]

        for _, risk in high_risks.iterrows():
            with st.expander(f"{risk['category']} - {risk['description']}"):
                st.write("**استراتيجية الاستجابة:**", risk['response_strategy'])
                st.write("**خطة العمل:**", risk['action_plan'])
                st.write("**المسؤول:**", risk['responsible'])
                st.write("**الموعد النهائي:**", risk['deadline'])

    def _analyze_market_risks(self, project_data):
        """تحليل مخاطر السوق"""
        return [
            {
                'category': 'مخاطر السوق',
                'description': 'تقلبات أسعار المواد الخام',
                'probability': 'مرجح',
                'impact': 'عالي',
                'response_strategy': 'تحوط',
                'action_plan': 'التعاقد المسبق مع الموردين وتثبيت الأسعار',
                'responsible': 'مدير المشتريات',
                'deadline': '2024-03-01'
            },
            # إضافة المزيد من المخاطر
        ]

    def _analyze_execution_risks(self, project_data):
        """تحليل مخاطر التنفيذ"""
        return [
            {
                'category': 'مخاطر التنفيذ',
                'description': 'تأخر في جدول التنفيذ',
                'probability': 'محتمل',
                'impact': 'عالي',
                'response_strategy': 'تخفيف',
                'action_plan': 'إعداد خطة تسريع وتحديد المسار الحرج',
                'responsible': 'مدير المشروع',
                'deadline': '2024-02-15'
            },
            # إضافة المزيد من المخاطر
        ]

    def _analyze_financial_risks(self, project_data):
        """تحليل المخاطر المالية"""
        return [
            {
                'category': 'مخاطر التمويل',
                'description': 'تأخر الدفعات',
                'probability': 'محتمل',
                'impact': 'عالي',
                'response_strategy': 'نقل',
                'action_plan': 'التأمين على مخاطر عدم السداد',
                'responsible': 'المدير المالي',
                'deadline': '2024-02-01'
            },
            # إضافة المزيد من المخاطر
        ]


class RiskAnalysisApp:
    """تطبيق تحليل المخاطر"""
    
    def __init__(self):
        """تهيئة تطبيق تحليل المخاطر"""
        self.ui = UIEnhancer(page_title="تحليل المخاطر - نظام تحليل المناقصات", page_icon="⚠️")
        self.ui.apply_theme_colors()
        self.risk_analyzer = RiskAnalyzer()
        
        # تهيئة بيانات المشاريع
        if 'projects' not in st.session_state:
            st.session_state.projects = self._generate_sample_projects()
        
        # تهيئة نتائج التحليل
        if 'risk_analysis_results' not in st.session_state:
            st.session_state.risk_analysis_results = {}
    
    def run(self):
        """تشغيل تطبيق تحليل المخاطر"""
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
            {"name": "التقارير", "icon": "bar-chart"},
            {"name": "الإعدادات", "icon": "gear"}
        ]
        
        # إنشاء الشريط الجانبي
        selected = self.ui.create_sidebar(menu_items)
        
        # إنشاء ترويسة الصفحة
        self.ui.create_header("تحليل المخاطر", "تحديد وتقييم وإدارة مخاطر المشاريع")
        
        # عرض واجهة تحليل المخاطر
        tabs = st.tabs([
            "لوحة المعلومات",
            "تحليل المخاطر",
            "سجل المخاطر",
            "مصفوفة المخاطر",
            "استراتيجيات التخفيف"
        ])
        
        with tabs[0]:
            self._render_dashboard_tab()
        
        with tabs[1]:
            self._render_analysis_tab()
        
        with tabs[2]:
            self._render_risk_register_tab()
        
        with tabs[3]:
            self._render_risk_matrix_tab()
        
        with tabs[4]:
            self._render_mitigation_strategies_tab()
    
    def _render_dashboard_tab(self):
        """عرض تبويب لوحة المعلومات"""
        
        st.markdown("### لوحة معلومات تحليل المخاطر")
        
        # عرض إحصائيات المخاطر
        col1, col2, col3, col4 = st.columns(4)
        
        # الحصول على إحصائيات المخاطر
        total_risks = 0
        high_risks = 0
        medium_risks = 0
        low_risks = 0
        
        for project_id, results in st.session_state.risk_analysis_results.items():
            if "identified_risks" in results:
                project_risks = results["identified_risks"]
                total_risks += len(project_risks)
                high_risks += len([r for r in project_risks if r["risk_score"] >= 6])
                medium_risks += len([r for r in project_risks if 3 <= r["risk_score"] < 6])
                low_risks += len([r for r in project_risks if r["risk_score"] < 3])
        
        with col1:
            self.ui.create_metric_card("إجمالي المخاطر", str(total_risks), None, self.ui.COLORS['primary'])
        
        with col2:
            self.ui.create_metric_card("مخاطر عالية", str(high_risks), None, self.ui.COLORS['danger'])
        
        with col3:
            self.ui.create_metric_card("مخاطر متوسطة", str(medium_risks), None, self.ui.COLORS['warning'])
        
        with col4:
            self.ui.create_metric_card("مخاطر منخفضة", str(low_risks), None, self.ui.COLORS['success'])
        
        # عرض توزيع المخاطر حسب الفئة
        st.markdown("#### توزيع المخاطر حسب الفئة")
        
        # جمع بيانات توزيع المخاطر
        category_distribution = {}
        
        for project_id, results in st.session_state.risk_analysis_results.items():
            if "identified_risks" in results:
                for risk in results["identified_risks"]:
                    category = risk["category"]
                    if category not in category_distribution:
                        category_distribution[category] = 0
                    category_distribution[category] += 1
        
        if category_distribution:
            # تحويل البيانات إلى DataFrame
            category_df = pd.DataFrame({
                'الفئة': list(category_distribution.keys()),
                'عدد المخاطر': list(category_distribution.values())
            })
            
            # عرض الرسم البياني
            st.bar_chart(category_df.set_index('الفئة'))
        else:
            st.info("لا توجد بيانات كافية لعرض توزيع المخاطر.")
        
        # عرض المشاريع ذات المخاطر العالية
        st.markdown("#### المشاريع ذات المخاطر العالية")
        
        high_risk_projects = []
        
        for project_id, results in st.session_state.risk_analysis_results.items():
            if "identified_risks" in results:
                project_high_risks = len([r for r in results["identified_risks"] if r["risk_score"] >= 6])
                if project_high_risks > 0:
                    # البحث عن بيانات المشروع
                    project = next((p for p in st.session_state.projects if p["id"] == int(project_id)), None)
                    if project:
                        high_risk_projects.append({
                            'اسم المشروع': project["name"],
                            'رقم المناقصة': project["number"],
                            'الجهة المالكة': project["client"],
                            'عدد المخاطر العالية': project_high_risks
                        })
        
        if high_risk_projects:
            high_risk_df = pd.DataFrame(high_risk_projects)
            st.dataframe(high_risk_df, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد مشاريع ذات مخاطر عالية حاليًا.")
    
    def _render_analysis_tab(self):
        """عرض تبويب تحليل المخاطر"""
        
        st.markdown("### تحليل مخاطر المشروع")
        
        # اختيار المشروع
        project_options = [f"{p['name']} ({p['number']})" for p in st.session_state.projects]
        selected_project = st.selectbox("اختر المشروع", project_options)
        
        if selected_project:
            # استخراج معرف المشروع من الاختيار
            project_index = project_options.index(selected_project)
            project = st.session_state.projects[project_index]
            project_id = project["id"]
            
            # عرض معلومات المشروع
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**اسم المشروع**: {project['name']}")
                st.markdown(f"**رقم المناقصة**: {project['number']}")
                st.markdown(f"**الجهة المالكة**: {project['client']}")
            
            with col2:
                st.markdown(f"**الموقع**: {project['location']}")
                st.markdown(f"**نوع المشروع**: {project['project_type']}")
                st.markdown(f"**مستوى التعقيد**: {project['complexity']}")
            
            # زر بدء التحليل
            if st.button("بدء تحليل المخاطر"):
                with st.spinner("جاري تحليل مخاطر المشروع..."):
                    # محاكاة وقت المعالجة
                    import time
                    time.sleep(2)
                    
                    # إجراء تحليل المخاطر  (Using the new RiskAnalyzer)
                    results = self.risk_analyzer.render_risk_analysis(project)
                    
                    # تخزين النتائج في حالة الجلسة
                    st.session_state.risk_analysis_results[str(project_id)] = {"analysis_results": results}
                    
                    st.success("تم الانتهاء من تحليل المخاطر بنجاح!")
                    st.experimental_rerun()
            
    
    def _render_risk_register_tab(self):
        """عرض تبويب سجل المخاطر"""
        
        st.markdown("### سجل المخاطر")
        
        # اختيار المشروع
        project_options = [f"{p['name']} ({p['number']})" for p in st.session_state.projects]
        project_options.insert(0, "جميع المشاريع")
        selected_project_option = st.selectbox("اختر المشروع", project_options, key="risk_register_project")
        
        # جمع المخاطر المحددة
        all_risks = []
        
        if selected_project_option == "جميع المشاريع":
            # جمع المخاطر من جميع المشاريع
            for project_id, results in st.session_state.risk_analysis_results.items():
                if "analysis_results" in results:
                    project = next((p for p in st.session_state.projects if p["id"] == int(project_id)), None)
                    project_name = project["name"] if project else f"مشروع {project_id}"
                    
                    for index, row in results["analysis_results"].iterrows():
                        risk_copy = row.to_dict()
                        risk_copy["project_name"] = project_name
                        all_risks.append(risk_copy)
        else:
            # استخراج معرف المشروع من الاختيار
            project_index = project_options.index(selected_project_option) - 1  # -1 لأننا أضفنا "جميع المشاريع" في البداية
            project = st.session_state.projects[project_index]
            project_id = project["id"]
            
            # جمع المخاطر من المشروع المحدد
            if str(project_id) in st.session_state.risk_analysis_results:
                results = st.session_state.risk_analysis_results[str(project_id)]
                if "analysis_results" in results:
                    for index, row in results["analysis_results"].iterrows():
                        risk_copy = row.to_dict()
                        risk_copy["project_name"] = project["name"]
                        all_risks.append(risk_copy)
        
        # فلترة المخاطر
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_filter = st.multiselect(
                "فئة المخاطر",
                list(set(risk["category"] for risk in all_risks)) if all_risks else [],
                key="risk_register_category"
            )
        
        with col2:
            probability_filter = st.multiselect(
                "الاحتمالية",
                list(set(risk["probability"] for risk in all_risks)) if all_risks else [],
                key="risk_register_probability"
            )
        
        with col3:
            impact_filter = st.multiselect(
                "التأثير",
                list(set(risk["impact"] for risk in all_risks)) if all_risks else [],
                key="risk_register_impact"
            )
        
        # تطبيق الفلترة
        filtered_risks = all_risks
        
        if category_filter:
            filtered_risks = [risk for risk in filtered_risks if risk["category"] in category_filter]
        
        if probability_filter:
            filtered_risks = [risk for risk in filtered_risks if risk["probability"] in probability_filter]
        
        if impact_filter:
            filtered_risks = [risk for risk in filtered_risks if risk["impact"] in impact_filter]
        
        # عرض سجل المخاطر
        if filtered_risks:
            # تحويل المخاطر إلى DataFrame
            risk_df = pd.DataFrame(filtered_risks)
            
            # ترتيب المخاطر حسب درجة المخاطرة (تنازليًا)
            risk_df = risk_df.sort_values(by='risk_score', ascending=False)
            
            # عرض الجدول
            st.dataframe(risk_df, use_container_width=True, hide_index=True)
            
            # زر تصدير سجل المخاطر
            if st.button("تصدير سجل المخاطر"):
                with st.spinner("جاري تصدير سجل المخاطر..."):
                    # محاكاة وقت المعالجة
                    time.sleep(1)
                    st.success("تم تصدير سجل المخاطر بنجاح!")
        else:
            st.info("لا توجد مخاطر تطابق معايير البحث أو لم يتم إجراء تحليل للمخاطر بعد.")
    
    def _render_risk_matrix_tab(self):
        """عرض تبويب مصفوفة المخاطر"""
        
        st.markdown("### مصفوفة المخاطر")
        
        # اختيار المشروع
        project_options = [f"{p['name']} ({p['number']})" for p in st.session_state.projects]
        selected_project = st.selectbox("اختر المشروع", project_options, key="risk_matrix_project")
        
        if selected_project:
            # استخراج معرف المشروع من الاختيار
            project_index = project_options.index(selected_project)
            project = st.session_state.projects[project_index]
            project_id = project["id"]
            
            # التحقق من وجود نتائج تحليل للمشروع
            if str(project_id) in st.session_state.risk_analysis_results:
                results = st.session_state.risk_analysis_results[str(project_id)]
                
                if "analysis_results" in results:
                    risks_df = results["analysis_results"]
                    self.risk_analyzer._render_risk_matrix(risks_df)
                else:
                    st.warning("لم يتم العثور على مصفوفة المخاطر للمشروع المحدد.")
            else:
                st.warning("لم يتم إجراء تحليل للمخاطر لهذا المشروع بعد.")
    
    def _render_mitigation_strategies_tab(self):
        """عرض تبويب استراتيجيات التخفيف"""
        
        st.markdown("### استراتيجيات التخفيف من المخاطر")
        
        # اختيار المشروع
        project_options = [f"{p['name']} ({p['number']})" for p in st.session_state.projects]
        selected_project = st.selectbox("اختر المشروع", project_options, key="mitigation_project")
        
        if selected_project:
            # استخراج معرف المشروع من الاختيار
            project_index = project_options.index(selected_project)
            project = st.session_state.projects[project_index]
            project_id = project["id"]
            
            # التحقق من وجود نتائج تحليل للمشروع
            if str(project_id) in st.session_state.risk_analysis_results:
                results = st.session_state.risk_analysis_results[str(project_id)]
                
                if "analysis_results" in results and not results["analysis_results"].empty:
                    risks_df = results["analysis_results"]
                    self.risk_analyzer._render_risk_response_plan(risks_df)
                else:
                    st.warning("لم يتم العثور على استراتيجيات تخفيف للمشروع المحدد.")
            else:
                st.warning("لم يتم إجراء تحليل للمخاطر لهذا المشروع بعد.")
    
    def _generate_sample_projects(self):
        """توليد بيانات افتراضية للمشاريع"""
        
        return [
            {
                'id': 1,
                'name': "إنشاء مبنى مستشفى الولادة والأطفال بمنطقة الشرقية",
                'number': "SHPD-2025-001",
                'client': "وزارة الصحة",
                'location': "الدمام، المنطقة الشرقية",
                'description': "يشمل المشروع إنشاء وتجهيز مبنى مستشفى الولادة والأطفال بسعة 300 سرير، ويتكون المبنى من 4 طوابق بمساحة إجمالية 15,000 متر مربع.",
                'status': "قيد التسعير",
                'tender_type': "عامة",
                'pricing_method': "قياسي",
                'submission_date': (datetime.datetime.now() + datetime.timedelta(days=5)),
                'created_at': datetime.datetime.now() - datetime.timedelta(days=10),
                'created_by_id': 1,
                'project_type': "مباني",
                'complexity': "عالي"
            },
            {
                'id': 2,
                'name': "صيانة وتطوير طريق الملك عبدالله",
                'number': "MOT-2025-042",
                'client': "وزارة النقل",
                'location': "الرياض، المنطقة الوسطى",
                'description': "صيانة وتطوير طريق الملك عبدالله بطول 25 كم، ويشمل المشروع إعادة الرصف وتحسين الإنارة وتركيب اللوحات الإرشادية.",
                'status': "تم التقديم",
                'tender_type': "عامة",
                'pricing_method': "غير متزن",
                'submission_date': (datetime.datetime.now() - datetime.timedelta(days=15)),
                'created_at': datetime.datetime.now() - datetime.timedelta(days=45),
                'created_by_id': 1,
                'project_type': "بنية تحتية",
                'complexity': "متوسط"
            },
            {
                'id': 3,
                'name': "إنشاء محطة معالجة مياه الصرف الصحي",
                'number': "SWPC-2025-007",
                'client': "شركة المياه الوطنية",
                'location': "جدة، المنطقة الغربية",
                'description': "إنشاء محطة معالجة مياه الصرف الصحي بطاقة استيعابية 50,000 م3/يوم، مع جميع الأعمال المدنية والكهروميكانيكية.",
                'status': "تمت الترسية",
                'tender_type': "عامة",
                'pricing_method': "قياسي",
                'submission_date': (datetime.datetime.now() - datetime.timedelta(days=90)),
                'created_at': datetime.datetime.now() - datetime.timedelta(days=120),
                'created_by_id': 1,
                'project_type': "بنية تحتية",
                'complexity': "عالي"
            }
        ]

# تشغيل التطبيق
if __name__ == "__main__":
    risk_app = RiskAnalysisApp()
    risk_app.run()