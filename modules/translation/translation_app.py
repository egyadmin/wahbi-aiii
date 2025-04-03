"""
وحدة الترجمة - نظام تحليل المناقصات
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
import re
import datetime

# إضافة مسار المشروع للنظام
sys.path.append(str(Path(__file__).parent.parent))

# استيراد محسن واجهة المستخدم
from styling.enhanced_ui import UIEnhancer

class TranslationApp:
    """تطبيق الترجمة"""
    
    def __init__(self):
        """تهيئة تطبيق الترجمة"""
        self.ui = UIEnhancer(page_title="الترجمة - نظام تحليل المناقصات", page_icon="🌐")
        self.ui.apply_theme_colors()
        
        # قائمة اللغات المدعومة
        self.supported_languages = {
            "ar": "العربية",
            "en": "الإنجليزية",
            "fr": "الفرنسية",
            "de": "الألمانية",
            "es": "الإسبانية",
            "it": "الإيطالية",
            "zh": "الصينية",
            "ja": "اليابانية",
            "ru": "الروسية",
            "tr": "التركية"
        }
        
        # بيانات نموذجية للمصطلحات الفنية
        self.technical_terms = [
            {"ar": "كراسة الشروط", "en": "Terms and Conditions Document", "category": "مستندات"},
            {"ar": "جدول الكميات", "en": "Bill of Quantities (BOQ)", "category": "مستندات"},
            {"ar": "المواصفات الفنية", "en": "Technical Specifications", "category": "مستندات"},
            {"ar": "ضمان ابتدائي", "en": "Bid Bond", "category": "ضمانات"},
            {"ar": "ضمان حسن التنفيذ", "en": "Performance Bond", "category": "ضمانات"},
            {"ar": "ضمان دفعة مقدمة", "en": "Advance Payment Guarantee", "category": "ضمانات"},
            {"ar": "ضمان صيانة", "en": "Maintenance Bond", "category": "ضمانات"},
            {"ar": "مناقصة عامة", "en": "Public Tender", "category": "أنواع المناقصات"},
            {"ar": "مناقصة محدودة", "en": "Limited Tender", "category": "أنواع المناقصات"},
            {"ar": "منافسة", "en": "Competition", "category": "أنواع المناقصات"},
            {"ar": "أمر شراء", "en": "Purchase Order", "category": "عقود"},
            {"ar": "عقد إطاري", "en": "Framework Agreement", "category": "عقود"},
            {"ar": "عقد زمني", "en": "Time-based Contract", "category": "عقود"},
            {"ar": "عقد تسليم مفتاح", "en": "Turnkey Contract", "category": "عقود"},
            {"ar": "مقاول من الباطن", "en": "Subcontractor", "category": "أطراف"},
            {"ar": "استشاري", "en": "Consultant", "category": "أطراف"},
            {"ar": "مالك المشروع", "en": "Project Owner", "category": "أطراف"},
            {"ar": "مدير المشروع", "en": "Project Manager", "category": "أطراف"},
            {"ar": "مهندس الموقع", "en": "Site Engineer", "category": "أطراف"},
            {"ar": "مراقب الجودة", "en": "Quality Control", "category": "أطراف"},
            {"ar": "أعمال مدنية", "en": "Civil Works", "category": "أعمال"},
            {"ar": "أعمال كهربائية", "en": "Electrical Works", "category": "أعمال"},
            {"ar": "أعمال ميكانيكية", "en": "Mechanical Works", "category": "أعمال"},
            {"ar": "أعمال معمارية", "en": "Architectural Works", "category": "أعمال"},
            {"ar": "أعمال تشطيبات", "en": "Finishing Works", "category": "أعمال"},
            {"ar": "غرامة تأخير", "en": "Delay Penalty", "category": "شروط"},
            {"ar": "مدة التنفيذ", "en": "Execution Period", "category": "شروط"},
            {"ar": "فترة الضمان", "en": "Warranty Period", "category": "شروط"},
            {"ar": "شروط الدفع", "en": "Payment Terms", "category": "شروط"},
            {"ar": "تسوية النزاعات", "en": "Dispute Resolution", "category": "شروط"}
        ]
        
        # بيانات نموذجية للمستندات المترجمة
        self.translated_documents = [
            {
                "id": "TD001",
                "name": "كراسة الشروط - مناقصة إنشاء مبنى إداري",
                "source_language": "ar",
                "target_language": "en",
                "original_file": "specs_v2.0_ar.pdf",
                "translated_file": "specs_v2.0_en.pdf",
                "translation_date": "2025-03-15",
                "translated_by": "أحمد محمد",
                "status": "مكتمل",
                "pages": 52,
                "related_entity": "T-2025-001"
            },
            {
                "id": "TD002",
                "name": "جدول الكميات - مناقصة إنشاء مبنى إداري",
                "source_language": "ar",
                "target_language": "en",
                "original_file": "boq_v1.1_ar.xlsx",
                "translated_file": "boq_v1.1_en.xlsx",
                "translation_date": "2025-02-25",
                "translated_by": "سارة عبدالله",
                "status": "مكتمل",
                "pages": 22,
                "related_entity": "T-2025-001"
            },
            {
                "id": "TD003",
                "name": "المخططات - مناقصة إنشاء مبنى إداري",
                "source_language": "ar",
                "target_language": "en",
                "original_file": "drawings_v2.0_ar.pdf",
                "translated_file": "drawings_v2.0_en.pdf",
                "translation_date": "2025-03-20",
                "translated_by": "محمد علي",
                "status": "مكتمل",
                "pages": 35,
                "related_entity": "T-2025-001"
            },
            {
                "id": "TD004",
                "name": "كراسة الشروط - مناقصة صيانة طرق",
                "source_language": "ar",
                "target_language": "en",
                "original_file": "specs_v1.1_ar.pdf",
                "translated_file": "specs_v1.1_en.pdf",
                "translation_date": "2025-03-25",
                "translated_by": "فاطمة أحمد",
                "status": "مكتمل",
                "pages": 34,
                "related_entity": "T-2025-002"
            },
            {
                "id": "TD005",
                "name": "جدول الكميات - مناقصة صيانة طرق",
                "source_language": "ar",
                "target_language": "en",
                "original_file": "boq_v1.0_ar.xlsx",
                "translated_file": "boq_v1.0_en.xlsx",
                "translation_date": "2025-03-10",
                "translated_by": "خالد عمر",
                "status": "مكتمل",
                "pages": 15,
                "related_entity": "T-2025-002"
            },
            {
                "id": "TD006",
                "name": "كراسة الشروط - مناقصة توريد معدات",
                "source_language": "en",
                "target_language": "ar",
                "original_file": "specs_v1.0_en.pdf",
                "translated_file": "specs_v1.0_ar.pdf",
                "translation_date": "2025-02-15",
                "translated_by": "أحمد محمد",
                "status": "مكتمل",
                "pages": 28,
                "related_entity": "T-2025-003"
            },
            {
                "id": "TD007",
                "name": "عقد توريد - مناقصة توريد معدات",
                "source_language": "en",
                "target_language": "ar",
                "original_file": "contract_v1.0_en.pdf",
                "translated_file": "contract_v1.0_ar.pdf",
                "translation_date": "2025-03-05",
                "translated_by": "سارة عبدالله",
                "status": "مكتمل",
                "pages": 20,
                "related_entity": "T-2025-003"
            },
            {
                "id": "TD008",
                "name": "كراسة الشروط - مناقصة تجهيز مختبرات",
                "source_language": "ar",
                "target_language": "en",
                "original_file": "specs_v1.0_ar.pdf",
                "translated_file": "specs_v1.0_en.pdf",
                "translation_date": "2025-03-28",
                "translated_by": "محمد علي",
                "status": "قيد التنفيذ",
                "pages": 30,
                "related_entity": "T-2025-004"
            }
        ]
        
        # بيانات نموذجية للنصوص المترجمة
        self.sample_translations = {
            "text1": {
                "ar": """
                # كراسة الشروط والمواصفات
                ## مناقصة إنشاء مبنى إداري
                
                ### 1. مقدمة
                تدعو شركة شبه الجزيرة للمقاولات الشركات المتخصصة للتقدم بعروضها لتنفيذ مشروع إنشاء مبنى إداري في مدينة الرياض.
                
                ### 2. نطاق العمل
                يشمل نطاق العمل تصميم وتنفيذ مبنى إداري مكون من 6 طوابق بمساحة إجمالية 6000 متر مربع، ويشمل ذلك:
                - أعمال الهيكل الإنشائي
                - أعمال التشطيبات الداخلية والخارجية
                - أعمال الكهرباء والميكانيكا
                - أعمال تنسيق الموقع
                - أعمال أنظمة الأمن والسلامة
                - أعمال أنظمة المباني الذكية
                """,
                
                "en": """
                # Terms and Conditions Document
                ## Administrative Building Construction Tender
                
                ### 1. Introduction
                Peninsula Contracting Company invites specialized companies to submit their offers for the implementation of an administrative building construction project in Riyadh.
                
                ### 2. Scope of Work
                The scope of work includes the design and implementation of a 6-floor administrative building with a total area of 6000 square meters, including:
                - Structural works
                - Interior and exterior finishing works
                - Electrical and mechanical works
                - Site coordination works
                - Security and safety systems works
                - Smart building systems works
                """
            },
            
            "text2": {
                "ar": """
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
                """,
                
                "en": """
                ### 3. Technical Specifications
                #### 3.1 Concrete Works
                - Reinforced concrete must have a strength of not less than 40 Newton/mm²
                - Reinforcement steel must comply with Saudi specifications
                - Concrete additives must be used to increase its resistance to weather conditions
                
                #### 3.2 Finishing Works
                - High-quality materials must be used for interior finishes
                - Exterior facades must be weather-resistant
                - Heat-reflective glass must be used for facades
                - Environmentally friendly materials must be used
                """
            }
        }
    
    def run(self):
        """تشغيل تطبيق الترجمة"""
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
            {"name": "الترجمة", "icon": "translate"},
            {"name": "المساعد الذكي", "icon": "robot"},
            {"name": "التقارير", "icon": "bar-chart"},
            {"name": "الإعدادات", "icon": "gear"}
        ]
        
        # إنشاء الشريط الجانبي
        selected = self.ui.create_sidebar(menu_items)
        
        # إنشاء ترويسة الصفحة
        self.ui.create_header("الترجمة", "أدوات ترجمة المستندات والنصوص")
        
        # إنشاء علامات تبويب للوظائف المختلفة
        tabs = st.tabs(["ترجمة النصوص", "ترجمة المستندات", "قاموس المصطلحات", "المستندات المترجمة"])
        
        # علامة تبويب ترجمة النصوص
        with tabs[0]:
            self.translate_text()
        
        # علامة تبويب ترجمة المستندات
        with tabs[1]:
            self.translate_documents()
        
        # علامة تبويب قاموس المصطلحات
        with tabs[2]:
            self.technical_terms_dictionary()
        
        # علامة تبويب المستندات المترجمة
        with tabs[3]:
            self.show_translated_documents()
    
    def translate_text(self):
        """ترجمة النصوص"""
        st.markdown("### ترجمة النصوص")
        
        # اختيار لغات الترجمة
        col1, col2 = st.columns(2)
        
        with col1:
            source_language = st.selectbox(
                "لغة المصدر",
                options=list(self.supported_languages.keys()),
                format_func=lambda x: self.supported_languages[x],
                index=0  # العربية كلغة افتراضية
            )
        
        with col2:
            # استبعاد لغة المصدر من خيارات لغة الهدف
            target_languages = {k: v for k, v in self.supported_languages.items() if k != source_language}
            target_language = st.selectbox(
                "لغة الهدف",
                options=list(target_languages.keys()),
                format_func=lambda x: self.supported_languages[x],
                index=0  # أول لغة متاحة
            )
        
        # خيارات الترجمة
        st.markdown("#### خيارات الترجمة")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            translation_engine = st.radio(
                "محرك الترجمة",
                options=["OpenAI", "Google Translate", "Microsoft Translator", "محلي"]
            )
        
        with col2:
            use_technical_terms = st.checkbox("استخدام قاموس المصطلحات الفنية", value=True)
        
        with col3:
            preserve_formatting = st.checkbox("الحفاظ على التنسيق", value=True)
        
        # إدخال النص المراد ترجمته
        st.markdown("#### النص المراد ترجمته")
        
        # إضافة أمثلة نصية
        examples = st.expander("أمثلة نصية")
        with examples:
            if st.button("مثال 1: مقدمة كراسة الشروط"):
                source_text = self.sample_translations["text1"][source_language] if source_language in self.sample_translations["text1"] else self.sample_translations["text1"]["ar"]
            elif st.button("مثال 2: المواصفات الفنية"):
                source_text = self.sample_translations["text2"][source_language] if source_language in self.sample_translations["text2"] else self.sample_translations["text2"]["ar"]
            else:
                source_text = ""
        
        if "source_text" not in locals():
            source_text = ""
        
        source_text = st.text_area(
            "أدخل النص المراد ترجمته",
            value=source_text,
            height=200
        )
        
        # زر الترجمة
        if st.button("ترجمة النص", use_container_width=True):
            if not source_text:
                st.error("يرجى إدخال النص المراد ترجمته")
            else:
                # في تطبيق حقيقي، سيتم استدعاء واجهة برمجة التطبيقات للترجمة
                # هنا نستخدم النصوص النموذجية المحددة مسبقاً للعرض
                
                with st.spinner("جاري الترجمة..."):
                    # محاكاة تأخير الترجمة
                    import time
                    time.sleep(1)
                    
                    # التحقق من وجود ترجمة نموذجية
                    if source_language == "ar" and target_language == "en" and source_text.strip() in [self.sample_translations["text1"]["ar"].strip(), self.sample_translations["text2"]["ar"].strip()]:
                        if source_text.strip() == self.sample_translations["text1"]["ar"].strip():
                            translated_text = self.sample_translations["text1"]["en"]
                        else:
                            translated_text = self.sample_translations["text2"]["en"]
                    elif source_language == "en" and target_language == "ar" and source_text.strip() in [self.sample_translations["text1"]["en"].strip(), self.sample_translations["text2"]["en"].strip()]:
                        if source_text.strip() == self.sample_translations["text1"]["en"].strip():
                            translated_text = self.sample_translations["text1"]["ar"]
                        else:
                            translated_text = self.sample_translations["text2"]["ar"]
                    else:
                        # ترجمة نموذجية للعرض فقط
                        translated_text = f"[هذا نص مترجم نموذجي من {self.supported_languages[source_language]} إلى {self.supported_languages[target_language]}]\n\n{source_text}"
                
                # عرض النص المترجم
                st.markdown("#### النص المترجم")
                st.text_area(
                    "النص المترجم",
                    value=translated_text,
                    height=200
                )
                
                # أزرار إضافية
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("نسخ النص المترجم", use_container_width=True):
                        st.success("تم نسخ النص المترجم إلى الحافظة")
                
                with col2:
                    if st.button("حفظ الترجمة", use_container_width=True):
                        st.success("تم حفظ الترجمة بنجاح")
                
                with col3:
                    if st.button("تصدير كملف", use_container_width=True):
                        st.success("تم تصدير الترجمة كملف بنجاح")
                
                # عرض إحصائيات الترجمة
                st.markdown("#### إحصائيات الترجمة")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    self.ui.create_metric_card(
                        "عدد الكلمات",
                        str(len(source_text.split())),
                        None,
                        self.ui.COLORS['primary']
                    )
                
                with col2:
                    self.ui.create_metric_card(
                        "عدد الأحرف",
                        str(len(source_text)),
                        None,
                        self.ui.COLORS['secondary']
                    )
                
                with col3:
                    self.ui.create_metric_card(
                        "وقت الترجمة",
                        "1.2 ثانية",
                        None,
                        self.ui.COLORS['success']
                    )
                
                with col4:
                    self.ui.create_metric_card(
                        "المصطلحات الفنية",
                        "5",
                        None,
                        self.ui.COLORS['accent']
                    )
    
    def translate_documents(self):
        """ترجمة المستندات"""
        st.markdown("### ترجمة المستندات")
        
        # اختيار لغات الترجمة
        col1, col2 = st.columns(2)
        
        with col1:
            source_language = st.selectbox(
                "لغة المصدر",
                options=list(self.supported_languages.keys()),
                format_func=lambda x: self.supported_languages[x],
                index=0,  # العربية كلغة افتراضية
                key="doc_source_lang"
            )
        
        with col2:
            # استبعاد لغة المصدر من خيارات لغة الهدف
            target_languages = {k: v for k, v in self.supported_languages.items() if k != source_language}
            target_language = st.selectbox(
                "لغة الهدف",
                options=list(target_languages.keys()),
                format_func=lambda x: self.supported_languages[x],
                index=0,  # أول لغة متاحة
                key="doc_target_lang"
            )
        
        # تحميل المستند
        st.markdown("#### تحميل المستند")
        
        uploaded_file = st.file_uploader("اختر المستند المراد ترجمته", type=["pdf", "docx", "xlsx", "txt"])
        
        if uploaded_file is not None:
            st.success(f"تم تحميل الملف: {uploaded_file.name}")
            
            # عرض معلومات الملف
            file_details = {
                "اسم الملف": uploaded_file.name,
                "نوع الملف": uploaded_file.type,
                "حجم الملف": f"{uploaded_file.size / 1024:.1f} كيلوبايت"
            }
            
            st.json(file_details)
        
        # خيارات الترجمة
        st.markdown("#### خيارات الترجمة")
        
        col1, col2 = st.columns(2)
        
        with col1:
            translation_engine = st.radio(
                "محرك الترجمة",
                options=["OpenAI", "Google Translate", "Microsoft Translator", "محلي"],
                key="doc_engine"
            )
            
            use_technical_terms = st.checkbox("استخدام قاموس المصطلحات الفنية", value=True, key="doc_terms")
        
        with col2:
            preserve_formatting = st.checkbox("الحفاظ على التنسيق", value=True, key="doc_format")
            
            translate_images = st.checkbox("ترجمة النصوص في الصور", value=False)
            
            maintain_layout = st.checkbox("الحفاظ على تخطيط المستند", value=True)
        
        # معلومات إضافية
        st.markdown("#### معلومات إضافية")
        
        col1, col2 = st.columns(2)
        
        with col1:
            document_name = st.text_input("اسم المستند")
        
        with col2:
            related_entity = st.text_input("الكيان المرتبط (مثل: رقم المناقصة أو المشروع)")
        
        # زر بدء الترجمة
        if st.button("بدء ترجمة المستند", use_container_width=True):
            if uploaded_file is None:
                st.error("يرجى تحميل المستند المراد ترجمته")
            else:
                # في تطبيق حقيقي، سيتم إرسال المستند إلى خدمة الترجمة
                # هنا نعرض محاكاة لعملية الترجمة
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # محاكاة تقدم الترجمة
                import time
                for i in range(101):
                    progress_bar.progress(i)
                    
                    if i < 10:
                        status_text.text("جاري تحليل المستند...")
                    elif i < 30:
                        status_text.text("جاري استخراج النصوص...")
                    elif i < 70:
                        status_text.text("جاري ترجمة المحتوى...")
                    elif i < 90:
                        status_text.text("جاري إعادة بناء المستند...")
                    else:
                        status_text.text("جاري إنهاء الترجمة...")
                    
                    time.sleep(0.05)
                
                # عرض نتيجة الترجمة
                st.success("تمت ترجمة المستند بنجاح!")
                
                # إنشاء اسم الملف المترجم
                file_name_parts = uploaded_file.name.split('.')
                translated_file_name = f"{'.'.join(file_name_parts[:-1])}_{target_language}.{file_name_parts[-1]}"
                
                # عرض معلومات الملف المترجم
                st.markdown("#### معلومات الملف المترجم")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**اسم الملف:** {translated_file_name}")
                    st.markdown(f"**لغة المصدر:** {self.supported_languages[source_language]}")
                    st.markdown(f"**لغة الهدف:** {self.supported_languages[target_language]}")
                
                with col2:
                    st.markdown(f"**محرك الترجمة:** {translation_engine}")
                    st.markdown(f"**تاريخ الترجمة:** {datetime.datetime.now().strftime('%Y-%m-%d')}")
                    st.markdown(f"**حالة الترجمة:** مكتمل")
                
                # أزرار إضافية
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("تنزيل الملف المترجم", use_container_width=True):
                        st.success("تم بدء تنزيل الملف المترجم")
                
                with col2:
                    if st.button("حفظ في المستندات المترجمة", use_container_width=True):
                        st.success("تم حفظ الملف في المستندات المترجمة")
                
                with col3:
                    if st.button("مشاركة الملف", use_container_width=True):
                        st.success("تم نسخ رابط مشاركة الملف")
                
                # عرض إحصائيات الترجمة
                st.markdown("#### إحصائيات الترجمة")
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    self.ui.create_metric_card(
                        "عدد الصفحات",
                        "12",
                        None,
                        self.ui.COLORS['primary']
                    )
                
                with col2:
                    self.ui.create_metric_card(
                        "عدد الكلمات",
                        "2,450",
                        None,
                        self.ui.COLORS['secondary']
                    )
                
                with col3:
                    self.ui.create_metric_card(
                        "وقت الترجمة",
                        "45 ثانية",
                        None,
                        self.ui.COLORS['success']
                    )
                
                with col4:
                    self.ui.create_metric_card(
                        "المصطلحات الفنية",
                        "28",
                        None,
                        self.ui.COLORS['accent']
                    )
    
    def technical_terms_dictionary(self):
        """قاموس المصطلحات الفنية"""
        st.markdown("### قاموس المصطلحات الفنية")
        
        # إضافة مصطلح جديد
        with st.expander("إضافة مصطلح جديد"):
            with st.form("add_term_form"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    term_ar = st.text_input("المصطلح بالعربية")
                
                with col2:
                    term_en = st.text_input("المصطلح بالإنجليزية")
                
                with col3:
                    term_category = st.selectbox(
                        "الفئة",
                        options=["مستندات", "ضمانات", "أنواع المناقصات", "عقود", "أطراف", "أعمال", "شروط", "أخرى"]
                    )
                
                # زر إضافة المصطلح
                submit_button = st.form_submit_button("إضافة المصطلح")
                
                if submit_button:
                    if not term_ar or not term_en:
                        st.error("يرجى ملء جميع الحقول المطلوبة")
                    else:
                        # في تطبيق حقيقي، سيتم إضافة المصطلح إلى قاعدة البيانات
                        st.success("تمت إضافة المصطلح بنجاح")
        
        # البحث في المصطلحات
        st.markdown("#### البحث في المصطلحات")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("البحث عن مصطلح")
        
        with col2:
            search_language = st.radio(
                "لغة البحث",
                options=["الكل", "العربية", "الإنجليزية"],
                horizontal=True
            )
        
        with col3:
            category_filter = st.selectbox(
                "تصفية حسب الفئة",
                options=["الكل", "مستندات", "ضمانات", "أنواع المناقصات", "عقود", "أطراف", "أعمال", "شروط", "أخرى"]
            )
        
        # تطبيق الفلاتر
        filtered_terms = self.technical_terms
        
        if search_term:
            if search_language == "العربية":
                filtered_terms = [term for term in filtered_terms if search_term.lower() in term["ar"].lower()]
            elif search_language == "الإنجليزية":
                filtered_terms = [term for term in filtered_terms if search_term.lower() in term["en"].lower()]
            else:
                filtered_terms = [term for term in filtered_terms if search_term.lower() in term["ar"].lower() or search_term.lower() in term["en"].lower()]
        
        if category_filter != "الكل":
            filtered_terms = [term for term in filtered_terms if term["category"] == category_filter]
        
        # عرض المصطلحات
        st.markdown("#### المصطلحات الفنية")
        
        if not filtered_terms:
            st.info("لا توجد مصطلحات تطابق معايير البحث")
        else:
            # تحويل البيانات إلى DataFrame
            terms_df = pd.DataFrame(filtered_terms)
            
            # إعادة تسمية الأعمدة
            terms_df = terms_df.rename(columns={
                "ar": "المصطلح بالعربية",
                "en": "المصطلح بالإنجليزية",
                "category": "الفئة"
            })
            
            # عرض الجدول
            st.dataframe(
                terms_df,
                use_container_width=True,
                hide_index=True
            )
            
            # أزرار إضافية
            col1, col2 = st.columns([1, 5])
            
            with col1:
                if st.button("تصدير القاموس", use_container_width=True):
                    st.success("تم تصدير القاموس بنجاح")
        
        # عرض إحصائيات القاموس
        st.markdown("#### إحصائيات القاموس")
        
        # حساب عدد المصطلحات في كل فئة
        category_counts = {}
        for term in self.technical_terms:
            if term["category"] not in category_counts:
                category_counts[term["category"]] = 0
            category_counts[term["category"]] += 1
        
        # عرض الإحصائيات
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### عدد المصطلحات حسب الفئة")
            
            # تحويل البيانات إلى DataFrame
            category_df = pd.DataFrame({
                "الفئة": list(category_counts.keys()),
                "العدد": list(category_counts.values())
            })
            
            # عرض الرسم البياني
            st.bar_chart(category_df.set_index("الفئة"))
        
        with col2:
            st.markdown("##### إحصائيات عامة")
            
            total_terms = len(self.technical_terms)
            categories_count = len(category_counts)
            
            st.markdown(f"**إجمالي المصطلحات:** {total_terms}")
            st.markdown(f"**عدد الفئات:** {categories_count}")
            st.markdown(f"**متوسط المصطلحات لكل فئة:** {total_terms / categories_count:.1f}")
            st.markdown(f"**آخر تحديث للقاموس:** {datetime.datetime.now().strftime('%Y-%m-%d')}")
    
    def show_translated_documents(self):
        """عرض المستندات المترجمة"""
        st.markdown("### المستندات المترجمة")
        
        # إنشاء فلاتر للمستندات
        col1, col2, col3 = st.columns(3)
        
        with col1:
            entity_filter = st.selectbox(
                "تصفية حسب الكيان",
                options=["الكل"] + list(set([doc["related_entity"] for doc in self.translated_documents]))
            )
        
        with col2:
            language_pair_filter = st.selectbox(
                "تصفية حسب زوج اللغات",
                options=["الكل"] + list(set([f"{doc['source_language']} -> {doc['target_language']}" for doc in self.translated_documents]))
            )
        
        with col3:
            status_filter = st.selectbox(
                "تصفية حسب الحالة",
                options=["الكل", "مكتمل", "قيد التنفيذ"]
            )
        
        # تطبيق الفلاتر
        filtered_docs = self.translated_documents
        
        if entity_filter != "الكل":
            filtered_docs = [doc for doc in filtered_docs if doc["related_entity"] == entity_filter]
        
        if language_pair_filter != "الكل":
            source_lang, target_lang = language_pair_filter.split(" -> ")
            filtered_docs = [doc for doc in filtered_docs if doc["source_language"] == source_lang and doc["target_language"] == target_lang]
        
        if status_filter != "الكل":
            filtered_docs = [doc for doc in filtered_docs if doc["status"] == status_filter]
        
        # عرض المستندات المترجمة
        if not filtered_docs:
            st.info("لا توجد مستندات مترجمة تطابق معايير التصفية")
        else:
            # تحويل البيانات إلى DataFrame
            docs_df = pd.DataFrame(filtered_docs)
            
            # تحويل رموز اللغات إلى أسماء اللغات
            docs_df["source_language"] = docs_df["source_language"].map(self.supported_languages)
            docs_df["target_language"] = docs_df["target_language"].map(self.supported_languages)
            
            # إعادة ترتيب الأعمدة وتغيير أسمائها
            display_df = docs_df[[
                "id", "name", "source_language", "target_language", "translation_date", "status", "pages", "related_entity"
            ]].rename(columns={
                "id": "الرقم",
                "name": "اسم المستند",
                "source_language": "لغة المصدر",
                "target_language": "لغة الهدف",
                "translation_date": "تاريخ الترجمة",
                "status": "الحالة",
                "pages": "عدد الصفحات",
                "related_entity": "الكيان المرتبط"
            })
            
            # عرض الجدول
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )
            
            # عرض تفاصيل المستند المحدد
            st.markdown("#### تفاصيل المستند المترجم")
            
            selected_doc_id = st.selectbox(
                "اختر مستنداً لعرض التفاصيل",
                options=[doc["id"] for doc in filtered_docs],
                format_func=lambda x: next((f"{doc['id']} - {doc['name']}" for doc in filtered_docs if doc["id"] == x), "")
            )
            
            # العثور على المستند المحدد
            selected_doc = next((doc for doc in filtered_docs if doc["id"] == selected_doc_id), None)
            
            if selected_doc:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**اسم المستند:** {selected_doc['name']}")
                    st.markdown(f"**لغة المصدر:** {self.supported_languages[selected_doc['source_language']]}")
                    st.markdown(f"**لغة الهدف:** {self.supported_languages[selected_doc['target_language']]}")
                    st.markdown(f"**تاريخ الترجمة:** {selected_doc['translation_date']}")
                
                with col2:
                    st.markdown(f"**الملف الأصلي:** {selected_doc['original_file']}")
                    st.markdown(f"**الملف المترجم:** {selected_doc['translated_file']}")
                    st.markdown(f"**المترجم:** {selected_doc['translated_by']}")
                    st.markdown(f"**الحالة:** {selected_doc['status']}")
                
                # أزرار الإجراءات
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("تنزيل الملف الأصلي", use_container_width=True):
                        st.success("تم بدء تنزيل الملف الأصلي")
                
                with col2:
                    if st.button("تنزيل الملف المترجم", use_container_width=True):
                        st.success("تم بدء تنزيل الملف المترجم")
                
                with col3:
                    if st.button("مشاركة الملف المترجم", use_container_width=True):
                        st.success("تم نسخ رابط مشاركة الملف المترجم")
        
        # عرض إحصائيات الترجمة
        st.markdown("#### إحصائيات الترجمة")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # إحصائيات حسب زوج اللغات
            language_pairs = {}
            for doc in self.translated_documents:
                pair = f"{self.supported_languages[doc['source_language']]} -> {self.supported_languages[doc['target_language']]}"
                if pair not in language_pairs:
                    language_pairs[pair] = 0
                language_pairs[pair] += 1
            
            st.markdown("##### المستندات حسب زوج اللغات")
            
            # تحويل البيانات إلى DataFrame
            language_df = pd.DataFrame({
                "زوج اللغات": list(language_pairs.keys()),
                "العدد": list(language_pairs.values())
            })
            
            # عرض الرسم البياني
            st.bar_chart(language_df.set_index("زوج اللغات"))
        
        with col2:
            # إحصائيات حسب الكيان المرتبط
            entity_counts = {}
            for doc in self.translated_documents:
                if doc["related_entity"] not in entity_counts:
                    entity_counts[doc["related_entity"]] = 0
                entity_counts[doc["related_entity"]] += 1
            
            st.markdown("##### المستندات حسب الكيان المرتبط")
            
            # تحويل البيانات إلى DataFrame
            entity_df = pd.DataFrame({
                "الكيان المرتبط": list(entity_counts.keys()),
                "العدد": list(entity_counts.values())
            })
            
            # عرض الرسم البياني
            st.bar_chart(entity_df.set_index("الكيان المرتبط"))
        
        with col3:
            # إحصائيات عامة
            total_docs = len(self.translated_documents)
            completed_docs = len([doc for doc in self.translated_documents if doc["status"] == "مكتمل"])
            in_progress_docs = len([doc for doc in self.translated_documents if doc["status"] == "قيد التنفيذ"])
            total_pages = sum([doc["pages"] for doc in self.translated_documents])
            
            st.markdown("##### إحصائيات عامة")
            st.markdown(f"**إجمالي المستندات المترجمة:** {total_docs}")
            st.markdown(f"**المستندات المكتملة:** {completed_docs}")
            st.markdown(f"**المستندات قيد التنفيذ:** {in_progress_docs}")
            st.markdown(f"**إجمالي الصفحات المترجمة:** {total_pages}")
            st.markdown(f"**متوسط الصفحات لكل مستند:** {total_pages / total_docs:.1f}")

# تشغيل التطبيق
if __name__ == "__main__":
    translation_app = TranslationApp()
    translation_app.run()
