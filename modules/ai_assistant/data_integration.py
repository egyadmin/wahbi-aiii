"""
وحدة تكامل البيانات مع الذكاء الاصطناعي

هذا الملف يحتوي على الفئات والدوال اللازمة لتكامل وحدة تحليل البيانات مع وحدة الذكاء الاصطناعي.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import os
import sys
from pathlib import Path

# إضافة المسار للوصول إلى وحدة تحليل البيانات
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

# محاولة استيراد وحدة تحليل البيانات
try:
    from modules.data_analysis.data_analysis_app import DataAnalysisApp
except ImportError:
    # تعريف فئة بديلة في حالة فشل الاستيراد
    class DataAnalysisApp:
        def __init__(self):
            pass
        
        def run(self):
            pass

class DataAIIntegration:
    """فئة تكامل البيانات مع الذكاء الاصطناعي"""
    
    def __init__(self):
        """تهيئة فئة تكامل البيانات مع الذكاء الاصطناعي"""
        self.data_analysis_app = DataAnalysisApp()
    
    def analyze_tender_data(self, tender_data):
        """
        تحليل بيانات المناقصة باستخدام الذكاء الاصطناعي
        
        المعلمات:
            tender_data (dict): بيانات المناقصة
            
        العوائد:
            dict: نتائج التحليل
        """
        # تحويل البيانات إلى DataFrame
        if isinstance(tender_data, dict):
            df = pd.DataFrame([tender_data])
        elif isinstance(tender_data, list):
            df = pd.DataFrame(tender_data)
        else:
            df = tender_data
        
        # تحليل البيانات
        results = {
            'summary': self._generate_summary(df),
            'recommendations': self._generate_recommendations(df),
            'risk_analysis': self._analyze_risks(df),
            'cost_analysis': self._analyze_costs(df),
            'competitive_analysis': self._analyze_competition(df)
        }
        
        return results
    
    def analyze_historical_data(self, project_type=None, location=None, time_period=None):
        """
        تحليل البيانات التاريخية للمناقصات
        
        المعلمات:
            project_type (str): نوع المشروع (اختياري)
            location (str): الموقع (اختياري)
            time_period (str): الفترة الزمنية (اختياري)
            
        العوائد:
            dict: نتائج التحليل
        """
        # الحصول على البيانات التاريخية (محاكاة)
        historical_data = self._get_historical_data()
        
        # تطبيق التصفية إذا تم تحديدها
        filtered_data = historical_data.copy()
        
        if project_type:
            filtered_data = filtered_data[filtered_data['نوع المشروع'] == project_type]
        
        if location:
            filtered_data = filtered_data[filtered_data['الموقع'] == location]
        
        if time_period:
            # تنفيذ تصفية الفترة الزمنية (محاكاة)
            pass
        
        # تحليل البيانات
        results = {
            'win_rate': self._calculate_win_rate(filtered_data),
            'avg_profit_margin': self._calculate_avg_profit_margin(filtered_data),
            'price_trends': self._analyze_price_trends(filtered_data),
            'success_factors': self._identify_success_factors(filtered_data),
            'visualizations': self._generate_visualizations(filtered_data)
        }
        
        return results
    
    def predict_tender_success(self, tender_data):
        """
        التنبؤ بفرص نجاح المناقصة
        
        المعلمات:
            tender_data (dict): بيانات المناقصة
            
        العوائد:
            dict: نتائج التنبؤ
        """
        # تحويل البيانات إلى DataFrame
        if isinstance(tender_data, dict):
            df = pd.DataFrame([tender_data])
        elif isinstance(tender_data, list):
            df = pd.DataFrame(tender_data)
        else:
            df = tender_data
        
        # تنفيذ التنبؤ (محاكاة)
        success_probability = np.random.uniform(0, 100)
        
        # تحديد العوامل المؤثرة (محاكاة)
        factors = [
            {'name': 'السعر التنافسي', 'impact': np.random.uniform(0, 1), 'direction': 'إيجابي' if np.random.random() > 0.5 else 'سلبي'},
            {'name': 'الخبرة السابقة', 'impact': np.random.uniform(0, 1), 'direction': 'إيجابي' if np.random.random() > 0.5 else 'سلبي'},
            {'name': 'الجودة الفنية', 'impact': np.random.uniform(0, 1), 'direction': 'إيجابي' if np.random.random() > 0.5 else 'سلبي'},
            {'name': 'المدة الزمنية', 'impact': np.random.uniform(0, 1), 'direction': 'إيجابي' if np.random.random() > 0.5 else 'سلبي'},
            {'name': 'المنافسة', 'impact': np.random.uniform(0, 1), 'direction': 'إيجابي' if np.random.random() > 0.5 else 'سلبي'}
        ]
        
        # ترتيب العوامل حسب التأثير
        factors = sorted(factors, key=lambda x: x['impact'], reverse=True)
        
        # إعداد النتائج
        results = {
            'success_probability': success_probability,
            'confidence': np.random.uniform(70, 95),
            'factors': factors,
            'recommendations': self._generate_success_recommendations(factors)
        }
        
        return results
    
    def optimize_pricing(self, tender_data, competitors_data=None):
        """
        تحسين التسعير للمناقصة
        
        المعلمات:
            tender_data (dict): بيانات المناقصة
            competitors_data (list): بيانات المنافسين (اختياري)
            
        العوائد:
            dict: نتائج التحسين
        """
        # تحويل البيانات إلى DataFrame
        if isinstance(tender_data, dict):
            df = pd.DataFrame([tender_data])
        elif isinstance(tender_data, list):
            df = pd.DataFrame(tender_data)
        else:
            df = tender_data
        
        # تحليل بيانات المنافسين إذا كانت متوفرة
        if competitors_data:
            competitors_df = pd.DataFrame(competitors_data)
        else:
            # استخدام بيانات افتراضية للمنافسين
            competitors_df = self._get_competitors_data()
        
        # تنفيذ تحسين التسعير (محاكاة)
        base_price = float(df['الميزانية التقديرية'].iloc[0]) if 'الميزانية التقديرية' in df.columns else 10000000
        
        # حساب نطاق السعر المقترح
        min_price = base_price * 0.85
        optimal_price = base_price * 0.92
        max_price = base_price * 0.98
        
        # تحليل حساسية السعر
        price_sensitivity = []
        for price_factor in np.linspace(0.8, 1.1, 7):
            price = base_price * price_factor
            win_probability = max(0, min(100, 100 - (price_factor - 0.9) * 200))
            profit = price - (base_price * 0.75)
            expected_value = win_probability / 100 * profit
            
            price_sensitivity.append({
                'price_factor': price_factor,
                'price': price,
                'win_probability': win_probability,
                'profit': profit,
                'expected_value': expected_value
            })
        
        # إعداد النتائج
        results = {
            'min_price': min_price,
            'optimal_price': optimal_price,
            'max_price': max_price,
            'price_sensitivity': price_sensitivity,
            'market_position': self._analyze_market_position(optimal_price, competitors_df),
            'recommendations': self._generate_pricing_recommendations(optimal_price, price_sensitivity)
        }
        
        return results
    
    def analyze_dwg_files(self, file_path):
        """
        تحليل ملفات DWG باستخدام الذكاء الاصطناعي
        
        المعلمات:
            file_path (str): مسار ملف DWG
            
        العوائد:
            dict: نتائج التحليل
        """
        # محاكاة تحليل ملف DWG
        results = {
            'file_name': os.path.basename(file_path),
            'file_size': f"{np.random.randint(1, 10)} MB",
            'elements_count': np.random.randint(100, 1000),
            'layers_count': np.random.randint(5, 20),
            'dimensions': {
                'width': f"{np.random.randint(10, 100)} م",
                'height': f"{np.random.randint(10, 100)} م",
                'area': f"{np.random.randint(100, 10000)} م²"
            },
            'elements': {
                'walls': np.random.randint(10, 100),
                'doors': np.random.randint(5, 50),
                'windows': np.random.randint(5, 50),
                'columns': np.random.randint(5, 50),
                'stairs': np.random.randint(1, 10)
            },
            'materials': [
                {'name': 'خرسانة', 'volume': f"{np.random.randint(10, 1000)} م³"},
                {'name': 'حديد', 'weight': f"{np.random.randint(1, 100)} طن"},
                {'name': 'طابوق', 'count': f"{np.random.randint(1000, 10000)} قطعة"},
                {'name': 'زجاج', 'area': f"{np.random.randint(10, 1000)} م²"},
                {'name': 'خشب', 'volume': f"{np.random.randint(1, 50)} م³"}
            ],
            'cost_estimate': {
                'materials': np.random.randint(100000, 1000000),
                'labor': np.random.randint(50000, 500000),
                'equipment': np.random.randint(10000, 100000),
                'total': np.random.randint(200000, 2000000)
            },
            'recommendations': [
                'يمكن تقليل تكلفة المواد باستخدام بدائل أقل تكلفة',
                'يمكن تحسين كفاءة استخدام المساحة',
                'يمكن تقليل عدد الأعمدة لتوفير التكلفة',
                'يمكن تحسين تصميم السلالم لزيادة السلامة',
                'يمكن تحسين توزيع النوافذ لزيادة الإضاءة الطبيعية'
            ]
        }
        
        return results
    
    def integrate_with_ai_assistant(self, ai_assistant):
        """
        تكامل وحدة تحليل البيانات مع وحدة الذكاء الاصطناعي
        
        المعلمات:
            ai_assistant: كائن وحدة الذكاء الاصطناعي
            
        العوائد:
            bool: نجاح التكامل
        """
        try:
            # إضافة وظائف تحليل البيانات إلى وحدة الذكاء الاصطناعي
            ai_assistant.data_integration = self
            
            # إضافة دوال التحليل إلى وحدة الذكاء الاصطناعي
            ai_assistant.analyze_tender_data = self.analyze_tender_data
            ai_assistant.analyze_historical_data = self.analyze_historical_data
            ai_assistant.predict_tender_success = self.predict_tender_success
            ai_assistant.optimize_pricing = self.optimize_pricing
            ai_assistant.analyze_dwg_files = self.analyze_dwg_files
            
            return True
        except Exception as e:
            print(f"خطأ في تكامل وحدة تحليل البيانات مع وحدة الذكاء الاصطناعي: {str(e)}")
            return False
    
    # دوال مساعدة داخلية
    
    def _get_historical_data(self):
        """الحصول على البيانات التاريخية"""
        # محاكاة البيانات التاريخية
        np.random.seed(42)
        
        n_tenders = 50
        tender_ids = [f"T-{2021 + i//20}-{i%20 + 1:03d}" for i in range(n_tenders)]
        tender_types = np.random.choice(["مبنى إداري", "مبنى سكني", "مدرسة", "مستشفى", "طرق", "جسور", "بنية تحتية"], n_tenders)
        tender_locations = np.random.choice(["الرياض", "جدة", "الدمام", "مكة", "المدينة", "أبها", "تبوك"], n_tenders)
        tender_areas = np.random.randint(1000, 10000, n_tenders)
        tender_durations = np.random.randint(6, 36, n_tenders)
        tender_budgets = np.random.randint(1000000, 50000000, n_tenders)
        tender_costs = np.array([budget * np.random.uniform(0.8, 1.1) for budget in tender_budgets])
        tender_profits = tender_budgets - tender_costs
        tender_profit_margins = tender_profits / tender_budgets * 100
        tender_statuses = np.random.choice(["فائز", "خاسر", "قيد التنفيذ", "منجز"], n_tenders)
        tender_dates = [f"202{1 + i//20}-{np.random.randint(1, 13):02d}-{np.random.randint(1, 29):02d}" for i in range(n_tenders)]
        
        # إنشاء DataFrame للمناقصات السابقة
        tenders_data = {
            "رقم المناقصة": tender_ids,
            "نوع المشروع": tender_types,
            "الموقع": tender_locations,
            "المساحة (م2)": tender_areas,
            "المدة (شهر)": tender_durations,
            "الميزانية (ريال)": tender_budgets,
            "التكلفة (ريال)": tender_costs,
            "الربح (ريال)": tender_profits,
            "هامش الربح (%)": tender_profit_margins,
            "الحالة": tender_statuses,
            "تاريخ التقديم": tender_dates
        }
        
        return pd.DataFrame(tenders_data)
    
    def _get_competitors_data(self):
        """الحصول على بيانات المنافسين"""
        # محاكاة بيانات المنافسين
        n_competitors = 10
        competitor_ids = [f"C-{i+1:02d}" for i in range(n_competitors)]
        competitor_names = [
            "شركة الإنشاءات المتطورة", "شركة البناء الحديث", "شركة التطوير العمراني", "شركة الإعمار الدولية",
            "شركة البنية التحتية المتكاملة", "شركة المقاولات العامة", "شركة التشييد والبناء", "شركة الهندسة والإنشاءات",
            "شركة المشاريع الكبرى", "شركة التطوير العقاري"
        ]
        competitor_specialties = np.random.choice(["مباني", "طرق", "جسور", "بنية تحتية", "متعددة"], n_competitors)
        competitor_sizes = np.random.choice(["صغيرة", "متوسطة", "كبيرة"], n_competitors)
        competitor_market_shares = np.random.uniform(1, 15, n_competitors)
        competitor_win_rates = np.random.uniform(10, 60, n_competitors)
        competitor_avg_margins = np.random.uniform(5, 20, n_competitors)
        
        # إنشاء DataFrame للمنافسين
        competitors_data = {
            "رمز المنافس": competitor_ids,
            "اسم المنافس": competitor_names,
            "التخصص": competitor_specialties,
            "الحجم": competitor_sizes,
            "حصة السوق (%)": competitor_market_shares,
            "معدل الفوز (%)": competitor_win_rates,
            "متوسط هامش الربح (%)": competitor_avg_margins
        }
        
        return pd.DataFrame(competitors_data)
    
    def _generate_summary(self, df):
        """توليد ملخص للبيانات"""
        # محاكاة توليد ملخص
        return "تحليل البيانات يشير إلى أن هذه المناقصة تتعلق بمشروع إنشائي متوسط الحجم. تتضمن المناقصة متطلبات فنية متوسطة المستوى وشروط تعاقدية معيارية. بناءً على البيانات التاريخية، هناك فرصة جيدة للفوز بهذه المناقصة إذا تم تقديم عرض تنافسي مع التركيز على الجوانب الفنية والجودة."
    
    def _generate_recommendations(self, df):
        """توليد توصيات بناءً على البيانات"""
        # محاكاة توليد توصيات
        return [
            "تقديم عرض سعر تنافسي يقل بنسبة 5-10% عن الميزانية التقديرية",
            "التركيز على الخبرات السابقة في مشاريع مماثلة",
            "تقديم حلول مبتكرة لتقليل مدة التنفيذ",
            "تعزيز الجوانب الفنية في العرض",
            "تقديم خطة تنفيذ مفصلة مع جدول زمني واضح"
        ]
    
    def _analyze_risks(self, df):
        """تحليل المخاطر"""
        # محاكاة تحليل المخاطر
        return [
            {"risk": "ارتفاع أسعار المواد", "probability": "متوسطة", "impact": "عالي", "mitigation": "تثبيت أسعار المواد الرئيسية مع الموردين"},
            {"risk": "تأخر التنفيذ", "probability": "متوسطة", "impact": "عالي", "mitigation": "وضع خطة تنفيذ مفصلة مع هوامش زمنية"},
            {"risk": "نقص العمالة الماهرة", "probability": "منخفضة", "impact": "متوسط", "mitigation": "التعاقد المسبق مع مقاولي الباطن"},
            {"risk": "تغيير نطاق العمل", "probability": "متوسطة", "impact": "عالي", "mitigation": "توثيق نطاق العمل بدقة وتحديد إجراءات التغيير"},
            {"risk": "مشاكل في التربة", "probability": "منخفضة", "impact": "عالي", "mitigation": "إجراء فحوصات شاملة للتربة قبل البدء"}
        ]
    
    def _analyze_costs(self, df):
        """تحليل التكاليف"""
        # محاكاة تحليل التكاليف
        total_budget = float(df['الميزانية التقديرية'].iloc[0]) if 'الميزانية التقديرية' in df.columns else 10000000
        
        # توزيع التكاليف
        materials_cost = total_budget * 0.6
        labor_cost = total_budget * 0.25
        equipment_cost = total_budget * 0.1
        overhead_cost = total_budget * 0.05
        
        return {
            "total_budget": total_budget,
            "cost_breakdown": [
                {"category": "المواد", "amount": materials_cost, "percentage": 60},
                {"category": "العمالة", "amount": labor_cost, "percentage": 25},
                {"category": "المعدات", "amount": equipment_cost, "percentage": 10},
                {"category": "المصاريف العامة", "amount": overhead_cost, "percentage": 5}
            ],
            "cost_saving_opportunities": [
                {"item": "استخدام مواد بديلة", "potential_saving": total_budget * 0.05},
                {"item": "تحسين إنتاجية العمالة", "potential_saving": total_budget * 0.03},
                {"item": "تأجير المعدات بدلاً من شرائها", "potential_saving": total_budget * 0.02}
            ]
        }
    
    def _analyze_competition(self, df):
        """تحليل المنافسة"""
        # محاكاة تحليل المنافسة
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
    
    def _calculate_win_rate(self, df):
        """حساب معدل الفوز"""
        # محاكاة حساب معدل الفوز
        if 'الحالة' in df.columns:
            total_tenders = len(df)
            won_tenders = len(df[df['الحالة'] == 'فائز'])
            win_rate = won_tenders / total_tenders * 100 if total_tenders > 0 else 0
        else:
            win_rate = 35  # قيمة افتراضية
        
        return {
            "overall_win_rate": win_rate,
            "win_rate_by_type": [
                {"type": "مبنى إداري", "win_rate": 40},
                {"type": "مبنى سكني", "win_rate": 35},
                {"type": "مدرسة", "win_rate": 45},
                {"type": "مستشفى", "win_rate": 30},
                {"type": "طرق", "win_rate": 25},
                {"type": "جسور", "win_rate": 20},
                {"type": "بنية تحتية", "win_rate": 30}
            ],
            "win_rate_by_location": [
                {"location": "الرياض", "win_rate": 40},
                {"location": "جدة", "win_rate": 35},
                {"location": "الدمام", "win_rate": 30},
                {"location": "مكة", "win_rate": 25},
                {"location": "المدينة", "win_rate": 30},
                {"location": "أبها", "win_rate": 35},
                {"location": "تبوك", "win_rate": 40}
            ]
        }
    
    def _calculate_avg_profit_margin(self, df):
        """حساب متوسط هامش الربح"""
        # محاكاة حساب متوسط هامش الربح
        if 'هامش الربح (%)' in df.columns:
            avg_profit_margin = df['هامش الربح (%)'].mean()
        else:
            avg_profit_margin = 15  # قيمة افتراضية
        
        return {
            "overall_avg_profit_margin": avg_profit_margin,
            "profit_margin_by_type": [
                {"type": "مبنى إداري", "profit_margin": 18},
                {"type": "مبنى سكني", "profit_margin": 15},
                {"type": "مدرسة", "profit_margin": 20},
                {"type": "مستشفى", "profit_margin": 12},
                {"type": "طرق", "profit_margin": 10},
                {"type": "جسور", "profit_margin": 8},
                {"type": "بنية تحتية", "profit_margin": 14}
            ],
            "profit_margin_by_location": [
                {"location": "الرياض", "profit_margin": 16},
                {"location": "جدة", "profit_margin": 14},
                {"location": "الدمام", "profit_margin": 15},
                {"location": "مكة", "profit_margin": 12},
                {"location": "المدينة", "profit_margin": 13},
                {"location": "أبها", "profit_margin": 18},
                {"location": "تبوك", "profit_margin": 17}
            ]
        }
    
    def _analyze_price_trends(self, df):
        """تحليل اتجاهات الأسعار"""
        # محاكاة تحليل اتجاهات الأسعار
        return {
            "price_trends_by_year": [
                {"year": 2021, "avg_price_per_sqm": 3500},
                {"year": 2022, "avg_price_per_sqm": 3800},
                {"year": 2023, "avg_price_per_sqm": 4200},
                {"year": 2024, "avg_price_per_sqm": 4500}
            ],
            "price_trends_by_material": [
                {"material": "خرسانة", "price_change": 15},
                {"material": "حديد", "price_change": 20},
                {"material": "أسمنت", "price_change": 10},
                {"material": "طابوق", "price_change": 5},
                {"material": "ألمنيوم", "price_change": 25}
            ],
            "price_forecast": [
                {"year": 2025, "forecasted_price_change": 8},
                {"year": 2026, "forecasted_price_change": 5},
                {"year": 2027, "forecasted_price_change": 3}
            ]
        }
    
    def _identify_success_factors(self, df):
        """تحديد عوامل النجاح"""
        # محاكاة تحديد عوامل النجاح
        return [
            {"factor": "السعر التنافسي", "importance": 0.8, "description": "تقديم أسعار أقل من المنافسين بنسبة 5-10%"},
            {"factor": "الجودة الفنية", "importance": 0.7, "description": "تقديم حلول فنية متميزة ومبتكرة"},
            {"factor": "الخبرة السابقة", "importance": 0.6, "description": "إظهار خبرة سابقة في مشاريع مماثلة"},
            {"factor": "مدة التنفيذ", "importance": 0.5, "description": "تقديم جدول زمني أقصر من المطلوب"},
            {"factor": "السمعة", "importance": 0.4, "description": "سمعة جيدة في السوق وعلاقات قوية مع العملاء"}
        ]
    
    def _generate_visualizations(self, df):
        """توليد الرسوم البيانية"""
        # محاكاة توليد الرسوم البيانية
        return {
            "visualization_types": [
                "توزيع المناقصات حسب النوع",
                "توزيع المناقصات حسب الموقع",
                "معدل الفوز حسب النوع",
                "معدل الفوز حسب الموقع",
                "متوسط هامش الربح حسب النوع",
                "متوسط هامش الربح حسب الموقع",
                "اتجاهات الأسعار عبر الزمن"
            ]
        }
    
    def _generate_success_recommendations(self, factors):
        """توليد توصيات لزيادة فرص النجاح"""
        # محاكاة توليد توصيات
        return [
            "تخفيض السعر بنسبة 5-10% لزيادة التنافسية",
            "تعزيز الجوانب الفنية في العرض",
            "إبراز الخبرات السابقة في مشاريع مماثلة",
            "تقديم جدول زمني أقصر من المطلوب",
            "تقديم ضمانات إضافية للجودة"
        ]
    
    def _analyze_market_position(self, price, competitors_df):
        """تحليل الموقف التنافسي في السوق"""
        # محاكاة تحليل الموقف التنافسي
        return {
            "market_position": "متوسط",
            "price_percentile": 45,
            "competitors_below": 3,
            "competitors_above": 7,
            "price_competitiveness": "عالية"
        }
    
    def _generate_pricing_recommendations(self, optimal_price, price_sensitivity):
        """توليد توصيات التسعير"""
        # محاكاة توليد توصيات التسعير
        return [
            f"السعر الأمثل: {optimal_price:,.0f} ريال",
            "تقديم خصم إضافي للعميل المتكرر",
            "تقديم خيارات دفع مرنة",
            "تضمين خدمات إضافية لتعزيز القيمة",
            "تقديم ضمانات إضافية لتبرير السعر"
        ]
