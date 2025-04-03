"""
كتالوج العمالة - وحدة إدارة العمالة والمهندسين
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json
from datetime import datetime
import io

class LaborCatalog:
    """كتالوج العمالة"""
    
    def __init__(self):
        """تهيئة كتالوج العمالة"""
        
        # تهيئة حالة الجلسة لكتالوج العمالة
        if 'labor_catalog' not in st.session_state:
            # إنشاء بيانات افتراضية للعمالة
            self._initialize_labor_catalog()
    
    def _initialize_labor_catalog(self):
        """تهيئة بيانات كتالوج العمالة"""
        
        # تعريف فئات العمالة
        labor_categories = [
            "مهندسين",
            "فنيين",
            "عمال مهرة",
            "عمال عاديين",
            "سائقين",
            "مشغلي معدات",
            "إداريين"
        ]
        
        # إنشاء قائمة العمالة
        labor_data = []
        
        # 1. مهندسين
        labor_data.extend([
            {
                "id": "ENG-001",
                "name": "مهندس مدني (خبرة 15+ سنة)",
                "category": "مهندسين",
                "subcategory": "مدني",
                "hourly_rate": 150,
                "daily_rate": 1200,
                "weekly_rate": 6000,
                "monthly_rate": 25000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "إدارة مشاريع، تصميم إنشائي، إشراف على التنفيذ",
                "certifications": "عضوية الهيئة السعودية للمهندسين، PMP",
                "description": "مهندس مدني ذو خبرة 15+ سنة في إدارة وتنفيذ مشاريع البنية التحتية والطرق والجسور"
            },
            {
                "id": "ENG-002",
                "name": "مهندس مدني (خبرة 10-15 سنة)",
                "category": "مهندسين",
                "subcategory": "مدني",
                "hourly_rate": 120,
                "daily_rate": 960,
                "weekly_rate": 4800,
                "monthly_rate": 20000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "إدارة مشاريع، تصميم إنشائي، إشراف على التنفيذ",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس مدني ذو خبرة 10-15 سنة في إدارة وتنفيذ مشاريع البنية التحتية والطرق والجسور"
            },
            {
                "id": "ENG-003",
                "name": "مهندس مدني (خبرة 5-10 سنوات)",
                "category": "مهندسين",
                "subcategory": "مدني",
                "hourly_rate": 100,
                "daily_rate": 800,
                "weekly_rate": 4000,
                "monthly_rate": 16000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تصميم إنشائي، إشراف على التنفيذ، حساب كميات",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس مدني ذو خبرة 5-10 سنوات في تنفيذ مشاريع البنية التحتية والطرق والجسور"
            },
            {
                "id": "ENG-004",
                "name": "مهندس مدني (خبرة 1-5 سنوات)",
                "category": "مهندسين",
                "subcategory": "مدني",
                "hourly_rate": 80,
                "daily_rate": 640,
                "weekly_rate": 3200,
                "monthly_rate": 13000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "إشراف على التنفيذ، حساب كميات، رسم هندسي",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس مدني حديث الخبرة في تنفيذ مشاريع البنية التحتية والطرق والجسور"
            },
            {
                "id": "ENG-005",
                "name": "مهندس ميكانيكي (خبرة 10+ سنة)",
                "category": "مهندسين",
                "subcategory": "ميكانيكي",
                "hourly_rate": 130,
                "daily_rate": 1040,
                "weekly_rate": 5200,
                "monthly_rate": 22000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تصميم أنظمة ميكانيكية، إدارة صيانة المعدات، إشراف على التنفيذ",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس ميكانيكي ذو خبرة 10+ سنة في تصميم وتنفيذ الأنظمة الميكانيكية وصيانة المعدات"
            },
            {
                "id": "ENG-006",
                "name": "مهندس ميكانيكي (خبرة 5-10 سنوات)",
                "category": "مهندسين",
                "subcategory": "ميكانيكي",
                "hourly_rate": 100,
                "daily_rate": 800,
                "weekly_rate": 4000,
                "monthly_rate": 16000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تصميم أنظمة ميكانيكية، صيانة المعدات، إشراف على التنفيذ",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس ميكانيكي ذو خبرة 5-10 سنوات في تنفيذ الأنظمة الميكانيكية وصيانة المعدات"
            },
            {
                "id": "ENG-007",
                "name": "مهندس كهربائي (خبرة 10+ سنة)",
                "category": "مهندسين",
                "subcategory": "كهربائي",
                "hourly_rate": 130,
                "daily_rate": 1040,
                "weekly_rate": 5200,
                "monthly_rate": 22000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تصميم أنظمة كهربائية، إدارة مشاريع كهربائية، إشراف على التنفيذ",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس كهربائي ذو خبرة 10+ سنة في تصميم وتنفيذ الأنظمة الكهربائية للمشاريع الكبرى"
            },
            {
                "id": "ENG-008",
                "name": "مهندس كهربائي (خبرة 5-10 سنوات)",
                "category": "مهندسين",
                "subcategory": "كهربائي",
                "hourly_rate": 100,
                "daily_rate": 800,
                "weekly_rate": 4000,
                "monthly_rate": 16000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تصميم أنظمة كهربائية، إشراف على التنفيذ، اختبار وتشغيل",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس كهربائي ذو خبرة 5-10 سنوات في تنفيذ الأنظمة الكهربائية للمشاريع"
            },
            {
                "id": "ENG-009",
                "name": "مهندس مساحة (خبرة 10+ سنة)",
                "category": "مهندسين",
                "subcategory": "مساحة",
                "hourly_rate": 120,
                "daily_rate": 960,
                "weekly_rate": 4800,
                "monthly_rate": 20000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "مسح طبوغرافي، نظم معلومات جغرافية، حساب كميات",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس مساحة ذو خبرة 10+ سنة في المسح الطبوغرافي ونظم المعلومات الجغرافية"
            },
            {
                "id": "ENG-010",
                "name": "مهندس مساحة (خبرة 5-10 سنوات)",
                "category": "مهندسين",
                "subcategory": "مساحة",
                "hourly_rate": 90,
                "daily_rate": 720,
                "weekly_rate": 3600,
                "monthly_rate": 15000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "مسح طبوغرافي، نظم معلومات جغرافية، حساب كميات",
                "certifications": "عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس مساحة ذو خبرة 5-10 سنوات في المسح الطبوغرافي ونظم المعلومات الجغرافية"
            }
        ])
        
        # 2. فنيين
        labor_data.extend([
            {
                "id": "TECH-001",
                "name": "فني مدني (خبرة 10+ سنة)",
                "category": "فنيين",
                "subcategory": "مدني",
                "hourly_rate": 60,
                "daily_rate": 480,
                "weekly_rate": 2400,
                "monthly_rate": 9500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "قراءة مخططات، إشراف على التنفيذ، فحص جودة",
                "certifications": "دبلوم فني",
                "description": "فني مدني ذو خبرة 10+ سنة في الإشراف على تنفيذ الأعمال المدنية"
            },
            {
                "id": "TECH-002",
                "name": "فني مدني (خبرة 5-10 سنوات)",
                "category": "فنيين",
                "subcategory": "مدني",
                "hourly_rate": 50,
                "daily_rate": 400,
                "weekly_rate": 2000,
                "monthly_rate": 8000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "قراءة مخططات، إشراف على التنفيذ، فحص جودة",
                "certifications": "دبلوم فني",
                "description": "فني مدني ذو خبرة 5-10 سنوات في الإشراف على تنفيذ الأعمال المدنية"
            },
            {
                "id": "TECH-003",
                "name": "فني مساحة (خبرة 10+ سنة)",
                "category": "فنيين",
                "subcategory": "مساحة",
                "hourly_rate": 55,
                "daily_rate": 440,
                "weekly_rate": 2200,
                "monthly_rate": 9000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "استخدام أجهزة المساحة، قراءة مخططات، حساب كميات",
                "certifications": "دبلوم فني",
                "description": "فني مساحة ذو خبرة 10+ سنة في أعمال المساحة وحساب الكميات"
            },
            {
                "id": "TECH-004",
                "name": "فني مساحة (خبرة 5-10 سنوات)",
                "category": "فنيين",
                "subcategory": "مساحة",
                "hourly_rate": 45,
                "daily_rate": 360,
                "weekly_rate": 1800,
                "monthly_rate": 7500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "استخدام أجهزة المساحة، قراءة مخططات، حساب كميات",
                "certifications": "دبلوم فني",
                "description": "فني مساحة ذو خبرة 5-10 سنوات في أعمال المساحة وحساب الكميات"
            },
            {
                "id": "TECH-005",
                "name": "فني كهربائي (خبرة 10+ سنة)",
                "category": "فنيين",
                "subcategory": "كهربائي",
                "hourly_rate": 55,
                "daily_rate": 440,
                "weekly_rate": 2200,
                "monthly_rate": 9000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تمديدات كهربائية، قراءة مخططات، صيانة",
                "certifications": "دبلوم فني",
                "description": "فني كهربائي ذو خبرة 10+ سنة في التمديدات الكهربائية والصيانة"
            },
            {
                "id": "TECH-006",
                "name": "فني كهربائي (خبرة 5-10 سنوات)",
                "category": "فنيين",
                "subcategory": "كهربائي",
                "hourly_rate": 45,
                "daily_rate": 360,
                "weekly_rate": 1800,
                "monthly_rate": 7500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تمديدات كهربائية، قراءة مخططات، صيانة",
                "certifications": "دبلوم فني",
                "description": "فني كهربائي ذو خبرة 5-10 سنوات في التمديدات الكهربائية والصيانة"
            },
            {
                "id": "TECH-007",
                "name": "فني ميكانيكي (خبرة 10+ سنة)",
                "category": "فنيين",
                "subcategory": "ميكانيكي",
                "hourly_rate": 55,
                "daily_rate": 440,
                "weekly_rate": 2200,
                "monthly_rate": 9000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "صيانة معدات، تركيب أنظمة ميكانيكية، قراءة مخططات",
                "certifications": "دبلوم فني",
                "description": "فني ميكانيكي ذو خبرة 10+ سنة في صيانة المعدات وتركيب الأنظمة الميكانيكية"
            },
            {
                "id": "TECH-008",
                "name": "فني ميكانيكي (خبرة 5-10 سنوات)",
                "category": "فنيين",
                "subcategory": "ميكانيكي",
                "hourly_rate": 45,
                "daily_rate": 360,
                "weekly_rate": 1800,
                "monthly_rate": 7500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "صيانة معدات، تركيب أنظمة ميكانيكية، قراءة مخططات",
                "certifications": "دبلوم فني",
                "description": "فني ميكانيكي ذو خبرة 5-10 سنوات في صيانة المعدات وتركيب الأنظمة الميكانيكية"
            },
            {
                "id": "TECH-009",
                "name": "فني سباكة (خبرة 10+ سنة)",
                "category": "فنيين",
                "subcategory": "سباكة",
                "hourly_rate": 50,
                "daily_rate": 400,
                "weekly_rate": 2000,
                "monthly_rate": 8000,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تمديدات صحية، تركيب أنظمة صرف، قراءة مخططات",
                "certifications": "شهادة مهنية",
                "description": "فني سباكة ذو خبرة 10+ سنة في التمديدات الصحية وأنظمة الصرف"
            },
            {
                "id": "TECH-010",
                "name": "فني سباكة (خبرة 5-10 سنوات)",
                "category": "فنيين",
                "subcategory": "سباكة",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تمديدات صحية، تركيب أنظمة صرف، قراءة مخططات",
                "certifications": "شهادة مهنية",
                "description": "فني سباكة ذو خبرة 5-10 سنوات في التمديدات الصحية وأنظمة الصرف"
            }
        ])
        
        # 3. عمال مهرة
        labor_data.extend([
            {
                "id": "SKILL-001",
                "name": "حداد مسلح (خبرة 10+ سنة)",
                "category": "عمال مهرة",
                "subcategory": "حداد",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تجهيز وتركيب حديد التسليح، قراءة مخططات",
                "certifications": "شهادة مهنية",
                "description": "حداد مسلح ذو خبرة 10+ سنة في تجهيز وتركيب حديد التسليح للمنشآت الخرسانية"
            },
            {
                "id": "SKILL-002",
                "name": "حداد مسلح (خبرة 5-10 سنوات)",
                "category": "عمال مهرة",
                "subcategory": "حداد",
                "hourly_rate": 35,
                "daily_rate": 280,
                "weekly_rate": 1400,
                "monthly_rate": 5500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تجهيز وتركيب حديد التسليح، قراءة مخططات",
                "certifications": "شهادة مهنية",
                "description": "حداد مسلح ذو خبرة 5-10 سنوات في تجهيز وتركيب حديد التسليح للمنشآت الخرسانية"
            },
            {
                "id": "SKILL-003",
                "name": "نجار مسلح (خبرة 10+ سنة)",
                "category": "عمال مهرة",
                "subcategory": "نجار",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تجهيز وتركيب الشدات الخشبية، قراءة مخططات",
                "certifications": "شهادة مهنية",
                "description": "نجار مسلح ذو خبرة 10+ سنة في تجهيز وتركيب الشدات الخشبية للمنشآت الخرسانية"
            },
            {
                "id": "SKILL-004",
                "name": "نجار مسلح (خبرة 5-10 سنوات)",
                "category": "عمال مهرة",
                "subcategory": "نجار",
                "hourly_rate": 35,
                "daily_rate": 280,
                "weekly_rate": 1400,
                "monthly_rate": 5500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تجهيز وتركيب الشدات الخشبية، قراءة مخططات",
                "certifications": "شهادة مهنية",
                "description": "نجار مسلح ذو خبرة 5-10 سنوات في تجهيز وتركيب الشدات الخشبية للمنشآت الخرسانية"
            },
            {
                "id": "SKILL-005",
                "name": "بناء (خبرة 10+ سنة)",
                "category": "عمال مهرة",
                "subcategory": "بناء",
                "hourly_rate": 35,
                "daily_rate": 280,
                "weekly_rate": 1400,
                "monthly_rate": 5500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "بناء طابوق، بناء حجر، تشطيبات",
                "certifications": "شهادة مهنية",
                "description": "بناء ذو خبرة 10+ سنة في أعمال البناء بالطابوق والحجر والتشطيبات"
            },
            {
                "id": "SKILL-006",
                "name": "بناء (خبرة 5-10 سنوات)",
                "category": "عمال مهرة",
                "subcategory": "بناء",
                "hourly_rate": 30,
                "daily_rate": 240,
                "weekly_rate": 1200,
                "monthly_rate": 4800,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "بناء طابوق، بناء حجر، تشطيبات",
                "certifications": "شهادة مهنية",
                "description": "بناء ذو خبرة 5-10 سنوات في أعمال البناء بالطابوق والحجر والتشطيبات"
            },
            {
                "id": "SKILL-007",
                "name": "لحام (خبرة 10+ سنة)",
                "category": "عمال مهرة",
                "subcategory": "لحام",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "لحام كهربائي، لحام أرجون، قراءة مخططات",
                "certifications": "شهادة مهنية",
                "description": "لحام ذو خبرة 10+ سنة في أعمال اللحام الكهربائي والأرجون"
            },
            {
                "id": "SKILL-008",
                "name": "لحام (خبرة 5-10 سنوات)",
                "category": "عمال مهرة",
                "subcategory": "لحام",
                "hourly_rate": 35,
                "daily_rate": 280,
                "weekly_rate": 1400,
                "monthly_rate": 5500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "لحام كهربائي، لحام أرجون، قراءة مخططات",
                "certifications": "شهادة مهنية",
                "description": "لحام ذو خبرة 5-10 سنوات في أعمال اللحام الكهربائي والأرجون"
            },
            {
                "id": "SKILL-009",
                "name": "كهربائي (خبرة 10+ سنة)",
                "category": "عمال مهرة",
                "subcategory": "كهربائي",
                "hourly_rate": 35,
                "daily_rate": 280,
                "weekly_rate": 1400,
                "monthly_rate": 5500,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تمديدات كهربائية، تركيب لوحات، صيانة",
                "certifications": "شهادة مهنية",
                "description": "كهربائي ذو خبرة 10+ سنة في التمديدات الكهربائية وتركيب اللوحات والصيانة"
            },
            {
                "id": "SKILL-010",
                "name": "كهربائي (خبرة 5-10 سنوات)",
                "category": "عمال مهرة",
                "subcategory": "كهربائي",
                "hourly_rate": 30,
                "daily_rate": 240,
                "weekly_rate": 1200,
                "monthly_rate": 4800,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تمديدات كهربائية، تركيب لوحات، صيانة",
                "certifications": "شهادة مهنية",
                "description": "كهربائي ذو خبرة 5-10 سنوات في التمديدات الكهربائية وتركيب اللوحات والصيانة"
            }
        ])
        
        # 4. عمال عاديين
        labor_data.extend([
            {
                "id": "LABOR-001",
                "name": "عامل عادي (خبرة 5+ سنة)",
                "category": "عمال عاديين",
                "subcategory": "عامل",
                "hourly_rate": 20,
                "daily_rate": 160,
                "weekly_rate": 800,
                "monthly_rate": 3200,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "أعمال يدوية، مناولة مواد، تنظيف",
                "certifications": "لا يوجد",
                "description": "عامل عادي ذو خبرة 5+ سنة في الأعمال اليدوية ومناولة المواد والتنظيف"
            },
            {
                "id": "LABOR-002",
                "name": "عامل عادي (خبرة 1-5 سنوات)",
                "category": "عمال عاديين",
                "subcategory": "عامل",
                "hourly_rate": 15,
                "daily_rate": 120,
                "weekly_rate": 600,
                "monthly_rate": 2400,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "أعمال يدوية، مناولة مواد، تنظيف",
                "certifications": "لا يوجد",
                "description": "عامل عادي ذو خبرة 1-5 سنوات في الأعمال اليدوية ومناولة المواد والتنظيف"
            },
            {
                "id": "LABOR-003",
                "name": "عامل نظافة (خبرة 3+ سنة)",
                "category": "عمال عاديين",
                "subcategory": "نظافة",
                "hourly_rate": 15,
                "daily_rate": 120,
                "weekly_rate": 600,
                "monthly_rate": 2400,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تنظيف، ترتيب، إزالة مخلفات",
                "certifications": "لا يوجد",
                "description": "عامل نظافة ذو خبرة 3+ سنة في أعمال التنظيف والترتيب وإزالة المخلفات"
            },
            {
                "id": "LABOR-004",
                "name": "عامل نظافة (خبرة 1-3 سنوات)",
                "category": "عمال عاديين",
                "subcategory": "نظافة",
                "hourly_rate": 12,
                "daily_rate": 96,
                "weekly_rate": 480,
                "monthly_rate": 1900,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "تنظيف، ترتيب، إزالة مخلفات",
                "certifications": "لا يوجد",
                "description": "عامل نظافة ذو خبرة 1-3 سنوات في أعمال التنظيف والترتيب وإزالة المخلفات"
            },
            {
                "id": "LABOR-005",
                "name": "عامل مساعد (خبرة 3+ سنة)",
                "category": "عمال عاديين",
                "subcategory": "مساعد",
                "hourly_rate": 18,
                "daily_rate": 144,
                "weekly_rate": 720,
                "monthly_rate": 2900,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "مساعدة في أعمال البناء، مناولة مواد، تنظيف",
                "certifications": "لا يوجد",
                "description": "عامل مساعد ذو خبرة 3+ سنة في مساعدة العمال المهرة ومناولة المواد"
            },
            {
                "id": "LABOR-006",
                "name": "عامل مساعد (خبرة 1-3 سنوات)",
                "category": "عمال عاديين",
                "subcategory": "مساعد",
                "hourly_rate": 15,
                "daily_rate": 120,
                "weekly_rate": 600,
                "monthly_rate": 2400,
                "nationality": "مقيم",
                "availability": "متاح",
                "skills": "مساعدة في أعمال البناء، مناولة مواد، تنظيف",
                "certifications": "لا يوجد",
                "description": "عامل مساعد ذو خبرة 1-3 سنوات في مساعدة العمال المهرة ومناولة المواد"
            }
        ])
        
        # 5. سائقين
        labor_data.extend([
            {
                "id": "DRIVER-001",
                "name": "سائق شاحنة ثقيلة (خبرة 10+ سنة)",
                "category": "سائقين",
                "subcategory": "شاحنة ثقيلة",
                "hourly_rate": 35,
                "daily_rate": 280,
                "weekly_rate": 1400,
                "monthly_rate": 5500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "قيادة شاحنات ثقيلة، صيانة أولية، سجل نظيف",
                "certifications": "رخصة قيادة شاحنات ثقيلة",
                "description": "سائق شاحنة ثقيلة ذو خبرة 10+ سنة في قيادة الشاحنات الثقيلة ونقل المواد"
            },
            {
                "id": "DRIVER-002",
                "name": "سائق شاحنة ثقيلة (خبرة 5-10 سنوات)",
                "category": "سائقين",
                "subcategory": "شاحنة ثقيلة",
                "hourly_rate": 30,
                "daily_rate": 240,
                "weekly_rate": 1200,
                "monthly_rate": 4800,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "قيادة شاحنات ثقيلة، صيانة أولية، سجل نظيف",
                "certifications": "رخصة قيادة شاحنات ثقيلة",
                "description": "سائق شاحنة ثقيلة ذو خبرة 5-10 سنوات في قيادة الشاحنات الثقيلة ونقل المواد"
            },
            {
                "id": "DRIVER-003",
                "name": "سائق شاحنة خلاطة خرسانة (خبرة 10+ سنة)",
                "category": "سائقين",
                "subcategory": "خلاطة خرسانة",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "قيادة خلاطات الخرسانة، صيانة أولية، سجل نظيف",
                "certifications": "رخصة قيادة شاحنات ثقيلة",
                "description": "سائق شاحنة خلاطة خرسانة ذو خبرة 10+ سنة في قيادة خلاطات الخرسانة وصب الخرسانة"
            },
            {
                "id": "DRIVER-004",
                "name": "سائق شاحنة خلاطة خرسانة (خبرة 5-10 سنوات)",
                "category": "سائقين",
                "subcategory": "خلاطة خرسانة",
                "hourly_rate": 35,
                "daily_rate": 280,
                "weekly_rate": 1400,
                "monthly_rate": 5500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "قيادة خلاطات الخرسانة، صيانة أولية، سجل نظيف",
                "certifications": "رخصة قيادة شاحنات ثقيلة",
                "description": "سائق شاحنة خلاطة خرسانة ذو خبرة 5-10 سنوات في قيادة خلاطات الخرسانة وصب الخرسانة"
            },
            {
                "id": "DRIVER-005",
                "name": "سائق شاحنة نقل مياه (خبرة 5+ سنة)",
                "category": "سائقين",
                "subcategory": "نقل مياه",
                "hourly_rate": 30,
                "daily_rate": 240,
                "weekly_rate": 1200,
                "monthly_rate": 4800,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "قيادة شاحنات نقل المياه، صيانة أولية، سجل نظيف",
                "certifications": "رخصة قيادة شاحنات ثقيلة",
                "description": "سائق شاحنة نقل مياه ذو خبرة 5+ سنة في قيادة شاحنات نقل المياه وتوزيع المياه"
            },
            {
                "id": "DRIVER-006",
                "name": "سائق سيارة نقل خفيف (خبرة 5+ سنة)",
                "category": "سائقين",
                "subcategory": "نقل خفيف",
                "hourly_rate": 25,
                "daily_rate": 200,
                "weekly_rate": 1000,
                "monthly_rate": 4000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "قيادة سيارات النقل الخفيف، صيانة أولية، سجل نظيف",
                "certifications": "رخصة قيادة",
                "description": "سائق سيارة نقل خفيف ذو خبرة 5+ سنة في قيادة سيارات النقل الخفيف ونقل المواد والعمال"
            }
        ])
        
        # 6. مشغلي معدات
        labor_data.extend([
            {
                "id": "OPER-001",
                "name": "مشغل حفارة (خبرة 10+ سنة)",
                "category": "مشغلي معدات",
                "subcategory": "حفارة",
                "hourly_rate": 45,
                "daily_rate": 360,
                "weekly_rate": 1800,
                "monthly_rate": 7500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل حفارات، صيانة أولية، حفر دقيق",
                "certifications": "رخصة تشغيل معدات ثقيلة",
                "description": "مشغل حفارة ذو خبرة 10+ سنة في تشغيل الحفارات وأعمال الحفر الدقيق"
            },
            {
                "id": "OPER-002",
                "name": "مشغل حفارة (خبرة 5-10 سنوات)",
                "category": "مشغلي معدات",
                "subcategory": "حفارة",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل حفارات، صيانة أولية، حفر دقيق",
                "certifications": "رخصة تشغيل معدات ثقيلة",
                "description": "مشغل حفارة ذو خبرة 5-10 سنوات في تشغيل الحفارات وأعمال الحفر الدقيق"
            },
            {
                "id": "OPER-003",
                "name": "مشغل لودر (خبرة 10+ سنة)",
                "category": "مشغلي معدات",
                "subcategory": "لودر",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل لودر، صيانة أولية، تحميل دقيق",
                "certifications": "رخصة تشغيل معدات ثقيلة",
                "description": "مشغل لودر ذو خبرة 10+ سنة في تشغيل اللودر وأعمال التحميل الدقيق"
            },
            {
                "id": "OPER-004",
                "name": "مشغل لودر (خبرة 5-10 سنوات)",
                "category": "مشغلي معدات",
                "subcategory": "لودر",
                "hourly_rate": 35,
                "daily_rate": 280,
                "weekly_rate": 1400,
                "monthly_rate": 5500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل لودر، صيانة أولية، تحميل دقيق",
                "certifications": "رخصة تشغيل معدات ثقيلة",
                "description": "مشغل لودر ذو خبرة 5-10 سنوات في تشغيل اللودر وأعمال التحميل الدقيق"
            },
            {
                "id": "OPER-005",
                "name": "مشغل بلدوزر (خبرة 10+ سنة)",
                "category": "مشغلي معدات",
                "subcategory": "بلدوزر",
                "hourly_rate": 45,
                "daily_rate": 360,
                "weekly_rate": 1800,
                "monthly_rate": 7500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل بلدوزر، صيانة أولية، تسوية دقيقة",
                "certifications": "رخصة تشغيل معدات ثقيلة",
                "description": "مشغل بلدوزر ذو خبرة 10+ سنة في تشغيل البلدوزر وأعمال التسوية الدقيقة"
            },
            {
                "id": "OPER-006",
                "name": "مشغل بلدوزر (خبرة 5-10 سنوات)",
                "category": "مشغلي معدات",
                "subcategory": "بلدوزر",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل بلدوزر، صيانة أولية، تسوية دقيقة",
                "certifications": "رخصة تشغيل معدات ثقيلة",
                "description": "مشغل بلدوزر ذو خبرة 5-10 سنوات في تشغيل البلدوزر وأعمال التسوية الدقيقة"
            },
            {
                "id": "OPER-007",
                "name": "مشغل جريدر (خبرة 10+ سنة)",
                "category": "مشغلي معدات",
                "subcategory": "جريدر",
                "hourly_rate": 45,
                "daily_rate": 360,
                "weekly_rate": 1800,
                "monthly_rate": 7500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل جريدر، صيانة أولية، تسوية دقيقة",
                "certifications": "رخصة تشغيل معدات ثقيلة",
                "description": "مشغل جريدر ذو خبرة 10+ سنة في تشغيل الجريدر وأعمال التسوية الدقيقة للطرق"
            },
            {
                "id": "OPER-008",
                "name": "مشغل جريدر (خبرة 5-10 سنوات)",
                "category": "مشغلي معدات",
                "subcategory": "جريدر",
                "hourly_rate": 40,
                "daily_rate": 320,
                "weekly_rate": 1600,
                "monthly_rate": 6500,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل جريدر، صيانة أولية، تسوية دقيقة",
                "certifications": "رخصة تشغيل معدات ثقيلة",
                "description": "مشغل جريدر ذو خبرة 5-10 سنوات في تشغيل الجريدر وأعمال التسوية الدقيقة للطرق"
            },
            {
                "id": "OPER-009",
                "name": "مشغل رافعة (خبرة 10+ سنة)",
                "category": "مشغلي معدات",
                "subcategory": "رافعة",
                "hourly_rate": 50,
                "daily_rate": 400,
                "weekly_rate": 2000,
                "monthly_rate": 8000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل رافعات، صيانة أولية، رفع دقيق",
                "certifications": "رخصة تشغيل رافعات",
                "description": "مشغل رافعة ذو خبرة 10+ سنة في تشغيل الرافعات وأعمال الرفع الدقيق"
            },
            {
                "id": "OPER-010",
                "name": "مشغل رافعة (خبرة 5-10 سنوات)",
                "category": "مشغلي معدات",
                "subcategory": "رافعة",
                "hourly_rate": 45,
                "daily_rate": 360,
                "weekly_rate": 1800,
                "monthly_rate": 7000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تشغيل رافعات، صيانة أولية، رفع دقيق",
                "certifications": "رخصة تشغيل رافعات",
                "description": "مشغل رافعة ذو خبرة 5-10 سنوات في تشغيل الرافعات وأعمال الرفع الدقيق"
            }
        ])
        
        # 7. إداريين
        labor_data.extend([
            {
                "id": "ADMIN-001",
                "name": "مدير مشروع (خبرة 15+ سنة)",
                "category": "إداريين",
                "subcategory": "مدير مشروع",
                "hourly_rate": 200,
                "daily_rate": 1600,
                "weekly_rate": 8000,
                "monthly_rate": 32000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "إدارة مشاريع، تخطيط، متابعة، إعداد تقارير",
                "certifications": "PMP، عضوية الهيئة السعودية للمهندسين",
                "description": "مدير مشروع ذو خبرة 15+ سنة في إدارة مشاريع البنية التحتية والطرق والجسور"
            },
            {
                "id": "ADMIN-002",
                "name": "مدير مشروع (خبرة 10-15 سنة)",
                "category": "إداريين",
                "subcategory": "مدير مشروع",
                "hourly_rate": 150,
                "daily_rate": 1200,
                "weekly_rate": 6000,
                "monthly_rate": 25000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "إدارة مشاريع، تخطيط، متابعة، إعداد تقارير",
                "certifications": "PMP، عضوية الهيئة السعودية للمهندسين",
                "description": "مدير مشروع ذو خبرة 10-15 سنة في إدارة مشاريع البنية التحتية والطرق والجسور"
            },
            {
                "id": "ADMIN-003",
                "name": "مهندس تخطيط (خبرة 10+ سنة)",
                "category": "إداريين",
                "subcategory": "تخطيط",
                "hourly_rate": 120,
                "daily_rate": 960,
                "weekly_rate": 4800,
                "monthly_rate": 20000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تخطيط مشاريع، جدولة، متابعة، إعداد تقارير",
                "certifications": "PMP، Primavera P6، MS Project",
                "description": "مهندس تخطيط ذو خبرة 10+ سنة في تخطيط وجدولة ومتابعة مشاريع البنية التحتية"
            },
            {
                "id": "ADMIN-004",
                "name": "مهندس تخطيط (خبرة 5-10 سنوات)",
                "category": "إداريين",
                "subcategory": "تخطيط",
                "hourly_rate": 100,
                "daily_rate": 800,
                "weekly_rate": 4000,
                "monthly_rate": 16000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "تخطيط مشاريع، جدولة، متابعة، إعداد تقارير",
                "certifications": "Primavera P6، MS Project",
                "description": "مهندس تخطيط ذو خبرة 5-10 سنوات في تخطيط وجدولة ومتابعة مشاريع البنية التحتية"
            },
            {
                "id": "ADMIN-005",
                "name": "مهندس مراقبة جودة (خبرة 10+ سنة)",
                "category": "إداريين",
                "subcategory": "مراقبة جودة",
                "hourly_rate": 120,
                "daily_rate": 960,
                "weekly_rate": 4800,
                "monthly_rate": 20000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "مراقبة جودة، اختبارات، إعداد تقارير، تطبيق معايير",
                "certifications": "ISO 9001، عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس مراقبة جودة ذو خبرة 10+ سنة في مراقبة جودة مشاريع البنية التحتية"
            },
            {
                "id": "ADMIN-006",
                "name": "مهندس مراقبة جودة (خبرة 5-10 سنوات)",
                "category": "إداريين",
                "subcategory": "مراقبة جودة",
                "hourly_rate": 100,
                "daily_rate": 800,
                "weekly_rate": 4000,
                "monthly_rate": 16000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "مراقبة جودة، اختبارات، إعداد تقارير، تطبيق معايير",
                "certifications": "ISO 9001، عضوية الهيئة السعودية للمهندسين",
                "description": "مهندس مراقبة جودة ذو خبرة 5-10 سنوات في مراقبة جودة مشاريع البنية التحتية"
            },
            {
                "id": "ADMIN-007",
                "name": "مهندس سلامة (خبرة 10+ سنة)",
                "category": "إداريين",
                "subcategory": "سلامة",
                "hourly_rate": 120,
                "daily_rate": 960,
                "weekly_rate": 4800,
                "monthly_rate": 20000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "إدارة السلامة، تدريب، تفتيش، إعداد تقارير",
                "certifications": "NEBOSH، OSHA",
                "description": "مهندس سلامة ذو خبرة 10+ سنة في إدارة السلامة في مشاريع البنية التحتية"
            },
            {
                "id": "ADMIN-008",
                "name": "مهندس سلامة (خبرة 5-10 سنوات)",
                "category": "إداريين",
                "subcategory": "سلامة",
                "hourly_rate": 100,
                "daily_rate": 800,
                "weekly_rate": 4000,
                "monthly_rate": 16000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "إدارة السلامة، تدريب، تفتيش، إعداد تقارير",
                "certifications": "NEBOSH، OSHA",
                "description": "مهندس سلامة ذو خبرة 5-10 سنوات في إدارة السلامة في مشاريع البنية التحتية"
            },
            {
                "id": "ADMIN-009",
                "name": "محاسب مشاريع (خبرة 10+ سنة)",
                "category": "إداريين",
                "subcategory": "محاسبة",
                "hourly_rate": 100,
                "daily_rate": 800,
                "weekly_rate": 4000,
                "monthly_rate": 16000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "محاسبة مشاريع، إعداد تقارير مالية، متابعة مصروفات",
                "certifications": "SOCPA",
                "description": "محاسب مشاريع ذو خبرة 10+ سنة في محاسبة مشاريع البنية التحتية"
            },
            {
                "id": "ADMIN-010",
                "name": "محاسب مشاريع (خبرة 5-10 سنوات)",
                "category": "إداريين",
                "subcategory": "محاسبة",
                "hourly_rate": 80,
                "daily_rate": 640,
                "weekly_rate": 3200,
                "monthly_rate": 13000,
                "nationality": "سعودي",
                "availability": "متاح",
                "skills": "محاسبة مشاريع، إعداد تقارير مالية، متابعة مصروفات",
                "certifications": "SOCPA",
                "description": "محاسب مشاريع ذو خبرة 5-10 سنوات في محاسبة مشاريع البنية التحتية"
            }
        ])
        
        # تخزين البيانات في حالة الجلسة
        st.session_state.labor_catalog = pd.DataFrame(labor_data)
    
    def render(self):
        """عرض واجهة كتالوج العمالة"""
        
        st.markdown("## كتالوج العمالة والمهندسين")
        
        # إنشاء تبويبات لعرض الكتالوج
        tabs = st.tabs([
            "عرض الكتالوج", 
            "إضافة عامل", 
            "تحليل الأسعار",
            "استيراد/تصدير"
        ])
        
        with tabs[0]:
            self._render_catalog_view_tab()
        
        with tabs[1]:
            self._render_add_labor_tab()
        
        with tabs[2]:
            self._render_price_analysis_tab()
        
        with tabs[3]:
            self._render_import_export_tab()
    
    def _render_catalog_view_tab(self):
        """عرض تبويب عرض الكتالوج"""
        
        st.markdown("### عرض كتالوج العمالة والمهندسين")
        
        # استخراج البيانات
        labor_df = st.session_state.labor_catalog
        
        # إنشاء فلاتر للعرض
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # فلتر حسب الفئة
            categories = ["الكل"] + sorted(labor_df["category"].unique().tolist())
            selected_category = st.selectbox("اختر فئة العمالة", categories)
        
        with col2:
            # فلتر حسب الفئة الفرعية
            if selected_category != "الكل":
                subcategories = ["الكل"] + sorted(labor_df[labor_df["category"] == selected_category]["subcategory"].unique().tolist())
            else:
                subcategories = ["الكل"] + sorted(labor_df["subcategory"].unique().tolist())
            
            selected_subcategory = st.selectbox("اختر التخصص", subcategories)
        
        with col3:
            # فلتر حسب الجنسية
            nationalities = ["الكل"] + sorted(labor_df["nationality"].unique().tolist())
            selected_nationality = st.selectbox("اختر الجنسية", nationalities)
        
        # تطبيق الفلاتر
        filtered_df = labor_df.copy()
        
        if selected_category != "الكل":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]
        
        if selected_subcategory != "الكل":
            filtered_df = filtered_df[filtered_df["subcategory"] == selected_subcategory]
        
        if selected_nationality != "الكل":
            filtered_df = filtered_df[filtered_df["nationality"] == selected_nationality]
        
        # عرض البيانات
        if not filtered_df.empty:
            # عرض عدد النتائج
            st.info(f"تم العثور على {len(filtered_df)} عامل/مهندس")
            
            # عرض العمالة في شكل بطاقات
            for i, (_, labor) in enumerate(filtered_df.iterrows()):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    # عرض صورة العامل (استخدام صورة افتراضية)
                    st.image("https://via.placeholder.com/150", caption=labor["name"])
                
                with col2:
                    # عرض معلومات العامل
                    st.markdown(f"**{labor['name']}** (الكود: {labor['id']})")
                    st.markdown(f"الفئة: {labor['category']} - {labor['subcategory']}")
                    st.markdown(f"الجنسية: {labor['nationality']} | الحالة: {labor['availability']}")
                    st.markdown(f"الأسعار: {labor['hourly_rate']} ريال/ساعة | {labor['daily_rate']} ريال/يوم | {labor['monthly_rate']} ريال/شهر")
                    st.markdown(f"المهارات: {labor['skills']}")
                
                # إضافة زر لعرض التفاصيل
                if st.button(f"عرض التفاصيل الكاملة", key=f"details_{labor['id']}"):
                    st.session_state.selected_labor = labor['id']
                    self._show_labor_details(labor)
                
                st.markdown("---")
        else:
            st.warning("لا توجد عمالة تطابق معايير البحث")
    
    def _show_labor_details(self, labor):
        """عرض تفاصيل العامل"""
        
        st.markdown(f"## تفاصيل العامل/المهندس: {labor['name']}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # عرض صورة العامل (استخدام صورة افتراضية)
            st.image("https://via.placeholder.com/300", caption=labor["name"])
        
        with col2:
            # عرض المعلومات الأساسية
            st.markdown("### المعلومات الأساسية")
            st.markdown(f"**الكود:** {labor['id']}")
            st.markdown(f"**الفئة:** {labor['category']} - {labor['subcategory']}")
            st.markdown(f"**الجنسية:** {labor['nationality']}")
            st.markdown(f"**الحالة:** {labor['availability']}")
            st.markdown(f"**المهارات:** {labor['skills']}")
            st.markdown(f"**الشهادات:** {labor['certifications']}")
            st.markdown(f"**الوصف:** {labor['description']}")
        
        # عرض معلومات الأسعار
        st.markdown("### معلومات الأسعار")
        
        price_data = {
            "وحدة الزمن": ["ساعة", "يوم", "أسبوع", "شهر"],
            "السعر (ريال)": [
                labor['hourly_rate'],
                labor['daily_rate'],
                labor['weekly_rate'],
                labor['monthly_rate']
            ]
        }
        
        price_df = pd.DataFrame(price_data)
        st.dataframe(price_df, use_container_width=True)
        
        # إضافة زر للتعديل
        if st.button("تعديل بيانات العامل"):
            st.session_state.edit_labor = labor['id']
            # هنا يمكن إضافة منطق التعديل
    
    def _render_add_labor_tab(self):
        """عرض تبويب إضافة عامل"""
        
        st.markdown("### إضافة عامل/مهندس جديد")
        
        # استخراج البيانات
        labor_df = st.session_state.labor_catalog
        
        # إنشاء نموذج إضافة عامل
        with st.form("add_labor_form"):
            st.markdown("#### المعلومات الأساسية")
            
            # الصف الأول
            col1, col2 = st.columns(2)
            with col1:
                labor_id = st.text_input("كود العامل", value=f"LABOR-{len(labor_df) + 1:03d}")
                labor_name = st.text_input("اسم العامل", placeholder="مثال: مهندس مدني (خبرة 10+ سنة)")
            
            with col2:
                # استخراج الفئات والفئات الفرعية الموجودة
                categories = sorted(labor_df["category"].unique().tolist())
                labor_category = st.selectbox("فئة العامل", categories)
                
                # استخراج الفئات الفرعية بناءً على الفئة المختارة
                subcategories = sorted(labor_df[labor_df["category"] == labor_category]["subcategory"].unique().tolist())
                labor_subcategory = st.selectbox("التخصص", subcategories)
            
            # الصف الثاني
            col1, col2 = st.columns(2)
            with col1:
                labor_nationality = st.selectbox("الجنسية", ["سعودي", "مقيم"])
            with col2:
                labor_availability = st.selectbox("الحالة", ["متاح", "غير متاح"])
            
            # الصف الثالث - الأسعار
            st.markdown("#### معلومات الأسعار")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                labor_hourly_rate = st.number_input("السعر بالساعة (ريال)", min_value=0, step=5)
            with col2:
                labor_daily_rate = st.number_input("السعر باليوم (ريال)", min_value=0, step=40)
            with col3:
                labor_weekly_rate = st.number_input("السعر بالأسبوع (ريال)", min_value=0, step=200)
            with col4:
                labor_monthly_rate = st.number_input("السعر بالشهر (ريال)", min_value=0, step=1000)
            
            # المهارات والشهادات
            st.markdown("#### المهارات والشهادات")
            
            labor_skills = st.text_area("المهارات", placeholder="مثال: إدارة مشاريع، تصميم إنشائي، إشراف على التنفيذ")
            labor_certifications = st.text_input("الشهادات", placeholder="مثال: عضوية الهيئة السعودية للمهندسين، PMP")
            
            # وصف العامل
            labor_description = st.text_area("وصف العامل", placeholder="أدخل وصفاً تفصيلياً للعامل/المهندس")
            
            # زر الإضافة
            submit_button = st.form_submit_button("إضافة العامل")
            
            if submit_button:
                # التحقق من البيانات
                if not labor_name or not labor_category or not labor_subcategory:
                    st.error("يرجى إدخال المعلومات الأساسية للعامل")
                else:
                    # إنشاء عامل جديد
                    new_labor = {
                        "id": labor_id,
                        "name": labor_name,
                        "category": labor_category,
                        "subcategory": labor_subcategory,
                        "hourly_rate": labor_hourly_rate,
                        "daily_rate": labor_daily_rate,
                        "weekly_rate": labor_weekly_rate,
                        "monthly_rate": labor_monthly_rate,
                        "nationality": labor_nationality,
                        "availability": labor_availability,
                        "skills": labor_skills,
                        "certifications": labor_certifications,
                        "description": labor_description
                    }
                    
                    # إضافة العامل إلى الكتالوج
                    st.session_state.labor_catalog = pd.concat([
                        st.session_state.labor_catalog,
                        pd.DataFrame([new_labor])
                    ], ignore_index=True)
                    
                    st.success(f"تمت إضافة العامل {labor_name} بنجاح!")
    
    def _render_price_analysis_tab(self):
        """عرض تبويب تحليل الأسعار"""
        
        st.markdown("### تحليل أسعار العمالة والمهندسين")
        
        # استخراج البيانات
        labor_df = st.session_state.labor_catalog
        
        # تحليل متوسط الأسعار حسب الفئة
        st.markdown("#### متوسط الأسعار حسب الفئة")
        
        # حساب متوسط الأسعار لكل فئة
        category_prices = labor_df.groupby("category").agg({
            "hourly_rate": "mean",
            "daily_rate": "mean",
            "monthly_rate": "mean"
        }).reset_index()
        
        # تغيير أسماء الأعمدة
        category_prices.columns = ["الفئة", "متوسط السعر بالساعة", "متوسط السعر باليوم", "متوسط السعر بالشهر"]
        
        # عرض الجدول
        st.dataframe(category_prices, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة
        st.markdown("#### مقارنة متوسط الأسعار الشهرية حسب الفئة")
        
        fig = px.bar(
            category_prices,
            x="الفئة",
            y="متوسط السعر بالشهر",
            title="متوسط أسعار العمالة والمهندسين الشهرية حسب الفئة",
            color="الفئة",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل توزيع العمالة حسب الجنسية
        st.markdown("#### توزيع العمالة حسب الجنسية")
        
        # حساب عدد العمالة حسب الجنسية
        nationality_counts = labor_df["nationality"].value_counts().reset_index()
        nationality_counts.columns = ["الجنسية", "عدد العمالة"]
        
        # إنشاء رسم بياني دائري
        fig = px.pie(
            nationality_counts,
            values="عدد العمالة",
            names="الجنسية",
            title="توزيع العمالة حسب الجنسية",
            color="الجنسية"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل متوسط الأسعار حسب التخصص
        st.markdown("#### متوسط الأسعار حسب التخصص")
        
        # اختيار الفئة للتحليل
        selected_category_for_analysis = st.selectbox(
            "اختر الفئة للتحليل",
            sorted(labor_df["category"].unique().tolist())
        )
        
        # حساب متوسط الأسعار لكل تخصص ضمن الفئة المختارة
        subcategory_prices = labor_df[labor_df["category"] == selected_category_for_analysis].groupby("subcategory").agg({
            "hourly_rate": "mean",
            "daily_rate": "mean",
            "monthly_rate": "mean"
        }).reset_index()
        
        # تغيير أسماء الأعمدة
        subcategory_prices.columns = ["التخصص", "متوسط السعر بالساعة", "متوسط السعر باليوم", "متوسط السعر بالشهر"]
        
        # عرض الجدول
        st.dataframe(subcategory_prices, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة
        fig = px.bar(
            subcategory_prices,
            x="التخصص",
            y="متوسط السعر بالشهر",
            title=f"متوسط أسعار {selected_category_for_analysis} الشهرية حسب التخصص",
            color="التخصص",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حاسبة تكاليف العمالة للمشروع
        st.markdown("#### حاسبة تكاليف العمالة للمشروع")
        
        with st.form("project_labor_calculator"):
            st.markdown("أدخل العمالة المطلوبة للمشروع")
            
            # اختيار العمالة
            selected_labor = st.multiselect(
                "اختر العمالة",
                options=labor_df["name"].tolist(),
                format_func=lambda x: f"{x} ({labor_df[labor_df['name'] == x]['id'].iloc[0]})"
            )
            
            # اختيار وحدة الزمن
            time_unit = st.radio("اختر وحدة الزمن", ["ساعة", "يوم", "أسبوع", "شهر"], horizontal=True)
            
            # إنشاء حقول إدخال الكميات
            quantities = {}
            
            if selected_labor:
                st.markdown("أدخل المدة المطلوبة")
                
                for labor_name in selected_labor:
                    quantities[labor_name] = st.number_input(
                        f"{labor_name}",
                        min_value=0,
                        step=1,
                        key=f"qty_{labor_df[labor_df['name'] == labor_name]['id'].iloc[0]}"
                    )
            
            # زر الحساب
            calculate_button = st.form_submit_button("حساب التكاليف")
            
            if calculate_button:
                if not selected_labor:
                    st.error("يرجى اختيار عامل واحد على الأقل")
                else:
                    # حساب التكاليف
                    project_costs = []
                    
                    for labor_name in selected_labor:
                        labor = labor_df[labor_df["name"] == labor_name].iloc[0]
                        quantity = quantities[labor_name]
                        
                        if quantity > 0:
                            # تحديد السعر بناءً على وحدة الزمن
                            if time_unit == "ساعة":
                                rate = labor["hourly_rate"]
                                rate_name = "السعر بالساعة"
                            elif time_unit == "يوم":
                                rate = labor["daily_rate"]
                                rate_name = "السعر باليوم"
                            elif time_unit == "أسبوع":
                                rate = labor["weekly_rate"]
                                rate_name = "السعر بالأسبوع"
                            else:  # شهر
                                rate = labor["monthly_rate"]
                                rate_name = "السعر بالشهر"
                            
                            cost = rate * quantity
                            
                            project_costs.append({
                                "العامل": labor_name,
                                "الكود": labor["id"],
                                "الفئة": labor["category"],
                                "التخصص": labor["subcategory"],
                                rate_name: rate,
                                f"عدد {time_unit}ات": quantity,
                                "التكلفة الإجمالية": cost
                            })
                    
                    if project_costs:
                        # عرض النتائج
                        project_costs_df = pd.DataFrame(project_costs)
                        st.dataframe(project_costs_df, use_container_width=True)
                        
                        # حساب إجمالي التكاليف
                        total_cost = project_costs_df["التكلفة الإجمالية"].sum()
                        st.metric("إجمالي تكاليف العمالة للمشروع", f"{total_cost:,.2f} ريال")
                    else:
                        st.warning("يرجى إدخال مدة أكبر من صفر")
    
    def _render_import_export_tab(self):
        """عرض تبويب استيراد/تصدير"""
        
        st.markdown("### استيراد وتصدير بيانات العمالة والمهندسين")
        
        # استيراد البيانات
        st.markdown("#### استيراد البيانات")
        
        uploaded_file = st.file_uploader("اختر ملف Excel لاستيراد بيانات العمالة", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                # قراءة الملف
                imported_df = pd.read_excel(uploaded_file)
                
                # عرض البيانات المستوردة
                st.dataframe(imported_df, use_container_width=True)
                
                # زر الاستيراد
                if st.button("استيراد البيانات"):
                    # التحقق من وجود الأعمدة المطلوبة
                    required_columns = ["id", "name", "category", "subcategory", "hourly_rate", "daily_rate", "weekly_rate", "monthly_rate"]
                    
                    if all(col in imported_df.columns for col in required_columns):
                        # دمج البيانات المستوردة مع البيانات الحالية
                        st.session_state.labor_catalog = pd.concat([
                            st.session_state.labor_catalog,
                            imported_df
                        ], ignore_index=True).drop_duplicates(subset=["id"])
                        
                        st.success(f"تم استيراد {len(imported_df)} عامل/مهندس بنجاح!")
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
            labor_df = st.session_state.labor_catalog
            
            # تصدير البيانات حسب التنسيق المختار
            if export_format == "Excel":
                # تصدير إلى Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    labor_df.to_excel(writer, index=False, sheet_name="Labor")
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف Excel",
                    data=output.getvalue(),
                    file_name="labor_catalog.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            elif export_format == "CSV":
                # تصدير إلى CSV
                csv_data = labor_df.to_csv(index=False)
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف CSV",
                    data=csv_data,
                    file_name="labor_catalog.csv",
                    mime="text/csv"
                )
            
            else:  # JSON
                # تصدير إلى JSON
                json_data = labor_df.to_json(orient="records", force_ascii=False)
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف JSON",
                    data=json_data,
                    file_name="labor_catalog.json",
                    mime="application/json"
                )
    
    def get_labor_by_id(self, labor_id):
        """الحصول على عامل بواسطة الكود"""
        
        labor_df = st.session_state.labor_catalog
        labor = labor_df[labor_df["id"] == labor_id]
        
        if not labor.empty:
            return labor.iloc[0].to_dict()
        
        return None
    
    def get_labor_by_category(self, category):
        """الحصول على العمالة حسب الفئة"""
        
        labor_df = st.session_state.labor_catalog
        labor = labor_df[labor_df["category"] == category]
        
        if not labor.empty:
            return labor.to_dict(orient="records")
        
        return []
    
    def calculate_labor_cost(self, labor_id, quantity, time_unit="day"):
        """حساب تكلفة العامل بناءً على الكمية ووحدة الزمن"""
        
        labor = self.get_labor_by_id(labor_id)
        
        if labor:
            if time_unit == "hour":
                return labor["hourly_rate"] * quantity
            elif time_unit == "day":
                return labor["daily_rate"] * quantity
            elif time_unit == "week":
                return labor["weekly_rate"] * quantity
            elif time_unit == "month":
                return labor["monthly_rate"] * quantity
        
        return 0
