"""
وحدة الموارد - التطبيق الرئيسي
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import io
import os
import json
import base64
from pathlib import Path

class ResourcesApp:
    """وحدة الموارد"""

    def __init__(self):
        """تهيئة وحدة الموارد"""

        # تهيئة حالة الجلسة
        if 'resources_data' not in st.session_state:
            # إنشاء بيانات افتراضية للموارد البشرية
            np.random.seed(42)

            # إنشاء بيانات الموظفين
            n_employees = 50
            employee_ids = [f"EMP-{i+1:03d}" for i in range(n_employees)]
            employee_names = [
                "أحمد محمد", "محمد علي", "علي إبراهيم", "إبراهيم خالد", "خالد عبدالله",
                "عبدالله سعد", "سعد فهد", "فهد ناصر", "ناصر سلطان", "سلطان عمر",
                "عمر يوسف", "يوسف عبدالرحمن", "عبدالرحمن حسن", "حسن أحمد", "أحمد عبدالعزيز",
                "عبدالعزيز سعود", "سعود فيصل", "فيصل تركي", "تركي بندر", "بندر سلمان",
                "سلمان محمد", "محمد عبدالله", "عبدالله فهد", "فهد سعد", "سعد خالد",
                "خالد علي", "علي عمر", "عمر سعيد", "سعيد ماجد", "ماجد فارس",
                "فارس نايف", "نايف سامي", "سامي راشد", "راشد وليد", "وليد هاني",
                "هاني زياد", "زياد طارق", "طارق عادل", "عادل فراس", "فراس باسم",
                "باسم جمال", "جمال كريم", "كريم نبيل", "نبيل هشام", "هشام عماد",
                "عماد أيمن", "أيمن رامي", "رامي سمير", "سمير وائل", "وائل مازن"
            ]
            employee_departments = np.random.choice(["الهندسة", "المشتريات", "المالية", "الموارد البشرية", "تقنية المعلومات", "التسويق", "المبيعات"], n_employees)
            employee_positions = np.random.choice(["مدير", "مهندس", "محلل", "مطور", "مصمم", "مشرف", "منسق", "أخصائي", "مساعد"], n_employees)
            employee_salaries = np.random.randint(5000, 25000, n_employees)
            employee_experiences = np.random.randint(1, 20, n_employees)
            employee_availabilities = np.random.choice([True, False], n_employees, p=[0.7, 0.3])

            # إنشاء DataFrame للموظفين
            employees_data = {
                "رقم الموظف": employee_ids,
                "الاسم": employee_names,
                "القسم": employee_departments,
                "المنصب": employee_positions,
                "التكلفة الشهرية": employee_salaries,
                "سنوات الخبرة": employee_experiences,
                "متاح": employee_availabilities
            }

            # إنشاء بيانات المعدات
            n_equipment = 30
            equipment_ids = [f"EQP-{i+1:03d}" for i in range(n_equipment)]
            equipment_names = [
                "حفارة", "جرافة", "شاحنة نقل", "رافعة", "خلاطة خرسانة", "مولد كهرباء", "ضاغط هواء",
                "مضخة مياه", "آلة حفر", "آلة تسوية", "آلة رصف", "آلة تشكيل", "آلة قطع", "آلة لحام",
                "آلة طلاء", "آلة تنظيف", "آلة تعبئة", "آلة تغليف", "آلة فرز", "آلة تجميع",
                "آلة تثقيب", "آلة تجليخ", "آلة تفريز", "آلة خراطة", "آلة تشكيل", "آلة تقطيع",
                "آلة تجفيف", "آلة تبريد", "آلة تسخين", "آلة تهوية"
            ]
            equipment_types = np.random.choice(["حفر", "نقل", "رفع", "خلط", "توليد", "ضغط", "ضخ", "تشكيل", "قطع", "لحام", "طلاء", "تنظيف", "تعبئة", "تغليف", "فرز", "تجميع", "تثقيب", "تجليخ", "تفريز", "خراطة"], n_equipment)
            equipment_costs = np.random.randint(500, 5000, n_equipment)
            equipment_availabilities = np.random.choice([True, False], n_equipment, p=[0.8, 0.2])
            equipment_conditions = np.random.choice(["ممتاز", "جيد", "متوسط", "سيء"], n_equipment, p=[0.4, 0.3, 0.2, 0.1])
            equipment_locations = np.random.choice(["المستودع", "موقع العمل 1", "موقع العمل 2", "موقع العمل 3", "في الصيانة"], n_equipment)

            # إنشاء DataFrame للمعدات
            equipment_data = {
                "رقم المعدة": equipment_ids,
                "الاسم": equipment_names,
                "النوع": equipment_types,
                "التكلفة اليومية": equipment_costs,
                "متاحة": equipment_availabilities,
                "الحالة": equipment_conditions,
                "الموقع": equipment_locations
            }

            # إنشاء بيانات المواد
            n_materials = 40
            material_ids = [f"MAT-{i+1:03d}" for i in range(n_materials)]
            material_names = [
                "خرسانة جاهزة", "حديد تسليح", "طابوق", "أسمنت", "رمل", "بحص", "خشب", "ألمنيوم", "زجاج", "دهان",
                "سيراميك", "رخام", "جبس", "عازل مائي", "عازل حراري", "أنابيب PVC", "أسلاك كهربائية", "مفاتيح كهربائية",
                "إنارة", "تكييف", "مصاعد", "أبواب خشبية", "أبواب حديدية", "نوافذ ألمنيوم", "نوافذ زجاجية",
                "أرضيات خشبية", "أرضيات بلاط", "أرضيات رخام", "أرضيات سيراميك", "أرضيات بورسلين",
                "دهان داخلي", "دهان خارجي", "مواد عزل", "مواد تشطيب", "مواد كهربائية", "مواد سباكة",
                "مواد تكييف", "مواد إضاءة", "مواد سلامة", "مواد متنوعة"
            ]
            material_units = np.random.choice(["م3", "طن", "م2", "كجم", "لتر", "قطعة", "متر"], n_materials)
            material_quantities = np.random.randint(10, 1000, n_materials)
            material_costs = np.random.randint(50, 5000, n_materials)
            material_suppliers = np.random.choice(["المورد 1", "المورد 2", "المورد 3", "المورد 4", "المورد 5"], n_materials)
            material_lead_times = np.random.randint(1, 30, n_materials)

            # إنشاء DataFrame للمواد
            materials_data = {
                "رقم المادة": material_ids,
                "اسم المادة": material_names,
                "الوحدة": material_units,
                "الكمية المتاحة": material_quantities,
                "تكلفة الوحدة": material_costs,
                "المورد": material_suppliers,
                "مدة التوريد (يوم)": material_lead_times
            }

            # إنشاء بيانات المشاريع
            n_projects = 10
            project_ids = [f"PRJ-{i+1:03d}" for i in range(n_projects)]
            project_names = [
                "مشروع إنشاء مبنى إداري", "مشروع إنشاء مبنى سكني", "مشروع إنشاء مدرسة",
                "مشروع إنشاء مستشفى", "مشروع تطوير طرق", "مشروع إنشاء جسر",
                "مشروع بنية تحتية", "مشروع إنشاء مركز تجاري", "مشروع إنشاء فندق",
                "مشروع إنشاء مصنع"
            ]
            project_locations = np.random.choice(["الرياض", "جدة", "الدمام", "مكة", "المدينة", "أبها", "تبوك"], n_projects)
            project_start_dates = [
                (datetime.now() - timedelta(days=np.random.randint(0, 180))).strftime("%Y-%m-%d")
                for _ in range(n_projects)
            ]
            project_end_dates = [
                (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=np.random.randint(180, 720))).strftime("%Y-%m-%d")
                for start_date in project_start_dates
            ]
            project_budgets = np.random.randint(1000000, 50000000, n_projects)
            project_statuses = np.random.choice(["قيد التنفيذ", "مكتمل", "متوقف", "مخطط"], n_projects)

            # إنشاء DataFrame للمشاريع
            projects_data = {
                "رقم المشروع": project_ids,
                "اسم المشروع": project_names,
                "الموقع": project_locations,
                "تاريخ البدء": project_start_dates,
                "تاريخ الانتهاء": project_end_dates,
                "الميزانية": project_budgets,
                "الحالة": project_statuses
            }

            # إنشاء بيانات تخصيص الموارد للمشاريع
            n_allocations = 100
            allocation_ids = [f"ALLOC-{i+1:03d}" for i in range(n_allocations)]
            allocation_projects = np.random.choice(project_ids, n_allocations)
            allocation_resource_types = np.random.choice(["موظف", "معدة", "مادة"], n_allocations)
            allocation_resource_ids = []
            for res_type in allocation_resource_types:
                if res_type == "موظف":
                    allocation_resource_ids.append(np.random.choice(employee_ids))
                elif res_type == "معدة":
                    allocation_resource_ids.append(np.random.choice(equipment_ids))
                else:
                    allocation_resource_ids.append(np.random.choice(material_ids))

            allocation_start_dates = [
                (datetime.now() - timedelta(days=np.random.randint(0, 90))).strftime("%Y-%m-%d")
                for _ in range(n_allocations)
            ]
            allocation_end_dates = [
                (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=np.random.randint(30, 180))).strftime("%Y-%m-%d")
                for start_date in allocation_start_dates
            ]
            allocation_quantities = np.random.randint(1, 10, n_allocations)
            allocation_costs = np.random.randint(5000, 50000, n_allocations)

            # إنشاء DataFrame لتخصيص الموارد
            allocations_data = {
                "رقم التخصيص": allocation_ids,
                "رقم المشروع": allocation_projects,
                "نوع المورد": allocation_resource_types,
                "رقم المورد": allocation_resource_ids,
                "تاريخ البدء": allocation_start_dates,
                "تاريخ الانتهاء": allocation_end_dates,
                "الكمية": allocation_quantities,
                "التكلفة": allocation_costs
            }

            # تخزين البيانات في حالة الجلسة
            st.session_state.resources_data = {
                "employees": pd.DataFrame(employees_data),
                "equipment": pd.DataFrame(equipment_data),
                "materials": pd.DataFrame(materials_data),
                "projects": pd.DataFrame(projects_data),
                "allocations": pd.DataFrame(allocations_data)
            }

    def run(self):
        """
        تشغيل وحدة الموارد

        هذه الدالة هي نقطة الدخول الرئيسية لوحدة الموارد وتقوم بتهيئة واجهة المستخدم
        وعرض جميع العناصر المطلوبة.
        """
        # استدعاء دالة العرض الرئيسية
        self.render()

    def render(self):
        """عرض واجهة وحدة الموارد"""

        st.markdown("<h1 class='module-title'>وحدة الموارد</h1>", unsafe_allow_html=True)

        tabs = st.tabs([
            "لوحة المعلومات", 
            "الموارد البشرية",
            "المعدات",
            "المواد",
            "تخصيص الموارد",
            "تخطيط الموارد"
        ])

        with tabs[0]:
            self._render_dashboard_tab()

        with tabs[1]:
            self._render_human_resources_tab()

        with tabs[2]:
            self._render_equipment_tab()

        with tabs[3]:
            self._render_materials_tab()

        with tabs[4]:
            self._render_resource_allocation_tab()

        with tabs[5]:
            self._render_resource_planning_tab()

    def _render_dashboard_tab(self):
        """عرض تبويب لوحة المعلومات"""

        st.markdown("### لوحة معلومات الموارد")

        # استخراج البيانات
        employees_df = st.session_state.resources_data["employees"]
        equipment_df = st.session_state.resources_data["equipment"]
        materials_df = st.session_state.resources_data["materials"]
        projects_df = st.session_state.resources_data["projects"]
        allocations_df = st.session_state.resources_data["allocations"]

        # عرض مؤشرات الأداء الرئيسية
        st.markdown("#### مؤشرات الأداء الرئيسية")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_employees = len(employees_df)
            available_employees = len(employees_df[employees_df["متاح"] == True])
            st.metric("الموظفون", f"{available_employees}/{total_employees}")

        with col2:
            total_equipment = len(equipment_df)
            available_equipment = len(equipment_df[equipment_df["متاحة"] == True])
            st.metric("المعدات", f"{available_equipment}/{total_equipment}")

        with col3:
            total_materials = len(materials_df)
            low_stock_materials = len(materials_df[materials_df["الكمية المتاحة"] < 50])
            st.metric("المواد", f"{total_materials}", f"-{low_stock_materials} منخفضة المخزون")

        with col4:
            total_projects = len(projects_df)
            active_projects = len(projects_df[projects_df["الحالة"] == "قيد التنفيذ"])
            st.metric("المشاريع النشطة", f"{active_projects}/{total_projects}")

        # عرض توزيع الموارد البشرية حسب القسم
        st.markdown("#### توزيع الموارد البشرية حسب القسم")

        dept_counts = employees_df["القسم"].value_counts().reset_index()
        dept_counts.columns = ["القسم", "العدد"]

        fig = px.pie(
            dept_counts,
            values="العدد",
            names="القسم",
            title="توزيع الموظفين حسب القسم",
            color="القسم"
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض توزيع المعدات حسب النوع
        st.markdown("#### توزيع المعدات حسب النوع")

        type_counts = equipment_df["النوع"].value_counts().reset_index()
        type_counts.columns = ["النوع", "العدد"]

        fig = px.bar(
            type_counts,
            x="النوع",
            y="العدد",
            title="توزيع المعدات حسب النوع",
            color="النوع",
            text_auto=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض توزيع المواد حسب المورد
        st.markdown("#### توزيع المواد حسب المورد")

        supplier_counts = materials_df["المورد"].value_counts().reset_index()
        supplier_counts.columns = ["المورد", "العدد"]

        fig = px.pie(
            supplier_counts,
            values="العدد",
            names="المورد",
            title="توزيع المواد حسب المورد",
            color="المورد"
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض توزيع تكاليف الموارد
        st.markdown("#### توزيع تكاليف الموارد")

        # حساب إجمالي تكاليف الموظفين
        total_employee_cost = employees_df["التكلفة الشهرية"].sum()

        # حساب إجمالي تكاليف المعدات (افتراضياً لشهر واحد)
        total_equipment_cost = equipment_df["التكلفة اليومية"].sum() * 30

        # حساب إجمالي تكاليف المواد
        total_material_cost = (materials_df["الكمية المتاحة"] * materials_df["تكلفة الوحدة"]).sum()

        # إنشاء DataFrame لتوزيع التكاليف
        cost_distribution = pd.DataFrame({
            "نوع المورد": ["الموظفون", "المعدات", "المواد"],
            "التكلفة": [total_employee_cost, total_equipment_cost, total_material_cost]
        })

        fig = px.pie(
            cost_distribution,
            values="التكلفة",
            names="نوع المورد",
            title="توزيع تكاليف الموارد",
            color="نوع المورد",
            color_discrete_map={
                "الموظفون": "#3498db",
                "المعدات": "#2ecc71",
                "المواد": "#f39c12"
            }
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض تخصيص الموارد للمشاريع
        st.markdown("#### تخصيص الموارد للمشاريع")

        # حساب عدد الموارد المخصصة لكل مشروع
        project_allocations = allocations_df["رقم المشروع"].value_counts().reset_index()
        project_allocations.columns = ["رقم المشروع", "عدد الموارد المخصصة"]

        # دمج بيانات المشاريع مع بيانات التخصيص
        project_allocations = project_allocations.merge(
            projects_df[["رقم المشروع", "اسم المشروع", "الحالة"]],
            on="رقم المشروع",
            how="left"
        )

        fig = px.bar(
            project_allocations,
            x="اسم المشروع",
            y="عدد الموارد المخصصة",
            title="توزيع الموارد على المشاريع",
            text_auto=True
        )
        st.plotly_chart(fig, use_container_width=True)


    def _render_human_resources_tab(self):
        """عرض تبويب الموارد البشرية"""
        st.markdown("### الموارد البشرية")
        # إضافة محتوى تبويب الموارد البشرية هنا ...
        pass

    def _render_equipment_tab(self):
        """عرض تبويب المعدات"""
        st.markdown("### المعدات")
        # إضافة محتوى تبويب المعدات هنا ...
        pass

    def _render_materials_tab(self):
        """عرض تبويب المواد"""
        st.markdown("### المواد")
        # إضافة محتوى تبويب المواد هنا ...
        pass

    def _render_resource_allocation_tab(self):
        """عرض تبويب تخصيص الموارد"""
        st.markdown("### تخصيص الموارد")
        # إضافة محتوى تبويب تخصيص الموارد هنا ...
        pass

    def _render_resource_planning_tab(self):
        """عرض تبويب تخطيط الموارد"""
        st.markdown("### تخطيط الموارد")
        # إضافة محتوى تبويب تخطيط الموارد هنا ...
        pass