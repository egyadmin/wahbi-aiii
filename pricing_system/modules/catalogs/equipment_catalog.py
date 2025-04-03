"""
كتالوج المعدات - وحدة إدارة معدات المقاولات
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json
from datetime import datetime
import io

class EquipmentCatalog:
    """كتالوج المعدات"""
    
    def __init__(self):
        """تهيئة كتالوج المعدات"""
        
        # تهيئة حالة الجلسة لكتالوج المعدات
        if 'equipment_catalog' not in st.session_state:
            # إنشاء بيانات افتراضية للمعدات
            self._initialize_equipment_catalog()
    
    def _initialize_equipment_catalog(self):
        """تهيئة بيانات كتالوج المعدات"""
        
        # تعريف فئات المعدات
        equipment_categories = [
            "معدات الحفر والردم",
            "معدات النقل",
            "معدات الرفع",
            "معدات الخرسانة",
            "معدات الطرق",
            "معدات الصرف الصحي",
            "معدات السيول والكباري",
            "معدات الضغط والتثبيت",
            "معدات التوليد والطاقة",
            "معدات القياس والمساحة"
        ]
        
        # إنشاء قائمة المعدات
        equipment_data = []
        
        # 1. معدات الحفر والردم
        equipment_data.extend([
            {
                "id": "EQ-001",
                "name": "حفارة هيدروليكية كبيرة",
                "category": "معدات الحفر والردم",
                "subcategory": "حفارات",
                "brand": "كاتربيلر",
                "model": "CAT 336",
                "capacity": "2.5 م3",
                "production_rate": "150 م3/ساعة",
                "hourly_cost": 350,
                "daily_cost": 2800,
                "weekly_cost": 16800,
                "monthly_cost": 67200,
                "fuel_consumption": "35 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 5000,
                "operator_required": True,
                "description": "حفارة هيدروليكية كبيرة مناسبة لأعمال الحفر الثقيلة ومشاريع البنية التحتية الكبيرة",
                "image_url": "https://example.com/cat336.jpg"
            },
            {
                "id": "EQ-002",
                "name": "حفارة هيدروليكية متوسطة",
                "category": "معدات الحفر والردم",
                "subcategory": "حفارات",
                "brand": "كاتربيلر",
                "model": "CAT 320",
                "capacity": "1.5 م3",
                "production_rate": "100 م3/ساعة",
                "hourly_cost": 250,
                "daily_cost": 2000,
                "weekly_cost": 12000,
                "monthly_cost": 48000,
                "fuel_consumption": "25 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 3500,
                "operator_required": True,
                "description": "حفارة هيدروليكية متوسطة الحجم مناسبة لمعظم مشاريع البنية التحتية",
                "image_url": "https://example.com/cat320.jpg"
            },
            {
                "id": "EQ-003",
                "name": "حفارة هيدروليكية صغيرة",
                "category": "معدات الحفر والردم",
                "subcategory": "حفارات",
                "brand": "كاتربيلر",
                "model": "CAT 308",
                "capacity": "0.8 م3",
                "production_rate": "50 م3/ساعة",
                "hourly_cost": 150,
                "daily_cost": 1200,
                "weekly_cost": 7200,
                "monthly_cost": 28800,
                "fuel_consumption": "15 لتر/ساعة",
                "maintenance_period": "200 ساعة",
                "maintenance_cost": 2000,
                "operator_required": True,
                "description": "حفارة هيدروليكية صغيرة مناسبة للمشاريع الصغيرة والمساحات الضيقة",
                "image_url": "https://example.com/cat308.jpg"
            },
            {
                "id": "EQ-004",
                "name": "بلدوزر كبير",
                "category": "معدات الحفر والردم",
                "subcategory": "بلدوزرات",
                "brand": "كاتربيلر",
                "model": "D9",
                "capacity": "13.5 م3",
                "production_rate": "300 م3/ساعة",
                "hourly_cost": 400,
                "daily_cost": 3200,
                "weekly_cost": 19200,
                "monthly_cost": 76800,
                "fuel_consumption": "45 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 6000,
                "operator_required": True,
                "description": "بلدوزر كبير لأعمال التسوية والدفع في المشاريع الكبيرة",
                "image_url": "https://example.com/catd9.jpg"
            },
            {
                "id": "EQ-005",
                "name": "بلدوزر متوسط",
                "category": "معدات الحفر والردم",
                "subcategory": "بلدوزرات",
                "brand": "كاتربيلر",
                "model": "D7",
                "capacity": "8.5 م3",
                "production_rate": "200 م3/ساعة",
                "hourly_cost": 300,
                "daily_cost": 2400,
                "weekly_cost": 14400,
                "monthly_cost": 57600,
                "fuel_consumption": "35 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 4500,
                "operator_required": True,
                "description": "بلدوزر متوسط الحجم مناسب لمعظم مشاريع البنية التحتية",
                "image_url": "https://example.com/catd7.jpg"
            },
            {
                "id": "EQ-006",
                "name": "لودر أمامي كبير",
                "category": "معدات الحفر والردم",
                "subcategory": "لودرات",
                "brand": "كاتربيلر",
                "model": "980",
                "capacity": "5.5 م3",
                "production_rate": "250 م3/ساعة",
                "hourly_cost": 300,
                "daily_cost": 2400,
                "weekly_cost": 14400,
                "monthly_cost": 57600,
                "fuel_consumption": "30 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 4000,
                "operator_required": True,
                "description": "لودر أمامي كبير لأعمال التحميل في المشاريع الكبيرة",
                "image_url": "https://example.com/cat980.jpg"
            },
            {
                "id": "EQ-007",
                "name": "لودر أمامي متوسط",
                "category": "معدات الحفر والردم",
                "subcategory": "لودرات",
                "brand": "كاتربيلر",
                "model": "950",
                "capacity": "3.5 م3",
                "production_rate": "180 م3/ساعة",
                "hourly_cost": 250,
                "daily_cost": 2000,
                "weekly_cost": 12000,
                "monthly_cost": 48000,
                "fuel_consumption": "25 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 3500,
                "operator_required": True,
                "description": "لودر أمامي متوسط الحجم مناسب لمعظم مشاريع البنية التحتية",
                "image_url": "https://example.com/cat950.jpg"
            },
            {
                "id": "EQ-008",
                "name": "باكهو لودر",
                "category": "معدات الحفر والردم",
                "subcategory": "لودرات",
                "brand": "جي سي بي",
                "model": "3CX",
                "capacity": "1.0 م3",
                "production_rate": "60 م3/ساعة",
                "hourly_cost": 150,
                "daily_cost": 1200,
                "weekly_cost": 7200,
                "monthly_cost": 28800,
                "fuel_consumption": "12 لتر/ساعة",
                "maintenance_period": "200 ساعة",
                "maintenance_cost": 2000,
                "operator_required": True,
                "description": "باكهو لودر متعدد الاستخدامات للحفر والتحميل",
                "image_url": "https://example.com/jcb3cx.jpg"
            },
            {
                "id": "EQ-009",
                "name": "جريدر",
                "category": "معدات الحفر والردم",
                "subcategory": "معدات تسوية",
                "brand": "كاتربيلر",
                "model": "140",
                "capacity": "3.7 م عرض الشفرة",
                "production_rate": "2000 م2/ساعة",
                "hourly_cost": 250,
                "daily_cost": 2000,
                "weekly_cost": 12000,
                "monthly_cost": 48000,
                "fuel_consumption": "20 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 3000,
                "operator_required": True,
                "description": "جريدر لتسوية الطرق والمساحات",
                "image_url": "https://example.com/cat140.jpg"
            },
            {
                "id": "EQ-010",
                "name": "سكريبر",
                "category": "معدات الحفر والردم",
                "subcategory": "معدات تسوية",
                "brand": "كاتربيلر",
                "model": "621",
                "capacity": "21 م3",
                "production_rate": "400 م3/ساعة",
                "hourly_cost": 350,
                "daily_cost": 2800,
                "weekly_cost": 16800,
                "monthly_cost": 67200,
                "fuel_consumption": "35 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 5000,
                "operator_required": True,
                "description": "سكريبر لنقل وتسوية التربة لمسافات متوسطة",
                "image_url": "https://example.com/cat621.jpg"
            }
        ])
        
        # 2. معدات النقل
        equipment_data.extend([
            {
                "id": "EQ-011",
                "name": "شاحنة قلاب كبيرة",
                "category": "معدات النقل",
                "subcategory": "شاحنات قلاب",
                "brand": "مان",
                "model": "TGS 40.480",
                "capacity": "30 م3",
                "production_rate": "30 م3/رحلة",
                "hourly_cost": 200,
                "daily_cost": 1600,
                "weekly_cost": 9600,
                "monthly_cost": 38400,
                "fuel_consumption": "25 لتر/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 3000,
                "operator_required": True,
                "description": "شاحنة قلاب كبيرة لنقل مواد الحفر والردم",
                "image_url": "https://example.com/mantgs.jpg"
            },
            {
                "id": "EQ-012",
                "name": "شاحنة قلاب متوسطة",
                "category": "معدات النقل",
                "subcategory": "شاحنات قلاب",
                "brand": "مرسيدس",
                "model": "Actros 3341",
                "capacity": "20 م3",
                "production_rate": "20 م3/رحلة",
                "hourly_cost": 180,
                "daily_cost": 1440,
                "weekly_cost": 8640,
                "monthly_cost": 34560,
                "fuel_consumption": "20 لتر/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 2500,
                "operator_required": True,
                "description": "شاحنة قلاب متوسطة لنقل مواد الحفر والردم",
                "image_url": "https://example.com/actros.jpg"
            },
            {
                "id": "EQ-013",
                "name": "شاحنة خلاطة خرسانة",
                "category": "معدات النقل",
                "subcategory": "شاحنات خرسانة",
                "brand": "مرسيدس",
                "model": "Actros 3236",
                "capacity": "8 م3",
                "production_rate": "8 م3/رحلة",
                "hourly_cost": 200,
                "daily_cost": 1600,
                "weekly_cost": 9600,
                "monthly_cost": 38400,
                "fuel_consumption": "20 لتر/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 3000,
                "operator_required": True,
                "description": "شاحنة خلاطة خرسانة لنقل الخرسانة الجاهزة",
                "image_url": "https://example.com/mixer.jpg"
            },
            {
                "id": "EQ-014",
                "name": "شاحنة نقل مياه",
                "category": "معدات النقل",
                "subcategory": "شاحنات مياه",
                "brand": "مان",
                "model": "TGS 33.360",
                "capacity": "20000 لتر",
                "production_rate": "20000 لتر/رحلة",
                "hourly_cost": 150,
                "daily_cost": 1200,
                "weekly_cost": 7200,
                "monthly_cost": 28800,
                "fuel_consumption": "18 لتر/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 2000,
                "operator_required": True,
                "description": "شاحنة نقل مياه للمشاريع والرش",
                "image_url": "https://example.com/watertruck.jpg"
            },
            {
                "id": "EQ-015",
                "name": "شاحنة نقل معدات",
                "category": "معدات النقل",
                "subcategory": "شاحنات نقل",
                "brand": "فولفو",
                "model": "FH16",
                "capacity": "60 طن",
                "production_rate": "60 طن/رحلة",
                "hourly_cost": 250,
                "daily_cost": 2000,
                "weekly_cost": 12000,
                "monthly_cost": 48000,
                "fuel_consumption": "25 لتر/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 3500,
                "operator_required": True,
                "description": "شاحنة نقل معدات ثقيلة (لوبد)",
                "image_url": "https://example.com/lowbed.jpg"
            }
        ])
        
        # 3. معدات الرفع
        equipment_data.extend([
            {
                "id": "EQ-016",
                "name": "رافعة برجية",
                "category": "معدات الرفع",
                "subcategory": "رافعات برجية",
                "brand": "ليبهر",
                "model": "200 EC-H",
                "capacity": "10 طن",
                "production_rate": "20 رفعة/ساعة",
                "hourly_cost": 400,
                "daily_cost": 3200,
                "weekly_cost": 19200,
                "monthly_cost": 76800,
                "fuel_consumption": "30 كيلوواط/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 5000,
                "operator_required": True,
                "description": "رافعة برجية للمشاريع الإنشائية الكبيرة",
                "image_url": "https://example.com/towercrane.jpg"
            },
            {
                "id": "EQ-017",
                "name": "رافعة متحركة كبيرة",
                "category": "معدات الرفع",
                "subcategory": "رافعات متحركة",
                "brand": "ليبهر",
                "model": "LTM 1200",
                "capacity": "200 طن",
                "production_rate": "15 رفعة/ساعة",
                "hourly_cost": 600,
                "daily_cost": 4800,
                "weekly_cost": 28800,
                "monthly_cost": 115200,
                "fuel_consumption": "40 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 8000,
                "operator_required": True,
                "description": "رافعة متحركة كبيرة للأحمال الثقيلة",
                "image_url": "https://example.com/mobilecrane.jpg"
            },
            {
                "id": "EQ-018",
                "name": "رافعة متحركة متوسطة",
                "category": "معدات الرفع",
                "subcategory": "رافعات متحركة",
                "brand": "ليبهر",
                "model": "LTM 1070",
                "capacity": "70 طن",
                "production_rate": "15 رفعة/ساعة",
                "hourly_cost": 400,
                "daily_cost": 3200,
                "weekly_cost": 19200,
                "monthly_cost": 76800,
                "fuel_consumption": "30 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 6000,
                "operator_required": True,
                "description": "رافعة متحركة متوسطة للاستخدامات المتنوعة",
                "image_url": "https://example.com/mobilecrane2.jpg"
            },
            {
                "id": "EQ-019",
                "name": "رافعة شوكية",
                "category": "معدات الرفع",
                "subcategory": "رافعات شوكية",
                "brand": "كاتربيلر",
                "model": "DP70N",
                "capacity": "7 طن",
                "production_rate": "30 رفعة/ساعة",
                "hourly_cost": 150,
                "daily_cost": 1200,
                "weekly_cost": 7200,
                "monthly_cost": 28800,
                "fuel_consumption": "12 لتر/ساعة",
                "maintenance_period": "200 ساعة",
                "maintenance_cost": 2000,
                "operator_required": True,
                "description": "رافعة شوكية لنقل المواد في الموقع",
                "image_url": "https://example.com/forklift.jpg"
            },
            {
                "id": "EQ-020",
                "name": "رافعة سلة",
                "category": "معدات الرفع",
                "subcategory": "رافعات سلة",
                "brand": "جيني",
                "model": "S-85",
                "capacity": "227 كجم",
                "production_rate": "ارتفاع 26 متر",
                "hourly_cost": 200,
                "daily_cost": 1600,
                "weekly_cost": 9600,
                "monthly_cost": 38400,
                "fuel_consumption": "10 لتر/ساعة",
                "maintenance_period": "200 ساعة",
                "maintenance_cost": 2500,
                "operator_required": True,
                "description": "رافعة سلة للوصول إلى الارتفاعات",
                "image_url": "https://example.com/boomlift.jpg"
            }
        ])
        
        # 4. معدات الخرسانة
        equipment_data.extend([
            {
                "id": "EQ-021",
                "name": "خلاطة خرسانة مركزية",
                "category": "معدات الخرسانة",
                "subcategory": "خلاطات",
                "brand": "ليبهر",
                "model": "Betomix 3.0",
                "capacity": "120 م3/ساعة",
                "production_rate": "120 م3/ساعة",
                "hourly_cost": 800,
                "daily_cost": 6400,
                "weekly_cost": 38400,
                "monthly_cost": 153600,
                "fuel_consumption": "60 كيلوواط/ساعة",
                "maintenance_period": "500 ساعة",
                "maintenance_cost": 10000,
                "operator_required": True,
                "description": "محطة خلط خرسانة مركزية للمشاريع الكبيرة",
                "image_url": "https://example.com/batchplant.jpg"
            },
            {
                "id": "EQ-022",
                "name": "خلاطة خرسانة متنقلة",
                "category": "معدات الخرسانة",
                "subcategory": "خلاطات",
                "brand": "كارمكس",
                "model": "MCP-30",
                "capacity": "30 م3/ساعة",
                "production_rate": "30 م3/ساعة",
                "hourly_cost": 300,
                "daily_cost": 2400,
                "weekly_cost": 14400,
                "monthly_cost": 57600,
                "fuel_consumption": "25 كيلوواط/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 5000,
                "operator_required": True,
                "description": "محطة خلط خرسانة متنقلة للمشاريع المتوسطة",
                "image_url": "https://example.com/mobilemixer.jpg"
            },
            {
                "id": "EQ-023",
                "name": "مضخة خرسانة ثابتة",
                "category": "معدات الخرسانة",
                "subcategory": "مضخات",
                "brand": "بوتزميستر",
                "model": "BSA 1409",
                "capacity": "90 م3/ساعة",
                "production_rate": "90 م3/ساعة",
                "hourly_cost": 350,
                "daily_cost": 2800,
                "weekly_cost": 16800,
                "monthly_cost": 67200,
                "fuel_consumption": "30 كيلوواط/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 6000,
                "operator_required": True,
                "description": "مضخة خرسانة ثابتة للمشاريع الكبيرة",
                "image_url": "https://example.com/concretepump.jpg"
            },
            {
                "id": "EQ-024",
                "name": "مضخة خرسانة متحركة",
                "category": "معدات الخرسانة",
                "subcategory": "مضخات",
                "brand": "بوتزميستر",
                "model": "M42-5",
                "capacity": "160 م3/ساعة",
                "production_rate": "160 م3/ساعة",
                "hourly_cost": 500,
                "daily_cost": 4000,
                "weekly_cost": 24000,
                "monthly_cost": 96000,
                "fuel_consumption": "40 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 8000,
                "operator_required": True,
                "description": "مضخة خرسانة متحركة بذراع 42 متر",
                "image_url": "https://example.com/boomconcretepump.jpg"
            },
            {
                "id": "EQ-025",
                "name": "هزاز خرسانة",
                "category": "معدات الخرسانة",
                "subcategory": "هزازات",
                "brand": "واكر نيوسن",
                "model": "IREN",
                "capacity": "غير محدد",
                "production_rate": "غير محدد",
                "hourly_cost": 20,
                "daily_cost": 160,
                "weekly_cost": 960,
                "monthly_cost": 3840,
                "fuel_consumption": "غير محدد",
                "maintenance_period": "100 ساعة",
                "maintenance_cost": 500,
                "operator_required": True,
                "description": "هزاز خرسانة لدمك الخرسانة",
                "image_url": "https://example.com/vibrator.jpg"
            },
            {
                "id": "EQ-026",
                "name": "ماكينة تسوية الخرسانة",
                "category": "معدات الخرسانة",
                "subcategory": "معدات تشطيب",
                "brand": "سومرو",
                "model": "S-840",
                "capacity": "840 م2/ساعة",
                "production_rate": "840 م2/ساعة",
                "hourly_cost": 100,
                "daily_cost": 800,
                "weekly_cost": 4800,
                "monthly_cost": 19200,
                "fuel_consumption": "5 لتر/ساعة",
                "maintenance_period": "150 ساعة",
                "maintenance_cost": 1500,
                "operator_required": True,
                "description": "ماكينة تسوية الخرسانة (هليكوبتر)",
                "image_url": "https://example.com/powertrowel.jpg"
            }
        ])
        
        # 5. معدات الطرق
        equipment_data.extend([
            {
                "id": "EQ-027",
                "name": "فرادة أسفلت كبيرة",
                "category": "معدات الطرق",
                "subcategory": "فرادات",
                "brand": "فوجيلي",
                "model": "Super 2100-3i",
                "capacity": "1100 طن/ساعة",
                "production_rate": "1100 طن/ساعة",
                "hourly_cost": 600,
                "daily_cost": 4800,
                "weekly_cost": 28800,
                "monthly_cost": 115200,
                "fuel_consumption": "45 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 8000,
                "operator_required": True,
                "description": "فرادة أسفلت كبيرة للطرق السريعة",
                "image_url": "https://example.com/paver.jpg"
            },
            {
                "id": "EQ-028",
                "name": "فرادة أسفلت متوسطة",
                "category": "معدات الطرق",
                "subcategory": "فرادات",
                "brand": "فوجيلي",
                "model": "Super 1800-3i",
                "capacity": "700 طن/ساعة",
                "production_rate": "700 طن/ساعة",
                "hourly_cost": 450,
                "daily_cost": 3600,
                "weekly_cost": 21600,
                "monthly_cost": 86400,
                "fuel_consumption": "35 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 6000,
                "operator_required": True,
                "description": "فرادة أسفلت متوسطة للطرق العامة",
                "image_url": "https://example.com/paver2.jpg"
            },
            {
                "id": "EQ-029",
                "name": "مدحلة أسفلت ثقيلة",
                "category": "معدات الطرق",
                "subcategory": "مداحل",
                "brand": "بوماج",
                "model": "BW 203",
                "capacity": "غير محدد",
                "production_rate": "3000 م2/ساعة",
                "hourly_cost": 250,
                "daily_cost": 2000,
                "weekly_cost": 12000,
                "monthly_cost": 48000,
                "fuel_consumption": "20 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 3500,
                "operator_required": True,
                "description": "مدحلة أسفلت ثقيلة للطرق",
                "image_url": "https://example.com/roller.jpg"
            },
            {
                "id": "EQ-030",
                "name": "مدحلة أسفلت مطاطية",
                "category": "معدات الطرق",
                "subcategory": "مداحل",
                "brand": "بوماج",
                "model": "BW 27 RH",
                "capacity": "غير محدد",
                "production_rate": "3500 م2/ساعة",
                "hourly_cost": 200,
                "daily_cost": 1600,
                "weekly_cost": 9600,
                "monthly_cost": 38400,
                "fuel_consumption": "18 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 3000,
                "operator_required": True,
                "description": "مدحلة أسفلت مطاطية للطرق",
                "image_url": "https://example.com/rubberroller.jpg"
            },
            {
                "id": "EQ-031",
                "name": "قاشطة أسفلت",
                "category": "معدات الطرق",
                "subcategory": "قاشطات",
                "brand": "ويرتجن",
                "model": "W 210",
                "capacity": "غير محدد",
                "production_rate": "800 م2/ساعة",
                "hourly_cost": 500,
                "daily_cost": 4000,
                "weekly_cost": 24000,
                "monthly_cost": 96000,
                "fuel_consumption": "40 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 7000,
                "operator_required": True,
                "description": "قاشطة أسفلت لإزالة طبقات الأسفلت القديمة",
                "image_url": "https://example.com/milling.jpg"
            },
            {
                "id": "EQ-032",
                "name": "شاحنة رش البيتومين",
                "category": "معدات الطرق",
                "subcategory": "معدات رش",
                "brand": "روزنباور",
                "model": "S12000",
                "capacity": "12000 لتر",
                "production_rate": "15000 م2/ساعة",
                "hourly_cost": 200,
                "daily_cost": 1600,
                "weekly_cost": 9600,
                "monthly_cost": 38400,
                "fuel_consumption": "15 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 3000,
                "operator_required": True,
                "description": "شاحنة رش البيتومين للطرق",
                "image_url": "https://example.com/bitumensprayer.jpg"
            }
        ])
        
        # 6. معدات الصرف الصحي
        equipment_data.extend([
            {
                "id": "EQ-033",
                "name": "حفارة خنادق كبيرة",
                "category": "معدات الصرف الصحي",
                "subcategory": "حفارات خنادق",
                "brand": "فيرمير",
                "model": "T1255III",
                "capacity": "غير محدد",
                "production_rate": "300 م/ساعة",
                "hourly_cost": 400,
                "daily_cost": 3200,
                "weekly_cost": 19200,
                "monthly_cost": 76800,
                "fuel_consumption": "35 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 6000,
                "operator_required": True,
                "description": "حفارة خنادق كبيرة لمشاريع الصرف الصحي",
                "image_url": "https://example.com/trencher.jpg"
            },
            {
                "id": "EQ-034",
                "name": "ماكينة دفع أنابيب",
                "category": "معدات الصرف الصحي",
                "subcategory": "معدات دفع",
                "brand": "هيرينكنيشت",
                "model": "HK-500",
                "capacity": "غير محدد",
                "production_rate": "20 م/ساعة",
                "hourly_cost": 600,
                "daily_cost": 4800,
                "weekly_cost": 28800,
                "monthly_cost": 115200,
                "fuel_consumption": "40 كيلوواط/ساعة",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 8000,
                "operator_required": True,
                "description": "ماكينة دفع أنابيب بدون حفر مفتوح",
                "image_url": "https://example.com/pipejacking.jpg"
            },
            {
                "id": "EQ-035",
                "name": "سيارة شفط وتنظيف مجاري",
                "category": "معدات الصرف الصحي",
                "subcategory": "معدات تنظيف",
                "brand": "كايزر",
                "model": "AquaStar",
                "capacity": "12000 لتر",
                "production_rate": "غير محدد",
                "hourly_cost": 300,
                "daily_cost": 2400,
                "weekly_cost": 14400,
                "monthly_cost": 57600,
                "fuel_consumption": "20 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 4000,
                "operator_required": True,
                "description": "سيارة شفط وتنظيف مجاري بضغط عالي",
                "image_url": "https://example.com/sewercleaner.jpg"
            },
            {
                "id": "EQ-036",
                "name": "كاميرا فحص مجاري",
                "category": "معدات الصرف الصحي",
                "subcategory": "معدات فحص",
                "brand": "إيبوس",
                "model": "ROVION",
                "capacity": "غير محدد",
                "production_rate": "غير محدد",
                "hourly_cost": 150,
                "daily_cost": 1200,
                "weekly_cost": 7200,
                "monthly_cost": 28800,
                "fuel_consumption": "غير محدد",
                "maintenance_period": "200 ساعة",
                "maintenance_cost": 2000,
                "operator_required": True,
                "description": "كاميرا فحص مجاري للتفتيش والصيانة",
                "image_url": "https://example.com/sewercamera.jpg"
            },
            {
                "id": "EQ-037",
                "name": "مضخة مياه غاطسة كبيرة",
                "category": "معدات الصرف الصحي",
                "subcategory": "مضخات",
                "brand": "جرندفوس",
                "model": "S2",
                "capacity": "400 م3/ساعة",
                "production_rate": "400 م3/ساعة",
                "hourly_cost": 100,
                "daily_cost": 800,
                "weekly_cost": 4800,
                "monthly_cost": 19200,
                "fuel_consumption": "15 كيلوواط/ساعة",
                "maintenance_period": "500 ساعة",
                "maintenance_cost": 2500,
                "operator_required": False,
                "description": "مضخة مياه غاطسة كبيرة لمشاريع الصرف الصحي",
                "image_url": "https://example.com/submersiblepump.jpg"
            }
        ])
        
        # 7. معدات السيول والكباري
        equipment_data.extend([
            {
                "id": "EQ-038",
                "name": "معدات دق الخوازيق",
                "category": "معدات السيول والكباري",
                "subcategory": "معدات خوازيق",
                "brand": "بوير",
                "model": "BG 28",
                "capacity": "غير محدد",
                "production_rate": "10 خازوق/يوم",
                "hourly_cost": 800,
                "daily_cost": 6400,
                "weekly_cost": 38400,
                "monthly_cost": 153600,
                "fuel_consumption": "60 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 10000,
                "operator_required": True,
                "description": "معدات دق الخوازيق للكباري والأساسات العميقة",
                "image_url": "https://example.com/piling.jpg"
            },
            {
                "id": "EQ-039",
                "name": "رافعة جسرية",
                "category": "معدات السيول والكباري",
                "subcategory": "رافعات",
                "brand": "ليبهر",
                "model": "LG 1750",
                "capacity": "750 طن",
                "production_rate": "غير محدد",
                "hourly_cost": 1200,
                "daily_cost": 9600,
                "weekly_cost": 57600,
                "monthly_cost": 230400,
                "fuel_consumption": "80 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 15000,
                "operator_required": True,
                "description": "رافعة جسرية لتركيب عناصر الكباري الثقيلة",
                "image_url": "https://example.com/bridgecrane.jpg"
            },
            {
                "id": "EQ-040",
                "name": "معدات شد الكابلات",
                "category": "معدات السيول والكباري",
                "subcategory": "معدات شد",
                "brand": "فرايسينت",
                "model": "C500",
                "capacity": "500 طن",
                "production_rate": "غير محدد",
                "hourly_cost": 300,
                "daily_cost": 2400,
                "weekly_cost": 14400,
                "monthly_cost": 57600,
                "fuel_consumption": "غير محدد",
                "maintenance_period": "300 ساعة",
                "maintenance_cost": 5000,
                "operator_required": True,
                "description": "معدات شد الكابلات للكباري المعلقة",
                "image_url": "https://example.com/stressing.jpg"
            },
            {
                "id": "EQ-041",
                "name": "معدات حفر الأنفاق",
                "category": "معدات السيول والكباري",
                "subcategory": "معدات أنفاق",
                "brand": "هيرينكنيشت",
                "model": "S-500",
                "capacity": "غير محدد",
                "production_rate": "15 م/يوم",
                "hourly_cost": 1500,
                "daily_cost": 12000,
                "weekly_cost": 72000,
                "monthly_cost": 288000,
                "fuel_consumption": "100 كيلوواط/ساعة",
                "maintenance_period": "500 ساعة",
                "maintenance_cost": 20000,
                "operator_required": True,
                "description": "معدات حفر الأنفاق للمشاريع الكبيرة",
                "image_url": "https://example.com/tbm.jpg"
            },
            {
                "id": "EQ-042",
                "name": "سدود مؤقتة",
                "category": "معدات السيول والكباري",
                "subcategory": "معدات سيول",
                "brand": "أكواباريير",
                "model": "K-100",
                "capacity": "غير محدد",
                "production_rate": "100 م/يوم",
                "hourly_cost": 200,
                "daily_cost": 1600,
                "weekly_cost": 9600,
                "monthly_cost": 38400,
                "fuel_consumption": "غير محدد",
                "maintenance_period": "غير محدد",
                "maintenance_cost": 2000,
                "operator_required": True,
                "description": "سدود مؤقتة للحماية من السيول",
                "image_url": "https://example.com/cofferdam.jpg"
            }
        ])
        
        # 8. معدات الضغط والتثبيت
        equipment_data.extend([
            {
                "id": "EQ-043",
                "name": "مدحلة تربة ثقيلة",
                "category": "معدات الضغط والتثبيت",
                "subcategory": "مداحل",
                "brand": "بوماج",
                "model": "BW 226",
                "capacity": "غير محدد",
                "production_rate": "3000 م2/ساعة",
                "hourly_cost": 250,
                "daily_cost": 2000,
                "weekly_cost": 12000,
                "monthly_cost": 48000,
                "fuel_consumption": "20 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 3500,
                "operator_required": True,
                "description": "مدحلة تربة ثقيلة للمشاريع الكبيرة",
                "image_url": "https://example.com/soilroller.jpg"
            },
            {
                "id": "EQ-044",
                "name": "دكاكة قفازة",
                "category": "معدات الضغط والتثبيت",
                "subcategory": "دكاكات",
                "brand": "واكر نيوسن",
                "model": "BS 60-4",
                "capacity": "غير محدد",
                "production_rate": "150 م2/ساعة",
                "hourly_cost": 50,
                "daily_cost": 400,
                "weekly_cost": 2400,
                "monthly_cost": 9600,
                "fuel_consumption": "2 لتر/ساعة",
                "maintenance_period": "100 ساعة",
                "maintenance_cost": 800,
                "operator_required": True,
                "description": "دكاكة قفازة للمساحات الضيقة",
                "image_url": "https://example.com/rammer.jpg"
            },
            {
                "id": "EQ-045",
                "name": "دكاكة هزازة",
                "category": "معدات الضغط والتثبيت",
                "subcategory": "دكاكات",
                "brand": "واكر نيوسن",
                "model": "DPU 6555",
                "capacity": "غير محدد",
                "production_rate": "500 م2/ساعة",
                "hourly_cost": 80,
                "daily_cost": 640,
                "weekly_cost": 3840,
                "monthly_cost": 15360,
                "fuel_consumption": "3 لتر/ساعة",
                "maintenance_period": "100 ساعة",
                "maintenance_cost": 1000,
                "operator_required": True,
                "description": "دكاكة هزازة للمساحات المتوسطة",
                "image_url": "https://example.com/platecompactor.jpg"
            },
            {
                "id": "EQ-046",
                "name": "معدات تثبيت التربة",
                "category": "معدات الضغط والتثبيت",
                "subcategory": "معدات تثبيت",
                "brand": "ويرتجن",
                "model": "WR 250",
                "capacity": "غير محدد",
                "production_rate": "5000 م2/يوم",
                "hourly_cost": 500,
                "daily_cost": 4000,
                "weekly_cost": 24000,
                "monthly_cost": 96000,
                "fuel_consumption": "40 لتر/ساعة",
                "maintenance_period": "250 ساعة",
                "maintenance_cost": 7000,
                "operator_required": True,
                "description": "معدات تثبيت التربة بالإسمنت أو الجير",
                "image_url": "https://example.com/soilstabilizer.jpg"
            }
        ])
        
        # 9. معدات التوليد والطاقة
        equipment_data.extend([
            {
                "id": "EQ-047",
                "name": "مولد كهرباء كبير",
                "category": "معدات التوليد والطاقة",
                "subcategory": "مولدات",
                "brand": "كاتربيلر",
                "model": "C15",
                "capacity": "500 كيلوواط",
                "production_rate": "500 كيلوواط",
                "hourly_cost": 300,
                "daily_cost": 2400,
                "weekly_cost": 14400,
                "monthly_cost": 57600,
                "fuel_consumption": "80 لتر/ساعة",
                "maintenance_period": "500 ساعة",
                "maintenance_cost": 5000,
                "operator_required": False,
                "description": "مولد كهرباء كبير للمشاريع الكبيرة",
                "image_url": "https://example.com/generator.jpg"
            },
            {
                "id": "EQ-048",
                "name": "مولد كهرباء متوسط",
                "category": "معدات التوليد والطاقة",
                "subcategory": "مولدات",
                "brand": "كاتربيلر",
                "model": "C9",
                "capacity": "250 كيلوواط",
                "production_rate": "250 كيلوواط",
                "hourly_cost": 200,
                "daily_cost": 1600,
                "weekly_cost": 9600,
                "monthly_cost": 38400,
                "fuel_consumption": "45 لتر/ساعة",
                "maintenance_period": "500 ساعة",
                "maintenance_cost": 3500,
                "operator_required": False,
                "description": "مولد كهرباء متوسط للمشاريع المتوسطة",
                "image_url": "https://example.com/generator2.jpg"
            },
            {
                "id": "EQ-049",
                "name": "ضاغط هواء كبير",
                "category": "معدات التوليد والطاقة",
                "subcategory": "ضواغط",
                "brand": "أطلس كوبكو",
                "model": "XRVS 1000",
                "capacity": "1000 قدم مكعب/دقيقة",
                "production_rate": "1000 قدم مكعب/دقيقة",
                "hourly_cost": 200,
                "daily_cost": 1600,
                "weekly_cost": 9600,
                "monthly_cost": 38400,
                "fuel_consumption": "30 لتر/ساعة",
                "maintenance_period": "500 ساعة",
                "maintenance_cost": 3000,
                "operator_required": False,
                "description": "ضاغط هواء كبير للمشاريع الكبيرة",
                "image_url": "https://example.com/compressor.jpg"
            },
            {
                "id": "EQ-050",
                "name": "ضاغط هواء متوسط",
                "category": "معدات التوليد والطاقة",
                "subcategory": "ضواغط",
                "brand": "أطلس كوبكو",
                "model": "XRVS 500",
                "capacity": "500 قدم مكعب/دقيقة",
                "production_rate": "500 قدم مكعب/دقيقة",
                "hourly_cost": 150,
                "daily_cost": 1200,
                "weekly_cost": 7200,
                "monthly_cost": 28800,
                "fuel_consumption": "20 لتر/ساعة",
                "maintenance_period": "500 ساعة",
                "maintenance_cost": 2500,
                "operator_required": False,
                "description": "ضاغط هواء متوسط للمشاريع المتوسطة",
                "image_url": "https://example.com/compressor2.jpg"
            }
        ])
        
        # 10. معدات القياس والمساحة
        equipment_data.extend([
            {
                "id": "EQ-051",
                "name": "محطة رصد متكاملة",
                "category": "معدات القياس والمساحة",
                "subcategory": "محطات رصد",
                "brand": "ليكا",
                "model": "TS16",
                "capacity": "غير محدد",
                "production_rate": "غير محدد",
                "hourly_cost": 100,
                "daily_cost": 800,
                "weekly_cost": 4800,
                "monthly_cost": 19200,
                "fuel_consumption": "غير محدد",
                "maintenance_period": "1000 ساعة",
                "maintenance_cost": 2000,
                "operator_required": True,
                "description": "محطة رصد متكاملة للمساحة الدقيقة",
                "image_url": "https://example.com/totalstation.jpg"
            },
            {
                "id": "EQ-052",
                "name": "جهاز GPS مساحي",
                "category": "معدات القياس والمساحة",
                "subcategory": "أجهزة GPS",
                "brand": "ترمبل",
                "model": "R10",
                "capacity": "غير محدد",
                "production_rate": "غير محدد",
                "hourly_cost": 80,
                "daily_cost": 640,
                "weekly_cost": 3840,
                "monthly_cost": 15360,
                "fuel_consumption": "غير محدد",
                "maintenance_period": "1000 ساعة",
                "maintenance_cost": 1500,
                "operator_required": True,
                "description": "جهاز GPS مساحي دقيق",
                "image_url": "https://example.com/gps.jpg"
            },
            {
                "id": "EQ-053",
                "name": "جهاز مسح ليزري ثلاثي الأبعاد",
                "category": "معدات القياس والمساحة",
                "subcategory": "أجهزة مسح",
                "brand": "ليكا",
                "model": "RTC360",
                "capacity": "غير محدد",
                "production_rate": "غير محدد",
                "hourly_cost": 150,
                "daily_cost": 1200,
                "weekly_cost": 7200,
                "monthly_cost": 28800,
                "fuel_consumption": "غير محدد",
                "maintenance_period": "1000 ساعة",
                "maintenance_cost": 3000,
                "operator_required": True,
                "description": "جهاز مسح ليزري ثلاثي الأبعاد للمشاريع المعقدة",
                "image_url": "https://example.com/laserscanner.jpg"
            },
            {
                "id": "EQ-054",
                "name": "طائرة بدون طيار للمسح",
                "category": "معدات القياس والمساحة",
                "subcategory": "طائرات مسح",
                "brand": "دي جي آي",
                "model": "Phantom 4 RTK",
                "capacity": "غير محدد",
                "production_rate": "غير محدد",
                "hourly_cost": 100,
                "daily_cost": 800,
                "weekly_cost": 4800,
                "monthly_cost": 19200,
                "fuel_consumption": "غير محدد",
                "maintenance_period": "500 ساعة",
                "maintenance_cost": 1000,
                "operator_required": True,
                "description": "طائرة بدون طيار للمسح الجوي والتصوير",
                "image_url": "https://example.com/drone.jpg"
            }
        ])
        
        # تخزين البيانات في حالة الجلسة
        st.session_state.equipment_catalog = pd.DataFrame(equipment_data)
    
    def render(self):
        """عرض واجهة كتالوج المعدات"""
        
        st.markdown("## كتالوج المعدات")
        
        # إنشاء تبويبات لعرض الكتالوج
        tabs = st.tabs([
            "عرض الكتالوج", 
            "إضافة معدة", 
            "تحليل التكاليف",
            "استيراد/تصدير"
        ])
        
        with tabs[0]:
            self._render_catalog_view_tab()
        
        with tabs[1]:
            self._render_add_equipment_tab()
        
        with tabs[2]:
            self._render_cost_analysis_tab()
        
        with tabs[3]:
            self._render_import_export_tab()
    
    def _render_catalog_view_tab(self):
        """عرض تبويب عرض الكتالوج"""
        
        st.markdown("### عرض كتالوج المعدات")
        
        # استخراج البيانات
        equipment_df = st.session_state.equipment_catalog
        
        # إنشاء فلاتر للعرض
        col1, col2 = st.columns(2)
        
        with col1:
            # فلتر حسب الفئة
            categories = ["الكل"] + sorted(equipment_df["category"].unique().tolist())
            selected_category = st.selectbox("اختر فئة المعدات", categories)
        
        with col2:
            # فلتر حسب الفئة الفرعية
            if selected_category != "الكل":
                subcategories = ["الكل"] + sorted(equipment_df[equipment_df["category"] == selected_category]["subcategory"].unique().tolist())
            else:
                subcategories = ["الكل"] + sorted(equipment_df["subcategory"].unique().tolist())
            
            selected_subcategory = st.selectbox("اختر الفئة الفرعية", subcategories)
        
        # تطبيق الفلاتر
        filtered_df = equipment_df.copy()
        
        if selected_category != "الكل":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]
        
        if selected_subcategory != "الكل":
            filtered_df = filtered_df[filtered_df["subcategory"] == selected_subcategory]
        
        # عرض البيانات
        if not filtered_df.empty:
            # عرض عدد النتائج
            st.info(f"تم العثور على {len(filtered_df)} معدة")
            
            # عرض المعدات في شكل بطاقات
            for i, (_, equipment) in enumerate(filtered_df.iterrows()):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # عرض صورة المعدة (استخدام صورة افتراضية)
                    st.image("https://via.placeholder.com/150", caption=equipment["name"])
                
                with col2:
                    # عرض معلومات المعدة
                    st.markdown(f"**{equipment['name']}** (الكود: {equipment['id']})")
                    st.markdown(f"الفئة: {equipment['category']} - {equipment['subcategory']}")
                    st.markdown(f"الماركة: {equipment['brand']} | الموديل: {equipment['model']}")
                    st.markdown(f"السعة: {equipment['capacity']} | معدل الإنتاج: {equipment['production_rate']}")
                    
                    # عرض التكاليف
                    cost_col1, cost_col2, cost_col3, cost_col4 = st.columns(4)
                    with cost_col1:
                        st.metric("بالساعة", f"{equipment['hourly_cost']} ريال")
                    with cost_col2:
                        st.metric("باليوم", f"{equipment['daily_cost']} ريال")
                    with cost_col3:
                        st.metric("بالأسبوع", f"{equipment['weekly_cost']} ريال")
                    with cost_col4:
                        st.metric("بالشهر", f"{equipment['monthly_cost']} ريال")
                
                # إضافة زر لعرض التفاصيل
                if st.button(f"عرض التفاصيل الكاملة", key=f"details_{equipment['id']}"):
                    st.session_state.selected_equipment = equipment['id']
                    self._show_equipment_details(equipment)
                
                st.markdown("---")
        else:
            st.warning("لا توجد معدات تطابق معايير البحث")
    
    def _show_equipment_details(self, equipment):
        """عرض تفاصيل المعدة"""
        
        st.markdown(f"## تفاصيل المعدة: {equipment['name']}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # عرض صورة المعدة (استخدام صورة افتراضية)
            st.image("https://via.placeholder.com/300", caption=equipment["name"])
        
        with col2:
            # عرض المعلومات الأساسية
            st.markdown("### المعلومات الأساسية")
            st.markdown(f"**الكود:** {equipment['id']}")
            st.markdown(f"**الفئة:** {equipment['category']} - {equipment['subcategory']}")
            st.markdown(f"**الماركة:** {equipment['brand']}")
            st.markdown(f"**الموديل:** {equipment['model']}")
            st.markdown(f"**السعة:** {equipment['capacity']}")
            st.markdown(f"**معدل الإنتاج:** {equipment['production_rate']}")
            st.markdown(f"**الوصف:** {equipment['description']}")
        
        # عرض معلومات التكلفة
        st.markdown("### معلومات التكلفة")
        cost_col1, cost_col2, cost_col3, cost_col4 = st.columns(4)
        with cost_col1:
            st.metric("التكلفة بالساعة", f"{equipment['hourly_cost']} ريال")
        with cost_col2:
            st.metric("التكلفة باليوم", f"{equipment['daily_cost']} ريال")
        with cost_col3:
            st.metric("التكلفة بالأسبوع", f"{equipment['weekly_cost']} ريال")
        with cost_col4:
            st.metric("التكلفة بالشهر", f"{equipment['monthly_cost']} ريال")
        
        # عرض معلومات التشغيل والصيانة
        st.markdown("### معلومات التشغيل والصيانة")
        maint_col1, maint_col2, maint_col3 = st.columns(3)
        with maint_col1:
            st.metric("استهلاك الوقود", f"{equipment['fuel_consumption']}")
        with maint_col2:
            st.metric("فترة الصيانة", f"{equipment['maintenance_period']}")
        with maint_col3:
            st.metric("تكلفة الصيانة", f"{equipment['maintenance_cost']} ريال")
        
        st.markdown(f"**يتطلب مشغل:** {'نعم' if equipment['operator_required'] else 'لا'}")
        
        # إضافة زر للتعديل
        if st.button("تعديل بيانات المعدة"):
            st.session_state.edit_equipment = equipment['id']
            # هنا يمكن إضافة منطق التعديل
    
    def _render_add_equipment_tab(self):
        """عرض تبويب إضافة معدة"""
        
        st.markdown("### إضافة معدة جديدة")
        
        # استخراج البيانات
        equipment_df = st.session_state.equipment_catalog
        
        # إنشاء نموذج إضافة معدة
        with st.form("add_equipment_form"):
            st.markdown("#### المعلومات الأساسية")
            
            # الصف الأول
            col1, col2 = st.columns(2)
            with col1:
                equipment_id = st.text_input("كود المعدة", value=f"EQ-{len(equipment_df) + 1:03d}")
                equipment_name = st.text_input("اسم المعدة", placeholder="مثال: حفارة هيدروليكية متوسطة")
            
            with col2:
                # استخراج الفئات والفئات الفرعية الموجودة
                categories = sorted(equipment_df["category"].unique().tolist())
                equipment_category = st.selectbox("فئة المعدة", categories)
                
                # استخراج الفئات الفرعية بناءً على الفئة المختارة
                subcategories = sorted(equipment_df[equipment_df["category"] == equipment_category]["subcategory"].unique().tolist())
                equipment_subcategory = st.selectbox("الفئة الفرعية", subcategories)
            
            # الصف الثاني
            col1, col2 = st.columns(2)
            with col1:
                equipment_brand = st.text_input("الماركة", placeholder="مثال: كاتربيلر")
                equipment_model = st.text_input("الموديل", placeholder="مثال: CAT 320")
            
            with col2:
                equipment_capacity = st.text_input("السعة", placeholder="مثال: 1.5 م3")
                equipment_production_rate = st.text_input("معدل الإنتاج", placeholder="مثال: 100 م3/ساعة")
            
            st.markdown("#### معلومات التكلفة")
            
            # الصف الثالث
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                equipment_hourly_cost = st.number_input("التكلفة بالساعة (ريال)", min_value=0, step=10)
            with col2:
                equipment_daily_cost = st.number_input("التكلفة باليوم (ريال)", min_value=0, step=100)
            with col3:
                equipment_weekly_cost = st.number_input("التكلفة بالأسبوع (ريال)", min_value=0, step=500)
            with col4:
                equipment_monthly_cost = st.number_input("التكلفة بالشهر (ريال)", min_value=0, step=1000)
            
            st.markdown("#### معلومات التشغيل والصيانة")
            
            # الصف الرابع
            col1, col2, col3 = st.columns(3)
            with col1:
                equipment_fuel_consumption = st.text_input("استهلاك الوقود", placeholder="مثال: 25 لتر/ساعة")
            with col2:
                equipment_maintenance_period = st.text_input("فترة الصيانة", placeholder="مثال: 250 ساعة")
            with col3:
                equipment_maintenance_cost = st.number_input("تكلفة الصيانة (ريال)", min_value=0, step=500)
            
            # الصف الخامس
            col1, col2 = st.columns(2)
            with col1:
                equipment_operator_required = st.checkbox("يتطلب مشغل")
            with col2:
                equipment_image_url = st.text_input("رابط الصورة", placeholder="مثال: https://example.com/image.jpg")
            
            # وصف المعدة
            equipment_description = st.text_area("وصف المعدة", placeholder="أدخل وصفاً تفصيلياً للمعدة")
            
            # زر الإضافة
            submit_button = st.form_submit_button("إضافة المعدة")
            
            if submit_button:
                # التحقق من البيانات
                if not equipment_name or not equipment_category or not equipment_subcategory:
                    st.error("يرجى إدخال المعلومات الأساسية للمعدة")
                else:
                    # إنشاء معدة جديدة
                    new_equipment = {
                        "id": equipment_id,
                        "name": equipment_name,
                        "category": equipment_category,
                        "subcategory": equipment_subcategory,
                        "brand": equipment_brand,
                        "model": equipment_model,
                        "capacity": equipment_capacity,
                        "production_rate": equipment_production_rate,
                        "hourly_cost": equipment_hourly_cost,
                        "daily_cost": equipment_daily_cost,
                        "weekly_cost": equipment_weekly_cost,
                        "monthly_cost": equipment_monthly_cost,
                        "fuel_consumption": equipment_fuel_consumption,
                        "maintenance_period": equipment_maintenance_period,
                        "maintenance_cost": equipment_maintenance_cost,
                        "operator_required": equipment_operator_required,
                        "description": equipment_description,
                        "image_url": equipment_image_url if equipment_image_url else "https://via.placeholder.com/150"
                    }
                    
                    # إضافة المعدة إلى الكتالوج
                    st.session_state.equipment_catalog = pd.concat([
                        st.session_state.equipment_catalog,
                        pd.DataFrame([new_equipment])
                    ], ignore_index=True)
                    
                    st.success(f"تمت إضافة المعدة {equipment_name} بنجاح!")
    
    def _render_cost_analysis_tab(self):
        """عرض تبويب تحليل التكاليف"""
        
        st.markdown("### تحليل تكاليف المعدات")
        
        # استخراج البيانات
        equipment_df = st.session_state.equipment_catalog
        
        # تحليل متوسط التكاليف حسب الفئة
        st.markdown("#### متوسط التكاليف حسب الفئة")
        
        # حساب متوسط التكاليف لكل فئة
        category_costs = equipment_df.groupby("category").agg({
            "hourly_cost": "mean",
            "daily_cost": "mean",
            "weekly_cost": "mean",
            "monthly_cost": "mean"
        }).reset_index()
        
        # تغيير أسماء الأعمدة
        category_costs.columns = ["الفئة", "متوسط التكلفة بالساعة", "متوسط التكلفة باليوم", "متوسط التكلفة بالأسبوع", "متوسط التكلفة بالشهر"]
        
        # عرض الجدول
        st.dataframe(category_costs, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة
        st.markdown("#### مقارنة متوسط التكاليف اليومية حسب الفئة")
        
        fig = px.bar(
            category_costs,
            x="الفئة",
            y="متوسط التكلفة باليوم",
            title="متوسط التكاليف اليومية حسب فئة المعدات",
            color="الفئة",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل توزيع المعدات حسب الفئة
        st.markdown("#### توزيع المعدات حسب الفئة")
        
        # حساب عدد المعدات في كل فئة
        category_counts = equipment_df["category"].value_counts().reset_index()
        category_counts.columns = ["الفئة", "عدد المعدات"]
        
        # إنشاء رسم بياني دائري
        fig = px.pie(
            category_counts,
            values="عدد المعدات",
            names="الفئة",
            title="توزيع المعدات حسب الفئة",
            color="الفئة"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حاسبة تكاليف المشروع
        st.markdown("#### حاسبة تكاليف المشروع")
        
        with st.form("project_cost_calculator"):
            st.markdown("أدخل المعدات المطلوبة للمشروع")
            
            # اختيار المعدات
            selected_equipment = st.multiselect(
                "اختر المعدات",
                options=equipment_df["name"].tolist(),
                format_func=lambda x: f"{x} ({equipment_df[equipment_df['name'] == x]['id'].iloc[0]})"
            )
            
            # اختيار مدة المشروع
            project_duration = st.number_input("مدة المشروع (بالأيام)", min_value=1, value=30)
            
            # زر الحساب
            calculate_button = st.form_submit_button("حساب التكاليف")
            
            if calculate_button:
                if not selected_equipment:
                    st.error("يرجى اختيار معدة واحدة على الأقل")
                else:
                    # حساب التكاليف
                    project_costs = []
                    
                    for equipment_name in selected_equipment:
                        equipment = equipment_df[equipment_df["name"] == equipment_name].iloc[0]
                        
                        # حساب التكلفة بناءً على المدة
                        if project_duration <= 1:
                            # تكلفة يوم واحد
                            cost = equipment["daily_cost"]
                            cost_type = "يومية"
                        elif project_duration <= 7:
                            # تكلفة أسبوع
                            cost = equipment["weekly_cost"]
                            cost_type = "أسبوعية"
                        else:
                            # تكلفة شهر أو أكثر
                            months = project_duration / 30
                            cost = equipment["monthly_cost"] * months
                            cost_type = "شهرية"
                        
                        project_costs.append({
                            "المعدة": equipment_name,
                            "الكود": equipment["id"],
                            "نوع التكلفة": cost_type,
                            "التكلفة الإجمالية": cost
                        })
                    
                    # عرض النتائج
                    project_costs_df = pd.DataFrame(project_costs)
                    st.dataframe(project_costs_df, use_container_width=True)
                    
                    # حساب إجمالي التكاليف
                    total_cost = project_costs_df["التكلفة الإجمالية"].sum()
                    st.metric("إجمالي تكاليف المعدات للمشروع", f"{total_cost:,.2f} ريال")
    
    def _render_import_export_tab(self):
        """عرض تبويب استيراد/تصدير"""
        
        st.markdown("### استيراد وتصدير بيانات المعدات")
        
        # استيراد البيانات
        st.markdown("#### استيراد البيانات")
        
        uploaded_file = st.file_uploader("اختر ملف Excel لاستيراد بيانات المعدات", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                # قراءة الملف
                imported_df = pd.read_excel(uploaded_file)
                
                # عرض البيانات المستوردة
                st.dataframe(imported_df, use_container_width=True)
                
                # زر الاستيراد
                if st.button("استيراد البيانات"):
                    # التحقق من وجود الأعمدة المطلوبة
                    required_columns = ["id", "name", "category", "subcategory"]
                    
                    if all(col in imported_df.columns for col in required_columns):
                        # دمج البيانات المستوردة مع البيانات الحالية
                        st.session_state.equipment_catalog = pd.concat([
                            st.session_state.equipment_catalog,
                            imported_df
                        ], ignore_index=True).drop_duplicates(subset=["id"])
                        
                        st.success(f"تم استيراد {len(imported_df)} معدة بنجاح!")
                    else:
                        st.error("الملف المستورد لا يحتوي على الأعمدة المطلوبة")
            
            except Exception as e:
                st.error(f"حدث خطأ أثناء استيراد الملف: {str(e)}")
        
        # تصدير البيانات
        st.markdown("#### تصدير البيانات")
        
        # اختيار تنسيق التصدير
        export_format = st.radio("اختر تنسيق التصدير", ["Excel", "CSV", "JSON"], horizontal=True)
        
        if st.button("تصدير البيانات"):
            # استخراج البيانات
            equipment_df = st.session_state.equipment_catalog
            
            # تصدير البيانات حسب التنسيق المختار
            if export_format == "Excel":
                # تصدير إلى Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    equipment_df.to_excel(writer, index=False, sheet_name="Equipment")
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف Excel",
                    data=output.getvalue(),
                    file_name="equipment_catalog.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            elif export_format == "CSV":
                # تصدير إلى CSV
                csv_data = equipment_df.to_csv(index=False)
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف CSV",
                    data=csv_data,
                    file_name="equipment_catalog.csv",
                    mime="text/csv"
                )
            
            else:  # JSON
                # تصدير إلى JSON
                json_data = equipment_df.to_json(orient="records", force_ascii=False)
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف JSON",
                    data=json_data,
                    file_name="equipment_catalog.json",
                    mime="application/json"
                )
    
    def get_equipment_by_id(self, equipment_id):
        """الحصول على معدة بواسطة الكود"""
        
        equipment_df = st.session_state.equipment_catalog
        equipment = equipment_df[equipment_df["id"] == equipment_id]
        
        if not equipment.empty:
            return equipment.iloc[0].to_dict()
        
        return None
    
    def get_equipment_by_category(self, category):
        """الحصول على المعدات حسب الفئة"""
        
        equipment_df = st.session_state.equipment_catalog
        equipment = equipment_df[equipment_df["category"] == category]
        
        if not equipment.empty:
            return equipment.to_dict(orient="records")
        
        return []
    
    def calculate_equipment_cost(self, equipment_id, duration_days):
        """حساب تكلفة المعدة بناءً على المدة"""
        
        equipment = self.get_equipment_by_id(equipment_id)
        
        if equipment:
            # حساب التكلفة بناءً على المدة
            if duration_days <= 1:
                # تكلفة يوم واحد
                return equipment["daily_cost"]
            elif duration_days <= 7:
                # تكلفة أسبوع
                return equipment["weekly_cost"]
            else:
                # تكلفة شهر أو أكثر
                months = duration_days / 30
                return equipment["monthly_cost"] * months
        
        return 0
