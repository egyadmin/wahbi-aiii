"""
وحدة إدارة الإدارات المساندة - إدارة تكاليف الإدارات المساندة
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import json
from datetime import datetime
import io

class IndirectSupportManagement:
    """فئة إدارة الإدارات المساندة"""
    
    def __init__(self):
        """تهيئة وحدة إدارة الإدارات المساندة"""
        
        # تهيئة حالة الجلسة لإدارة الإدارات المساندة
        if 'indirect_support' not in st.session_state:
            self._initialize_indirect_support()
    
    def _initialize_indirect_support(self):
        """تهيئة بيانات إدارة الإدارات المساندة"""
        
        # إنشاء بيانات افتراضية للإدارات المساندة
        departments = [
            {
                "id": "ADM-001",
                "name": "الإدارة العليا",
                "category": "إدارية",
                "annual_cost": 2400000,
                "staff_count": 5,
                "allocation_method": "نسبة من قيمة المشروع",
                "allocation_percentage": 0.02,
                "description": "تشمل الرئيس التنفيذي والمدراء التنفيذيين"
            },
            {
                "id": "ADM-002",
                "name": "إدارة الموارد البشرية",
                "category": "إدارية",
                "annual_cost": 1200000,
                "staff_count": 8,
                "allocation_method": "نسبة من قيمة المشروع",
                "allocation_percentage": 0.01,
                "description": "مسؤولة عن التوظيف والتدريب وشؤون الموظفين"
            },
            {
                "id": "ADM-003",
                "name": "الإدارة المالية",
                "category": "إدارية",
                "annual_cost": 1500000,
                "staff_count": 10,
                "allocation_method": "نسبة من قيمة المشروع",
                "allocation_percentage": 0.015,
                "description": "مسؤولة عن المحاسبة والميزانية والتقارير المالية"
            },
            {
                "id": "ADM-004",
                "name": "إدارة تقنية المعلومات",
                "category": "إدارية",
                "annual_cost": 1800000,
                "staff_count": 12,
                "allocation_method": "تكلفة ثابتة",
                "allocation_percentage": 0,
                "fixed_cost": 50000,
                "description": "مسؤولة عن البنية التحتية التقنية والدعم الفني"
            },
            {
                "id": "TEC-001",
                "name": "إدارة الجودة",
                "category": "فنية",
                "annual_cost": 1600000,
                "staff_count": 15,
                "allocation_method": "نسبة من قيمة المشروع",
                "allocation_percentage": 0.02,
                "description": "مسؤولة عن ضمان الجودة ومراقبة الجودة"
            },
            {
                "id": "TEC-002",
                "name": "إدارة السلامة",
                "category": "فنية",
                "annual_cost": 1400000,
                "staff_count": 12,
                "allocation_method": "نسبة من قيمة المشروع",
                "allocation_percentage": 0.015,
                "description": "مسؤولة عن السلامة المهنية وسلامة الموقع"
            },
            {
                "id": "TEC-003",
                "name": "إدارة المشتريات",
                "category": "فنية",
                "annual_cost": 2000000,
                "staff_count": 18,
                "allocation_method": "نسبة من قيمة المشروع",
                "allocation_percentage": 0.025,
                "description": "مسؤولة عن المشتريات والتعاقدات"
            },
            {
                "id": "TEC-004",
                "name": "إدارة المستودعات",
                "category": "فنية",
                "annual_cost": 1200000,
                "staff_count": 20,
                "allocation_method": "تكلفة ثابتة",
                "allocation_percentage": 0,
                "fixed_cost": 100000,
                "description": "مسؤولة عن إدارة المخزون والمستودعات"
            },
            {
                "id": "SUP-001",
                "name": "إدارة النقل",
                "category": "مساندة",
                "annual_cost": 2500000,
                "staff_count": 25,
                "allocation_method": "تكلفة ثابتة",
                "allocation_percentage": 0,
                "fixed_cost": 200000,
                "description": "مسؤولة عن نقل المواد والمعدات والعمالة"
            },
            {
                "id": "SUP-002",
                "name": "إدارة الصيانة",
                "category": "مساندة",
                "annual_cost": 1800000,
                "staff_count": 22,
                "allocation_method": "تكلفة ثابتة",
                "allocation_percentage": 0,
                "fixed_cost": 150000,
                "description": "مسؤولة عن صيانة المعدات والآليات"
            },
            {
                "id": "SUP-003",
                "name": "إدارة الأمن",
                "category": "مساندة",
                "annual_cost": 1000000,
                "staff_count": 30,
                "allocation_method": "تكلفة ثابتة",
                "allocation_percentage": 0,
                "fixed_cost": 80000,
                "description": "مسؤولة عن أمن المواقع والمنشآت"
            },
            {
                "id": "SUP-004",
                "name": "إدارة الخدمات العامة",
                "category": "مساندة",
                "annual_cost": 800000,
                "staff_count": 15,
                "allocation_method": "تكلفة ثابتة",
                "allocation_percentage": 0,
                "fixed_cost": 50000,
                "description": "مسؤولة عن الخدمات العامة والضيافة"
            }
        ]
        
        # إنشاء بيانات افتراضية للمشاريع
        projects = [
            {
                "id": "PRJ-001",
                "name": "مشروع تطوير طريق الملك عبدالله",
                "value": 50000000,
                "duration": 24,
                "start_date": "2025-01-01",
                "end_date": "2026-12-31",
                "status": "جاري",
                "location": "الرياض",
                "client": "وزارة النقل",
                "description": "مشروع تطوير وتوسعة طريق الملك عبدالله بطول 15 كم"
            },
            {
                "id": "PRJ-002",
                "name": "مشروع إنشاء شبكة صرف صحي",
                "value": 30000000,
                "duration": 18,
                "start_date": "2025-03-01",
                "end_date": "2026-08-31",
                "status": "جاري",
                "location": "جدة",
                "client": "شركة المياه الوطنية",
                "description": "مشروع إنشاء شبكة صرف صحي في حي النزهة بجدة"
            },
            {
                "id": "PRJ-003",
                "name": "مشروع إنشاء جسر تقاطع طريق الملك فهد",
                "value": 80000000,
                "duration": 30,
                "start_date": "2025-02-01",
                "end_date": "2027-07-31",
                "status": "جاري",
                "location": "الدمام",
                "client": "أمانة المنطقة الشرقية",
                "description": "مشروع إنشاء جسر علوي عند تقاطع طريق الملك فهد مع طريق الأمير محمد بن فهد"
            }
        ]
        
        # إنشاء بيانات افتراضية لتخصيص الإدارات المساندة للمشاريع
        allocations = []
        
        for project in projects:
            for department in departments:
                if department["allocation_method"] == "نسبة من قيمة المشروع":
                    allocation_amount = project["value"] * department["allocation_percentage"]
                else:  # تكلفة ثابتة
                    allocation_amount = department.get("fixed_cost", 0)
                
                allocations.append({
                    "project_id": project["id"],
                    "department_id": department["id"],
                    "allocation_amount": allocation_amount,
                    "allocation_method": department["allocation_method"],
                    "allocation_percentage": department["allocation_percentage"] if department["allocation_method"] == "نسبة من قيمة المشروع" else 0,
                    "fixed_cost": department.get("fixed_cost", 0) if department["allocation_method"] == "تكلفة ثابتة" else 0,
                    "notes": ""
                })
        
        # تخزين البيانات في حالة الجلسة
        st.session_state.indirect_support = {
            "departments": pd.DataFrame(departments),
            "projects": pd.DataFrame(projects),
            "allocations": pd.DataFrame(allocations)
        }
    
    def render(self):
        """عرض واجهة إدارة الإدارات المساندة"""
        
        st.markdown("## إدارة الإدارات المساندة")
        
        # إنشاء تبويبات لعرض إدارة الإدارات المساندة
        tabs = st.tabs([
            "الإدارات المساندة", 
            "المشاريع", 
            "تخصيص التكاليف",
            "التقارير"
        ])
        
        with tabs[0]:
            self._render_departments_tab()
        
        with tabs[1]:
            self._render_projects_tab()
        
        with tabs[2]:
            self._render_allocations_tab()
        
        with tabs[3]:
            self._render_reports_tab()
    
    def _render_departments_tab(self):
        """عرض تبويب الإدارات المساندة"""
        
        st.markdown("### الإدارات المساندة")
        
        # استخراج البيانات
        departments = st.session_state.indirect_support["departments"]
        
        # إنشاء فلاتر للعرض
        col1, col2 = st.columns(2)
        
        with col1:
            # فلتر حسب الفئة
            categories = ["الكل"] + sorted(departments["category"].unique().tolist())
            selected_category = st.selectbox("اختر فئة الإدارة", categories, key="departments_category")
        
        with col2:
            # فلتر حسب طريقة التخصيص
            allocation_methods = ["الكل"] + sorted(departments["allocation_method"].unique().tolist())
            selected_allocation_method = st.selectbox("اختر طريقة التخصيص", allocation_methods, key="departments_allocation_method")
        
        # تطبيق الفلاتر
        filtered_df = departments.copy()
        
        if selected_category != "الكل":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]
        
        if selected_allocation_method != "الكل":
            filtered_df = filtered_df[filtered_df["allocation_method"] == selected_allocation_method]
        
        # عرض البيانات
        if not filtered_df.empty:
            # عرض عدد النتائج
            st.info(f"تم العثور على {len(filtered_df)} إدارة")
            
            # إنشاء جدول للعرض
            display_df = filtered_df[["id", "name", "category", "annual_cost", "staff_count", "allocation_method"]].copy()
            display_df.columns = ["الكود", "الاسم", "الفئة", "التكلفة السنوية", "عدد الموظفين", "طريقة التخصيص"]
            
            # عرض الجدول
            st.dataframe(display_df, use_container_width=True)
            
            # إضافة إدارة جديدة
            st.markdown("### إضافة إدارة جديدة")
            
            with st.form("add_department_form"):
                # الصف الأول
                col1, col2 = st.columns(2)
                
                with col1:
                    department_id = st.text_input("كود الإدارة", value=f"DEP-{len(departments) + 1:03d}")
                    department_name = st.text_input("اسم الإدارة", placeholder="مثال: إدارة الموارد البشرية")
                
                with col2:
                    department_category = st.selectbox("فئة الإدارة", ["إدارية", "فنية", "مساندة"])
                    department_staff_count = st.number_input("عدد الموظفين", min_value=1, step=1)
                
                # الصف الثاني
                col1, col2 = st.columns(2)
                
                with col1:
                    department_annual_cost = st.number_input("التكلفة السنوية (ريال)", min_value=0, step=100000)
                
                with col2:
                    department_allocation_method = st.selectbox("طريقة التخصيص", ["نسبة من قيمة المشروع", "تكلفة ثابتة"])
                
                # الصف الثالث
                if department_allocation_method == "نسبة من قيمة المشروع":
                    department_allocation_percentage = st.slider("نسبة التخصيص", min_value=0.0, max_value=0.1, value=0.01, step=0.001, format="%g%%") * 100
                    department_fixed_cost = 0
                else:  # تكلفة ثابتة
                    department_fixed_cost = st.number_input("التكلفة الثابتة (ريال)", min_value=0, step=10000)
                    department_allocation_percentage = 0
                
                # الصف الرابع
                department_description = st.text_area("وصف الإدارة", placeholder="أدخل وصفاً تفصيلياً للإدارة")
                
                # زر الإضافة
                submit_button = st.form_submit_button("إضافة الإدارة")
                
                if submit_button:
                    # التحقق من البيانات
                    if not department_name or not department_category:
                        st.error("يرجى إدخال المعلومات الأساسية للإدارة")
                    else:
                        # إنشاء إدارة جديدة
                        new_department = {
                            "id": department_id,
                            "name": department_name,
                            "category": department_category,
                            "annual_cost": department_annual_cost,
                            "staff_count": department_staff_count,
                            "allocation_method": department_allocation_method,
                            "allocation_percentage": department_allocation_percentage / 100 if department_allocation_method == "نسبة من قيمة المشروع" else 0,
                            "fixed_cost": department_fixed_cost if department_allocation_method == "تكلفة ثابتة" else 0,
                            "description": department_description
                        }
                        
                        # إضافة الإدارة إلى الجدول
                        st.session_state.indirect_support["departments"] = pd.concat([
                            st.session_state.indirect_support["departments"],
                            pd.DataFrame([new_department])
                        ], ignore_index=True)
                        
                        # إضافة تخصيصات للإدارة الجديدة
                        projects = st.session_state.indirect_support["projects"]
                        allocations = st.session_state.indirect_support["allocations"]
                        
                        new_allocations = []
                        
                        for _, project in projects.iterrows():
                            if department_allocation_method == "نسبة من قيمة المشروع":
                                allocation_amount = project["value"] * (department_allocation_percentage / 100)
                            else:  # تكلفة ثابتة
                                allocation_amount = department_fixed_cost
                            
                            new_allocations.append({
                                "project_id": project["id"],
                                "department_id": department_id,
                                "allocation_amount": allocation_amount,
                                "allocation_method": department_allocation_method,
                                "allocation_percentage": department_allocation_percentage / 100 if department_allocation_method == "نسبة من قيمة المشروع" else 0,
                                "fixed_cost": department_fixed_cost if department_allocation_method == "تكلفة ثابتة" else 0,
                                "notes": ""
                            })
                        
                        # إضافة التخصيصات الجديدة
                        st.session_state.indirect_support["allocations"] = pd.concat([
                            allocations,
                            pd.DataFrame(new_allocations)
                        ], ignore_index=True)
                        
                        st.success(f"تمت إضافة الإدارة {department_name} بنجاح!")
                        
                        # إعادة تحميل الصفحة
                        st.experimental_rerun()
            
            # عرض تفاصيل الإدارات
            st.markdown("### تفاصيل الإدارات")
            
            selected_department_id = st.selectbox("اختر إدارة لعرض التفاصيل", filtered_df["id"].tolist(), key="department_details")
            
            # استخراج الإدارة المختارة
            selected_department = filtered_df[filtered_df["id"] == selected_department_id].iloc[0]
            
            # عرض تفاصيل الإدارة
            st.markdown(f"**الإدارة:** {selected_department['name']} ({selected_department['id']})")
            st.markdown(f"**الفئة:** {selected_department['category']}")
            st.markdown(f"**التكلفة السنوية:** {selected_department['annual_cost']:,} ريال")
            st.markdown(f"**عدد الموظفين:** {selected_department['staff_count']} موظف")
            st.markdown(f"**طريقة التخصيص:** {selected_department['allocation_method']}")
            
            if selected_department["allocation_method"] == "نسبة من قيمة المشروع":
                st.markdown(f"**نسبة التخصيص:** {selected_department['allocation_percentage'] * 100:.2f}%")
            else:  # تكلفة ثابتة
                st.markdown(f"**التكلفة الثابتة:** {selected_department.get('fixed_cost', 0):,} ريال")
            
            if "description" in selected_department and selected_department["description"]:
                st.markdown(f"**الوصف:** {selected_department['description']}")
            
            # عرض تخصيصات الإدارة
            st.markdown("#### تخصيصات الإدارة للمشاريع")
            
            # استخراج تخصيصات الإدارة
            allocations = st.session_state.indirect_support["allocations"]
            projects = st.session_state.indirect_support["projects"]
            
            department_allocations = allocations[allocations["department_id"] == selected_department_id]
            
            if not department_allocations.empty:
                # دمج بيانات المشاريع
                merged_allocations = pd.merge(
                    department_allocations,
                    projects[["id", "name", "value"]],
                    left_on="project_id",
                    right_on="id",
                    suffixes=("", "_project")
                )
                
                # إنشاء جدول للعرض
                display_allocations = merged_allocations[["id_project", "name", "value", "allocation_amount"]].copy()
                display_allocations.columns = ["كود المشروع", "اسم المشروع", "قيمة المشروع", "مبلغ التخصيص"]
                
                # عرض الجدول
                st.dataframe(display_allocations, use_container_width=True)
                
                # إنشاء رسم بياني للتخصيصات
                fig = px.bar(
                    display_allocations,
                    x="اسم المشروع",
                    y="مبلغ التخصيص",
                    title=f"تخصيصات إدارة {selected_department['name']} للمشاريع",
                    color="اسم المشروع",
                    text_auto=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("لا يوجد تخصيصات لهذه الإدارة")
        else:
            st.warning("لا يوجد إدارات تطابق معايير البحث")
    
    def _render_projects_tab(self):
        """عرض تبويب المشاريع"""
        
        st.markdown("### المشاريع")
        
        # استخراج البيانات
        projects = st.session_state.indirect_support["projects"]
        
        # إنشاء فلاتر للعرض
        col1, col2 = st.columns(2)
        
        with col1:
            # فلتر حسب الحالة
            statuses = ["الكل"] + sorted(projects["status"].unique().tolist())
            selected_status = st.selectbox("اختر حالة المشروع", statuses, key="projects_status")
        
        with col2:
            # فلتر حسب الموقع
            locations = ["الكل"] + sorted(projects["location"].unique().tolist())
            selected_location = st.selectbox("اختر موقع المشروع", locations, key="projects_location")
        
        # تطبيق الفلاتر
        filtered_df = projects.copy()
        
        if selected_status != "الكل":
            filtered_df = filtered_df[filtered_df["status"] == selected_status]
        
        if selected_location != "الكل":
            filtered_df = filtered_df[filtered_df["location"] == selected_location]
        
        # عرض البيانات
        if not filtered_df.empty:
            # عرض عدد النتائج
            st.info(f"تم العثور على {len(filtered_df)} مشروع")
            
            # إنشاء جدول للعرض
            display_df = filtered_df[["id", "name", "value", "duration", "status", "location", "client"]].copy()
            display_df.columns = ["الكود", "الاسم", "القيمة", "المدة (شهر)", "الحالة", "الموقع", "العميل"]
            
            # عرض الجدول
            st.dataframe(display_df, use_container_width=True)
            
            # إضافة مشروع جديد
            st.markdown("### إضافة مشروع جديد")
            
            with st.form("add_project_form"):
                # الصف الأول
                col1, col2 = st.columns(2)
                
                with col1:
                    project_id = st.text_input("كود المشروع", value=f"PRJ-{len(projects) + 1:03d}")
                    project_name = st.text_input("اسم المشروع", placeholder="مثال: مشروع تطوير طريق الملك عبدالله")
                
                with col2:
                    project_value = st.number_input("قيمة المشروع (ريال)", min_value=0, step=1000000)
                    project_duration = st.number_input("مدة المشروع (شهر)", min_value=1, step=1)
                
                # الصف الثاني
                col1, col2 = st.columns(2)
                
                with col1:
                    project_start_date = st.date_input("تاريخ البدء")
                    project_status = st.selectbox("حالة المشروع", ["جاري", "مكتمل", "متوقف", "ملغي"])
                
                with col2:
                    project_end_date = st.date_input("تاريخ الانتهاء")
                    project_location = st.text_input("موقع المشروع", placeholder="مثال: الرياض")
                
                # الصف الثالث
                project_client = st.text_input("العميل", placeholder="مثال: وزارة النقل")
                project_description = st.text_area("وصف المشروع", placeholder="أدخل وصفاً تفصيلياً للمشروع")
                
                # زر الإضافة
                submit_button = st.form_submit_button("إضافة المشروع")
                
                if submit_button:
                    # التحقق من البيانات
                    if not project_name or not project_value or not project_location or not project_client:
                        st.error("يرجى إدخال المعلومات الأساسية للمشروع")
                    else:
                        # إنشاء مشروع جديد
                        new_project = {
                            "id": project_id,
                            "name": project_name,
                            "value": project_value,
                            "duration": project_duration,
                            "start_date": project_start_date.strftime("%Y-%m-%d"),
                            "end_date": project_end_date.strftime("%Y-%m-%d"),
                            "status": project_status,
                            "location": project_location,
                            "client": project_client,
                            "description": project_description
                        }
                        
                        # إضافة المشروع إلى الجدول
                        st.session_state.indirect_support["projects"] = pd.concat([
                            st.session_state.indirect_support["projects"],
                            pd.DataFrame([new_project])
                        ], ignore_index=True)
                        
                        # إضافة تخصيصات للمشروع الجديد
                        departments = st.session_state.indirect_support["departments"]
                        allocations = st.session_state.indirect_support["allocations"]
                        
                        new_allocations = []
                        
                        for _, department in departments.iterrows():
                            if department["allocation_method"] == "نسبة من قيمة المشروع":
                                allocation_amount = project_value * department["allocation_percentage"]
                            else:  # تكلفة ثابتة
                                allocation_amount = department.get("fixed_cost", 0)
                            
                            new_allocations.append({
                                "project_id": project_id,
                                "department_id": department["id"],
                                "allocation_amount": allocation_amount,
                                "allocation_method": department["allocation_method"],
                                "allocation_percentage": department["allocation_percentage"] if department["allocation_method"] == "نسبة من قيمة المشروع" else 0,
                                "fixed_cost": department.get("fixed_cost", 0) if department["allocation_method"] == "تكلفة ثابتة" else 0,
                                "notes": ""
                            })
                        
                        # إضافة التخصيصات الجديدة
                        st.session_state.indirect_support["allocations"] = pd.concat([
                            allocations,
                            pd.DataFrame(new_allocations)
                        ], ignore_index=True)
                        
                        st.success(f"تمت إضافة المشروع {project_name} بنجاح!")
                        
                        # إعادة تحميل الصفحة
                        st.experimental_rerun()
            
            # عرض تفاصيل المشاريع
            st.markdown("### تفاصيل المشاريع")
            
            selected_project_id = st.selectbox("اختر مشروع لعرض التفاصيل", filtered_df["id"].tolist(), key="project_details")
            
            # استخراج المشروع المختار
            selected_project = filtered_df[filtered_df["id"] == selected_project_id].iloc[0]
            
            # عرض تفاصيل المشروع
            st.markdown(f"**المشروع:** {selected_project['name']} ({selected_project['id']})")
            st.markdown(f"**القيمة:** {selected_project['value']:,} ريال")
            st.markdown(f"**المدة:** {selected_project['duration']} شهر")
            st.markdown(f"**تاريخ البدء:** {selected_project['start_date']}")
            st.markdown(f"**تاريخ الانتهاء:** {selected_project['end_date']}")
            st.markdown(f"**الحالة:** {selected_project['status']}")
            st.markdown(f"**الموقع:** {selected_project['location']}")
            st.markdown(f"**العميل:** {selected_project['client']}")
            
            if "description" in selected_project and selected_project["description"]:
                st.markdown(f"**الوصف:** {selected_project['description']}")
            
            # عرض تخصيصات المشروع
            st.markdown("#### تخصيصات الإدارات المساندة للمشروع")
            
            # استخراج تخصيصات المشروع
            allocations = st.session_state.indirect_support["allocations"]
            departments = st.session_state.indirect_support["departments"]
            
            project_allocations = allocations[allocations["project_id"] == selected_project_id]
            
            if not project_allocations.empty:
                # دمج بيانات الإدارات
                merged_allocations = pd.merge(
                    project_allocations,
                    departments[["id", "name", "category"]],
                    left_on="department_id",
                    right_on="id",
                    suffixes=("", "_department")
                )
                
                # إنشاء جدول للعرض
                display_allocations = merged_allocations[["id_department", "name", "category", "allocation_amount", "allocation_method"]].copy()
                display_allocations.columns = ["كود الإدارة", "اسم الإدارة", "الفئة", "مبلغ التخصيص", "طريقة التخصيص"]
                
                # عرض الجدول
                st.dataframe(display_allocations, use_container_width=True)
                
                # حساب إجمالي التخصيصات
                total_allocation = display_allocations["مبلغ التخصيص"].sum()
                
                st.markdown(f"**إجمالي تخصيصات الإدارات المساندة:** {total_allocation:,} ريال")
                st.markdown(f"**نسبة التخصيصات من قيمة المشروع:** {(total_allocation / selected_project['value']) * 100:.2f}%")
                
                # إنشاء رسم بياني للتخصيصات
                fig = px.bar(
                    display_allocations,
                    x="اسم الإدارة",
                    y="مبلغ التخصيص",
                    title=f"تخصيصات الإدارات المساندة لمشروع {selected_project['name']}",
                    color="الفئة",
                    text_auto=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # إنشاء رسم بياني دائري للتخصيصات حسب الفئة
                category_allocations = display_allocations.groupby("الفئة")["مبلغ التخصيص"].sum().reset_index()
                
                fig = px.pie(
                    category_allocations,
                    values="مبلغ التخصيص",
                    names="الفئة",
                    title=f"توزيع تخصيصات الإدارات المساندة حسب الفئة لمشروع {selected_project['name']}",
                    color="الفئة"
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("لا يوجد تخصيصات لهذا المشروع")
        else:
            st.warning("لا يوجد مشاريع تطابق معايير البحث")
    
    def _render_allocations_tab(self):
        """عرض تبويب تخصيص التكاليف"""
        
        st.markdown("### تخصيص تكاليف الإدارات المساندة")
        
        # استخراج البيانات
        allocations = st.session_state.indirect_support["allocations"]
        departments = st.session_state.indirect_support["departments"]
        projects = st.session_state.indirect_support["projects"]
        
        # دمج البيانات
        merged_allocations = pd.merge(
            allocations,
            departments[["id", "name", "category"]],
            left_on="department_id",
            right_on="id",
            suffixes=("", "_department")
        )
        
        merged_allocations = pd.merge(
            merged_allocations,
            projects[["id", "name", "value", "status"]],
            left_on="project_id",
            right_on="id",
            suffixes=("_department", "_project")
        )
        
        # إنشاء فلاتر للعرض
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # فلتر حسب المشروع
            project_options = ["الكل"] + sorted(projects["name"].unique().tolist())
            selected_project = st.selectbox("اختر المشروع", project_options, key="allocations_project")
        
        with col2:
            # فلتر حسب فئة الإدارة
            department_categories = ["الكل"] + sorted(departments["category"].unique().tolist())
            selected_department_category = st.selectbox("اختر فئة الإدارة", department_categories, key="allocations_department_category")
        
        with col3:
            # فلتر حسب طريقة التخصيص
            allocation_methods = ["الكل"] + sorted(allocations["allocation_method"].unique().tolist())
            selected_allocation_method = st.selectbox("اختر طريقة التخصيص", allocation_methods, key="allocations_method")
        
        # تطبيق الفلاتر
        filtered_df = merged_allocations.copy()
        
        if selected_project != "الكل":
            filtered_df = filtered_df[filtered_df["name_project"] == selected_project]
        
        if selected_department_category != "الكل":
            filtered_df = filtered_df[filtered_df["category"] == selected_department_category]
        
        if selected_allocation_method != "الكل":
            filtered_df = filtered_df[filtered_df["allocation_method"] == selected_allocation_method]
        
        # عرض البيانات
        if not filtered_df.empty:
            # عرض عدد النتائج
            st.info(f"تم العثور على {len(filtered_df)} تخصيص")
            
            # إنشاء جدول للعرض
            display_df = filtered_df[["id_project", "name_project", "id_department", "name_department", "category", "allocation_method", "allocation_amount"]].copy()
            display_df.columns = ["كود المشروع", "اسم المشروع", "كود الإدارة", "اسم الإدارة", "فئة الإدارة", "طريقة التخصيص", "مبلغ التخصيص"]
            
            # عرض الجدول
            st.dataframe(display_df, use_container_width=True)
            
            # تعديل التخصيصات
            st.markdown("### تعديل التخصيصات")
            
            # اختيار مشروع وإدارة لتعديل التخصيص
            col1, col2 = st.columns(2)
            
            with col1:
                edit_project_id = st.selectbox("اختر المشروع", projects["id"].tolist(), key="edit_allocation_project")
            
            with col2:
                edit_department_id = st.selectbox("اختر الإدارة", departments["id"].tolist(), key="edit_allocation_department")
            
            # استخراج التخصيص المختار
            selected_allocation = allocations[
                (allocations["project_id"] == edit_project_id) &
                (allocations["department_id"] == edit_department_id)
            ]
            
            if not selected_allocation.empty:
                selected_allocation = selected_allocation.iloc[0]
                
                # استخراج بيانات المشروع والإدارة
                selected_project = projects[projects["id"] == edit_project_id].iloc[0]
                selected_department = departments[departments["id"] == edit_department_id].iloc[0]
                
                st.markdown(f"**المشروع:** {selected_project['name']} ({selected_project['id']})")
                st.markdown(f"**الإدارة:** {selected_department['name']} ({selected_department['id']})")
                st.markdown(f"**طريقة التخصيص الحالية:** {selected_allocation['allocation_method']}")
                st.markdown(f"**مبلغ التخصيص الحالي:** {selected_allocation['allocation_amount']:,} ريال")
                
                # نموذج تعديل التخصيص
                with st.form("edit_allocation_form"):
                    # اختيار طريقة التخصيص
                    allocation_method = st.selectbox(
                        "طريقة التخصيص",
                        ["نسبة من قيمة المشروع", "تكلفة ثابتة"],
                        index=0 if selected_allocation["allocation_method"] == "نسبة من قيمة المشروع" else 1,
                        key="edit_allocation_method"
                    )
                    
                    # إدخال قيمة التخصيص
                    if allocation_method == "نسبة من قيمة المشروع":
                        allocation_percentage = st.slider(
                            "نسبة التخصيص",
                            min_value=0.0,
                            max_value=0.1,
                            value=float(selected_allocation["allocation_percentage"]),
                            step=0.001,
                            format="%g%%",
                            key="edit_allocation_percentage"
                        ) * 100
                        
                        # حساب مبلغ التخصيص
                        allocation_amount = selected_project["value"] * (allocation_percentage / 100)
                        
                        st.markdown(f"**مبلغ التخصيص المحسوب:** {allocation_amount:,} ريال")
                        
                        fixed_cost = 0
                    else:  # تكلفة ثابتة
                        fixed_cost = st.number_input(
                            "التكلفة الثابتة (ريال)",
                            min_value=0,
                            value=int(selected_allocation["fixed_cost"]),
                            step=10000,
                            key="edit_allocation_fixed_cost"
                        )
                        
                        allocation_amount = fixed_cost
                        allocation_percentage = 0
                    
                    # ملاحظات
                    notes = st.text_area(
                        "ملاحظات",
                        value=selected_allocation["notes"] if "notes" in selected_allocation else "",
                        key="edit_allocation_notes"
                    )
                    
                    # زر الحفظ
                    submit_button = st.form_submit_button("حفظ التعديلات")
                    
                    if submit_button:
                        # تحديث التخصيص
                        allocation_index = allocations[
                            (allocations["project_id"] == edit_project_id) &
                            (allocations["department_id"] == edit_department_id)
                        ].index[0]
                        
                        allocations.at[allocation_index, "allocation_method"] = allocation_method
                        allocations.at[allocation_index, "allocation_percentage"] = allocation_percentage / 100 if allocation_method == "نسبة من قيمة المشروع" else 0
                        allocations.at[allocation_index, "fixed_cost"] = fixed_cost if allocation_method == "تكلفة ثابتة" else 0
                        allocations.at[allocation_index, "allocation_amount"] = allocation_amount
                        allocations.at[allocation_index, "notes"] = notes
                        
                        # تحديث حالة الجلسة
                        st.session_state.indirect_support["allocations"] = allocations
                        
                        st.success("تم تحديث التخصيص بنجاح!")
                        
                        # إعادة تحميل الصفحة
                        st.experimental_rerun()
            else:
                st.warning("لم يتم العثور على تخصيص للمشروع والإدارة المختارين")
            
            # عرض ملخص التخصيصات
            st.markdown("### ملخص التخصيصات")
            
            # حساب إجمالي التخصيصات لكل مشروع
            project_allocations = filtered_df.groupby("name_project")["allocation_amount"].sum().reset_index()
            project_allocations.columns = ["المشروع", "إجمالي التخصيصات"]
            
            # عرض الجدول
            st.dataframe(project_allocations, use_container_width=True)
            
            # إنشاء رسم بياني للتخصيصات حسب المشروع
            fig = px.bar(
                project_allocations,
                x="المشروع",
                y="إجمالي التخصيصات",
                title="إجمالي تخصيصات الإدارات المساندة حسب المشروع",
                color="المشروع",
                text_auto=True
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # حساب إجمالي التخصيصات لكل فئة إدارة
            category_allocations = filtered_df.groupby("category")["allocation_amount"].sum().reset_index()
            category_allocations.columns = ["فئة الإدارة", "إجمالي التخصيصات"]
            
            # عرض الجدول
            st.dataframe(category_allocations, use_container_width=True)
            
            # إنشاء رسم بياني للتخصيصات حسب فئة الإدارة
            fig = px.pie(
                category_allocations,
                values="إجمالي التخصيصات",
                names="فئة الإدارة",
                title="توزيع تخصيصات الإدارات المساندة حسب الفئة",
                color="فئة الإدارة"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("لا يوجد تخصيصات تطابق معايير البحث")
    
    def _render_reports_tab(self):
        """عرض تبويب التقارير"""
        
        st.markdown("### تقارير الإدارات المساندة")
        
        # استخراج البيانات
        allocations = st.session_state.indirect_support["allocations"]
        departments = st.session_state.indirect_support["departments"]
        projects = st.session_state.indirect_support["projects"]
        
        # دمج البيانات
        merged_allocations = pd.merge(
            allocations,
            departments[["id", "name", "category", "annual_cost", "staff_count"]],
            left_on="department_id",
            right_on="id",
            suffixes=("", "_department")
        )
        
        merged_allocations = pd.merge(
            merged_allocations,
            projects[["id", "name", "value", "status", "duration"]],
            left_on="project_id",
            right_on="id",
            suffixes=("_department", "_project")
        )
        
        # اختيار نوع التقرير
        report_type = st.selectbox(
            "اختر نوع التقرير",
            [
                "تقرير تكاليف الإدارات المساندة",
                "تقرير تخصيصات المشاريع",
                "تقرير مقارنة التكاليف",
                "تقرير تحليل الكفاءة"
            ],
            key="report_type"
        )
        
        if report_type == "تقرير تكاليف الإدارات المساندة":
            self._render_departments_cost_report(departments, merged_allocations)
        elif report_type == "تقرير تخصيصات المشاريع":
            self._render_projects_allocation_report(projects, merged_allocations)
        elif report_type == "تقرير مقارنة التكاليف":
            self._render_cost_comparison_report(departments, projects, merged_allocations)
        elif report_type == "تقرير تحليل الكفاءة":
            self._render_efficiency_analysis_report(departments, projects, merged_allocations)
    
    def _render_departments_cost_report(self, departments, merged_allocations):
        """عرض تقرير تكاليف الإدارات المساندة"""
        
        st.markdown("#### تقرير تكاليف الإدارات المساندة")
        
        # حساب إجمالي التكاليف السنوية
        total_annual_cost = departments["annual_cost"].sum()
        total_staff_count = departments["staff_count"].sum()
        
        # عرض ملخص التكاليف
        st.markdown(f"**إجمالي التكاليف السنوية للإدارات المساندة:** {total_annual_cost:,} ريال")
        st.markdown(f"**إجمالي عدد الموظفين:** {total_staff_count} موظف")
        st.markdown(f"**متوسط تكلفة الموظف السنوية:** {total_annual_cost / total_staff_count:,.2f} ريال")
        
        # حساب التكاليف حسب الفئة
        category_costs = departments.groupby("category").agg({
            "annual_cost": "sum",
            "staff_count": "sum"
        }).reset_index()
        
        category_costs["نسبة التكلفة"] = category_costs["annual_cost"] / total_annual_cost * 100
        category_costs["متوسط تكلفة الموظف"] = category_costs["annual_cost"] / category_costs["staff_count"]
        
        # تغيير أسماء الأعمدة
        category_costs.columns = ["الفئة", "التكلفة السنوية", "عدد الموظفين", "نسبة التكلفة", "متوسط تكلفة الموظف"]
        
        # عرض الجدول
        st.dataframe(category_costs, use_container_width=True)
        
        # إنشاء رسم بياني للتكاليف حسب الفئة
        fig = px.pie(
            category_costs,
            values="التكلفة السنوية",
            names="الفئة",
            title="توزيع تكاليف الإدارات المساندة حسب الفئة",
            color="الفئة"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # إنشاء رسم بياني لمتوسط تكلفة الموظف حسب الفئة
        fig = px.bar(
            category_costs,
            x="الفئة",
            y="متوسط تكلفة الموظف",
            title="متوسط تكلفة الموظف السنوية حسب فئة الإدارة",
            color="الفئة",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حساب إجمالي التخصيصات لكل إدارة
        department_allocations = merged_allocations.groupby("name_department").agg({
            "allocation_amount": "sum",
            "annual_cost": "first",
            "category": "first"
        }).reset_index()
        
        department_allocations["نسبة التغطية"] = department_allocations["allocation_amount"] / department_allocations["annual_cost"] * 100
        
        # تغيير أسماء الأعمدة
        department_allocations.columns = ["الإدارة", "إجمالي التخصيصات", "التكلفة السنوية", "الفئة", "نسبة التغطية"]
        
        # ترتيب البيانات حسب نسبة التغطية
        department_allocations = department_allocations.sort_values(by="نسبة التغطية", ascending=False)
        
        # عرض الجدول
        st.dataframe(department_allocations, use_container_width=True)
        
        # إنشاء رسم بياني لنسبة التغطية
        fig = px.bar(
            department_allocations,
            x="الإدارة",
            y="نسبة التغطية",
            title="نسبة تغطية تكاليف الإدارات المساندة من خلال التخصيصات",
            color="الفئة",
            text_auto=True
        )
        
        # إضافة خط أفقي عند 100%
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=100,
            x1=len(department_allocations) - 0.5,
            y1=100,
            line=dict(
                color="red",
                width=2,
                dash="dash"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حساب إجمالي التغطية
        total_allocations = department_allocations["إجمالي التخصيصات"].sum()
        total_coverage = total_allocations / total_annual_cost * 100
        
        st.markdown(f"**إجمالي التخصيصات:** {total_allocations:,} ريال")
        st.markdown(f"**نسبة التغطية الإجمالية:** {total_coverage:.2f}%")
        
        if total_coverage < 100:
            st.warning(f"هناك عجز في تغطية تكاليف الإدارات المساندة بنسبة {100 - total_coverage:.2f}%")
        elif total_coverage > 100:
            st.success(f"هناك فائض في تغطية تكاليف الإدارات المساندة بنسبة {total_coverage - 100:.2f}%")
        else:
            st.success("تمت تغطية تكاليف الإدارات المساندة بالكامل")
    
    def _render_projects_allocation_report(self, projects, merged_allocations):
        """عرض تقرير تخصيصات المشاريع"""
        
        st.markdown("#### تقرير تخصيصات المشاريع")
        
        # حساب إجمالي قيم المشاريع
        total_projects_value = projects["value"].sum()
        
        # عرض ملخص المشاريع
        st.markdown(f"**عدد المشاريع:** {len(projects)}")
        st.markdown(f"**إجمالي قيم المشاريع:** {total_projects_value:,} ريال")
        
        # حساب إجمالي التخصيصات لكل مشروع
        project_allocations = merged_allocations.groupby("name_project").agg({
            "allocation_amount": "sum",
            "value": "first",
            "status": "first",
            "duration": "first"
        }).reset_index()
        
        project_allocations["نسبة التخصيص"] = project_allocations["allocation_amount"] / project_allocations["value"] * 100
        project_allocations["تكلفة التخصيص الشهرية"] = project_allocations["allocation_amount"] / project_allocations["duration"]
        
        # تغيير أسماء الأعمدة
        project_allocations.columns = ["المشروع", "إجمالي التخصيصات", "قيمة المشروع", "الحالة", "المدة (شهر)", "نسبة التخصيص", "تكلفة التخصيص الشهرية"]
        
        # ترتيب البيانات حسب نسبة التخصيص
        project_allocations = project_allocations.sort_values(by="نسبة التخصيص", ascending=False)
        
        # عرض الجدول
        st.dataframe(project_allocations, use_container_width=True)
        
        # إنشاء رسم بياني لنسبة التخصيص
        fig = px.bar(
            project_allocations,
            x="المشروع",
            y="نسبة التخصيص",
            title="نسبة تخصيص الإدارات المساندة من قيمة المشروع",
            color="الحالة",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # إنشاء رسم بياني للتكلفة الشهرية
        fig = px.bar(
            project_allocations,
            x="المشروع",
            y="تكلفة التخصيص الشهرية",
            title="تكلفة تخصيص الإدارات المساندة الشهرية لكل مشروع",
            color="الحالة",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حساب توزيع التخصيصات حسب فئة الإدارة لكل مشروع
        category_allocations = merged_allocations.groupby(["name_project", "category"]).agg({
            "allocation_amount": "sum"
        }).reset_index()
        
        # تغيير أسماء الأعمدة
        category_allocations.columns = ["المشروع", "فئة الإدارة", "مبلغ التخصيص"]
        
        # إنشاء رسم بياني للتخصيصات حسب فئة الإدارة لكل مشروع
        fig = px.bar(
            category_allocations,
            x="المشروع",
            y="مبلغ التخصيص",
            color="فئة الإدارة",
            title="توزيع تخصيصات الإدارات المساندة حسب الفئة لكل مشروع",
            barmode="stack",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حساب متوسط نسبة التخصيص
        avg_allocation_percentage = project_allocations["نسبة التخصيص"].mean()
        
        st.markdown(f"**متوسط نسبة تخصيص الإدارات المساندة من قيمة المشروع:** {avg_allocation_percentage:.2f}%")
        
        # تحليل العلاقة بين قيمة المشروع ونسبة التخصيص
        fig = px.scatter(
            project_allocations,
            x="قيمة المشروع",
            y="نسبة التخصيص",
            title="العلاقة بين قيمة المشروع ونسبة تخصيص الإدارات المساندة",
            color="الحالة",
            size="المدة (شهر)",
            hover_data=["المشروع"],
            trendline="ols"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل العلاقة بين مدة المشروع وتكلفة التخصيص الشهرية
        fig = px.scatter(
            project_allocations,
            x="المدة (شهر)",
            y="تكلفة التخصيص الشهرية",
            title="العلاقة بين مدة المشروع وتكلفة تخصيص الإدارات المساندة الشهرية",
            color="الحالة",
            size="قيمة المشروع",
            hover_data=["المشروع"],
            trendline="ols"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_cost_comparison_report(self, departments, projects, merged_allocations):
        """عرض تقرير مقارنة التكاليف"""
        
        st.markdown("#### تقرير مقارنة التكاليف")
        
        # حساب إجمالي التكاليف السنوية
        total_annual_cost = departments["annual_cost"].sum()
        
        # حساب إجمالي قيم المشاريع
        total_projects_value = projects["value"].sum()
        
        # حساب إجمالي التخصيصات
        total_allocations = merged_allocations["allocation_amount"].sum()
        
        # عرض ملخص التكاليف
        st.markdown(f"**إجمالي التكاليف السنوية للإدارات المساندة:** {total_annual_cost:,} ريال")
        st.markdown(f"**إجمالي قيم المشاريع:** {total_projects_value:,} ريال")
        st.markdown(f"**إجمالي التخصيصات:** {total_allocations:,} ريال")
        st.markdown(f"**نسبة التكاليف السنوية من إجمالي قيم المشاريع:** {(total_annual_cost / total_projects_value) * 100:.2f}%")
        st.markdown(f"**نسبة التخصيصات من إجمالي قيم المشاريع:** {(total_allocations / total_projects_value) * 100:.2f}%")
        st.markdown(f"**نسبة تغطية التكاليف السنوية من خلال التخصيصات:** {(total_allocations / total_annual_cost) * 100:.2f}%")
        
        # إنشاء بيانات للرسم البياني
        comparison_data = pd.DataFrame({
            "البند": ["التكاليف السنوية", "التخصيصات"],
            "القيمة": [total_annual_cost, total_allocations]
        })
        
        # إنشاء رسم بياني للمقارنة
        fig = px.bar(
            comparison_data,
            x="البند",
            y="القيمة",
            title="مقارنة بين التكاليف السنوية والتخصيصات",
            color="البند",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حساب التكاليف والتخصيصات حسب فئة الإدارة
        category_costs = departments.groupby("category").agg({
            "annual_cost": "sum"
        }).reset_index()
        
        category_allocations = merged_allocations.groupby("category").agg({
            "allocation_amount": "sum"
        }).reset_index()
        
        # دمج البيانات
        category_comparison = pd.merge(
            category_costs,
            category_allocations,
            on="category",
            how="left"
        )
        
        category_comparison["نسبة التغطية"] = category_comparison["allocation_amount"] / category_comparison["annual_cost"] * 100
        
        # تغيير أسماء الأعمدة
        category_comparison.columns = ["الفئة", "التكلفة السنوية", "التخصيصات", "نسبة التغطية"]
        
        # عرض الجدول
        st.dataframe(category_comparison, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة حسب الفئة
        category_comparison_data = []
        
        for _, row in category_comparison.iterrows():
            category_comparison_data.extend([
                {"الفئة": row["الفئة"], "البند": "التكلفة السنوية", "القيمة": row["التكلفة السنوية"]},
                {"الفئة": row["الفئة"], "البند": "التخصيصات", "القيمة": row["التخصيصات"]}
            ])
        
        category_comparison_df = pd.DataFrame(category_comparison_data)
        
        fig = px.bar(
            category_comparison_df,
            x="الفئة",
            y="القيمة",
            color="البند",
            title="مقارنة بين التكاليف السنوية والتخصيصات حسب فئة الإدارة",
            barmode="group",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # إنشاء رسم بياني لنسبة التغطية
        fig = px.bar(
            category_comparison,
            x="الفئة",
            y="نسبة التغطية",
            title="نسبة تغطية التكاليف السنوية من خلال التخصيصات حسب فئة الإدارة",
            color="الفئة",
            text_auto=True
        )
        
        # إضافة خط أفقي عند 100%
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=100,
            x1=len(category_comparison) - 0.5,
            y1=100,
            line=dict(
                color="red",
                width=2,
                dash="dash"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل تأثير التخصيصات على تكلفة المشاريع
        project_allocations = merged_allocations.groupby("name_project").agg({
            "allocation_amount": "sum",
            "value": "first"
        }).reset_index()
        
        project_allocations["نسبة التخصيص"] = project_allocations["allocation_amount"] / project_allocations["value"] * 100
        
        # تغيير أسماء الأعمدة
        project_allocations.columns = ["المشروع", "التخصيصات", "قيمة المشروع", "نسبة التخصيص"]
        
        # ترتيب البيانات حسب نسبة التخصيص
        project_allocations = project_allocations.sort_values(by="نسبة التخصيص", ascending=False)
        
        # عرض الجدول
        st.dataframe(project_allocations, use_container_width=True)
        
        # إنشاء رسم بياني لتأثير التخصيصات على تكلفة المشاريع
        fig = px.bar(
            project_allocations,
            x="المشروع",
            y=["قيمة المشروع", "التخصيصات"],
            title="تأثير تخصيصات الإدارات المساندة على تكلفة المشاريع",
            barmode="stack",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_efficiency_analysis_report(self, departments, projects, merged_allocations):
        """عرض تقرير تحليل الكفاءة"""
        
        st.markdown("#### تقرير تحليل الكفاءة")
        
        # حساب مؤشرات الكفاءة للإدارات
        department_efficiency = departments.copy()
        
        # حساب إجمالي التخصيصات لكل إدارة
        department_allocations = merged_allocations.groupby("department_id").agg({
            "allocation_amount": "sum"
        }).reset_index()
        
        # دمج البيانات
        department_efficiency = pd.merge(
            department_efficiency,
            department_allocations,
            left_on="id",
            right_on="department_id",
            how="left"
        )
        
        # حساب مؤشرات الكفاءة
        department_efficiency["allocation_amount"] = department_efficiency["allocation_amount"].fillna(0)
        department_efficiency["نسبة التغطية"] = department_efficiency["allocation_amount"] / department_efficiency["annual_cost"] * 100
        department_efficiency["تكلفة الموظف السنوية"] = department_efficiency["annual_cost"] / department_efficiency["staff_count"]
        department_efficiency["تخصيص الموظف"] = department_efficiency["allocation_amount"] / department_efficiency["staff_count"]
        department_efficiency["مؤشر الكفاءة"] = department_efficiency["تخصيص الموظف"] / department_efficiency["تكلفة الموظف السنوية"] * 100
        
        # تغيير أسماء الأعمدة
        efficiency_display = department_efficiency[["name", "category", "annual_cost", "staff_count", "allocation_amount", "نسبة التغطية", "تكلفة الموظف السنوية", "تخصيص الموظف", "مؤشر الكفاءة"]].copy()
        efficiency_display.columns = ["الإدارة", "الفئة", "التكلفة السنوية", "عدد الموظفين", "التخصيصات", "نسبة التغطية", "تكلفة الموظف السنوية", "تخصيص الموظف", "مؤشر الكفاءة"]
        
        # ترتيب البيانات حسب مؤشر الكفاءة
        efficiency_display = efficiency_display.sort_values(by="مؤشر الكفاءة", ascending=False)
        
        # عرض الجدول
        st.dataframe(efficiency_display, use_container_width=True)
        
        # إنشاء رسم بياني لمؤشر الكفاءة
        fig = px.bar(
            efficiency_display,
            x="الإدارة",
            y="مؤشر الكفاءة",
            title="مؤشر كفاءة الإدارات المساندة",
            color="الفئة",
            text_auto=True
        )
        
        # إضافة خط أفقي عند 100%
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=100,
            x1=len(efficiency_display) - 0.5,
            y1=100,
            line=dict(
                color="red",
                width=2,
                dash="dash"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل العلاقة بين عدد الموظفين ومؤشر الكفاءة
        fig = px.scatter(
            efficiency_display,
            x="عدد الموظفين",
            y="مؤشر الكفاءة",
            title="العلاقة بين عدد الموظفين ومؤشر الكفاءة",
            color="الفئة",
            size="التكلفة السنوية",
            hover_data=["الإدارة"],
            trendline="ols"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل العلاقة بين تكلفة الموظف السنوية ومؤشر الكفاءة
        fig = px.scatter(
            efficiency_display,
            x="تكلفة الموظف السنوية",
            y="مؤشر الكفاءة",
            title="العلاقة بين تكلفة الموظف السنوية ومؤشر الكفاءة",
            color="الفئة",
            size="عدد الموظفين",
            hover_data=["الإدارة"],
            trendline="ols"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل كفاءة الإدارات حسب الفئة
        category_efficiency = efficiency_display.groupby("الفئة").agg({
            "التكلفة السنوية": "sum",
            "عدد الموظفين": "sum",
            "التخصيصات": "sum",
            "مؤشر الكفاءة": "mean"
        }).reset_index()
        
        category_efficiency["نسبة التغطية"] = category_efficiency["التخصيصات"] / category_efficiency["التكلفة السنوية"] * 100
        category_efficiency["تكلفة الموظف السنوية"] = category_efficiency["التكلفة السنوية"] / category_efficiency["عدد الموظفين"]
        
        # عرض الجدول
        st.dataframe(category_efficiency, use_container_width=True)
        
        # إنشاء رسم بياني لمؤشر الكفاءة حسب الفئة
        fig = px.bar(
            category_efficiency,
            x="الفئة",
            y="مؤشر الكفاءة",
            title="متوسط مؤشر كفاءة الإدارات المساندة حسب الفئة",
            color="الفئة",
            text_auto=True
        )
        
        # إضافة خط أفقي عند 100%
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=100,
            x1=len(category_efficiency) - 0.5,
            y1=100,
            line=dict(
                color="red",
                width=2,
                dash="dash"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # توصيات لتحسين الكفاءة
        st.markdown("#### توصيات لتحسين الكفاءة")
        
        # تحديد الإدارات ذات الكفاءة المنخفضة
        low_efficiency_departments = efficiency_display[efficiency_display["مؤشر الكفاءة"] < 80].sort_values(by="مؤشر الكفاءة")
        
        if not low_efficiency_departments.empty:
            st.markdown("##### الإدارات ذات الكفاءة المنخفضة")
            
            for _, row in low_efficiency_departments.iterrows():
                st.markdown(f"**{row['الإدارة']} (مؤشر الكفاءة: {row['مؤشر الكفاءة']:.2f}%):**")
                
                if row["نسبة التغطية"] < 80:
                    st.markdown("- زيادة التخصيصات للإدارة من خلال مراجعة طريقة التخصيص")
                
                if row["تكلفة الموظف السنوية"] > category_efficiency[category_efficiency["الفئة"] == row["الفئة"]]["تكلفة الموظف السنوية"].values[0]:
                    st.markdown("- مراجعة تكلفة الموظفين في الإدارة")
                
                st.markdown("- تحسين إنتاجية الإدارة من خلال تطوير العمليات وأتمتة الأعمال")
                st.markdown("- مراجعة عدد الموظفين في الإدارة")
                
                st.markdown("---")
        else:
            st.success("جميع الإدارات تتمتع بمستوى كفاءة جيد (أكثر من 80%)")
        
        # تحديد الإدارات ذات الكفاءة العالية
        high_efficiency_departments = efficiency_display[efficiency_display["مؤشر الكفاءة"] > 120].sort_values(by="مؤشر الكفاءة", ascending=False)
        
        if not high_efficiency_departments.empty:
            st.markdown("##### الإدارات ذات الكفاءة العالية")
            
            for _, row in high_efficiency_departments.iterrows():
                st.markdown(f"**{row['الإدارة']} (مؤشر الكفاءة: {row['مؤشر الكفاءة']:.2f}%):**")
                
                if row["نسبة التغطية"] > 120:
                    st.markdown("- مراجعة طريقة التخصيص للتأكد من عدم المبالغة في التخصيصات")
                
                st.markdown("- دراسة أسباب ارتفاع الكفاءة والاستفادة منها في تطوير الإدارات الأخرى")
                st.markdown("- تقييم جودة الخدمات المقدمة للتأكد من عدم تأثرها بارتفاع الكفاءة")
                
                st.markdown("---")
        
        # توصيات عامة
        st.markdown("##### توصيات عامة لتحسين كفاءة الإدارات المساندة")
        
        st.markdown("1. مراجعة طرق تخصيص تكاليف الإدارات المساندة للمشاريع")
        st.markdown("2. تطوير نظام لقياس أداء الإدارات المساندة")
        st.markdown("3. تحسين عمليات الإدارات المساندة من خلال أتمتة الأعمال")
        st.markdown("4. تطوير برامج تدريبية لرفع كفاءة الموظفين")
        st.markdown("5. مراجعة الهيكل التنظيمي للإدارات المساندة")
        st.markdown("6. تطبيق مبادئ الإدارة الرشيقة (Lean Management) في الإدارات المساندة")
        st.markdown("7. تحسين التنسيق بين الإدارات المساندة والمشاريع")
    
    def calculate_project_indirect_cost(self, project_id):
        """حساب تكلفة الإدارات المساندة لمشروع معين"""
        
        # استخراج البيانات
        allocations = st.session_state.indirect_support["allocations"]
        
        # حساب إجمالي التخصيصات للمشروع
        project_allocations = allocations[allocations["project_id"] == project_id]
        
        if not project_allocations.empty:
            return project_allocations["allocation_amount"].sum()
        
        return 0
    
    def calculate_department_allocations(self, department_id):
        """حساب تخصيصات إدارة معينة"""
        
        # استخراج البيانات
        allocations = st.session_state.indirect_support["allocations"]
        
        # حساب إجمالي التخصيصات للإدارة
        department_allocations = allocations[allocations["department_id"] == department_id]
        
        if not department_allocations.empty:
            return department_allocations["allocation_amount"].sum()
        
        return 0
    
    def get_department_by_id(self, department_id):
        """الحصول على إدارة بواسطة الكود"""
        
        # استخراج البيانات
        departments = st.session_state.indirect_support["departments"]
        
        # البحث عن الإدارة
        department = departments[departments["id"] == department_id]
        
        if not department.empty:
            return department.iloc[0].to_dict()
        
        return None
    
    def get_project_by_id(self, project_id):
        """الحصول على مشروع بواسطة الكود"""
        
        # استخراج البيانات
        projects = st.session_state.indirect_support["projects"]
        
        # البحث عن المشروع
        project = projects[projects["id"] == project_id]
        
        if not project.empty:
            return project.iloc[0].to_dict()
        
        return None
