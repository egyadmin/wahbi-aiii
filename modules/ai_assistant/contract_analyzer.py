"""
محلل العقود المتقدم - وحدة تحليل العقود والمناقصات باستخدام الذكاء الاصطناعي

هذا الملف يحتوي على الفئات والدوال اللازمة لتحليل العقود والمناقصات باستخدام نماذج OpenAI وClaude.
"""

import os
import json
import re
import time
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import base64
import io
import streamlit as st

# محاكاة استيراد مكتبات الذكاء الاصطناعي
try:
    import openai
    import anthropic
    from transformers import pipeline
    import torch
    import nltk
    import gensim
    MODELS_AVAILABLE = True
except ImportError:
    MODELS_AVAILABLE = False

class ContractAnalyzer:
    """فئة تحليل العقود والمناقصات باستخدام الذكاء الاصطناعي"""
    
    def __init__(self, api_key_source="security_section"):
        """
        تهيئة محلل العقود
        
        المعلمات:
            api_key_source (str): مصدر مفتاح API، إما "security_section" أو "manual"
        """
        self.api_key_source = api_key_source
        self.openai_api_key = None
        self.claude_api_key = None
        self.hybrid_environment = True
        
        # تهيئة مفاتيح API
        self._initialize_api_keys()
        
        # تهيئة نماذج الذكاء الاصطناعي
        self._initialize_ai_models()
    
    def _initialize_api_keys(self):
        """تهيئة مفاتيح API"""
        if self.api_key_source == "security_section":
            # محاكاة الحصول على مفاتيح API من قسم الأمان
            self.openai_api_key = "sk-security-section-openai-key"
            self.claude_api_key = "sk-security-section-claude-key"
        else:
            # استخدام مفاتيح API المدخلة يدوياً
            self.openai_api_key = st.session_state.get("openai_api_key", "")
            self.claude_api_key = st.session_state.get("claude_api_key", "")
    
    def _initialize_ai_models(self):
        """تهيئة نماذج الذكاء الاصطناعي"""
        if MODELS_AVAILABLE:
            # تهيئة نماذج OpenAI
            if self.openai_api_key:
                openai.api_key = self.openai_api_key
            
            # تهيئة نماذج Claude
            if self.claude_api_key:
                self.claude_client = anthropic.Anthropic(api_key=self.claude_api_key)
            
            # تهيئة نماذج Hugging Face
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            self.ner_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
            
            # تهيئة NLTK
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
    
    def analyze_contract(self, file_path, analysis_type="comprehensive"):
        """
        تحليل العقد باستخدام الذكاء الاصطناعي
        
        المعلمات:
            file_path (str): مسار ملف العقد
            analysis_type (str): نوع التحليل، إما "comprehensive" أو "quick" أو "legal" أو "financial"
            
        العوائد:
            dict: نتائج التحليل
        """
        # استخراج النص من الملف
        contract_text = self._extract_text_from_file(file_path)
        
        # تحليل العقد باستخدام الذكاء الاصطناعي
        if analysis_type == "comprehensive":
            return self._comprehensive_analysis(contract_text, os.path.basename(file_path))
        elif analysis_type == "quick":
            return self._quick_analysis(contract_text, os.path.basename(file_path))
        elif analysis_type == "legal":
            return self._legal_analysis(contract_text, os.path.basename(file_path))
        elif analysis_type == "financial":
            return self._financial_analysis(contract_text, os.path.basename(file_path))
        else:
            return self._comprehensive_analysis(contract_text, os.path.basename(file_path))
    
    def analyze_tender(self, file_path, analysis_type="comprehensive"):
        """
        تحليل المناقصة باستخدام الذكاء الاصطناعي
        
        المعلمات:
            file_path (str): مسار ملف المناقصة
            analysis_type (str): نوع التحليل، إما "comprehensive" أو "quick" أو "technical" أو "financial"
            
        العوائد:
            dict: نتائج التحليل
        """
        # استخراج النص من الملف
        tender_text = self._extract_text_from_file(file_path)
        
        # تحليل المناقصة باستخدام الذكاء الاصطناعي
        if analysis_type == "comprehensive":
            return self._comprehensive_tender_analysis(tender_text, os.path.basename(file_path))
        elif analysis_type == "quick":
            return self._quick_tender_analysis(tender_text, os.path.basename(file_path))
        elif analysis_type == "technical":
            return self._technical_tender_analysis(tender_text, os.path.basename(file_path))
        elif analysis_type == "financial":
            return self._financial_tender_analysis(tender_text, os.path.basename(file_path))
        else:
            return self._comprehensive_tender_analysis(tender_text, os.path.basename(file_path))
    
    def analyze_dwg_file(self, file_path):
        """
        تحليل ملف DWG باستخدام الذكاء الاصطناعي
        
        المعلمات:
            file_path (str): مسار ملف DWG
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل ملف DWG
        return self._simulate_dwg_analysis(file_path)
    
    def compare_contracts(self, file_path1, file_path2):
        """
        مقارنة عقدين باستخدام الذكاء الاصطناعي
        
        المعلمات:
            file_path1 (str): مسار الملف الأول
            file_path2 (str): مسار الملف الثاني
            
        العوائد:
            dict: نتائج المقارنة
        """
        # استخراج النص من الملفين
        text1 = self._extract_text_from_file(file_path1)
        text2 = self._extract_text_from_file(file_path2)
        
        # مقارنة العقدين باستخدام الذكاء الاصطناعي
        return self._compare_documents(text1, text2, os.path.basename(file_path1), os.path.basename(file_path2))
    
    def extract_key_terms(self, file_path):
        """
        استخراج الشروط الرئيسية من العقد
        
        المعلمات:
            file_path (str): مسار ملف العقد
            
        العوائد:
            dict: الشروط الرئيسية المستخرجة
        """
        # استخراج النص من الملف
        contract_text = self._extract_text_from_file(file_path)
        
        # استخراج الشروط الرئيسية باستخدام الذكاء الاصطناعي
        return self._extract_key_terms_from_text(contract_text)
    
    def identify_risks(self, file_path):
        """
        تحديد المخاطر في العقد
        
        المعلمات:
            file_path (str): مسار ملف العقد
            
        العوائد:
            dict: المخاطر المحددة
        """
        # استخراج النص من الملف
        contract_text = self._extract_text_from_file(file_path)
        
        # تحديد المخاطر باستخدام الذكاء الاصطناعي
        return self._identify_risks_in_text(contract_text)
    
    def suggest_improvements(self, file_path):
        """
        اقتراح تحسينات للعقد
        
        المعلمات:
            file_path (str): مسار ملف العقد
            
        العوائد:
            dict: التحسينات المقترحة
        """
        # استخراج النص من الملف
        contract_text = self._extract_text_from_file(file_path)
        
        # اقتراح تحسينات باستخدام الذكاء الاصطناعي
        return self._suggest_improvements_for_text(contract_text)
    
    def _extract_text_from_file(self, file_path):
        """
        استخراج النص من الملف
        
        المعلمات:
            file_path (str): مسار الملف
            
        العوائد:
            str: النص المستخرج
        """
        # محاكاة استخراج النص من الملف
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # محاكاة نص العقد
        if "contract" in file_path.lower() or "عقد" in file_path:
            return """
            عقد إنشاء مبنى إداري
            
            المادة الأولى: أطراف العقد
            الطرف الأول: وزارة المالية، ويمثلها السيد/ أحمد محمد علي، بصفته وكيل الوزارة للمشاريع.
            الطرف الثاني: شركة الإنشاءات المتطورة، ويمثلها السيد/ خالد عبدالله محمد، بصفته المدير العام.
            
            المادة الثانية: موضوع العقد
            يتعهد الطرف الثاني بتنفيذ مشروع إنشاء مبنى إداري لصالح الطرف الأول وفقاً للمواصفات والشروط المرفقة بهذا العقد.
            
            المادة الثالثة: قيمة العقد
            قيمة العقد الإجمالية هي 25,000,000 ريال (خمسة وعشرون مليون ريال) شاملة جميع الضرائب والرسوم.
            
            المادة الرابعة: مدة التنفيذ
            مدة تنفيذ المشروع 18 شهراً تبدأ من تاريخ استلام الموقع.
            
            المادة الخامسة: الدفعات
            يتم سداد قيمة العقد على دفعات شهرية حسب نسبة الإنجاز، مع احتجاز 10% من قيمة كل دفعة كضمان حسن التنفيذ.
            
            المادة السادسة: الضمانات
            يقدم الطرف الثاني ضماناً نهائياً بنسبة 5% من قيمة العقد ساري المفعول حتى انتهاء فترة الضمان.
            
            المادة السابعة: غرامات التأخير
            في حالة تأخر الطرف الثاني عن التنفيذ في الموعد المحدد، يتم تطبيق غرامة تأخير بنسبة 1% من قيمة العقد عن كل أسبوع تأخير بحد أقصى 10% من قيمة العقد.
            
            المادة الثامنة: فترة الضمان
            فترة ضمان المشروع سنة واحدة من تاريخ الاستلام الابتدائي.
            
            المادة التاسعة: فسخ العقد
            يحق للطرف الأول فسخ العقد في حالة إخلال الطرف الثاني بالتزاماته التعاقدية بعد إنذاره كتابياً.
            
            المادة العاشرة: تسوية النزاعات
            في حالة نشوء أي نزاع بين الطرفين، يتم حله ودياً، وفي حالة تعذر ذلك يتم اللجوء إلى التحكيم وفقاً لأنظمة المملكة العربية السعودية.
            
            المادة الحادية عشر: القانون الواجب التطبيق
            تخضع جميع بنود هذا العقد لأنظمة المملكة العربية السعودية.
            
            حرر هذا العقد من نسختين أصليتين بتاريخ 15/03/2024م.
            
            الطرف الأول                                  الطرف الثاني
            وزارة المالية                               شركة الإنشاءات المتطورة
            """
        elif "tender" in file_path.lower() or "مناقصة" in file_path:
            return """
            كراسة الشروط والمواصفات
            مناقصة إنشاء مبنى إداري
            
            أولاً: معلومات المناقصة
            رقم المناقصة: T-2024-001
            الجهة المالكة: وزارة المالية
            موقع المشروع: الرياض - حي العليا
            تاريخ الطرح: 01/03/2024م
            تاريخ الإقفال: 15/04/2024م
            
            ثانياً: وصف المشروع
            يتكون المشروع من إنشاء مبنى إداري مكون من 5 طوابق بمساحة إجمالية 5000 متر مربع. يشمل المشروع الأعمال الإنشائية والمعمارية والكهربائية والميكانيكية وأعمال التشطيبات.
            
            ثالثاً: شروط التأهيل
            1. أن يكون المقاول مصنفاً في مجال المباني من الدرجة الأولى.
            2. أن يكون لديه خبرة سابقة في تنفيذ مشاريع مماثلة لا تقل عن 3 مشاريع خلال الخمس سنوات الماضية.
            3. أن يكون لديه سيولة مالية كافية لتنفيذ المشروع.
            
            رابعاً: الضمانات المطلوبة
            1. ضمان ابتدائي: 2% من قيمة العطاء ساري المفعول لمدة 90 يوماً من تاريخ تقديم العطاء.
            2. ضمان نهائي: 5% من قيمة العقد ساري المفعول حتى انتهاء فترة الضمان.
            
            خامساً: مدة التنفيذ
            مدة تنفيذ المشروع 18 شهراً من تاريخ استلام الموقع.
            
            سادساً: غرامات التأخير
            في حالة تأخر المقاول عن التنفيذ في الموعد المحدد، يتم تطبيق غرامة تأخير بنسبة 1% من قيمة العقد عن كل أسبوع تأخير بحد أقصى 10% من قيمة العقد.
            
            سابعاً: شروط الدفع
            يتم سداد قيمة العقد على دفعات شهرية حسب نسبة الإنجاز، مع احتجاز 10% من قيمة كل دفعة كضمان حسن التنفيذ.
            
            ثامناً: المواصفات الفنية
            1. الأعمال الإنشائية:
               - الخرسانة المسلحة: مقاومة لا تقل عن 300 كجم/سم²
               - حديد التسليح: درجة 60
            
            2. الأعمال المعمارية:
               - الواجهات: زجاج عاكس وحجر طبيعي
               - الأرضيات: رخام للمداخل وبورسلين للمكاتب
               - الأسقف: أسقف مستعارة من الجبس المزخرف
            
            3. الأعمال الكهربائية:
               - نظام إنارة موفر للطاقة
               - نظام إنذار وإطفاء حريق آلي
               - نظام مراقبة بالكاميرات
            
            4. الأعمال الميكانيكية:
               - نظام تكييف مركزي
               - نظام تهوية متطور
               - مصاعد عدد 3
            
            تاسعاً: معايير التقييم
            1. السعر: 50%
            2. الجودة الفنية: 30%
            3. الخبرة السابقة: 15%
            4. مدة التنفيذ: 5%
            
            عاشراً: تقديم العطاءات
            يتم تقديم العطاءات في مظروفين منفصلين (فني ومالي) إلى إدارة المشتريات بوزارة المالية في موعد أقصاه الساعة 12 ظهراً من يوم 15/04/2024م.
            """
        else:
            return """
            محتوى الملف غير معروف. يرجى التأكد من نوع الملف وصيغته.
            """
    
    def _comprehensive_analysis(self, contract_text, file_name):
        """
        تحليل شامل للعقد
        
        المعلمات:
            contract_text (str): نص العقد
            file_name (str): اسم الملف
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل شامل للعقد
        
        # استخراج الأطراف
        parties = self._extract_parties(contract_text)
        
        # استخراج قيمة العقد
        contract_value = self._extract_contract_value(contract_text)
        
        # استخراج مدة التنفيذ
        duration = self._extract_duration(contract_text)
        
        # استخراج الضمانات
        guarantees = self._extract_guarantees(contract_text)
        
        # استخراج غرامات التأخير
        penalties = self._extract_penalties(contract_text)
        
        # استخراج شروط الدفع
        payment_terms = self._extract_payment_terms(contract_text)
        
        # استخراج فترة الضمان
        warranty_period = self._extract_warranty_period(contract_text)
        
        # استخراج شروط فسخ العقد
        termination_terms = self._extract_termination_terms(contract_text)
        
        # استخراج آلية تسوية النزاعات
        dispute_resolution = self._extract_dispute_resolution(contract_text)
        
        # تحديد المخاطر
        risks = self._identify_risks_in_text(contract_text)
        
        # اقتراح تحسينات
        improvements = self._suggest_improvements_for_text(contract_text)
        
        # إعداد النتائج
        results = {
            "title": f"تحليل شامل - {file_name}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": "هذا العقد يتعلق بإنشاء مبنى إداري لصالح وزارة المالية. يتضمن العقد شروطاً متعلقة بقيمة العقد، مدة التنفيذ، الدفعات، الضمانات، غرامات التأخير، فترة الضمان، فسخ العقد، وتسوية النزاعات.",
            "key_points": [
                f"قيمة العقد: {contract_value}",
                f"مدة التنفيذ: {duration}",
                f"الضمانات: {guarantees}",
                f"غرامات التأخير: {penalties}",
                f"شروط الدفع: {payment_terms}",
                f"فترة الضمان: {warranty_period}"
            ],
            "entities": {
                "الأطراف": parties,
                "قيمة العقد": contract_value,
                "مدة التنفيذ": duration,
                "الضمانات": guarantees,
                "غرامات التأخير": penalties,
                "شروط الدفع": payment_terms,
                "فترة الضمان": warranty_period,
                "شروط فسخ العقد": termination_terms,
                "آلية تسوية النزاعات": dispute_resolution
            },
            "risks": risks,
            "improvements": improvements,
            "recommendations": [
                "مراجعة قيمة الضمان النهائي للتأكد من كفايتها",
                "توضيح آلية احتساب نسبة الإنجاز للدفعات الشهرية",
                "إضافة بند يتعلق بالتغييرات في نطاق العمل",
                "توضيح حقوق الملكية الفكرية للتصاميم والمخططات",
                "إضافة بند يتعلق بالقوة القاهرة"
            ]
        }
        
        return results
    
    def _quick_analysis(self, contract_text, file_name):
        """
        تحليل سريع للعقد
        
        المعلمات:
            contract_text (str): نص العقد
            file_name (str): اسم الملف
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل سريع للعقد
        
        # استخراج الأطراف
        parties = self._extract_parties(contract_text)
        
        # استخراج قيمة العقد
        contract_value = self._extract_contract_value(contract_text)
        
        # استخراج مدة التنفيذ
        duration = self._extract_duration(contract_text)
        
        # استخراج الضمانات
        guarantees = self._extract_guarantees(contract_text)
        
        # إعداد النتائج
        results = {
            "title": f"تحليل سريع - {file_name}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": "هذا العقد يتعلق بإنشاء مبنى إداري لصالح وزارة المالية.",
            "key_points": [
                f"قيمة العقد: {contract_value}",
                f"مدة التنفيذ: {duration}",
                f"الضمانات: {guarantees}"
            ],
            "entities": {
                "الأطراف": parties,
                "قيمة العقد": contract_value,
                "مدة التنفيذ": duration,
                "الضمانات": guarantees
            },
            "recommendations": [
                "مراجعة قيمة الضمان النهائي للتأكد من كفايتها",
                "توضيح آلية احتساب نسبة الإنجاز للدفعات الشهرية"
            ]
        }
        
        return results
    
    def _legal_analysis(self, contract_text, file_name):
        """
        تحليل قانوني للعقد
        
        المعلمات:
            contract_text (str): نص العقد
            file_name (str): اسم الملف
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل قانوني للعقد
        
        # استخراج الأطراف
        parties = self._extract_parties(contract_text)
        
        # استخراج الضمانات
        guarantees = self._extract_guarantees(contract_text)
        
        # استخراج غرامات التأخير
        penalties = self._extract_penalties(contract_text)
        
        # استخراج شروط فسخ العقد
        termination_terms = self._extract_termination_terms(contract_text)
        
        # استخراج آلية تسوية النزاعات
        dispute_resolution = self._extract_dispute_resolution(contract_text)
        
        # تحديد المخاطر القانونية
        legal_risks = [
            "عدم وضوح آلية تسوية النزاعات",
            "عدم تحديد المحكمة المختصة",
            "عدم وضوح شروط فسخ العقد",
            "عدم وجود بند يتعلق بالقوة القاهرة",
            "عدم وضوح حقوق الملكية الفكرية"
        ]
        
        # إعداد النتائج
        results = {
            "title": f"تحليل قانوني - {file_name}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": "هذا العقد يتضمن بعض الثغرات القانونية التي قد تؤدي إلى نزاعات مستقبلية.",
            "key_points": [
                f"الضمانات: {guarantees}",
                f"غرامات التأخير: {penalties}",
                f"شروط فسخ العقد: {termination_terms}",
                f"آلية تسوية النزاعات: {dispute_resolution}"
            ],
            "entities": {
                "الأطراف": parties,
                "الضمانات": guarantees,
                "غرامات التأخير": penalties,
                "شروط فسخ العقد": termination_terms,
                "آلية تسوية النزاعات": dispute_resolution
            },
            "legal_risks": legal_risks,
            "recommendations": [
                "توضيح آلية تسوية النزاعات وتحديد المحكمة المختصة",
                "إضافة بند يتعلق بالقوة القاهرة",
                "توضيح شروط فسخ العقد بشكل أكثر تفصيلاً",
                "إضافة بند يتعلق بحقوق الملكية الفكرية",
                "توضيح آلية تعديل العقد"
            ]
        }
        
        return results
    
    def _financial_analysis(self, contract_text, file_name):
        """
        تحليل مالي للعقد
        
        المعلمات:
            contract_text (str): نص العقد
            file_name (str): اسم الملف
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل مالي للعقد
        
        # استخراج قيمة العقد
        contract_value = self._extract_contract_value(contract_text)
        
        # استخراج شروط الدفع
        payment_terms = self._extract_payment_terms(contract_text)
        
        # استخراج الضمانات
        guarantees = self._extract_guarantees(contract_text)
        
        # استخراج غرامات التأخير
        penalties = self._extract_penalties(contract_text)
        
        # تحليل التدفقات النقدية
        cash_flow = [
            {"month": 1, "income": 1250000, "expense": 1000000, "net": 250000},
            {"month": 2, "income": 1250000, "expense": 1100000, "net": 150000},
            {"month": 3, "income": 1250000, "expense": 1200000, "net": 50000},
            {"month": 4, "income": 1250000, "expense": 1000000, "net": 250000},
            {"month": 5, "income": 1250000, "expense": 900000, "net": 350000},
            {"month": 6, "income": 1250000, "expense": 950000, "net": 300000}
        ]
        
        # تحليل المخاطر المالية
        financial_risks = [
            "تأخر الدفعات",
            "زيادة أسعار المواد",
            "نقص السيولة",
            "تغير أسعار العملات",
            "زيادة تكاليف العمالة"
        ]
        
        # إعداد النتائج
        results = {
            "title": f"تحليل مالي - {file_name}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": f"هذا العقد بقيمة {contract_value} يتضمن شروط دفع شهرية حسب نسبة الإنجاز مع احتجاز 10% من قيمة كل دفعة كضمان حسن التنفيذ.",
            "key_points": [
                f"قيمة العقد: {contract_value}",
                f"شروط الدفع: {payment_terms}",
                f"الضمانات: {guarantees}",
                f"غرامات التأخير: {penalties}"
            ],
            "entities": {
                "قيمة العقد": contract_value,
                "شروط الدفع": payment_terms,
                "الضمانات": guarantees,
                "غرامات التأخير": penalties
            },
            "cash_flow": cash_flow,
            "financial_risks": financial_risks,
            "recommendations": [
                "توضيح آلية احتساب نسبة الإنجاز للدفعات الشهرية",
                "إضافة بند يتعلق بتعديل قيمة العقد في حالة تغير أسعار المواد",
                "تقليل نسبة احتجاز ضمان حسن التنفيذ",
                "إضافة بند يتعلق بالدفعة المقدمة",
                "توضيح آلية تسوية المستخلصات النهائية"
            ]
        }
        
        return results
    
    def _comprehensive_tender_analysis(self, tender_text, file_name):
        """
        تحليل شامل للمناقصة
        
        المعلمات:
            tender_text (str): نص المناقصة
            file_name (str): اسم الملف
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل شامل للمناقصة
        
        # استخراج معلومات المناقصة
        tender_info = self._extract_tender_info(tender_text)
        
        # استخراج وصف المشروع
        project_description = self._extract_project_description(tender_text)
        
        # استخراج شروط التأهيل
        qualification_conditions = self._extract_qualification_conditions(tender_text)
        
        # استخراج الضمانات المطلوبة
        required_guarantees = self._extract_required_guarantees(tender_text)
        
        # استخراج مدة التنفيذ
        duration = self._extract_duration(tender_text)
        
        # استخراج غرامات التأخير
        penalties = self._extract_penalties(tender_text)
        
        # استخراج شروط الدفع
        payment_terms = self._extract_payment_terms(tender_text)
        
        # استخراج المواصفات الفنية
        technical_specifications = self._extract_technical_specifications(tender_text)
        
        # استخراج معايير التقييم
        evaluation_criteria = self._extract_evaluation_criteria(tender_text)
        
        # تحليل المنافسة
        competition_analysis = self._analyze_competition(tender_info)
        
        # تحليل المخاطر
        risk_analysis = self._analyze_risks(tender_text)
        
        # تحليل الفرص
        opportunity_analysis = self._analyze_opportunities(tender_text)
        
        # إعداد النتائج
        results = {
            "title": f"تحليل شامل - {file_name}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": f"هذه المناقصة تتعلق بإنشاء مبنى إداري لصالح وزارة المالية. تتضمن المناقصة شروطاً متعلقة بالتأهيل، الضمانات، مدة التنفيذ، غرامات التأخير، شروط الدفع، المواصفات الفنية، ومعايير التقييم.",
            "key_points": [
                f"رقم المناقصة: {tender_info.get('رقم المناقصة', 'غير محدد')}",
                f"الجهة المالكة: {tender_info.get('الجهة المالكة', 'غير محدد')}",
                f"موقع المشروع: {tender_info.get('موقع المشروع', 'غير محدد')}",
                f"تاريخ الطرح: {tender_info.get('تاريخ الطرح', 'غير محدد')}",
                f"تاريخ الإقفال: {tender_info.get('تاريخ الإقفال', 'غير محدد')}",
                f"مدة التنفيذ: {duration}",
                f"الضمانات المطلوبة: {required_guarantees}"
            ],
            "entities": {
                "معلومات المناقصة": tender_info,
                "وصف المشروع": project_description,
                "شروط التأهيل": qualification_conditions,
                "الضمانات المطلوبة": required_guarantees,
                "مدة التنفيذ": duration,
                "غرامات التأخير": penalties,
                "شروط الدفع": payment_terms,
                "المواصفات الفنية": technical_specifications,
                "معايير التقييم": evaluation_criteria
            },
            "competition_analysis": competition_analysis,
            "risk_analysis": risk_analysis,
            "opportunity_analysis": opportunity_analysis,
            "recommendations": [
                "تقديم عرض سعر تنافسي يقل بنسبة 5-10% عن الميزانية التقديرية",
                "التركيز على الجوانب الفنية في العرض",
                "إبراز الخبرات السابقة في مشاريع مماثلة",
                "تقديم جدول زمني مفصل للتنفيذ",
                "تقديم حلول مبتكرة لتقليل التكاليف وزيادة الجودة"
            ]
        }
        
        return results
    
    def _quick_tender_analysis(self, tender_text, file_name):
        """
        تحليل سريع للمناقصة
        
        المعلمات:
            tender_text (str): نص المناقصة
            file_name (str): اسم الملف
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل سريع للمناقصة
        
        # استخراج معلومات المناقصة
        tender_info = self._extract_tender_info(tender_text)
        
        # استخراج وصف المشروع
        project_description = self._extract_project_description(tender_text)
        
        # استخراج مدة التنفيذ
        duration = self._extract_duration(tender_text)
        
        # استخراج الضمانات المطلوبة
        required_guarantees = self._extract_required_guarantees(tender_text)
        
        # إعداد النتائج
        results = {
            "title": f"تحليل سريع - {file_name}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": f"هذه المناقصة تتعلق بإنشاء مبنى إداري لصالح وزارة المالية.",
            "key_points": [
                f"رقم المناقصة: {tender_info.get('رقم المناقصة', 'غير محدد')}",
                f"الجهة المالكة: {tender_info.get('الجهة المالكة', 'غير محدد')}",
                f"موقع المشروع: {tender_info.get('موقع المشروع', 'غير محدد')}",
                f"تاريخ الإقفال: {tender_info.get('تاريخ الإقفال', 'غير محدد')}",
                f"مدة التنفيذ: {duration}"
            ],
            "entities": {
                "معلومات المناقصة": tender_info,
                "وصف المشروع": project_description,
                "مدة التنفيذ": duration,
                "الضمانات المطلوبة": required_guarantees
            },
            "recommendations": [
                "تقديم عرض سعر تنافسي",
                "إبراز الخبرات السابقة في مشاريع مماثلة"
            ]
        }
        
        return results
    
    def _technical_tender_analysis(self, tender_text, file_name):
        """
        تحليل فني للمناقصة
        
        المعلمات:
            tender_text (str): نص المناقصة
            file_name (str): اسم الملف
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل فني للمناقصة
        
        # استخراج وصف المشروع
        project_description = self._extract_project_description(tender_text)
        
        # استخراج المواصفات الفنية
        technical_specifications = self._extract_technical_specifications(tender_text)
        
        # استخراج مدة التنفيذ
        duration = self._extract_duration(tender_text)
        
        # تحليل المتطلبات الفنية
        technical_requirements_analysis = self._analyze_technical_requirements(technical_specifications)
        
        # تحليل المخاطر الفنية
        technical_risks = self._analyze_technical_risks(technical_specifications)
        
        # إعداد النتائج
        results = {
            "title": f"تحليل فني - {file_name}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": f"هذه المناقصة تتضمن متطلبات فنية متوسطة المستوى. المشروع يتكون من إنشاء مبنى إداري مكون من 5 طوابق بمساحة إجمالية 5000 متر مربع.",
            "key_points": [
                f"وصف المشروع: {project_description}",
                f"مدة التنفيذ: {duration}",
                "المواصفات الفنية تشمل الأعمال الإنشائية والمعمارية والكهربائية والميكانيكية"
            ],
            "entities": {
                "وصف المشروع": project_description,
                "المواصفات الفنية": technical_specifications,
                "مدة التنفيذ": duration
            },
            "technical_requirements_analysis": technical_requirements_analysis,
            "technical_risks": technical_risks,
            "recommendations": [
                "التركيز على الجوانب الفنية في العرض",
                "تقديم حلول مبتكرة لتحسين الجودة",
                "تقديم جدول زمني مفصل للتنفيذ",
                "اقتراح بدائل فنية لتقليل التكاليف",
                "تقديم خطة ضمان الجودة"
            ]
        }
        
        return results
    
    def _financial_tender_analysis(self, tender_text, file_name):
        """
        تحليل مالي للمناقصة
        
        المعلمات:
            tender_text (str): نص المناقصة
            file_name (str): اسم الملف
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل مالي للمناقصة
        
        # استخراج معلومات المناقصة
        tender_info = self._extract_tender_info(tender_text)
        
        # استخراج وصف المشروع
        project_description = self._extract_project_description(tender_text)
        
        # استخراج الضمانات المطلوبة
        required_guarantees = self._extract_required_guarantees(tender_text)
        
        # استخراج شروط الدفع
        payment_terms = self._extract_payment_terms(tender_text)
        
        # استخراج غرامات التأخير
        penalties = self._extract_penalties(tender_text)
        
        # تقدير التكاليف
        cost_estimation = self._estimate_costs(project_description)
        
        # تحليل التدفقات النقدية
        cash_flow = self._analyze_cash_flow(payment_terms, cost_estimation)
        
        # تحليل المخاطر المالية
        financial_risks = self._analyze_financial_risks(tender_text)
        
        # إعداد النتائج
        results = {
            "title": f"تحليل مالي - {file_name}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": f"هذه المناقصة تتطلب ضماناً ابتدائياً بنسبة 2% من قيمة العطاء وضماناً نهائياً بنسبة 5% من قيمة العقد. شروط الدفع هي دفعات شهرية حسب نسبة الإنجاز مع احتجاز 10% من قيمة كل دفعة.",
            "key_points": [
                f"الضمانات المطلوبة: {required_guarantees}",
                f"شروط الدفع: {payment_terms}",
                f"غرامات التأخير: {penalties}",
                f"تقدير التكلفة الإجمالية: {cost_estimation.get('total_cost', 0):,} ريال"
            ],
            "entities": {
                "معلومات المناقصة": tender_info,
                "الضمانات المطلوبة": required_guarantees,
                "شروط الدفع": payment_terms,
                "غرامات التأخير": penalties
            },
            "cost_estimation": cost_estimation,
            "cash_flow": cash_flow,
            "financial_risks": financial_risks,
            "recommendations": [
                "تقديم عرض سعر يقل بنسبة 5-10% عن الميزانية التقديرية",
                "طلب دفعة مقدمة لتحسين التدفق النقدي",
                "تقليل نسبة احتجاز ضمان حسن التنفيذ",
                "تقديم بدائل لتقليل التكاليف",
                "وضع خطة للتعامل مع المخاطر المالية"
            ]
        }
        
        return results
    
    def _simulate_dwg_analysis(self, file_path):
        """
        محاكاة تحليل ملف DWG
        
        المعلمات:
            file_path (str): مسار ملف DWG
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل ملف DWG
        results = {
            "file_name": os.path.basename(file_path),
            "file_size": f"{np.random.randint(1, 10)} MB",
            "elements_count": np.random.randint(100, 1000),
            "layers_count": np.random.randint(5, 20),
            "dimensions": {
                "width": f"{np.random.randint(10, 100)} م",
                "height": f"{np.random.randint(10, 100)} م",
                "area": f"{np.random.randint(100, 10000)} م²"
            },
            "elements": {
                "walls": np.random.randint(10, 100),
                "doors": np.random.randint(5, 50),
                "windows": np.random.randint(5, 50),
                "columns": np.random.randint(5, 50),
                "stairs": np.random.randint(1, 10)
            },
            "materials": [
                {"name": "خرسانة", "volume": f"{np.random.randint(10, 1000)} م³"},
                {"name": "حديد", "weight": f"{np.random.randint(1, 100)} طن"},
                {"name": "طابوق", "count": f"{np.random.randint(1000, 10000)} قطعة"},
                {"name": "زجاج", "area": f"{np.random.randint(10, 1000)} م²"},
                {"name": "خشب", "volume": f"{np.random.randint(1, 50)} م³"}
            ],
            "cost_estimate": {
                "materials": np.random.randint(100000, 1000000),
                "labor": np.random.randint(50000, 500000),
                "equipment": np.random.randint(10000, 100000),
                "total": np.random.randint(200000, 2000000)
            },
            "recommendations": [
                "يمكن تقليل تكلفة المواد باستخدام بدائل أقل تكلفة",
                "يمكن تحسين كفاءة استخدام المساحة",
                "يمكن تقليل عدد الأعمدة لتوفير التكلفة",
                "يمكن تحسين تصميم السلالم لزيادة السلامة",
                "يمكن تحسين توزيع النوافذ لزيادة الإضاءة الطبيعية"
            ]
        }
        
        return results
    
    def _compare_documents(self, text1, text2, file_name1, file_name2):
        """
        مقارنة مستندين
        
        المعلمات:
            text1 (str): نص المستند الأول
            text2 (str): نص المستند الثاني
            file_name1 (str): اسم الملف الأول
            file_name2 (str): اسم الملف الثاني
            
        العوائد:
            dict: نتائج المقارنة
        """
        # محاكاة مقارنة مستندين
        
        # تحليل المستند الأول
        doc1_analysis = self._quick_analysis(text1, file_name1)
        
        # تحليل المستند الثاني
        doc2_analysis = self._quick_analysis(text2, file_name2)
        
        # تحديد أوجه التشابه
        similarities = [
            "كلا المستندين يتعلقان بمشاريع إنشائية",
            "كلا المستندين يتضمنان شروطاً متعلقة بالضمانات",
            "كلا المستندين يتضمنان شروطاً متعلقة بغرامات التأخير",
            "كلا المستندين يتضمنان شروطاً متعلقة بشروط الدفع"
        ]
        
        # تحديد أوجه الاختلاف
        differences = [
            "المستند الأول يتعلق بعقد إنشاء، بينما المستند الثاني يتعلق بمناقصة",
            "قيمة الضمان النهائي في المستند الأول 5%، بينما في المستند الثاني 10%",
            "مدة التنفيذ في المستند الأول 18 شهراً، بينما في المستند الثاني 24 شهراً",
            "شروط الدفع في المستند الأول تتضمن دفعة مقدمة، بينما في المستند الثاني لا توجد دفعة مقدمة"
        ]
        
        # إعداد النتائج
        results = {
            "title": f"مقارنة بين {file_name1} و {file_name2}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "summary": "هذه المقارنة تظهر أوجه التشابه والاختلاف بين المستندين. يتشابه المستندان في كونهما يتعلقان بمشاريع إنشائية ويتضمنان شروطاً متعلقة بالضمانات وغرامات التأخير وشروط الدفع. ومع ذلك، هناك اختلافات في نوع المستند وقيمة الضمان النهائي ومدة التنفيذ وشروط الدفع.",
            "document1": {
                "title": doc1_analysis.get("title", ""),
                "summary": doc1_analysis.get("summary", ""),
                "key_points": doc1_analysis.get("key_points", [])
            },
            "document2": {
                "title": doc2_analysis.get("title", ""),
                "summary": doc2_analysis.get("summary", ""),
                "key_points": doc2_analysis.get("key_points", [])
            },
            "similarities": similarities,
            "differences": differences,
            "recommendations": [
                "مراجعة الاختلافات في قيمة الضمان النهائي",
                "مراجعة الاختلافات في مدة التنفيذ",
                "مراجعة الاختلافات في شروط الدفع",
                "توحيد الشروط في المستندين إذا كانا يتعلقان بنفس المشروع"
            ]
        }
        
        return results
    
    def _extract_key_terms_from_text(self, text):
        """
        استخراج الشروط الرئيسية من النص
        
        المعلمات:
            text (str): نص العقد
            
        العوائد:
            dict: الشروط الرئيسية المستخرجة
        """
        # محاكاة استخراج الشروط الرئيسية
        key_terms = {
            "الأطراف": self._extract_parties(text),
            "قيمة العقد": self._extract_contract_value(text),
            "مدة التنفيذ": self._extract_duration(text),
            "الضمانات": self._extract_guarantees(text),
            "غرامات التأخير": self._extract_penalties(text),
            "شروط الدفع": self._extract_payment_terms(text),
            "فترة الضمان": self._extract_warranty_period(text),
            "شروط فسخ العقد": self._extract_termination_terms(text),
            "آلية تسوية النزاعات": self._extract_dispute_resolution(text)
        }
        
        return key_terms
    
    def _identify_risks_in_text(self, text):
        """
        تحديد المخاطر في النص
        
        المعلمات:
            text (str): نص العقد
            
        العوائد:
            list: المخاطر المحددة
        """
        # محاكاة تحديد المخاطر
        risks = [
            {"risk": "ارتفاع أسعار المواد", "probability": "متوسطة", "impact": "عالي", "mitigation": "تثبيت أسعار المواد الرئيسية مع الموردين"},
            {"risk": "تأخر التنفيذ", "probability": "متوسطة", "impact": "عالي", "mitigation": "وضع خطة تنفيذ مفصلة مع هوامش زمنية"},
            {"risk": "نقص العمالة الماهرة", "probability": "منخفضة", "impact": "متوسط", "mitigation": "التعاقد المسبق مع مقاولي الباطن"},
            {"risk": "تغيير نطاق العمل", "probability": "متوسطة", "impact": "عالي", "mitigation": "توثيق نطاق العمل بدقة وتحديد إجراءات التغيير"},
            {"risk": "مشاكل في التربة", "probability": "منخفضة", "impact": "عالي", "mitigation": "إجراء فحوصات شاملة للتربة قبل البدء"}
        ]
        
        return risks
    
    def _suggest_improvements_for_text(self, text):
        """
        اقتراح تحسينات للنص
        
        المعلمات:
            text (str): نص العقد
            
        العوائد:
            list: التحسينات المقترحة
        """
        # محاكاة اقتراح تحسينات
        improvements = [
            "إضافة بند يتعلق بالقوة القاهرة",
            "توضيح آلية تسوية النزاعات وتحديد المحكمة المختصة",
            "إضافة بند يتعلق بحقوق الملكية الفكرية",
            "توضيح آلية تعديل العقد",
            "إضافة بند يتعلق بالتأمين على المشروع",
            "توضيح آلية احتساب نسبة الإنجاز للدفعات الشهرية",
            "إضافة بند يتعلق بالتغييرات في نطاق العمل",
            "توضيح مسؤوليات كل طرف بشكل أكثر تفصيلاً"
        ]
        
        return improvements
    
    def _extract_parties(self, text):
        """استخراج الأطراف من النص"""
        if "الطرف الأول: وزارة المالية" in text:
            return {
                "الطرف الأول": "وزارة المالية",
                "الطرف الثاني": "شركة الإنشاءات المتطورة"
            }
        elif "الجهة المالكة: وزارة المالية" in text:
            return {
                "الجهة المالكة": "وزارة المالية"
            }
        else:
            return {
                "الطرف الأول": "غير محدد",
                "الطرف الثاني": "غير محدد"
            }
    
    def _extract_contract_value(self, text):
        """استخراج قيمة العقد من النص"""
        if "قيمة العقد الإجمالية هي 25,000,000 ريال" in text:
            return "25,000,000 ريال"
        else:
            return "غير محدد"
    
    def _extract_duration(self, text):
        """استخراج مدة التنفيذ من النص"""
        if "مدة تنفيذ المشروع 18 شهراً" in text:
            return "18 شهراً"
        else:
            return "غير محدد"
    
    def _extract_guarantees(self, text):
        """استخراج الضمانات من النص"""
        if "ضماناً نهائياً بنسبة 5% من قيمة العقد" in text:
            return "ضمان نهائي بنسبة 5% من قيمة العقد"
        elif "ضمان ابتدائي: 2% من قيمة العطاء" in text:
            return "ضمان ابتدائي بنسبة 2% من قيمة العطاء، وضمان نهائي بنسبة 5% من قيمة العقد"
        else:
            return "غير محدد"
    
    def _extract_penalties(self, text):
        """استخراج غرامات التأخير من النص"""
        if "غرامة تأخير بنسبة 1% من قيمة العقد عن كل أسبوع تأخير بحد أقصى 10% من قيمة العقد" in text:
            return "1% من قيمة العقد عن كل أسبوع تأخير بحد أقصى 10% من قيمة العقد"
        else:
            return "غير محدد"
    
    def _extract_payment_terms(self, text):
        """استخراج شروط الدفع من النص"""
        if "دفعات شهرية حسب نسبة الإنجاز، مع احتجاز 10% من قيمة كل دفعة كضمان حسن التنفيذ" in text:
            return "دفعات شهرية حسب نسبة الإنجاز، مع احتجاز 10% من قيمة كل دفعة كضمان حسن التنفيذ"
        else:
            return "غير محدد"
    
    def _extract_warranty_period(self, text):
        """استخراج فترة الضمان من النص"""
        if "فترة ضمان المشروع سنة واحدة من تاريخ الاستلام الابتدائي" in text:
            return "سنة واحدة من تاريخ الاستلام الابتدائي"
        else:
            return "غير محدد"
    
    def _extract_termination_terms(self, text):
        """استخراج شروط فسخ العقد من النص"""
        if "يحق للطرف الأول فسخ العقد في حالة إخلال الطرف الثاني بالتزاماته التعاقدية بعد إنذاره كتابياً" in text:
            return "يحق للطرف الأول فسخ العقد في حالة إخلال الطرف الثاني بالتزاماته التعاقدية بعد إنذاره كتابياً"
        else:
            return "غير محدد"
    
    def _extract_dispute_resolution(self, text):
        """استخراج آلية تسوية النزاعات من النص"""
        if "في حالة نشوء أي نزاع بين الطرفين، يتم حله ودياً، وفي حالة تعذر ذلك يتم اللجوء إلى التحكيم" in text:
            return "يتم حل النزاعات ودياً، وفي حالة تعذر ذلك يتم اللجوء إلى التحكيم وفقاً لأنظمة المملكة العربية السعودية"
        else:
            return "غير محدد"
    
    def _extract_tender_info(self, text):
        """استخراج معلومات المناقصة من النص"""
        tender_info = {}
        
        if "رقم المناقصة: T-2024-001" in text:
            tender_info["رقم المناقصة"] = "T-2024-001"
        
        if "الجهة المالكة: وزارة المالية" in text:
            tender_info["الجهة المالكة"] = "وزارة المالية"
        
        if "موقع المشروع: الرياض - حي العليا" in text:
            tender_info["موقع المشروع"] = "الرياض - حي العليا"
        
        if "تاريخ الطرح: 01/03/2024م" in text:
            tender_info["تاريخ الطرح"] = "01/03/2024م"
        
        if "تاريخ الإقفال: 15/04/2024م" in text:
            tender_info["تاريخ الإقفال"] = "15/04/2024م"
        
        return tender_info
    
    def _extract_project_description(self, text):
        """استخراج وصف المشروع من النص"""
        if "يتكون المشروع من إنشاء مبنى إداري مكون من 5 طوابق بمساحة إجمالية 5000 متر مربع" in text:
            return "إنشاء مبنى إداري مكون من 5 طوابق بمساحة إجمالية 5000 متر مربع. يشمل المشروع الأعمال الإنشائية والمعمارية والكهربائية والميكانيكية وأعمال التشطيبات."
        else:
            return "غير محدد"
    
    def _extract_qualification_conditions(self, text):
        """استخراج شروط التأهيل من النص"""
        if "أن يكون المقاول مصنفاً في مجال المباني من الدرجة الأولى" in text:
            return [
                "أن يكون المقاول مصنفاً في مجال المباني من الدرجة الأولى",
                "أن يكون لديه خبرة سابقة في تنفيذ مشاريع مماثلة لا تقل عن 3 مشاريع خلال الخمس سنوات الماضية",
                "أن يكون لديه سيولة مالية كافية لتنفيذ المشروع"
            ]
        else:
            return ["غير محدد"]
    
    def _extract_required_guarantees(self, text):
        """استخراج الضمانات المطلوبة من النص"""
        if "ضمان ابتدائي: 2% من قيمة العطاء" in text:
            return [
                "ضمان ابتدائي: 2% من قيمة العطاء ساري المفعول لمدة 90 يوماً من تاريخ تقديم العطاء",
                "ضمان نهائي: 5% من قيمة العقد ساري المفعول حتى انتهاء فترة الضمان"
            ]
        else:
            return ["غير محدد"]
    
    def _extract_technical_specifications(self, text):
        """استخراج المواصفات الفنية من النص"""
        if "الأعمال الإنشائية:" in text:
            return {
                "الأعمال الإنشائية": [
                    "الخرسانة المسلحة: مقاومة لا تقل عن 300 كجم/سم²",
                    "حديد التسليح: درجة 60"
                ],
                "الأعمال المعمارية": [
                    "الواجهات: زجاج عاكس وحجر طبيعي",
                    "الأرضيات: رخام للمداخل وبورسلين للمكاتب",
                    "الأسقف: أسقف مستعارة من الجبس المزخرف"
                ],
                "الأعمال الكهربائية": [
                    "نظام إنارة موفر للطاقة",
                    "نظام إنذار وإطفاء حريق آلي",
                    "نظام مراقبة بالكاميرات"
                ],
                "الأعمال الميكانيكية": [
                    "نظام تكييف مركزي",
                    "نظام تهوية متطور",
                    "مصاعد عدد 3"
                ]
            }
        else:
            return {"غير محدد": ["غير محدد"]}
    
    def _extract_evaluation_criteria(self, text):
        """استخراج معايير التقييم من النص"""
        if "السعر: 50%" in text:
            return {
                "السعر": "50%",
                "الجودة الفنية": "30%",
                "الخبرة السابقة": "15%",
                "مدة التنفيذ": "5%"
            }
        else:
            return {"غير محدد": "غير محدد"}
    
    def _analyze_competition(self, tender_info):
        """تحليل المنافسة"""
        return {
            "expected_competitors": [
                {"name": "شركة الإنشاءات المتطورة", "strength": "خبرة طويلة في مشاريع مماثلة", "weakness": "أسعار مرتفعة", "win_probability": 30},
                {"name": "شركة البناء الحديث", "strength": "أسعار تنافسية", "weakness": "خبرة محدودة", "win_probability": 25},
                {"name": "شركة التطوير العمراني", "strength": "جودة عالية", "weakness": "بطء في التنفيذ", "win_probability": 20}
            ],
            "competitive_advantages": [
                "خبرة في مشاريع مماثلة",
                "فريق فني متميز",
                "علاقات جيدة مع الموردين",
                "تقنيات حديثة في التنفيذ"
            ],
            "competitive_disadvantages": [
                "محدودية الموارد المالية",
                "قلة الخبرة في بعض الجوانب الفنية"
            ]
        }
    
    def _analyze_risks(self, text):
        """تحليل المخاطر"""
        return [
            {"risk": "ارتفاع أسعار المواد", "probability": "متوسطة", "impact": "عالي", "mitigation": "تثبيت أسعار المواد الرئيسية مع الموردين"},
            {"risk": "تأخر التنفيذ", "probability": "متوسطة", "impact": "عالي", "mitigation": "وضع خطة تنفيذ مفصلة مع هوامش زمنية"},
            {"risk": "نقص العمالة الماهرة", "probability": "منخفضة", "impact": "متوسط", "mitigation": "التعاقد المسبق مع مقاولي الباطن"},
            {"risk": "تغيير نطاق العمل", "probability": "متوسطة", "impact": "عالي", "mitigation": "توثيق نطاق العمل بدقة وتحديد إجراءات التغيير"},
            {"risk": "مشاكل في التربة", "probability": "منخفضة", "impact": "عالي", "mitigation": "إجراء فحوصات شاملة للتربة قبل البدء"}
        ]
    
    def _analyze_opportunities(self, text):
        """تحليل الفرص"""
        return [
            {"opportunity": "تقديم حلول مبتكرة لتقليل التكاليف", "benefit": "زيادة هامش الربح", "implementation": "استخدام تقنيات حديثة في التنفيذ"},
            {"opportunity": "تقديم جدول زمني أقصر من المطلوب", "benefit": "زيادة فرص الفوز", "implementation": "استخدام فرق عمل متعددة"},
            {"opportunity": "تقديم خدمات إضافية", "benefit": "تعزيز العلاقة مع العميل", "implementation": "تقديم خدمات الصيانة بعد انتهاء فترة الضمان"},
            {"opportunity": "استخدام مواد صديقة للبيئة", "benefit": "تحسين السمعة", "implementation": "استخدام مواد معتمدة من هيئات البيئة"},
            {"opportunity": "تطوير شراكات مع موردين", "benefit": "تقليل التكاليف", "implementation": "توقيع اتفاقيات طويلة الأمد مع الموردين"}
        ]
    
    def _analyze_technical_requirements(self, technical_specifications):
        """تحليل المتطلبات الفنية"""
        return {
            "complexity_level": "متوسط",
            "special_requirements": [
                "نظام إنارة موفر للطاقة",
                "نظام إنذار وإطفاء حريق آلي",
                "نظام تكييف مركزي"
            ],
            "technical_challenges": [
                "تنفيذ الواجهات الزجاجية بالمواصفات المطلوبة",
                "تركيب نظام التكييف المركزي",
                "تنفيذ أعمال التشطيبات بالجودة المطلوبة"
            ],
            "required_expertise": [
                "خبرة في تنفيذ المباني الإدارية",
                "خبرة في تركيب أنظمة التكييف المركزي",
                "خبرة في تنفيذ الواجهات الزجاجية"
            ]
        }
    
    def _analyze_technical_risks(self, technical_specifications):
        """تحليل المخاطر الفنية"""
        return [
            {"risk": "عدم توفر المواد بالمواصفات المطلوبة", "probability": "منخفضة", "impact": "عالي", "mitigation": "التعاقد المسبق مع الموردين"},
            {"risk": "صعوبة تنفيذ الواجهات الزجاجية", "probability": "متوسطة", "impact": "متوسط", "mitigation": "الاستعانة بمقاول باطن متخصص"},
            {"risk": "مشاكل في تركيب نظام التكييف المركزي", "probability": "منخفضة", "impact": "عالي", "mitigation": "الاستعانة بخبراء في تركيب أنظمة التكييف"},
            {"risk": "عدم مطابقة التشطيبات للمواصفات", "probability": "متوسطة", "impact": "متوسط", "mitigation": "تطبيق نظام ضبط الجودة"},
            {"risk": "تأخر توريد المواد", "probability": "متوسطة", "impact": "عالي", "mitigation": "وضع خطة توريد مفصلة مع هوامش زمنية"}
        ]
    
    def _estimate_costs(self, project_description):
        """تقدير التكاليف"""
        return {
            "total_cost": 25000000,
            "cost_breakdown": [
                {"category": "الأعمال الإنشائية", "amount": 10000000, "percentage": 40},
                {"category": "الأعمال المعمارية", "amount": 6250000, "percentage": 25},
                {"category": "الأعمال الكهربائية", "amount": 3750000, "percentage": 15},
                {"category": "الأعمال الميكانيكية", "amount": 3750000, "percentage": 15},
                {"category": "أعمال الموقع", "amount": 1250000, "percentage": 5}
            ],
            "cost_per_sqm": 5000,
            "cost_saving_opportunities": [
                {"item": "استخدام مواد بديلة", "potential_saving": 1250000},
                {"item": "تحسين إنتاجية العمالة", "potential_saving": 750000},
                {"item": "تأجير المعدات بدلاً من شرائها", "potential_saving": 500000}
            ]
        }
    
    def _analyze_cash_flow(self, payment_terms, cost_estimation):
        """تحليل التدفقات النقدية"""
        return [
            {"month": 1, "income": 0, "expense": 2500000, "net": -2500000, "cumulative": -2500000},
            {"month": 2, "income": 1125000, "expense": 2000000, "net": -875000, "cumulative": -3375000},
            {"month": 3, "income": 1125000, "expense": 1500000, "net": -375000, "cumulative": -3750000},
            {"month": 4, "income": 1125000, "expense": 1500000, "net": -375000, "cumulative": -4125000},
            {"month": 5, "income": 1125000, "expense": 1500000, "net": -375000, "cumulative": -4500000},
            {"month": 6, "income": 1125000, "expense": 1500000, "net": -375000, "cumulative": -4875000}
        ]
    
    def _analyze_financial_risks(self, text):
        """تحليل المخاطر المالية"""
        return [
            {"risk": "تأخر الدفعات", "probability": "متوسطة", "impact": "عالي", "mitigation": "وضع شروط واضحة للدفعات في العقد"},
            {"risk": "زيادة أسعار المواد", "probability": "عالية", "impact": "عالي", "mitigation": "تثبيت أسعار المواد الرئيسية مع الموردين"},
            {"risk": "نقص السيولة", "probability": "متوسطة", "impact": "عالي", "mitigation": "الحصول على تسهيلات بنكية"},
            {"risk": "تغير أسعار العملات", "probability": "منخفضة", "impact": "متوسط", "mitigation": "استخدام عقود التحوط"},
            {"risk": "زيادة تكاليف العمالة", "probability": "متوسطة", "impact": "متوسط", "mitigation": "التعاقد مع مقاولي الباطن بأسعار ثابتة"}
        ]
