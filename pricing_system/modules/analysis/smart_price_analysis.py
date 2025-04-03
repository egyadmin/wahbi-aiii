"""
وحدة التحليل الذكي للأسعار - تحليل أسعار البنود بطريقة ذكية
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
import math

class SmartPriceAnalysis:
    """فئة التحليل الذكي للأسعار"""

    def __init__(self):
        """تهيئة وحدة التحليل الذكي للأسعار"""

        # تهيئة حالة الجلسة للتحليل الذكي للأسعار
        if 'smart_price_analysis' not in st.session_state:
            self._initialize_smart_price_analysis()

        # الوصول إلى كتالوجات الموارد
        self.equipment_catalog = self._get_equipment_catalog()
        self.materials_catalog = self._get_materials_catalog()
        self.labor_catalog = self._get_labor_catalog()
        self.subcontractors_catalog = self._get_subcontractors_catalog()
        self.cost_breakdown = {} #Added this line

    def _initialize_smart_price_analysis(self):
        """تهيئة بيانات التحليل الذكي للأسعار"""

        # إنشاء بيانات افتراضية للتحليل الذكي للأسعار
        st.session_state.smart_price_analysis = {
            "price_components": {
                "materials": 0.45,  # نسبة المواد من إجمالي التكلفة
                "equipment": 0.25,  # نسبة المعدات من إجمالي التكلفة
                "labor": 0.20,      # نسبة العمالة من إجمالي التكلفة
                "subcontractors": 0.10  # نسبة مقاولي الباطن من إجمالي التكلفة
            },
            "indirect_costs": {
                "overhead": 0.10,    # نسبة المصاريف العمومية والإدارية
                "profit": 0.15,      # نسبة الربح
                "contingency": 0.05,  # نسبة الطوارئ
                "bonds": 0.02,        # نسبة الضمانات
                "insurance": 0.03     # نسبة التأمين
            },
            "local_content": {
                "target": 0.40,      # النسبة المستهدفة للمحتوى المحلي
                "materials_local": 0.30,  # نسبة المواد المحلية
                "equipment_local": 0.20,  # نسبة المعدات المحلية
                "labor_local": 0.80,      # نسبة العمالة المحلية
                "subcontractors_local": 0.60  # نسبة مقاولي الباطن المحليين
            },
            "productivity_factors": {
                "weather": 1.0,      # عامل الطقس
                "location": 1.0,     # عامل الموقع
                "complexity": 1.0,   # عامل التعقيد
                "schedule": 1.0,     # عامل الجدول الزمني
                "resources": 1.0     # عامل الموارد
            },
            "analysis_history": [],  # سجل تحليلات الأسعار
            "current_item": None     # البند الحالي قيد التحليل
        }

        # إنشاء بيانات افتراضية لبنود جدول الكميات
        if 'boq_items' not in st.session_state:
            self._initialize_boq_items()

    def _initialize_boq_items(self):
        """تهيئة بيانات بنود جدول الكميات"""

        # إنشاء بيانات افتراضية لبنود جدول الكميات
        boq_items = [
            {
                "id": "C-001",
                "description": "توريد وصب خرسانة مسلحة للأساسات",
                "unit": "م3",
                "quantity": 500,
                "unit_price": 1200,
                "total_price": 600000,
                "category": "أعمال الخرسانة",
                "subcategory": "أساسات",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "C-002",
                "description": "توريد وصب خرسانة مسلحة للأعمدة",
                "unit": "م3",
                "quantity": 300,
                "unit_price": 1500,
                "total_price": 450000,
                "category": "أعمال الخرسانة",
                "subcategory": "أعمدة",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "E-001",
                "description": "حفر وردم لزوم الأساسات",
                "unit": "م3",
                "quantity": 800,
                "unit_price": 80,
                "total_price": 64000,
                "category": "أعمال الحفر والردم",
                "subcategory": "حفر",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "R-001",
                "description": "توريد وتركيب طبقة أساس من الحصى المدكوك",
                "unit": "م2",
                "quantity": 2000,
                "unit_price": 120,
                "total_price": 240000,
                "category": "أعمال الطرق",
                "subcategory": "طبقة أساس",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "R-002",
                "description": "توريد وفرش طبقة إسفلتية سمك 5 سم",
                "unit": "م2",
                "quantity": 2000,
                "unit_price": 180,
                "total_price": 360000,
                "category": "أعمال الطرق",
                "subcategory": "طبقة إسفلتية",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "S-001",
                "description": "توريد وتركيب مواسير صرف صحي قطر 300 مم",
                "unit": "م.ط",
                "quantity": 1500,
                "unit_price": 450,
                "total_price": 675000,
                "category": "أعمال الصرف الصحي",
                "subcategory": "مواسير",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "S-002",
                "description": "توريد وتركيب غرف تفتيش قطر 1.0 م",
                "unit": "عدد",
                "quantity": 50,
                "unit_price": 3500,
                "total_price": 175000,
                "category": "أعمال الصرف الصحي",
                "subcategory": "غرف تفتيش",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "E-002",
                "description": "توريد وتركيب كابلات كهربائية جهد منخفض",
                "unit": "م.ط",
                "quantity": 3000,
                "unit_price": 120,
                "total_price": 360000,
                "category": "أعمال الكهرباء",
                "subcategory": "كابلات",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "E-003",
                "description": "توريد وتركيب أعمدة إنارة ارتفاع 10 م",
                "unit": "عدد",
                "quantity": 80,
                "unit_price": 5000,
                "total_price": 400000,
                "category": "أعمال الكهرباء",
                "subcategory": "إنارة",
                "analyzed": False,
                "components": {}
            },
            {
                "id": "W-001",
                "description": "توريد وتركيب مواسير مياه قطر 200 مم",
                "unit": "م.ط",
                "quantity": 2000,
                "unit_price": 350,
                "total_price": 700000,
                "category": "أعمال المياه",
                "subcategory": "مواسير",
                "analyzed": False,
                "components": {}
            }
        ]

        # تخزين البيانات في حالة الجلسة
        st.session_state.boq_items = pd.DataFrame(boq_items)

    def _get_equipment_catalog(self):
        """الحصول على كتالوج المعدات"""

        # التحقق من وجود كتالوج المعدات في حالة الجلسة
        if 'equipment_catalog' in st.session_state:
            return st.session_state.equipment_catalog

        # إذا لم يكن موجوداً، إنشاء كتالوج افتراضي
        equipment_data = []

        # تخزين البيانات في حالة الجلسة
        st.session_state.equipment_catalog = pd.DataFrame(equipment_data)

        return st.session_state.equipment_catalog

    def _get_materials_catalog(self):
        """الحصول على كتالوج المواد"""

        # التحقق من وجود كتالوج المواد في حالة الجلسة
        if 'materials_catalog' in st.session_state:
            return st.session_state.materials_catalog

        # إذا لم يكن موجوداً، إنشاء كتالوج افتراضي
        materials_data = []

        # تخزين البيانات في حالة الجلسة
        st.session_state.materials_catalog = pd.DataFrame(materials_data)

        return st.session_state.materials_catalog

    def _get_labor_catalog(self):
        """الحصول على كتالوج العمالة"""

        # التحقق من وجود كتالوج العمالة في حالة الجلسة
        if 'labor_catalog' in st.session_state:
            return st.session_state.labor_catalog

        # إذا لم يكن موجوداً، إنشاء كتالوج افتراضي
        labor_data = []

        # تخزين البيانات في حالة الجلسة
        st.session_state.labor_catalog = pd.DataFrame(labor_data)

        return st.session_state.labor_catalog

    def _get_subcontractors_catalog(self):
        """الحصول على كتالوج مقاولي الباطن"""

        # التحقق من وجود كتالوج مقاولي الباطن في حالة الجلسة
        if 'subcontractors_catalog' in st.session_state:
            return st.session_state.subcontractors_catalog

        # إذا لم يكن موجوداً، إنشاء كتالوج افتراضي
        subcontractors_data = []

        # تخزين البيانات في حالة الجلسة
        st.session_state.subcontractors_catalog = pd.DataFrame(subcontractors_data)

        return st.session_state.subcontractors_catalog

    def render(self):
        """عرض واجهة التحليل الذكي للأسعار"""

        st.markdown("## التحليل الذكي للأسعار")

        # إنشاء تبويبات لعرض التحليل الذكي للأسعار
        tabs = st.tabs([
            "تحليل البنود", 
            "إعدادات التحليل", 
            "تقارير التحليل",
            "المحتوى المحلي"
        ])

        with tabs[0]:
            self._render_item_analysis_tab()

        with tabs[1]:
            self._render_analysis_settings_tab()

        with tabs[2]:
            self._render_analysis_reports_tab()

        with tabs[3]:
            self._render_local_content_tab()

    def _render_item_analysis_tab(self):
        """عرض تبويب تحليل البنود"""

        st.markdown("### تحليل بنود جدول الكميات")

        # استخراج البيانات
        boq_items = st.session_state.boq_items

        # إنشاء فلاتر للعرض
        col1, col2, col3 = st.columns(3)

        with col1:
            # فلتر حسب الفئة
            categories = ["الكل"] + sorted(boq_items["category"].unique().tolist())
            selected_category = st.selectbox("اختر فئة البند", categories, key="item_analysis_category")

        with col2:
            # فلتر حسب الفئة الفرعية
            if selected_category != "الكل":
                subcategories = ["الكل"] + sorted(boq_items[boq_items["category"] == selected_category]["subcategory"].unique().tolist())
            else:
                subcategories = ["الكل"] + sorted(boq_items["subcategory"].unique().tolist())

            selected_subcategory = st.selectbox("اختر التخصص", subcategories, key="item_analysis_subcategory")

        with col3:
            # فلتر حسب حالة التحليل
            analysis_status = ["الكل", "تم التحليل", "لم يتم التحليل"]
            selected_status = st.selectbox("اختر حالة التحليل", analysis_status, key="item_analysis_status")

        # تطبيق الفلاتر
        filtered_df = boq_items.copy()

        if selected_category != "الكل":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]

        if selected_subcategory != "الكل":
            filtered_df = filtered_df[filtered_df["subcategory"] == selected_subcategory]

        if selected_status != "الكل":
            if selected_status == "تم التحليل":
                filtered_df = filtered_df[filtered_df["analyzed"] == True]
            else:
                filtered_df = filtered_df[filtered_df["analyzed"] == False]

        # عرض البيانات
        if not filtered_df.empty:
            # عرض عدد النتائج
            st.info(f"تم العثور على {len(filtered_df)} بند")

            # إنشاء جدول للعرض
            display_df = filtered_df[["id", "description", "unit", "quantity", "unit_price", "total_price", "analyzed"]].copy()
            display_df.columns = ["الكود", "الوصف", "الوحدة", "الكمية", "سعر الوحدة", "الإجمالي", "تم التحليل"]
            display_df["تم التحليل"] = display_df["تم التحليل"].map({True: "✅", False: "❌"})

            # عرض الجدول
            st.dataframe(display_df, use_container_width=True)

            # اختيار بند للتحليل
            st.markdown("#### اختر بند للتحليل")

            selected_item_id = st.selectbox("اختر كود البند", filtered_df["id"].tolist(), key="item_analysis_selected_id")

            # استخراج البند المختار
            selected_item = filtered_df[filtered_df["id"] == selected_item_id].iloc[0]

            # عرض تفاصيل البند
            st.markdown(f"**البند:** {selected_item['description']}")
            st.markdown(f"**الوحدة:** {selected_item['unit']} | **الكمية:** {selected_item['quantity']} | **سعر الوحدة:** {selected_item['unit_price']} ريال | **الإجمالي:** {selected_item['total_price']} ريال")

            # تحليل البند
            st.markdown("#### تحليل البند")

            # التحقق من حالة التحليل
            if selected_item["analyzed"]:
                # عرض نتائج التحليل السابق
                st.success("تم تحليل هذا البند مسبقاً")

                # استخراج مكونات البند
                components = selected_item["components"]

                # عرض مكونات البند
                self._display_item_components(selected_item)

                # زر إعادة التحليل
                if st.button("إعادة تحليل البند", key="reanalyze_button"):
                    # تعيين البند الحالي
                    st.session_state.smart_price_analysis["current_item"] = selected_item.to_dict()

                    # إعادة توجيه إلى صفحة التحليل
                    st.rerun()
            else:
                # تحليل البند لأول مرة
                if st.button("تحليل البند", key="analyze_button"):
                    # تعيين البند الحالي
                    st.session_state.smart_price_analysis["current_item"] = selected_item.to_dict()

                    # إعادة توجيه إلى صفحة التحليل
                    st.rerun()

            # التحقق من وجود بند حالي قيد التحليل
            current_item = st.session_state.smart_price_analysis["current_item"]

            if current_item and current_item["id"] == selected_item_id:
                # عرض نموذج التحليل
                self._render_analysis_form(current_item)
        else:
            st.warning("لا يوجد بنود تطابق معايير البحث")

    def _render_analysis_form(self, item):
        """عرض نموذج تحليل البند"""

        st.markdown("### تحليل البند")
        st.markdown(f"**البند:** {item['description']}")
        st.markdown(f"**الوحدة:** {item['unit']} | **الكمية:** {item['quantity']} | **سعر الوحدة:** {item['unit_price']} ريال | **الإجمالي:** {item['total_price']} ريال")

        # استخراج نسب المكونات
        price_components = st.session_state.smart_price_analysis["price_components"]

        # حساب قيم المكونات
        materials_value = item["unit_price"] * price_components["materials"]
        equipment_value = item["unit_price"] * price_components["equipment"]
        labor_value = item["unit_price"] * price_components["labor"]
        subcontractors_value = item["unit_price"] * price_components["subcontractors"]

        # إنشاء نموذج التحليل
        with st.form("analysis_form"):
            st.markdown("#### تحليل سعر الوحدة")

            # المواد
            st.markdown("##### المواد")
            materials_col1, materials_col2 = st.columns(2)

            with materials_col1:
                materials_percentage = st.slider(
                    "نسبة المواد من سعر الوحدة",
                    min_value=0.0,
                    max_value=1.0,
                    value=price_components["materials"],
                    step=0.01,
                    format="%g%%",
                    key="materials_percentage"
                ) * 100

            with materials_col2:
                materials_amount = st.number_input(
                    "قيمة المواد (ريال)",
                    min_value=0.0,
                    value=float(materials_value),
                    step=10.0,
                    key="materials_amount"
                )

            # إضافة المواد
            materials_items = []

            st.markdown("إضافة المواد")

            for i in range(3):  # السماح بإضافة 3 مواد كحد أقصى
                material_col1, material_col2, material_col3, material_col4 = st.columns([3, 1, 1, 1])

                with material_col1:
                    material_name = st.text_input(
                        "اسم المادة",
                        key=f"material_name_{i}"
                    )

                with material_col2:
                    material_unit = st.text_input(
                        "الوحدة",
                        key=f"material_unit_{i}"
                    )

                with material_col3:
                    material_quantity = st.number_input(
                        "الكمية",
                        min_value=0.0,
                        step=0.1,
                        key=f"material_quantity_{i}"
                    )

                with material_col4:
                    material_price = st.number_input(
                        "السعر",
                        min_value=0.0,
                        step=10.0,
                        key=f"material_price_{i}"
                    )

                if material_name and material_unit and material_quantity > 0 and material_price > 0:
                    materials_items.append({
                        "name": material_name,
                        "unit": material_unit,
                        "quantity": material_quantity,
                        "price": material_price,
                        "total": material_quantity * material_price
                    })

            # المعدات
            st.markdown("##### المعدات")
            equipment_col1, equipment_col2 = st.columns(2)

            with equipment_col1:
                equipment_percentage = st.slider(
                    "نسبة المعدات من سعر الوحدة",
                    min_value=0.0,
                    max_value=1.0,
                    value=price_components["equipment"],
                    step=0.01,
                    format="%g%%",
                    key="equipment_percentage"
                ) * 100

            with equipment_col2:
                equipment_amount = st.number_input(
                    "قيمة المعدات (ريال)",
                    min_value=0.0,
                    value=float(equipment_value),
                    step=10.0,
                    key="equipment_amount"
                )

            # إضافة المعدات
            equipment_items = []

            st.markdown("إضافة المعدات")

            for i in range(3):  # السماح بإضافة 3 معدات كحد أقصى
                equipment_col1, equipment_col2, equipment_col3, equipment_col4 = st.columns([3, 1, 1, 1])

                with equipment_col1:
                    equipment_name = st.text_input(
                        "اسم المعدة",
                        key=f"equipment_name_{i}"
                    )

                with equipment_col2:
                    equipment_unit = st.text_input(
                        "الوحدة",
                        key=f"equipment_unit_{i}"
                    )

                with equipment_col3:
                    equipment_quantity = st.number_input(
                        "الكمية",
                        min_value=0.0,
                        step=0.1,
                        key=f"equipment_quantity_{i}"
                    )

                with equipment_col4:
                    equipment_price = st.number_input(
                        "السعر",
                        min_value=0.0,
                        step=10.0,
                        key=f"equipment_price_{i}"
                    )

                if equipment_name and equipment_unit and equipment_quantity > 0 and equipment_price > 0:
                    equipment_items.append({
                        "name": equipment_name,
                        "unit": equipment_unit,
                        "quantity": equipment_quantity,
                        "price": equipment_price,
                        "total": equipment_quantity * equipment_price
                    })

            # العمالة
            st.markdown("##### العمالة")
            labor_col1, labor_col2 = st.columns(2)

            with labor_col1:
                labor_percentage = st.slider(
                    "نسبة العمالة من سعر الوحدة",
                    min_value=0.0,
                    max_value=1.0,
                    value=price_components["labor"],
                    step=0.01,
                    format="%g%%",
                    key="labor_percentage"
                ) * 100

            with labor_col2:
                labor_amount = st.number_input(
                    "قيمة العمالة (ريال)",
                    min_value=0.0,
                    value=float(labor_value),
                    step=10.0,
                    key="labor_amount"
                )

            # إضافة العمالة
            labor_items = []

            st.markdown("إضافة العمالة")

            for i in range(3):  # السماح بإضافة 3 عمال كحد أقصى
                labor_col1, labor_col2, labor_col3, labor_col4 = st.columns([3, 1, 1, 1])

                with labor_col1:
                    labor_name = st.text_input(
                        "المسمى الوظيفي",
                        key=f"labor_name_{i}"
                    )

                with labor_col2:
                    labor_unit = st.text_input(
                        "الوحدة",
                        key=f"labor_unit_{i}"
                    )

                with labor_col3:
                    labor_quantity = st.number_input(
                        "الكمية",
                        min_value=0.0,
                        step=0.1,
                        key=f"labor_quantity_{i}"
                    )

                with labor_col4:
                    labor_price = st.number_input(
                        "السعر",
                        min_value=0.0,
                        step=10.0,
                        key=f"labor_price_{i}"
                    )

                if labor_name and labor_unit and labor_quantity > 0 and labor_price > 0:
                    labor_items.append({
                        "name": labor_name,
                        "unit": labor_unit,
                        "quantity": labor_quantity,
                        "price": labor_price,
                        "total": labor_quantity * labor_price
                    })

            # مقاولي الباطن
            st.markdown("##### مقاولي الباطن")
            subcontractors_col1, subcontractors_col2 = st.columns(2)

            with subcontractors_col1:
                subcontractors_percentage = st.slider(
                    "نسبة مقاولي الباطن من سعر الوحدة",
                    min_value=0.0,
                    max_value=1.0,
                    value=price_components["subcontractors"],
                    step=0.01,
                    format="%g%%",
                    key="subcontractors_percentage"
                ) * 100

            with subcontractors_col2:
                subcontractors_amount = st.number_input(
                    "قيمة مقاولي الباطن (ريال)",
                    min_value=0.0,
                    value=float(subcontractors_value),
                    step=10.0,
                    key="subcontractors_amount"
                )

            # إضافة مقاولي الباطن
            subcontractors_items = []

            st.markdown("إضافة مقاولي الباطن")

            for i in range(2):  # السماح بإضافة 2 مقاول باطن كحد أقصى
                subcontractor_col1, subcontractor_col2, subcontractor_col3 = st.columns([4, 1, 1])

                with subcontractor_col1:
                    subcontractor_name = st.text_input(
                        "اسم مقاول الباطن",
                        key=f"subcontractor_name_{i}"
                    )

                with subcontractor_col2:
                    subcontractor_work = st.text_input(
                        "نوع العمل",
                        key=f"subcontractor_work_{i}"
                    )

                with subcontractor_col3:
                    subcontractor_price = st.number_input(
                        "السعر",
                        min_value=0.0,
                        step=10.0,
                        key=f"subcontractor_price_{i}"
                    )

                if subcontractor_name and subcontractor_work and subcontractor_price > 0:
                    subcontractors_items.append({
                        "name": subcontractor_name,
                        "work": subcontractor_work,
                        "price": subcontractor_price
                    })

            # التكاليف غير المباشرة
            st.markdown("##### التكاليف غير المباشرة")

            # استخراج نسب التكاليف غير المباشرة
            indirect_costs = st.session_state.smart_price_analysis["indirect_costs"]

            indirect_col1, indirect_col2, indirect_col3 = st.columns(3)

            with indirect_col1:
                overhead_percentage = st.slider(
                    "نسبة المصاريف العمومية والإدارية",
                    min_value=0.0,
                    max_value=0.5,
                    value=indirect_costs["overhead"],
                    step=0.01,
                    format="%g%%",
                    key="overhead_percentage"
                ) * 100

            with indirect_col2:
                profit_percentage = st.slider(
                    "نسبة الربح",
                    min_value=0.0,
                    max_value=0.5,
                    value=indirect_costs["profit"],
                    step=0.01,
                    format="%g%%",
                    key="profit_percentage"
                ) * 100

            with indirect_col3:
                contingency_percentage = st.slider(
                    "نسبة الطوارئ",
                    min_value=0.0,
                    max_value=0.2,
                    value=indirect_costs["contingency"],
                    step=0.01,
                    format="%g%%",
                    key="contingency_percentage"
                ) * 100

            # زر حفظ التحليل
            submit_button = st.form_submit_button("حفظ التحليل")

            if submit_button:
                # التحقق من صحة البيانات
                total_percentage = (materials_percentage + equipment_percentage + labor_percentage + subcontractors_percentage) / 100

                if abs(total_percentage - 1.0) > 0.01:
                    st.error("مجموع نسب المكونات يجب أن يساوي 100%")
                else:
                    # حساب إجمالي المكونات
                    materials_total = sum([item["total"] for item in materials_items]) if materials_items else materials_amount
                    equipment_total = sum([item["total"] for item in equipment_items]) if equipment_items else equipment_amount
                    labor_total = sum([item["total"] for item in labor_items]) if labor_items else labor_amount
                    subcontractors_total = sum([item["price"] for item in subcontractors_items]) if subcontractors_items else subcontractors_amount

                    # حساب التكاليف المباشرة
                    direct_cost = materials_total + equipment_total + labor_total + subcontractors_total

                    # حساب التكاليف غير المباشرة
                    overhead_amount = direct_cost * (overhead_percentage / 100)
                    profit_amount = direct_cost * (profit_percentage / 100)
                    contingency_amount = direct_cost * (contingency_percentage / 100)

                    # حساب إجمالي التكاليف
                    total_cost = direct_cost + overhead_amount + profit_amount + contingency_amount

                    # إنشاء مكونات البند
                    components = {
                        "materials": {
                            "percentage": materials_percentage / 100,
                            "amount": materials_amount,
                            "items": materials_items
                        },
                        "equipment": {
                            "percentage": equipment_percentage / 100,
                            "amount": equipment_amount,
                            "items": equipment_items
                        },
                        "labor": {
                            "percentage": labor_percentage / 100,
                            "amount": labor_amount,
                            "items": labor_items
                        },
                        "subcontractors": {
                            "percentage": subcontractors_percentage / 100,
                            "amount": subcontractors_amount,
                            "items": subcontractors_items
                        },
                        "indirect_costs": {
                            "overhead": {
                                "percentage": overhead_percentage / 100,
                                "amount": overhead_amount
                            },
                            "profit": {
                                "percentage": profit_percentage / 100,
                                "amount": profit_amount
                            },
                            "contingency": {
                                "percentage": contingency_percentage / 100,
                                "amount": contingency_amount
                            }
                        },
                        "direct_cost": direct_cost,
                        "total_cost": total_cost,
                        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }

                    # تحديث البند في جدول الكميات
                    boq_items = st.session_state.boq_items
                    item_index = boq_items[boq_items["id"] == item["id"]].index[0]

                    boq_items.at[item_index, "analyzed"] = True
                    boq_items.at[item_index, "components"] = components

                    # تحديث حالة الجلسة
                    st.session_state.boq_items = boq_items

                    # إضافة التحليل إلى سجل التحليلات
                    analysis_history = st.session_state.smart_price_analysis["analysis_history"]
                    analysis_history.append({
                        "item_id": item["id"],
                        "item_description": item["description"],
                        "unit_price": item["unit_price"],
                        "components": components,
                        "analysis_date": components["analysis_date"]
                    })

                    st.session_state.smart_price_analysis["analysis_history"] = analysis_history

                    # إعادة تعيين البند الحالي
                    st.session_state.smart_price_analysis["current_item"] = None

                    # عرض رسالة نجاح
                    st.success(f"تم تحليل البند {item['id']} بنجاح!")

                    # إعادة توجيه إلى صفحة التحليل
                    st.rerun()

    def _display_item_components(self, item):
        """عرض مكونات البند"""

        # استخراج مكونات البند
        components = item["components"]

        if not components:
            st.warning("لم يتم تحليل هذا البند بعد")
            return

        # عرض ملخص التحليل
        st.markdown("#### ملخص التحليل")

        # عرض تاريخ التحليل
        st.markdown(f"**تاريخ التحليل:** {components['analysis_date']}")

        # عرض التكاليف المباشرة وغير المباشرة
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**التكاليفالمباشرة:** {components['direct_cost']:.2f} ريال")
            st.markdown(f"**التكاليف غير المباشرة:** {(components['total_cost'] - components['direct_cost']):.2f} ريال")

        with col2:
            st.markdown(f"**إجمالي التكاليف:** {components['total_cost']:.2f} ريال")
            st.markdown(f"**سعر الوحدة:** {item['unit_price']:.2f} ريال")

        # عرض نسب المكونات
        st.markdown("#### نسب المكونات")

        # إنشاء بيانات الرسم البياني
        components_data = {
            "المكون": ["المواد", "المعدات", "العمالة", "مقاولي الباطن"],
            "النسبة": [
                components["materials"]["percentage"] * 100,
                components["equipment"]["percentage"] * 100,
                components["labor"]["percentage"] * 100,
                components["subcontractors"]["percentage"] * 100
            ],
            "القيمة": [
                components["materials"]["amount"],
                components["equipment"]["amount"],
                components["labor"]["amount"],
                components["subcontractors"]["amount"]
            ]
        }

        # إنشاء رسم بياني دائري
        fig = px.pie(
            components_data,
            values="النسبة",
            names="المكون",
            title="توزيع مكونات سعر الوحدة",
            color="المكون",
            hover_data=["القيمة"]
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض تفاصيل المكونات
        st.markdown("#### تفاصيل المكونات")

        # إنشاء تبويبات لعرض تفاصيل المكونات
        component_tabs = st.tabs(["المواد", "المعدات", "العمالة", "مقاولي الباطن", "التكاليف غير المباشرة"])

        with component_tabs[0]:
            # عرض تفاصيل المواد
            st.markdown("##### المواد")
            st.markdown(f"**نسبة المواد:** {components['materials']['percentage'] * 100:.2f}%")
            st.markdown(f"**قيمة المواد:** {components['materials']['amount']:.2f} ريال")

            # عرض قائمة المواد
            if components["materials"]["items"]:
                materials_df = pd.DataFrame(components["materials"]["items"])
                materials_df.columns = ["اسم المادة", "الوحدة", "الكمية", "السعر", "الإجمالي"]

                st.dataframe(materials_df, use_container_width=True)
            else:
                st.info("لم يتم إضافة مواد محددة")

        with component_tabs[1]:
            # عرض تفاصيل المعدات
            st.markdown("##### المعدات")
            st.markdown(f"**نسبة المعدات:** {components['equipment']['percentage'] * 100:.2f}%")
            st.markdown(f"**قيمة المعدات:** {components['equipment']['amount']:.2f} ريال")

            # عرض قائمة المعدات
            if components["equipment"]["items"]:
                equipment_df = pd.DataFrame(components["equipment"]["items"])
                equipment_df.columns = ["اسم المعدة", "الوحدة", "الكمية", "السعر", "الإجمالي"]

                st.dataframe(equipment_df, use_container_width=True)
            else:
                st.info("لم يتم إضافة معدات محددة")

        with component_tabs[2]:
            # عرض تفاصيل العمالة
            st.markdown("##### العمالة")
            st.markdown(f"**نسبة العمالة:** {components['labor']['percentage'] * 100:.2f}%")
            st.markdown(f"**قيمة العمالة:** {components['labor']['amount']:.2f} ريال")

            # عرض قائمة العمالة
            if components["labor"]["items"]:
                labor_df = pd.DataFrame(components["labor"]["items"])
                labor_df.columns = ["المسمى الوظيفي", "الوحدة", "الكمية", "السعر", "الإجمالي"]

                st.dataframe(labor_df, use_container_width=True)
            else:
                st.info("لم يتم إضافة عمالة محددة")

        with component_tabs[3]:
            # عرض تفاصيل مقاولي الباطن
            st.markdown("##### مقاولي الباطن")
            st.markdown(f"**نسبة مقاولي الباطن:** {components['subcontractors']['percentage'] * 100:.2f}%")
            st.markdown(f"**قيمة مقاولي الباطن:** {components['subcontractors']['amount']:.2f} ريال")

            # عرض قائمة مقاولي الباطن
            if components["subcontractors"]["items"]:
                subcontractors_df = pd.DataFrame(components["subcontractors"]["items"])
                subcontractors_df.columns = ["اسم مقاول الباطن", "نوع العمل", "السعر"]

                st.dataframe(subcontractors_df, use_container_width=True)
            else:
                st.info("لم يتم إضافة مقاولي باطن محددين")

        with component_tabs[4]:
            # عرض تفاصيل التكاليف غير المباشرة
            st.markdown("##### التكاليف غير المباشرة")

            # إنشاء بيانات التكاليف غير المباشرة
            indirect_costs = components["indirect_costs"]

            indirect_data = {
                "البند": ["المصاريف العمومية والإدارية", "الربح", "الطوارئ"],
                "النسبة": [
                    indirect_costs["overhead"]["percentage"] * 100,
                    indirect_costs["profit"]["percentage"] * 100,
                    indirect_costs["contingency"]["percentage"] * 100
                ],
                "القيمة": [
                    indirect_costs["overhead"]["amount"],
                    indirect_costs["profit"]["amount"],
                    indirect_costs["contingency"]["amount"]
                ]
            }

            # إنشاء جدول للعرض
            indirect_df = pd.DataFrame(indirect_data)

            st.dataframe(indirect_df, use_container_width=True)

            # إنشاء رسم بياني للتكاليف غير المباشرة
            fig = px.bar(
                indirect_df,
                x="البند",
                y="القيمة",
                title="توزيع التكاليف غير المباشرة",
                color="البند",
                text_auto=True
            )

            st.plotly_chart(fig, use_container_width=True)

    def _render_analysis_settings_tab(self):
        """عرض تبويب إعدادات التحليل"""

        st.markdown("### إعدادات التحليل الذكي للأسعار")

        # استخراج إعدادات التحليل
        price_components = st.session_state.smart_price_analysis["price_components"]
        indirect_costs = st.session_state.smart_price_analysis["indirect_costs"]
        productivity_factors = st.session_state.smart_price_analysis["productivity_factors"]

        # إنشاء نموذج إعدادات التحليل
        with st.form("analysis_settings_form"):
            st.markdown("#### نسب مكونات السعر الافتراضية")

            # نسب مكونات السعر
            components_col1, components_col2 = st.columns(2)

            with components_col1:
                materials_percentage = st.slider(
                    "نسبة المواد من سعر الوحدة",
                    min_value=0.0,
                    max_value=1.0,
                    value=price_components["materials"],
                    step=0.01,
                    format="%g%%",
                    key="settings_materials_percentage"
                ) * 100

                equipment_percentage = st.slider(
                    "نسبة المعدات من سعر الوحدة",
                    min_value=0.0,
                    max_value=1.0,
                    value=price_components["equipment"],
                    step=0.01,
                    format="%g%%",
                    key="settings_equipment_percentage"
                ) * 100

            with components_col2:
                labor_percentage = st.slider(
                    "نسبة العمالة من سعر الوحدة",
                    min_value=0.0,
                    max_value=1.0,
                    value=price_components["labor"],
                    step=0.01,
                    format="%g%%",
                    key="settings_labor_percentage"
                ) * 100

                subcontractors_percentage = st.slider(
                    "نسبة مقاولي الباطن من سعر الوحدة",
                    min_value=0.0,
                    max_value=1.0,
                    value=price_components["subcontractors"],
                    step=0.01,
                    format="%g%%",
                    key="settings_subcontractors_percentage"
                ) * 100

            # التكاليف غير المباشرة
            st.markdown("#### نسب التكاليف غير المباشرة الافتراضية")

            indirect_col1, indirect_col2, indirect_col3 = st.columns(3)

            with indirect_col1:
                overhead_percentage = st.slider(
                    "نسبة المصاريف العمومية والإدارية",
                    min_value=0.0,
                    max_value=0.5,
                    value=indirect_costs["overhead"],
                    step=0.01,
                    format="%g%%",
                    key="settings_overhead_percentage"
                ) * 100

            with indirect_col2:
                profit_percentage = st.slider(
                    "نسبة الربح",
                    min_value=0.0,
                    max_value=0.5,
                    value=indirect_costs["profit"],
                    step=0.01,
                    format="%g%%",
                    key="settings_profit_percentage"
                ) * 100

            with indirect_col3:
                contingency_percentage = st.slider(
                    "نسبة الطوارئ",
                    min_value=0.0,
                    max_value=0.2,
                    value=indirect_costs["contingency"],
                    step=0.01,
                    format="%g%%",
                    key="settings_contingency_percentage"
                ) * 100

            # عوامل الإنتاجية
            st.markdown("#### عوامل الإنتاجية")

            productivity_col1, productivity_col2 = st.columns(2)

            with productivity_col1:
                weather_factor = st.slider(
                    "عامل الطقس",
                    min_value=0.5,
                    max_value=1.5,
                    value=productivity_factors["weather"],
                    step=0.1,
                    key="settings_weather_factor"
                )

                location_factor = st.slider(
                    "عامل الموقع",
                    min_value=0.5,
                    max_value=1.5,
                    value=productivity_factors["location"],
                    step=0.1,
                    key="settings_location_factor"
                )

                complexity_factor = st.slider(
                    "عامل التعقيد",
                    min_value=0.5,
                    max_value=1.5,
                    value=productivity_factors["complexity"],
                    step=0.1,
                    key="settings_complexity_factor"
                )

            with productivity_col2:
                schedule_factor = st.slider(
                    "عامل الجدول الزمني",
                    min_value=0.5,
                    max_value=1.5,
                    value=productivity_factors["schedule"],
                    step=0.1,
                    key="settings_schedule_factor"
                )

                resources_factor = st.slider(
                    "عامل الموارد",
                    min_value=0.5,
                    max_value=1.5,
                    value=productivity_factors["resources"],
                    step=0.1,
                    key="settings_resources_factor"
                )

            # زر حفظ الإعدادات
            submit_button = st.form_submit_button("حفظ الإعدادات")

            if submit_button:
                # التحقق من صحة البيانات
                total_percentage = (materials_percentage + equipment_percentage + labor_percentage + subcontractors_percentage) / 100

                if abs(total_percentage - 1.0) > 0.01:
                    st.error("مجموع نسب المكونات يجب أن يساوي 100%")
                else:
                    # تحديث نسب مكونات السعر
                    price_components["materials"] = materials_percentage / 100
                    price_components["equipment"] = equipment_percentage / 100
                    price_components["labor"] = labor_percentage / 100
                    price_components["subcontractors"] = subcontractors_percentage / 100

                    # تحديث نسب التكاليف غير المباشرة
                    indirect_costs["overhead"] = overhead_percentage / 100
                    indirect_costs["profit"] = profit_percentage / 100
                    indirect_costs["contingency"] = contingency_percentage / 100

                    # تحديث عوامل الإنتاجية
                    productivity_factors["weather"] = weather_factor
                    productivity_factors["location"] = location_factor
                    productivity_factors["complexity"] = complexity_factor
                    productivity_factors["schedule"] = schedule_factor
                    productivity_factors["resources"] = resources_factor

                    # تحديث حالة الجلسة
                    st.session_state.smart_price_analysis["price_components"] = price_components
                    st.session_state.smart_price_analysis["indirect_costs"] = indirect_costs
                    st.session_state.smart_price_analysis["productivity_factors"] = productivity_factors

                    # عرض رسالة نجاح
                    st.success("تم حفظ إعدادات التحليل بنجاح!")

        # عرض الإعدادات الحالية
        st.markdown("### الإعدادات الحالية")

        # عرض نسب مكونات السعر
        st.markdown("#### نسب مكونات السعر")

        # إنشاء بيانات الرسم البياني
        components_data = {
            "المكون": ["المواد", "المعدات", "العمالة", "مقاولي الباطن"],
            "النسبة": [
                price_components["materials"] * 100,
                price_components["equipment"] * 100,
                price_components["labor"] * 100,
                price_components["subcontractors"] * 100
            ]
        }

        # إنشاء رسم بياني دائري
        fig = px.pie(
            components_data,
            values="النسبة",
            names="المكون",
            title="توزيع مكونات سعر الوحدة",
            color="المكون"
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض نسب التكاليف غير المباشرة
        st.markdown("#### نسب التكاليف غير المباشرة")

        # إنشاء بيانات الرسم البياني
        indirect_data = {
            "البند": ["المصاريف العمومية والإدارية", "الربح", "الطوارئ"],
            "النسبة": [
                indirect_costs["overhead"] * 100,
                indirect_costs["profit"] * 100,
                indirect_costs["contingency"] * 100
            ]
        }

        # إنشاء رسم بياني شريطي
        fig = px.bar(
            indirect_data,
            x="البند",
            y="النسبة",
            title="نسب التكاليف غير المباشرة",
            color="البند",
            text_auto=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض عوامل الإنتاجية
        st.markdown("#### عوامل الإنتاجية")

        # إنشاء بيانات الرسم البياني
        productivity_data = {
            "العامل": ["الطقس", "الموقع", "التعقيد", "الجدول الزمني", "الموارد"],
            "القيمة": [
                productivity_factors["weather"],
                productivity_factors["location"],
                productivity_factors["complexity"],
                productivity_factors["schedule"],
                productivity_factors["resources"]
            ]
        }

        # إنشاء رسم بياني شريطي
        fig = px.bar(
            productivity_data,
            x="العامل",
            y="القيمة",
            title="عوامل الإنتاجية",
            color="العامل",
            text_auto=True
        )

        # إضافة خط أفقي عند القيمة 1.0
        fig.add_shape(
            type="line",
            x0=-0.5,
            y0=1.0,
            x1=4.5,
            y1=1.0,
            line=dict(
                color="red",
                width=2,
                dash="dash"
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    def _render_analysis_reports_tab(self):
        """عرض تبويب تقارير التحليل"""

        st.markdown("### تقارير التحليل الذكي للأسعار")

        # استخراج البيانات
        boq_items = st.session_state.boq_items
        analysis_history = st.session_state.smart_price_analysis["analysis_history"]

        # عرض ملخص التحليل
        st.markdown("#### ملخص التحليل")

        # حساب عدد البنود المحللة وغير المحللة
        analyzed_count = len(boq_items[boq_items["analyzed"] == True])
        not_analyzed_count = len(boq_items[boq_items["analyzed"] == False])

        # عرض نسبة التحليل
        analysis_percentage = analyzed_count / len(boq_items) * 100 if len(boq_items) > 0 else 0

        st.markdown(f"**عدد البنود المحللة:** {analyzed_count} من أصل {len(boq_items)} ({analysis_percentage:.2f}%)")

        # إنشاء مؤشر التقدم
        st.progress(analysis_percentage / 100)

        # عرض توزيع البنود المحللة حسب الفئة
        st.markdown("#### توزيع البنود المحللة حسب الفئة")

        # حساب عدد البنود المحللة لكل فئة
        category_analysis = boq_items.groupby(["category", "analyzed"]).size().unstack(fill_value=0).reset_index()

        if True in category_analysis.columns:
            category_analysis.columns = ["الفئة", "غير محلل", "محلل"]

            # إنشاء رسم بياني شريطي
            fig = px.bar(
                category_analysis,
                x="الفئة",
                y=["محلل", "غير محلل"],
                title="توزيع البنود المحللة حسب الفئة",
                barmode="stack",
                color_discrete_map={"محلل": "green", "غير محلل": "red"}
            )

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا يوجد بنود محللة بعد")

        # عرض توزيع مكونات الأسعار
        st.markdown("#### توزيع مكونات الأسعار")

        # التحقق من وجود بنود محللة
        if analyzed_count > 0:
            # استخراج البنود المحللة
            analyzed_items = boq_items[boq_items["analyzed"] == True]

            # إنشاء قائمة لتخزين بيانات المكونات
            components_data = []

            # استخراج بيانات المكونات
            for _, item in analyzed_items.iterrows():
                components = item["components"]

                components_data.append({
                    "id": item["id"],
                    "description": item["description"],
                    "unit_price": item["unit_price"],
                    "materials_percentage": components["materials"]["percentage"],
                    "equipment_percentage": components["equipment"]["percentage"],
                    "labor_percentage": components["labor"]["percentage"],
                    "subcontractors_percentage": components["subcontractors"]["percentage"],
                    "materials_amount": components["materials"]["amount"],
                    "equipment_amount": components["equipment"]["amount"],
                    "labor_amount": components["labor"]["amount"],
                    "subcontractors_amount": components["subcontractors"]["amount"]
                })

            # إنشاء DataFrame
            components_df = pd.DataFrame(components_data)

            # حساب متوسط النسب
            avg_materials_percentage = components_df["materials_percentage"].mean() * 100
            avg_equipment_percentage = components_df["equipment_percentage"].mean() * 100
            avg_labor_percentage = components_df["labor_percentage"].mean() * 100
            avg_subcontractors_percentage = components_df["subcontractors_percentage"].mean() * 100

            # عرض متوسط النسب
            st.markdown("##### متوسط نسب المكونات")

            avg_components_data = {
                "المكون": ["المواد", "المعدات", "العمالة", "مقاولي الباطن"],
                "النسبة": [
                    avg_materials_percentage,
                    avg_equipment_percentage,
                    avg_labor_percentage,
                    avg_subcontractors_percentage
                ]
            }

            # إنشاء رسم بياني دائري
            fig = px.pie(
                avg_components_data,
                values="النسبة",
                names="المكون",
                title="متوسط نسب مكونات الأسعار",
                color="المكون"
            )

            st.plotly_chart(fig, use_container_width=True)

            # عرض توزيع النسب حسب البند
            st.markdown("##### توزيع نسب المكونات حسب البند")

            # إنشاء بيانات للرسم البياني
            item_components_data = []

            for _, row in components_df.iterrows():
                item_components_data.extend([
                    {"البند": row["id"], "المكون": "المواد", "النسبة": row["materials_percentage"] * 100},
                    {"البند": row["id"], "المكون": "المعدات", "النسبة": row["equipment_percentage"] * 100},
                    {"البند": row["id"], "المكون": "العمالة", "النسبة": row["labor_percentage"] * 100},
                    {"البند": row["id"], "المكون": "مقاولي الباطن", "النسبة": row["subcontractors_percentage"] * 100}
                ])

            # إنشاء DataFrame
            item_components_df = pd.DataFrame(item_components_data)

            # إنشاء رسم بياني شريطي
            fig = px.bar(
                item_components_df,
                x="البند",
                y="النسبة",
                color="المكون",
                title="توزيع نسب المكونات حسب البند",
                barmode="stack"
            )

            st.plotly_chart(fig, use_container_width=True)

            # عرض مقارنة أسعار الوحدة
            st.markdown("##### مقارنة أسعار الوحدة")

            # إنشاء بيانات للرسم البياني
            unit_price_data = []

            for _, row in components_df.iterrows():
                unit_price_data.extend([
                    {"البند": row["id"], "المكون": "المواد", "القيمة": row["materials_amount"]},
                    {"البند": row["id"], "المكون": "المعدات", "القيمة": row["equipment_amount"]},
                    {"البند": row["id"], "المكون": "العمالة", "القيمة": row["labor_amount"]},
                    {"البند": row["id"], "المكون": "مقاولي الباطن", "القيمة": row["subcontractors_amount"]}
                ])

            # إنشاء DataFrame
            unit_price_df = pd.DataFrame(unit_price_data)

            # إنشاء رسم بياني شريطي
            fig = px.bar(
                unit_price_df,
                x="البند",
                y="القيمة",
                color="المكون",
                title="مقارنة مكونات أسعار الوحدة",
                barmode="stack"
            )

            # إضافة خط لسعر الوحدة
            for i, row in components_df.iterrows():
                fig.add_shape(
                    type="line",
                    x0=i - 0.4,
                    y0=row["unit_price"],
                    x1=i + 0.4,
                    y1=row["unit_price"],
                    line=dict(
                        color="red",
                        width=2,
                        dash="dash"
                    )
                )

            st.plotly_chart(fig, use_container_width=True)
            self.render_cost_breakdown() #Added this line
        else:
            st.info("لا يوجد بنود محللة بعد")

        # عرض سجل التحليلات
        st.markdown("#### سجل التحليلات")

        if analysis_history:
            # عرض عدد التحليلات
            st.markdown(f"**عدد التحليلات:** {len(analysis_history)}")

            # عرض آخر 5 تحليلات
            st.markdown("##### آخر 5 تحليلات")

            for i, analysis in enumerate(analysis_history[-5:]):
                st.markdown(f"**{i+1}. البند:** {analysis['item_id']} - {analysis['item_description']}")
                st.markdown(f"**تاريخ التحليل:** {analysis['analysis_date']}")
                st.markdown(f"**سعر الوحدة:** {analysis['unit_price']} ريال")
                st.markdown("---")
        else:
            st.info("لا يوجد سجل تحليلات بعد")

    def _render_local_content_tab(self):
        """عرض تبويب المحتوى المحلي"""

        st.markdown("### تحليل المحتوى المحلي")

        # استخراج بيانات المحتوى المحلي
        local_content = st.session_state.smart_price_analysis["local_content"]

        # إنشاء نموذج إعدادات المحتوى المحلي
        with st.form("local_content_form"):
            st.markdown("#### إعدادات المحتوى المحلي")

            # النسبة المستهدفة للمحتوى المحلي
            target_percentage = st.slider(
                "النسبة المستهدفة للمحتوى المحلي",
                min_value=0.0,
                max_value=1.0,
                value=local_content["target"],
                step=0.01,
                format="%g%%",
                key="local_content_target"
            ) * 100

            # نسب المحتوى المحلي لكل مكون
            st.markdown("#### نسب المحتوى المحلي لكل مكون")

            local_col1, local_col2 = st.columns(2)

            with local_col1:
                materials_local = st.slider(
                    "نسبة المواد المحلية",
                    min_value=0.0,
                    max_value=1.0,
                    value=local_content["materials_local"],
                    step=0.01,
                    format="%g%%",
                    key="materials_local"
                ) * 100

                equipment_local = st.slider(
                    "نسبة المعدات المحلية",
                    min_value=0.0,
                    max_value=1.0,
                    value=local_content["equipment_local"],
                    step=0.01,
                    format="%g%%",
                    key="equipment_local"
                ) * 100

            with local_col2:
                labor_local = st.slider(
                    "نسبة العمالة المحلية",
                    min_value=0.0,
                    max_value=1.0,
                    value=local_content["labor_local"],
                    step=0.01,
                    format="%g%%",
                    key="labor_local"
                ) * 100

                subcontractors_local = st.slider(
                    "نسبة مقاولي الباطن المحليين",
                    min_value=0.0,
                    max_value=1.0,
                    value=local_content["subcontractors_local"],
                    step=0.01,
                    format="%g%%",
                    key="subcontractors_local"
                ) * 100

            # زر حفظ الإعدادات
            submit_button = st.form_submit_button("حفظ إعدادات المحتوى المحلي")

            if submit_button:
                # تحديث إعدادات المحتوى المحلي
                local_content["target"] = target_percentage / 100
                local_content["materials_local"] = materials_local / 100
                local_content["equipment_local"] = equipment_local / 100
                local_content["labor_local"] = labor_local / 100
                local_content["subcontractors_local"] = subcontractors_local / 100

                # تحديث حالة الجلسة
                st.session_state.smart_price_analysis["local_content"] = local_content

                # عرض رسالة نجاح
                st.success("تم حفظ إعدادات المحتوى المحلي بنجاح!")

        # حساب نسبة المحتوى المحلي الفعلية
        st.markdown("#### حساب نسبة المحتوى المحلي الفعلية")

        # استخراج نسب مكونات السعر
        price_components = st.session_state.smart_price_analysis["price_components"]

        # حساب نسبة المحتوى المحلي الفعلية
        actual_local_content = (
            price_components["materials"] * local_content["materials_local"] +
            price_components["equipment"] * local_content["equipment_local"] +
            price_components["labor"] * local_content["labor_local"] +
            price_components["subcontractors"] * local_content["subcontractors_local"]
        )

        # عرض نسبة المحتوى المحلي الفعلية
        st.markdown(f"**نسبة المحتوى المحلي الفعلية:** {actual_local_content * 100:.2f}%")
        st.markdown(f"**النسبة المستهدفة للمحتوى المحلي:** {local_content['target'] * 100:.2f}%")

        # عرض مؤشر التقدم
        progress_percentage = min(actual_local_content / local_content["target"], 1.0) if local_content["target"] > 0 else 0

        st.progress(progress_percentage)

        # عرض حالة المحتوى المحلي
        if actual_local_content >= local_content["target"]:
            st.success("تم تحقيق النسبة المستهدفة للمحتوى المحلي")
        else:
            st.warning("لم يتم تحقيق النسبة المستهدفة للمحتوى المحلي")

        # عرض مساهمة كل مكون في المحتوى المحلي
        st.markdown("#### مساهمة كل مكون في المحتوى المحلي")

        # حساب مساهمة كل مكون
        materials_contribution = price_components["materials"] * local_content["materials_local"]
        equipment_contribution = price_components["equipment"] * local_content["equipment_local"]
        labor_contribution = price_components["labor"] * local_content["labor_local"]
        subcontractors_contribution = price_components["subcontractors"] * local_content["subcontractors_local"]

        # إنشاء بيانات الرسم البياني
        contribution_data = {
            "المكون": ["المواد", "المعدات", "العمالة", "مقاولي الباطن"],
            "المساهمة": [
                materials_contribution * 100,
                equipment_contribution * 100,
                labor_contribution * 100,
                subcontractors_contribution * 100
            ]
        }

        # إنشاء رسم بياني شريطي
        fig = px.bar(
            contribution_data,
            x="المكون",
            y="المساهمة",
            title="مساهمة كل مكون في المحتوى المحلي",
            color="المكون",
            text_auto=True
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض توصيات لتحسين نسبة المحتوى المحلي
        st.markdown("#### توصيات لتحسين نسبة المحتوى المحلي")

        if actual_local_content < local_content["target"]:
            # حساب الفجوة
            gap = local_content["target"] - actual_local_content

            st.markdown(f"**الفجوة الحالية:** {gap * 100:.2f}%")

            # تحديد المكونات التي يمكن تحسينها
            components_to_improve = []

            if local_content["materials_local"] < 1.0:
                components_to_improve.append({
                    "name": "المواد",
                    "current": local_content["materials_local"],
                    "weight": price_components["materials"],
                    "potential": price_components["materials"] * (1.0 - local_content["materials_local"])
                })

            if local_content["equipment_local"] < 1.0:
                components_to_improve.append({
                    "name": "المعدات",
                    "current": local_content["equipment_local"],
                    "weight": price_components["equipment"],
                    "potential": price_components["equipment"] * (1.0 - local_content["equipment_local"])
                })

            if local_content["labor_local"] < 1.0:
                components_to_improve.append({
                    "name": "العمالة",
                    "current": local_content["labor_local"],
                    "weight": price_components["labor"],
                    "potential": price_components["labor"] * (1.0 - local_content["labor_local"])
                })

            if local_content["subcontractors_local"] < 1.0:
                components_to_improve.append({
                    "name": "مقاولي الباطن",
                    "current": local_content["subcontractors_local"],
                    "weight": price_components["subcontractors"],
                    "potential": price_components["subcontractors"] * (1.0 - local_content["subcontractors_local"])
                })

            # ترتيب المكونات حسب إمكانية التحسين
            components_to_improve.sort(key=lambda x: x["potential"], reverse=True)

            # عرض التوصيات
            for component in components_to_improve:
                st.markdown(f"**{component['name']}:** زيادة نسبة {component['name']} المحلية من {component['current'] * 100:.2f}% إلى {min(component['current'] + gap / component['weight'], 1.0) * 100:.2f}%")
        else:
            st.success("تم تحقيق النسبة المستهدفة للمحتوى المحلي")

    def calculate_item_price(self, item_data):
        """حساب سعر البند بناءً على مكوناته"""

        # استخراج مكونات البند
        materials = item_data.get("materials", [])
        equipment = item_data.get("equipment", [])
        labor = item_data.get("labor", [])
        subcontractors = item_data.get("subcontractors", [])

        # حساب تكلفة المواد
        materials_cost = sum([material["quantity"] * material["price"] for material in materials])

        # حساب تكلفة المعدات
        equipment_cost = sum([equipment_item["quantity"] * equipment_item["price"] for equipment_item in equipment])

        # حساب تكلفة العمالة
        labor_cost = sum([labor_item["quantity"] * labor_item["price"] for labor_item in labor])

        # حساب تكلفة مقاولي الباطن
        subcontractors_cost = sum([subcontractor["price"] for subcontractor in subcontractors])

        # حساب التكاليف المباشرة
        direct_cost = materials_cost + equipment_cost + labor_cost + subcontractors_cost

        # استخراج نسب التكاليف غير المباشرة
        indirect_costs = st.session_state.smart_price_analysis["indirect_costs"]

        # حساب التكاليف غير المباشرة
        overhead_amount = direct_cost * indirect_costs["overhead"]
        profit_amount = direct_cost * indirect_costs["profit"]
        contingency_amount = direct_cost * indirect_costs["contingency"]

        # حساب إجمالي التكاليف
        total_cost = direct_cost + overhead_amount + profit_amount + contingency_amount

        return total_cost

    def calculate_local_content(self, item_data):
        """حساب نسبة المحتوى المحلي للبند"""

        # استخراج مكونات البند
        materials = item_data.get("materials", [])
        equipment = item_data.get("equipment", [])
        labor = item_data.get("labor", [])
        subcontractors = item_data.get("subcontractors", [])

        # استخراج نسب المحتوى المحلي
        local_content = st.session_state.smart_price_analysis["local_content"]

        # حساب تكلفة المواد
        materials_cost = sum([material["quantity"] * material["price"] for material in materials])

        # حساب تكلفة المعدات
        equipment_cost = sum([equipment_item["quantity"] * equipment_item["price"] for equipment_item in equipment])

        # حساب تكلفة العمالة
        labor_cost = sum([labor_item["quantity"] * labor_item["price"] for labor_item in labor])

        # حساب تكلفة مقاولي الباطن
        subcontractors_cost = sum([subcontractor["price"] for subcontractor in subcontractors])

        # حساب التكاليف المباشرة
        direct_cost = materials_cost + equipment_cost + labor_cost + subcontractors_cost

        # حساب المحتوى المحلي
        local_materials = materials_cost * local_content["materials_local"]
        local_equipment = equipment_cost * local_content["equipment_local"]
        local_labor = labor_cost * local_content["labor_local"]
        local_subcontractors = subcontractors_cost * local_content["subcontractors_local"]

        # حساب إجمالي المحتوى المحلي
        total_local_content = local_materials + local_equipment + local_labor + local_subcontractors

        # حساب نسبة المحتوى المحلي
        local_content_percentage = total_local_content / direct_cost if direct_cost > 0 else 0

        return local_content_percentage

    def analyze_costs(self, items):
        """تحليل التكاليف لبنود المشروع"""
        total_cost = sum(item['total_price'] for item in items)
        categories = {}

        for item in items:
            if item['category'] not in categories:
                categories[item['category']] = 0
            categories[item['category']] += item['total_price']

        return {
            'total_cost': total_cost,
            'categories': categories
        }

    def render_cost_breakdown(self): #Added this function
        """عرض تحليل التكاليف"""
        if 'bill_of_quantities' not in st.session_state:
            st.session_state.bill_of_quantities = []

        if len(st.session_state.bill_of_quantities) > 0:
            analysis = self.analyze_costs(st.session_state.bill_of_quantities)

            st.metric("إجمالي التكاليف", f"{analysis['total_cost']:,.2f} ريال")

            # عرض التكاليف حسب الفئة
            st.subheader("التكاليف حسب الفئة")
            categories_df = pd.DataFrame([
                {"الفئة": cat, "التكلفة": cost}
                for cat, cost in analysis['categories'].items()
            ])

            if not categories_df.empty:
                fig = px.pie(
                    categories_df,
                    values="التكلفة",
                    names="الفئة",
                    title="توزيع التكاليف حسب الفئة"
                )
                st.plotly_chart(fig)
        else:
            st.warning("لا توجد بنود في جدول الكميات")