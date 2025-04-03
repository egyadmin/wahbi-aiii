import unittest
import sys
import os
import pandas as pd
import numpy as np
import streamlit as st
from unittest.mock import patch, MagicMock

# إضافة مسار الوحدات
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# استيراد الوحدات للاختبار
from pricing_system.integration_framework import IntegrationFramework
from pricing_system.modules.catalogs.equipment_catalog import EquipmentCatalog
from pricing_system.modules.catalogs.materials_catalog import MaterialsCatalog
from pricing_system.modules.catalogs.labor_catalog import LaborCatalog
from pricing_system.modules.catalogs.subcontractors_catalog import SubcontractorsCatalog
from pricing_system.modules.analysis.smart_price_analysis import SmartPriceAnalysis
from pricing_system.modules.indirect_support.indirect_support_management import IndirectSupportManagement
from pricing_system.modules.pricing_strategies.pricing_strategies import PricingStrategies

class TestIntegratedSystem(unittest.TestCase):
    """
    اختبارات النظام المتكامل للتأكد من عمل جميع المكونات معًا بشكل صحيح
    """
    
    def setUp(self):
        """
        إعداد بيئة الاختبار
        """
        # تهيئة حالة الجلسة الوهمية
        st.session_state = {}
        
        # إنشاء مثيلات من الوحدات للاختبار
        self.equipment_catalog = EquipmentCatalog()
        self.materials_catalog = MaterialsCatalog()
        self.labor_catalog = LaborCatalog()
        self.subcontractors_catalog = SubcontractorsCatalog()
        self.smart_price_analysis = SmartPriceAnalysis()
        self.indirect_support = IndirectSupportManagement()
        self.pricing_strategies = PricingStrategies()
        
        # إنشاء مثيل من إطار التكامل
        self.integration_framework = IntegrationFramework()
        
        # إعداد بيانات اختبار المشروع
        self.project_data = {
            'name': 'مشروع اختبار',
            'location': 'الرياض',
            'client': 'وزارة الإسكان',
            'start_date': '2025-01-01',
            'end_date': '2025-12-31',
            'budget': 10000000.0,
            'boq_items': [
                {
                    'item_code': 'B001',
                    'description': 'حفر وردم',
                    'unit': 'م3',
                    'quantity': 1000.0,
                    'unit_price': 50.0,
                    'total_price': 50000.0
                },
                {
                    'item_code': 'B002',
                    'description': 'خرسانة مسلحة',
                    'unit': 'م3',
                    'quantity': 500.0,
                    'unit_price': 1200.0,
                    'total_price': 600000.0
                },
                {
                    'item_code': 'B003',
                    'description': 'أعمال تشطيبات',
                    'unit': 'م2',
                    'quantity': 2000.0,
                    'unit_price': 300.0,
                    'total_price': 600000.0
                }
            ],
            'resources': [],
            'pricing_strategy': 'standard',
            'indirect_costs': {},
            'profit_margin': 0.15,
            'local_content_target': 0.40
        }
        
        # إضافة بيانات اختبار للكتالوجات
        self._add_test_data_to_catalogs()
    
    def _add_test_data_to_catalogs(self):
        """
        إضافة بيانات اختبار إلى الكتالوجات
        """
        # إضافة معدات للاختبار
        equipment_data = [
            {
                'name': 'حفار',
                'type': 'حفار',
                'description': 'حفار هيدروليكي',
                'price_per_hour': 200.0,
                'price_per_day': 1600.0,
                'price_per_week': 8000.0,
                'price_per_month': 30000.0,
                'is_local': True
            },
            {
                'name': 'لودر',
                'type': 'لودر',
                'description': 'لودر متوسط الحجم',
                'price_per_hour': 150.0,
                'price_per_day': 1200.0,
                'price_per_week': 6000.0,
                'price_per_month': 22000.0,
                'is_local': False
            },
            {
                'name': 'شاحنة نقل',
                'type': 'شاحنة',
                'description': 'شاحنة نقل ثقيلة',
                'price_per_hour': 120.0,
                'price_per_day': 960.0,
                'price_per_week': 4800.0,
                'price_per_month': 18000.0,
                'is_local': True
            }
        ]
        
        for equipment in equipment_data:
            self.equipment_catalog.add_equipment(equipment['name'], equipment)
        
        # إضافة مواد للاختبار
        materials_data = [
            {
                'name': 'اسمنت',
                'description': 'اسمنت بورتلاندي',
                'unit': 'طن',
                'price': 600.0,
                'is_local': True
            },
            {
                'name': 'حديد تسليح',
                'description': 'حديد تسليح قطر 16 مم',
                'unit': 'طن',
                'price': 3500.0,
                'is_local': True
            },
            {
                'name': 'رمل',
                'description': 'رمل ناعم للخرسانة',
                'unit': 'م3',
                'price': 80.0,
                'is_local': True
            },
            {
                'name': 'بلاط سيراميك',
                'description': 'بلاط سيراميك للأرضيات',
                'unit': 'م2',
                'price': 120.0,
                'is_local': False
            }
        ]
        
        for material in materials_data:
            self.materials_catalog.add_material(material['name'], material)
        
        # إضافة عمالة للاختبار
        labor_data = [
            {
                'name': 'مهندس مدني',
                'type': 'مهندس مدني',
                'description': 'مهندس مدني خبرة 5 سنوات',
                'price_per_hour': 100.0,
                'price_per_day': 800.0,
                'price_per_week': 4000.0,
                'price_per_month': 15000.0,
                'is_local': True
            },
            {
                'name': 'عامل بناء',
                'type': 'عامل بناء',
                'description': 'عامل بناء ماهر',
                'price_per_hour': 20.0,
                'price_per_day': 160.0,
                'price_per_week': 800.0,
                'price_per_month': 3000.0,
                'is_local': False
            },
            {
                'name': 'فني كهرباء',
                'type': 'كهربائي',
                'description': 'فني كهرباء خبرة 3 سنوات',
                'price_per_hour': 30.0,
                'price_per_day': 240.0,
                'price_per_week': 1200.0,
                'price_per_month': 4500.0,
                'is_local': True
            }
        ]
        
        for labor in labor_data:
            self.labor_catalog.add_labor(labor['name'], labor)
        
        # إضافة مقاولي باطن للاختبار
        subcontractors_data = [
            {
                'name': 'شركة الأعمال الكهربائية',
                'specialization': 'أعمال كهربائية',
                'description': 'شركة متخصصة في الأعمال الكهربائية',
                'contact_info': 'info@electrical-works.com',
                'is_local': True
            },
            {
                'name': 'مؤسسة أنظمة التكييف',
                'specialization': 'أعمال تكييف',
                'description': 'مؤسسة متخصصة في أنظمة التكييف',
                'contact_info': 'info@hvac-systems.com',
                'is_local': True
            },
            {
                'name': 'شركة أنظمة المراقبة',
                'specialization': 'أعمال CCTV',
                'description': 'شركة متخصصة في أنظمة المراقبة والكاميرات',
                'contact_info': 'info@cctv-systems.com',
                'is_local': False
            }
        ]
        
        for subcontractor in subcontractors_data:
            self.subcontractors_catalog.add_subcontractor(subcontractor['name'], subcontractor)
        
        # إضافة إدارات مساندة للاختبار
        departments_data = [
            {
                'name': 'إدارة المشاريع',
                'description': 'إدارة متابعة وتنفيذ المشاريع',
                'monthly_cost': 100000.0,
                'employees_count': 10,
                'allocation_percentage': 20.0
            },
            {
                'name': 'إدارة المشتريات',
                'description': 'إدارة المشتريات والتوريدات',
                'monthly_cost': 80000.0,
                'employees_count': 8,
                'allocation_percentage': 15.0
            },
            {
                'name': 'الإدارة المالية',
                'description': 'الإدارة المالية والمحاسبة',
                'monthly_cost': 70000.0,
                'employees_count': 7,
                'allocation_percentage': 10.0
            }
        ]
        
        for department in departments_data:
            self.indirect_support.add_department(department['name'], department)
    
    def test_equipment_catalog_integration(self):
        """
        اختبار تكامل كتالوج المعدات
        """
        # التحقق من وجود المعدات في الكتالوج
        equipment_list = self.equipment_catalog.get_equipment_list()
        self.assertEqual(len(equipment_list), 3)
        self.assertIn('حفار', equipment_list)
        self.assertIn('لودر', equipment_list)
        self.assertIn('شاحنة نقل', equipment_list)
        
        # التحقق من تفاصيل المعدات
        حفار_details = self.equipment_catalog.get_equipment_details('حفار')
        self.assertEqual(حفار_details['price_per_day'], 1600.0)
        self.assertTrue(حفار_details['is_local'])
        
        لودر_details = self.equipment_catalog.get_equipment_details('لودر')
        self.assertEqual(لودر_details['price_per_day'], 1200.0)
        self.assertFalse(لودر_details['is_local'])
    
    def test_materials_catalog_integration(self):
        """
        اختبار تكامل كتالوج المواد
        """
        # التحقق من وجود المواد في الكتالوج
        materials_list = self.materials_catalog.get_materials_list()
        self.assertEqual(len(materials_list), 4)
        self.assertIn('اسمنت', materials_list)
        self.assertIn('حديد تسليح', materials_list)
        self.assertIn('رمل', materials_list)
        self.assertIn('بلاط سيراميك', materials_list)
        
        # التحقق من تفاصيل المواد
        اسمنت_details = self.materials_catalog.get_material_details('اسمنت')
        self.assertEqual(اسمنت_details['price'], 600.0)
        self.assertEqual(اسمنت_details['unit'], 'طن')
        self.assertTrue(اسمنت_details['is_local'])
        
        بلاط_details = self.materials_catalog.get_material_details('بلاط سيراميك')
        self.assertEqual(بلاط_details['price'], 120.0)
        self.assertEqual(بلاط_details['unit'], 'م2')
        self.assertFalse(بلاط_details['is_local'])
    
    def test_labor_catalog_integration(self):
        """
        اختبار تكامل كتالوج العمالة
        """
        # التحقق من وجود العمالة في الكتالوج
        labor_list = self.labor_catalog.get_labor_list()
        self.assertEqual(len(labor_list), 3)
        self.assertIn('مهندس مدني', labor_list)
        self.assertIn('عامل بناء', labor_list)
        self.assertIn('فني كهرباء', labor_list)
        
        # التحقق من تفاصيل العمالة
        مهندس_details = self.labor_catalog.get_labor_details('مهندس مدني')
        self.assertEqual(مهندس_details['price_per_month'], 15000.0)
        self.assertTrue(مهندس_details['is_local'])
        
        عامل_details = self.labor_catalog.get_labor_details('عامل بناء')
        self.assertEqual(عامل_details['price_per_day'], 160.0)
        self.assertFalse(عامل_details['is_local'])
    
    def test_subcontractors_catalog_integration(self):
        """
        اختبار تكامل كتالوج مقاولي الباطن
        """
        # التحقق من وجود مقاولي الباطن في الكتالوج
        subcontractors_list = self.subcontractors_catalog.get_subcontractors_list()
        self.assertEqual(len(subcontractors_list), 3)
        self.assertIn('شركة الأعمال الكهربائية', subcontractors_list)
        self.assertIn('مؤسسة أنظمة التكييف', subcontractors_list)
        self.assertIn('شركة أنظمة المراقبة', subcontractors_list)
        
        # التحقق من تفاصيل مقاولي الباطن
        كهرباء_details = self.subcontractors_catalog.get_subcontractor_details('شركة الأعمال الكهربائية')
        self.assertEqual(كهرباء_details['specialization'], 'أعمال كهربائية')
        self.assertTrue(كهرباء_details['is_local'])
        
        مراقبة_details = self.subcontractors_catalog.get_subcontractor_details('شركة أنظمة المراقبة')
        self.assertEqual(مراقبة_details['specialization'], 'أعمال CCTV')
        self.assertFalse(مراقبة_details['is_local'])
    
    def test_indirect_support_integration(self):
        """
        اختبار تكامل إدارة الإدارات المساندة
        """
        # التحقق من وجود الإدارات المساندة
        departments = self.indirect_support.get_departments()
        self.assertEqual(len(departments), 3)
        self.assertIn('إدارة المشاريع', departments)
        self.assertIn('إدارة المشتريات', departments)
        self.assertIn('الإدارة المالية', departments)
        
        # التحقق من تفاصيل الإدارات المساندة
        مشاريع_details = self.indirect_support.get_department_details('إدارة المشاريع')
        self.assertEqual(مشاريع_details['monthly_cost'], 100000.0)
        self.assertEqual(مشاريع_details['allocation_percentage'], 20.0)
        
        # التحقق من حساب التكاليف الإجمالية
        total_monthly_cost = self.indirect_support.get_total_monthly_cost()
        self.assertEqual(total_monthly_cost, 250000.0)
        
        total_allocated_cost = self.indirect_support.get_total_allocated_cost()
        self.assertEqual(total_allocated_cost, 45000.0)  # (100000*0.2 + 80000*0.15 + 70000*0.1)
    
    def test_smart_price_analysis_integration(self):
        """
        اختبار تكامل التحليل الذكي للأسعار
        """
        # إضافة تحليل لبنود المشروع
        for i, item in enumerate(self.project_data['boq_items']):
            analysis = {
                'direct_cost': item['total_price'] * 0.7,  # 70% من السعر الإجمالي
                'indirect_cost': item['total_price'] * 0.15,  # 15% من السعر الإجمالي
                'profit_margin': item['total_price'] * 0.15,  # 15% من السعر الإجمالي
                'total_price': item['total_price'],
                'materials': [
                    {
                        'name': 'اسمنت',
                        'quantity': 10,
                        'unit': 'طن',
                        'price': 600.0,
                        'total': 6000.0,
                        'is_local': True
                    },
                    {
                        'name': 'حديد تسليح',
                        'quantity': 5,
                        'unit': 'طن',
                        'price': 3500.0,
                        'total': 17500.0,
                        'is_local': True
                    }
                ],
                'equipment': [
                    {
                        'name': 'حفار',
                        'duration': 5,
                        'duration_unit': 'يوم',
                        'price': 1600.0,
                        'total': 8000.0,
                        'is_local': True
                    }
                ],
                'labor': [
                    {
                        'name': 'عامل بناء',
                        'duration': 20,
                        'duration_unit': 'يوم',
                        'price': 160.0,
                        'total': 3200.0,
                        'is_local': False
                    }
                ],
                'materials_cost': 23500.0,
                'equipment_cost': 8000.0,
                'labor_cost': 3200.0,
                'subcontractors_cost': 0.0
            }
            
            self.smart_price_analysis.add_item_analysis(i, analysis)
        
        # التحقق من تحليل البنود
        all_analyses = self.smart_price_analysis.get_all_items_analysis()
        self.assertEqual(len(all_analyses), 3)
        
        # التحقق من تحليل التكاليف الإجمالية للمشروع
        cost_analysis = self.smart_price_analysis.get_project_cost_analysis()
        self.assertEqual(cost_analysis['total_materials_cost'], 23500.0 * 3)
        self.assertEqual(cost_analysis['total_equipment_cost'], 8000.0 * 3)
        self.assertEqual(cost_analysis['total_labor_cost'], 3200.0 * 3)
        
        # التحقق من المواد الأكثر تكلفة
        top_materials = self.smart_price_analysis.get_top_materials(limit=2)
        self.assertEqual(len(top_materials), 2)
        self.assertEqual(top_materials[0]['name'], 'حديد تسليح')
        self.assertEqual(top_materials[0]['total_cost'], 17500.0 * 3)
    
    def test_pricing_strategies_integration(self):
        """
        اختبار تكامل استراتيجيات التسعير
        """
        # تطبيق استراتيجية التسعير القياسي
        result = self.pricing_strategies.apply_strategy(
            'standard',
            self.project_data,
            self.smart_price_analysis
        )
        
        self.assertTrue(result['success'])
        self.assertEqual(len(result['items_result']), 3)
        
        # التحقق من نتائج تطبيق الاستراتيجية
        total_cost = sum(item['cost'] for item in result['items_result'])
        total_price = sum(item['price'] for item in result['items_result'])
        profit_margin = total_price - total_cost
        
        self.assertEqual(result['total_cost'], total_cost)
        self.assertEqual(result['total_price'], total_price)
        self.assertEqual(result['profit_margin'], profit_margin)
        
        # مقارنة استراتيجيات التسعير
        comparison_result = self.pricing_strategies.compare_strategies(
            self.project_data,
            self.smart_price_analysis
        )
        
        self.assertTrue(comparison_result['success'])
        self.assertEqual(len(comparison_result['strategies_result']), 6)  # 6 استراتيجيات
    
    def test_local_content_analysis_integration(self):
        """
        اختبار تكامل تحليل المحتوى المحلي
        """
        # تحليل المحتوى المحلي
        local_content_analysis = self.pricing_strategies.analyze_local_content(
            self.project_data,
            self.smart_price_analysis
        )
        
        self.assertTrue(local_content_analysis['success'])
        
        # التحقق من نتائج تحليل المحتوى المحلي
        self.assertIn('local_content_percentage', local_content_analysis)
        self.assertIn('resources_local_content', local_content_analysis)
        
        # التحقق من تحليل المحتوى المحلي حسب نوع الموارد
        resources_local_content = local_content_analysis['resources_local_content']
        self.assertIn('materials', resources_local_content)
        self.assertIn('equipment', resources_local_content)
        self.assertIn('labor', resources_local_content)
        
        # التحقق من التوصيات
        if local_content_analysis['local_content_percentage'] < self.project_data['local_content_target']:
            self.assertIn('recommendations', local_content_analysis)
            self.assertTrue(len(local_content_analysis['recommendations']) > 0)
    
    def test_integration_framework(self):
        """
        اختبار إطار التكامل
        """
        # تهيئة حالة الجلسة
        st.session_state = {}
        
        # إنشاء مثيلات وهمية من PricingApp و ResourcesApp
        pricing_app_mock = MagicMock()
        pricing_app_mock.tabs = ["جدول الكميات", "تحليل التكاليف", "سيناريوهات التسعير", "التحليل التنافسي", "التقارير"]
        pricing_app_mock._render_bill_of_quantities_tab = MagicMock()
        pricing_app_mock._render_cost_analysis_tab = MagicMock()
        pricing_app_mock._render_pricing_scenarios_tab = MagicMock()
        pricing_app_mock._render_competitive_analysis_tab = MagicMock()
        pricing_app_mock._render_reports_tab = MagicMock()
        
        resources_app_mock = MagicMock()
        
        # ربط إطار التكامل مع التطبيقات الوهمية
        self.integration_framework.connect_pricing_app(pricing_app_mock)
        self.integration_framework.connect_resources_app(resources_app_mock)
        
        # التحقق من إضافة علامات التبويب الجديدة
        self.assertEqual(len(pricing_app_mock.tabs), 8)  # 5 علامات أصلية + 3 جديدة
        self.assertIn("كتالوجات الموارد", pricing_app_mock.tabs)
        self.assertIn("الإدارات المساندة", pricing_app_mock.tabs)
        self.assertIn("المحتوى المحلي", pricing_app_mock.tabs)
        
        # التحقق من إضافة الدوال الجديدة
        self.assertTrue(hasattr(pricing_app_mock, '_render_resource_catalogs_tab'))
        self.assertTrue(hasattr(pricing_app_mock, '_render_indirect_support_tab'))
        self.assertTrue(hasattr(pricing_app_mock, '_render_local_content_tab'))

if __name__ == '__main__':
    unittest.main()
