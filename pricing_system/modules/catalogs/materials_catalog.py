"""
كتالوج المواد - وحدة إدارة مواد المقاولات
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json
from datetime import datetime
import io

class MaterialsCatalog:
    """كتالوج المواد"""
    
    def __init__(self):
        """تهيئة كتالوج المواد"""
        
        # تهيئة حالة الجلسة لكتالوج المواد
        if 'materials_catalog' not in st.session_state:
            # إنشاء بيانات افتراضية للمواد
            self._initialize_materials_catalog()
    
    def _initialize_materials_catalog(self):
        """تهيئة بيانات كتالوج المواد"""
        
        # تعريف فئات المواد
        material_categories = [
            "مواد الخرسانة",
            "مواد البناء",
            "مواد الطرق",
            "مواد الصرف الصحي",
            "مواد العزل",
            "مواد التشطيبات",
            "مواد كهربائية",
            "مواد ميكانيكية",
            "مواد الري والزراعة",
            "مواد متنوعة"
        ]
        
        # إنشاء قائمة المواد
        materials_data = []
        
        # 1. مواد الخرسانة
        materials_data.extend([
            {
                "id": "MAT-001",
                "name": "أسمنت بورتلاندي عادي",
                "category": "مواد الخرسانة",
                "subcategory": "أسمنت",
                "unit": "طن",
                "price": 600,
                "supplier": "شركة أسمنت اليمامة",
                "origin": "محلي",
                "lead_time": 2,
                "min_order": 10,
                "description": "أسمنت بورتلاندي عادي مطابق للمواصفات السعودية",
                "image_url": "https://example.com/cement.jpg"
            },
            {
                "id": "MAT-002",
                "name": "أسمنت مقاوم للكبريتات",
                "category": "مواد الخرسانة",
                "subcategory": "أسمنت",
                "unit": "طن",
                "price": 650,
                "supplier": "شركة أسمنت ينبع",
                "origin": "محلي",
                "lead_time": 2,
                "min_order": 10,
                "description": "أسمنت مقاوم للكبريتات للمناطق ذات التربة الكبريتية",
                "image_url": "https://example.com/srcement.jpg"
            },
            {
                "id": "MAT-003",
                "name": "رمل خشن",
                "category": "مواد الخرسانة",
                "subcategory": "ركام",
                "unit": "م3",
                "price": 80,
                "supplier": "كسارات الرياض",
                "origin": "محلي",
                "lead_time": 1,
                "min_order": 20,
                "description": "رمل خشن للخرسانة مطابق للمواصفات",
                "image_url": "https://example.com/sand.jpg"
            },
            {
                "id": "MAT-004",
                "name": "بحص مقاس 3/4 بوصة",
                "category": "مواد الخرسانة",
                "subcategory": "ركام",
                "unit": "م3",
                "price": 120,
                "supplier": "كسارات الرياض",
                "origin": "محلي",
                "lead_time": 1,
                "min_order": 20,
                "description": "بحص مقاس 3/4 بوصة للخرسانة مطابق للمواصفات",
                "image_url": "https://example.com/gravel.jpg"
            },
            {
                "id": "MAT-005",
                "name": "بحص مقاس 3/8 بوصة",
                "category": "مواد الخرسانة",
                "subcategory": "ركام",
                "unit": "م3",
                "price": 130,
                "supplier": "كسارات الرياض",
                "origin": "محلي",
                "lead_time": 1,
                "min_order": 20,
                "description": "بحص مقاس 3/8 بوصة للخرسانة مطابق للمواصفات",
                "image_url": "https://example.com/gravel2.jpg"
            },
            {
                "id": "MAT-006",
                "name": "ماء",
                "category": "مواد الخرسانة",
                "subcategory": "سوائل",
                "unit": "م3",
                "price": 5,
                "supplier": "متعدد",
                "origin": "محلي",
                "lead_time": 1,
                "min_order": 10,
                "description": "ماء صالح للخلط في الخرسانة",
                "image_url": "https://example.com/water.jpg"
            },
            {
                "id": "MAT-007",
                "name": "إضافة ملدنة للخرسانة",
                "category": "مواد الخرسانة",
                "subcategory": "إضافات",
                "unit": "لتر",
                "price": 15,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 200,
                "description": "إضافة ملدنة لتحسين قابلية تشغيل الخرسانة",
                "image_url": "https://example.com/plasticizer.jpg"
            },
            {
                "id": "MAT-008",
                "name": "إضافة مؤخرة للشك",
                "category": "مواد الخرسانة",
                "subcategory": "إضافات",
                "unit": "لتر",
                "price": 18,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 200,
                "description": "إضافة مؤخرة للشك للصب في الأجواء الحارة",
                "image_url": "https://example.com/retarder.jpg"
            },
            {
                "id": "MAT-009",
                "name": "إضافة معجلة للشك",
                "category": "مواد الخرسانة",
                "subcategory": "إضافات",
                "unit": "لتر",
                "price": 20,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 200,
                "description": "إضافة معجلة للشك للصب في الأجواء الباردة",
                "image_url": "https://example.com/accelerator.jpg"
            },
            {
                "id": "MAT-010",
                "name": "ألياف بوليبروبلين",
                "category": "مواد الخرسانة",
                "subcategory": "إضافات",
                "unit": "كجم",
                "price": 35,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 100,
                "description": "ألياف بوليبروبلين لتقليل التشققات في الخرسانة",
                "image_url": "https://example.com/fibers.jpg"
            }
        ])
        
        # 2. مواد البناء
        materials_data.extend([
            {
                "id": "MAT-011",
                "name": "طابوق أسمنتي مقاس 20×20×40 سم",
                "category": "مواد البناء",
                "subcategory": "طابوق",
                "unit": "قطعة",
                "price": 3.5,
                "supplier": "مصنع الرياض للطابوق",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 1000,
                "description": "طابوق أسمنتي مقاس 20×20×40 سم للجدران الخارجية",
                "image_url": "https://example.com/block.jpg"
            },
            {
                "id": "MAT-012",
                "name": "طابوق أسمنتي مقاس 15×20×40 سم",
                "category": "مواد البناء",
                "subcategory": "طابوق",
                "unit": "قطعة",
                "price": 3,
                "supplier": "مصنع الرياض للطابوق",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 1000,
                "description": "طابوق أسمنتي مقاس 15×20×40 سم للجدران الداخلية",
                "image_url": "https://example.com/block2.jpg"
            },
            {
                "id": "MAT-013",
                "name": "طابوق أسمنتي مقاس 10×20×40 سم",
                "category": "مواد البناء",
                "subcategory": "طابوق",
                "unit": "قطعة",
                "price": 2.5,
                "supplier": "مصنع الرياض للطابوق",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 1000,
                "description": "طابوق أسمنتي مقاس 10×20×40 سم للجدران الداخلية",
                "image_url": "https://example.com/block3.jpg"
            },
            {
                "id": "MAT-014",
                "name": "حديد تسليح قطر 8 مم",
                "category": "مواد البناء",
                "subcategory": "حديد تسليح",
                "unit": "طن",
                "price": 3200,
                "supplier": "شركة حديد الراجحي",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 5,
                "description": "حديد تسليح قطر 8 مم مطابق للمواصفات السعودية",
                "image_url": "https://example.com/rebar8.jpg"
            },
            {
                "id": "MAT-015",
                "name": "حديد تسليح قطر 10 مم",
                "category": "مواد البناء",
                "subcategory": "حديد تسليح",
                "unit": "طن",
                "price": 3150,
                "supplier": "شركة حديد الراجحي",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 5,
                "description": "حديد تسليح قطر 10 مم مطابق للمواصفات السعودية",
                "image_url": "https://example.com/rebar10.jpg"
            },
            {
                "id": "MAT-016",
                "name": "حديد تسليح قطر 12 مم",
                "category": "مواد البناء",
                "subcategory": "حديد تسليح",
                "unit": "طن",
                "price": 3100,
                "supplier": "شركة حديد الراجحي",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 5,
                "description": "حديد تسليح قطر 12 مم مطابق للمواصفات السعودية",
                "image_url": "https://example.com/rebar12.jpg"
            },
            {
                "id": "MAT-017",
                "name": "حديد تسليح قطر 16 مم",
                "category": "مواد البناء",
                "subcategory": "حديد تسليح",
                "unit": "طن",
                "price": 3050,
                "supplier": "شركة حديد الراجحي",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 5,
                "description": "حديد تسليح قطر 16 مم مطابق للمواصفات السعودية",
                "image_url": "https://example.com/rebar16.jpg"
            },
            {
                "id": "MAT-018",
                "name": "حديد تسليح قطر 20 مم",
                "category": "مواد البناء",
                "subcategory": "حديد تسليح",
                "unit": "طن",
                "price": 3000,
                "supplier": "شركة حديد الراجحي",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 5,
                "description": "حديد تسليح قطر 20 مم مطابق للمواصفات السعودية",
                "image_url": "https://example.com/rebar20.jpg"
            },
            {
                "id": "MAT-019",
                "name": "حديد تسليح قطر 25 مم",
                "category": "مواد البناء",
                "subcategory": "حديد تسليح",
                "unit": "طن",
                "price": 2950,
                "supplier": "شركة حديد الراجحي",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 5,
                "description": "حديد تسليح قطر 25 مم مطابق للمواصفات السعودية",
                "image_url": "https://example.com/rebar25.jpg"
            },
            {
                "id": "MAT-020",
                "name": "شبك حديد ملحوم 6 مم",
                "category": "مواد البناء",
                "subcategory": "حديد تسليح",
                "unit": "م2",
                "price": 25,
                "supplier": "شركة حديد الراجحي",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "شبك حديد ملحوم 6 مم للأرضيات والأسقف",
                "image_url": "https://example.com/wiremesh.jpg"
            }
        ])
        
        # 3. مواد الطرق
        materials_data.extend([
            {
                "id": "MAT-021",
                "name": "بيس كورس",
                "category": "مواد الطرق",
                "subcategory": "طبقات أساس",
                "unit": "م3",
                "price": 70,
                "supplier": "كسارات الرياض",
                "origin": "محلي",
                "lead_time": 2,
                "min_order": 50,
                "description": "مادة بيس كورس لطبقات الأساس في الطرق",
                "image_url": "https://example.com/basecourse.jpg"
            },
            {
                "id": "MAT-022",
                "name": "ساب بيس",
                "category": "مواد الطرق",
                "subcategory": "طبقات أساس",
                "unit": "م3",
                "price": 60,
                "supplier": "كسارات الرياض",
                "origin": "محلي",
                "lead_time": 2,
                "min_order": 50,
                "description": "مادة ساب بيس لطبقات ما تحت الأساس في الطرق",
                "image_url": "https://example.com/subbase.jpg"
            },
            {
                "id": "MAT-023",
                "name": "بيتومين MC-70",
                "category": "مواد الطرق",
                "subcategory": "بيتومين",
                "unit": "لتر",
                "price": 3.5,
                "supplier": "أرامكو",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 10000,
                "description": "بيتومين MC-70 للطبقة التأسيسية",
                "image_url": "https://example.com/bitumen1.jpg"
            },
            {
                "id": "MAT-024",
                "name": "بيتومين RC-250",
                "category": "مواد الطرق",
                "subcategory": "بيتومين",
                "unit": "لتر",
                "price": 3.8,
                "supplier": "أرامكو",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 10000,
                "description": "بيتومين RC-250 للطبقة اللاصقة",
                "image_url": "https://example.com/bitumen2.jpg"
            },
            {
                "id": "MAT-025",
                "name": "خلطة إسفلتية ساخنة",
                "category": "مواد الطرق",
                "subcategory": "إسفلت",
                "unit": "طن",
                "price": 250,
                "supplier": "مصنع الإسفلت المركزي",
                "origin": "محلي",
                "lead_time": 1,
                "min_order": 20,
                "description": "خلطة إسفلتية ساخنة لطبقات الرصف",
                "image_url": "https://example.com/asphalt.jpg"
            },
            {
                "id": "MAT-026",
                "name": "بردورات خرسانية",
                "category": "مواد الطرق",
                "subcategory": "بردورات",
                "unit": "متر طولي",
                "price": 35,
                "supplier": "مصنع الخرسانة الجاهزة",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "بردورات خرسانية مقاس 15×30×50 سم",
                "image_url": "https://example.com/curb.jpg"
            },
            {
                "id": "MAT-027",
                "name": "انترلوك خرساني",
                "category": "مواد الطرق",
                "subcategory": "رصف",
                "unit": "م2",
                "price": 45,
                "supplier": "مصنع الخرسانة الجاهزة",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "انترلوك خرساني سماكة 8 سم للأرصفة",
                "image_url": "https://example.com/interlock.jpg"
            },
            {
                "id": "MAT-028",
                "name": "دهان خطوط طرق أبيض",
                "category": "مواد الطرق",
                "subcategory": "دهانات",
                "unit": "لتر",
                "price": 25,
                "supplier": "شركة الدهانات السعودية",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 200,
                "description": "دهان خطوط طرق أبيض عاكس",
                "image_url": "https://example.com/roadpaint.jpg"
            },
            {
                "id": "MAT-029",
                "name": "دهان خطوط طرق أصفر",
                "category": "مواد الطرق",
                "subcategory": "دهانات",
                "unit": "لتر",
                "price": 25,
                "supplier": "شركة الدهانات السعودية",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 200,
                "description": "دهان خطوط طرق أصفر عاكس",
                "image_url": "https://example.com/roadpaint2.jpg"
            },
            {
                "id": "MAT-030",
                "name": "حبيبات زجاجية عاكسة",
                "category": "مواد الطرق",
                "subcategory": "دهانات",
                "unit": "كجم",
                "price": 15,
                "supplier": "شركة الدهانات السعودية",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 100,
                "description": "حبيبات زجاجية عاكسة لدهانات الطرق",
                "image_url": "https://example.com/reflective.jpg"
            }
        ])
        
        # 4. مواد الصرف الصحي
        materials_data.extend([
            {
                "id": "MAT-031",
                "name": "أنابيب PVC قطر 110 مم",
                "category": "مواد الصرف الصحي",
                "subcategory": "أنابيب",
                "unit": "متر طولي",
                "price": 35,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "أنابيب PVC قطر 110 مم للصرف الصحي الداخلي",
                "image_url": "https://example.com/pvcpipe.jpg"
            },
            {
                "id": "MAT-032",
                "name": "أنابيب PVC قطر 160 مم",
                "category": "مواد الصرف الصحي",
                "subcategory": "أنابيب",
                "unit": "متر طولي",
                "price": 55,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "أنابيب PVC قطر 160 مم للصرف الصحي الخارجي",
                "image_url": "https://example.com/pvcpipe2.jpg"
            },
            {
                "id": "MAT-033",
                "name": "أنابيب UPVC قطر 200 مم",
                "category": "مواد الصرف الصحي",
                "subcategory": "أنابيب",
                "unit": "متر طولي",
                "price": 80,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 50,
                "description": "أنابيب UPVC قطر 200 مم للصرف الصحي الرئيسي",
                "image_url": "https://example.com/upvcpipe.jpg"
            },
            {
                "id": "MAT-034",
                "name": "أنابيب UPVC قطر 315 مم",
                "category": "مواد الصرف الصحي",
                "subcategory": "أنابيب",
                "unit": "متر طولي",
                "price": 150,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 50,
                "description": "أنابيب UPVC قطر 315 مم للصرف الصحي الرئيسي",
                "image_url": "https://example.com/upvcpipe2.jpg"
            },
            {
                "id": "MAT-035",
                "name": "أنابيب خرسانية مسلحة قطر 600 مم",
                "category": "مواد الصرف الصحي",
                "subcategory": "أنابيب",
                "unit": "متر طولي",
                "price": 450,
                "supplier": "مصنع الأنابيب الخرسانية",
                "origin": "محلي",
                "lead_time": 10,
                "min_order": 20,
                "description": "أنابيب خرسانية مسلحة قطر 600 مم للصرف الصحي الرئيسي",
                "image_url": "https://example.com/concretepipe.jpg"
            },
            {
                "id": "MAT-036",
                "name": "أنابيب خرسانية مسلحة قطر 1000 مم",
                "category": "مواد الصرف الصحي",
                "subcategory": "أنابيب",
                "unit": "متر طولي",
                "price": 850,
                "supplier": "مصنع الأنابيب الخرسانية",
                "origin": "محلي",
                "lead_time": 14,
                "min_order": 10,
                "description": "أنابيب خرسانية مسلحة قطر 1000 مم للصرف الصحي الرئيسي",
                "image_url": "https://example.com/concretepipe2.jpg"
            },
            {
                "id": "MAT-037",
                "name": "غرفة تفتيش خرسانية مسبقة الصب 80×80 سم",
                "category": "مواد الصرف الصحي",
                "subcategory": "غرف تفتيش",
                "unit": "قطعة",
                "price": 650,
                "supplier": "مصنع الخرسانة الجاهزة",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 5,
                "description": "غرفة تفتيش خرسانية مسبقة الصب 80×80 سم",
                "image_url": "https://example.com/manhole.jpg"
            },
            {
                "id": "MAT-038",
                "name": "غطاء غرفة تفتيش حديد زهر ثقيل",
                "category": "مواد الصرف الصحي",
                "subcategory": "غرف تفتيش",
                "unit": "قطعة",
                "price": 450,
                "supplier": "مصنع المسبوكات الحديدية",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 10,
                "description": "غطاء غرفة تفتيش حديد زهر ثقيل للطرق",
                "image_url": "https://example.com/manholecoverheavy.jpg"
            },
            {
                "id": "MAT-039",
                "name": "غطاء غرفة تفتيش حديد زهر خفيف",
                "category": "مواد الصرف الصحي",
                "subcategory": "غرف تفتيش",
                "unit": "قطعة",
                "price": 300,
                "supplier": "مصنع المسبوكات الحديدية",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 10,
                "description": "غطاء غرفة تفتيش حديد زهر خفيف للأرصفة",
                "image_url": "https://example.com/manholecoverlight.jpg"
            },
            {
                "id": "MAT-040",
                "name": "مصافي مطر حديد زهر",
                "category": "مواد الصرف الصحي",
                "subcategory": "مصافي",
                "unit": "قطعة",
                "price": 350,
                "supplier": "مصنع المسبوكات الحديدية",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 10,
                "description": "مصافي مطر حديد زهر للطرق",
                "image_url": "https://example.com/gully.jpg"
            }
        ])
        
        # 5. مواد العزل
        materials_data.extend([
            {
                "id": "MAT-041",
                "name": "رولات عزل مائي بيتوميني 4 مم",
                "category": "مواد العزل",
                "subcategory": "عزل مائي",
                "unit": "م2",
                "price": 25,
                "supplier": "شركة العزل السعودية",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 200,
                "description": "رولات عزل مائي بيتوميني 4 مم للأسطح",
                "image_url": "https://example.com/waterproofing.jpg"
            },
            {
                "id": "MAT-042",
                "name": "دهان عزل مائي أكريليك",
                "category": "مواد العزل",
                "subcategory": "عزل مائي",
                "unit": "لتر",
                "price": 18,
                "supplier": "شركة العزل السعودية",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "دهان عزل مائي أكريليك للأسطح",
                "image_url": "https://example.com/waterproofingpaint.jpg"
            },
            {
                "id": "MAT-043",
                "name": "مادة عزل مائي بوليمرية",
                "category": "مواد العزل",
                "subcategory": "عزل مائي",
                "unit": "كجم",
                "price": 35,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 50,
                "description": "مادة عزل مائي بوليمرية للحمامات والمطابخ",
                "image_url": "https://example.com/polymerwaterproofing.jpg"
            },
            {
                "id": "MAT-044",
                "name": "ألواح بوليسترين للعزل الحراري 5 سم",
                "category": "مواد العزل",
                "subcategory": "عزل حراري",
                "unit": "م2",
                "price": 20,
                "supplier": "شركة العزل السعودية",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "ألواح بوليسترين للعزل الحراري سماكة 5 سم",
                "image_url": "https://example.com/polystyrene.jpg"
            },
            {
                "id": "MAT-045",
                "name": "ألواح صوف صخري 5 سم",
                "category": "مواد العزل",
                "subcategory": "عزل حراري",
                "unit": "م2",
                "price": 35,
                "supplier": "شركة العزل السعودية",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 100,
                "description": "ألواح صوف صخري للعزل الحراري والصوتي سماكة 5 سم",
                "image_url": "https://example.com/rockwool.jpg"
            },
            {
                "id": "MAT-046",
                "name": "ألواح عزل صوتي 2 سم",
                "category": "مواد العزل",
                "subcategory": "عزل صوتي",
                "unit": "م2",
                "price": 45,
                "supplier": "شركة العزل السعودية",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 50,
                "description": "ألواح عزل صوتي سماكة 2 سم",
                "image_url": "https://example.com/acousticinsulation.jpg"
            },
            {
                "id": "MAT-047",
                "name": "شريط عزل مطاطي",
                "category": "مواد العزل",
                "subcategory": "عزل مائي",
                "unit": "متر طولي",
                "price": 15,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 100,
                "description": "شريط عزل مطاطي للفواصل الإنشائية",
                "image_url": "https://example.com/rubberstrip.jpg"
            },
            {
                "id": "MAT-048",
                "name": "مادة حشو فواصل بوليوريثان",
                "category": "مواد العزل",
                "subcategory": "عزل مائي",
                "unit": "لتر",
                "price": 40,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 20,
                "description": "مادة حشو فواصل بوليوريثان للفواصل الإنشائية",
                "image_url": "https://example.com/sealant.jpg"
            }
        ])
        
        # 6. مواد التشطيبات
        materials_data.extend([
            {
                "id": "MAT-049",
                "name": "بلاط سيراميك للأرضيات 60×60 سم",
                "category": "مواد التشطيبات",
                "subcategory": "بلاط",
                "unit": "م2",
                "price": 65,
                "supplier": "شركة السيراميك السعودية",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 100,
                "description": "بلاط سيراميك للأرضيات مقاس 60×60 سم",
                "image_url": "https://example.com/ceramictile.jpg"
            },
            {
                "id": "MAT-050",
                "name": "بلاط بورسلين للأرضيات 60×60 سم",
                "category": "مواد التشطيبات",
                "subcategory": "بلاط",
                "unit": "م2",
                "price": 85,
                "supplier": "شركة السيراميك السعودية",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 100,
                "description": "بلاط بورسلين للأرضيات مقاس 60×60 سم",
                "image_url": "https://example.com/porcelaintile.jpg"
            },
            {
                "id": "MAT-051",
                "name": "بلاط سيراميك للجدران 30×60 سم",
                "category": "مواد التشطيبات",
                "subcategory": "بلاط",
                "unit": "م2",
                "price": 60,
                "supplier": "شركة السيراميك السعودية",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 100,
                "description": "بلاط سيراميك للجدران مقاس 30×60 سم",
                "image_url": "https://example.com/walltile.jpg"
            },
            {
                "id": "MAT-052",
                "name": "رخام أبيض كرارة",
                "category": "مواد التشطيبات",
                "subcategory": "رخام",
                "unit": "م2",
                "price": 350,
                "supplier": "شركة الرخام السعودية",
                "origin": "مستورد",
                "lead_time": 14,
                "min_order": 20,
                "description": "رخام أبيض كرارة للأرضيات سماكة 2 سم",
                "image_url": "https://example.com/marble.jpg"
            },
            {
                "id": "MAT-053",
                "name": "جرانيت أسود",
                "category": "مواد التشطيبات",
                "subcategory": "جرانيت",
                "unit": "م2",
                "price": 450,
                "supplier": "شركة الرخام السعودية",
                "origin": "مستورد",
                "lead_time": 14,
                "min_order": 20,
                "description": "جرانيت أسود للأرضيات سماكة 2 سم",
                "image_url": "https://example.com/granite.jpg"
            },
            {
                "id": "MAT-054",
                "name": "دهان أساس للجدران الداخلية",
                "category": "مواد التشطيبات",
                "subcategory": "دهانات",
                "unit": "لتر",
                "price": 15,
                "supplier": "شركة الدهانات السعودية",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "دهان أساس للجدران الداخلية",
                "image_url": "https://example.com/primer.jpg"
            },
            {
                "id": "MAT-055",
                "name": "دهان بلاستيك للجدران الداخلية",
                "category": "مواد التشطيبات",
                "subcategory": "دهانات",
                "unit": "لتر",
                "price": 25,
                "supplier": "شركة الدهانات السعودية",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "دهان بلاستيك للجدران الداخلية",
                "image_url": "https://example.com/paint.jpg"
            },
            {
                "id": "MAT-056",
                "name": "دهان خارجي مقاوم للعوامل الجوية",
                "category": "مواد التشطيبات",
                "subcategory": "دهانات",
                "unit": "لتر",
                "price": 35,
                "supplier": "شركة الدهانات السعودية",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "دهان خارجي مقاوم للعوامل الجوية",
                "image_url": "https://example.com/exteriorpaint.jpg"
            },
            {
                "id": "MAT-057",
                "name": "ألواح جبس 12 مم",
                "category": "مواد التشطيبات",
                "subcategory": "جبس",
                "unit": "م2",
                "price": 18,
                "supplier": "شركة الجبس السعودية",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "ألواح جبس سماكة 12 مم للأسقف والجدران",
                "image_url": "https://example.com/gypsum.jpg"
            },
            {
                "id": "MAT-058",
                "name": "ألواح جبس مقاومة للرطوبة 12 مم",
                "category": "مواد التشطيبات",
                "subcategory": "جبس",
                "unit": "م2",
                "price": 25,
                "supplier": "شركة الجبس السعودية",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "ألواح جبس مقاومة للرطوبة سماكة 12 مم للحمامات والمطابخ",
                "image_url": "https://example.com/moistureresistantgypsum.jpg"
            }
        ])
        
        # 7. مواد كهربائية
        materials_data.extend([
            {
                "id": "MAT-059",
                "name": "كابل نحاس 1×10 مم2",
                "category": "مواد كهربائية",
                "subcategory": "كابلات",
                "unit": "متر طولي",
                "price": 15,
                "supplier": "الشركة السعودية للكابلات",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "كابل نحاس 1×10 مم2 للتمديدات الكهربائية",
                "image_url": "https://example.com/coppercable.jpg"
            },
            {
                "id": "MAT-060",
                "name": "كابل نحاس 1×6 مم2",
                "category": "مواد كهربائية",
                "subcategory": "كابلات",
                "unit": "متر طولي",
                "price": 10,
                "supplier": "الشركة السعودية للكابلات",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "كابل نحاس 1×6 مم2 للتمديدات الكهربائية",
                "image_url": "https://example.com/coppercable2.jpg"
            },
            {
                "id": "MAT-061",
                "name": "كابل نحاس 1×2.5 مم2",
                "category": "مواد كهربائية",
                "subcategory": "كابلات",
                "unit": "متر طولي",
                "price": 5,
                "supplier": "الشركة السعودية للكابلات",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "كابل نحاس 1×2.5 مم2 للتمديدات الكهربائية",
                "image_url": "https://example.com/coppercable3.jpg"
            },
            {
                "id": "MAT-062",
                "name": "كابل نحاس 1×1.5 مم2",
                "category": "مواد كهربائية",
                "subcategory": "كابلات",
                "unit": "متر طولي",
                "price": 3,
                "supplier": "الشركة السعودية للكابلات",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 100,
                "description": "كابل نحاس 1×1.5 مم2 للتمديدات الكهربائية",
                "image_url": "https://example.com/coppercable4.jpg"
            },
            {
                "id": "MAT-063",
                "name": "أنابيب بلاستيكية للتمديدات الكهربائية 20 مم",
                "category": "مواد كهربائية",
                "subcategory": "أنابيب",
                "unit": "متر طولي",
                "price": 3,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "أنابيب بلاستيكية للتمديدات الكهربائية قطر 20 مم",
                "image_url": "https://example.com/conduit.jpg"
            },
            {
                "id": "MAT-064",
                "name": "أنابيب بلاستيكية للتمديدات الكهربائية 25 مم",
                "category": "مواد كهربائية",
                "subcategory": "أنابيب",
                "unit": "متر طولي",
                "price": 4,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "أنابيب بلاستيكية للتمديدات الكهربائية قطر 25 مم",
                "image_url": "https://example.com/conduit2.jpg"
            },
            {
                "id": "MAT-065",
                "name": "علب كهربائية بلاستيكية",
                "category": "مواد كهربائية",
                "subcategory": "علب",
                "unit": "قطعة",
                "price": 2,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "علب كهربائية بلاستيكية للمفاتيح والبرايز",
                "image_url": "https://example.com/electricalbox.jpg"
            },
            {
                "id": "MAT-066",
                "name": "مفتاح إنارة مفرد",
                "category": "مواد كهربائية",
                "subcategory": "مفاتيح",
                "unit": "قطعة",
                "price": 15,
                "supplier": "شركة الأدوات الكهربائية",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 50,
                "description": "مفتاح إنارة مفرد",
                "image_url": "https://example.com/switch.jpg"
            },
            {
                "id": "MAT-067",
                "name": "مفتاح إنارة ثنائي",
                "category": "مواد كهربائية",
                "subcategory": "مفاتيح",
                "unit": "قطعة",
                "price": 20,
                "supplier": "شركة الأدوات الكهربائية",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 50,
                "description": "مفتاح إنارة ثنائي",
                "image_url": "https://example.com/switch2.jpg"
            },
            {
                "id": "MAT-068",
                "name": "بريزة كهربائية",
                "category": "مواد كهربائية",
                "subcategory": "برايز",
                "unit": "قطعة",
                "price": 15,
                "supplier": "شركة الأدوات الكهربائية",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 50,
                "description": "بريزة كهربائية",
                "image_url": "https://example.com/socket.jpg"
            }
        ])
        
        # 8. مواد ميكانيكية
        materials_data.extend([
            {
                "id": "MAT-069",
                "name": "أنابيب مياه PPR قطر 20 مم",
                "category": "مواد ميكانيكية",
                "subcategory": "أنابيب مياه",
                "unit": "متر طولي",
                "price": 8,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "أنابيب مياه PPR قطر 20 مم",
                "image_url": "https://example.com/pprpipe.jpg"
            },
            {
                "id": "MAT-070",
                "name": "أنابيب مياه PPR قطر 25 مم",
                "category": "مواد ميكانيكية",
                "subcategory": "أنابيب مياه",
                "unit": "متر طولي",
                "price": 12,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "أنابيب مياه PPR قطر 25 مم",
                "image_url": "https://example.com/pprpipe2.jpg"
            },
            {
                "id": "MAT-071",
                "name": "أنابيب مياه PPR قطر 32 مم",
                "category": "مواد ميكانيكية",
                "subcategory": "أنابيب مياه",
                "unit": "متر طولي",
                "price": 18,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "أنابيب مياه PPR قطر 32 مم",
                "image_url": "https://example.com/pprpipe3.jpg"
            },
            {
                "id": "MAT-072",
                "name": "أنابيب حديد مجلفن قطر 2 بوصة",
                "category": "مواد ميكانيكية",
                "subcategory": "أنابيب حريق",
                "unit": "متر طولي",
                "price": 65,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 50,
                "description": "أنابيب حديد مجلفن قطر 2 بوصة لأنظمة مكافحة الحريق",
                "image_url": "https://example.com/galvanizedpipe.jpg"
            },
            {
                "id": "MAT-073",
                "name": "أنابيب حديد مجلفن قطر 4 بوصة",
                "category": "مواد ميكانيكية",
                "subcategory": "أنابيب حريق",
                "unit": "متر طولي",
                "price": 120,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 50,
                "description": "أنابيب حديد مجلفن قطر 4 بوصة لأنظمة مكافحة الحريق",
                "image_url": "https://example.com/galvanizedpipe2.jpg"
            },
            {
                "id": "MAT-074",
                "name": "أنابيب نحاس قطر 1/2 بوصة",
                "category": "مواد ميكانيكية",
                "subcategory": "أنابيب تكييف",
                "unit": "متر طولي",
                "price": 45,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 50,
                "description": "أنابيب نحاس قطر 1/2 بوصة لأنظمة التكييف",
                "image_url": "https://example.com/copperpipe.jpg"
            },
            {
                "id": "MAT-075",
                "name": "أنابيب نحاس قطر 3/4 بوصة",
                "category": "مواد ميكانيكية",
                "subcategory": "أنابيب تكييف",
                "unit": "متر طولي",
                "price": 65,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 50,
                "description": "أنابيب نحاس قطر 3/4 بوصة لأنظمة التكييف",
                "image_url": "https://example.com/copperpipe2.jpg"
            },
            {
                "id": "MAT-076",
                "name": "مضخة مياه 1 حصان",
                "category": "مواد ميكانيكية",
                "subcategory": "مضخات",
                "unit": "قطعة",
                "price": 850,
                "supplier": "شركة المضخات السعودية",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 2,
                "description": "مضخة مياه 1 حصان",
                "image_url": "https://example.com/waterpump.jpg"
            },
            {
                "id": "MAT-077",
                "name": "مضخة مياه 2 حصان",
                "category": "مواد ميكانيكية",
                "subcategory": "مضخات",
                "unit": "قطعة",
                "price": 1200,
                "supplier": "شركة المضخات السعودية",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 2,
                "description": "مضخة مياه 2 حصان",
                "image_url": "https://example.com/waterpump2.jpg"
            },
            {
                "id": "MAT-078",
                "name": "خزان مياه بلاستيكي 1000 لتر",
                "category": "مواد ميكانيكية",
                "subcategory": "خزانات",
                "unit": "قطعة",
                "price": 650,
                "supplier": "شركة الخزانات السعودية",
                "origin": "محلي",
                "lead_time": 5,
                "min_order": 2,
                "description": "خزان مياه بلاستيكي سعة 1000 لتر",
                "image_url": "https://example.com/watertank.jpg"
            }
        ])
        
        # 9. مواد الري والزراعة
        materials_data.extend([
            {
                "id": "MAT-079",
                "name": "أنابيب بولي إيثيلين قطر 32 مم",
                "category": "مواد الري والزراعة",
                "subcategory": "أنابيب ري",
                "unit": "متر طولي",
                "price": 8,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "أنابيب بولي إيثيلين قطر 32 مم لأنظمة الري",
                "image_url": "https://example.com/pepipe.jpg"
            },
            {
                "id": "MAT-080",
                "name": "أنابيب بولي إيثيلين قطر 63 مم",
                "category": "مواد الري والزراعة",
                "subcategory": "أنابيب ري",
                "unit": "متر طولي",
                "price": 15,
                "supplier": "الشركة السعودية للأنابيب",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 100,
                "description": "أنابيب بولي إيثيلين قطر 63 مم لأنظمة الري",
                "image_url": "https://example.com/pepipe2.jpg"
            },
            {
                "id": "MAT-081",
                "name": "نقاطات ري 4 لتر/ساعة",
                "category": "مواد الري والزراعة",
                "subcategory": "نقاطات",
                "unit": "قطعة",
                "price": 1,
                "supplier": "شركة أنظمة الري",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 1000,
                "description": "نقاطات ري 4 لتر/ساعة",
                "image_url": "https://example.com/dripper.jpg"
            },
            {
                "id": "MAT-082",
                "name": "نقاطات ري 8 لتر/ساعة",
                "category": "مواد الري والزراعة",
                "subcategory": "نقاطات",
                "unit": "قطعة",
                "price": 1.2,
                "supplier": "شركة أنظمة الري",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 1000,
                "description": "نقاطات ري 8 لتر/ساعة",
                "image_url": "https://example.com/dripper2.jpg"
            },
            {
                "id": "MAT-083",
                "name": "رشاشات ري دوارة",
                "category": "مواد الري والزراعة",
                "subcategory": "رشاشات",
                "unit": "قطعة",
                "price": 25,
                "supplier": "شركة أنظمة الري",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 100,
                "description": "رشاشات ري دوارة للمسطحات الخضراء",
                "image_url": "https://example.com/sprinkler.jpg"
            },
            {
                "id": "MAT-084",
                "name": "محابس بلاستيكية قطر 32 مم",
                "category": "مواد الري والزراعة",
                "subcategory": "محابس",
                "unit": "قطعة",
                "price": 15,
                "supplier": "شركة أنظمة الري",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 50,
                "description": "محابس بلاستيكية قطر 32 مم لأنظمة الري",
                "image_url": "https://example.com/valve.jpg"
            },
            {
                "id": "MAT-085",
                "name": "محابس بلاستيكية قطر 63 مم",
                "category": "مواد الري والزراعة",
                "subcategory": "محابس",
                "unit": "قطعة",
                "price": 35,
                "supplier": "شركة أنظمة الري",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 50,
                "description": "محابس بلاستيكية قطر 63 مم لأنظمة الري",
                "image_url": "https://example.com/valve2.jpg"
            },
            {
                "id": "MAT-086",
                "name": "وحدة تحكم ري 6 محطات",
                "category": "مواد الري والزراعة",
                "subcategory": "وحدات تحكم",
                "unit": "قطعة",
                "price": 450,
                "supplier": "شركة أنظمة الري",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 5,
                "description": "وحدة تحكم ري 6 محطات",
                "image_url": "https://example.com/controller.jpg"
            },
            {
                "id": "MAT-087",
                "name": "وحدة تحكم ري 12 محطة",
                "category": "مواد الري والزراعة",
                "subcategory": "وحدات تحكم",
                "unit": "قطعة",
                "price": 750,
                "supplier": "شركة أنظمة الري",
                "origin": "مستورد",
                "lead_time": 10,
                "min_order": 5,
                "description": "وحدة تحكم ري 12 محطة",
                "image_url": "https://example.com/controller2.jpg"
            },
            {
                "id": "MAT-088",
                "name": "تربة زراعية",
                "category": "مواد الري والزراعة",
                "subcategory": "تربة",
                "unit": "م3",
                "price": 120,
                "supplier": "شركة المواد الزراعية",
                "origin": "محلي",
                "lead_time": 2,
                "min_order": 10,
                "description": "تربة زراعية للزراعة",
                "image_url": "https://example.com/soil.jpg"
            }
        ])
        
        # 10. مواد متنوعة
        materials_data.extend([
            {
                "id": "MAT-089",
                "name": "أسلاك تربيط حديد التسليح",
                "category": "مواد متنوعة",
                "subcategory": "أسلاك",
                "unit": "كجم",
                "price": 12,
                "supplier": "شركة حديد الراجحي",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 50,
                "description": "أسلاك تربيط حديد التسليح",
                "image_url": "https://example.com/bindingwire.jpg"
            },
            {
                "id": "MAT-090",
                "name": "مسامير متنوعة",
                "category": "مواد متنوعة",
                "subcategory": "مسامير",
                "unit": "كجم",
                "price": 15,
                "supplier": "شركة الأدوات",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 20,
                "description": "مسامير متنوعة للأعمال الإنشائية",
                "image_url": "https://example.com/nails.jpg"
            },
            {
                "id": "MAT-091",
                "name": "شدات معدنية",
                "category": "مواد متنوعة",
                "subcategory": "شدات",
                "unit": "م2",
                "price": 120,
                "supplier": "شركة معدات البناء",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 50,
                "description": "شدات معدنية للأعمال الخرسانية",
                "image_url": "https://example.com/formwork.jpg"
            },
            {
                "id": "MAT-092",
                "name": "سقالات معدنية",
                "category": "مواد متنوعة",
                "subcategory": "سقالات",
                "unit": "م2",
                "price": 85,
                "supplier": "شركة معدات البناء",
                "origin": "محلي",
                "lead_time": 7,
                "min_order": 50,
                "description": "سقالات معدنية للأعمال الإنشائية",
                "image_url": "https://example.com/scaffold.jpg"
            },
            {
                "id": "MAT-093",
                "name": "خشب أبلكاش 18 مم",
                "category": "مواد متنوعة",
                "subcategory": "خشب",
                "unit": "م2",
                "price": 65,
                "supplier": "شركة الأخشاب",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 20,
                "description": "خشب أبلكاش سماكة 18 مم للشدات الخشبية",
                "image_url": "https://example.com/plywood.jpg"
            },
            {
                "id": "MAT-094",
                "name": "عوارض خشبية 10×10 سم",
                "category": "مواد متنوعة",
                "subcategory": "خشب",
                "unit": "متر طولي",
                "price": 25,
                "supplier": "شركة الأخشاب",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 50,
                "description": "عوارض خشبية 10×10 سم للشدات الخشبية",
                "image_url": "https://example.com/timber.jpg"
            },
            {
                "id": "MAT-095",
                "name": "مواد لاصقة للبلاط",
                "category": "مواد متنوعة",
                "subcategory": "مواد لاصقة",
                "unit": "كجم",
                "price": 2.5,
                "supplier": "شركة مواد البناء",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 500,
                "description": "مواد لاصقة للبلاط",
                "image_url": "https://example.com/tileadhesive.jpg"
            },
            {
                "id": "MAT-096",
                "name": "روبة للبلاط",
                "category": "مواد متنوعة",
                "subcategory": "مواد لاصقة",
                "unit": "كجم",
                "price": 3,
                "supplier": "شركة مواد البناء",
                "origin": "محلي",
                "lead_time": 3,
                "min_order": 200,
                "description": "روبة للبلاط",
                "image_url": "https://example.com/grout.jpg"
            },
            {
                "id": "MAT-097",
                "name": "مواد معالجة الخرسانة",
                "category": "مواد متنوعة",
                "subcategory": "مواد معالجة",
                "unit": "لتر",
                "price": 12,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 100,
                "description": "مواد معالجة الخرسانة",
                "image_url": "https://example.com/curing.jpg"
            },
            {
                "id": "MAT-098",
                "name": "مواد إصلاح الخرسانة",
                "category": "مواد متنوعة",
                "subcategory": "مواد معالجة",
                "unit": "كجم",
                "price": 18,
                "supplier": "سيكا",
                "origin": "مستورد",
                "lead_time": 7,
                "min_order": 50,
                "description": "مواد إصلاح الخرسانة",
                "image_url": "https://example.com/repair.jpg"
            }
        ])
        
        # تخزين البيانات في حالة الجلسة
        st.session_state.materials_catalog = pd.DataFrame(materials_data)
    
    def render(self):
        """عرض واجهة كتالوج المواد"""
        
        st.markdown("## كتالوج المواد")
        
        # إنشاء تبويبات لعرض الكتالوج
        tabs = st.tabs([
            "عرض الكتالوج", 
            "إضافة مادة", 
            "تحليل الأسعار",
            "استيراد/تصدير"
        ])
        
        with tabs[0]:
            self._render_catalog_view_tab()
        
        with tabs[1]:
            self._render_add_material_tab()
        
        with tabs[2]:
            self._render_price_analysis_tab()
        
        with tabs[3]:
            self._render_import_export_tab()
    
    def _render_catalog_view_tab(self):
        """عرض تبويب عرض الكتالوج"""
        
        st.markdown("### عرض كتالوج المواد")
        
        # استخراج البيانات
        materials_df = st.session_state.materials_catalog
        
        # إنشاء فلاتر للعرض
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # فلتر حسب الفئة
            categories = ["الكل"] + sorted(materials_df["category"].unique().tolist())
            selected_category = st.selectbox("اختر فئة المواد", categories)
        
        with col2:
            # فلتر حسب الفئة الفرعية
            if selected_category != "الكل":
                subcategories = ["الكل"] + sorted(materials_df[materials_df["category"] == selected_category]["subcategory"].unique().tolist())
            else:
                subcategories = ["الكل"] + sorted(materials_df["subcategory"].unique().tolist())
            
            selected_subcategory = st.selectbox("اختر الفئة الفرعية", subcategories)
        
        with col3:
            # فلتر حسب المورد
            suppliers = ["الكل"] + sorted(materials_df["supplier"].unique().tolist())
            selected_supplier = st.selectbox("اختر المورد", suppliers)
        
        # تطبيق الفلاتر
        filtered_df = materials_df.copy()
        
        if selected_category != "الكل":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]
        
        if selected_subcategory != "الكل":
            filtered_df = filtered_df[filtered_df["subcategory"] == selected_subcategory]
        
        if selected_supplier != "الكل":
            filtered_df = filtered_df[filtered_df["supplier"] == selected_supplier]
        
        # عرض البيانات
        if not filtered_df.empty:
            # عرض عدد النتائج
            st.info(f"تم العثور على {len(filtered_df)} مادة")
            
            # عرض المواد في شكل بطاقات
            for i, (_, material) in enumerate(filtered_df.iterrows()):
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    # عرض صورة المادة (استخدام صورة افتراضية)
                    st.image("https://via.placeholder.com/150", caption=material["name"])
                
                with col2:
                    # عرض معلومات المادة
                    st.markdown(f"**{material['name']}** (الكود: {material['id']})")
                    st.markdown(f"الفئة: {material['category']} - {material['subcategory']}")
                    st.markdown(f"الوحدة: {material['unit']} | السعر: {material['price']} ريال/{material['unit']}")
                    st.markdown(f"المورد: {material['supplier']} | المنشأ: {material['origin']}")
                    st.markdown(f"مدة التوريد: {material['lead_time']} يوم | الحد الأدنى للطلب: {material['min_order']} {material['unit']}")
                
                # إضافة زر لعرض التفاصيل
                if st.button(f"عرض التفاصيل الكاملة", key=f"details_{material['id']}"):
                    st.session_state.selected_material = material['id']
                    self._show_material_details(material)
                
                st.markdown("---")
        else:
            st.warning("لا توجد مواد تطابق معايير البحث")
    
    def _show_material_details(self, material):
        """عرض تفاصيل المادة"""
        
        st.markdown(f"## تفاصيل المادة: {material['name']}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # عرض صورة المادة (استخدام صورة افتراضية)
            st.image("https://via.placeholder.com/300", caption=material["name"])
        
        with col2:
            # عرض المعلومات الأساسية
            st.markdown("### المعلومات الأساسية")
            st.markdown(f"**الكود:** {material['id']}")
            st.markdown(f"**الفئة:** {material['category']} - {material['subcategory']}")
            st.markdown(f"**الوحدة:** {material['unit']}")
            st.markdown(f"**السعر:** {material['price']} ريال/{material['unit']}")
            st.markdown(f"**المورد:** {material['supplier']}")
            st.markdown(f"**المنشأ:** {material['origin']}")
            st.markdown(f"**مدة التوريد:** {material['lead_time']} يوم")
            st.markdown(f"**الحد الأدنى للطلب:** {material['min_order']} {material['unit']}")
            st.markdown(f"**الوصف:** {material['description']}")
        
        # إضافة زر للتعديل
        if st.button("تعديل بيانات المادة"):
            st.session_state.edit_material = material['id']
            # هنا يمكن إضافة منطق التعديل
    
    def _render_add_material_tab(self):
        """عرض تبويب إضافة مادة"""
        
        st.markdown("### إضافة مادة جديدة")
        
        # استخراج البيانات
        materials_df = st.session_state.materials_catalog
        
        # إنشاء نموذج إضافة مادة
        with st.form("add_material_form"):
            st.markdown("#### المعلومات الأساسية")
            
            # الصف الأول
            col1, col2 = st.columns(2)
            with col1:
                material_id = st.text_input("كود المادة", value=f"MAT-{len(materials_df) + 1:03d}")
                material_name = st.text_input("اسم المادة", placeholder="مثال: أسمنت بورتلاندي عادي")
            
            with col2:
                # استخراج الفئات والفئات الفرعية الموجودة
                categories = sorted(materials_df["category"].unique().tolist())
                material_category = st.selectbox("فئة المادة", categories)
                
                # استخراج الفئات الفرعية بناءً على الفئة المختارة
                subcategories = sorted(materials_df[materials_df["category"] == material_category]["subcategory"].unique().tolist())
                material_subcategory = st.selectbox("الفئة الفرعية", subcategories)
            
            # الصف الثاني
            col1, col2, col3 = st.columns(3)
            with col1:
                material_unit = st.text_input("وحدة القياس", placeholder="مثال: م3، طن، قطعة")
            with col2:
                material_price = st.number_input("السعر (ريال)", min_value=0.0, step=0.5)
            with col3:
                material_min_order = st.number_input("الحد الأدنى للطلب", min_value=1, step=1)
            
            # الصف الثالث
            col1, col2, col3 = st.columns(3)
            with col1:
                material_supplier = st.text_input("المورد", placeholder="مثال: شركة الإسمنت السعودية")
            with col2:
                material_origin = st.selectbox("المنشأ", ["محلي", "مستورد"])
            with col3:
                material_lead_time = st.number_input("مدة التوريد (يوم)", min_value=1, step=1)
            
            # وصف المادة
            material_description = st.text_area("وصف المادة", placeholder="أدخل وصفاً تفصيلياً للمادة")
            
            # رابط الصورة
            material_image_url = st.text_input("رابط الصورة", placeholder="مثال: https://example.com/image.jpg")
            
            # زر الإضافة
            submit_button = st.form_submit_button("إضافة المادة")
            
            if submit_button:
                # التحقق من البيانات
                if not material_name or not material_category or not material_subcategory or not material_unit:
                    st.error("يرجى إدخال المعلومات الأساسية للمادة")
                else:
                    # إنشاء مادة جديدة
                    new_material = {
                        "id": material_id,
                        "name": material_name,
                        "category": material_category,
                        "subcategory": material_subcategory,
                        "unit": material_unit,
                        "price": material_price,
                        "supplier": material_supplier,
                        "origin": material_origin,
                        "lead_time": material_lead_time,
                        "min_order": material_min_order,
                        "description": material_description,
                        "image_url": material_image_url if material_image_url else "https://via.placeholder.com/150"
                    }
                    
                    # إضافة المادة إلى الكتالوج
                    st.session_state.materials_catalog = pd.concat([
                        st.session_state.materials_catalog,
                        pd.DataFrame([new_material])
                    ], ignore_index=True)
                    
                    st.success(f"تمت إضافة المادة {material_name} بنجاح!")
    
    def _render_price_analysis_tab(self):
        """عرض تبويب تحليل الأسعار"""
        
        st.markdown("### تحليل أسعار المواد")
        
        # استخراج البيانات
        materials_df = st.session_state.materials_catalog
        
        # تحليل متوسط الأسعار حسب الفئة
        st.markdown("#### متوسط الأسعار حسب الفئة")
        
        # حساب متوسط الأسعار لكل فئة
        category_prices = materials_df.groupby("category").agg({
            "price": "mean"
        }).reset_index()
        
        # تغيير أسماء الأعمدة
        category_prices.columns = ["الفئة", "متوسط السعر"]
        
        # عرض الجدول
        st.dataframe(category_prices, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة
        st.markdown("#### مقارنة متوسط الأسعار حسب الفئة")
        
        fig = px.bar(
            category_prices,
            x="الفئة",
            y="متوسط السعر",
            title="متوسط أسعار المواد حسب الفئة",
            color="الفئة",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل توزيع المواد حسب المنشأ
        st.markdown("#### توزيع المواد حسب المنشأ")
        
        # حساب عدد المواد حسب المنشأ
        origin_counts = materials_df["origin"].value_counts().reset_index()
        origin_counts.columns = ["المنشأ", "عدد المواد"]
        
        # إنشاء رسم بياني دائري
        fig = px.pie(
            origin_counts,
            values="عدد المواد",
            names="المنشأ",
            title="توزيع المواد حسب المنشأ",
            color="المنشأ"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل مدة التوريد
        st.markdown("#### تحليل مدة التوريد")
        
        # حساب متوسط مدة التوريد حسب المنشأ
        lead_time_by_origin = materials_df.groupby("origin").agg({
            "lead_time": "mean"
        }).reset_index()
        
        # تغيير أسماء الأعمدة
        lead_time_by_origin.columns = ["المنشأ", "متوسط مدة التوريد (يوم)"]
        
        # عرض الجدول
        st.dataframe(lead_time_by_origin, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة
        fig = px.bar(
            lead_time_by_origin,
            x="المنشأ",
            y="متوسط مدة التوريد (يوم)",
            title="متوسط مدة التوريد حسب المنشأ",
            color="المنشأ",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # حاسبة تكاليف المشروع
        st.markdown("#### حاسبة تكاليف المشروع")
        
        with st.form("project_cost_calculator"):
            st.markdown("أدخل المواد المطلوبة للمشروع")
            
            # اختيار المواد
            selected_materials = st.multiselect(
                "اختر المواد",
                options=materials_df["name"].tolist(),
                format_func=lambda x: f"{x} ({materials_df[materials_df['name'] == x]['id'].iloc[0]})"
            )
            
            # إنشاء حقول إدخال الكميات
            quantities = {}
            
            if selected_materials:
                st.markdown("أدخل الكميات المطلوبة")
                
                for material_name in selected_materials:
                    material = materials_df[materials_df["name"] == material_name].iloc[0]
                    quantities[material_name] = st.number_input(
                        f"{material_name} ({material['unit']})",
                        min_value=0.0,
                        step=0.5,
                        key=f"qty_{material['id']}"
                    )
            
            # زر الحساب
            calculate_button = st.form_submit_button("حساب التكاليف")
            
            if calculate_button:
                if not selected_materials:
                    st.error("يرجى اختيار مادة واحدة على الأقل")
                else:
                    # حساب التكاليف
                    project_costs = []
                    
                    for material_name in selected_materials:
                        material = materials_df[materials_df["name"] == material_name].iloc[0]
                        quantity = quantities[material_name]
                        
                        if quantity > 0:
                            cost = material["price"] * quantity
                            
                            project_costs.append({
                                "المادة": material_name,
                                "الكود": material["id"],
                                "الوحدة": material["unit"],
                                "الكمية": quantity,
                                "سعر الوحدة": material["price"],
                                "التكلفة الإجمالية": cost
                            })
                    
                    if project_costs:
                        # عرض النتائج
                        project_costs_df = pd.DataFrame(project_costs)
                        st.dataframe(project_costs_df, use_container_width=True)
                        
                        # حساب إجمالي التكاليف
                        total_cost = project_costs_df["التكلفة الإجمالية"].sum()
                        st.metric("إجمالي تكاليف المواد للمشروع", f"{total_cost:,.2f} ريال")
                    else:
                        st.warning("يرجى إدخال كميات أكبر من صفر")
    
    def _render_import_export_tab(self):
        """عرض تبويب استيراد/تصدير"""
        
        st.markdown("### استيراد وتصدير بيانات المواد")
        
        # استيراد البيانات
        st.markdown("#### استيراد البيانات")
        
        uploaded_file = st.file_uploader("اختر ملف Excel لاستيراد بيانات المواد", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                # قراءة الملف
                imported_df = pd.read_excel(uploaded_file)
                
                # عرض البيانات المستوردة
                st.dataframe(imported_df, use_container_width=True)
                
                # زر الاستيراد
                if st.button("استيراد البيانات"):
                    # التحقق من وجود الأعمدة المطلوبة
                    required_columns = ["id", "name", "category", "subcategory", "unit", "price"]
                    
                    if all(col in imported_df.columns for col in required_columns):
                        # دمج البيانات المستوردة مع البيانات الحالية
                        st.session_state.materials_catalog = pd.concat([
                            st.session_state.materials_catalog,
                            imported_df
                        ], ignore_index=True).drop_duplicates(subset=["id"])
                        
                        st.success(f"تم استيراد {len(imported_df)} مادة بنجاح!")
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
            materials_df = st.session_state.materials_catalog
            
            # تصدير البيانات حسب التنسيق المختار
            if export_format == "Excel":
                # تصدير إلى Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    materials_df.to_excel(writer, index=False, sheet_name="Materials")
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف Excel",
                    data=output.getvalue(),
                    file_name="materials_catalog.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            elif export_format == "CSV":
                # تصدير إلى CSV
                csv_data = materials_df.to_csv(index=False)
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف CSV",
                    data=csv_data,
                    file_name="materials_catalog.csv",
                    mime="text/csv"
                )
            
            else:  # JSON
                # تصدير إلى JSON
                json_data = materials_df.to_json(orient="records", force_ascii=False)
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف JSON",
                    data=json_data,
                    file_name="materials_catalog.json",
                    mime="application/json"
                )
    
    def get_material_by_id(self, material_id):
        """الحصول على مادة بواسطة الكود"""
        
        materials_df = st.session_state.materials_catalog
        material = materials_df[materials_df["id"] == material_id]
        
        if not material.empty:
            return material.iloc[0].to_dict()
        
        return None
    
    def get_materials_by_category(self, category):
        """الحصول على المواد حسب الفئة"""
        
        materials_df = st.session_state.materials_catalog
        materials = materials_df[materials_df["category"] == category]
        
        if not materials.empty:
            return materials.to_dict(orient="records")
        
        return []
    
    def calculate_material_cost(self, material_id, quantity):
        """حساب تكلفة المادة بناءً على الكمية"""
        
        material = self.get_material_by_id(material_id)
        
        if material:
            return material["price"] * quantity
        
        return 0
