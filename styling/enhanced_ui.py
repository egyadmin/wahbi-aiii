"""
محسن واجهة المستخدم - نظام تحليل المناقصات
"""

import streamlit as st
import pandas as pd
import numpy as np
import base64
from pathlib import Path
import os

class UIEnhancer:
    """فئة لتحسين واجهة المستخدم وتوحيد التصميم عبر النظام"""
    
    # ألوان النظام
    COLORS = {
        'primary': '#1E88E5',      # أزرق
        'secondary': '#5E35B1',    # بنفسجي
        'success': '#43A047',      # أخضر
        'warning': '#FB8C00',      # برتقالي
        'danger': '#E53935',       # أحمر
        'info': '#00ACC1',         # سماوي
        'light': '#F5F5F5',        # رمادي فاتح
        'dark': '#212121',         # رمادي داكن
        'accent': '#FF4081',       # وردي
        'background': '#FFFFFF',   # أبيض
        'text': '#212121',         # أسود
        'border': '#E0E0E0'        # رمادي حدود
    }
    
    # أحجام الخطوط
    FONT_SIZES = {
        'xs': '0.75rem',
        'sm': '0.875rem',
        'md': '1rem',
        'lg': '1.125rem',
        'xl': '1.25rem',
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
        '5xl': '3rem'
    }
    
    def __init__(self, page_title="نظام تحليل المناقصات", page_icon="📊"):
        """تهيئة محسن واجهة المستخدم"""
        self.page_title = page_title
        self.page_icon = page_icon
        self.theme_mode = "light"  # الوضع الافتراضي هو الوضع الفاتح
        
        # تهيئة متغير السمة في حالة الجلسة إذا لم يكن موجوداً
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'
    
    def apply_global_styles(self):
        """تطبيق التنسيقات العامة على الصفحة"""
        # تعريف CSS العام
        css = f"""
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');
        
        * {{
            font-family: 'Tajawal', sans-serif;
            direction: rtl;
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Tajawal', sans-serif;
            font-weight: 700;
            color: {self.COLORS['dark']};
        }}
        
        .module-title {{
            color: {self.COLORS['primary']};
            font-size: {self.FONT_SIZES['3xl']};
            margin-bottom: 1rem;
            border-bottom: 2px solid {self.COLORS['primary']};
            padding-bottom: 0.5rem;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2px;
        }}
        
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            background-color: {self.COLORS['light']};
            border-radius: 4px 4px 0 0;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
        }}
        
        .stTabs [aria-selected="true"] {{
            background-color: {self.COLORS['primary']};
            color: white;
        }}
        
        div[data-testid="stSidebarNav"] li div a span {{
            direction: rtl;
            text-align: right;
            font-family: 'Tajawal', sans-serif;
        }}
        
        div[data-testid="stSidebarNav"] {{
            background-color: {self.COLORS['light']};
        }}
        
        div[data-testid="stSidebarNav"] li div {{
            margin-right: 0;
            margin-left: auto;
        }}
        
        div[data-testid="stSidebarNav"] li div a {{
            padding-right: 10px;
            padding-left: 0;
        }}
        
        div[data-testid="stSidebarNav"] li div a:hover {{
            background-color: {self.COLORS['primary'] + '20'};
        }}
        
        div[data-testid="stSidebarNav"] li div[aria-selected="true"] {{
            background-color: {self.COLORS['primary'] + '40'};
        }}
        
        div[data-testid="stSidebarNav"] li div[aria-selected="true"] a span {{
            color: {self.COLORS['primary']};
            font-weight: 500;
        }}
        
        .metric-card {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-5px);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin: 10px 0;
        }}
        
        .metric-label {{
            font-size: 1rem;
            color: #666;
        }}
        
        .metric-change {{
            font-size: 0.9rem;
            margin-top: 5px;
        }}
        
        .metric-change-positive {{
            color: {self.COLORS['success']};
        }}
        
        .metric-change-negative {{
            color: {self.COLORS['danger']};
        }}
        
        .custom-button {{
            background-color: {self.COLORS['primary']};
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 1rem;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }}
        
        .custom-button:hover {{
            background-color: {self.COLORS['secondary']};
        }}
        
        .custom-card {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }}
        
        .header-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 1px solid {self.COLORS['border']};
        }}
        
        .header-title {{
            color: {self.COLORS['primary']};
            font-size: {self.FONT_SIZES['3xl']};
            margin: 0;
        }}
        
        .header-subtitle {{
            color: {self.COLORS['dark']};
            font-size: {self.FONT_SIZES['lg']};
            margin: 0;
        }}
        
        .header-actions {{
            display: flex;
            gap: 10px;
        }}
        
        /* تنسيق الجداول */
        div[data-testid="stTable"] table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        div[data-testid="stTable"] thead tr th {{
            background-color: {self.COLORS['primary']};
            color: white;
            text-align: right;
            padding: 12px;
        }}
        
        div[data-testid="stTable"] tbody tr:nth-child(even) {{
            background-color: {self.COLORS['light']};
        }}
        
        div[data-testid="stTable"] tbody tr:hover {{
            background-color: {self.COLORS['primary'] + '10'};
        }}
        
        div[data-testid="stTable"] tbody tr td {{
            padding: 10px;
            text-align: right;
        }}
        
        /* تنسيق النماذج */
        div[data-testid="stForm"] {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        
        button[kind="primaryFormSubmit"] {{
            background-color: {self.COLORS['primary']};
            color: white;
        }}
        
        button[kind="secondaryFormSubmit"] {{
            background-color: {self.COLORS['light']};
            color: {self.COLORS['dark']};
            border: 1px solid {self.COLORS['border']};
        }}
        
        /* تنسيق الرسوم البيانية */
        div[data-testid="stVegaLiteChart"] {{
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        """
        
        # تطبيق CSS
        st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    
    def apply_theme_colors(self):
        """تطبيق ألوان السمة الحالية"""
        # تحديد ألوان السمة بناءً على الوضع
        if self.theme_mode == "dark":
            self.COLORS['background'] = '#121212'
            self.COLORS['text'] = '#FFFFFF'
            self.COLORS['border'] = '#333333'
        else:
            self.COLORS['background'] = '#FFFFFF'
            self.COLORS['text'] = '#212121'
            self.COLORS['border'] = '#E0E0E0'
        
        # تطبيق CSS للسمة
        theme_css = f"""
        body {{
            background-color: {self.COLORS['background']};
            color: {self.COLORS['text']};
        }}
        """
        
        st.markdown(f'<style>{theme_css}</style>', unsafe_allow_html=True)
    
    def toggle_theme(self):
        """تبديل وضع السمة بين الفاتح والداكن"""
        if self.theme_mode == "light":
            self.theme_mode = "dark"
        else:
            self.theme_mode = "light"
        
        self.apply_theme_colors()
    
    def create_sidebar(self, menu_items):
        """إنشاء الشريط الجانبي مع قائمة العناصر"""
        with st.sidebar:
            # إضافة الشعار
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <h2 style="color: {self.COLORS['primary']};">{self.page_icon} {self.page_title}</h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # إضافة معلومات المستخدم
            st.markdown(
                f"""
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="width: 60px; height: 60px; border-radius: 50%; background-color: {self.COLORS['primary']}; color: white; display: flex; align-items: center; justify-content: center; margin: 0 auto; font-size: 24px; font-weight: bold;">
                        م
                    </div>
                    <p style="margin-top: 10px; font-weight: bold;">مهندس تامر الجوهري</p>
                    <p style="margin-top: -15px; font-size: 0.8rem; color: #666;">مدير المشاريع</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            st.divider()
            
            # إنشاء القائمة
            selected = st.radio(
                "القائمة الرئيسية",
                [item["name"] for item in menu_items],
                format_func=lambda x: x,
                label_visibility="collapsed"
            )
            
            st.divider()
            
            # إضافة معلومات النظام
            st.markdown(
                """
                <div style="position: absolute; bottom: 20px; left: 20px; right: 20px; text-align: center;">
                    <p style="font-size: 0.8rem; color: #666;">نظام تحليل المناقصات | الإصدار 2.0.0</p>
                    <p style="font-size: 0.7rem; color: #888;">© 2025 جميع الحقوق محفوظة</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        return selected
    
    def create_header(self, title, subtitle=None, show_actions=True):
        """إنشاء ترويسة الصفحة"""
        # إنشاء معرفات فريدة للأزرار
        add_button_key = f"add_button_{title}"
        update_button_key = f"update_button_{title}"
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f'<h1 class="header-title">{title}</h1>', unsafe_allow_html=True)
            if subtitle:
                st.markdown(f'<p class="header-subtitle">{subtitle}</p>', unsafe_allow_html=True)
        
        if show_actions:
            with col2:
                col2_1, col2_2 = st.columns(2)
                with col2_1:
                    st.button("إضافة جديد", key=add_button_key)
                with col2_2:
                    st.button("تحديث", key=update_button_key)
        
        st.divider()
    
    def create_metric_card(self, label, value, change=None, color=None):
        """إنشاء بطاقة مقياس"""
        if color is None:
            color = self.COLORS['primary']
        
        change_html = ""
        if change is not None:
            if change.startswith("+"):
                change_class = "metric-change-positive"
                change_icon = "↑"
            elif change.startswith("-"):
                change_class = "metric-change-negative"
                change_icon = "↓"
            else:
                change_class = ""
                change_icon = ""
            
            change_html = f'<div class="metric-change {change_class}">{change_icon} {change}</div>'
        
        st.markdown(
            f"""
            <div class="metric-card" style="border-top: 4px solid {color};">
                <div class="metric-label">{label}</div>
                <div class="metric-value" style="color: {color};">{value}</div>
                {change_html}
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def create_card(self, title, content, color=None):
        """إنشاء بطاقة عامة"""
        if color is None:
            color = self.COLORS['primary']
        
        st.markdown(
            f"""
            <div class="custom-card" style="border-top: 4px solid {color};">
                <h3 style="color: {color}; margin-top: 0;">{title}</h3>
                <div>{content}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def create_button(self, label, color=None, icon=None, key=None):
        """إنشاء زر مخصص"""
        if color is None:
            color = self.COLORS['primary']
        
        # إنشاء معرف فريد للزر إذا لم يتم توفيره
        if key is None:
            key = f"button_{label}_{hash(label)}"
        
        icon_html = f"{icon} " if icon else ""
        
        return st.button(
            f"{icon_html}{label}",
            key=key
        )
    
    def create_tabs(self, tab_names):
        """إنشاء تبويبات"""
        return st.tabs(tab_names)
    
    def create_expander(self, title, expanded=False, key=None):
        """إنشاء عنصر قابل للتوسيع"""
        # إنشاء معرف فريد للعنصر إذا لم يتم توفيره
        if key is None:
            key = f"expander_{title}_{hash(title)}"
        
        return st.expander(title, expanded=expanded, key=key)
    
    def create_data_table(self, data, use_container_width=True, hide_index=True):
        """إنشاء جدول بيانات"""
        return st.dataframe(data, use_container_width=use_container_width, hide_index=hide_index)
    
    def create_chart(self, chart_type, data, **kwargs):
        """إنشاء رسم بياني"""
        if chart_type == "bar":
            return st.bar_chart(data, **kwargs)
        elif chart_type == "line":
            return st.line_chart(data, **kwargs)
        elif chart_type == "area":
            return st.area_chart(data, **kwargs)
        else:
            return st.bar_chart(data, **kwargs)
    
    def create_form(self, title, key=None):
        """إنشاء نموذج"""
        # إنشاء معرف فريد للنموذج إذا لم يتم توفيره
        if key is None:
            key = f"form_{title}_{hash(title)}"
        
        return st.form(key=key)
    
    def create_file_uploader(self, label, types=None, key=None):
        """إنشاء أداة رفع الملفات"""
        # إنشاء معرف فريد لأداة رفع الملفات إذا لم يتم توفيره
        if key is None:
            key = f"file_uploader_{label}_{hash(label)}"
        
        return st.file_uploader(label, type=types, key=key)
    
    def create_date_input(self, label, value=None, key=None):
        """إنشاء حقل إدخال تاريخ"""
        # إنشاء معرف فريد لحقل إدخال التاريخ إذا لم يتم توفيره
        if key is None:
            key = f"date_input_{label}_{hash(label)}"
        
        return st.date_input(label, value=value, key=key)
    
    def create_select_box(self, label, options, index=0, key=None):
        """إنشاء قائمة منسدلة"""
        # إنشاء معرف فريد للقائمة المنسدلة إذا لم يتم توفيره
        if key is None:
            key = f"select_box_{label}_{hash(label)}"
        
        return st.selectbox(label, options, index=index, key=key)
    
    def create_multi_select(self, label, options, default=None, key=None):
        """إنشاء قائمة اختيار متعدد"""
        # إنشاء معرف فريد لقائمة الاختيار المتعدد إذا لم يتم توفيره
        if key is None:
            key = f"multi_select_{label}_{hash(label)}"
        
        return st.multiselect(label, options, default=default, key=key)
    
    def create_slider(self, label, min_value, max_value, value=None, step=1, key=None):
        """إنشاء شريط تمرير"""
        # إنشاء معرف فريد لشريط التمرير إذا لم يتم توفيره
        if key is None:
            key = f"slider_{label}_{hash(label)}"
        
        return st.slider(label, min_value=min_value, max_value=max_value, value=value, step=step, key=key)
    
    def create_text_input(self, label, value="", key=None):
        """إنشاء حقل إدخال نصي"""
        # إنشاء معرف فريد لحقل الإدخال النصي إذا لم يتم توفيره
        if key is None:
            key = f"text_input_{label}_{hash(label)}"
        
        return st.text_input(label, value=value, key=key)
    
    def create_text_area(self, label, value="", height=None, key=None):
        """إنشاء منطقة نص"""
        # إنشاء معرف فريد لمنطقة النص إذا لم يتم توفيره
        if key is None:
            key = f"text_area_{label}_{hash(label)}"
        
        return st.text_area(label, value=value, height=height, key=key)
    
    def create_number_input(self, label, min_value=None, max_value=None, value=0, step=1, key=None):
        """إنشاء حقل إدخال رقمي"""
        # إنشاء معرف فريد لحقل الإدخال الرقمي إذا لم يتم توفيره
        if key is None:
            key = f"number_input_{label}_{hash(label)}"
        
        return st.number_input(label, min_value=min_value, max_value=max_value, value=value, step=step, key=key)
    
    def create_checkbox(self, label, value=False, key=None):
        """إنشاء خانة اختيار"""
        # إنشاء معرف فريد لخانة الاختيار إذا لم يتم توفيره
        if key is None:
            key = f"checkbox_{label}_{hash(label)}"
        
        return st.checkbox(label, value=value, key=key)
    
    def create_radio(self, label, options, index=0, key=None):
        """إنشاء أزرار راديو"""
        # إنشاء معرف فريد لأزرار الراديو إذا لم يتم توفيره
        if key is None:
            key = f"radio_{label}_{hash(label)}"
        
        return st.radio(label, options, index=index, key=key)
    
    def create_progress_bar(self, value, key=None):
        """إنشاء شريط تقدم"""
        # إنشاء معرف فريد لشريط التقدم إذا لم يتم توفيره
        if key is None:
            key = f"progress_bar_{value}_{hash(str(value))}"
        
        return st.progress(value, key=key)
    
    def create_spinner(self, text="جاري التحميل..."):
        """إنشاء مؤشر تحميل"""
        return st.spinner(text)
    
    def create_success_message(self, message):
        """إنشاء رسالة نجاح"""
        return st.success(message)
    
    def create_error_message(self, message):
        """إنشاء رسالة خطأ"""
        return st.error(message)
    
    def create_warning_message(self, message):
        """إنشاء رسالة تحذير"""
        return st.warning(message)
    
    def create_info_message(self, message):
        """إنشاء رسالة معلومات"""
        return st.info(message)
