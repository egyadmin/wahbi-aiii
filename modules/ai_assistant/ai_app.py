# -*- coding: utf-8 -*-
"""
وحدة مساعد الذكاء الاصطناعي
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from datetime import datetime
import time
import os
import sys
import json
import requests
from pathlib import Path
import io
import base64
import re
from PIL import Image
import PyPDF2
import docx
import anthropic
import tempfile

# إضافة المسار للوصول إلى الوحدات الأخرى
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

class AIAssistantApp:
    """تطبيق مساعد الذكاء الاصطناعي"""
    
    def __init__(self):
        """تهيئة تطبيق مساعد الذكاء الاصطناعي"""
        self.uploaded_files = {}
        self.analysis_results = {}
        
        # تهيئة مفاتيح API لنماذج هجين فيس
        # تحميل المفاتيح من متغيرات البيئة أو من الإعدادات
        if 'ai_api_key' not in st.session_state:
            # محاولة الحصول على المفتاح من متغيرات البيئة أولاً
            ai_key = os.environ.get('AI_API_KEY', '')
            # إذا لم يكن موجودًا، حاول الحصول عليه من أسرار هجين فيس
            if not ai_key and os.path.exists('/home/user/.huggingface/token'):
                with open('/home/user/.huggingface/token', 'r') as f:
                    ai_key = f.read().strip()
            # إذا لم يكن موجودًا، استخدم المفتاح المقدم في وحدة المعرفة
            if not ai_key:
                ai_key = ""
            st.session_state.ai_api_key = ai_key
        
        if 'anthropic_api_key' not in st.session_state:
            # محاولة الحصول على المفتاح من متغيرات البيئة أولاً
            anthropic_key = os.environ.get('ANTHROPIC_API_KEY', '')
            # إذا لم يكن موجودًا، حاول الحصول عليه من أسرار هجين فيس
            if not anthropic_key:
                # استخدم نفس المفتاح لـ anthropic مؤقتًا
                anthropic_key = st.session_state.ai_api_key
            st.session_state.anthropic_api_key = anthropic_key
        
        # تهيئة محادثة الذكاء الاصطناعي
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        if 'selected_model' not in st.session_state:
            st.session_state.selected_model = "anthropic"
    
    def run(self):
        """تشغيل تطبيق مساعد الذكاء الاصطناعي"""
        # عرض عنوان التطبيق
        st.title("مساعد الذكاء الاصطناعي")
        
        # إنشاء تبويبات التطبيق
        tabs = st.tabs([
            "المحادثة",
            "تحليل المستندات",
            "تحليل العقود",
            "تقدير التكاليف",
            "تحليل المخاطر",
            "الإعدادات"
        ])
        
        # عرض محتوى كل تبويب
        with tabs[0]:
            self._render_chat_tab()
        
        with tabs[1]:
            self._render_document_analysis_tab()
        
        with tabs[2]:
            self._render_contract_analysis_tab()
        
        with tabs[3]:
            self._render_cost_estimation_tab()
        
        with tabs[4]:
            self._render_risk_analysis_tab()
        
        with tabs[5]:
            self._render_settings_tab()
    
    def _render_chat_tab(self):
        """عرض تبويب المحادثة مع الذكاء الاصطناعي"""
        st.markdown("### المحادثة مع الذكاء الاصطناعي")
        
        # اختيار نموذج الذكاء الاصطناعي
        selected_model = st.selectbox(
            "اختر نموذج الذكاء الاصطناعي:",
            ["anthropic", "ai"],
            index=0 if st.session_state.selected_model == "anthropic" else 1
        )
        
        # تحديث النموذج المختار إذا تغير
        if selected_model != st.session_state.selected_model:
            st.session_state.selected_model = selected_model
            st.rerun()  # تم تعديل هذا من st.experimental_rerun()
        
        # التحقق من وجود مفتاح API للنموذج المختار
        api_key_available = False
        if selected_model == "anthropic" and st.session_state.anthropic_api_key:
            api_key_available = True
        elif selected_model == "ai" and st.session_state.ai_api_key:
            api_key_available = True
        
        # عرض رسائل المحادثة
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # إذا لم يكن مفتاح API متاحًا، عرض رسالة خطأ
        if not api_key_available:
            st.error(f"لم يتم تكوين مفتاح API لنموذج {selected_model}. يرجى تكوين المفتاح في الإعدادات.")
        else:
            # مربع إدخال الرسالة
            if prompt := st.chat_input("اكتب رسالتك هنا:"):
                # إضافة رسالة المستخدم إلى المحادثة
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # عرض رسالة المستخدم
                with st.chat_message("user"):
                    st.markdown(prompt)
                
                # عرض مؤشر التحميل أثناء معالجة الرسالة
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("جاري التفكير...")
                    
                    try:
                        # الحصول على رد من النموذج المختار
                        if selected_model == "anthropic":
                            response = self._get_anthropic_response(prompt)
                        else:
                            response = self._get_ai_response(prompt)
                        
                        # عرض الرد
                        message_placeholder.markdown(response)
                        
                        # إضافة رد المساعد إلى المحادثة
                        st.session_state.messages.append({"role": "assistant", "content": response})
                    except Exception as e:
                        message_placeholder.markdown(f"حدث خطأ: {str(e)}")
        
        # زر لمسح المحادثة
        if st.button("مسح المحادثة"):
            st.session_state.messages = []
            st.rerun()  # تم تعديل هذا من st.experimental_rerun()
    
    def _render_document_analysis_tab(self):
        """عرض تبويب تحليل المستندات"""
        st.markdown("### تحليل المستندات")
        
        st.markdown("""
        يمكنك استخدام هذه الأداة لتحليل المستندات والتقارير باستخدام الذكاء الاصطناعي.
        الأداة تدعم تحليل الملفات التالية:
        - ملفات PDF
        - ملفات Word
        - ملفات النصوص TXT
        """)
        
        # إنشاء تبويبات فرعية
        doc_tabs = st.tabs([
            "تحميل المستندات",
            "استخراج النص",
            "تحليل المحتوى",
            "الملخص والتوصيات"
        ])
        
        # تبويب تحميل المستندات
        with doc_tabs[0]:
            st.markdown("#### تحميل المستندات")
            
            uploaded_file = st.file_uploader(
                "اختر ملفًا للتحليل (PDF, DOCX, TXT)",
                type=["pdf", "docx", "txt"],
                key="document_file_uploader"
            )
            
            if uploaded_file is not None:
                # حفظ الملف المرفوع
                file_details = {
                    "filename": uploaded_file.name,
                    "filetype": uploaded_file.type,
                    "filesize": uploaded_file.size
                }
                
                st.write("### تفاصيل الملف")
                st.write(f"اسم الملف: {file_details['filename']}")
                st.write(f"نوع الملف: {file_details['filetype']}")
                st.write(f"حجم الملف: {file_details['filesize']} بايت")
                
                # حفظ الملف في الذاكرة المؤقتة
                self.uploaded_files["document"] = uploaded_file
                
                st.success(f"تم تحميل الملف {uploaded_file.name} بنجاح!")
        
        # تبويب استخراج النص
        with doc_tabs[1]:
            st.markdown("#### استخراج النص")
            
            if "document" not in self.uploaded_files:
                st.info("الرجاء تحميل مستند أولاً من تبويب 'تحميل المستندات'")
            else:
                if st.button("استخراج النص من المستند"):
                    with st.spinner("جاري استخراج النص..."):
                        # استخراج النص من الملف
                        extracted_text = self._extract_text_from_file(self.uploaded_files["document"])
                        
                        # حفظ النص المستخرج
                        self.analysis_results["extracted_text"] = extracted_text
                        
                        # عرض النص المستخرج
                        st.markdown("### النص المستخرج")
                        st.text_area("النص:", value=extracted_text, height=400, disabled=True)
                        
                        st.success("تم استخراج النص بنجاح!")
                
                # إذا كان النص قد تم استخراجه بالفعل، عرضه
                if "extracted_text" in self.analysis_results:
                    st.markdown("### النص المستخرج")
                    st.text_area("النص:", value=self.analysis_results["extracted_text"], height=400, disabled=True)
        
        # تبويب تحليل المحتوى
        with doc_tabs[2]:
            st.markdown("#### تحليل المحتوى")
            
            if "extracted_text" not in self.analysis_results:
                st.info("الرجاء استخراج النص أولاً من تبويب 'استخراج النص'")
            else:
                if st.button("تحليل المحتوى"):
                    with st.spinner("جاري تحليل المحتوى..."):
                        # تحليل المحتوى باستخدام الذكاء الاصطناعي
                        analysis_prompt = f"""
                        قم بتحليل النص التالي وتقديم:
                        1. الموضوعات الرئيسية
                        2. الكلمات المفتاحية
                        3. الأفكار الرئيسية
                        4. أي معلومات مهمة أخرى
                        
                        النص:
                        {self.analysis_results["extracted_text"][:4000]}
                        """
                        
                        # الحصول على التحليل من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            analysis_result = self._get_anthropic_response(analysis_prompt)
                        else:
                            analysis_result = self._get_ai_response(analysis_prompt)
                        
                        # حفظ نتيجة التحليل
                        self.analysis_results["content_analysis"] = analysis_result
                        
                        # عرض نتيجة التحليل
                        st.markdown("### نتيجة التحليل")
                        st.markdown(analysis_result)
                        
                        st.success("تم تحليل المحتوى بنجاح!")
                
                # إذا كان التحليل قد تم بالفعل، عرضه
                if "content_analysis" in self.analysis_results:
                    st.markdown("### نتيجة التحليل")
                    st.markdown(self.analysis_results["content_analysis"])
        
        # تبويب الملخص والتوصيات
        with doc_tabs[3]:
            st.markdown("#### الملخص والتوصيات")
            
            if "content_analysis" not in self.analysis_results:
                st.info("الرجاء تحليل المحتوى أولاً من تبويب 'تحليل المحتوى'")
            else:
                if st.button("إنشاء ملخص وتوصيات"):
                    with st.spinner("جاري إنشاء الملخص والتوصيات..."):
                        # إنشاء ملخص وتوصيات باستخدام الذكاء الاصطناعي
                        summary_prompt = f"""
                        بناءً على التحليل التالي، قم بإنشاء:
                        1. ملخص موجز (لا يزيد عن 300 كلمة)
                        2. توصيات عملية (3-5 توصيات)
                        
                        التحليل:
                        {self.analysis_results["content_analysis"]}
                        """
                        
                        # الحصول على الملخص والتوصيات من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            summary_result = self._get_anthropic_response(summary_prompt)
                        else:
                            summary_result = self._get_ai_response(summary_prompt)
                        
                        # حفظ الملخص والتوصيات
                        self.analysis_results["summary_recommendations"] = summary_result
                        
                        # عرض الملخص والتوصيات
                        st.markdown("### الملخص والتوصيات")
                        st.markdown(summary_result)
                        
                        st.success("تم إنشاء الملخص والتوصيات بنجاح!")
                
                # إذا كان الملخص والتوصيات قد تم إنشاؤهما بالفعل، عرضهما
                if "summary_recommendations" in self.analysis_results:
                    st.markdown("### الملخص والتوصيات")
                    st.markdown(self.analysis_results["summary_recommendations"])
                    
                    # زر لتصدير التقرير
                    report_content = f"""
                    # تقرير تحليل المستند
                    
                    ## معلومات الملف
                    - اسم الملف: {self.uploaded_files["document"].name}
                    - نوع الملف: {self.uploaded_files["document"].type}
                    - حجم الملف: {self.uploaded_files["document"].size} بايت
                    
                    ## تحليل المحتوى
                    {self.analysis_results["content_analysis"]}
                    
                    ## الملخص والتوصيات
                    {self.analysis_results["summary_recommendations"]}
                    
                    ## تم إنشاء هذا التقرير بواسطة مساعد الذكاء الاصطناعي
                    تاريخ الإنشاء: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    """
                    
                    st.download_button(
                        label="تصدير التقرير (PDF)",
                        data=report_content.encode('utf-8'),
                        file_name=f"تقرير_تحليل_المستند_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        key="export_document_report_pdf"
                    )
    
    def _render_contract_analysis_tab(self):
        """عرض تبويب تحليل العقود"""
        st.markdown("### تحليل العقود")
        
        st.markdown("""
        يمكنك استخدام هذه الأداة لتحليل العقود واستخراج البنود المهمة باستخدام الذكاء الاصطناعي.
        الأداة تدعم تحليل الملفات التالية:
        - ملفات PDF
        - ملفات Word
        - ملفات النصوص TXT
        """)
        
        # إنشاء تبويبات فرعية
        contract_tabs = st.tabs([
            "تحميل العقد",
            "استخراج البنود",
            "تحليل المخاطر",
            "التقرير النهائي"
        ])
        
        # تبويب تحميل العقد
        with contract_tabs[0]:
            st.markdown("#### تحميل العقد")
            
            uploaded_file = st.file_uploader(
                "اختر ملف العقد للتحليل (PDF, DOCX, TXT)",
                type=["pdf", "docx", "txt"],
                key="contract_file_uploader"
            )
            
            if uploaded_file is not None:
                # حفظ الملف المرفوع
                file_details = {
                    "filename": uploaded_file.name,
                    "filetype": uploaded_file.type,
                    "filesize": uploaded_file.size
                }
                
                st.write("### تفاصيل الملف")
                st.write(f"اسم الملف: {file_details['filename']}")
                st.write(f"نوع الملف: {file_details['filetype']}")
                st.write(f"حجم الملف: {file_details['filesize']} بايت")
                
                # حفظ الملف في الذاكرة المؤقتة
                self.uploaded_files["contract"] = uploaded_file
                
                st.success(f"تم تحميل الملف {uploaded_file.name} بنجاح!")
        
        # تبويب استخراج البنود
        with contract_tabs[1]:
            st.markdown("#### استخراج البنود")
            
            if "contract" not in self.uploaded_files:
                st.info("الرجاء تحميل ملف العقد أولاً من تبويب 'تحميل العقد'")
            else:
                if st.button("استخراج البنود من العقد"):
                    with st.spinner("جاري استخراج البنود..."):
                        # استخراج النص من الملف
                        extracted_text = self._extract_text_from_file(self.uploaded_files["contract"])
                        
                        # حفظ النص المستخرج
                        self.analysis_results["contract_text"] = extracted_text
                        
                        # استخراج البنود باستخدام الذكاء الاصطناعي
                        clauses_prompt = f"""
                        قم بتحليل نص العقد التالي واستخراج البنود المهمة التالية:
                        1. الأطراف المتعاقدة
                        2. موضوع العقد
                        3. مدة العقد
                        4. قيمة العقد
                        5. شروط الدفع
                        6. الالتزامات والمسؤوليات
                        7. شروط الإنهاء
                        8. تسوية النزاعات
                        9. القانون الحاكم
                        10. أي بنود أخرى مهمة
                        
                        نص العقد:
                        {extracted_text[:4000]}
                        """
                        
                        # الحصول على البنود من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            clauses_result = self._get_anthropic_response(clauses_prompt)
                        else:
                            clauses_result = self._get_ai_response(clauses_prompt)
                        
                        # حفظ البنود المستخرجة
                        self.analysis_results["contract_clauses"] = clauses_result
                        
                        # عرض البنود المستخرجة
                        st.markdown("### البنود المستخرجة")
                        st.markdown(clauses_result)
                        
                        st.success("تم استخراج البنود بنجاح!")
                
                # إذا كانت البنود قد تم استخراجها بالفعل، عرضها
                if "contract_clauses" in self.analysis_results:
                    st.markdown("### البنود المستخرجة")
                    st.markdown(self.analysis_results["contract_clauses"])
        
        # تبويب تحليل المخاطر
        with contract_tabs[2]:
            st.markdown("#### تحليل المخاطر")
            
            if "contract_clauses" not in self.analysis_results:
                st.info("الرجاء استخراج البنود أولاً من تبويب 'استخراج البنود'")
            else:
                if st.button("تحليل المخاطر في العقد"):
                    with st.spinner("جاري تحليل المخاطر..."):
                        # تحليل المخاطر باستخدام الذكاء الاصطناعي
                        risks_prompt = f"""
                        بناءً على البنود المستخرجة من العقد، قم بتحليل المخاطر المحتملة:
                        1. المخاطر القانونية
                        2. المخاطر المالية
                        3. مخاطر التنفيذ
                        4. مخاطر الجدول الزمني
                        5. أي مخاطر أخرى
                        
                        لكل مخاطرة، قدم:
                        - وصف المخاطرة
                        - احتمالية حدوثها (منخفضة، متوسطة، عالية)
                        - تأثيرها (منخفض، متوسط، عالي)
                        - توصيات للتخفيف من المخاطرة
                        
                        البنود المستخرجة:
                        {self.analysis_results["contract_clauses"]}
                        """
                        
                        # الحصول على تحليل المخاطر من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            risks_result = self._get_anthropic_response(risks_prompt)
                        else:
                            risks_result = self._get_ai_response(risks_prompt)
                        
                        # حفظ تحليل المخاطر
                        self.analysis_results["contract_risks"] = risks_result
                        
                        # عرض تحليل المخاطر
                        st.markdown("### تحليل المخاطر")
                        st.markdown(risks_result)
                        
                        st.success("تم تحليل المخاطر بنجاح!")
                
                # إذا كان تحليل المخاطر قد تم بالفعل، عرضه
                if "contract_risks" in self.analysis_results:
                    st.markdown("### تحليل المخاطر")
                    st.markdown(self.analysis_results["contract_risks"])
        
        # تبويب التقرير النهائي
        with contract_tabs[3]:
            st.markdown("#### التقرير النهائي")
            
            if "contract_risks" not in self.analysis_results:
                st.info("الرجاء تحليل المخاطر أولاً من تبويب 'تحليل المخاطر'")
            else:
                if st.button("إنشاء التقرير النهائي"):
                    with st.spinner("جاري إنشاء التقرير النهائي..."):
                        # إنشاء التقرير النهائي باستخدام الذكاء الاصطناعي
                        report_prompt = f"""
                        بناءً على البنود المستخرجة وتحليل المخاطر، قم بإنشاء تقرير نهائي يتضمن:
                        1. ملخص تنفيذي
                        2. تحليل البنود الرئيسية
                        3. تحليل المخاطر
                        4. التوصيات
                        5. الخلاصة
                        
                        البنود المستخرجة:
                        {self.analysis_results["contract_clauses"]}
                        
                        تحليل المخاطر:
                        {self.analysis_results["contract_risks"]}
                        """
                        
                        # الحصول على التقرير النهائي من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            report_result = self._get_anthropic_response(report_prompt)
                        else:
                            report_result = self._get_ai_response(report_prompt)
                        
                        # حفظ التقرير النهائي
                        self.analysis_results["contract_report"] = report_result
                        
                        # عرض التقرير النهائي
                        st.markdown("### التقرير النهائي")
                        st.markdown(report_result)
                        
                        st.success("تم إنشاء التقرير النهائي بنجاح!")
                
                # إذا كان التقرير النهائي قد تم إنشاؤه بالفعل، عرضه
                if "contract_report" in self.analysis_results:
                    st.markdown("### التقرير النهائي")
                    st.markdown(self.analysis_results["contract_report"])
                    
                    # زر لتصدير التقرير
                    report_content = f"""
                    # تقرير تحليل العقد
                    
                    ## معلومات الملف
                    - اسم الملف: {self.uploaded_files["contract"].name}
                    - نوع الملف: {self.uploaded_files["contract"].type}
                    - حجم الملف: {self.uploaded_files["contract"].size} بايت
                    
                    ## البنود المستخرجة
                    {self.analysis_results["contract_clauses"]}
                    
                    ## تحليل المخاطر
                    {self.analysis_results["contract_risks"]}
                    
                    ## التقرير النهائي
                    {self.analysis_results["contract_report"]}
                    
                    ## تم إنشاء هذا التقرير بواسطة مساعد الذكاء الاصطناعي
                    تاريخ الإنشاء: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
                    """
                    
                    st.download_button(
                        label="تصدير التقرير (PDF)",
                        data=report_content.encode('utf-8'),
                        file_name=f"تقرير_تحليل_العقد_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        key="export_contract_report_pdf"
                    )
    
    def _render_cost_estimation_tab(self):
        """عرض تبويب تقدير التكاليف باستخدام نماذج هجين فيس"""
        
        st.markdown("### تقدير التكاليف")
        
        st.markdown("""
        يمكنك استخدام هذه الأداة لتقدير تكاليف المشاريع باستخدام نماذج الذكاء الاصطناعي المتقدمة من بيئة هجين فيس.
        الأداة تدعم تحليل الملفات التالية:
        - ملفات PDF (كراسات الشروط، المواصفات الفنية)
        - ملفات DWG (المخططات الهندسية)
        - ملفات Excel (جداول الكميات، التكاليف)
        - ملفات Word (العقود، المستندات)
        - ملفات النصوص TXT
        - ملفات الصور (PNG, JPG) للمخططات والرسومات
        """)
        
        # إنشاء تبويبات فرعية
        cost_tabs = st.tabs([
            "تحميل الملفات",
            "تقدير التكاليف",
            "تحليل البنود",
            "المقارنة مع السوق",
            "التقارير"
        ])
        
        # تبويب تحميل الملفات
        with cost_tabs[0]:
            st.markdown("#### تحميل ملفات المشروع")
            
            uploaded_files = st.file_uploader(
                "اختر ملفات المشروع للتحليل",
                type=["pdf", "dwg", "xlsx", "docx", "txt", "png", "jpg"],
                accept_multiple_files=True,
                key="cost_files_uploader"
            )
            
            if uploaded_files:
                st.write("### الملفات المرفوعة")
                
                for uploaded_file in uploaded_files:
                    file_details = {
                        "filename": uploaded_file.name,
                        "filetype": uploaded_file.type,
                        "filesize": uploaded_file.size
                    }
                    
                    # حفظ الملف في الذاكرة المؤقتة
                    self.uploaded_files[uploaded_file.name] = uploaded_file
                    
                    # عرض تفاصيل الملف
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                    with col1:
                        st.write(f"**{file_details['filename']}**")
                    with col2:
                        st.write(f"النوع: {self._detect_file_type(file_details['filename'])}")
                    with col3:
                        st.write(f"الحجم: {file_details['filesize']} بايت")
                    with col4:
                        if st.button("حذف", key=f"delete_{file_details['filename']}"):
                            del self.uploaded_files[file_details['filename']]
                            st.rerun()  # تم تعديل هذا من st.experimental_rerun()
                
                st.success(f"تم تحميل {len(uploaded_files)} ملف بنجاح!")
        
        # تبويب تقدير التكاليف
        with cost_tabs[1]:
            st.markdown("#### تقدير التكاليف")
            
            if not self.uploaded_files:
                st.info("الرجاء تحميل ملفات المشروع أولاً من تبويب 'تحميل الملفات'")
            else:
                # نموذج إدخال معلومات المشروع
                st.markdown("### معلومات المشروع")
                
                col1, col2 = st.columns(2)
                with col1:
                    project_name = st.text_input("اسم المشروع")
                    project_location = st.text_input("موقع المشروع")
                    project_type = st.selectbox(
                        "نوع المشروع",
                        ["سكني", "تجاري", "صناعي", "بنية تحتية", "آخر"]
                    )
                
                with col2:
                    project_area = st.number_input("مساحة المشروع (م²)", min_value=0.0, step=100.0)
                    project_duration = st.number_input("مدة المشروع (بالأشهر)", min_value=1, step=1)
                    project_quality = st.select_slider(
                        "مستوى الجودة",
                        options=["اقتصادي", "متوسط", "عالي", "فاخر"]
                    )
                
                # زر لبدء تقدير التكاليف
                if st.button("تقدير التكاليف"):
                    with st.spinner("جاري تقدير التكاليف..."):
                        # إنشاء تقدير التكاليف باستخدام الذكاء الاصطناعي
                        
                        # تجميع معلومات المشروع
                        project_info = f"""
                        اسم المشروع: {project_name}
                        موقع المشروع: {project_location}
                        نوع المشروع: {project_type}
                        مساحة المشروع: {project_area} م²
                        مدة المشروع: {project_duration} أشهر
                        مستوى الجودة: {project_quality}
                        
                        الملفات المرفوعة:
                        {', '.join(self.uploaded_files.keys())}
                        """
                        
                        # إنشاء تقدير التكاليف
                        estimation_prompt = f"""
                        أنت خبير في تقدير تكاليف مشاريع البناء في المملكة العربية السعودية.
                        قم بتقدير تكاليف المشروع التالي بناءً على المعلومات المقدمة:
                        
                        {project_info}
                        
                        قدم تقديرًا مفصلاً للتكاليف يتضمن:
                        1. تكلفة المواد الرئيسية (الخرسانة، حديد التسليح، الطوب، إلخ)
                        2. تكلفة العمالة
                        3. تكلفة المعدات
                        4. التكاليف غير المباشرة
                        5. هامش الربح المقترح
                        6. إجمالي التكلفة المقدرة
                        7. تكلفة المتر المربع
                        
                        استخدم أسعار السوق الحالية في المملكة العربية السعودية لعام 2025.
                        """
                        
                        # الحصول على تقدير التكاليف من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            estimation_result = self._get_anthropic_response(estimation_prompt)
                        else:
                            estimation_result = self._get_ai_response(estimation_prompt)
                        
                        # حفظ تقدير التكاليف
                        self.analysis_results["cost_estimation"] = estimation_result
                        
                        # عرض تقدير التكاليف
                        st.markdown("### تقدير التكاليف")
                        st.markdown(estimation_result)
                        
                        st.success("تم تقدير التكاليف بنجاح!")
                
                # إذا كان تقدير التكاليف قد تم بالفعل، عرضه
                if "cost_estimation" in self.analysis_results:
                    st.markdown("### تقدير التكاليف")
                    st.markdown(self.analysis_results["cost_estimation"])
                    
                    # زر لتصدير التقرير
                    st.download_button(
                        label="تصدير التقرير (PDF)",
                        data="تقرير تقدير التكاليف".encode('utf-8'),  # تم تعديل هذا من b"تقرير تقدير التكاليف"
                        file_name=f"تقرير_تقدير_التكاليف_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        key="export_cost_report_pdf"
                    )
                    
                    st.download_button(
                        label="تصدير البيانات (Excel)",
                        data="بيانات تقدير التكاليف".encode('utf-8'),  # تم تعديل هذا من b"بيانات تقدير التكاليف"
                        file_name=f"بيانات_تقدير_التكاليف_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="export_cost_data_excel"
                    )
        
        # تبويب تحليل البنود
        with cost_tabs[2]:
            st.markdown("#### تحليل البنود")
            
            if "cost_estimation" not in self.analysis_results:
                st.info("الرجاء تقدير التكاليف أولاً من تبويب 'تقدير التكاليف'")
            else:
                # إنشاء تحليل البنود باستخدام الذكاء الاصطناعي
                if st.button("تحليل البنود"):
                    with st.spinner("جاري تحليل البنود..."):
                        # تحليل البنود
                        items_prompt = f"""
                        بناءً على تقدير التكاليف التالي، قم بتحليل البنود الرئيسية:
                        
                        {self.analysis_results["cost_estimation"]}
                        
                        قدم تحليلاً مفصلاً للبنود يتضمن:
                        1. البنود ذات التكلفة الأعلى
                        2. البنود التي يمكن تقليل تكلفتها
                        3. البنود التي قد تتغير أسعارها بشكل كبير
                        4. توصيات لتحسين التكلفة الإجمالية
                        
                        قدم البيانات في شكل جدول حيثما أمكن.
                        """
                        
                        # الحصول على تحليل البنود من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            items_result = self._get_anthropic_response(items_prompt)
                        else:
                            items_result = self._get_ai_response(items_prompt)
                        
                        # حفظ تحليل البنود
                        self.analysis_results["items_analysis"] = items_result
                        
                        # عرض تحليل البنود
                        st.markdown("### تحليل البنود")
                        st.markdown(items_result)
                        
                        st.success("تم تحليل البنود بنجاح!")
                
                # إذا كان تحليل البنود قد تم بالفعل، عرضه
                if "items_analysis" in self.analysis_results:
                    st.markdown("### تحليل البنود")
                    st.markdown(self.analysis_results["items_analysis"])
        
        # تبويب المقارنة مع السوق
        with cost_tabs[3]:
            st.markdown("#### المقارنة مع السوق")
            
            if "items_analysis" not in self.analysis_results:
                st.info("الرجاء تحليل البنود أولاً من تبويب 'تحليل البنود'")
            else:
                # إنشاء مقارنة مع السوق باستخدام الذكاء الاصطناعي
                if st.button("مقارنة مع السوق"):
                    with st.spinner("جاري إجراء المقارنة مع السوق..."):
                        # مقارنة مع السوق
                        market_prompt = f"""
                        بناءً على تقدير التكاليف وتحليل البنود التاليين، قم بإجراء مقارنة مع أسعار السوق الحالية في المملكة العربية السعودية:
                        
                        تقدير التكاليف:
                        {self.analysis_results["cost_estimation"]}
                        
                        تحليل البنود:
                        {self.analysis_results["items_analysis"]}
                        
                        قدم مقارنة مفصلة تتضمن:
                        1. مقارنة أسعار المواد الرئيسية مع متوسط أسعار السوق
                        2. مقارنة تكلفة المتر المربع مع المشاريع المماثلة
                        3. تحليل الفروقات وأسبابها
                        4. توصيات للحصول على أفضل الأسعار
                        
                        استخدم أسعار السوق الحالية في المملكة العربية السعودية لعام 2025.
                        """
                        
                        # الحصول على مقارنة مع السوق من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            market_result = self._get_anthropic_response(market_prompt)
                        else:
                            market_result = self._get_ai_response(market_prompt)
                        
                        # حفظ مقارنة مع السوق
                        self.analysis_results["market_comparison"] = market_result
                        
                        # عرض مقارنة مع السوق
                        st.markdown("### المقارنة مع السوق")
                        st.markdown(market_result)
                        
                        st.success("تمت المقارنة مع السوق بنجاح!")
                
                # إذا كانت المقارنة مع السوق قد تمت بالفعل، عرضها
                if "market_comparison" in self.analysis_results:
                    st.markdown("### المقارنة مع السوق")
                    st.markdown(self.analysis_results["market_comparison"])
        
        # تبويب التقارير
        with cost_tabs[4]:
            st.markdown("#### التقارير")
            
            if "market_comparison" not in self.analysis_results:
                st.info("الرجاء إجراء المقارنة مع السوق أولاً من تبويب 'المقارنة مع السوق'")
            else:
                # إنشاء التقرير النهائي
                if st.button("إنشاء التقرير النهائي"):
                    with st.spinner("جاري إنشاء التقرير النهائي..."):
                        # إنشاء التقرير النهائي
                        report_prompt = f"""
                        بناءً على المعلومات التالية، قم بإنشاء تقرير نهائي شامل لتقدير تكاليف المشروع:
                        
                        تقدير التكاليف:
                        {self.analysis_results["cost_estimation"]}
                        
                        تحليل البنود:
                        {self.analysis_results["items_analysis"]}
                        
                        المقارنة مع السوق:
                        {self.analysis_results["market_comparison"]}
                        
                        قدم تقريرًا شاملاً يتضمن:
                        1. ملخص تنفيذي
                        2. معلومات المشروع
                        3. منهجية تقدير التكاليف
                        4. تقدير التكاليف المفصل
                        5. تحليل البنود
                        6. المقارنة مع السوق
                        7. التوصيات
                        8. الخلاصة
                        
                        نسق التقرير بشكل احترافي وقابل للطباعة.
                        """
                        
                        # الحصول على التقرير النهائي من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            report_result = self._get_anthropic_response(report_prompt)
                        else:
                            report_result = self._get_ai_response(report_prompt)
                        
                        # حفظ التقرير النهائي
                        self.analysis_results["final_report"] = report_result
                        
                        # عرض التقرير النهائي
                        st.markdown("### التقرير النهائي")
                        st.markdown(report_result)
                        
                        st.success("تم إنشاء التقرير النهائي بنجاح!")
                
                # إذا كان التقرير النهائي قد تم إنشاؤه بالفعل، عرضه
                if "final_report" in self.analysis_results:
                    st.markdown("### التقرير النهائي")
                    st.markdown(self.analysis_results["final_report"])
                    
                    # اسم ملف التقرير
                    report_file_name = f"تقرير_تقدير_تكاليف_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    # أزرار لتنزيل التقرير بصيغ مختلفة
                    st.download_button(
                        label="تنزيل التقرير (PDF)",
                        data="تقرير تقدير التكاليف".encode('utf-8'),  # تم تعديل هذا من b"تقرير تقدير التكاليف"
                        file_name=f"{report_file_name}.pdf",
                        mime="application/pdf",
                        key="download_report_pdf"
                    )
                    
                    st.download_button(
                        label="تنزيل التقرير (Excel)",
                        data="بيانات تقدير التكاليف".encode('utf-8'),  # تم تعديل هذا من b"بيانات تقدير التكاليف"
                        file_name=f"{report_file_name}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="download_report_excel"
                    )
                    
                    st.download_button(
                        label="تنزيل التقرير (Word)",
                        data="تقرير تقدير التكاليف".encode('utf-8'),  # تم تعديل هذا من b"تقرير تقدير التكاليف"
                        file_name=f"{report_file_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_report_word"
                    )
    
    def _render_risk_analysis_tab(self):
        """عرض تبويب تحليل المخاطر"""
        st.markdown("### تحليل المخاطر")
        
        st.markdown("""
        يمكنك استخدام هذه الأداة لتحليل المخاطر المحتملة في المشاريع باستخدام الذكاء الاصطناعي.
        """)
        
        # إنشاء تبويبات فرعية
        risk_tabs = st.tabs([
            "تحديد المخاطر",
            "تقييم المخاطر",
            "خطة الاستجابة",
            "التقرير النهائي"
        ])
        
        # تبويب تحديد المخاطر
        with risk_tabs[0]:
            st.markdown("#### تحديد المخاطر")
            
            # نموذج إدخال معلومات المشروع
            st.markdown("### معلومات المشروع")
            
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input("اسم المشروع", key="risk_project_name")
                project_location = st.text_input("موقع المشروع", key="risk_project_location")
                project_type = st.selectbox(
                    "نوع المشروع",
                    ["سكني", "تجاري", "صناعي", "بنية تحتية", "آخر"],
                    key="risk_project_type"
                )
            
            with col2:
                project_budget = st.number_input("ميزانية المشروع (ريال سعودي)", min_value=0.0, step=100000.0)
                project_duration = st.number_input("مدة المشروع (بالأشهر)", min_value=1, step=1, key="risk_project_duration")
                project_complexity = st.select_slider(
                    "مستوى تعقيد المشروع",
                    options=["بسيط", "متوسط", "معقد", "معقد جدًا"]
                )
            
            # وصف المشروع
            project_description = st.text_area("وصف المشروع", height=150)
            
            # زر لتحديد المخاطر
            if st.button("تحديد المخاطر"):
                with st.spinner("جاري تحديد المخاطر..."):
                    # تجميع معلومات المشروع
                    project_info = f"""
                    اسم المشروع: {project_name}
                    موقع المشروع: {project_location}
                    نوع المشروع: {project_type}
                    ميزانية المشروع: {project_budget} ريال سعودي
                    مدة المشروع: {project_duration} أشهر
                    مستوى تعقيد المشروع: {project_complexity}
                    
                    وصف المشروع:
                    {project_description}
                    """
                    
                    # تحديد المخاطر باستخدام الذكاء الاصطناعي
                    risks_prompt = f"""
                    أنت خبير في إدارة المخاطر في مشاريع البناء في المملكة العربية السعودية.
                    قم بتحديد المخاطر المحتملة للمشروع التالي:
                    
                    {project_info}
                    
                    حدد المخاطر في الفئات التالية:
                    1. المخاطر الفنية
                    2. المخاطر الإدارية
                    3. المخاطر المالية
                    4. المخاطر التعاقدية
                    5. المخاطر البيئية
                    6. مخاطر الجدول الزمني
                    7. مخاطر الموارد البشرية
                    8. مخاطر الصحة والسلامة
                    9. المخاطر القانونية والتنظيمية
                    10. مخاطر أخرى
                    
                    لكل فئة، قدم قائمة بالمخاطر المحتملة مع وصف موجز لكل مخاطرة.
                    """
                    
                    # الحصول على تحديد المخاطر من النموذج المختار
                    if st.session_state.selected_model == "anthropic":
                        risks_result = self._get_anthropic_response(risks_prompt)
                    else:
                        risks_result = self._get_ai_response(risks_prompt)
                    
                    # حفظ تحديد المخاطر
                    self.analysis_results["identified_risks"] = risks_result
                    
                    # حفظ معلومات المشروع
                    self.analysis_results["risk_project_info"] = project_info
                    
                    # عرض تحديد المخاطر
                    st.markdown("### المخاطر المحددة")
                    st.markdown(risks_result)
                    
                    st.success("تم تحديد المخاطر بنجاح!")
            
            # إذا كان تحديد المخاطر قد تم بالفعل، عرضه
            if "identified_risks" in self.analysis_results:
                st.markdown("### المخاطر المحددة")
                st.markdown(self.analysis_results["identified_risks"])
        
        # تبويب تقييم المخاطر
        with risk_tabs[1]:
            st.markdown("#### تقييم المخاطر")
            
            if "identified_risks" not in self.analysis_results:
                st.info("الرجاء تحديد المخاطر أولاً من تبويب 'تحديد المخاطر'")
            else:
                # زر لتقييم المخاطر
                if st.button("تقييم المخاطر"):
                    with st.spinner("جاري تقييم المخاطر..."):
                        # تقييم المخاطر باستخدام الذكاء الاصطناعي
                        assessment_prompt = f"""
                        بناءً على المخاطر المحددة للمشروع، قم بتقييم كل مخاطرة من حيث:
                        
                        1. احتمالية الحدوث (منخفضة، متوسطة، عالية)
                        2. التأثير (منخفض، متوسط، عالي)
                        3. درجة المخاطرة (منخفضة، متوسطة، عالية، حرجة)
                        
                        معلومات المشروع:
                        {self.analysis_results["risk_project_info"]}
                        
                        المخاطر المحددة:
                        {self.analysis_results["identified_risks"]}
                        
                        قدم تقييمًا مفصلاً لكل مخاطرة في شكل جدول يتضمن:
                        - وصف المخاطرة
                        - الفئة
                        - احتمالية الحدوث
                        - التأثير
                        - درجة المخاطرة
                        
                        ثم قم بترتيب المخاطر حسب درجة المخاطرة من الأعلى إلى الأدنى.
                        """
                        
                        # الحصول على تقييم المخاطر من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            assessment_result = self._get_anthropic_response(assessment_prompt)
                        else:
                            assessment_result = self._get_ai_response(assessment_prompt)
                        
                        # حفظ تقييم المخاطر
                        self.analysis_results["risk_assessment"] = assessment_result
                        
                        # عرض تقييم المخاطر
                        st.markdown("### تقييم المخاطر")
                        st.markdown(assessment_result)
                        
                        st.success("تم تقييم المخاطر بنجاح!")
                
                # إذا كان تقييم المخاطر قد تم بالفعل، عرضه
                if "risk_assessment" in self.analysis_results:
                    st.markdown("### تقييم المخاطر")
                    st.markdown(self.analysis_results["risk_assessment"])
        
        # تبويب خطة الاستجابة
        with risk_tabs[2]:
            st.markdown("#### خطة الاستجابة")
            
            if "risk_assessment" not in self.analysis_results:
                st.info("الرجاء تقييم المخاطر أولاً من تبويب 'تقييم المخاطر'")
            else:
                # زر لإنشاء خطة الاستجابة
                if st.button("إنشاء خطة الاستجابة"):
                    with st.spinner("جاري إنشاء خطة الاستجابة..."):
                        # إنشاء خطة الاستجابة باستخدام الذكاء الاصطناعي
                        response_prompt = f"""
                        بناءً على تقييم المخاطر للمشروع، قم بإنشاء خطة استجابة لكل مخاطرة تتضمن:
                        
                        1. استراتيجية الاستجابة (تجنب، تخفيف، نقل، قبول)
                        2. الإجراءات المحددة
                        3. المسؤول عن التنفيذ
                        4. الموارد المطلوبة
                        5. الجدول الزمني
                        
                        معلومات المشروع:
                        {self.analysis_results["risk_project_info"]}
                        
                        تقييم المخاطر:
                        {self.analysis_results["risk_assessment"]}
                        
                        قدم خطة استجابة مفصلة لكل مخاطرة، مع التركيز على المخاطر ذات الدرجة العالية والحرجة.
                        """
                        
                        # الحصول على خطة الاستجابة من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            response_result = self._get_anthropic_response(response_prompt)
                        else:
                            response_result = self._get_ai_response(response_prompt)
                        
                        # حفظ خطة الاستجابة
                        self.analysis_results["risk_response"] = response_result
                        
                        # عرض خطة الاستجابة
                        st.markdown("### خطة الاستجابة")
                        st.markdown(response_result)
                        
                        st.success("تم إنشاء خطة الاستجابة بنجاح!")
                
                # إذا كانت خطة الاستجابة قد تم إنشاؤها بالفعل، عرضها
                if "risk_response" in self.analysis_results:
                    st.markdown("### خطة الاستجابة")
                    st.markdown(self.analysis_results["risk_response"])
        
        # تبويب التقرير النهائي
        with risk_tabs[3]:
            st.markdown("#### التقرير النهائي")
            
            if "risk_response" not in self.analysis_results:
                st.info("الرجاء إنشاء خطة الاستجابة أولاً من تبويب 'خطة الاستجابة'")
            else:
                # زر لإنشاء التقرير النهائي
                if st.button("إنشاء التقرير النهائي"):
                    with st.spinner("جاري إنشاء التقرير النهائي..."):
                        # إنشاء التقرير النهائي باستخدام الذكاء الاصطناعي
                        report_prompt = f"""
                        بناءً على المعلومات التالية، قم بإنشاء تقرير نهائي شامل لتحليل المخاطر في المشروع:
                        
                        معلومات المشروع:
                        {self.analysis_results["risk_project_info"]}
                        
                        المخاطر المحددة:
                        {self.analysis_results["identified_risks"]}
                        
                        تقييم المخاطر:
                        {self.analysis_results["risk_assessment"]}
                        
                        خطة الاستجابة:
                        {self.analysis_results["risk_response"]}
                        
                        قدم تقريرًا شاملاً يتضمن:
                        1. ملخص تنفيذي
                        2. معلومات المشروع
                        3. منهجية تحليل المخاطر
                        4. المخاطر المحددة
                        5. تقييم المخاطر
                        6. خطة الاستجابة
                        7. خطة المراقبة والتحكم
                        8. التوصيات
                        9. الخلاصة
                        
                        نسق التقرير بشكل احترافي وقابل للطباعة.
                        """
                        
                        # الحصول على التقرير النهائي من النموذج المختار
                        if st.session_state.selected_model == "anthropic":
                            report_result = self._get_anthropic_response(report_prompt)
                        else:
                            report_result = self._get_ai_response(report_prompt)
                        
                        # حفظ التقرير النهائي
                        self.analysis_results["risk_report"] = report_result
                        
                        # عرض التقرير النهائي
                        st.markdown("### التقرير النهائي")
                        st.markdown(report_result)
                        
                        st.success("تم إنشاء التقرير النهائي بنجاح!")
                
                # إذا كان التقرير النهائي قد تم إنشاؤه بالفعل، عرضه
                if "risk_report" in self.analysis_results:
                    st.markdown("### التقرير النهائي")
                    st.markdown(self.analysis_results["risk_report"])
                    
                    # اسم ملف التقرير
                    report_file_name = f"تقرير_تحليل_المخاطر_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                    
                    # أزرار لتنزيل التقرير بصيغ مختلفة
                    st.download_button(
                        label="تنزيل التقرير (PDF)",
                        data="تقرير تحليل المخاطر".encode('utf-8'),  # تم تعديل هذا من b"تقرير تحليل المخاطر"
                        file_name=f"{report_file_name}.pdf",
                        mime="application/pdf",
                        key="download_risk_report_pdf"
                    )
                    
                    st.download_button(
                        label="تنزيل التقرير (Word)",
                        data="تقرير تحليل المخاطر".encode('utf-8'),  # تم تعديل هذا من b"تقرير تحليل المخاطر"
                        file_name=f"{report_file_name}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_risk_report_word"
                    )
    
    def _render_settings_tab(self):
        """عرض تبويب الإعدادات"""
        st.markdown("### الإعدادات")
        
        st.markdown("#### إعدادات نماذج الذكاء الاصطناعي")
        
        # إعدادات مفاتيح API
        st.markdown("##### مفاتيح API")
        
        # مفتاح API لنموذج ai
        ai_api_key = st.text_input(
            "مفتاح API لنموذج ai",
            value=st.session_state.ai_api_key,
            type="password"
        )
        
        # مفتاح API لنموذج anthropic
        anthropic_api_key = st.text_input(
            "مفتاح API لنموذج anthropic",
            value=st.session_state.anthropic_api_key,
            type="password"
        )
        
        # زر لحفظ الإعدادات
        if st.button("حفظ الإعدادات"):
            # تحديث مفاتيح API
            st.session_state.ai_api_key = ai_api_key
            st.session_state.anthropic_api_key = anthropic_api_key
            
            st.success("تم حفظ الإعدادات بنجاح!")
    
    def _get_anthropic_response(self, prompt):
        """الحصول على رد من نموذج anthropic"""
        try:
            # التحقق من وجود مفتاح API
            if not st.session_state.anthropic_api_key:
                return "لم يتم تكوين مفتاح API لنموذج anthropic. يرجى تكوين المفتاح في الإعدادات."
            
            # إنشاء عميل anthropic
            client = anthropic.Anthropic(api_key=st.session_state.anthropic_api_key)
            
            # إرسال الطلب إلى النموذج
            response = client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=4000,
                temperature=0.7,
                system="أنت مساعد ذكي متخصص في تحليل مشاريع البناء والمقاولات في المملكة العربية السعودية. تقدم تحليلات دقيقة وتوصيات عملية بناءً على البيانات المقدمة.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # إرجاع الرد
            return response.content[0].text
        except Exception as e:
            return f"حدث خطأ أثناء الاتصال بنموذج anthropic: {str(e)}"
    
    def _get_ai_response(self, prompt):
        """الحصول على رد من نموذج ai"""
        try:
            # التحقق من وجود مفتاح API
            if not st.session_state.ai_api_key:
                return "لم يتم تكوين مفتاح API لنموذج ai. يرجى تكوين المفتاح في الإعدادات."
            
            # إعداد رأس الطلب
            headers = {
                "Authorization": f"Bearer {st.session_state.ai_api_key}",
                "Content-Type": "application/json"
            }
            
            # إعداد بيانات الطلب
            data = {
                "model": "gpt-4",
                "messages": [
                    {
                        "role": "system",
                        "content": "أنت مساعد ذكي متخصص في تحليل مشاريع البناء والمقاولات في المملكة العربية السعودية. تقدم تحليلات دقيقة وتوصيات عملية بناءً على البيانات المقدمة."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            # إرسال الطلب إلى النموذج
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data
            ) 
            
            # التحقق من نجاح الطلب
            if response.status_code == 200:
                # إرجاع الرد
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"حدث خطأ أثناء الاتصال بنموذج ai: {response.text}"
        except Exception as e:
            return f"حدث خطأ أثناء الاتصال بنموذج ai: {str(e)}"
    
    def _extract_text_from_file(self, file):
        """استخراج النص من الملف"""
        try:
            # تحديد نوع الملف
            file_name = file.name
            file_extension = file_name.split('.')[-1].lower()
            
            # استخراج النص حسب نوع الملف
            if file_extension == 'pdf':
                # استخراج النص من ملف PDF
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
            elif file_extension in ['docx', 'doc']:
                # استخراج النص من ملف Word
                doc = docx.Document(file)
                text = ""
                for para in doc.paragraphs:
                    text += para.text + "\n"
                return text
            elif file_extension == 'txt':
                # استخراج النص من ملف نصي
                return file.getvalue().decode('utf-8')
            else:
                return f"نوع الملف {file_extension} غير مدعوم لاستخراج النص."
        except Exception as e:
            return f"حدث خطأ أثناء استخراج النص من الملف: {str(e)}"
    
    def _detect_file_type(self, file_name):
        """تحديد نوع الملف بناءً على الامتداد"""
        extension = file_name.split('.')[-1].lower()
        
        if extension in ['pdf']:
            return 'application/pdf'
        elif extension in ['dwg']:
            return 'application/acad'
        elif extension in ['xlsx', 'xls']:
            return 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        elif extension in ['docx', 'doc']:
            return 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        elif extension in ['txt']:
            return 'text/plain'
        elif extension in ['png']:
            return 'image/png'
        elif extension in ['jpg', 'jpeg']:
            return 'image/jpeg'
        else:
            return 'application/octet-stream'
