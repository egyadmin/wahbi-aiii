"""
وحدة إدارة المشاريع - نظام تحليل المناقصات
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import time
import io
import sys
from pathlib import Path

# إضافة مسار المشروع للنظام
sys.path.append(str(Path(__file__).parent.parent))

# استيراد محسن واجهة المستخدم
from styling.enhanced_ui import UIEnhancer

class ProjectsApp:
    """وحدة إدارة المشاريع"""
    
    def __init__(self):
        """تهيئة وحدة إدارة المشاريع"""
        self.ui = UIEnhancer(page_title="إدارة المشاريع - نظام تحليل المناقصات", page_icon="📋")
        self.ui.apply_theme_colors()
        
        # تهيئة البيانات المبدئية
        if 'projects' not in st.session_state:
            st.session_state.projects = self._generate_sample_projects()
    
    def run(self):
        """تشغيل وحدة إدارة المشاريع"""
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
        self.ui.create_header("إدارة المشاريع", "إدارة ومتابعة المشاريع والمناقصات")
        
        # عرض واجهة وحدة إدارة المشاريع
        tabs = st.tabs([
            "قائمة المشاريع",
            "إضافة مشروع جديد",
            "تفاصيل المشروع",
            "متابعة المشاريع"
        ])
        
        with tabs[0]:
            self._render_projects_list_tab()
        
        with tabs[1]:
            self._render_add_project_tab()
        
        with tabs[2]:
            self._render_project_details_tab()
        
        with tabs[3]:
            self._render_projects_tracking_tab()
    
    def _render_projects_list_tab(self):
        """عرض تبويب قائمة المشاريع"""
        
        st.markdown("### قائمة المشاريع")
        
        # فلترة المشاريع
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("البحث في المشاريع", key="project_search")
        
        with col2:
            status_filter = st.multiselect(
                "حالة المشروع",
                ["جديد", "قيد التسعير", "تم التقديم", "تمت الترسية", "قيد التنفيذ", "منتهي", "ملغي"],
                default=["جديد", "قيد التسعير", "تم التقديم"],
                key="project_status_filter"
            )
        
        with col3:
            client_filter = st.multiselect(
                "الجهة المالكة",
                list(set([p['client'] for p in st.session_state.projects])),
                key="project_client_filter"
            )
        
        # تطبيق الفلترة
        filtered_projects = st.session_state.projects
        
        if search_term:
            filtered_projects = [p for p in filtered_projects if search_term.lower() in p['name'].lower() or search_term in p['number']]
        
        if status_filter:
            filtered_projects = [p for p in filtered_projects if p['status'] in status_filter]
        
        if client_filter:
            filtered_projects = [p for p in filtered_projects if p['client'] in client_filter]
        
        # تحويل المشاريع المفلترة إلى DataFrame للعرض
        if filtered_projects:
            projects_df = pd.DataFrame(filtered_projects)
            
            # اختيار وترتيب الأعمدة
            display_columns = [
                'name', 'number', 'client', 'location', 'status',
                'submission_date', 'tender_type', 'created_at'
            ]
            
            # تغيير أسماء الأعمدة للعرض
            column_names = {
                'name': 'اسم المشروع',
                'number': 'رقم المناقصة',
                'client': 'الجهة المالكة',
                'location': 'الموقع',
                'status': 'الحالة',
                'submission_date': 'تاريخ التقديم',
                'tender_type': 'نوع المناقصة',
                'created_at': 'تاريخ الإنشاء'
            }
            
            display_df = projects_df[display_columns].rename(columns=column_names)
            
            # تنسيق التواريخ
            date_columns = ['تاريخ التقديم', 'تاريخ الإنشاء']
            for col in date_columns:
                if col in display_df.columns:
                    display_df[col] = pd.to_datetime(display_df[col]).dt.strftime('%Y-%m-%d')
            
            # عرض الجدول
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # زر تصدير المشاريع
            if st.button("تصدير المشاريع إلى Excel"):
                # محاكاة التصدير
                st.success("تم تصدير المشاريع بنجاح!")
        else:
            st.info("لا توجد مشاريع تطابق معايير البحث.")
    
    def _render_add_project_tab(self):
        """عرض تبويب إضافة مشروع جديد"""
        
        st.markdown("### إضافة مشروع جديد")
        
        # نموذج إدخال بيانات المشروع
        with st.form("new_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_name = st.text_input("اسم المشروع", key="new_project_name")
                client = st.text_input("الجهة المالكة", key="new_project_client")
                location = st.text_input("الموقع", key="new_project_location")
                tender_type = st.selectbox(
                    "نوع المناقصة",
                    ["عامة", "خاصة", "أمر مباشر"],
                    key="new_project_tender_type"
                )
            
            with col2:
                tender_number = st.text_input("رقم المناقصة", key="new_project_number")
                submission_date = st.date_input("تاريخ التقديم", key="new_project_submission_date")
                pricing_method = st.selectbox(
                    "طريقة التسعير",
                    ["قياسي", "غير متزن", "تنافسي", "موجه بالربحية"],
                    key="new_project_pricing_method"
                )
                status = st.selectbox(
                    "حالة المشروع",
                    ["جديد", "قيد التسعير", "تم التقديم", "تمت الترسية", "قيد التنفيذ", "منتهي", "ملغي"],
                    index=0,
                    key="new_project_status"
                )
            
            description = st.text_area("وصف المشروع", key="new_project_description")
            
            submitted = st.form_submit_button("إضافة المشروع")
            
            if submitted:
                # التحقق من تعبئة الحقول الإلزامية
                if not project_name or not tender_number or not client:
                    st.error("يرجى تعبئة جميع الحقول الإلزامية (اسم المشروع، رقم المناقصة، الجهة المالكة).")
                else:
                    # إنشاء مشروع جديد
                    new_project = {
                        'id': len(st.session_state.projects) + 1,
                        'name': project_name,
                        'number': tender_number,
                        'client': client,
                        'location': location,
                        'description': description,
                        'status': status,
                        'tender_type': tender_type,
                        'pricing_method': pricing_method,
                        'submission_date': submission_date,
                        'created_at': datetime.now(),
                        'created_by_id': 1  # معرف المستخدم الحالي
                    }
                    
                    # إضافة المشروع إلى قائمة المشاريع
                    st.session_state.projects.append(new_project)
                    
                    # رسالة نجاح
                    st.success(f"تم إضافة المشروع [{project_name}] بنجاح!")
                    
                    # تعيين المشروع الحالي
                    st.session_state.current_project = new_project
    
    def _render_project_details_tab(self):
        """عرض تبويب تفاصيل المشروع"""
        
        st.markdown("### تفاصيل المشروع")
        
        # التحقق من وجود مشروع حالي
        if 'current_project' not in st.session_state or st.session_state.current_project is None:
            # إذا لم يكن هناك مشروع محدد، اعرض قائمة باختيار المشروع
            project_names = [p['name'] for p in st.session_state.projects]
            selected_project_name = st.selectbox("اختر المشروع", project_names)
            
            if selected_project_name:
                selected_project = next((p for p in st.session_state.projects if p['name'] == selected_project_name), None)
                if selected_project:
                    st.session_state.current_project = selected_project
                else:
                    st.warning("لم يتم العثور على المشروع المحدد.")
                    return
            else:
                st.info("يرجى اختيار مشروع لعرض تفاصيله.")
                return
        
        # عرض تفاصيل المشروع
        project = st.session_state.current_project
        
        # عرض معلومات المشروع الأساسية
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**اسم المشروع**: {project['name']}")
            st.markdown(f"**رقم المناقصة**: {project['number']}")
            st.markdown(f"**الجهة المالكة**: {project['client']}")
        
        with col2:
            st.markdown(f"**الموقع**: {project['location']}")
            st.markdown(f"**نوع المناقصة**: {project['tender_type']}")
            st.markdown(f"**حالة المشروع**: {project['status']}")
        
        with col3:
            st.markdown(f"**طريقة التسعير**: {project['pricing_method']}")
            st.markdown(f"**تاريخ التقديم**: {project['submission_date'].strftime('%Y-%m-%d') if isinstance(project['submission_date'], datetime) else project['submission_date']}")
            st.markdown(f"**تاريخ الإنشاء**: {project['created_at'].strftime('%Y-%m-%d') if isinstance(project['created_at'], datetime) else project['created_at']}")
        
        # عرض وصف المشروع
        st.markdown("#### وصف المشروع")
        st.text_area("", value=project.get('description', ''), disabled=True, height=100)
        
        # عرض المستندات المرتبطة بالمشروع
        st.markdown("#### مستندات المشروع")
        
        if 'documents' in project and project['documents']:
            docs_df = pd.DataFrame(project['documents'])
            st.dataframe(docs_df, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد مستندات مرتبطة بهذا المشروع حاليًا.")
            
            # زر إضافة مستندات
            if st.button("إضافة مستندات"):
                st.session_state.upload_documents = True
        
        # واجهة تحميل المستندات
        if 'upload_documents' in st.session_state and st.session_state.upload_documents:
            st.markdown("#### تحميل مستندات جديدة")
            
            uploaded_file = st.file_uploader("اختر ملفًا", type=['pdf', 'docx', 'xlsx', 'png', 'jpg', 'dwg'])
            doc_type = st.selectbox("نوع المستند", ["كراسة شروط", "عقد", "مخططات", "جدول كميات", "مواصفات فنية", "تعديلات وملاحق"])
            
            if uploaded_file and st.button("تحميل المستند"):
                # محاكاة تحميل المستند
                with st.spinner("جاري تحميل المستند..."):
                    time.sleep(2)
                    
                    # إنشاء مستند جديد
                    new_document = {
                        'filename': uploaded_file.name,
                        'type': doc_type,
                        'upload_date': datetime.now().strftime('%Y-%m-%d'),
                        'size': f"{uploaded_file.size / 1024:.1f} KB"
                    }
                    
                    # إضافة المستند إلى المشروع
                    if 'documents' not in project:
                        project['documents'] = []
                    
                    project['documents'].append(new_document)
                    
                    st.success(f"تم تحميل المستند [{uploaded_file.name}] بنجاح!")
                    st.session_state.upload_documents = False
                    st.experimental_rerun()
        
        # عرض البنود والكميات
        st.markdown("#### بنود وكميات المشروع")
        
        if 'items' in project and project['items']:
            items_df = pd.DataFrame(project['items'])
            st.dataframe(items_df, use_container_width=True, hide_index=True)
            
            # زر لتحويل البنود إلى وحدة التسعير
            if st.button("تحويل البنود إلى وحدة التسعير"):
                if 'manual_items' not in st.session_state:
                    st.session_state.manual_items = pd.DataFrame()
                
                st.session_state.manual_items = items_df.copy()
                st.success("تم تحويل البنود إلى وحدة التسعير بنجاح!")
        else:
            st.info("لا توجد بنود وكميات لهذا المشروع حاليًا.")
            
            # زر استيراد البنود من وحدة تحليل المستندات
            if st.button("استيراد البنود من تحليل المستندات"):
                st.warning("ميزة استيراد البنود من تحليل المستندات قيد التطوير.")
        
        # أزرار الإجراءات
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("تعديل المشروع"):
                st.session_state.edit_project = True
                st.experimental_rerun()
        
        with col2:
            if st.button("تصدير بيانات المشروع"):
                st.success("تم تصدير بيانات المشروع بنجاح!")
        
        with col3:
            if st.button("إرسال للاعتماد"):
                st.success("تم إرسال المشروع للاعتماد بنجاح!")
        
        # نموذج تعديل المشروع
        if 'edit_project' in st.session_state and st.session_state.edit_project:
            st.markdown("#### تعديل المشروع")
            
            with st.form("edit_project_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    project_name = st.text_input("اسم المشروع", value=project['name'])
                    client = st.text_input("الجهة المالكة", value=project['client'])
                    location = st.text_input("الموقع", value=project['location'])
                    tender_type = st.selectbox(
                        "نوع المناقصة",
                        ["عامة", "خاصة", "أمر مباشر"],
                        index=["عامة", "خاصة", "أمر مباشر"].index(project['tender_type'])
                    )
                
                with col2:
                    tender_number = st.text_input("رقم المناقصة", value=project['number'])
                    submission_date = st.date_input(
                        "تاريخ التقديم",
                        value=datetime.strptime(project['submission_date'], "%Y-%m-%d") if isinstance(project['submission_date'], str) else project['submission_date']
                    )
                    pricing_method = st.selectbox(
                        "طريقة التسعير",
                        ["قياسي", "غير متزن", "تنافسي", "موجه بالربحية"],
                        index=["قياسي", "غير متزن", "تنافسي", "موجه بالربحية"].index(project['pricing_method'])
                    )
                    status = st.selectbox(
                        "حالة المشروع",
                        ["جديد", "قيد التسعير", "تم التقديم", "تمت الترسية", "قيد التنفيذ", "منتهي", "ملغي"],
                        index=["جديد", "قيد التسعير", "تم التقديم", "تمت الترسية", "قيد التنفيذ", "منتهي", "ملغي"].index(project['status'])
                    )
                
                description = st.text_area("وصف المشروع", value=project.get('description', ''))
                
                col1, col2 = st.columns(2)
                
                with col1:
                    submit = st.form_submit_button("حفظ التعديلات")
                
                with col2:
                    cancel = st.form_submit_button("إلغاء")
                
                if submit:
                    # تحديث بيانات المشروع
                    project['name'] = project_name
                    project['number'] = tender_number
                    project['client'] = client
                    project['location'] = location
                    project['description'] = description
                    project['status'] = status
                    project['tender_type'] = tender_type
                    project['pricing_method'] = pricing_method
                    project['submission_date'] = submission_date
                    
                    st.success("تم تحديث بيانات المشروع بنجاح!")
                    st.session_state.edit_project = False
                    st.experimental_rerun()
                
                elif cancel:
                    st.session_state.edit_project = False
                    st.experimental_rerun()
    
    def _render_projects_tracking_tab(self):
        """عرض تبويب متابعة المشاريع"""
        
        st.markdown("### متابعة المشاريع")
        
        # عرض إحصائيات المشاريع
        col1, col2, col3, col4 = st.columns(4)
        
        projects = st.session_state.projects
        
        with col1:
            total_projects = len(projects)
            self.ui.create_metric_card("إجمالي المشاريع", str(total_projects), None, self.ui.COLORS['primary'])
        
        with col2:
            active_projects = len([p for p in projects if p['status'] in ["قيد التسعير", "تم التقديم", "تمت الترسية", "قيد التنفيذ"]])
            self.ui.create_metric_card("المشاريع النشطة", str(active_projects), None, self.ui.COLORS['success'])
        
        with col3:
            pending_submission = len([p for p in projects if p['status'] in ["جديد", "قيد التسعير"]])
            self.ui.create_metric_card("مشاريع قيد التسعير", str(pending_submission), None, self.ui.COLORS['warning'])
        
        with col4:
            completed_projects = len([p for p in projects if p['status'] in ["منتهي"]])
            self.ui.create_metric_card("المشاريع المنتهية", str(completed_projects), None, self.ui.COLORS['info'])
        
        # عرض رسم بياني لحالة المشاريع
        st.markdown("#### توزيع المشاريع حسب الحالة")
        
        status_counts = {}
        for p in projects:
            status = p['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        status_df = pd.DataFrame({
            'الحالة': list(status_counts.keys()),
            'عدد المشاريع': list(status_counts.values())
        })
        
        st.bar_chart(status_df.set_index('الحالة'))
        
        # عرض المشاريع قيد المتابعة
        st.markdown("#### المشاريع قيد المتابعة")
        
        # عرض المشاريع النشطة المرتبة حسب تاريخ التقديم
        active_projects_list = [p for p in projects if p['status'] in ["قيد التسعير", "تم التقديم", "تمت الترسية", "قيد التنفيذ"]]
        
        if active_projects_list:
            # تحويل التواريخ إلى كائنات تاريخ إذا كانت نصوصًا
            for p in active_projects_list:
                if isinstance(p['submission_date'], str):
                    p['submission_date'] = datetime.strptime(p['submission_date'], "%Y-%m-%d")
            
            # ترتيب المشاريع حسب تاريخ التقديم
            active_projects_list.sort(key=lambda x: x['submission_date'])
            
            # تحويل إلى DataFrame
            active_df = pd.DataFrame(active_projects_list)
            
            # اختيار وترتيب الأعمدة
            display_columns = [
                'name', 'number', 'client', 'status',
                'submission_date', 'tender_type'
            ]
            
            # تغيير أسماء الأعمدة
            column_names = {
                'name': 'اسم المشروع',
                'number': 'رقم المناقصة',
                'client': 'الجهة المالكة',
                'status': 'الحالة',
                'submission_date': 'تاريخ التقديم',
                'tender_type': 'نوع المناقصة'
            }
            
            # تنسيق البيانات
            display_df = active_df[display_columns].rename(columns=column_names)
            display_df['تاريخ التقديم'] = pd.to_datetime(display_df['تاريخ التقديم']).dt.strftime('%Y-%m-%d')
            
            # عرض الجدول
            st.dataframe(display_df, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد مشاريع نشطة حاليًا.")
        
        # عرض المشاريع المقبلة
        st.markdown("#### المواعيد المقبلة")
        
        upcoming_events = []
        today = datetime.now().date()
        
        for p in projects:
            submission_date = p['submission_date']
            if isinstance(submission_date, str):
                submission_date = datetime.strptime(submission_date, "%Y-%m-%d").date()
            elif isinstance(submission_date, datetime):
                submission_date = submission_date.date()
            
            # المشاريع التي موعد تقديمها خلال الأسبوعين القادمين
            if today <= submission_date <= today + timedelta(days=14) and p['status'] in ["قيد التسعير"]:
                days_left = (submission_date - today).days
                upcoming_events.append({
                    'المشروع': p['name'],
                    'الحدث': 'موعد تقديم المناقصة',
                    'التاريخ': submission_date.strftime('%Y-%m-%d'),
                    'الأيام المتبقية': days_left
                })
        
        if upcoming_events:
            events_df = pd.DataFrame(upcoming_events)
            st.dataframe(events_df, use_container_width=True, hide_index=True)
        else:
            st.info("لا توجد مواعيد قريبة.")
    
    def _generate_sample_projects(self):
        """توليد بيانات افتراضية للمشاريع"""
        
        projects = [
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
                'submission_date': (datetime.now() + timedelta(days=5)),
                'created_at': datetime.now() - timedelta(days=10),
                'created_by_id': 1,
                'documents': [
                    {
                        'filename': "كراسة الشروط والمواصفات.pdf",
                        'type': "كراسة شروط",
                        'upload_date': (datetime.now() - timedelta(days=9)).strftime('%Y-%m-%d'),
                        'size': "5.2 MB"
                    },
                    {
                        'filename': "المخططات الهندسية.dwg",
                        'type': "مخططات",
                        'upload_date': (datetime.now() - timedelta(days=8)).strftime('%Y-%m-%d'),
                        'size': "25.7 MB"
                    },
                    {
                        'filename': "جدول الكميات.xlsx",
                        'type': "جدول كميات",
                        'upload_date': (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'),
                        'size': "1.8 MB"
                    }
                ],
                'items': [
                    {
                        'رقم البند': "A1",
                        'وصف البند': "أعمال الحفر والردم",
                        'الوحدة': "م3",
                        'الكمية': 12500
                    },
                    {
                        'رقم البند': "A2",
                        'وصف البند': "أعمال الخرسانة المسلحة للأساسات",
                        'الوحدة': "م3",
                        'الكمية': 3500
                    },
                    {
                        'رقم البند': "A3",
                        'وصف البند': "أعمال حديد التسليح",
                        'الوحدة': "طن",
                        'الكمية': 450
                    }
                ]
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
                'submission_date': (datetime.now() - timedelta(days=15)),
                'created_at': datetime.now() - timedelta(days=45),
                'created_by_id': 1
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
                'submission_date': (datetime.now() - timedelta(days=90)),
                'created_at': datetime.now() - timedelta(days=120),
                'created_by_id': 1
            },
            {
                'id': 4,
                'name': "إنشاء منتزه الملك سلمان",
                'number': "RAM-2025-015",
                'client': "أمانة منطقة الرياض",
                'location': "الرياض، المنطقة الوسطى",
                'description': "إنشاء منتزه الملك سلمان على مساحة 500,000 متر مربع، ويشمل المشروع أعمال التشجير والتنسيق والمسطحات المائية والمباني الخدمية.",
                'status': "قيد التنفيذ",
                'tender_type': "عامة",
                'pricing_method': "قياسي",
                'submission_date': (datetime.now() - timedelta(days=180)),
                'created_at': datetime.now() - timedelta(days=210),
                'created_by_id': 1
            },
            {
                'id': 5,
                'name': "إنشاء مبنى مختبرات كلية العلوم",
                'number': "KSU-2025-032",
                'client': "جامعة الملك سعود",
                'location': "الرياض، المنطقة الوسطى",
                'description': "إنشاء مبنى المختبرات الجديد لكلية العلوم بمساحة 8,000 متر مربع، ويتكون من 3 طوابق ويشمل تجهيز المعامل والمختبرات العلمية.",
                'status': "جديد",
                'tender_type': "خاصة",
                'pricing_method': "تنافسي",
                'submission_date': (datetime.now() + timedelta(days=10)),
                'created_at': datetime.now() - timedelta(days=5),
                'created_by_id': 1
            },
            {
                'id': 6,
                'name': "توريد وتركيب أنظمة الطاقة الشمسية",
                'number': "SEC-2025-098",
                'client': "الشركة السعودية للكهرباء",
                'location': "تبوك، المنطقة الشمالية",
                'description': "توريد وتركيب أنظمة الطاقة الشمسية بقدرة 5 ميجاوات، مع جميع الأعمال المدنية والكهربائية.",
                'status': "جديد",
                'tender_type': "عامة",
                'pricing_method': "قياسي",
                'submission_date': (datetime.now() + timedelta(days=20)),
                'created_at': datetime.now() - timedelta(days=2),
                'created_by_id': 1
            }
        ]
        
        return projects

# تشغيل التطبيق
if __name__ == "__main__":
    projects_app = ProjectsApp()
    projects_app.run()
