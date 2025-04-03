"""
اختبارات وحدات نظام المناقصات

هذا الملف يحتوي على اختبارات للتحقق من عمل وحدات نظام المناقصات بشكل صحيح.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import numpy as np

# إضافة مسار المشروع إلى مسار النظام
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# محاكاة Streamlit
class StreamlitMock:
    def __init__(self):
        self.session_state = {"theme": "light"}
        self.sidebar_items = []
        self.page_items = []
    
    def title(self, text):
        self.page_items.append(f"TITLE: {text}")
        return None
    
    def header(self, text):
        self.page_items.append(f"HEADER: {text}")
        return None
    
    def subheader(self, text):
        self.page_items.append(f"SUBHEADER: {text}")
        return None
    
    def write(self, text):
        self.page_items.append(f"WRITE: {text}")
        return None
    
    def sidebar(self):
        return self
    
    def selectbox(self, label, options, index=0):
        self.page_items.append(f"SELECTBOX: {label}, OPTIONS: {options}")
        return options[index] if options else None
    
    def radio(self, label, options, index=0):
        self.page_items.append(f"RADIO: {label}, OPTIONS: {options}")
        return options[index] if options else None
    
    def checkbox(self, label, value=False):
        self.page_items.append(f"CHECKBOX: {label}, VALUE: {value}")
        return value
    
    def button(self, label):
        self.page_items.append(f"BUTTON: {label}")
        return False
    
    def file_uploader(self, label, type=None, accept_multiple_files=False):
        self.page_items.append(f"FILE_UPLOADER: {label}, TYPE: {type}")
        return None
    
    def columns(self, spec):
        cols = [StreamlitMock() for _ in range(len(spec))]
        self.page_items.append(f"COLUMNS: {spec}")
        return cols
    
    def tabs(self, tabs):
        tab_objects = [StreamlitMock() for _ in tabs]
        self.page_items.append(f"TABS: {tabs}")
        return tab_objects
    
    def expander(self, label):
        exp = StreamlitMock()
        self.page_items.append(f"EXPANDER: {label}")
        return exp
    
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
    
    def success(self, text):
        self.page_items.append(f"SUCCESS: {text}")
        return None
    
    def error(self, text):
        self.page_items.append(f"ERROR: {text}")
        return None
    
    def warning(self, text):
        self.page_items.append(f"WARNING: {text}")
        return None
    
    def info(self, text):
        self.page_items.append(f"INFO: {text}")
        return None
    
    def markdown(self, text):
        self.page_items.append(f"MARKDOWN: {text}")
        return None
    
    def metric(self, label, value, delta=None):
        self.page_items.append(f"METRIC: {label}, VALUE: {value}, DELTA: {delta}")
        return None
    
    def progress(self, value):
        self.page_items.append(f"PROGRESS: {value}")
        return None
    
    def json(self, data):
        self.page_items.append(f"JSON: {data}")
        return None
    
    def dataframe(self, data):
        self.page_items.append(f"DATAFRAME: {type(data)}")
        return None
    
    def line_chart(self, data):
        self.page_items.append(f"LINE_CHART: {type(data)}")
        return None
    
    def bar_chart(self, data):
        self.page_items.append(f"BAR_CHART: {type(data)}")
        return None
    
    def pyplot(self, fig):
        self.page_items.append(f"PYPLOT: {type(fig)}")
        return None
    
    def download_button(self, label, data, file_name, mime=None):
        self.page_items.append(f"DOWNLOAD_BUTTON: {label}, FILE_NAME: {file_name}")
        return False
    
    def form(self, key):
        form = StreamlitMock()
        self.page_items.append(f"FORM: {key}")
        return form
    
    def form_submit_button(self, label):
        self.page_items.append(f"FORM_SUBMIT_BUTTON: {label}")
        return False
    
    def rerun(self):
        self.page_items.append("RERUN")
        return None

# تعريف الاختبارات
class TestContractAnalyzer(unittest.TestCase):
    """اختبارات محلل العقود"""
    
    def test_contract_analyzer_initialization(self):
        """اختبار تهيئة محلل العقود"""
        from modules.ai_assistant.contract_analyzer import ContractAnalyzer
        
        # تهيئة المحلل
        analyzer = ContractAnalyzer()
        
        # التحقق من تهيئة الخصائص
        self.assertEqual(analyzer.api_key_source, "security_section")
        self.assertIsNotNone(analyzer.openai_api_key)
        self.assertIsNotNone(analyzer.claude_api_key)
        self.assertTrue(analyzer.hybrid_environment)
    
    def test_contract_analysis(self):
        """اختبار تحليل العقود"""
        from modules.ai_assistant.contract_analyzer import ContractAnalyzer
        
        # تهيئة المحلل
        analyzer = ContractAnalyzer()
        
        # إنشاء ملف عقد وهمي
        contract_file = "/tmp/test_contract.txt"
        with open(contract_file, "w") as f:
            f.write("عقد إنشاء مبنى إداري")
        
        # تحليل العقد
        result = analyzer.analyze_contract(contract_file)
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertIn("title", result)
        self.assertIn("summary", result)
        self.assertIn("key_points", result)
        self.assertIn("entities", result)
        
        # حذف الملف الوهمي
        os.remove(contract_file)
    
    def test_tender_analysis(self):
        """اختبار تحليل المناقصات"""
        from modules.ai_assistant.contract_analyzer import ContractAnalyzer
        
        # تهيئة المحلل
        analyzer = ContractAnalyzer()
        
        # إنشاء ملف مناقصة وهمي
        tender_file = "/tmp/test_tender.txt"
        with open(tender_file, "w") as f:
            f.write("مناقصة إنشاء مبنى إداري")
        
        # تحليل المناقصة
        result = analyzer.analyze_tender(tender_file)
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertIn("title", result)
        self.assertIn("summary", result)
        self.assertIn("key_points", result)
        self.assertIn("entities", result)
        
        # حذف الملف الوهمي
        os.remove(tender_file)
    
    def test_dwg_analysis(self):
        """اختبار تحليل ملفات DWG"""
        from modules.ai_assistant.contract_analyzer import ContractAnalyzer
        
        # تهيئة المحلل
        analyzer = ContractAnalyzer()
        
        # إنشاء ملف DWG وهمي
        dwg_file = "/tmp/test_drawing.dwg"
        with open(dwg_file, "w") as f:
            f.write("DWG FILE CONTENT")
        
        # تحليل ملف DWG
        result = analyzer.analyze_dwg_file(dwg_file)
        
        # التحقق من النتائج
        self.assertIsNotNone(result)
        self.assertIn("file_name", result)
        self.assertIn("elements_count", result)
        self.assertIn("dimensions", result)
        self.assertIn("materials", result)
        self.assertIn("cost_estimate", result)
        
        # حذف الملف الوهمي
        os.remove(dwg_file)

# تشغيل الاختبارات
if __name__ == '__main__':
    unittest.main()
