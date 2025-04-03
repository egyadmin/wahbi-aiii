"""
وحدة الإشعارات الذكية - نظام تحليل المناقصات
"""

import streamlit as st
import pandas as pd
import datetime
import json
import os
import sys
from pathlib import Path

# إضافة مسار المشروع للنظام
sys.path.append(str(Path(__file__).parent.parent))

# استيراد محسن واجهة المستخدم
from styling.enhanced_ui import UIEnhancer

class NotificationsApp:
    """تطبيق الإشعارات الذكية"""
    
    def __init__(self):
        """تهيئة تطبيق الإشعارات الذكية"""
        self.ui = UIEnhancer(page_title="الإشعارات الذكية - نظام تحليل المناقصات", page_icon="🔔")
        
        # تهيئة متغير السمة في حالة الجلسة إذا لم يكن موجوداً
        if 'theme' not in st.session_state:
            st.session_state.theme = 'light'
            
        self.ui.apply_theme_colors()
        
        # بيانات الإشعارات (نموذجية)
        self.notifications_data = [
            {
                "id": "N001",
                "title": "موعد تسليم مناقصة",
                "message": "موعد تسليم مناقصة T-2025-001 (إنشاء مبنى إداري) بعد 5 أيام",
                "type": "deadline",
                "priority": "high",
                "related_entity": "T-2025-001",
                "created_at": "2025-03-25T10:30:00",
                "is_read": False
            },
            {
                "id": "N002",
                "title": "ترسية مناقصة",
                "message": "تم ترسية مناقصة T-2025-003 (توريد معدات) بنجاح",
                "type": "award",
                "priority": "medium",
                "related_entity": "T-2025-003",
                "created_at": "2025-03-28T14:15:00",
                "is_read": True
            },
            {
                "id": "N003",
                "title": "تحديث مستندات",
                "message": "تم تحديث مستندات مناقصة T-2025-002 (صيانة طرق)",
                "type": "document",
                "priority": "medium",
                "related_entity": "T-2025-002",
                "created_at": "2025-03-29T09:45:00",
                "is_read": False
            },
            {
                "id": "N004",
                "title": "تغيير في المواصفات",
                "message": "تم تغيير المواصفات الفنية لمناقصة T-2025-001 (إنشاء مبنى إداري)",
                "type": "change",
                "priority": "high",
                "related_entity": "T-2025-001",
                "created_at": "2025-03-27T11:20:00",
                "is_read": False
            },
            {
                "id": "N005",
                "title": "تأخير في المشروع",
                "message": "تأخير في تنفيذ مشروع P002 (تطوير طريق الملك فهد - جدة)",
                "type": "delay",
                "priority": "high",
                "related_entity": "P002",
                "created_at": "2025-03-26T16:10:00",
                "is_read": True
            },
            {
                "id": "N006",
                "title": "اكتمال مرحلة",
                "message": "اكتمال مرحلة الأساسات في مشروع P001 (إنشاء مبنى إداري - الرياض)",
                "type": "milestone",
                "priority": "low",
                "related_entity": "P001",
                "created_at": "2025-03-24T13:30:00",
                "is_read": True
            },
            {
                "id": "N007",
                "title": "طلب معلومات إضافية",
                "message": "طلب معلومات إضافية لمناقصة T-2025-004 (تجهيز مختبرات)",
                "type": "request",
                "priority": "medium",
                "related_entity": "T-2025-004",
                "created_at": "2025-03-30T08:15:00",
                "is_read": False
            },
            {
                "id": "N008",
                "title": "تحديث أسعار المواد",
                "message": "تم تحديث أسعار مواد البناء في قاعدة البيانات",
                "type": "update",
                "priority": "low",
                "related_entity": "DB-MATERIALS",
                "created_at": "2025-03-29T15:40:00",
                "is_read": False
            },
            {
                "id": "N009",
                "title": "اجتماع فريق العمل",
                "message": "اجتماع فريق العمل لمناقشة مناقصة T-2025-001 غداً الساعة 10:00 صباحاً",
                "type": "meeting",
                "priority": "medium",
                "related_entity": "T-2025-001",
                "created_at": "2025-03-28T16:20:00",
                "is_read": True
            },
            {
                "id": "N010",
                "title": "تغيير في الميزانية",
                "message": "تم تغيير الميزانية المخصصة لمشروع P004 (بناء مدرسة - أبها)",
                "type": "budget",
                "priority": "high",
                "related_entity": "P004",
                "created_at": "2025-03-25T14:50:00",
                "is_read": False
            }
        ]
        
        # إعدادات الإشعارات (نموذجية)
        self.notification_settings = {
            "deadline": True,
            "award": True,
            "document": True,
            "change": True,
            "delay": True,
            "milestone": True,
            "request": True,
            "update": True,
            "meeting": True,
            "budget": True,
            "email_notifications": True,
            "sms_notifications": False,
            "push_notifications": True,
            "notification_frequency": "realtime"
        }
    
    def run(self):
        """تشغيل تطبيق الإشعارات الذكية"""
        # إضافة زر تبديل السمة في أعلى الصفحة
        col1, col2, col3 = st.columns([1, 8, 1])
        with col3:
            if st.button("🌓 تبديل السمة"):
                # تبديل السمة
                if st.session_state.theme == "light":
                    st.session_state.theme = "dark"
                else:
                    st.session_state.theme = "light"
                
                # تطبيق السمة الجديدة
                self.ui.theme_mode = st.session_state.theme
                self.ui.apply_theme_colors()
                st.rerun()
        
        # إنشاء ترويسة الصفحة
        self.ui.create_header("الإشعارات الذكية", "إدارة ومتابعة الإشعارات والتنبيهات")
        
        # إنشاء علامات تبويب للوظائف المختلفة
        tabs = st.tabs(["الإشعارات الحالية", "إعدادات الإشعارات", "إنشاء إشعار", "سجل الإشعارات"])
        
        # علامة تبويب الإشعارات الحالية
        with tabs[0]:
            self.show_current_notifications()
        
        # علامة تبويب إعدادات الإشعارات
        with tabs[1]:
            self.show_notification_settings()
        
        # علامة تبويب إنشاء إشعار
        with tabs[2]:
            self.create_notification()
        
        # علامة تبويب سجل الإشعارات
        with tabs[3]:
            self.show_notification_history()
    
    def show_current_notifications(self):
        """عرض الإشعارات الحالية"""
        st.markdown("### الإشعارات الحالية")
        
        # إنشاء فلاتر للإشعارات
        col1, col2, col3 = st.columns(3)
        
        with col1:
            type_filter = st.multiselect(
                "نوع الإشعار",
                options=["الكل", "موعد نهائي", "ترسية", "مستند", "تغيير", "تأخير", "مرحلة", "طلب", "تحديث", "اجتماع", "ميزانية"],
                default=["الكل"]
            )
        
        with col2:
            priority_filter = st.multiselect(
                "الأولوية",
                options=["الكل", "عالية", "متوسطة", "منخفضة"],
                default=["الكل"]
            )
        
        with col3:
            read_filter = st.radio(
                "الحالة",
                options=["الكل", "غير مقروءة", "مقروءة"],
                horizontal=True
            )
        
        # تطبيق الفلاتر
        filtered_notifications = self.notifications_data
        
        # تحويل أنواع الإشعارات من الإنجليزية إلى العربية للفلترة
        type_mapping = {
            "موعد نهائي": "deadline",
            "ترسية": "award",
            "مستند": "document",
            "تغيير": "change",
            "تأخير": "delay",
            "مرحلة": "milestone",
            "طلب": "request",
            "تحديث": "update",
            "اجتماع": "meeting",
            "ميزانية": "budget"
        }
        
        # تحويل الأولويات من العربية إلى الإنجليزية للفلترة
        priority_mapping = {
            "عالية": "high",
            "متوسطة": "medium",
            "منخفضة": "low"
        }
        
        if "الكل" not in type_filter and type_filter:
            filtered_types = [type_mapping[t] for t in type_filter if t in type_mapping]
            filtered_notifications = [n for n in filtered_notifications if n["type"] in filtered_types]
        
        if "الكل" not in priority_filter and priority_filter:
            filtered_priorities = [priority_mapping[p] for p in priority_filter if p in priority_mapping]
            filtered_notifications = [n for n in filtered_notifications if n["priority"] in filtered_priorities]
        
        if read_filter == "غير مقروءة":
            filtered_notifications = [n for n in filtered_notifications if not n["is_read"]]
        elif read_filter == "مقروءة":
            filtered_notifications = [n for n in filtered_notifications if n["is_read"]]
        
        # عرض عدد الإشعارات غير المقروءة
        unread_count = len([n for n in filtered_notifications if not n["is_read"]])
        
        st.markdown(f"**عدد الإشعارات غير المقروءة:** {unread_count}")
        
        # زر تحديث وتعليم الكل كمقروء
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("تحديث الإشعارات", use_container_width=True):
                st.success("تم تحديث الإشعارات بنجاح")
        
        with col2:
            if st.button("تعليم الكل كمقروء", use_container_width=True):
                st.success("تم تعليم جميع الإشعارات كمقروءة")
        
        # عرض الإشعارات
        if not filtered_notifications:
            st.info("لا توجد إشعارات تطابق الفلاتر المحددة")
        else:
            for notification in filtered_notifications:
                self.display_notification(notification)
    
    def display_notification(self, notification):
        """عرض إشعار واحد"""
        # تحديد لون الإشعار بناءً على الأولوية
        if notification["priority"] == "high":
            color = self.ui.COLORS['danger']
            priority_text = "عالية"
        elif notification["priority"] == "medium":
            color = self.ui.COLORS['warning']
            priority_text = "متوسطة"
        else:
            color = self.ui.COLORS['secondary']
            priority_text = "منخفضة"
        
        # تحويل نوع الإشعار إلى العربية
        type_mapping = {
            "deadline": "موعد نهائي",
            "award": "ترسية",
            "document": "مستند",
            "change": "تغيير",
            "delay": "تأخير",
            "milestone": "مرحلة",
            "request": "طلب",
            "update": "تحديث",
            "meeting": "اجتماع",
            "budget": "ميزانية"
        }
        
        notification_type = type_mapping.get(notification["type"], notification["type"])
        
        # تحويل التاريخ إلى تنسيق مناسب
        created_at = datetime.datetime.fromisoformat(notification["created_at"])
        formatted_date = created_at.strftime("%Y-%m-%d %H:%M")
        
        # تحديد أيقونة الإشعار
        icon_mapping = {
            "deadline": "⏰",
            "award": "🏆",
            "document": "📄",
            "change": "🔄",
            "delay": "⚠️",
            "milestone": "🏁",
            "request": "❓",
            "update": "🔄",
            "meeting": "👥",
            "budget": "💰"
        }
        
        icon = icon_mapping.get(notification["type"], "📌")
        
        # إنشاء بطاقة الإشعار
        st.markdown(
            f"""
            <div style="border-left: 5px solid {color}; padding: 10px; margin-bottom: 10px; background-color: {'#f8f9fa' if st.session_state.theme == 'light' else '#2b2b2b'}; border-radius: 5px; {'opacity: 0.7;' if notification['is_read'] else ''}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0;">{icon} {notification['title']}</h4>
                        <p style="margin: 5px 0;">{notification['message']}</p>
                        <div style="display: flex; gap: 10px; font-size: 0.8em; color: {'#6c757d' if st.session_state.theme == 'light' else '#adb5bd'};">
                            <span>النوع: {notification_type}</span>
                            <span>الأولوية: {priority_text}</span>
                            <span>التاريخ: {formatted_date}</span>
                        </div>
                    </div>
                    <div>
                        <button style="background: none; border: none; cursor: pointer; color: {'#6c757d' if st.session_state.theme == 'light' else '#adb5bd'};">✓</button>
                        <button style="background: none; border: none; cursor: pointer; color: {'#6c757d' if st.session_state.theme == 'light' else '#adb5bd'};">🗑️</button>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    def show_notification_settings(self):
        """عرض إعدادات الإشعارات"""
        st.markdown("### إعدادات الإشعارات")
        
        # إنشاء نموذج الإعدادات
        with st.form("notification_settings_form"):
            st.markdown("#### أنواع الإشعارات")
            
            col1, col2 = st.columns(2)
            
            with col1:
                deadline = st.checkbox("المواعيد النهائية", value=self.notification_settings["deadline"])
                award = st.checkbox("ترسية المناقصات", value=self.notification_settings["award"])
                document = st.checkbox("تحديثات المستندات", value=self.notification_settings["document"])
                change = st.checkbox("التغييرات في المواصفات", value=self.notification_settings["change"])
                delay = st.checkbox("التأخيرات في المشاريع", value=self.notification_settings["delay"])
            
            with col2:
                milestone = st.checkbox("اكتمال المراحل", value=self.notification_settings["milestone"])
                request = st.checkbox("طلبات المعلومات", value=self.notification_settings["request"])
                update = st.checkbox("تحديثات النظام", value=self.notification_settings["update"])
                meeting = st.checkbox("الاجتماعات", value=self.notification_settings["meeting"])
                budget = st.checkbox("تغييرات الميزانية", value=self.notification_settings["budget"])
            
            st.markdown("#### طرق الإشعار")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                email_notifications = st.checkbox("البريد الإلكتروني", value=self.notification_settings["email_notifications"])
            
            with col2:
                sms_notifications = st.checkbox("الرسائل النصية", value=self.notification_settings["sms_notifications"])
            
            with col3:
                push_notifications = st.checkbox("إشعارات الويب", value=self.notification_settings["push_notifications"])
            
            st.markdown("#### تكرار الإشعارات")
            
            notification_frequency = st.radio(
                "تكرار الإشعارات",
                options=["في الوقت الحقيقي", "مرة واحدة يومياً", "مرة واحدة أسبوعياً"],
                index=0 if self.notification_settings["notification_frequency"] == "realtime" else 1 if self.notification_settings["notification_frequency"] == "daily" else 2,
                horizontal=True
            )
            
            # زر حفظ الإعدادات
            submit_button = st.form_submit_button("حفظ الإعدادات")
            
            if submit_button:
                # تحديث الإعدادات (في تطبيق حقيقي، سيتم حفظ الإعدادات في قاعدة البيانات)
                self.notification_settings.update({
                    "deadline": deadline,
                    "award": award,
                    "document": document,
                    "change": change,
                    "delay": delay,
                    "milestone": milestone,
                    "request": request,
                    "update": update,
                    "meeting": meeting,
                    "budget": budget,
                    "email_notifications": email_notifications,
                    "sms_notifications": sms_notifications,
                    "push_notifications": push_notifications,
                    "notification_frequency": "realtime" if notification_frequency == "في الوقت الحقيقي" else "daily" if notification_frequency == "مرة واحدة يومياً" else "weekly"
                })
                
                st.success("تم حفظ الإعدادات بنجاح")
        
        # إعدادات متقدمة
        st.markdown("### إعدادات متقدمة")
        
        with st.expander("إعدادات متقدمة"):
            st.markdown("#### جدولة الإشعارات")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.time_input("وقت الإشعارات اليومية", datetime.time(9, 0))
            
            with col2:
                st.selectbox(
                    "يوم الإشعارات الأسبوعية",
                    options=["الأحد", "الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت"],
                    index=0
                )
            
            st.markdown("#### فلترة الإشعارات")
            
            min_priority = st.select_slider(
                "الحد الأدنى للأولوية",
                options=["منخفضة", "متوسطة", "عالية"],
                value="منخفضة"
            )
            
            st.markdown("#### حفظ الإشعارات")
            
            retention_period = st.slider(
                "فترة الاحتفاظ بالإشعارات (بالأيام)",
                min_value=7,
                max_value=365,
                value=90,
                step=1
            )
            
            if st.button("حفظ الإعدادات المتقدمة"):
                st.success("تم حفظ الإعدادات المتقدمة بنجاح")
    
    def create_notification(self):
        """إنشاء إشعار جديد"""
        st.markdown("### إنشاء إشعار جديد")
        
        # إنشاء نموذج إشعار جديد
        with st.form("new_notification_form"):
            title = st.text_input("عنوان الإشعار")
            message = st.text_area("نص الإشعار")
            
            col1, col2 = st.columns(2)
            
            with col1:
                notification_type = st.selectbox(
                    "نوع الإشعار",
                    options=["موعد نهائي", "ترسية", "مستند", "تغيير", "تأخير", "مرحلة", "طلب", "تحديث", "اجتماع", "ميزانية"]
                )
                
                # تحويل نوع الإشعار إلى الإنجليزية
                type_mapping = {
                    "موعد نهائي": "deadline",
                    "ترسية": "award",
                    "مستند": "document",
                    "تغيير": "change",
                    "تأخير": "delay",
                    "مرحلة": "milestone",
                    "طلب": "request",
                    "تحديث": "update",
                    "اجتماع": "meeting",
                    "ميزانية": "budget"
                }
                
                notification_type_en = type_mapping.get(notification_type, "deadline")
                
                priority = st.selectbox(
                    "الأولوية",
                    options=["عالية", "متوسطة", "منخفضة"]
                )
                
                # تحويل الأولوية إلى الإنجليزية
                priority_mapping = {
                    "عالية": "high",
                    "متوسطة": "medium",
                    "منخفضة": "low"
                }
                
                priority_en = priority_mapping.get(priority, "medium")
            
            with col2:
                related_entity = st.text_input("الكيان المرتبط (مثل: رقم المناقصة، رقم المشروع)")
                
                notification_date = st.date_input(
                    "تاريخ الإشعار",
                    value=datetime.datetime.now().date()
                )
                
                notification_time = st.time_input(
                    "وقت الإشعار",
                    value=datetime.datetime.now().time()
                )
            
            # زر إنشاء الإشعار
            submit_button = st.form_submit_button("إنشاء الإشعار")
            
            if submit_button and title and message:
                # إنشاء إشعار جديد (في تطبيق حقيقي، سيتم حفظ الإشعار في قاعدة البيانات)
                new_id = f"N{len(self.notifications_data) + 1:03d}"
                
                # تحويل التاريخ والوقت إلى تنسيق ISO
                notification_datetime = datetime.datetime.combine(notification_date, notification_time)
                notification_datetime_iso = notification_datetime.isoformat()
                
                # إضافة الإشعار الجديد إلى قائمة الإشعارات
                self.notifications_data.append({
                    "id": new_id,
                    "title": title,
                    "message": message,
                    "type": notification_type_en,
                    "priority": priority_en,
                    "related_entity": related_entity,
                    "created_at": notification_datetime_iso,
                    "is_read": False
                })
                
                st.success("تم إنشاء الإشعار بنجاح")
                
                # عرض الإشعار الجديد
                st.markdown("### الإشعار الجديد")
                self.display_notification(self.notifications_data[-1])
        
        # إنشاء إشعارات متعددة
        st.markdown("### إنشاء إشعارات متعددة")
        
        with st.expander("إنشاء إشعارات متعددة"):
            st.markdown("#### تحميل ملف إشعارات")
            
            uploaded_file = st.file_uploader("قم بتحميل ملف إشعارات (CSV, JSON)", type=["csv", "json"])
            
            if uploaded_file is not None:
                if st.button("استيراد الإشعارات"):
                    st.success("تم استيراد الإشعارات بنجاح")
            
            st.markdown("#### إنشاء إشعارات من قالب")
            
            template_type = st.selectbox(
                "نوع القالب",
                options=["إشعارات المواعيد النهائية", "إشعارات الاجتماعات", "إشعارات التحديثات"]
            )
            
            if st.button("إنشاء إشعارات من القالب"):
                st.success("تم إنشاء الإشعارات من القالب بنجاح")
    
    def show_notification_history(self):
        """عرض سجل الإشعارات"""
        st.markdown("### سجل الإشعارات")
        
        # إنشاء فلاتر للسجل
        col1, col2 = st.columns(2)
        
        with col1:
            date_range = st.date_input(
                "نطاق التاريخ",
                value=(
                    datetime.datetime.now().date() - datetime.timedelta(days=30),
                    datetime.datetime.now().date()
                )
            )
        
        with col2:
            entity_filter = st.text_input("الكيان المرتبط")
        
        # تحويل البيانات إلى DataFrame
        notifications_df = pd.DataFrame(self.notifications_data)
        
        # تحويل عمود التاريخ إلى نوع datetime
        notifications_df["created_at"] = pd.to_datetime(notifications_df["created_at"])
        
        # تطبيق فلتر التاريخ
        if len(date_range) == 2:
            start_date, end_date = date_range
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
            
            notifications_df = notifications_df[
                (notifications_df["created_at"] >= start_date) &
                (notifications_df["created_at"] <= end_date)
            ]
        
        # تطبيق فلتر الكيان المرتبط
        if entity_filter:
            notifications_df = notifications_df[
                notifications_df["related_entity"].str.contains(entity_filter, case=False)
            ]
        
        # تحويل أنواع الإشعارات من الإنجليزية إلى العربية
        type_mapping = {
            "deadline": "موعد نهائي",
            "award": "ترسية",
            "document": "مستند",
            "change": "تغيير",
            "delay": "تأخير",
            "milestone": "مرحلة",
            "request": "طلب",
            "update": "تحديث",
            "meeting": "اجتماع",
            "budget": "ميزانية"
        }
        
        notifications_df["type_ar"] = notifications_df["type"].map(type_mapping)
        
        # تحويل الأولويات من الإنجليزية إلى العربية
        priority_mapping = {
            "high": "عالية",
            "medium": "متوسطة",
            "low": "منخفضة"
        }
        
        notifications_df["priority_ar"] = notifications_df["priority"].map(priority_mapping)
        
        # تحويل حالة القراءة إلى نص
        notifications_df["is_read_text"] = notifications_df["is_read"].map({True: "مقروءة", False: "غير مقروءة"})
        
        # تنسيق عمود التاريخ
        notifications_df["created_at_formatted"] = notifications_df["created_at"].dt.strftime("%Y-%m-%d %H:%M")
        
        # إنشاء DataFrame للعرض
        display_df = notifications_df[[
            "id", "title", "type_ar", "priority_ar", "related_entity",
            "created_at_formatted", "is_read_text"
        ]].rename(columns={
            "id": "الرقم",
            "title": "العنوان",
            "type_ar": "النوع",
            "priority_ar": "الأولوية",
            "related_entity": "الكيان المرتبط",
            "created_at_formatted": "التاريخ",
            "is_read_text": "الحالة"
        })
        
        # عرض الجدول
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # إحصائيات الإشعارات
        st.markdown("### إحصائيات الإشعارات")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_count = len(notifications_df)
            st.metric("إجمالي الإشعارات", total_count)
        
        with col2:
            read_count = len(notifications_df[notifications_df["is_read"] == True])
            st.metric("الإشعارات المقروءة", read_count)
        
        with col3:
            unread_count = len(notifications_df[notifications_df["is_read"] == False])
            st.metric("الإشعارات غير المقروءة", unread_count)
        
        # رسم بياني لتوزيع الإشعارات حسب النوع
        st.markdown("#### توزيع الإشعارات حسب النوع")
        
        type_counts = notifications_df["type_ar"].value_counts().reset_index()
        type_counts.columns = ["النوع", "العدد"]
        
        st.bar_chart(type_counts, x="النوع", y="العدد")
        
        # رسم بياني لتوزيع الإشعارات حسب الأولوية
        st.markdown("#### توزيع الإشعارات حسب الأولوية")
        
        priority_counts = notifications_df["priority_ar"].value_counts().reset_index()
        priority_counts.columns = ["الأولوية", "العدد"]
        
        st.bar_chart(priority_counts, x="الأولوية", y="العدد")
        
        # خيارات التصدير
        st.markdown("### تصدير البيانات")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("تصدير إلى CSV"):
                st.success("تم تصدير البيانات إلى CSV بنجاح")
        
        with col2:
            if st.button("تصدير إلى Excel"):
                st.success("تم تصدير البيانات إلى Excel بنجاح")
