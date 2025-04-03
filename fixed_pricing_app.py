"""
وحدة التسعير - التطبيق الرئيسي
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

class PricingApp:
    """وحدة التسعير"""
    
    def __init__(self):
        """تهيئة وحدة التسعير"""
        
        # تهيئة حالة الجلسة
        if 'bill_of_quantities' not in st.session_state:
            st.session_state.bill_of_quantities = [
                {
                    'id': 1,
                    'code': 'A-001',
                    'description': 'أعمال الحفر والردم',
                    'unit': 'م3',
                    'quantity': 1500,
                    'unit_price': 45,
                    'total_price': 67500,
                    'category': 'أعمال ترابية'
                },
                {
                    'id': 2,
                    'code': 'A-002',
                    'description': 'توريد وصب خرسانة عادية',
                    'unit': 'م3',
                    'quantity': 250,
                    'unit_price': 350,
                    'total_price': 87500,
                    'category': 'أعمال خرسانية'
                },
                {
                    'id': 3,
                    'code': 'A-003',
                    'description': 'توريد وصب خرسانة مسلحة للأساسات',
                    'unit': 'م3',
                    'quantity': 180,
                    'unit_price': 450,
                    'total_price': 81000,
                    'category': 'أعمال خرسانية'
                },
                {
                    'id': 4,
                    'code': 'A-004',
                    'description': 'توريد وصب خرسانة مسلحة للأعمدة',
                    'unit': 'م3',
                    'quantity': 120,
                    'unit_price': 500,
                    'total_price': 60000,
                    'category': 'أعمال خرسانية'
                },
                {
                    'id': 5,
                    'code': 'A-005',
                    'description': 'توريد وتركيب حديد تسليح',
                    'unit': 'طن',
                    'quantity': 45,
                    'unit_price': 3000,
                    'total_price': 135000,
                    'category': 'أعمال حديد'
                },
                {
                    'id': 6,
                    'code': 'A-006',
                    'description': 'توريد وبناء طابوق',
                    'unit': 'م2',
                    'quantity': 1200,
                    'unit_price': 45,
                    'total_price': 54000,
                    'category': 'أعمال بناء'
                },
                {
                    'id': 7,
                    'code': 'A-007',
                    'description': 'أعمال اللياسة والتشطيبات',
                    'unit': 'م2',
                    'quantity': 2400,
                    'unit_price': 35,
                    'total_price': 84000,
                    'category': 'أعمال تشطيبات'
                },
                {
                    'id': 8,
                    'code': 'A-008',
                    'description': 'أعمال الدهانات',
                    'unit': 'م2',
                    'quantity': 2400,
                    'unit_price': 25,
                    'total_price': 60000,
                    'category': 'أعمال تشطيبات'
                },
                {
                    'id': 9,
                    'code': 'A-009',
                    'description': 'توريد وتركيب أبواب خشبية',
                    'unit': 'عدد',
                    'quantity': 24,
                    'unit_price': 750,
                    'total_price': 18000,
                    'category': 'أعمال نجارة'
                },
                {
                    'id': 10,
                    'code': 'A-010',
                    'description': 'توريد وتركيب نوافذ ألمنيوم',
                    'unit': 'م2',
                    'quantity': 120,
                    'unit_price': 350,
                    'total_price': 42000,
                    'category': 'أعمال ألمنيوم'
                }
            ]
        
        if 'cost_analysis' not in st.session_state:
            st.session_state.cost_analysis = [
                {
                    'id': 1,
                    'category': 'تكاليف مباشرة',
                    'subcategory': 'مواد',
                    'description': 'خرسانة',
                    'amount': 120000,
                    'percentage': 17.9
                },
                {
                    'id': 2,
                    'category': 'تكاليف مباشرة',
                    'subcategory': 'مواد',
                    'description': 'حديد تسليح',
                    'amount': 135000,
                    'percentage': 20.1
                },
                {
                    'id': 3,
                    'category': 'تكاليف مباشرة',
                    'subcategory': 'مواد',
                    'description': 'طابوق',
                    'amount': 54000,
                    'percentage': 8.1
                },
                {
                    'id': 4,
                    'category': 'تكاليف مباشرة',
                    'subcategory': 'عمالة',
                    'description': 'عمالة تنفيذ',
                    'amount': 120000,
                    'percentage': 17.9
                },
                {
                    'id': 5,
                    'category': 'تكاليف مباشرة',
                    'subcategory': 'معدات',
                    'description': 'معدات إنشائية',
                    'amount': 85000,
                    'percentage': 12.7
                },
                {
                    'id': 6,
                    'category': 'تكاليف غير مباشرة',
                    'subcategory': 'إدارة',
                    'description': 'إدارة المشروع',
                    'amount': 45000,
                    'percentage': 6.7
                },
                {
                    'id': 7,
                    'category': 'تكاليف غير مباشرة',
                    'subcategory': 'إدارة',
                    'description': 'إشراف هندسي',
                    'amount': 35000,
                    'percentage': 5.2
                },
                {
                    'id': 8,
                    'category': 'تكاليف غير مباشرة',
                    'subcategory': 'عامة',
                    'description': 'تأمينات وضمانات',
                    'amount': 25000,
                    'percentage': 3.7
                },
                {
                    'id': 9,
                    'category': 'تكاليف غير مباشرة',
                    'subcategory': 'عامة',
                    'description': 'مصاريف إدارية',
                    'amount': 30000,
                    'percentage': 4.5
                },
                {
                    'id': 10,
                    'category': 'أرباح',
                    'subcategory': 'أرباح',
                    'description': 'هامش الربح',
                    'amount': 55000,
                    'percentage': 8.2
                }
            ]
        
        if 'price_scenarios' not in st.session_state:
            st.session_state.price_scenarios = [
                {
                    'id': 1,
                    'name': 'السيناريو الأساسي',
                    'description': 'التسعير الأساسي مع هامش ربح 8%',
                    'total_cost': 615000,
                    'profit_margin': 8.2,
                    'total_price': 670000,
                    'is_active': True
                },
                {
                    'id': 2,
                    'name': 'سيناريو تنافسي',
                    'description': 'تخفيض هامش الربح للمنافسة',
                    'total_cost': 615000,
                    'profit_margin': 5.0,
                    'total_price': 650000,
                    'is_active': False
                },
                {
                    'id': 3,
                    'name': 'سيناريو مرتفع',
                    'description': 'زيادة هامش الربح للمشاريع ذات المخاطر العالية',
                    'total_cost': 615000,
                    'profit_margin': 12.0,
                    'total_price': 700000,
                    'is_active': False
                }
            ]
    
    def run(self):
        """تشغيل وحدة التسعير"""
        # استدعاء دالة العرض
        self.render()
    
    def render(self):
        """عرض واجهة وحدة التسعير"""
        
        st.markdown("<h1 class='module-title'>وحدة التسعير</h1>", unsafe_allow_html=True)
        
        tabs = st.tabs([
            "لوحة التحكم", 
            "جدول الكميات",
            "تحليل التكاليف",
            "سيناريوهات التسعير",
            "المقارنة التنافسية",
            "التقارير"
        ])
        
        with tabs[0]:
            self._render_dashboard_tab()
        
        with tabs[1]:
            self._render_bill_of_quantities_tab()
        
        with tabs[2]:
            self._render_cost_analysis_tab()
        
        with tabs[3]:
            self._render_pricing_scenarios_tab()
        
        with tabs[4]:
            self._render_competitive_analysis_tab()
        
        with tabs[5]:
            self._render_reports_tab()
    
    def _render_dashboard_tab(self):
        """عرض تبويب لوحة التحكم"""
        
        st.markdown("### لوحة تحكم التسعير")
        
        # عرض ملخص التسعير
        col1, col2, col3, col4 = st.columns(4)
        
        # حساب إجمالي التكاليف
        total_direct_cost = sum(item['amount'] for item in st.session_state.cost_analysis if item['category'] == 'تكاليف مباشرة')
        total_indirect_cost = sum(item['amount'] for item in st.session_state.cost_analysis if item['category'] == 'تكاليف غير مباشرة')
        total_profit = sum(item['amount'] for item in st.session_state.cost_analysis if item['category'] == 'أرباح')
        total_cost = total_direct_cost + total_indirect_cost
        total_price = total_cost + total_profit
        
        with col1:
            st.metric("إجمالي التكاليف المباشرة", f"{total_direct_cost:,.0f} ريال")
        
        with col2:
            st.metric("إجمالي التكاليف غير المباشرة", f"{total_indirect_cost:,.0f} ريال")
        
        with col3:
            st.metric("إجمالي التكاليف", f"{total_cost:,.0f} ريال")
        
        with col4:
            st.metric("السعر الإجمالي", f"{total_price:,.0f} ريال")
        
        # عرض توزيع التكاليف
        st.markdown("### توزيع التكاليف")
        
        # تجميع البيانات حسب الفئة
        cost_categories = {}
        
        for item in st.session_state.cost_analysis:
            category = item['category']
            if category in cost_categories:
                cost_categories[category] += item['amount']
            else:
                cost_categories[category] = item['amount']
        
        # إنشاء DataFrame للرسم البياني
        cost_df = pd.DataFrame({
            'الفئة': list(cost_categories.keys()),
            'المبلغ': list(cost_categories.values())
        })
        
        # إنشاء رسم بياني دائري
        fig = px.pie(
            cost_df,
            values='المبلغ',
            names='الفئة',
            title='توزيع التكاليف حسب الفئة',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض توزيع التكاليف المباشرة
        st.markdown("### توزيع التكاليف المباشرة")
        
        # تجميع البيانات حسب الفئة الفرعية للتكاليف المباشرة
        direct_cost_subcategories = {}
        
        for item in st.session_state.cost_analysis:
            if item['category'] == 'تكاليف مباشرة':
                subcategory = item['subcategory']
                if subcategory in direct_cost_subcategories:
                    direct_cost_subcategories[subcategory] += item['amount']
                else:
                    direct_cost_subcategories[subcategory] = item['amount']
        
        # إنشاء DataFrame للرسم البياني
        direct_cost_df = pd.DataFrame({
            'الفئة الفرعية': list(direct_cost_subcategories.keys()),
            'المبلغ': list(direct_cost_subcategories.values())
        })
        
        # إنشاء رسم بياني دائري
        fig = px.pie(
            direct_cost_df,
            values='المبلغ',
            names='الفئة الفرعية',
            title='توزيع التكاليف المباشرة',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض توزيع التكاليف غير المباشرة
        st.markdown("### توزيع التكاليف غير المباشرة")
        
        # تجميع البيانات حسب الفئة الفرعية للتكاليف غير المباشرة
        indirect_cost_subcategories = {}
        
        for item in st.session_state.cost_analysis:
            if item['category'] == 'تكاليف غير مباشرة':
                subcategory = item['subcategory']
                if subcategory in indirect_cost_subcategories:
                    indirect_cost_subcategories[subcategory] += item['amount']
                else:
                    indirect_cost_subcategories[subcategory] = item['amount']
        
        # إنشاء DataFrame للرسم البياني
        indirect_cost_df = pd.DataFrame({
            'الفئة الفرعية': list(indirect_cost_subcategories.keys()),
            'المبلغ': list(indirect_cost_subcategories.values())
        })
        
        # إنشاء رسم بياني دائري
        fig = px.pie(
            indirect_cost_df,
            values='المبلغ',
            names='الفئة الفرعية',
            title='توزيع التكاليف غير المباشرة',
            color_discrete_sequence=px.colors.qualitative.Pastel1
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_bill_of_quantities_tab(self):
        """عرض تبويب جدول الكميات"""
        
        st.markdown("### جدول الكميات")
        
        # إنشاء DataFrame من بيانات جدول الكميات
        boq_df = pd.DataFrame(st.session_state.bill_of_quantities)
        
        # عرض جدول الكميات
        st.dataframe(
            boq_df[['code', 'description', 'unit', 'quantity', 'unit_price', 'total_price', 'category']],
            column_config={
                'code': 'الكود',
                'description': 'الوصف',
                'unit': 'الوحدة',
                'quantity': 'الكمية',
                'unit_price': st.column_config.NumberColumn('سعر الوحدة', format='%d ريال'),
                'total_price': st.column_config.NumberColumn('السعر الإجمالي', format='%d ريال'),
                'category': 'الفئة'
            },
            hide_index=True,
            use_container_width=True
        )
        
        # إضافة بند جديد
        st.markdown("### إضافة بند جديد")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_code = st.text_input("الكود", key="new_boq_code")
            new_description = st.text_input("الوصف", key="new_boq_description")
            new_unit = st.selectbox("الوحدة", ["م3", "م2", "طن", "عدد", "متر طولي"], key="new_boq_unit")
        
        with col2:
            new_quantity = st.number_input("الكمية", min_value=0.0, step=1.0, key="new_boq_quantity")
            new_unit_price = st.number_input("سعر الوحدة", min_value=0.0, step=10.0, key="new_boq_unit_price")
            new_category = st.selectbox(
                "الفئة",
                [
                    "أعمال ترابية",
                    "أعمال خرسانية",
                    "أعمال حديد",
                    "أعمال بناء",
                    "أعمال تشطيبات",
                    "أعمال نجارة",
                    "أعمال ألمنيوم",
                    "أعمال كهربائية",
                    "أعمال ميكانيكية",
                    "أعمال صحية"
                ],
                key="new_boq_category"
            )
        
        if st.button("إضافة البند", key="add_boq_item"):
            if new_code and new_description and new_quantity > 0 and new_unit_price > 0:
                # حساب السعر الإجمالي
                new_total_price = new_quantity * new_unit_price
                
                # إضافة بند جديد
                new_id = max([item['id'] for item in st.session_state.bill_of_quantities]) + 1
                
                st.session_state.bill_of_quantities.append({
                    'id': new_id,
                    'code': new_code,
                    'description': new_description,
                    'unit': new_unit,
                    'quantity': new_quantity,
                    'unit_price': new_unit_price,
                    'total_price': new_total_price,
                    'category': new_category
                })
                
                st.success(f"تمت إضافة البند بنجاح: {new_description}")
                
                # تحديث الصفحة لعرض البند الجديد
                st.rerun()
            else:
                st.error("يرجى إدخال جميع البيانات المطلوبة بشكل صحيح")
        
        # عرض ملخص جدول الكميات (إزالة التكرار)
        st.markdown("### ملخص جدول الكميات")
        
        # تجميع البيانات حسب الفئة
        category_totals = {}
        for item in st.session_state.bill_of_quantities:
            category = item['category']
            if category in category_totals:
                category_totals[category] += item['total_price']
            else:
                category_totals[category] = item['total_price']
        
        # إنشاء DataFrame للرسم البياني
        category_df = pd.DataFrame({
            'الفئة': list(category_totals.keys()),
            'المبلغ': list(category_totals.values())
        })
        
        # ترتيب البيانات تنازليًا حسب المبلغ
        category_df = category_df.sort_values('المبلغ', ascending=False)
        
        # إنشاء رسم بياني شريطي
        fig = px.bar(
            category_df,
            x='الفئة',
            y='المبلغ',
            title='إجمالي تكلفة البنود حسب الفئة',
            color='الفئة',
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حساب إجمالي جدول الكميات
        total_boq = sum(item['total_price'] for item in st.session_state.bill_of_quantities)
    
    # يجب إضافة باقي الدوال المفقودة هنا
    def _render_cost_analysis_tab(self):
        """عرض تبويب تحليل التكاليف"""
        # تنفيذ هذه الدالة حسب متطلبات التطبيق
        st.markdown("### تحليل التكاليف")
        # محتوى مؤقت
        st.info("تبويب تحليل التكاليف قيد التطوير")
    
    def _render_pricing_scenarios_tab(self):
        """عرض تبويب سيناريوهات التسعير"""
        # تنفيذ هذه الدالة حسب متطلبات التطبيق
        st.markdown("### سيناريوهات التسعير")
        # محتوى مؤقت
        st.info("تبويب سيناريوهات التسعير قيد التطوير")
    
    def _render_competitive_analysis_tab(self):
        """عرض تبويب المقارنة التنافسية"""
        # تنفيذ هذه الدالة حسب متطلبات التطبيق
        st.markdown("### المقارنة التنافسية")
        # محتوى مؤقت
        st.info("تبويب المقارنة التنافسية قيد التطوير")
    
    def _render_reports_tab(self):
        """عرض تبويب التقارير"""
        # تنفيذ هذه الدالة حسب متطلبات التطبيق
        st.markdown("### التقارير")
        # محتوى مؤقت
        st.info("تبويب التقارير قيد التطوير")
