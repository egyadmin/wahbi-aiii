"""
وحدة الخرائط والمواقع - نظام تحليل المناقصات
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import json
import os
import sys
from pathlib import Path

# إضافة مسار المشروع للنظام
sys.path.append(str(Path(__file__).parent.parent))

# استيراد محسن واجهة المستخدم
from styling.enhanced_ui import UIEnhancer

class MapsApp:
    """تطبيق الخرائط والمواقع"""
    
    def __init__(self):
        """تهيئة تطبيق الخرائط والمواقع"""
        self.ui = UIEnhancer(page_title="الخرائط والمواقع - نظام تحليل المناقصات", page_icon="🗺️")
        self.ui.apply_theme_colors()
        
        # بيانات المشاريع (نموذجية)
        self.projects_data = [
            {
                "id": "P001",
                "name": "إنشاء مبنى إداري - الرياض",
                "location": "الرياض",
                "coordinates": [24.7136, 46.6753],
                "status": "جاري التنفيذ",
                "budget": 15000000,
                "completion": 45,
                "client": "وزارة الإسكان",
                "start_date": "2024-10-15",
                "end_date": "2025-12-30"
            },
            {
                "id": "P002",
                "name": "تطوير طريق الملك فهد - جدة",
                "location": "جدة",
                "coordinates": [21.5433, 39.1728],
                "status": "قيد الدراسة",
                "budget": 8500000,
                "completion": 0,
                "client": "أمانة جدة",
                "start_date": "2025-05-01",
                "end_date": "2026-02-28"
            },
            {
                "id": "P003",
                "name": "إنشاء مجمع سكني - الدمام",
                "location": "الدمام",
                "coordinates": [26.4207, 50.0888],
                "status": "مكتمل",
                "budget": 22000000,
                "completion": 100,
                "client": "شركة الإسكان للتطوير",
                "start_date": "2023-08-10",
                "end_date": "2025-01-15"
            },
            {
                "id": "P004",
                "name": "بناء مدرسة - أبها",
                "location": "أبها",
                "coordinates": [18.2164, 42.5053],
                "status": "جاري التنفيذ",
                "budget": 5200000,
                "completion": 75,
                "client": "وزارة التعليم",
                "start_date": "2024-06-20",
                "end_date": "2025-07-30"
            },
            {
                "id": "P005",
                "name": "تطوير شبكة مياه - المدينة المنورة",
                "location": "المدينة المنورة",
                "coordinates": [24.5247, 39.5692],
                "status": "جاري التنفيذ",
                "budget": 12800000,
                "completion": 30,
                "client": "شركة المياه الوطنية",
                "start_date": "2024-11-05",
                "end_date": "2026-03-15"
            }
        ]
    
    def run(self):
        """تشغيل تطبيق الخرائط والمواقع"""
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
            {"name": "المساعد الذكي", "icon": "robot"},
            {"name": "التقارير", "icon": "bar-chart"},
            {"name": "الإعدادات", "icon": "gear"}
        ]
        
        # إنشاء الشريط الجانبي
        selected = self.ui.create_sidebar(menu_items)
        
        # إنشاء ترويسة الصفحة
        self.ui.create_header("الخرائط والمواقع", "عرض وإدارة مواقع المشاريع")
        
        # إنشاء علامات تبويب للوظائف المختلفة
        tabs = st.tabs(["خريطة المشاريع", "تفاصيل المواقع", "إضافة موقع جديد", "تحليل المناطق"])
        
        # علامة تبويب خريطة المشاريع
        with tabs[0]:
            self.show_projects_map()
        
        # علامة تبويب تفاصيل المواقع
        with tabs[1]:
            self.show_location_details()
        
        # علامة تبويب إضافة موقع جديد
        with tabs[2]:
            self.add_new_location()
        
        # علامة تبويب تحليل المناطق
        with tabs[3]:
            self.analyze_regions()
    
    def show_projects_map(self):
        """عرض خريطة المشاريع"""
        # إنشاء فلاتر للخريطة
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.multiselect(
                "حالة المشروع",
                options=["الكل", "جاري التنفيذ", "قيد الدراسة", "مكتمل"],
                default=["الكل"]
            )
        
        with col2:
            location_filter = st.multiselect(
                "الموقع",
                options=["الكل"] + list(set([p["location"] for p in self.projects_data])),
                default=["الكل"]
            )
        
        with col3:
            budget_range = st.slider(
                "نطاق الميزانية (مليون ريال)",
                0.0, 25.0, (0.0, 25.0),
                step=0.5
            )
        
        # تطبيق الفلاتر
        filtered_projects = self.projects_data
        
        if "الكل" not in status_filter and status_filter:
            filtered_projects = [p for p in filtered_projects if p["status"] in status_filter]
        
        if "الكل" not in location_filter and location_filter:
            filtered_projects = [p for p in filtered_projects if p["location"] in location_filter]
        
        filtered_projects = [p for p in filtered_projects if budget_range[0] * 1000000 <= p["budget"] <= budget_range[1] * 1000000]
        
        # إنشاء الخريطة
        st.markdown("### خريطة المشاريع")
        
        # تحديد مركز الخريطة (وسط المملكة العربية السعودية تقريباً)
        center = [24.0, 45.0]
        
        # إنشاء خريطة folium
        m = folium.Map(location=center, zoom_start=5, tiles="OpenStreetMap")
        
        # إضافة المشاريع إلى الخريطة
        for project in filtered_projects:
            # تحديد لون العلامة بناءً على حالة المشروع
            if project["status"] == "جاري التنفيذ":
                color = "blue"
            elif project["status"] == "قيد الدراسة":
                color = "orange"
            elif project["status"] == "مكتمل":
                color = "green"
            else:
                color = "gray"
            
            # إنشاء نص النافذة المنبثقة
            popup_text = f"""
            <div dir="rtl" style="text-align: right; width: 200px;">
                <h4>{project['name']}</h4>
                <p><strong>الحالة:</strong> {project['status']}</p>
                <p><strong>الميزانية:</strong> {project['budget']:,} ريال</p>
                <p><strong>نسبة الإنجاز:</strong> {project['completion']}%</p>
                <p><strong>العميل:</strong> {project['client']}</p>
                <p><strong>تاريخ البدء:</strong> {project['start_date']}</p>
                <p><strong>تاريخ الانتهاء:</strong> {project['end_date']}</p>
                <a href="#" onclick="alert('تم فتح تفاصيل المشروع');">عرض التفاصيل</a>
            </div>
            """
            
            # إضافة علامة للمشروع
            folium.Marker(
                location=project["coordinates"],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=project["name"],
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(m)
        
        # عرض الخريطة
        folium_static(m, width=1000, height=500)
        
        # عرض إحصائيات المشاريع
        st.markdown("### إحصائيات المشاريع")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            self.ui.create_metric_card(
                "إجمالي المشاريع",
                str(len(filtered_projects)),
                None,
                self.ui.COLORS['primary']
            )
        
        with col2:
            projects_in_progress = len([p for p in filtered_projects if p["status"] == "جاري التنفيذ"])
            self.ui.create_metric_card(
                "مشاريع جارية",
                str(projects_in_progress),
                None,
                self.ui.COLORS['secondary']
            )
        
        with col3:
            total_budget = sum([p["budget"] for p in filtered_projects])
            self.ui.create_metric_card(
                "إجمالي الميزانية",
                f"{total_budget/1000000:.1f} مليون ريال",
                None,
                self.ui.COLORS['accent']
            )
        
        with col4:
            avg_completion = np.mean([p["completion"] for p in filtered_projects])
            self.ui.create_metric_card(
                "متوسط نسبة الإنجاز",
                f"{avg_completion:.1f}%",
                None,
                self.ui.COLORS['success']
            )
    
    def show_location_details(self):
        """عرض تفاصيل المواقع"""
        st.markdown("### تفاصيل مواقع المشاريع")
        
        # إنشاء جدول بيانات المشاريع
        projects_df = pd.DataFrame(self.projects_data)
        projects_df = projects_df.rename(columns={
            "id": "رقم المشروع",
            "name": "اسم المشروع",
            "location": "الموقع",
            "status": "الحالة",
            "budget": "الميزانية (ريال)",
            "completion": "نسبة الإنجاز (%)",
            "client": "العميل",
            "start_date": "تاريخ البدء",
            "end_date": "تاريخ الانتهاء"
        })
        
        # حذف عمود الإحداثيات من العرض
        projects_df = projects_df.drop(columns=["coordinates"])
        
        # عرض الجدول
        st.dataframe(
            projects_df,
            use_container_width=True,
            hide_index=True
        )
        
        # إضافة خيار تصدير البيانات
        col1, col2 = st.columns([1, 5])
        with col1:
            self.ui.create_button("تصدير البيانات", "primary")
        
        # عرض تفاصيل مشروع محدد
        st.markdown("### تفاصيل مشروع محدد")
        
        selected_project = st.selectbox(
            "اختر مشروعاً لعرض التفاصيل",
            options=[p["name"] for p in self.projects_data]
        )
        
        # العثور على المشروع المحدد
        project = next((p for p in self.projects_data if p["name"] == selected_project), None)
        
        if project:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # عرض تفاصيل المشروع
                st.markdown(f"#### {project['name']}")
                st.markdown(f"**الموقع:** {project['location']}")
                st.markdown(f"**الحالة:** {project['status']}")
                st.markdown(f"**الميزانية:** {project['budget']:,} ريال")
                st.markdown(f"**نسبة الإنجاز:** {project['completion']}%")
                st.markdown(f"**العميل:** {project['client']}")
                st.markdown(f"**تاريخ البدء:** {project['start_date']}")
                st.markdown(f"**تاريخ الانتهاء:** {project['end_date']}")
                
                # أزرار الإجراءات
                col1, col2, col3 = st.columns(3)
                with col1:
                    self.ui.create_button("تعديل البيانات", "primary")
                with col2:
                    self.ui.create_button("عرض المستندات", "secondary")
                with col3:
                    self.ui.create_button("تقرير الموقع", "accent")
            
            with col2:
                # عرض خريطة مصغرة للمشروع
                m = folium.Map(location=project["coordinates"], zoom_start=12)
                folium.Marker(
                    location=project["coordinates"],
                    tooltip=project["name"],
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)
                folium_static(m, width=300, height=300)
    
    def add_new_location(self):
        """إضافة موقع جديد"""
        st.markdown("### إضافة موقع مشروع جديد")
        
        # نموذج إضافة موقع جديد
        with st.form("new_location_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                project_id = st.text_input("رقم المشروع", value="P00" + str(len(self.projects_data) + 1))
                project_name = st.text_input("اسم المشروع")
                location = st.text_input("الموقع")
                status = st.selectbox(
                    "الحالة",
                    options=["جاري التنفيذ", "قيد الدراسة", "مكتمل"]
                )
                budget = st.number_input("الميزانية (ريال)", min_value=0, step=100000)
            
            with col2:
                completion = st.slider("نسبة الإنجاز (%)", 0, 100, 0)
                client = st.text_input("العميل")
                start_date = st.date_input("تاريخ البدء")
                end_date = st.date_input("تاريخ الانتهاء")
            
            st.markdown("### تحديد الموقع على الخريطة")
            st.markdown("انقر على الخريطة لتحديد موقع المشروع أو أدخل الإحداثيات يدوياً")
            
            col1, col2 = st.columns(2)
            
            with col1:
                latitude = st.number_input("خط العرض", value=24.0, format="%.4f")
            
            with col2:
                longitude = st.number_input("خط الطول", value=45.0, format="%.4f")
            
            # عرض الخريطة لتحديد الموقع
            m = folium.Map(location=[latitude, longitude], zoom_start=5)
            folium.Marker(
                location=[latitude, longitude],
                tooltip="موقع المشروع الجديد",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)
            folium_static(m, width=700, height=300)
            
            # زر الإرسال
            submit_button = st.form_submit_button("إضافة المشروع")
            
            if submit_button:
                # إضافة المشروع الجديد (في تطبيق حقيقي، سيتم حفظ البيانات في قاعدة البيانات)
                st.success("تم إضافة المشروع بنجاح!")
                
                # إعادة تعيين النموذج
                st.experimental_rerun()
    
    def analyze_regions(self):
        """تحليل المناطق"""
        st.markdown("### تحليل المناطق")
        
        # إنشاء بيانات المناطق (نموذجية)
        regions_data = {
            "المنطقة": ["الرياض", "مكة المكرمة", "المدينة المنورة", "القصيم", "المنطقة الشرقية", "عسير", "تبوك", "حائل", "الحدود الشمالية", "جازان", "نجران", "الباحة", "الجوف"],
            "عدد المشاريع": [15, 12, 8, 5, 18, 7, 4, 3, 2, 6, 3, 2, 3],
            "إجمالي الميزانية (مليون ريال)": [120, 95, 45, 30, 150, 40, 25, 18, 12, 35, 20, 15, 22],
            "متوسط مدة المشروع (شهر)": [18, 16, 14, 12, 20, 15, 12, 10, 9, 14, 12, 10, 11]
        }
        
        regions_df = pd.DataFrame(regions_data)
        
        # عرض خريطة حرارية للمناطق
        st.markdown("#### توزيع المشاريع حسب المناطق")
        
        # في تطبيق حقيقي، يمكن استخدام خريطة حرارية حقيقية للمملكة
        st.image("https://via.placeholder.com/800x400?text=خريطة+حرارية+للمشاريع+حسب+المناطق", use_column_width=True)
        
        # عرض إحصائيات المناطق
        st.markdown("#### إحصائيات المناطق")
        
        # عرض الجدول
        st.dataframe(
            regions_df,
            use_container_width=True,
            hide_index=True
        )
        
        # عرض رسوم بيانية للمقارنة
        st.markdown("#### مقارنة المناطق")
        
        chart_type = st.radio(
            "نوع الرسم البياني",
            options=["عدد المشاريع", "إجمالي الميزانية", "متوسط مدة المشروع"],
            horizontal=True
        )
        
        if chart_type == "عدد المشاريع":
            chart_data = regions_df[["المنطقة", "عدد المشاريع"]].sort_values(by="عدد المشاريع", ascending=False)
            st.bar_chart(chart_data.set_index("المنطقة"))
        elif chart_type == "إجمالي الميزانية":
            chart_data = regions_df[["المنطقة", "إجمالي الميزانية (مليون ريال)"]].sort_values(by="إجمالي الميزانية (مليون ريال)", ascending=False)
            st.bar_chart(chart_data.set_index("المنطقة"))
        else:
            chart_data = regions_df[["المنطقة", "متوسط مدة المشروع (شهر)"]].sort_values(by="متوسط مدة المشروع (شهر)", ascending=False)
            st.bar_chart(chart_data.set_index("المنطقة"))
        
        # تحليل الكثافة
        st.markdown("#### تحليل كثافة المشاريع")
        st.markdown("""
        يوضح هذا التحليل توزيع المشاريع حسب المناطق الجغرافية، مما يساعد في:
        - تحديد المناطق ذات النشاط العالي
        - تحديد فرص النمو في المناطق الأقل نشاطاً
        - تخطيط الموارد بناءً على التوزيع الجغرافي
        """)
        
        # في تطبيق حقيقي، يمكن إضافة تحليلات أكثر تفصيلاً

# تشغيل التطبيق
if __name__ == "__main__":
    maps_app = MapsApp()
    maps_app.run()
