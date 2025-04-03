"""
وحدة تحليل السوق والأسعار التاريخية
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

class MarketAnalysis:
    def __init__(self):
        if 'market_data' not in st.session_state:
            self._initialize_market_data()

    def _initialize_market_data(self):
        st.session_state.market_data = {
            'price_indices': {},
            'historical_prices': {},
            'market_trends': {}
        }

    def render(self):
        st.header("تحليل السوق والأسعار")

        tabs = st.tabs([
            "مؤشرات الأسعار",
            "التحليل التاريخي",
            "اتجاهات السوق"
        ])

        with tabs[0]:
            self._render_price_indices()

        with tabs[1]:
            self._render_historical_analysis()

        with tabs[2]:
            self._render_market_trends()

    def _render_price_indices(self):
        st.subheader("مؤشرات الأسعار الرئيسية")

        # عرض مؤشرات المواد الرئيسية
        materials = {
            'الحديد': {'current': 3200, 'change': 5.2},
            'الأسمنت': {'current': 400, 'change': -2.1},
            'الخرسانة': {'current': 250, 'change': 1.5},
            'الأسفلت': {'current': 2800, 'change': 3.8}
        }

        cols = st.columns(4)
        for i, (material, data) in enumerate(materials.items()):
            with cols[i]:
                st.metric(
                    material,
                    f"{data['current']} ريال",
                    f"{data['change']}%"
                )

    def _render_historical_analysis(self):
        st.subheader("تحليل الأسعار التاريخي")

        # إنشاء بيانات تاريخية افتراضية
        dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
        materials = ['الحديد', 'الأسمنت', 'الخرسانة', 'الأسفلت']

        data = []
        for material in materials:
            base_price = 1000 if material == 'الحديد' else 500
            for date in dates:
                data.append({
                    'التاريخ': date,
                    'المادة': material,
                    'السعر': base_price * (1 + 0.1 * np.random.randn())
                })

        df = pd.DataFrame(data)

        # رسم بياني للأسعار التاريخية
        fig = px.line(
            df,
            x='التاريخ',
            y='السعر',
            color='المادة',
            title='تطور الأسعار خلال العام'
        )
        st.plotly_chart(fig)

    def _render_market_trends(self):
        st.subheader("اتجاهات السوق والتوقعات")

        # تحليل الاتجاهات
        trends = {
            'قصير المدى': {
                'الحديد': 'صعود',
                'الأسمنت': 'هبوط',
                'الخرسانة': 'ثبات',
                'الأسفلت': 'صعود'
            },
            'متوسط المدى': {
                'الحديد': 'ثبات',
                'الأسمنت': 'صعود',
                'الخرسانة': 'صعود',
                'الأسفلت': 'ثبات'
            },
            'طويل المدى': {
                'الحديد': 'صعود',
                'الأسمنت': 'صعود',
                'الخرسانة': 'صعود',
                'الأسفلت': 'صعود'
            }
        }

        st.dataframe(pd.DataFrame(trends))