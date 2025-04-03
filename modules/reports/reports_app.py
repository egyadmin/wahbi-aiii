import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import time

class ReportsApp:
    """وحدة التقارير والتحليلات"""

    def __init__(self):
        """تهيئة وحدة التقارير والتحليلات"""
        # تهيئة متغير السمة في حالة الجلسة إذا لم يكن موجوداً
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'

    def run(self):
        """
        تشغيل وحدة التقارير والتحليلات
        
        هذه الدالة هي نقطة الدخول الرئيسية لوحدة التقارير والتحليلات.
        تقوم بتهيئة واجهة المستخدم وعرض الوظائف المختلفة للتقارير والتحليلات.
        """
        try:
            # تعيين عنوان الصفحة
            st.set_page_config(
                page_title="وحدة التقارير والتحليلات - نظام المناقصات",
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
            
            # إضافة زر تبديل السمة في أعلى الصفحة
            col1, col2, col3 = st.columns([1, 8, 1])
            with col3:
                if st.button("🌓 تبديل السمة"):
                    # تبديل السمة
                    if st.session_state.theme == "light":
                        st.session_state.theme = "dark"
                    else:
                        st.session_state.theme = "light"
                    
                    # تطبيق السمة الجديدة وإعادة تشغيل التطبيق
                    st.rerun()
            
            # عرض الشريط الجانبي
            with st.sidebar:
                st.image("/home/ubuntu/tender_system/tender_system/assets/images/logo.png", width=200)
                st.markdown("## نظام تحليل المناقصات")
                st.markdown("### وحدة التقارير والتحليلات")
                
                st.markdown("---")
                
                # إضافة خيارات تصفية التقارير
                st.markdown("### خيارات التصفية")
                
                # تصفية حسب الفترة الزمنية
                date_range = st.selectbox(
                    "الفترة الزمنية",
                    ["آخر 7 أيام", "آخر 30 يوم", "آخر 90 يوم", "آخر 365 يوم", "كل الفترات"]
                )
                
                # تصفية حسب نوع المشروع
                project_type = st.multiselect(
                    "نوع المشروع",
                    ["مباني", "طرق", "جسور", "أنفاق", "بنية تحتية", "أخرى"],
                    default=["مباني", "طرق", "جسور", "أنفاق", "بنية تحتية", "أخرى"]
                )
                
                # تصفية حسب حالة المشروع
                project_status = st.multiselect(
                    "حالة المشروع",
                    ["جديد", "قيد التقديم", "تم التقديم", "فائز", "خاسر", "ملغي"],
                    default=["جديد", "قيد التقديم", "تم التقديم", "فائز", "خاسر"]
                )
                
                # زر تطبيق التصفية
                if st.button("تطبيق التصفية"):
                    st.success("تم تطبيق التصفية بنجاح!")
                
                st.markdown("---")
                
                # إضافة معلومات المستخدم
                st.markdown("### معلومات المستخدم")
                st.markdown("**المستخدم:** مهندس تامر الجوهري")
                st.markdown("**الدور:** محلل مناقصات")
                st.markdown("**تاريخ آخر دخول:** " + datetime.now().strftime("%Y-%m-%d %H:%M"))
            
            # عرض واجهة وحدة التقارير والتحليلات
            self.render()
            
            # إضافة معلومات في أسفل الصفحة
            st.markdown("---")
            st.markdown("### نظام تحليل المناقصات - وحدة التقارير والتحليلات")
            st.markdown("**الإصدار:** 2.0.0")
            st.markdown("**تاريخ التحديث:** 2025-03-31")
            st.markdown("**جميع الحقوق محفوظة © 2025**")
            
            return True
            
        except Exception as e:
            st.error(f"حدث خطأ أثناء تشغيل وحدة التقارير والتحليلات: {str(e)}")
            return False

    def render(self):
        """عرض واجهة وحدة التقارير والتحليلات"""
        
        st.markdown("<h1 class='module-title'>وحدة التقارير والتحليلات</h1>", unsafe_allow_html=True)
        
        tabs = st.tabs(["لوحة المعلومات", "تقارير المشاريع", "تقارير التسعير", "تقارير المخاطر", "التقارير المخصصة"])
        
        with tabs[0]:
            self._render_dashboard_tab()
        
        with tabs[1]:
            self._render_projects_reports_tab()
        
        with tabs[2]:
            self._render_pricing_reports_tab()
        
        with tabs[3]:
            self._render_risk_reports_tab()
        
        with tabs[4]:
            self._render_custom_reports_tab()

    def _render_dashboard_tab(self):
        """عرض تبويب لوحة المعلومات"""
        
        st.markdown("### لوحة معلومات النظام")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_projects = self._get_total_projects()
            st.metric("إجمالي المشاريع", total_projects)
        
        with col2:
            active_projects = self._get_active_projects()
            st.metric("المشاريع النشطة", active_projects, delta=f"{active_projects/total_projects*100:.1f}%" if total_projects > 0 else "0%")
        
        with col3:
            won_projects = self._get_won_projects()
            st.metric("المشاريع المرساة", won_projects, delta=f"{won_projects/total_projects*100:.1f}%" if total_projects > 0 else "0%")
        
        with col4:
            avg_local_content = self._get_avg_local_content()
            st.metric("متوسط المحتوى المحلي", f"{avg_local_content:.1f}%", delta=f"{avg_local_content-70:.1f}%" if avg_local_content > 0 else "0%")
        
        st.markdown("#### توزيع المشاريع حسب الحالة")
        project_status_data = self._get_project_status_data()
        fig = px.pie(project_status_data, values='count', names='status', title='توزيع المشاريع حسب الحالة', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### اتجاه المشاريع الشهري")
        monthly_data = self._get_monthly_project_data()
        fig = px.line(monthly_data, x='month', y=['new', 'submitted', 'won'], title='اتجاه المشاريع الشهري')
        st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### توزيع المشاريع حسب النوع")
            project_type_data = self._get_project_type_data()
            fig = px.bar(project_type_data, x='type', y='count', title='توزيع المشاريع حسب النوع')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### توزيع المشاريع حسب الموقع")
            project_location_data = self._get_project_location_data()
            fig = px.bar(project_location_data, x='location', y='count', title='توزيع المشاريع حسب الموقع')
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### أحدث المشاريع")
        latest_projects = self._get_latest_projects()
        st.dataframe(latest_projects)

    def _render_projects_reports_tab(self):
        """عرض تبويب تقارير المشاريع"""
        
        st.markdown("### تقارير المشاريع")
        
        report_type = st.selectbox(
            "نوع التقرير",
            ["تقرير حالة المشاريع", "تقرير أداء المشاريع", "تقرير المشاريع المتأخرة", "تقرير المشاريع المكتملة"]
        )
        
        if report_type == "تقرير حالة المشاريع":
            self._render_project_status_report()
        elif report_type == "تقرير أداء المشاريع":
            self._render_project_performance_report()
        elif report_type == "تقرير المشاريع المتأخرة":
            self._render_delayed_projects_report()
        elif report_type == "تقرير المشاريع المكتملة":
            self._render_completed_projects_report()

    def _render_pricing_reports_tab(self):
        """عرض تبويب تقارير التسعير"""
        
        st.markdown("### تقارير التسعير")
        
        report_type = st.selectbox(
            "نوع التقرير",
            ["تقرير تحليل الأسعار", "تقرير مقارنة الأسعار", "تقرير اتجاهات الأسعار", "تقرير تحليل المنافسين"]
        )
        
        if report_type == "تقرير تحليل الأسعار":
            self._render_price_analysis_report()
        elif report_type == "تقرير مقارنة الأسعار":
            self._render_price_comparison_report()
        elif report_type == "تقرير اتجاهات الأسعار":
            self._render_price_trends_report()
        elif report_type == "تقرير تحليل المنافسين":
            self._render_competitors_analysis_report()

    def _render_risk_reports_tab(self):
        """عرض تبويب تقارير المخاطر"""
        
        st.markdown("### تقارير المخاطر")
        
        report_type = st.selectbox(
            "نوع التقرير",
            ["تقرير تحليل المخاطر", "تقرير مصفوفة المخاطر", "تقرير متابعة المخاطر", "تقرير استراتيجيات التخفيف"]
        )
        
        if report_type == "تقرير تحليل المخاطر":
            self._render_risk_analysis_report()
        elif report_type == "تقرير مصفوفة المخاطر":
            self._render_risk_matrix_report()
        elif report_type == "تقرير متابعة المخاطر":
            self._render_risk_monitoring_report()
        elif report_type == "تقرير استراتيجيات التخفيف":
            self._render_risk_mitigation_report()

    def _render_custom_reports_tab(self):
        """عرض تبويب التقارير المخصصة"""
        
        st.markdown("### التقارير المخصصة")
        
        st.markdown("#### إنشاء تقرير مخصص")
        
        col1, col2 = st.columns(2)
        
        with col1:
            report_name = st.text_input("اسم التقرير")
            report_description = st.text_area("وصف التقرير")
        
        with col2:
            report_fields = st.multiselect(
                "حقول التقرير",
                ["رقم المشروع", "اسم المشروع", "نوع المشروع", "حالة المشروع", "تاريخ البدء", "تاريخ الانتهاء", "الميزانية", "التكلفة الفعلية", "نسبة الإنجاز", "المخاطر", "الموقع", "المالك", "المقاول"]
            )
            
            report_filters = st.multiselect(
                "تصفية التقرير",
                ["نوع المشروع", "حالة المشروع", "الفترة الزمنية", "الميزانية", "الموقع", "المالك", "المقاول"]
            )
        
        if st.button("إنشاء التقرير"):
            if report_name and report_description and report_fields:
                with st.spinner("جاري إنشاء التقرير..."):
                    time.sleep(2)  # محاكاة وقت المعالجة
                    st.success("تم إنشاء التقرير بنجاح!")
                    
                    # عرض التقرير المخصص (محاكاة)
                    custom_report_data = self._generate_custom_report(report_fields)
                    st.dataframe(custom_report_data)
                    
                    # تصدير التقرير
                    st.download_button(
                        label="تصدير التقرير (Excel)",
                        data=self._export_to_excel(custom_report_data),
                        file_name=f"{report_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
            else:
                st.warning("يرجى ملء جميع الحقول المطلوبة")
        
        st.markdown("#### التقارير المخصصة المحفوظة")
        
        saved_reports = [
            {"id": 1, "name": "تقرير المشاريع المتأخرة في الرياض", "created_at": "2025-03-15", "last_run": "2025-03-30"},
            {"id": 2, "name": "تقرير مشاريع الطرق ذات المخاطر العالية", "created_at": "2025-03-10", "last_run": "2025-03-28"},
            {"id": 3, "name": "تقرير المشاريع المكتملة في الربع الأول", "created_at": "2025-03-05", "last_run": "2025-03-25"}
        ]
        
        saved_reports_df = pd.DataFrame(saved_reports)
        st.dataframe(saved_reports_df)

    # تنفيذ دوال الحصول على البيانات
    
    def _get_total_projects(self):
        """الحصول على إجمالي عدد المشاريع"""
        # محاكاة البيانات
        return 120
    
    def _get_active_projects(self):
        """الحصول على عدد المشاريع النشطة"""
        # محاكاة البيانات
        return 45
    
    def _get_won_projects(self):
        """الحصول على عدد المشاريع المرساة"""
        # محاكاة البيانات
        return 30
    
    def _get_avg_local_content(self):
        """الحصول على متوسط المحتوى المحلي"""
        # محاكاة البيانات
        return 75.5
    
    def _get_project_status_data(self):
        """الحصول على بيانات توزيع المشاريع حسب الحالة"""
        # محاكاة البيانات
        data = {
            'status': ['جديد', 'قيد التقديم', 'تم التقديم', 'فائز', 'خاسر', 'ملغي'],
            'count': [25, 20, 15, 30, 25, 5]
        }
        return pd.DataFrame(data)
    
    def _get_monthly_project_data(self):
        """الحصول على بيانات اتجاه المشاريع الشهري"""
        # محاكاة البيانات
        data = {
            'month': ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو'],
            'new': [10, 15, 12, 8, 20, 18],
            'submitted': [8, 12, 10, 6, 15, 14],
            'won': [5, 8, 6, 4, 10, 9]
        }
        return pd.DataFrame(data)
    
    def _get_project_type_data(self):
        """الحصول على بيانات توزيع المشاريع حسب النوع"""
        # محاكاة البيانات
        data = {
            'type': ['مباني', 'طرق', 'جسور', 'أنفاق', 'بنية تحتية', 'أخرى'],
            'count': [40, 30, 15, 10, 20, 5]
        }
        return pd.DataFrame(data)
    
    def _get_project_location_data(self):
        """الحصول على بيانات توزيع المشاريع حسب الموقع"""
        # محاكاة البيانات
        data = {
            'location': ['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة', 'أخرى'],
            'count': [35, 25, 20, 15, 10, 15]
        }
        return pd.DataFrame(data)
    
    def _get_latest_projects(self):
        """الحصول على بيانات أحدث المشاريع"""
        # محاكاة البيانات
        data = {
            'رقم المشروع': ['P-2025-001', 'P-2025-002', 'P-2025-003', 'P-2025-004', 'P-2025-005'],
            'اسم المشروع': ['إنشاء مبنى إداري', 'تطوير شبكة طرق', 'إنشاء جسر', 'بناء مدرسة', 'تطوير شبكة مياه'],
            'نوع المشروع': ['مباني', 'طرق', 'جسور', 'مباني', 'بنية تحتية'],
            'حالة المشروع': ['جديد', 'قيد التقديم', 'تم التقديم', 'فائز', 'جديد'],
            'تاريخ الإضافة': ['2025-03-30', '2025-03-28', '2025-03-25', '2025-03-20', '2025-03-18']
        }
        return pd.DataFrame(data)
    
    # تنفيذ دوال عرض التقارير
    
    def _render_project_status_report(self):
        """عرض تقرير حالة المشاريع"""
        
        st.markdown("#### تقرير حالة المشاريع")
        
        # محاكاة بيانات التقرير
        data = {
            'رقم المشروع': ['P-2025-001', 'P-2025-002', 'P-2025-003', 'P-2025-004', 'P-2025-005', 'P-2025-006', 'P-2025-007', 'P-2025-008', 'P-2025-009', 'P-2025-010'],
            'اسم المشروع': ['إنشاء مبنى إداري', 'تطوير شبكة طرق', 'إنشاء جسر', 'بناء مدرسة', 'تطوير شبكة مياه', 'إنشاء مستشفى', 'بناء مركز تجاري', 'تطوير حديقة عامة', 'إنشاء مصنع', 'تطوير مطار'],
            'نوع المشروع': ['مباني', 'طرق', 'جسور', 'مباني', 'بنية تحتية', 'مباني', 'مباني', 'أخرى', 'مباني', 'بنية تحتية'],
            '
(Content truncated due to size limit. Use line ranges to read in chunks)
        