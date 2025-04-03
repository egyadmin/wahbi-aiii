"""
وحدة تحليل المستندات لنظام إدارة المناقصات - Hybrid Face
"""

import os
import re
import logging
import threading
from pathlib import Path
import datetime
import json

# تهيئة السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('document_analysis')

class DocumentAnalyzer:
    """فئة تحليل المستندات"""
    
    def __init__(self, config=None):
        """تهيئة محلل المستندات"""
        self.config = config
        self.analysis_in_progress = False
        self.current_document = None
        self.analysis_results = {}
        
        # إنشاء مجلد المستندات إذا لم يكن موجوداً
        if config and hasattr(config, 'DOCUMENTS_PATH'):
            self.documents_path = Path(config.DOCUMENTS_PATH)
        else:
            self.documents_path = Path('data/documents')
            
        if not self.documents_path.exists():
            self.documents_path.mkdir(parents=True, exist_ok=True)
    
    def analyze_document(self, document_path, document_type="tender", callback=None):
        """تحليل مستند"""
        if self.analysis_in_progress:
            logger.warning("هناك عملية تحليل جارية بالفعل")
            return False
        
        if not os.path.exists(document_path):
            logger.error(f"المستند غير موجود: {document_path}")
            return False
        
        self.analysis_in_progress = True
        self.current_document = document_path
        self.analysis_results = {
            "document_path": document_path,
            "document_type": document_type,
            "analysis_start_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "جاري التحليل",
            "items": [],
            "entities": [],
            "dates": [],
            "amounts": [],
            "risks": []
        }
        
        # بدء التحليل في خيط منفصل
        thread = threading.Thread(
            target=self._analyze_document_thread,
            args=(document_path, document_type, callback)
        )
        thread.daemon = True
        thread.start()
        
        return True
    
    def _analyze_document_thread(self, document_path, document_type, callback):
        """خيط تحليل المستند"""
        try:
            # تحديد نوع المستند
            file_extension = os.path.splitext(document_path)[1].lower()
            
            if file_extension == '.pdf':
                self._analyze_pdf(document_path, document_type)
            elif file_extension == '.docx':
                self._analyze_docx(document_path, document_type)
            elif file_extension == '.xlsx':
                self._analyze_xlsx(document_path, document_type)
            elif file_extension == '.txt':
                self._analyze_txt(document_path, document_type)
            else:
                logger.error(f"نوع المستند غير مدعوم: {file_extension}")
                self.analysis_results["status"] = "فشل التحليل"
                self.analysis_results["error"] = "نوع المستند غير مدعوم"
            
            # تحديث حالة التحليل
            if self.analysis_results["status"] != "فشل التحليل":
                self.analysis_results["status"] = "اكتمل التحليل"
                self.analysis_results["analysis_end_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"اكتمل تحليل المستند: {document_path}")
            
        except Exception as e:
            logger.error(f"خطأ في تحليل المستند: {str(e)}")
            self.analysis_results["status"] = "فشل التحليل"
            self.analysis_results["error"] = str(e)
        
        finally:
            self.analysis_in_progress = False
            
            # استدعاء دالة الاستجابة إذا تم توفيرها
            if callback and callable(callback):
                callback(self.analysis_results)
    
    def _analyze_pdf(self, document_path, document_type):
        """تحليل مستند PDF"""
        try:
            # محاكاة تحليل مستند PDF
            logger.info(f"تحليل مستند PDF: {document_path}")
            
            # في التطبيق الفعلي، سيتم استخدام مكتبة مثل PyPDF2 أو pdfplumber
            # لاستخراج النص من ملف PDF وتحليله
            
            # محاكاة استخراج البنود
            self.analysis_results["items"] = [
                {"id": 1, "name": "أعمال الحفر", "description": "حفر وإزالة التربة", "unit": "م³", "estimated_quantity": 1500},
                {"id": 2, "name": "أعمال الخرسانة", "description": "صب خرسانة مسلحة", "unit": "م³", "estimated_quantity": 750},
                {"id": 3, "name": "أعمال الأسفلت", "description": "تمهيد وفرش طبقة أسفلت", "unit": "م²", "estimated_quantity": 5000}
            ]
            
            # محاكاة استخراج الكيانات
            self.analysis_results["entities"] = [
                {"type": "client", "name": "وزارة النقل", "mentions": 5},
                {"type": "location", "name": "المنطقة الشرقية", "mentions": 3},
                {"type": "contractor", "name": "شركة المقاولات المتحدة", "mentions": 2}
            ]
            
            # محاكاة استخراج التواريخ
            self.analysis_results["dates"] = [
                {"type": "start_date", "date": "2025-05-01", "description": "تاريخ بدء المشروع"},
                {"type": "end_date", "date": "2025-11-30", "description": "تاريخ انتهاء المشروع"},
                {"type": "submission_date", "date": "2025-04-15", "description": "تاريخ تقديم العروض"}
            ]
            
            # محاكاة استخراج المبالغ
            self.analysis_results["amounts"] = [
                {"type": "estimated_cost", "amount": 5000000, "currency": "SAR", "description": "التكلفة التقديرية للمشروع"},
                {"type": "advance_payment", "amount": 500000, "currency": "SAR", "description": "الدفعة المقدمة (10%)"},
                {"type": "performance_bond", "amount": 250000, "currency": "SAR", "description": "ضمان حسن التنفيذ (5%)"}
            ]
            
            # محاكاة استخراج المخاطر
            self.analysis_results["risks"] = [
                {"type": "delay_risk", "description": "مخاطر التأخير في التنفيذ", "probability": "متوسط", "impact": "عالي"},
                {"type": "cost_risk", "description": "مخاطر زيادة التكاليف", "probability": "عالي", "impact": "عالي"},
                {"type": "quality_risk", "description": "مخاطر جودة التنفيذ", "probability": "منخفض", "impact": "متوسط"}
            ]
            
        except Exception as e:
            logger.error(f"خطأ في تحليل مستند PDF: {str(e)}")
            raise
    
    def _analyze_docx(self, document_path, document_type):
        """تحليل مستند Word"""
        try:
            # محاكاة تحليل مستند Word
            logger.info(f"تحليل مستند Word: {document_path}")
            
            # في التطبيق الفعلي، سيتم استخدام مكتبة مثل python-docx
            # لاستخراج النص من ملف Word وتحليله
            
            # محاكاة استخراج البنود والكيانات والتواريخ والمبالغ والمخاطر
            # (مشابه لتحليل PDF)
            self.analysis_results["items"] = [
                {"id": 1, "name": "توريد معدات", "description": "توريد معدات المشروع", "unit": "مجموعة", "estimated_quantity": 10},
                {"id": 2, "name": "تركيب المعدات", "description": "تركيب وتشغيل المعدات", "unit": "مجموعة", "estimated_quantity": 10},
                {"id": 3, "name": "التدريب", "description": "تدريب الموظفين على استخدام المعدات", "unit": "يوم", "estimated_quantity": 20}
            ]
            
            # محاكاة استخراج الكيانات والتواريخ والمبالغ والمخاطر
            # (مشابه لتحليل PDF)
            
        except Exception as e:
            logger.error(f"خطأ في تحليل مستند Word: {str(e)}")
            raise
    
    def _analyze_xlsx(self, document_path, document_type):
        """تحليل مستند Excel"""
        try:
            # محاكاة تحليل مستند Excel
            logger.info(f"تحليل مستند Excel: {document_path}")
            
            # في التطبيق الفعلي، سيتم استخدام مكتبة مثل pandas أو openpyxl
            # لاستخراج البيانات من ملف Excel وتحليلها
            
            # محاكاة استخراج البنود
            self.analysis_results["items"] = [
                {"id": 1, "name": "بند 1", "description": "وصف البند 1", "unit": "وحدة", "estimated_quantity": 100},
                {"id": 2, "name": "بند 2", "description": "وصف البند 2", "unit": "وحدة", "estimated_quantity": 200},
                {"id": 3, "name": "بند 3", "description": "وصف البند 3", "unit": "وحدة", "estimated_quantity": 300}
            ]
            
            # محاكاة استخراج المبالغ
            self.analysis_results["amounts"] = [
                {"type": "item_cost", "amount": 10000, "currency": "SAR", "description": "تكلفة البند 1"},
                {"type": "item_cost", "amount": 20000, "currency": "SAR", "description": "تكلفة البند 2"},
                {"type": "item_cost", "amount": 30000, "currency": "SAR", "description": "تكلفة البند 3"}
            ]
            
        except Exception as e:
            logger.error(f"خطأ في تحليل مستند Excel: {str(e)}")
            raise
    
    def _analyze_txt(self, document_path, document_type):
        """تحليل مستند نصي"""
        try:
            # محاكاة تحليل مستند نصي
            logger.info(f"تحليل مستند نصي: {document_path}")
            
            # في التطبيق الفعلي، سيتم قراءة الملف النصي وتحليله
            
            # محاكاة استخراج البنود والكيانات والتواريخ والمبالغ والمخاطر
            # (مشابه للتحليلات الأخرى)
            
        except Exception as e:
            logger.error(f"خطأ في تحليل مستند نصي: {str(e)}")
            raise
    
    def get_analysis_status(self):
        """الحصول على حالة التحليل الحالي"""
        if not self.analysis_in_progress:
            if not self.analysis_results:
                return {"status": "لا يوجد تحليل جارٍ"}
            else:
                return {"status": self.analysis_results.get("status", "غير معروف")}
        
        return {
            "status": "جاري التحليل",
            "document_path": self.current_document,
            "start_time": self.analysis_results.get("analysis_start_time")
        }
    
    def get_analysis_results(self):
        """الحصول على نتائج التحليل"""
        return self.analysis_results
    
    def export_analysis_results(self, output_path=None):
        """تصدير نتائج التحليل إلى ملف JSON"""
        if not self.analysis_results:
            logger.warning("لا توجد نتائج تحليل للتصدير")
            return None
        
        if not output_path:
            # إنشاء اسم ملف افتراضي
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"analysis_results_{timestamp}.json"
            output_path = os.path.join(self.documents_path, filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.analysis_results, f, ensure_ascii=False, indent=4)
            
            logger.info(f"تم تصدير نتائج التحليل إلى: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"خطأ في تصدير نتائج التحليل: {str(e)}")
            return None
    
    def import_analysis_results(self, input_path):
        """استيراد نتائج التحليل من ملف JSON"""
        if not os.path.exists(input_path):
            logger.error(f"ملف نتائج التحليل غير موجود: {input_path}")
            return False
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                self.analysis_results = json.load(f)
            
            logger.info(f"تم استيراد نتائج التحليل من: {input_path}")
            return True
        
        except Exception as e:
            logger.error(f"خطأ في استيراد نتائج التحليل: {str(e)}")
            return False
