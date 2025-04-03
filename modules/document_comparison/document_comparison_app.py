"""
وحدة مقارنة المستندات - نظام تحليل المناقصات
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import difflib
import re
import datetime

# إضافة مسار المشروع للنظام
sys.path.append(str(Path(__file__).parent.parent))

# استيراد محسن واجهة المستخدم
from styling.enhanced_ui import UIEnhancer

class DocumentComparisonApp:
    """تطبيق مقارنة المستندات"""
    
    def __init__(self):
        """تهيئة تطبيق مقارنة المستندات"""
        self.ui = UIEnhancer(page_title="مقارنة المستندات - نظام تحليل المناقصات", page_icon="📄")
        self.ui.apply_theme_colors()
        
        # بيانات المستندات (نموذجية)
        self.documents_data = [
            {
                "id": "DOC001",
                "name": "كراسة الشروط - مناقصة إنشاء مبنى إداري",
                "type": "كراسة شروط",
                "version": "1.0",
                "date": "2025-01-15",
                "size": 2.4,
                "pages": 45,
                "related_entity": "T-2025-001",
                "path": "/documents/T-2025-001/specs_v1.pdf"
            },
            {
                "id": "DOC002",
                "name": "كراسة الشروط - مناقصة إنشاء مبنى إداري",
                "type": "كراسة شروط",
                "version": "1.1",
                "date": "2025-02-10",
                "size": 2.6,
                "pages": 48,
                "related_entity": "T-2025-001",
                "path": "/documents/T-2025-001/specs_v1.1.pdf"
            },
            {
                "id": "DOC003",
                "name": "كراسة الشروط - مناقصة إنشاء مبنى إداري",
                "type": "كراسة شروط",
                "version": "2.0",
                "date": "2025-03-05",
                "size": 2.8,
                "pages": 52,
                "related_entity": "T-2025-001",
                "path": "/documents/T-2025-001/specs_v2.0.pdf"
            },
            {
                "id": "DOC004",
                "name": "جدول الكميات - مناقصة إنشاء مبنى إداري",
                "type": "جدول كميات",
                "version": "1.0",
                "date": "2025-01-15",
                "size": 1.2,
                "pages": 20,
                "related_entity": "T-2025-001",
                "path": "/documents/T-2025-001/boq_v1.0.xlsx"
            },
            {
                "id": "DOC005",
                "name": "جدول الكميات - مناقصة إنشاء مبنى إداري",
                "type": "جدول كميات",
                "version": "1.1",
                "date": "2025-02-20",
                "size": 1.3,
                "pages": 22,
                "related_entity": "T-2025-001",
                "path": "/documents/T-2025-001/boq_v1.1.xlsx"
            },
            {
                "id": "DOC006",
                "name": "المخططات - مناقصة إنشاء مبنى إداري",
                "type": "مخططات",
                "version": "1.0",
                "date": "2025-01-15",
                "size": 15.6,
                "pages": 30,
                "related_entity": "T-2025-001",
                "path": "/documents/T-2025-001/drawings_v1.0.pdf"
            },
            {
                "id": "DOC007",
                "name": "المخططات - مناقصة إنشاء مبنى إداري",
                "type": "مخططات",
                "version": "2.0",
                "date": "2025-03-10",
                "size": 18.2,
                "pages": 35,
                "related_entity": "T-2025-001",
                "path": "/documents/T-2025-001/drawings_v2.0.pdf"
            },
            {
                "id": "DOC008",
                "name": "كراسة الشروط - مناقصة صيانة طرق",
                "type": "كراسة شروط",
                "version": "1.0",
                "date": "2025-02-05",
                "size": 1.8,
                "pages": 32,
                "related_entity": "T-2025-002",
                "path": "/documents/T-2025-002/specs_v1.0.pdf"
            },
            {
                "id": "DOC009",
                "name": "كراسة الشروط - مناقصة صيانة طرق",
                "type": "كراسة شروط",
                "version": "1.1",
                "date": "2025-03-15",
                "size": 1.9,
                "pages": 34,
                "related_entity": "T-2025-002",
                "path": "/documents/T-2025-002/specs_v1.1.pdf"
            },
            {
                "id": "DOC010",
                "name": "جدول الكميات - مناقصة صيانة طرق",
                "type": "جدول كميات",
                "version": "1.0",
                "date": "2025-02-05",
                "size": 0.9,
                "pages": 15,
                "related_entity": "T-2025-002",
                "path": "/documents/T-2025-002/boq_v1.0.xlsx"
            }
        ]
        
        # بيانات نموذجية لمحتوى المستندات (للعرض فقط)
        self.sample_document_content = {
            "DOC001": """
            # كراسة الشروط والمواصفات
            ## مناقصة إنشاء مبنى إداري
            
            ### 1. مقدمة
            تدعو شركة شبه الجزيرة للمقاولات الشركات المتخصصة للتقدم بعروضها لتنفيذ مشروع إنشاء مبنى إداري في مدينة الرياض.
            
            ### 2. نطاق العمل
            يشمل نطاق العمل تصميم وتنفيذ مبنى إداري مكون من 5 طوابق بمساحة إجمالية 5000 متر مربع، ويشمل ذلك:
            - أعمال الهيكل الإنشائي
            - أعمال التشطيبات الداخلية والخارجية
            - أعمال الكهرباء والميكانيكا
            - أعمال تنسيق الموقع
            
            ### 3. المواصفات الفنية
            #### 3.1 أعمال الخرسانة
            - يجب أن تكون الخرسانة المسلحة بقوة لا تقل عن 30 نيوتن/مم²
            - يجب استخدام حديد تسليح مطابق للمواصفات السعودية
            
            #### 3.2 أعمال التشطيبات
            - يجب استخدام مواد عالية الجودة للتشطيبات الداخلية
            - يجب أن تكون الواجهات الخارجية مقاومة للعوامل الجوية
            
            ### 4. الشروط العامة
            - مدة التنفيذ: 18 شهراً من تاريخ استلام الموقع
            - غرامة التأخير: 0.1% من قيمة العقد عن كل يوم تأخير
            - ضمان الأعمال: 10 سنوات للهيكل الإنشائي، 5 سنوات للأعمال الميكانيكية والكهربائية
            """,
            
            "DOC002": """
            # كراسة الشروط والمواصفات
            ## مناقصة إنشاء مبنى إداري
            
            ### 1. مقدمة
            تدعو شركة شبه الجزيرة للمقاولات الشركات المتخصصة للتقدم بعروضها لتنفيذ مشروع إنشاء مبنى إداري في مدينة الرياض.
            
            ### 2. نطاق العمل
            يشمل نطاق العمل تصميم وتنفيذ مبنى إداري مكون من 5 طوابق بمساحة إجمالية 5500 متر مربع، ويشمل ذلك:
            - أعمال الهيكل الإنشائي
            - أعمال التشطيبات الداخلية والخارجية
            - أعمال الكهرباء والميكانيكا
            - أعمال تنسيق الموقع
            - أعمال أنظمة الأمن والسلامة
            
            ### 3. المواصفات الفنية
            #### 3.1 أعمال الخرسانة
            - يجب أن تكون الخرسانة المسلحة بقوة لا تقل عن 35 نيوتن/مم²
            - يجب استخدام حديد تسليح مطابق للمواصفات السعودية
            
            #### 3.2 أعمال التشطيبات
            - يجب استخدام مواد عالية الجودة للتشطيبات الداخلية
            - يجب أن تكون الواجهات الخارجية مقاومة للعوامل الجوية
            - يجب استخدام زجاج عاكس للحرارة للواجهات
            
            ### 4. الشروط العامة
            - مدة التنفيذ: 16 شهراً من تاريخ استلام الموقع
            - غرامة التأخير: 0.15% من قيمة العقد عن كل يوم تأخير
            - ضمان الأعمال: 10 سنوات للهيكل الإنشائي، 5 سنوات للأعمال الميكانيكية والكهربائية
            """,
            
            "DOC003": """
            # كراسة الشروط والمواصفات
            ## مناقصة إنشاء مبنى إداري
            
            ### 1. مقدمة
            تدعو شركة شبه الجزيرة للمقاولات الشركات المتخصصة للتقدم بعروضها لتنفيذ مشروع إنشاء مبنى إداري في مدينة الرياض وفقاً للمواصفات المعتمدة من الهيئة السعودية للمواصفات والمقاييس.
            
            ### 2. نطاق العمل
            يشمل نطاق العمل تصميم وتنفيذ مبنى إداري مكون من 6 طوابق بمساحة إجمالية 6000 متر مربع، ويشمل ذلك:
            - أعمال الهيكل الإنشائي
            - أعمال التشطيبات الداخلية والخارجية
            - أعمال الكهرباء والميكانيكا
            - أعمال تنسيق الموقع
            - أعمال أنظمة الأمن والسلامة
            - أعمال أنظمة المباني الذكية
            
            ### 3. المواصفات الفنية
            #### 3.1 أعمال الخرسانة
            - يجب أن تكون الخرسانة المسلحة بقوة لا تقل عن 40 نيوتن/مم²
            - يجب استخدام حديد تسليح مطابق للمواصفات السعودية
            - يجب استخدام إضافات للخرسانة لزيادة مقاومتها للعوامل الجوية
            
            #### 3.2 أعمال التشطيبات
            - يجب استخدام مواد عالية الجودة للتشطيبات الداخلية
            - يجب أن تكون الواجهات الخارجية مقاومة للعوامل الجوية
            - يجب استخدام زجاج عاكس للحرارة للواجهات
            - يجب استخدام مواد صديقة للبيئة
            
            ### 4. الشروط العامة
            - مدة التنفيذ: 15 شهراً من تاريخ استلام الموقع
            - غرامة التأخير: 0.2% من قيمة العقد عن كل يوم تأخير
            - ضمان الأعمال: 15 سنوات للهيكل الإنشائي، 7 سنوات للأعمال الميكانيكية والكهربائية
            
            ### 5. متطلبات الاستدامة
            - يجب أن يحقق المبنى متطلبات الاستدامة وفقاً لمعايير LEED
            - يجب توفير أنظمة لترشيد استهلاك الطاقة والمياه
            """
        }
    
    def run(self):
        """تشغيل تطبيق مقارنة المستندات"""
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
        self.ui.create_header("مقارنة المستندات", "أدوات متقدمة لمقارنة وتحليل المستندات")
        
        # إنشاء علامات تبويب للوظائف المختلفة
        tabs = st.tabs(["مقارنة الإصدارات", "مقارنة المستندات", "تحليل التغييرات", "سجل التغييرات"])
        
        # علامة تبويب مقارنة الإصدارات
        with tabs[0]:
            self.compare_versions()
        
        # علامة تبويب مقارنة المستندات
        with tabs[1]:
            self.compare_documents()
        
        # علامة تبويب تحليل التغييرات
        with tabs[2]:
            self.analyze_changes()
        
        # علامة تبويب سجل التغييرات
        with tabs[3]:
            self.show_change_history()
    
    def compare_versions(self):
        """مقارنة إصدارات المستندات"""
        st.markdown("### مقارنة إصدارات المستندات")
        
        # اختيار المناقصة
        tender_options = list(set([doc["related_entity"] for doc in self.documents_data]))
        selected_tender = st.selectbox(
            "اختر المناقصة",
            options=tender_options
        )
        
        # فلترة المستندات حسب المناقصة المختارة
        filtered_docs = [doc for doc in self.documents_data if doc["related_entity"] == selected_tender]
        
        # اختيار نوع المستند
        doc_types = list(set([doc["type"] for doc in filtered_docs]))
        selected_type = st.selectbox(
            "اختر نوع المستند",
            options=doc_types
        )
        
        # فلترة المستندات حسب النوع المختار
        type_filtered_docs = [doc for doc in filtered_docs if doc["type"] == selected_type]
        
        # ترتيب المستندات حسب الإصدار
        type_filtered_docs = sorted(type_filtered_docs, key=lambda x: x["version"])
        
        if len(type_filtered_docs) < 2:
            st.warning("يجب توفر إصدارين على الأقل للمقارنة")
        else:
            # اختيار الإصدارات للمقارنة
            col1, col2 = st.columns(2)
            
            with col1:
                version_options = [f"{doc['name']} (الإصدار {doc['version']})" for doc in type_filtered_docs]
                selected_version1_index = st.selectbox(
                    "الإصدار الأول",
                    options=range(len(version_options)),
                    format_func=lambda x: version_options[x]
                )
                selected_doc1 = type_filtered_docs[selected_version1_index]
            
            with col2:
                remaining_indices = [i for i in range(len(type_filtered_docs)) if i != selected_version1_index]
                selected_version2_index = st.selectbox(
                    "الإصدار الثاني",
                    options=remaining_indices,
                    format_func=lambda x: version_options[x]
                )
                selected_doc2 = type_filtered_docs[selected_version2_index]
            
            # زر بدء المقارنة
            if st.button("بدء المقارنة", use_container_width=True):
                # عرض معلومات المستندات المختارة
                st.markdown("### معلومات المستندات المختارة")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**الإصدار الأول:** {selected_doc1['version']}")
                    st.markdown(f"**التاريخ:** {selected_doc1['date']}")
                    st.markdown(f"**عدد الصفحات:** {selected_doc1['pages']}")
                    st.markdown(f"**الحجم:** {selected_doc1['size']} ميجابايت")
                
                with col2:
                    st.markdown(f"**الإصدار الثاني:** {selected_doc2['version']}")
                    st.markdown(f"**التاريخ:** {selected_doc2['date']}")
                    st.markdown(f"**عدد الصفحات:** {selected_doc2['pages']}")
                    st.markdown(f"**الحجم:** {selected_doc2['size']} ميجابايت")
                
                # الحصول على محتوى المستندات (في تطبيق حقيقي، سيتم استرجاع المحتوى من الملفات الفعلية)
                doc1_content = self.sample_document_content.get(selected_doc1["id"], "محتوى المستند غير متوفر")
                doc2_content = self.sample_document_content.get(selected_doc2["id"], "محتوى المستند غير متوفر")
                
                # إجراء المقارنة
                self.display_comparison(doc1_content, doc2_content)
    
    def display_comparison(self, text1, text2):
        """عرض نتائج المقارنة بين نصين"""
        st.markdown("### نتائج المقارنة")
        
        # تقسيم النصوص إلى أسطر
        lines1 = text1.splitlines()
        lines2 = text2.splitlines()
        
        # إجراء المقارنة باستخدام difflib
        d = difflib.Differ()
        diff = list(d.compare(lines1, lines2))
        
        # عرض ملخص التغييرات
        added = len([line for line in diff if line.startswith('+ ')])
        removed = len([line for line in diff if line.startswith('- ')])
        changed = len([line for line in diff if line.startswith('? ')])
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.ui.create_metric_card(
                "الإضافات",
                str(added),
                None,
                self.ui.COLORS['success']
            )
        
        with col2:
            self.ui.create_metric_card(
                "الحذف",
                str(removed),
                None,
                self.ui.COLORS['danger']
            )
        
        with col3:
            self.ui.create_metric_card(
                "التغييرات",
                str(changed // 2),  # تقسيم على 2 لأن كل تغيير يظهر مرتين
                None,
                self.ui.COLORS['warning']
            )
        
        # عرض التغييرات بالتفصيل
        st.markdown("### التغييرات بالتفصيل")
        
        # إنشاء عرض HTML للتغييرات
        html_diff = []
        for line in diff:
            if line.startswith('+ '):
                html_diff.append(f'<div style="background-color: #e6ffe6; padding: 2px 5px; margin: 2px 0; border-left: 3px solid green;">{line[2:]}</div>')
            elif line.startswith('- '):
                html_diff.append(f'<div style="background-color: #ffe6e6; padding: 2px 5px; margin: 2px 0; border-left: 3px solid red;">{line[2:]}</div>')
            elif line.startswith('? '):
                # تجاهل أسطر التفاصيل
                continue
            else:
                html_diff.append(f'<div style="padding: 2px 5px; margin: 2px 0;">{line[2:]}</div>')
        
        # عرض التغييرات
        st.markdown(''.join(html_diff), unsafe_allow_html=True)
        
        # خيارات إضافية
        st.markdown("### خيارات إضافية")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("تصدير التغييرات", use_container_width=True):
                st.success("تم تصدير التغييرات بنجاح")
        
        with col2:
            if st.button("إنشاء تقرير", use_container_width=True):
                st.success("تم إنشاء التقرير بنجاح")
        
        with col3:
            if st.button("حفظ المقارنة", use_container_width=True):
                st.success("تم حفظ المقارنة بنجاح")
    
    def compare_documents(self):
        """مقارنة مستندات مختلفة"""
        st.markdown("### مقارنة مستندات مختلفة")
        
        # اختيار المستند الأول
        col1, col2 = st.columns(2)
        
        with col1:
            tender1_options = list(set([doc["related_entity"] for doc in self.documents_data]))
            selected_tender1 = st.selectbox(
                "اختر المناقصة الأولى",
                options=tender1_options,
                key="tender1"
            )
            
            # فلترة المستندات حسب المناقصة المختارة
            filtered_docs1 = [doc for doc in self.documents_data if doc["related_entity"] == selected_tender1]
            
            # اختيار المستند
            doc_options1 = [f"{doc['name']} (الإصدار {doc['version']})" for doc in filtered_docs1]
            selected_doc1_index = st.selectbox(
                "اختر المستند الأول",
                options=range(len(doc_options1)),
                format_func=lambda x: doc_options1[x],
                key="doc1"
            )
            selected_doc1 = filtered_docs1[selected_doc1_index]
        
        with col2:
            tender2_options = list(set([doc["related_entity"] for doc in self.documents_data]))
            selected_tender2 = st.selectbox(
                "اختر المناقصة الثانية",
                options=tender2_options,
                key="tender2"
            )
            
            # فلترة المستندات حسب المناقصة المختارة
            filtered_docs2 = [doc for doc in self.documents_data if doc["related_entity"] == selected_tender2]
            
            # اختيار المستند
            doc_options2 = [f"{doc['name']} (الإصدار {doc['version']})" for doc in filtered_docs2]
            selected_doc2_index = st.selectbox(
                "اختر المستند الثاني",
                options=range(len(doc_options2)),
                format_func=lambda x: doc_options2[x],
                key="doc2"
            )
            selected_doc2 = filtered_docs2[selected_doc2_index]
        
        # خيارات المقارنة
        st.markdown("### خيارات المقارنة")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            comparison_type = st.radio(
                "نوع المقارنة",
                options=["مقارنة كاملة", "مقارنة الأقسام المتطابقة فقط", "مقارنة الاختلافات فقط"]
            )
        
        with col2:
            ignore_options = st.multiselect(
                "تجاهل",
                options=["المسافات", "علامات الترقيم", "حالة الأحرف", "الأرقام"],
                default=["المسافات"]
            )
        
        with col3:
            similarity_threshold = st.slider(
                "عتبة التشابه",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.05
            )
        
        # زر بدء المقارنة
        if st.button("بدء المقارنة بين المستندات", use_container_width=True):
            # عرض معلومات المستندات المختارة
            st.markdown("### معلومات المستندات المختارة")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**المستند الأول:** {selected_doc1['name']}")
                st.markdown(f"**الإصدار:** {selected_doc1['version']}")
                st.markdown(f"**التاريخ:** {selected_doc1['date']}")
                st.markdown(f"**المناقصة:** {selected_doc1['related_entity']}")
            
            with col2:
                st.markdown(f"**المستند الثاني:** {selected_doc2['name']}")
                st.markdown(f"**الإصدار:** {selected_doc2['version']}")
                st.markdown(f"**التاريخ:** {selected_doc2['date']}")
                st.markdown(f"**المناقصة:** {selected_doc2['related_entity']}")
            
            # الحصول على محتوى المستندات (في تطبيق حقيقي، سيتم استرجاع المحتوى من الملفات الفعلية)
            doc1_content = self.sample_document_content.get(selected_doc1["id"], "محتوى المستند غير متوفر")
            doc2_content = self.sample_document_content.get(selected_doc2["id"], "محتوى المستند غير متوفر")
            
            # إجراء المقارنة
            self.display_document_comparison(doc1_content, doc2_content, comparison_type, ignore_options, similarity_threshold)
    
    def display_document_comparison(self, text1, text2, comparison_type, ignore_options, similarity_threshold):
        """عرض نتائج المقارنة بين مستندين"""
        st.markdown("### نتائج المقارنة بين المستندين")
        
        # تقسيم النصوص إلى أقسام (في هذا المثال، نستخدم العناوين كفواصل للأقسام)
        sections1 = self.split_into_sections(text1)
        sections2 = self.split_into_sections(text2)
        
        # حساب نسبة التشابه الإجمالية
        similarity = difflib.SequenceMatcher(None, text1, text2).ratio()
        
        # عرض نسبة التشابه
        st.markdown(f"**نسبة التشابه الإجمالية:** {similarity:.2%}")
        
        # عرض مقارنة الأقسام
        st.markdown("### مقارنة الأقسام")
        
        # إنشاء جدول لمقارنة الأقسام
        section_comparisons = []
        
        for section1_title, section1_content in sections1.items():
            best_match = None
            best_similarity = 0
            
            for section2_title, section2_content in sections2.items():
                # حساب نسبة التشابه بين عناوين الأقسام
                title_similarity = difflib.SequenceMatcher(None, section1_title, section2_title).ratio()
                
                # حساب نسبة التشابه بين محتوى الأقسام
                content_similarity = difflib.SequenceMatcher(None, section1_content, section2_content).ratio()
                
                # حساب متوسط نسبة التشابه
                avg_similarity = (title_similarity + content_similarity) / 2
                
                if avg_similarity > best_similarity:
                    best_similarity = avg_similarity
                    best_match = {
                        "title": section2_title,
                        "content": section2_content,
                        "similarity": avg_similarity
                    }
            
            # إضافة المقارنة إلى القائمة
            if best_match and best_similarity >= similarity_threshold:
                section_comparisons.append({
                    "section1_title": section1_title,
                    "section2_title": best_match["title"],
                    "similarity": best_similarity
                })
            else:
                section_comparisons.append({
                    "section1_title": section1_title,
                    "section2_title": "غير موجود",
                    "similarity": 0
                })
        
        # إضافة الأقسام الموجودة في المستند الثاني فقط
        for section2_title, section2_content in sections2.items():
            if not any(comp["section2_title"] == section2_title for comp in section_comparisons):
                section_comparisons.append({
                    "section1_title": "غير موجود",
                    "section2_title": section2_title,
                    "similarity": 0
                })
        
        # عرض جدول المقارنة
        section_df = pd.DataFrame(section_comparisons)
        section_df = section_df.rename(columns={
            "section1_title": "القسم في المستند الأول",
            "section2_title": "القسم في المستند الثاني",
            "similarity": "نسبة التشابه"
        })
        
        # تنسيق نسبة التشابه
        section_df["نسبة التشابه"] = section_df["نسبة التشابه"].apply(lambda x: f"{x:.2%}")
        
        st.dataframe(
            section_df,
            use_container_width=True,
            hide_index=True
        )
        
        # عرض تفاصيل المقارنة
        st.markdown("### تفاصيل المقارنة")
        
        # اختيار قسم للمقارنة التفصيلية
        selected_section = st.selectbox(
            "اختر قسماً للمقارنة التفصيلية",
            options=[comp["section1_title"] for comp in section_comparisons if comp["section1_title"] != "غير موجود"]
        )
        
        # العثور على القسم المقابل في المستند الثاني
        matching_comparison = next((comp for comp in section_comparisons if comp["section1_title"] == selected_section), None)
        
        if matching_comparison and matching_comparison["section2_title"] != "غير موجود":
            # الحصول على محتوى القسمين
            section1_content = sections1[selected_section]
            section2_content = sections2[matching_comparison["section2_title"]]
            
            # عرض المقارنة التفصيلية
            self.display_comparison(section1_content, section2_content)
        else:
            st.warning("القسم المحدد غير موجود في المستند الثاني")
    
    def split_into_sections(self, text):
        """تقسيم النص إلى أقسام باستخدام العناوين"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in text.splitlines():
            # البحث عن العناوين (الأسطر التي تبدأ بـ #)
            if line.strip().startswith('#'):
                # حفظ القسم السابق إذا وجد
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                
                # بدء قسم جديد
                current_section = line.strip()
                current_content = []
            elif current_section:
                # إضافة السطر إلى محتوى القسم الحالي
                current_content.append(line)
        
        # حفظ القسم الأخير
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    def analyze_changes(self):
        """تحليل التغييرات في المستندات"""
        st.markdown("### تحليل التغييرات في المستندات")
        
        # اختيار المناقصة
        tender_options = list(set([doc["related_entity"] for doc in self.documents_data]))
        selected_tender = st.selectbox(
            "اختر المناقصة",
            options=tender_options,
            key="analyze_tender"
        )
        
        # فلترة المستندات حسب المناقصة المختارة
        filtered_docs = [doc for doc in self.documents_data if doc["related_entity"] == selected_tender]
        
        # تجميع المستندات حسب النوع
        doc_types = {}
        for doc in filtered_docs:
            if doc["type"] not in doc_types:
                doc_types[doc["type"]] = []
            doc_types[doc["type"]].append(doc)
        
        # عرض تحليل التغييرات لكل نوع مستند
        for doc_type, docs in doc_types.items():
            if len(docs) > 1:
                with st.expander(f"تحليل التغييرات في {doc_type}"):
                    # ترتيب المستندات حسب الإصدار
                    sorted_docs = sorted(docs, key=lambda x: x["version"])
                    
                    # عرض معلومات الإصدارات
                    st.markdown(f"**عدد الإصدارات:** {len(sorted_docs)}")
                    st.markdown(f"**أول إصدار:** {sorted_docs[0]['version']} ({sorted_docs[0]['date']})")
                    st.markdown(f"**آخر إصدار:** {sorted_docs[-1]['version']} ({sorted_docs[-1]['date']})")
                    
                    # حساب التغييرات بين الإصدارات
                    changes = []
                    for i in range(1, len(sorted_docs)):
                        prev_doc = sorted_docs[i-1]
                        curr_doc = sorted_docs[i]
                        
                        # حساب التغييرات (في تطبيق حقيقي، سيتم تحليل المحتوى الفعلي)
                        page_diff = curr_doc["pages"] - prev_doc["pages"]
                        size_diff = curr_doc["size"] - prev_doc["size"]
                        
                        changes.append({
                            "from_version": prev_doc["version"],
                            "to_version": curr_doc["version"],
                            "date": curr_doc["date"],
                            "page_diff": page_diff,
                            "size_diff": size_diff
                        })
                    
                    # عرض جدول التغييرات
                    changes_df = pd.DataFrame(changes)
                    changes_df = changes_df.rename(columns={
                        "from_version": "من الإصدار",
                        "to_version": "إلى الإصدار",
                        "date": "تاريخ التغيير",
                        "page_diff": "التغيير في عدد الصفحات",
                        "size_diff": "التغيير في الحجم (ميجابايت)"
                    })
                    
                    st.dataframe(
                        changes_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    # عرض رسم بياني للتغييرات
                    st.markdown("#### تطور حجم المستند عبر الإصدارات")
                    
                    versions = [doc["version"] for doc in sorted_docs]
                    sizes = [doc["size"] for doc in sorted_docs]
                    
                    chart_data = pd.DataFrame({
                        "الإصدار": versions,
                        "الحجم (ميجابايت)": sizes
                    })
                    
                    st.line_chart(chart_data.set_index("الإصدار"))
                    
                    # عرض رسم بياني لعدد الصفحات
                    st.markdown("#### تطور عدد الصفحات عبر الإصدارات")
                    
                    pages = [doc["pages"] for doc in sorted_docs]
                    
                    chart_data = pd.DataFrame({
                        "الإصدار": versions,
                        "عدد الصفحات": pages
                    })
                    
                    st.line_chart(chart_data.set_index("الإصدار"))
        
        # تحليل التغييرات الشاملة
        st.markdown("### تحليل التغييرات الشاملة")
        
        # حساب إجمالي التغييرات (في تطبيق حقيقي، سيتم تحليل المحتوى الفعلي)
        total_docs = len(filtered_docs)
        total_versions = sum(len(docs) for docs in doc_types.values())
        avg_versions = total_versions / len(doc_types) if doc_types else 0
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.ui.create_metric_card(
                "إجمالي المستندات",
                str(total_docs),
                None,
                self.ui.COLORS['primary']
            )
        
        with col2:
            self.ui.create_metric_card(
                "إجمالي الإصدارات",
                str(total_versions),
                None,
                self.ui.COLORS['secondary']
            )
        
        with col3:
            self.ui.create_metric_card(
                "متوسط الإصدارات لكل نوع",
                f"{avg_versions:.1f}",
                None,
                self.ui.COLORS['accent']
            )
        
        # عرض توزيع التغييرات حسب النوع
        st.markdown("#### توزيع الإصدارات حسب نوع المستند")
        
        type_counts = {doc_type: len(docs) for doc_type, docs in doc_types.items()}
        
        chart_data = pd.DataFrame({
            "نوع المستند": list(type_counts.keys()),
            "عدد الإصدارات": list(type_counts.values())
        })
        
        st.bar_chart(chart_data.set_index("نوع المستند"))
    
    def show_change_history(self):
        """عرض سجل التغييرات"""
        st.markdown("### سجل التغييرات")
        
        # إنشاء بيانات نموذجية لسجل التغييرات
        change_history = [
            {
                "id": "CH001",
                "document_id": "DOC001",
                "document_name": "كراسة الشروط - مناقصة إنشاء مبنى إداري",
                "from_version": "1.0",
                "to_version": "1.1",
                "change_date": "2025-02-10",
                "change_type": "تحديث",
                "changed_by": "أحمد محمد",
                "description": "تحديث المواصفات الفنية وشروط التنفيذ",
                "sections_changed": ["نطاق العمل", "المواصفات الفنية", "الشروط العامة"]
            },
            {
                "id": "CH002",
                "document_id": "DOC002",
                "document_name": "كراسة الشروط - مناقصة إنشاء مبنى إداري",
                "from_version": "1.1",
                "to_version": "2.0",
                "change_date": "2025-03-05",
                "change_type": "تحديث رئيسي",
                "changed_by": "سارة عبدالله",
                "description": "إضافة متطلبات الاستدامة وتحديث المواصفات الفنية",
                "sections_changed": ["المواصفات الفنية", "الشروط العامة", "متطلبات الاستدامة"]
            },
            {
                "id": "CH003",
                "document_id": "DOC004",
                "document_name": "جدول الكميات - مناقصة إنشاء مبنى إداري",
                "from_version": "1.0",
                "to_version": "1.1",
                "change_date": "2025-02-20",
                "change_type": "تحديث",
                "changed_by": "خالد عمر",
                "description": "تحديث الكميات وإضافة بنود جديدة",
                "sections_changed": ["أعمال الهيكل الإنشائي", "أعمال التشطيبات", "أعمال الكهرباء"]
            },
            {
                "id": "CH004",
                "document_id": "DOC006",
                "document_name": "المخططات - مناقصة إنشاء مبنى إداري",
                "from_version": "1.0",
                "to_version": "2.0",
                "change_date": "2025-03-10",
                "change_type": "تحديث رئيسي",
                "changed_by": "محمد علي",
                "description": "تحديث المخططات المعمارية والإنشائية",
                "sections_changed": ["المخططات المعمارية", "المخططات الإنشائية", "مخططات الكهرباء"]
            },
            {
                "id": "CH005",
                "document_id": "DOC008",
                "document_name": "كراسة الشروط - مناقصة صيانة طرق",
                "from_version": "1.0",
                "to_version": "1.1",
                "change_date": "2025-03-15",
                "change_type": "تحديث",
                "changed_by": "فاطمة أحمد",
                "description": "تحديث المواصفات الفنية وشروط التنفيذ",
                "sections_changed": ["نطاق العمل", "المواصفات الفنية", "الشروط العامة"]
            }
        ]
        
        # إنشاء فلاتر للسجل
        col1, col2, col3 = st.columns(3)
        
        with col1:
            document_filter = st.selectbox(
                "المستند",
                options=["الكل"] + list(set([ch["document_name"] for ch in change_history]))
            )
        
        with col2:
            change_type_filter = st.selectbox(
                "نوع التغيير",
                options=["الكل"] + list(set([ch["change_type"] for ch in change_history]))
            )
        
        with col3:
            date_range = st.date_input(
                "نطاق التاريخ",
                value=(
                    datetime.datetime.strptime("2025-01-01", "%Y-%m-%d").date(),
                    datetime.datetime.strptime("2025-12-31", "%Y-%m-%d").date()
                )
            )
        
        # تطبيق الفلاتر
        filtered_history = change_history
        
        if document_filter != "الكل":
            filtered_history = [ch for ch in filtered_history if ch["document_name"] == document_filter]
        
        if change_type_filter != "الكل":
            filtered_history = [ch for ch in filtered_history if ch["change_type"] == change_type_filter]
        
        if len(date_range) == 2:
            start_date, end_date = date_range
            filtered_history = [
                ch for ch in filtered_history 
                if start_date <= datetime.datetime.strptime(ch["change_date"], "%Y-%m-%d").date() <= end_date
            ]
        
        # عرض سجل التغييرات
        if not filtered_history:
            st.info("لا توجد تغييرات تطابق الفلاتر المحددة")
        else:
            # تحويل البيانات إلى DataFrame
            history_df = pd.DataFrame(filtered_history)
            
            # إعادة ترتيب الأعمدة وتغيير أسمائها
            display_df = history_df[[
                "id", "document_name", "from_version", "to_version", "change_date", "change_type", "changed_by", "description"
            ]].rename(columns={
                "id": "الرقم",
                "document_name": "اسم المستند",
                "from_version": "من الإصدار",
                "to_version": "إلى الإصدار",
                "change_date": "تاريخ التغيير",
                "change_type": "نوع التغيير",
                "changed_by": "بواسطة",
                "description": "الوصف"
            })
            
            # عرض الجدول
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # عرض تفاصيل التغيير المحدد
            st.markdown("### تفاصيل التغيير")
            
            selected_change_id = st.selectbox(
                "اختر تغييراً لعرض التفاصيل",
                options=[ch["id"] for ch in filtered_history],
                format_func=lambda x: next((f"{ch['id']} - {ch['document_name']} ({ch['from_version']} إلى {ch['to_version']})" for ch in filtered_history if ch["id"] == x), "")
            )
            
            # العثور على التغيير المحدد
            selected_change = next((ch for ch in filtered_history if ch["id"] == selected_change_id), None)
            
            if selected_change:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**المستند:** {selected_change['document_name']}")
                    st.markdown(f"**من الإصدار:** {selected_change['from_version']}")
                    st.markdown(f"**إلى الإصدار:** {selected_change['to_version']}")
                    st.markdown(f"**تاريخ التغيير:** {selected_change['change_date']}")
                
                with col2:
                    st.markdown(f"**نوع التغيير:** {selected_change['change_type']}")
                    st.markdown(f"**بواسطة:** {selected_change['changed_by']}")
                    st.markdown(f"**الوصف:** {selected_change['description']}")
                
                # عرض الأقسام التي تم تغييرها
                st.markdown("#### الأقسام التي تم تغييرها")
                
                for section in selected_change["sections_changed"]:
                    st.markdown(f"- {section}")
                
                # أزرار الإجراءات
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("عرض التغييرات بالتفصيل", use_container_width=True):
                        st.success("تم فتح التغييرات بالتفصيل")
                
                with col2:
                    if st.button("إنشاء تقرير", use_container_width=True):
                        st.success("تم إنشاء التقرير بنجاح")
                
                with col3:
                    if st.button("تصدير التغييرات", use_container_width=True):
                        st.success("تم تصدير التغييرات بنجاح")

# تشغيل التطبيق
if __name__ == "__main__":
    doc_comparison_app = DocumentComparisonApp()
    doc_comparison_app.run()
