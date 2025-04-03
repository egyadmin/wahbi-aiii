"""
وحدة اختبار التطبيق لنظام إدارة المناقصات - Hybrid Face
"""

import os
import sys
import logging
import unittest
import tkinter as tk
from pathlib import Path

# تهيئة السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_app')

# إضافة المسار الرئيسي للتطبيق إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# استيراد الوحدات المطلوبة للاختبار
from database.db_connector import DatabaseConnector
from database.models import User, Project, Document, ProjectItem, Resource, Risk, Report, SystemLog
from modules.document_analysis.analyzer import DocumentAnalyzer
from modules.pricing.pricing_engine import PricingEngine
from modules.risk_analysis.risk_analyzer import RiskAnalyzer
from modules.ai_assistant.assistant import AIAssistant
from styling.theme import AppTheme
from styling.icons import IconGenerator
from styling.charts import ChartGenerator
from config import AppConfig

class TestDatabaseConnector(unittest.TestCase):
    """اختبار وحدة اتصال قاعدة البيانات"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        # استخدام قاعدة بيانات اختبار مؤقتة
        self.config = AppConfig()
        self.config.DB_NAME = "test_tender_system.db"
        self.db = DatabaseConnector(self.config)
    
    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        self.db.disconnect()
        # حذف قاعدة البيانات المؤقتة
        if os.path.exists(self.config.DB_NAME):
            os.remove(self.config.DB_NAME)
    
    def test_connection(self):
        """اختبار الاتصال بقاعدة البيانات"""
        self.assertTrue(self.db.is_connected)
    
    def test_execute_query(self):
        """اختبار تنفيذ استعلام"""
        cursor = self.db.execute("SELECT 1")
        self.assertIsNotNone(cursor)
        result = cursor.fetchone()
        self.assertEqual(result[0], 1)
    
    def test_insert_and_fetch(self):
        """اختبار إدراج واسترجاع البيانات"""
        # إدراج بيانات
        user_data = {
            "username": "test_user",
            "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin
            "full_name": "مستخدم اختبار",
            "email": "test@example.com",
            "role": "user"
        }
        user_id = self.db.insert("users", user_data)
        self.assertIsNotNone(user_id)
        
        # استرجاع البيانات
        user = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        self.assertIsNotNone(user)
        self.assertEqual(user["username"], "test_user")
        self.assertEqual(user["full_name"], "مستخدم اختبار")
    
    def test_update(self):
        """اختبار تحديث البيانات"""
        # إدراج بيانات
        user_data = {
            "username": "update_user",
            "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin
            "full_name": "مستخدم للتحديث",
            "email": "update@example.com",
            "role": "user"
        }
        user_id = self.db.insert("users", user_data)
        
        # تحديث البيانات
        updated_data = {
            "full_name": "مستخدم تم تحديثه",
            "role": "admin"
        }
        rows_affected = self.db.update("users", updated_data, "id = ?", (user_id,))
        self.assertEqual(rows_affected, 1)
        
        # التحقق من التحديث
        user = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        self.assertEqual(user["full_name"], "مستخدم تم تحديثه")
        self.assertEqual(user["role"], "admin")
    
    def test_delete(self):
        """اختبار حذف البيانات"""
        # إدراج بيانات
        user_data = {
            "username": "delete_user",
            "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin
            "full_name": "مستخدم للحذف",
            "email": "delete@example.com",
            "role": "user"
        }
        user_id = self.db.insert("users", user_data)
        
        # حذف البيانات
        rows_affected = self.db.delete("users", "id = ?", (user_id,))
        self.assertEqual(rows_affected, 1)
        
        # التحقق من الحذف
        user = self.db.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
        self.assertIsNone(user)


class TestModels(unittest.TestCase):
    """اختبار نماذج البيانات"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        # استخدام قاعدة بيانات اختبار مؤقتة
        self.config = AppConfig()
        self.config.DB_NAME = "test_models.db"
        self.db = DatabaseConnector(self.config)
    
    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        self.db.disconnect()
        # حذف قاعدة البيانات المؤقتة
        if os.path.exists(self.config.DB_NAME):
            os.remove(self.config.DB_NAME)
    
    def test_user_model(self):
        """اختبار نموذج المستخدم"""
        # إنشاء مستخدم جديد
        user = User(self.db)
        user.data = {
            "username": "model_user",
            "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin
            "full_name": "مستخدم نموذج",
            "email": "model@example.com",
            "role": "user",
            "is_active": 1
        }
        
        # حفظ المستخدم
        self.assertTrue(user.save())
        self.assertIsNotNone(user.data.get("id"))
        
        # استرجاع المستخدم
        retrieved_user = User.get_by_id(user.data["id"], self.db)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.data["username"], "model_user")
        
        # مصادقة المستخدم
        authenticated_user = User.authenticate("model_user", "admin", self.db)
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.data["username"], "model_user")
        
        # تعيين كلمة مرور جديدة
        user.set_password("newpassword")
        user.save()
        
        # مصادقة المستخدم بكلمة المرور الجديدة
        authenticated_user = User.authenticate("model_user", "newpassword", self.db)
        self.assertIsNotNone(authenticated_user)
        
        # حذف المستخدم
        self.assertTrue(user.delete())
    
    def test_project_model(self):
        """اختبار نموذج المشروع"""
        # إنشاء مستخدم للمشروع
        user = User(self.db)
        user.data = {
            "username": "project_user",
            "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # admin
            "full_name": "مستخدم المشروع",
            "email": "project@example.com",
            "role": "user",
            "is_active": 1
        }
        user.save()
        
        # إنشاء مشروع جديد
        project = Project(self.db)
        project.data = {
            "name": "مشروع اختبار",
            "client": "عميل اختبار",
            "description": "وصف مشروع الاختبار",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "status": "تخطيط",
            "created_by": user.data["id"]
        }
        
        # حفظ المشروع
        self.assertTrue(project.save())
        self.assertIsNotNone(project.data.get("id"))
        
        # استرجاع المشروع
        retrieved_project = Project.get_by_id(project.data["id"], self.db)
        self.assertIsNotNone(retrieved_project)
        self.assertEqual(retrieved_project.data["name"], "مشروع اختبار")
        
        # إضافة بند للمشروع
        item = ProjectItem(self.db)
        item.data = {
            "project_id": project.data["id"],
            "name": "بند اختبار",
            "description": "وصف بند الاختبار",
            "unit": "م²",
            "quantity": 100,
            "unit_price": 500,
            "total_price": 50000
        }
        item.save()
        
        # حساب التكلفة الإجمالية للمشروع
        total_cost = project.calculate_total_cost()
        self.assertEqual(total_cost, 50000)
        
        # حذف المشروع
        self.assertTrue(project.delete())
        
        # حذف المستخدم
        self.assertTrue(user.delete())


class TestDocumentAnalyzer(unittest.TestCase):
    """اختبار محلل المستندات"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        self.config = AppConfig()
        self.analyzer = DocumentAnalyzer(self.config)
        
        # إنشاء مجلد المستندات للاختبار
        self.test_docs_dir = Path("test_documents")
        self.test_docs_dir.mkdir(exist_ok=True)
        
        # إنشاء ملف مستند اختبار
        self.test_doc_path = self.test_docs_dir / "test_document.txt"
        with open(self.test_doc_path, "w", encoding="utf-8") as f:
            f.write("هذا مستند اختبار لمحلل المستندات")
    
    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        # حذف ملف المستند
        if self.test_doc_path.exists():
            self.test_doc_path.unlink()
        
        # حذف مجلد المستندات
        if self.test_docs_dir.exists():
            self.test_docs_dir.rmdir()
    
    def test_analyze_document(self):
        """اختبار تحليل المستند"""
        # تحليل المستند
        result = self.analyzer.analyze_document(str(self.test_doc_path), "tender")
        self.assertTrue(result)
        
        # انتظار اكتمال التحليل
        import time
        max_wait = 5  # ثوانٍ
        waited = 0
        while self.analyzer.analysis_in_progress and waited < max_wait:
            time.sleep(0.5)
            waited += 0.5
        
        # التحقق من نتائج التحليل
        self.assertFalse(self.analyzer.analysis_in_progress)
        results = self.analyzer.get_analysis_results()
        self.assertEqual(results["status"], "اكتمل التحليل")
        self.assertEqual(results["document_path"], str(self.test_doc_path))
    
    def test_export_analysis_results(self):
        """اختبار تصدير نتائج التحليل"""
        # تحليل المستند
        self.analyzer.analyze_document(str(self.test_doc_path), "tender")
        
        # انتظار اكتمال التحليل
        import time
        max_wait = 5  # ثوانٍ
        waited = 0
        while self.analyzer.analysis_in_progress and waited < max_wait:
            time.sleep(0.5)
            waited += 0.5
        
        # تصدير النتائج
        export_path = self.test_docs_dir / "analysis_results.json"
        result_path = self.analyzer.export_analysis_results(str(export_path))
        self.assertIsNotNone(result_path)
        
        # التحقق من وجود ملف التصدير
        self.assertTrue(export_path.exists())
        
        # حذف ملف التصدير
        if export_path.exists():
            export_path.unlink()


class TestPricingEngine(unittest.TestCase):
    """اختبار محرك التسعير"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        self.config = AppConfig()
        self.pricing_engine = PricingEngine(self.config)
    
    def test_calculate_pricing(self):
        """اختبار حساب التسعير"""
        # حساب التسعير
        result = self.pricing_engine.calculate_pricing(1, "comprehensive")
        self.assertTrue(result)
        
        # انتظار اكتمال التسعير
        import time
        max_wait = 5  # ثوانٍ
        waited = 0
        while self.pricing_engine.pricing_in_progress and waited < max_wait:
            time.sleep(0.5)
            waited += 0.5
        
        # التحقق من نتائج التسعير
        self.assertFalse(self.pricing_engine.pricing_in_progress)
        results = self.pricing_engine.get_pricing_results()
        self.assertEqual(results["status"], "اكتمل التسعير")
        self.assertEqual(results["project_id"], 1)
        self.assertEqual(results["strategy"], "comprehensive")
        
        # التحقق من وجود التكاليف المباشرة
        self.assertIn("direct_costs", results)
        self.assertIn("total_direct_costs", results["direct_costs"])
        
        # التحقق من وجود التكاليف غير المباشرة
        self.assertIn("indirect_costs", results)
        self.assertIn("total_indirect_costs", results["indirect_costs"])
        
        # التحقق من وجود تكاليف المخاطر
        self.assertIn("risk_costs", results)
        self.assertIn("total_risk_cost", results["risk_costs"])
        
        # التحقق من وجود ملخص التسعير
        self.assertIn("summary", results)
        self.assertIn("final_price", results["summary"])


class TestRiskAnalyzer(unittest.TestCase):
    """اختبار محلل المخاطر"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        self.config = AppConfig()
        self.risk_analyzer = RiskAnalyzer(self.config)
    
    def test_analyze_risks(self):
        """اختبار تحليل المخاطر"""
        # تحليل المخاطر
        result = self.risk_analyzer.analyze_risks(1, "comprehensive")
        self.assertTrue(result)
        
        # انتظار اكتمال التحليل
        import time
        max_wait = 5  # ثوانٍ
        waited = 0
        while self.risk_analyzer.analysis_in_progress and waited < max_wait:
            time.sleep(0.5)
            waited += 0.5
        
        # التحقق من نتائج التحليل
        self.assertFalse(self.risk_analyzer.analysis_in_progress)
        results = self.risk_analyzer.get_analysis_results()
        self.assertEqual(results["status"], "اكتمل التحليل")
        self.assertEqual(results["project_id"], 1)
        self.assertEqual(results["method"], "comprehensive")
        
        # التحقق من وجود المخاطر المحددة
        self.assertIn("identified_risks", results)
        self.assertTrue(len(results["identified_risks"]) > 0)
        
        # التحقق من وجود فئات المخاطر
        self.assertIn("risk_categories", results)
        
        # التحقق من وجود مصفوفة المخاطر
        self.assertIn("risk_matrix", results)
        
        # التحقق من وجود استراتيجيات التخفيف
        self.assertIn("mitigation_strategies", results)
        self.assertTrue(len(results["mitigation_strategies"]) > 0)
        
        # التحقق من وجود ملخص التحليل
        self.assertIn("summary", results)
        self.assertIn("overall_risk_level", results["summary"])


class TestAIAssistant(unittest.TestCase):
    """اختبار المساعد الذكي"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        self.config = AppConfig()
        self.assistant = AIAssistant(self.config)
    
    def test_process_query(self):
        """اختبار معالجة الاستعلام"""
        # معالجة استعلام
        query = "كيف يمكنني تحليل مستند مناقصة؟"
        result = self.assistant.process_query(query)
        self.assertTrue(result)
        
        # انتظار اكتمال المعالجة
        import time
        max_wait = 5  # ثوانٍ
        waited = 0
        while self.assistant.processing_in_progress and waited < max_wait:
            time.sleep(0.5)
            waited += 0.5
        
        # التحقق من نتائج المعالجة
        self.assertFalse(self.assistant.processing_in_progress)
        results = self.assistant.get_processing_results()
        self.assertEqual(results["status"], "اكتملت المعالجة")
        self.assertEqual(results["query"], query)
        
        # التحقق من وجود استجابة
        self.assertIn("response", results)
        self.assertTrue(len(results["response"]) > 0)
        
        # التحقق من وجود اقتراحات
        self.assertIn("suggestions", results)
        self.assertTrue(len(results["suggestions"]) > 0)
    
    def test_conversation_history(self):
        """اختبار سجل المحادثة"""
        # معالجة استعلام
        query = "ما هي استراتيجيات التسعير المتاحة؟"
        self.assistant.process_query(query)
        
        # انتظار اكتمال المعالجة
        import time
        max_wait = 5  # ثوانٍ
        waited = 0
        while self.assistant.processing_in_progress and waited < max_wait:
            time.sleep(0.5)
            waited += 0.5
        
        # التحقق من سجل المحادثة
        history = self.assistant.get_conversation_history()
        self.assertEqual(len(history), 2)  # استعلام المستخدم واستجابة المساعد
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[0]["content"], query)
        self.assertEqual(history[1]["role"], "assistant")
        
        # مسح سجل المحادثة
        self.assertTrue(self.assistant.clear_conversation_history())
        history = self.assistant.get_conversation_history()
        self.assertEqual(len(history), 0)


class TestStyling(unittest.TestCase):
    """اختبار وحدات التصميم"""
    
    def test_app_theme(self):
        """اختبار نمط التطبيق"""
        theme = AppTheme()
        
        # التحقق من الألوان
        self.assertIsNotNone(theme.get_color("bg_color"))
        self.assertIsNotNone(theme.get_color("fg_color"))
        
        # التحقق من الخطوط
        self.assertIsNotNone(theme.get_font("body"))
        self.assertIsNotNone(theme.get_font("title"))
        
        # التحقق من الأحجام
        self.assertIsNotNone(theme.get_size("padding_medium"))
        self.assertIsNotNone(theme.get_size("border_radius"))
        
        # تغيير النمط
        self.assertTrue(theme.set_theme("dark"))
        self.assertEqual(theme.current_theme, "dark")
        
        # تغيير اللغة
        self.assertTrue(theme.set_language("en"))
        self.assertEqual(theme.current_language, "en")
    
    def test_icon_generator(self):
        """اختبار مولد الأيقونات"""
        icon_generator = IconGenerator()
        
        # توليد الأيقونات الافتراضية
        icon_generator.generate_default_icons()
        
        # التحقق من وجود مجلد الأيقونات
        self.assertTrue(Path('assets/icons').exists())
        
        # التحقق من وجود بعض الأيقونات
        self.assertTrue(Path('assets/icons/dashboard.png').exists())
        self.assertTrue(Path('assets/icons/projects.png').exists())
    
    def test_chart_generator(self):
        """اختبار مولد الرسوم البيانية"""
        theme = AppTheme()
        chart_generator = ChartGenerator(theme)
        
        # إنشاء بيانات للرسم البياني الشريطي
        bar_data = {
            'labels': ['الربع الأول', 'الربع الثاني', 'الربع الثالث', 'الربع الرابع'],
            'values': [15000, 20000, 18000, 25000]
        }
        
        # إنشاء رسم بياني شريطي
        fig = chart_generator.create_bar_chart(
            bar_data,
            'الإيرادات الفصلية',
            'الفصل',
            'الإيرادات (ريال)'
        )
        
        # التحقق من إنشاء الرسم البياني
        self.assertIsNotNone(fig)
        
        # حفظ الرسم البياني
        save_path = 'test_chart.png'
        chart_generator.create_bar_chart(
            bar_data,
            'الإيرادات الفصلية',
            'الفصل',
            'الإيرادات (ريال)',
            save_path=save_path
        )
        
        # التحقق من وجود ملف الرسم البياني
        self.assertTrue(Path(save_path).exists())
        
        # حذف ملف الرسم البياني
        if Path(save_path).exists():
            Path(save_path).unlink()


def run_tests():
    """تشغيل الاختبارات"""
    # إنشاء مجلد الاختبارات
    test_dir = Path('test_results')
    test_dir.mkdir(exist_ok=True)
    
    # إنشاء ملف لنتائج الاختبارات
    test_results_file = test_dir / 'test_results.txt'
    
    # تشغيل الاختبارات وحفظ النتائج
    with open(test_results_file, 'w', encoding='utf-8') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        suite = unittest.TestSuite()
        
        # إضافة اختبارات قاعدة البيانات
        suite.addTest(unittest.makeSuite(TestDatabaseConnector))
        suite.addTest(unittest.makeSuite(TestModels))
        
        # إضافة اختبارات الوحدات
        suite.addTest(unittest.makeSuite(TestDocumentAnalyzer))
        suite.addTest(unittest.makeSuite(TestPricingEngine))
        suite.addTest(unittest.makeSuite(TestRiskAnalyzer))
        suite.addTest(unittest.makeSuite(TestAIAssistant))
        
        # إضافة اختبارات التصميم
        suite.addTest(unittest.makeSuite(TestStyling))
        
        # تشغيل الاختبارات
        result = runner.run(suite)
        
        # كتابة ملخص النتائج
        f.write("\n\n=== ملخص نتائج الاختبارات ===\n")
        f.write(f"عدد الاختبارات: {result.testsRun}\n")
        f.write(f"عدد النجاحات: {result.testsRun - len(result.failures) - len(result.errors)}\n")
        f.write(f"عدد الإخفاقات: {len(result.failures)}\n")
        f.write(f"عدد الأخطاء: {len(result.errors)}\n")
    
    # طباعة ملخص النتائج
    logger.info(f"تم تشغيل {result.testsRun} اختبار")
    logger.info(f"النجاحات: {result.testsRun - len(result.failures) - len(result.errors)}")
    logger.info(f"الإخفاقات: {len(result.failures)}")
    logger.info(f"الأخطاء: {len(result.errors)}")
    logger.info(f"تم حفظ نتائج الاختبارات في: {test_results_file}")
    
    return result


if __name__ == "__main__":
    run_tests()
