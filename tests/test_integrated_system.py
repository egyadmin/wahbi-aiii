"""
وحدة اختبار النظام المتكامل
"""

import unittest
import os
import sys
from pathlib import Path

# إضافة المسار الرئيسي للنظام
sys.path.append(str(Path(__file__).parent.parent))

# استيراد الوحدات
from modules.pricing.pricing_app import PricingApp
from modules.ai_assistant.ai_app import AIAssistantApp
from modules.document_analysis.document_app import DocumentAnalysisApp
from modules.data_analysis.data_analysis_app import DataAnalysisApp
from modules.resources.resources_app import ResourcesApp

class TestIntegratedSystem(unittest.TestCase):
    """اختبارات النظام المتكامل"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        # التأكد من وجود جميع الملفات الرئيسية
        self.main_files = [
            "app.py",
            "config.py",
            "requirements.txt"
        ]
        
        # التأكد من وجود جميع المجلدات الرئيسية
        self.main_directories = [
            "modules",
            "assets",
            "data",
            "utils"
        ]
        
        # التأكد من وجود جميع وحدات النظام
        self.modules = [
            "modules/pricing",
            "modules/ai_assistant",
            "modules/document_analysis",
            "modules/data_analysis",
            "modules/resources",
            "modules/project_management",
            "modules/reports",
            "modules/risk_analysis"
        ]
    
    def test_main_files_exist(self):
        """اختبار وجود الملفات الرئيسية"""
        for file in self.main_files:
            file_path = Path(__file__).parent.parent / file
            self.assertTrue(file_path.exists(), f"الملف {file} غير موجود")
    
    def test_main_directories_exist(self):
        """اختبار وجود المجلدات الرئيسية"""
        for directory in self.main_directories:
            dir_path = Path(__file__).parent.parent / directory
            self.assertTrue(dir_path.exists(), f"المجلد {directory} غير موجود")
    
    def test_modules_exist(self):
        """اختبار وجود وحدات النظام"""
        for module in self.modules:
            module_path = Path(__file__).parent.parent / module
            self.assertTrue(module_path.exists(), f"الوحدة {module} غير موجودة")
    
    def test_pricing_module(self):
        """اختبار وحدة التسعير"""
        pricing_app = PricingApp()
        self.assertIsNotNone(pricing_app, "فشل إنشاء وحدة التسعير")
    
    def test_ai_assistant_module(self):
        """اختبار وحدة الذكاء الاصطناعي"""
        ai_app = AIAssistantApp()
        self.assertIsNotNone(ai_app, "فشل إنشاء وحدة الذكاء الاصطناعي")
    
    def test_document_analysis_module(self):
        """اختبار وحدة تحليل المستندات"""
        document_app = DocumentAnalysisApp()
        self.assertIsNotNone(document_app, "فشل إنشاء وحدة تحليل المستندات")
    
    def test_data_analysis_module(self):
        """اختبار وحدة تحليل البيانات"""
        data_analysis_app = DataAnalysisApp()
        self.assertIsNotNone(data_analysis_app, "فشل إنشاء وحدة تحليل البيانات")
    
    def test_resources_module(self):
        """اختبار وحدة الموارد"""
        resources_app = ResourcesApp()
        self.assertIsNotNone(resources_app, "فشل إنشاء وحدة الموارد")

if __name__ == "__main__":
    unittest.main()
