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
            
        # إضافة بيانات المقارنة التنافسية
        if 'competitive_analysis' not in st.session_state:
            st.session_state.competitive_analysis = [
                {
                    'id': 1,
                    'competitor': 'شركة الإنشاءات المتحدة',
                    'project_type': 'مباني سكنية',
                    'price_per_sqm': 1800,
                    'delivery_time': 12,
                    'quality_rating': 4.2,
                    'market_share': 15.5
                },
                {
                    'id': 2,
                    'competitor': 'مجموعة البناء الحديث',
                    'project_type': 'مباني سكنية',
                    'price_per_sqm': 2100,
                    'delivery_time': 10,
                    'quality_rating': 4.5,
                    'market_share': 18.2
                },
                {
                    'id': 3,
                    'competitor': 'شركة الإعمار الدولية',
                    'project_type': 'مباني سكنية',
                    'price_per_sqm': 2300,
                    'delivery_time': 14,
                    'quality_rating': 4.7,
                    'market_share': 22.0
                },
                {
                    'id': 4,
                    'competitor': 'مؤسسة البناء المتكامل',
                    'project_type': 'مباني سكنية',
                    'price_per_sqm': 1750,
                    'delivery_time': 15,
                    'quality_rating': 3.8,
                    'market_share': 12.5
                },
                {
                    'id': 5,
                    'competitor': 'شركتنا',
                    'project_type': 'مباني سكنية',
                    'price_per_sqm': 1950,
                    'delivery_time': 11,
                    'quality_rating': 4.4,
                    'market_share': 14.8
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
    
    def _render_cost_analysis_tab(self):
        """عرض تبويب تحليل التكاليف"""
        
        st.markdown("### تحليل التكاليف")
        
        # عرض جدول تحليل التكاليف
        cost_df = pd.DataFrame(st.session_state.cost_analysis)
        
        st.dataframe(
            cost_df[['category', 'subcategory', 'description', 'amount', 'percentage']],
            column_config={
                'category': 'الفئة',
                'subcategory': 'الفئة الفرعية',
                'description': 'الوصف',
                'amount': st.column_config.NumberColumn('المبلغ', format='%d ريال'),
                'percentage': st.column_config.NumberColumn('النسبة المئوية', format='%.1f%%')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # إضافة بند تكلفة جديد
        st.markdown("### إضافة بند تكلفة جديد")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_category = st.selectbox(
                "الفئة",
                ["تكاليف مباشرة", "تكاليف غير مباشرة", "أرباح"],
                key="new_cost_category"
            )
            
            # تحديد الفئات الفرعية بناءً على الفئة المختارة
            subcategory_options = []
            if new_category == "تكاليف مباشرة":
                subcategory_options = ["مواد", "عمالة", "معدات"]
            elif new_category == "تكاليف غير مباشرة":
                subcategory_options = ["إدارة", "عامة", "تمويل"]
            else:
                subcategory_options = ["أرباح"]
                
            new_subcategory = st.selectbox(
                "الفئة الفرعية",
                subcategory_options,
                key="new_cost_subcategory"
            )
            
            new_description = st.text_input("الوصف", key="new_cost_description")
        
        with col2:
            new_amount = st.number_input("المبلغ", min_value=0.0, step=1000.0, key="new_cost_amount")
            
            # حساب إجمالي التكاليف الحالية
            total_cost = sum(item['amount'] for item in st.session_state.cost_analysis)
            
            # حساب النسبة المئوية التقريبية
            if total_cost > 0:
                estimated_percentage = (new_amount / total_cost) * 100
            else:
                estimated_percentage = 0
                
            st.metric("النسبة المئوية التقديرية", f"{estimated_percentage:.1f}%")
        
        if st.button("إضافة بند التكلفة", key="add_cost_item"):
            if new_description and new_amount > 0:
                # إضافة بند جديد
                new_id = max([item['id'] for item in st.session_state.cost_analysis]) + 1
                
                # حساب النسبة المئوية الفعلية بعد إضافة البند الجديد
                new_total = total_cost + new_amount
                
                # إعادة حساب النسب المئوية لجميع البنود
                for item in st.session_state.cost_analysis:
                    item['percentage'] = (item['amount'] / new_total) * 100
                
                # إضافة البند الجديد
                st.session_state.cost_analysis.append({
                    'id': new_id,
                    'category': new_category,
                    'subcategory': new_subcategory,
                    'description': new_description,
                    'amount': new_amount,
                    'percentage': (new_amount / new_total) * 100
                })
                
                st.success(f"تمت إضافة بند التكلفة بنجاح: {new_description}")
                
                # تحديث الصفحة لعرض البند الجديد
                st.rerun()
            else:
                st.error("يرجى إدخال جميع البيانات المطلوبة بشكل صحيح")
        
        # تحليل التكاليف حسب الفئة والفئة الفرعية
        st.markdown("### تحليل التكاليف حسب الفئة والفئة الفرعية")
        
        # تجميع البيانات حسب الفئة والفئة الفرعية
        cost_by_category_subcategory = {}
        
        for item in st.session_state.cost_analysis:
            category = item['category']
            subcategory = item['subcategory']
            key = f"{category} - {subcategory}"
            
            if key in cost_by_category_subcategory:
                cost_by_category_subcategory[key] += item['amount']
            else:
                cost_by_category_subcategory[key] = item['amount']
        
        # إنشاء DataFrame للرسم البياني
        cost_category_subcategory_df = pd.DataFrame({
            'الفئة والفئة الفرعية': list(cost_by_category_subcategory.keys()),
            'المبلغ': list(cost_by_category_subcategory.values())
        })
        
        # ترتيب البيانات تنازليًا حسب المبلغ
        cost_category_subcategory_df = cost_category_subcategory_df.sort_values('المبلغ', ascending=False)
        
        # إنشاء رسم بياني شريطي
        fig = px.bar(
            cost_category_subcategory_df,
            x='الفئة والفئة الفرعية',
            y='المبلغ',
            title='تحليل التكاليف حسب الفئة والفئة الفرعية',
            color='الفئة والفئة الفرعية',
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل نسب التكاليف
        st.markdown("### تحليل نسب التكاليف")
        
        # إنشاء رسم بياني للنسب المئوية
        percentage_df = pd.DataFrame(st.session_state.cost_analysis)
        
        fig = px.treemap(
            percentage_df,
            path=['category', 'subcategory', 'description'],
            values='amount',
            title='تحليل هيكل التكاليف',
            color='percentage',
            color_continuous_scale='RdBu',
            color_continuous_midpoint=np.average(percentage_df['percentage'])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل اتجاهات التكاليف (بيانات افتراضية)
        st.markdown("### تحليل اتجاهات التكاليف")
        
        # إنشاء بيانات افتراضية للاتجاهات
        months = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو']
        direct_costs = [510000, 520000, 515000, 525000, 530000, 514000]
        indirect_costs = [130000, 135000, 132000, 138000, 140000, 135000]
        
        # إنشاء DataFrame للرسم البياني
        trends_df = pd.DataFrame({
            'الشهر': months * 2,
            'نوع التكلفة': ['تكاليف مباشرة'] * 6 + ['تكاليف غير مباشرة'] * 6,
            'المبلغ': direct_costs + indirect_costs
        })
        
        # إنشاء رسم بياني خطي
        fig = px.line(
            trends_df,
            x='الشهر',
            y='المبلغ',
            color='نوع التكلفة',
            title='اتجاهات التكاليف على مدار الأشهر الستة الماضية',
            markers=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_pricing_scenarios_tab(self):
        """عرض تبويب سيناريوهات التسعير"""
        
        st.markdown("### سيناريوهات التسعير")
        
        # عرض جدول سيناريوهات التسعير
        scenarios_df = pd.DataFrame(st.session_state.price_scenarios)
        
        st.dataframe(
            scenarios_df[['name', 'description', 'total_cost', 'profit_margin', 'total_price', 'is_active']],
            column_config={
                'name': 'اسم السيناريو',
                'description': 'الوصف',
                'total_cost': st.column_config.NumberColumn('إجمالي التكلفة', format='%d ريال'),
                'profit_margin': st.column_config.NumberColumn('هامش الربح', format='%.1f%%'),
                'total_price': st.column_config.NumberColumn('السعر الإجمالي', format='%d ريال'),
                'is_active': st.column_config.CheckboxColumn('نشط')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # إنشاء سيناريو جديد
        st.markdown("### إنشاء سيناريو جديد")
        
        col1, col2 = st.columns(2)
        
        # حساب إجمالي التكاليف
        total_cost = sum(item['amount'] for item in st.session_state.cost_analysis 
                         if item['category'] != 'أرباح')
        
        with col1:
            new_name = st.text_input("اسم السيناريو", key="new_scenario_name")
            new_description = st.text_input("وصف السيناريو", key="new_scenario_description")
        
        with col2:
            new_profit_margin = st.slider(
                "هامش الربح (%)",
                min_value=0.0,
                max_value=30.0,
                value=10.0,
                step=0.5,
                key="new_scenario_profit_margin"
            )
            
            # حساب السعر الإجمالي بناءً على هامش الربح
            profit_amount = total_cost * (new_profit_margin / 100)
            new_total_price = total_cost + profit_amount
            
            st.metric("إجمالي التكلفة", f"{total_cost:,.0f} ريال")
            st.metric("السعر الإجمالي المقترح", f"{new_total_price:,.0f} ريال")
        
        if st.button("إضافة السيناريو", key="add_scenario"):
            if new_name and new_description:
                # إضافة سيناريو جديد
                new_id = max([item['id'] for item in st.session_state.price_scenarios]) + 1
                
                st.session_state.price_scenarios.append({
                    'id': new_id,
                    'name': new_name,
                    'description': new_description,
                    'total_cost': total_cost,
                    'profit_margin': new_profit_margin,
                    'total_price': new_total_price,
                    'is_active': False
                })
                
                st.success(f"تمت إضافة السيناريو بنجاح: {new_name}")
                
                # تحديث الصفحة لعرض السيناريو الجديد
                st.rerun()
            else:
                st.error("يرجى إدخال جميع البيانات المطلوبة بشكل صحيح")
        
        # مقارنة السيناريوهات
        st.markdown("### مقارنة السيناريوهات")
        
        # إنشاء رسم بياني للمقارنة
        fig = go.Figure()
        
        for scenario in st.session_state.price_scenarios:
            fig.add_trace(go.Bar(
                name=scenario['name'],
                x=['التكلفة', 'الربح', 'السعر الإجمالي'],
                y=[
                    scenario['total_cost'],
                    scenario['total_price'] - scenario['total_cost'],
                    scenario['total_price']
                ],
                text=[
                    f"{scenario['total_cost']:,.0f}",
                    f"{scenario['total_price'] - scenario['total_cost']:,.0f}",
                    f"{scenario['total_price']:,.0f}"
                ],
                textposition='auto'
            ))
        
        fig.update_layout(
            title='مقارنة السيناريوهات',
            barmode='group',
            xaxis_title='العنصر',
            yaxis_title='المبلغ (ريال)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل حساسية هامش الربح
        st.markdown("### تحليل حساسية هامش الربح")
        
        # إنشاء بيانات لتحليل الحساسية
        profit_margins = list(range(5, 26, 1))  # من 5% إلى 25%
        total_prices = [total_cost * (1 + margin/100) for margin in profit_margins]
        
        # إنشاء DataFrame للرسم البياني
        sensitivity_df = pd.DataFrame({
            'هامش الربح (%)': profit_margins,
            'السعر الإجمالي': total_prices
        })
        
        # إنشاء رسم بياني خطي
        fig = px.line(
            sensitivity_df,
            x='هامش الربح (%)',
            y='السعر الإجمالي',
            title='تحليل حساسية هامش الربح',
            markers=True
        )
        
        # إضافة خط أفقي يمثل السعر التنافسي (افتراضي)
        competitive_price = 650000
        fig.add_hline(
            y=competitive_price,
            line_dash="dash",
            line_color="red",
            annotation_text="السعر التنافسي",
            annotation_position="bottom right"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تفعيل/تعطيل السيناريوهات
        st.markdown("### تفعيل/تعطيل السيناريوهات")
        
        for i, scenario in enumerate(st.session_state.price_scenarios):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(f"**{scenario['name']}**: {scenario['description']}")
            
            with col2:
                is_active = st.checkbox(
                    "تفعيل",
                    value=scenario['is_active'],
                    key=f"activate_scenario_{scenario['id']}"
                )
                
                # تحديث حالة التفعيل
                if is_active != scenario['is_active']:
                    # إذا تم تفعيل سيناريو، قم بتعطيل جميع السيناريوهات الأخرى
                    if is_active:
                        for j, other_scenario in enumerate(st.session_state.price_scenarios):
                            if j != i:
                                other_scenario['is_active'] = False
                    
                    # تحديث حالة السيناريو الحالي
                    scenario['is_active'] = is_active
                    
                    # تحديث الصفحة
                    st.rerun()
    
    def _render_competitive_analysis_tab(self):
        """عرض تبويب المقارنة التنافسية"""
        
        st.markdown("### المقارنة التنافسية")
        
        # عرض جدول المقارنة التنافسية
        competitive_df = pd.DataFrame(st.session_state.competitive_analysis)
        
        st.dataframe(
            competitive_df[['competitor', 'project_type', 'price_per_sqm', 'delivery_time', 'quality_rating', 'market_share']],
            column_config={
                'competitor': 'المنافس',
                'project_type': 'نوع المشروع',
                'price_per_sqm': st.column_config.NumberColumn('السعر لكل متر مربع', format='%d ريال'),
                'delivery_time': st.column_config.NumberColumn('مدة التسليم (شهر)', format='%d'),
                'quality_rating': st.column_config.NumberColumn('تقييم الجودة', format='%.1f/5.0'),
                'market_share': st.column_config.NumberColumn('الحصة السوقية', format='%.1f%%')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # إضافة منافس جديد
        st.markdown("### إضافة منافس جديد")
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_competitor = st.text_input("اسم المنافس", key="new_competitor_name")
            new_project_type = st.selectbox(
                "نوع المشروع",
                ["مباني سكنية", "مباني تجارية", "مباني صناعية", "بنية تحتية"],
                key="new_competitor_project_type"
            )
            new_price_per_sqm = st.number_input(
                "السعر لكل متر مربع (ريال)",
                min_value=0,
                step=50,
                key="new_competitor_price"
            )
        
        with col2:
            new_delivery_time = st.number_input(
                "مدة التسليم (شهر)",
                min_value=1,
                max_value=36,
                step=1,
                key="new_competitor_delivery"
            )
            new_quality_rating = st.slider(
                "تقييم الجودة",
                min_value=1.0,
                max_value=5.0,
                value=3.5,
                step=0.1,
                key="new_competitor_quality"
            )
            new_market_share = st.number_input(
                "الحصة السوقية (%)",
                min_value=0.0,
                max_value=100.0,
                step=0.5,
                key="new_competitor_market_share"
            )
        
        if st.button("إضافة منافس", key="add_competitor"):
            if new_competitor and new_price_per_sqm > 0:
                # إضافة منافس جديد
                new_id = max([item['id'] for item in st.session_state.competitive_analysis]) + 1
                
                st.session_state.competitive_analysis.append({
                    'id': new_id,
                    'competitor': new_competitor,
                    'project_type': new_project_type,
                    'price_per_sqm': new_price_per_sqm,
                    'delivery_time': new_delivery_time,
                    'quality_rating': new_quality_rating,
                    'market_share': new_market_share
                })
                
                st.success(f"تمت إضافة المنافس بنجاح: {new_competitor}")
                
                # تحديث الصفحة لعرض المنافس الجديد
                st.rerun()
            else:
                st.error("يرجى إدخال جميع البيانات المطلوبة بشكل صحيح")
        
        # تحليل مقارنة الأسعار
        st.markdown("### مقارنة الأسعار")
        
        # إنشاء DataFrame للرسم البياني
        price_comparison_df = pd.DataFrame(st.session_state.competitive_analysis)
        
        # ترتيب البيانات تصاعديًا حسب السعر
        price_comparison_df = price_comparison_df.sort_values('price_per_sqm')
        
        # إنشاء رسم بياني شريطي
        fig = px.bar(
            price_comparison_df,
            x='competitor',
            y='price_per_sqm',
            title='مقارنة الأسعار لكل متر مربع',
            color='competitor',
            text_auto=True
        )
        
        # تمييز شركتنا
        for i, competitor in enumerate(price_comparison_df['competitor']):
            if competitor == 'شركتنا':
                fig.data[0].marker.color = ['blue' if x != i else 'red' for x in range(len(price_comparison_df))]
                break
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل مقارنة الجودة والسعر
        st.markdown("### مقارنة الجودة والسعر")
        
        # إنشاء رسم بياني للعلاقة بين السعر والجودة
        fig = px.scatter(
            price_comparison_df,
            x='price_per_sqm',
            y='quality_rating',
            size='market_share',
            color='competitor',
            title='العلاقة بين السعر والجودة والحصة السوقية',
            labels={
                'price_per_sqm': 'السعر لكل متر مربع (ريال)',
                'quality_rating': 'تقييم الجودة',
                'market_share': 'الحصة السوقية (%)'
            },
            text='competitor'
        )
        
        fig.update_traces(textposition='top center')
        
        # إضافة خط اتجاه
        fig.update_layout(
            shapes=[
                dict(
                    type='line',
                    x0=min(price_comparison_df['price_per_sqm']),
                    y0=min(price_comparison_df['quality_rating']),
                    x1=max(price_comparison_df['price_per_sqm']),
                    y1=max(price_comparison_df['quality_rating']),
                    line=dict(color='gray', dash='dash')
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل مقارنة مدة التسليم
        st.markdown("### مقارنة مدة التسليم")
        
        # ترتيب البيانات تصاعديًا حسب مدة التسليم
        delivery_comparison_df = price_comparison_df.sort_values('delivery_time')
        
        # إنشاء رسم بياني شريطي
        fig = px.bar(
            delivery_comparison_df,
            x='competitor',
            y='delivery_time',
            title='مقارنة مدة التسليم (شهر)',
            color='competitor',
            text_auto=True
        )
        
        # تمييز شركتنا
        for i, competitor in enumerate(delivery_comparison_df['competitor']):
            if competitor == 'شركتنا':
                fig.data[0].marker.color = ['blue' if x != i else 'red' for x in range(len(delivery_comparison_df))]
                break
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل الحصة السوقية
        st.markdown("### تحليل الحصة السوقية")
        
        # إنشاء رسم بياني دائري للحصة السوقية
        fig = px.pie(
            price_comparison_df,
            values='market_share',
            names='competitor',
            title='توزيع الحصة السوقية',
            hole=0.4
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_reports_tab(self):
        """عرض تبويب التقارير"""
        
        st.markdown("### تقارير التسعير")
        
        # اختيار نوع التقرير
        report_type = st.selectbox(
            "اختر نوع التقرير",
            [
                "ملخص التسعير",
                "تقرير جدول الكميات",
                "تقرير تحليل التكاليف",
                "تقرير سيناريوهات التسعير",
                "تقرير المقارنة التنافسية",
                "التقرير الشامل"
            ]
        )
        
        # عرض معلومات المشروع
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("اسم المشروع", "مشروع إنشاء مبنى سكني")
            client_name = st.text_input("اسم العميل", "شركة التطوير العقاري")
        
        with col2:
            project_location = st.text_input("موقع المشروع", "الرياض، المملكة العربية السعودية")
            report_date = st.date_input("تاريخ التقرير", datetime.now())
        
        # إنشاء التقرير
        if st.button("إنشاء التقرير"):
            st.markdown("### معاينة التقرير")
            
            # عرض ترويسة التقرير
            st.markdown(f"""
            ## {report_type}
            **اسم المشروع:** {project_name}  
            **اسم العميل:** {client_name}  
            **موقع المشروع:** {project_location}  
            **تاريخ التقرير:** {report_date.strftime('%Y-%m-%d')}
            """)
            
            # عرض محتوى التقرير حسب النوع المختار
            if report_type == "ملخص التسعير" or report_type == "التقرير الشامل":
                self._render_pricing_summary_report()
            
            if report_type == "تقرير جدول الكميات" or report_type == "التقرير الشامل":
                self._render_boq_report()
            
            if report_type == "تقرير تحليل التكاليف" or report_type == "التقرير الشامل":
                self._render_cost_analysis_report()
            
            if report_type == "تقرير سيناريوهات التسعير" or report_type == "التقرير الشامل":
                self._render_pricing_scenarios_report()
            
            if report_type == "تقرير المقارنة التنافسية" or report_type == "التقرير الشامل":
                self._render_competitive_analysis_report()
            
            # خيارات تصدير التقرير
            st.markdown("### تصدير التقرير")
            
            export_format = st.radio(
                "اختر صيغة التصدير",
                ["PDF", "Excel", "Word"],
                horizontal=True
            )
            
            if st.button("تصدير التقرير"):
                st.success(f"تم تصدير التقرير بصيغة {export_format} بنجاح!")
    
    def _render_pricing_summary_report(self):
        """عرض تقرير ملخص التسعير"""
        
        st.markdown("## ملخص التسعير")
        
        # حساب إجمالي التكاليف
        total_direct_cost = sum(item['amount'] for item in st.session_state.cost_analysis if item['category'] == 'تكاليف مباشرة')
        total_indirect_cost = sum(item['amount'] for item in st.session_state.cost_analysis if item['category'] == 'تكاليف غير مباشرة')
        total_profit = sum(item['amount'] for item in st.session_state.cost_analysis if item['category'] == 'أرباح')
        total_cost = total_direct_cost + total_indirect_cost
        total_price = total_cost + total_profit
        
        # عرض ملخص التكاليف
        st.markdown("### ملخص التكاليف")
        
        summary_data = {
            'البند': ['التكاليف المباشرة', 'التكاليف غير المباشرة', 'إجمالي التكاليف', 'هامش الربح', 'السعر الإجمالي'],
            'المبلغ (ريال)': [total_direct_cost, total_indirect_cost, total_cost, total_profit, total_price],
            'النسبة المئوية': [
                total_direct_cost / total_price * 100,
                total_indirect_cost / total_price * 100,
                total_cost / total_price * 100,
                total_profit / total_price * 100,
                100.0
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        
        st.dataframe(
            summary_df,
            column_config={
                'البند': st.column_config.TextColumn('البند'),
                'المبلغ (ريال)': st.column_config.NumberColumn('المبلغ (ريال)', format='%d'),
                'النسبة المئوية': st.column_config.NumberColumn('النسبة المئوية', format='%.1f%%')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # عرض رسم بياني للملخص
        fig = px.pie(
            summary_df.iloc[0:3],  # استخدام أول 3 صفوف فقط (التكاليف)
            values='المبلغ (ريال)',
            names='البند',
            title='توزيع التكاليف',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض رسم بياني للسعر الإجمالي
        fig = px.pie(
            summary_df.iloc[[2, 3]],  # استخدام صفوف التكاليف والربح
            values='المبلغ (ريال)',
            names='البند',
            title='تركيبة السعر الإجمالي',
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_boq_report(self):
        """عرض تقرير جدول الكميات"""
        
        st.markdown("## تقرير جدول الكميات")
        
        # عرض جدول الكميات
        boq_df = pd.DataFrame(st.session_state.bill_of_quantities)
        
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
        
        # عرض ملخص جدول الكميات حسب الفئة
        st.markdown("### ملخص جدول الكميات حسب الفئة")
        
        # تجميع البيانات حسب الفئة
        category_totals = {}
        for item in st.session_state.bill_of_quantities:
            category = item['category']
            if category in category_totals:
                category_totals[category] += item['total_price']
            else:
                category_totals[category] = item['total_price']
        
        # إنشاء DataFrame للملخص
        category_summary_df = pd.DataFrame({
            'الفئة': list(category_totals.keys()),
            'المبلغ الإجمالي': list(category_totals.values())
        })
        
        # حساب النسبة المئوية
        total_boq = sum(category_totals.values())
        category_summary_df['النسبة المئوية'] = category_summary_df['المبلغ الإجمالي'] / total_boq * 100
        
        # ترتيب البيانات تنازليًا حسب المبلغ
        category_summary_df = category_summary_df.sort_values('المبلغ الإجمالي', ascending=False)
        
        st.dataframe(
            category_summary_df,
            column_config={
                'الفئة': st.column_config.TextColumn('الفئة'),
                'المبلغ الإجمالي': st.column_config.NumberColumn('المبلغ الإجمالي', format='%d ريال'),
                'النسبة المئوية': st.column_config.NumberColumn('النسبة المئوية', format='%.1f%%')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # عرض رسم بياني للملخص
        fig = px.pie(
            category_summary_df,
            values='المبلغ الإجمالي',
            names='الفئة',
            title='توزيع تكاليف البنود حسب الفئة',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض رسم بياني شريطي للملخص
        fig = px.bar(
            category_summary_df,
            x='الفئة',
            y='المبلغ الإجمالي',
            title='إجمالي تكلفة البنود حسب الفئة',
            color='الفئة',
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_cost_analysis_report(self):
        """عرض تقرير تحليل التكاليف"""
        
        st.markdown("## تقرير تحليل التكاليف")
        
        # عرض جدول تحليل التكاليف
        cost_df = pd.DataFrame(st.session_state.cost_analysis)
        
        st.dataframe(
            cost_df[['category', 'subcategory', 'description', 'amount', 'percentage']],
            column_config={
                'category': 'الفئة',
                'subcategory': 'الفئة الفرعية',
                'description': 'الوصف',
                'amount': st.column_config.NumberColumn('المبلغ', format='%d ريال'),
                'percentage': st.column_config.NumberColumn('النسبة المئوية', format='%.1f%%')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # عرض ملخص تحليل التكاليف حسب الفئة
        st.markdown("### ملخص تحليل التكاليف حسب الفئة")
        
        # تجميع البيانات حسب الفئة
        category_totals = {}
        for item in st.session_state.cost_analysis:
            category = item['category']
            if category in category_totals:
                category_totals[category] += item['amount']
            else:
                category_totals[category] = item['amount']
        
        # إنشاء DataFrame للملخص
        category_summary_df = pd.DataFrame({
            'الفئة': list(category_totals.keys()),
            'المبلغ الإجمالي': list(category_totals.values())
        })
        
        # حساب النسبة المئوية
        total_cost = sum(category_totals.values())
        category_summary_df['النسبة المئوية'] = category_summary_df['المبلغ الإجمالي'] / total_cost * 100
        
        # ترتيب البيانات تنازليًا حسب المبلغ
        category_summary_df = category_summary_df.sort_values('المبلغ الإجمالي', ascending=False)
        
        st.dataframe(
            category_summary_df,
            column_config={
                'الفئة': st.column_config.TextColumn('الفئة'),
                'المبلغ الإجمالي': st.column_config.NumberColumn('المبلغ الإجمالي', format='%d ريال'),
                'النسبة المئوية': st.column_config.NumberColumn('النسبة المئوية', format='%.1f%%')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # عرض رسم بياني للملخص
        fig = px.pie(
            category_summary_df,
            values='المبلغ الإجمالي',
            names='الفئة',
            title='توزيع التكاليف حسب الفئة',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض ملخص تحليل التكاليف حسب الفئة والفئة الفرعية
        st.markdown("### ملخص تحليل التكاليف حسب الفئة والفئة الفرعية")
        
        # تجميع البيانات حسب الفئة والفئة الفرعية
        subcategory_totals = {}
        for item in st.session_state.cost_analysis:
            category = item['category']
            subcategory = item['subcategory']
            key = f"{category} - {subcategory}"
            if key in subcategory_totals:
                subcategory_totals[key] += item['amount']
            else:
                subcategory_totals[key] = item['amount']
        
        # إنشاء DataFrame للملخص
        subcategory_summary_df = pd.DataFrame({
            'الفئة والفئة الفرعية': list(subcategory_totals.keys()),
            'المبلغ الإجمالي': list(subcategory_totals.values())
        })
        
        # حساب النسبة المئوية
        subcategory_summary_df['النسبة المئوية'] = subcategory_summary_df['المبلغ الإجمالي'] / total_cost * 100
        
        # ترتيب البيانات تنازليًا حسب المبلغ
        subcategory_summary_df = subcategory_summary_df.sort_values('المبلغ الإجمالي', ascending=False)
        
        st.dataframe(
            subcategory_summary_df,
            column_config={
                'الفئة والفئة الفرعية': st.column_config.TextColumn('الفئة والفئة الفرعية'),
                'المبلغ الإجمالي': st.column_config.NumberColumn('المبلغ الإجمالي', format='%d ريال'),
                'النسبة المئوية': st.column_config.NumberColumn('النسبة المئوية', format='%.1f%%')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # عرض رسم بياني للملخص
        fig = px.bar(
            subcategory_summary_df,
            x='الفئة والفئة الفرعية',
            y='المبلغ الإجمالي',
            title='توزيع التكاليف حسب الفئة والفئة الفرعية',
            color='الفئة والفئة الفرعية',
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض تحليل هيكل التكاليف
        st.markdown("### تحليل هيكل التكاليف")
        
        # إنشاء رسم بياني للنسب المئوية
        fig = px.treemap(
            cost_df,
            path=['category', 'subcategory', 'description'],
            values='amount',
            title='تحليل هيكل التكاليف',
            color='percentage',
            color_continuous_scale='RdBu',
            color_continuous_midpoint=np.average(cost_df['percentage'])
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_pricing_scenarios_report(self):
        """عرض تقرير سيناريوهات التسعير"""
        
        st.markdown("## تقرير سيناريوهات التسعير")
        
        # عرض جدول سيناريوهات التسعير
        scenarios_df = pd.DataFrame(st.session_state.price_scenarios)
        
        st.dataframe(
            scenarios_df[['name', 'description', 'total_cost', 'profit_margin', 'total_price', 'is_active']],
            column_config={
                'name': 'اسم السيناريو',
                'description': 'الوصف',
                'total_cost': st.column_config.NumberColumn('إجمالي التكلفة', format='%d ريال'),
                'profit_margin': st.column_config.NumberColumn('هامش الربح', format='%.1f%%'),
                'total_price': st.column_config.NumberColumn('السعر الإجمالي', format='%d ريال'),
                'is_active': st.column_config.CheckboxColumn('نشط')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # عرض مقارنة السيناريوهات
        st.markdown("### مقارنة السيناريوهات")
        
        # إنشاء رسم بياني للمقارنة
        fig = go.Figure()
        
        for scenario in st.session_state.price_scenarios:
            fig.add_trace(go.Bar(
                name=scenario['name'],
                x=['التكلفة', 'الربح', 'السعر الإجمالي'],
                y=[
                    scenario['total_cost'],
                    scenario['total_price'] - scenario['total_cost'],
                    scenario['total_price']
                ],
                text=[
                    f"{scenario['total_cost']:,.0f}",
                    f"{scenario['total_price'] - scenario['total_cost']:,.0f}",
                    f"{scenario['total_price']:,.0f}"
                ],
                textposition='auto'
            ))
        
        fig.update_layout(
            title='مقارنة السيناريوهات',
            barmode='group',
            xaxis_title='العنصر',
            yaxis_title='المبلغ (ريال)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض مقارنة هوامش الربح
        st.markdown("### مقارنة هوامش الربح")
        
        # إنشاء DataFrame للمقارنة
        profit_comparison_df = pd.DataFrame({
            'السيناريو': [scenario['name'] for scenario in st.session_state.price_scenarios],
            'هامش الربح (%)': [scenario['profit_margin'] for scenario in st.session_state.price_scenarios],
            'مبلغ الربح (ريال)': [scenario['total_price'] - scenario['total_cost'] for scenario in st.session_state.price_scenarios]
        })
        
        # ترتيب البيانات تنازليًا حسب هامش الربح
        profit_comparison_df = profit_comparison_df.sort_values('هامش الربح (%)', ascending=False)
        
        # إنشاء رسم بياني شريطي
        fig = px.bar(
            profit_comparison_df,
            x='السيناريو',
            y='هامش الربح (%)',
            title='مقارنة هوامش الربح',
            color='السيناريو',
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض تحليل حساسية هامش الربح
        st.markdown("### تحليل حساسية هامش الربح")
        
        # الحصول على التكلفة الإجمالية من السيناريو النشط أو الأول
        active_scenario = next((s for s in st.session_state.price_scenarios if s['is_active']), st.session_state.price_scenarios[0])
        total_cost = active_scenario['total_cost']
        
        # إنشاء بيانات لتحليل الحساسية
        profit_margins = list(range(5, 26, 1))  # من 5% إلى 25%
        total_prices = [total_cost * (1 + margin/100) for margin in profit_margins]
        
        # إنشاء DataFrame للرسم البياني
        sensitivity_df = pd.DataFrame({
            'هامش الربح (%)': profit_margins,
            'السعر الإجمالي': total_prices
        })
        
        # إنشاء رسم بياني خطي
        fig = px.line(
            sensitivity_df,
            x='هامش الربح (%)',
            y='السعر الإجمالي',
            title='تحليل حساسية هامش الربح',
            markers=True
        )
        
        # إضافة خط أفقي يمثل السعر التنافسي (افتراضي)
        competitive_price = 650000
        fig.add_hline(
            y=competitive_price,
            line_dash="dash",
            line_color="red",
            annotation_text="السعر التنافسي",
            annotation_position="bottom right"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def _render_competitive_analysis_report(self):
        """عرض تقرير المقارنة التنافسية"""
        
        st.markdown("## تقرير المقارنة التنافسية")
        
        # عرض جدول المقارنة التنافسية
        competitive_df = pd.DataFrame(st.session_state.competitive_analysis)
        
        st.dataframe(
            competitive_df[['competitor', 'project_type', 'price_per_sqm', 'delivery_time', 'quality_rating', 'market_share']],
            column_config={
                'competitor': 'المنافس',
                'project_type': 'نوع المشروع',
                'price_per_sqm': st.column_config.NumberColumn('السعر لكل متر مربع', format='%d ريال'),
                'delivery_time': st.column_config.NumberColumn('مدة التسليم (شهر)', format='%d'),
                'quality_rating': st.column_config.NumberColumn('تقييم الجودة', format='%.1f/5.0'),
                'market_share': st.column_config.NumberColumn('الحصة السوقية', format='%.1f%%')
            },
            hide_index=True,
            use_container_width=True
        )
        
        # عرض مقارنة الأسعار
        st.markdown("### مقارنة الأسعار")
        
        # ترتيب البيانات تصاعديًا حسب السعر
        price_comparison_df = competitive_df.sort_values('price_per_sqm')
        
        # إنشاء رسم بياني شريطي
        fig = px.bar(
            price_comparison_df,
            x='competitor',
            y='price_per_sqm',
            title='مقارنة الأسعار لكل متر مربع',
            color='competitor',
            text_auto=True
        )
        
        # تمييز شركتنا
        for i, competitor in enumerate(price_comparison_df['competitor']):
            if competitor == 'شركتنا':
                fig.data[0].marker.color = ['blue' if x != i else 'red' for x in range(len(price_comparison_df))]
                break
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض مقارنة الجودة والسعر
        st.markdown("### مقارنة الجودة والسعر")
        
        # إنشاء رسم بياني للعلاقة بين السعر والجودة
        fig = px.scatter(
            price_comparison_df,
            x='price_per_sqm',
            y='quality_rating',
            size='market_share',
            color='competitor',
            title='العلاقة بين السعر والجودة والحصة السوقية',
            labels={
                'price_per_sqm': 'السعر لكل متر مربع (ريال)',
                'quality_rating': 'تقييم الجودة',
                'market_share': 'الحصة السوقية (%)'
            },
            text='competitor'
        )
        
        fig.update_traces(textposition='top center')
        
        # إضافة خط اتجاه
        fig.update_layout(
            shapes=[
                dict(
                    type='line',
                    x0=min(price_comparison_df['price_per_sqm']),
                    y0=min(price_comparison_df['quality_rating']),
                    x1=max(price_comparison_df['price_per_sqm']),
                    y1=max(price_comparison_df['quality_rating']),
                    line=dict(color='gray', dash='dash')
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض مقارنة مدة التسليم
        st.markdown("### مقارنة مدة التسليم")
        
        # ترتيب البيانات تصاعديًا حسب مدة التسليم
        delivery_comparison_df = competitive_df.sort_values('delivery_time')
        
        # إنشاء رسم بياني شريطي
        fig = px.bar(
            delivery_comparison_df,
            x='competitor',
            y='delivery_time',
            title='مقارنة مدة التسليم (شهر)',
            color='competitor',
            text_auto=True
        )
        
        # تمييز شركتنا
        for i, competitor in enumerate(delivery_comparison_df['competitor']):
            if competitor == 'شركتنا':
                fig.data[0].marker.color = ['blue' if x != i else 'red' for x in range(len(delivery_comparison_df))]
                break
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض تحليل الحصة السوقية
        st.markdown("### تحليل الحصة السوقية")
        
        # إنشاء رسم بياني دائري للحصة السوقية
        fig = px.pie(
            competitive_df,
            values='market_share',
            names='competitor',
            title='توزيع الحصة السوقية',
            hole=0.4
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # عرض تحليل الموقع التنافسي
        st.markdown("### تحليل الموقع التنافسي")
        
        # إيجاد بيانات شركتنا
        our_company = next((item for item in st.session_state.competitive_analysis if item['competitor'] == 'شركتنا'), None)
        
        if our_company:
            # حساب متوسطات السوق
            avg_price = competitive_df['price_per_sqm'].mean()
            avg_delivery = competitive_df['delivery_time'].mean()
            avg_quality = competitive_df['quality_rating'].mean()
            
            # إنشاء بيانات المقارنة
            comparison_data = {
                'المؤشر': ['السعر لكل متر مربع', 'مدة التسليم', 'تقييم الجودة'],
                'قيمة شركتنا': [our_company['price_per_sqm'], our_company['delivery_time'], our_company['quality_rating']],
                'متوسط السوق': [avg_price, avg_delivery, avg_quality],
                'الفرق (%)': [
                    (our_company['price_per_sqm'] - avg_price) / avg_price * 100,
                    (our_company['delivery_time'] - avg_delivery) / avg_delivery * 100,
                    (our_company['quality_rating'] - avg_quality) / avg_quality * 100
                ]
            }
            
            comparison_df = pd.DataFrame(comparison_data)
            
            st.dataframe(
                comparison_df,
                column_config={
                    'المؤشر': st.column_config.TextColumn('المؤشر'),
                    'قيمة شركتنا': st.column_config.NumberColumn('قيمة شركتنا'),
                    'متوسط السوق': st.column_config.NumberColumn('متوسط السوق'),
                    'الفرق (%)': st.column_config.NumberColumn('الفرق (%)', format='%+.1f%%')
                },
                hide_index=True,
                use_container_width=True
            )
            
            # إنشاء رسم بياني راداري للموقع التنافسي
            # تحويل البيانات إلى نسب مئوية للمقارنة
            max_price = competitive_df['price_per_sqm'].max()
            min_price = competitive_df['price_per_sqm'].min()
            price_range = max_price - min_price
            
            max_delivery = competitive_df['delivery_time'].max()
            min_delivery = competitive_df['delivery_time'].min()
            delivery_range = max_delivery - min_delivery
            
            # ملاحظة: نقوم بعكس مقياس السعر ومدة التسليم لأن القيم الأقل أفضل
            normalized_price = 100 - ((our_company['price_per_sqm'] - min_price) / price_range * 100) if price_range > 0 else 50
            normalized_delivery = 100 - ((our_company['delivery_time'] - min_delivery) / delivery_range * 100) if delivery_range > 0 else 50
            normalized_quality = (our_company['quality_rating'] / 5) * 100
            normalized_market_share = (our_company['market_share'] / competitive_df['market_share'].max()) * 100
            
            # إنشاء رسم بياني راداري
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=[normalized_price, normalized_delivery, normalized_quality, normalized_market_share],
                theta=['السعر التنافسي', 'سرعة التسليم', 'الجودة', 'الحصة السوقية'],
                fill='toself',
                name='شركتنا'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                title='تحليل الموقع التنافسي لشركتنا'
            )
            
            st.plotly_chart(fig, use_container_width=True)
