"""
كتالوج مقاولي الباطن - وحدة إدارة مقاولي الباطن
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import json
from datetime import datetime
import io

class SubcontractorsCatalog:
    """كتالوج مقاولي الباطن"""
    
    def __init__(self):
        """تهيئة كتالوج مقاولي الباطن"""
        
        # تهيئة حالة الجلسة لكتالوج مقاولي الباطن
        if 'subcontractors_catalog' not in st.session_state:
            # إنشاء بيانات افتراضية لمقاولي الباطن
            self._initialize_subcontractors_catalog()
    
    def _initialize_subcontractors_catalog(self):
        """تهيئة بيانات كتالوج مقاولي الباطن"""
        
        # تعريف فئات مقاولي الباطن
        subcontractor_categories = [
            "أعمال الكهرباء",
            "أعمال ITC",
            "أعمال CCTV",
            "أنظمة التحكم في الوصول",
            "شبكات الري",
            "أعمال الصرف الصحي",
            "أعمال الطرق",
            "أعمال الجسور",
            "أعمال الحفر والردم",
            "أعمال الخرسانة"
        ]
        
        # إنشاء قائمة مقاولي الباطن
        subcontractors_data = []
        
        # 1. أعمال الكهرباء
        subcontractors_data.extend([
            {
                "id": "ELEC-001",
                "name": "شركة الأنظمة الكهربائية المتكاملة",
                "category": "أعمال الكهرباء",
                "subcategory": "تمديدات كهربائية",
                "contact_person": "م. خالد العتيبي",
                "phone": "0555123456",
                "email": "khalid@ies-sa.com",
                "address": "الرياض - حي العليا",
                "classification": "درجة أولى",
                "experience_years": 15,
                "completed_projects": 120,
                "ongoing_projects": 8,
                "min_project_value": 500000,
                "max_project_value": 50000000,
                "specialties": "تمديدات كهربائية، محطات توزيع، لوحات توزيع، أنظمة إنارة",
                "rating": 4.8,
                "description": "شركة متخصصة في تنفيذ أعمال التمديدات الكهربائية ومحطات التوزيع واللوحات الكهربائية وأنظمة الإنارة للمشاريع الكبرى"
            },
            {
                "id": "ELEC-002",
                "name": "مؤسسة النور للمقاولات الكهربائية",
                "category": "أعمال الكهرباء",
                "subcategory": "إنارة طرق",
                "contact_person": "م. سعد القحطاني",
                "phone": "0555234567",
                "email": "saad@alnoor-elec.com",
                "address": "جدة - حي الروضة",
                "classification": "درجة ثانية",
                "experience_years": 10,
                "completed_projects": 75,
                "ongoing_projects": 5,
                "min_project_value": 200000,
                "max_project_value": 20000000,
                "specialties": "إنارة طرق، إنارة ميادين، إنارة حدائق، أنظمة تحكم",
                "rating": 4.5,
                "description": "مؤسسة متخصصة في تنفيذ أعمال إنارة الطرق والميادين والحدائق وأنظمة التحكم في الإنارة"
            },
            {
                "id": "ELEC-003",
                "name": "شركة الطاقة للمقاولات الكهربائية",
                "category": "أعمال الكهرباء",
                "subcategory": "محطات كهربائية",
                "contact_person": "م. فهد الشمري",
                "phone": "0555345678",
                "email": "fahad@energy-sa.com",
                "address": "الدمام - حي الفيصلية",
                "classification": "درجة أولى",
                "experience_years": 18,
                "completed_projects": 150,
                "ongoing_projects": 10,
                "min_project_value": 1000000,
                "max_project_value": 100000000,
                "specialties": "محطات توزيع، محطات تحويل، خطوط نقل، أنظمة حماية",
                "rating": 4.9,
                "description": "شركة متخصصة في تنفيذ أعمال محطات التوزيع والتحويل وخطوط النقل وأنظمة الحماية الكهربائية"
            }
        ])
        
        # 2. أعمال ITC
        subcontractors_data.extend([
            {
                "id": "ITC-001",
                "name": "شركة التقنية المتكاملة للاتصالات",
                "category": "أعمال ITC",
                "subcategory": "شبكات اتصالات",
                "contact_person": "م. محمد العمري",
                "phone": "0555456789",
                "email": "mohammed@itc-sa.com",
                "address": "الرياض - حي الملز",
                "classification": "درجة أولى",
                "experience_years": 12,
                "completed_projects": 90,
                "ongoing_projects": 7,
                "min_project_value": 500000,
                "max_project_value": 40000000,
                "specialties": "شبكات اتصالات، أنظمة مراقبة، أنظمة صوتية، شبكات ألياف ضوئية",
                "rating": 4.7,
                "description": "شركة متخصصة في تنفيذ أعمال شبكات الاتصالات وأنظمة المراقبة والأنظمة الصوتية وشبكات الألياف الضوئية"
            },
            {
                "id": "ITC-002",
                "name": "مؤسسة الاتصالات المتقدمة",
                "category": "أعمال ITC",
                "subcategory": "أنظمة معلومات",
                "contact_person": "م. عبدالله الزهراني",
                "phone": "0555567890",
                "email": "abdullah@advanced-comm.com",
                "address": "جدة - حي السلامة",
                "classification": "درجة ثانية",
                "experience_years": 8,
                "completed_projects": 60,
                "ongoing_projects": 4,
                "min_project_value": 200000,
                "max_project_value": 15000000,
                "specialties": "أنظمة معلومات، شبكات داخلية، أنظمة تخزين، أنظمة حماية",
                "rating": 4.4,
                "description": "مؤسسة متخصصة في تنفيذ أعمال أنظمة المعلومات والشبكات الداخلية وأنظمة التخزين وأنظمة الحماية"
            },
            {
                "id": "ITC-003",
                "name": "شركة البيانات للاتصالات وتقنية المعلومات",
                "category": "أعمال ITC",
                "subcategory": "بنية تحتية للاتصالات",
                "contact_person": "م. سلطان المالكي",
                "phone": "0555678901",
                "email": "sultan@data-sa.com",
                "address": "الدمام - حي الشاطئ",
                "classification": "درجة أولى",
                "experience_years": 15,
                "completed_projects": 110,
                "ongoing_projects": 9,
                "min_project_value": 800000,
                "max_project_value": 60000000,
                "specialties": "بنية تحتية للاتصالات، أبراج اتصالات، محطات إرسال، شبكات ألياف ضوئية",
                "rating": 4.8,
                "description": "شركة متخصصة في تنفيذ أعمال البنية التحتية للاتصالات وأبراج الاتصالات ومحطات الإرسال وشبكات الألياف الضوئية"
            }
        ])
        
        # 3. أعمال CCTV
        subcontractors_data.extend([
            {
                "id": "CCTV-001",
                "name": "شركة الأمان لأنظمة المراقبة",
                "category": "أعمال CCTV",
                "subcategory": "أنظمة مراقبة",
                "contact_person": "م. ناصر الحربي",
                "phone": "0555789012",
                "email": "nasser@security-sa.com",
                "address": "الرياض - حي النزهة",
                "classification": "درجة ثانية",
                "experience_years": 10,
                "completed_projects": 85,
                "ongoing_projects": 6,
                "min_project_value": 100000,
                "max_project_value": 10000000,
                "specialties": "أنظمة مراقبة، كاميرات أمنية، أنظمة تسجيل، أنظمة تحكم",
                "rating": 4.6,
                "description": "شركة متخصصة في تنفيذ أعمال أنظمة المراقبة والكاميرات الأمنية وأنظمة التسجيل وأنظمة التحكم"
            },
            {
                "id": "CCTV-002",
                "name": "مؤسسة الحماية للأنظمة الأمنية",
                "category": "أعمال CCTV",
                "subcategory": "أنظمة أمنية",
                "contact_person": "م. سعيد الغامدي",
                "phone": "0555890123",
                "email": "saeed@protection-sa.com",
                "address": "جدة - حي الصفا",
                "classification": "درجة ثالثة",
                "experience_years": 7,
                "completed_projects": 50,
                "ongoing_projects": 3,
                "min_project_value": 50000,
                "max_project_value": 5000000,
                "specialties": "أنظمة أمنية، كاميرات مراقبة، أنظمة إنذار، أنظمة دخول",
                "rating": 4.3,
                "description": "مؤسسة متخصصة في تنفيذ أعمال الأنظمة الأمنية وكاميرات المراقبة وأنظمة الإنذار وأنظمة الدخول"
            },
            {
                "id": "CCTV-003",
                "name": "شركة المراقبة الذكية",
                "category": "أعمال CCTV",
                "subcategory": "أنظمة مراقبة ذكية",
                "contact_person": "م. عمر السعدي",
                "phone": "0555901234",
                "email": "omar@smart-surveillance.com",
                "address": "الدمام - حي الخليج",
                "classification": "درجة أولى",
                "experience_years": 12,
                "completed_projects": 95,
                "ongoing_projects": 8,
                "min_project_value": 300000,
                "max_project_value": 25000000,
                "specialties": "أنظمة مراقبة ذكية، تحليل فيديو، تعرف على الوجوه، تتبع حركة",
                "rating": 4.8,
                "description": "شركة متخصصة في تنفيذ أعمال أنظمة المراقبة الذكية وتحليل الفيديو والتعرف على الوجوه وتتبع الحركة"
            }
        ])
        
        # 4. أنظمة التحكم في الوصول
        subcontractors_data.extend([
            {
                "id": "ACCESS-001",
                "name": "شركة التحكم الأمني",
                "category": "أنظمة التحكم في الوصول",
                "subcategory": "أنظمة تحكم",
                "contact_person": "م. فيصل العنزي",
                "phone": "0556012345",
                "email": "faisal@security-control.com",
                "address": "الرياض - حي الورود",
                "classification": "درجة ثانية",
                "experience_years": 9,
                "completed_projects": 70,
                "ongoing_projects": 5,
                "min_project_value": 100000,
                "max_project_value": 8000000,
                "specialties": "أنظمة تحكم في الدخول، بصمات، بطاقات ذكية، أقفال إلكترونية",
                "rating": 4.5,
                "description": "شركة متخصصة في تنفيذ أعمال أنظمة التحكم في الدخول والبصمات والبطاقات الذكية والأقفال الإلكترونية"
            },
            {
                "id": "ACCESS-002",
                "name": "مؤسسة الوصول الآمن",
                "category": "أنظمة التحكم في الوصول",
                "subcategory": "أنظمة أمنية",
                "contact_person": "م. ماجد الدوسري",
                "phone": "0556123456",
                "email": "majed@safe-access.com",
                "address": "جدة - حي المروة",
                "classification": "درجة ثالثة",
                "experience_years": 6,
                "completed_projects": 40,
                "ongoing_projects": 3,
                "min_project_value": 50000,
                "max_project_value": 3000000,
                "specialties": "أنظمة أمنية، بوابات إلكترونية، حواجز آلية، كاميرات تعرف",
                "rating": 4.2,
                "description": "مؤسسة متخصصة في تنفيذ أعمال الأنظمة الأمنية والبوابات الإلكترونية والحواجز الآلية وكاميرات التعرف"
            },
            {
                "id": "ACCESS-003",
                "name": "شركة الأمن الذكي",
                "category": "أنظمة التحكم في الوصول",
                "subcategory": "أنظمة متكاملة",
                "contact_person": "م. طارق الشهري",
                "phone": "0556234567",
                "email": "tariq@smart-security.com",
                "address": "الدمام - حي النور",
                "classification": "درجة أولى",
                "experience_years": 14,
                "completed_projects": 100,
                "ongoing_projects": 7,
                "min_project_value": 500000,
                "max_project_value": 20000000,
                "specialties": "أنظمة متكاملة، تحكم مركزي، مراقبة ذكية، تحليل سلوك",
                "rating": 4.7,
                "description": "شركة متخصصة في تنفيذ أعمال الأنظمة المتكاملة والتحكم المركزي والمراقبة الذكية وتحليل السلوك"
            }
        ])
        
        # 5. شبكات الري
        subcontractors_data.extend([
            {
                "id": "IRR-001",
                "name": "شركة الواحة لأنظمة الري",
                "category": "شبكات الري",
                "subcategory": "أنظمة ري",
                "contact_person": "م. سامي المطيري",
                "phone": "0556345678",
                "email": "sami@oasis-irrigation.com",
                "address": "الرياض - حي الياسمين",
                "classification": "درجة ثانية",
                "experience_years": 11,
                "completed_projects": 80,
                "ongoing_projects": 6,
                "min_project_value": 200000,
                "max_project_value": 15000000,
                "specialties": "أنظمة ري، شبكات مياه، مضخات، أنظمة تحكم",
                "rating": 4.6,
                "description": "شركة متخصصة في تنفيذ أعمال أنظمة الري وشبكات المياه والمضخات وأنظمة التحكم"
            },
            {
                "id": "IRR-002",
                "name": "مؤسسة الخضراء للري والزراعة",
                "category": "شبكات الري",
                "subcategory": "ري زراعي",
                "contact_person": "م. عبدالرحمن الحربي",
                "phone": "0556456789",
                "email": "abdulrahman@green-irrigation.com",
                "address": "جدة - حي الفيحاء",
                "classification": "درجة ثالثة",
                "experience_years": 8,
                "completed_projects": 55,
                "ongoing_projects": 4,
                "min_project_value": 100000,
                "max_project_value": 5000000,
                "specialties": "ري زراعي، ري بالتنقيط، ري بالرش، أنظمة تسميد",
                "rating": 4.4,
                "description": "مؤسسة متخصصة في تنفيذ أعمال الري الزراعي والري بالتنقيط والري بالرش وأنظمة التسميد"
            },
            {
                "id": "IRR-003",
                "name": "شركة المياه الذكية",
                "category": "شبكات الري",
                "subcategory": "أنظمة ري ذكية",
                "contact_person": "م. خالد السبيعي",
                "phone": "0556567890",
                "email": "khalid@smart-water.com",
                "address": "الدمام - حي الفردوس",
                "classification": "درجة أولى",
                "experience_years": 13,
                "completed_projects": 90,
                "ongoing_projects": 7,
                "min_project_value": 500000,
                "max_project_value": 25000000,
                "specialties": "أنظمة ري ذكية، تحكم عن بعد، استشعار رطوبة، توفير مياه",
                "rating": 4.8,
                "description": "شركة متخصصة في تنفيذ أعمال أنظمة الري الذكية والتحكم عن بعد واستشعار الرطوبة وتوفير المياه"
            }
        ])
        
        # 6. أعمال الصرف الصحي
        subcontractors_data.extend([
            {
                "id": "SEW-001",
                "name": "شركة البنية التحتية للصرف الصحي",
                "category": "أعمال الصرف الصحي",
                "subcategory": "شبكات صرف",
                "contact_person": "م. عبدالعزيز الشمري",
                "phone": "0556678901",
                "email": "abdulaziz@infrastructure-sewage.com",
                "address": "الرياض - حي الملقا",
                "classification": "درجة أولى",
                "experience_years": 16,
                "completed_projects": 120,
                "ongoing_projects": 9,
                "min_project_value": 1000000,
                "max_project_value": 80000000,
                "specialties": "شبكات صرف، محطات ضخ، محطات معالجة، خطوط رئيسية",
                "rating": 4.9,
                "description": "شركة متخصصة في تنفيذ أعمال شبكات الصرف ومحطات الضخ ومحطات المعالجة والخطوط الرئيسية"
            },
            {
                "id": "SEW-002",
                "name": "مؤسسة الصرف المتكاملة",
                "category": "أعمال الصرف الصحي",
                "subcategory": "صرف داخلي",
                "contact_person": "م. فهد العتيبي",
                "phone": "0556789012",
                "email": "fahad@integrated-sewage.com",
                "address": "جدة - حي الحمراء",
                "classification": "درجة ثانية",
                "experience_years": 9,
                "completed_projects": 65,
                "ongoing_projects": 5,
                "min_project_value": 300000,
                "max_project_value": 20000000,
                "specialties": "صرف داخلي، تمديدات صحية، غرف تفتيش، خزانات تحليل",
                "rating": 4.5,
                "description": "مؤسسة متخصصة في تنفيذ أعمال الصرف الداخلي والتمديدات الصحية وغرف التفتيش وخزانات التحليل"
            },
            {
                "id": "SEW-003",
                "name": "شركة معالجة المياه",
                "category": "أعمال الصرف الصحي",
                "subcategory": "محطات معالجة",
                "contact_person": "م. سلطان القحطاني",
                "phone": "0556890123",
                "email": "sultan@water-treatment.com",
                "address": "الدمام - حي الأنوار",
                "classification": "درجة أولى",
                "experience_years": 18,
                "completed_projects": 130,
                "ongoing_projects": 10,
                "min_project_value": 2000000,
                "max_project_value": 100000000,
                "specialties": "محطات معالجة، تنقية مياه، إعادة تدوير، أنظمة تحكم",
                "rating": 4.9,
                "description": "شركة متخصصة في تنفيذ أعمال محطات المعالجة وتنقية المياه وإعادة التدوير وأنظمة التحكم"
            }
        ])
        
        # 7. أعمال الطرق
        subcontractors_data.extend([
            {
                "id": "ROAD-001",
                "name": "شركة الطرق الحديثة",
                "category": "أعمال الطرق",
                "subcategory": "إنشاء طرق",
                "contact_person": "م. محمد الحارثي",
                "phone": "0556901234",
                "email": "mohammed@modern-roads.com",
                "address": "الرياض - حي النخيل",
                "classification": "درجة أولى",
                "experience_years": 20,
                "completed_projects": 150,
                "ongoing_projects": 12,
                "min_project_value": 5000000,
                "max_project_value": 200000000,
                "specialties": "إنشاء طرق، تقاطعات، أنفاق، جسور صغيرة",
                "rating": 4.9,
                "description": "شركة متخصصة في تنفيذ أعمال إنشاء الطرق والتقاطعات والأنفاق والجسور الصغيرة"
            },
            {
                "id": "ROAD-002",
                "name": "مؤسسة الطرق السريعة",
                "category": "أعمال الطرق",
                "subcategory": "رصف طرق",
                "contact_person": "م. سعد الغامدي",
                "phone": "0557012345",
                "email": "saad@highway-contractors.com",
                "address": "جدة - حي الشرفية",
                "classification": "درجة ثانية",
                "experience_years": 12,
                "completed_projects": 85,
                "ongoing_projects": 7,
                "min_project_value": 1000000,
                "max_project_value": 50000000,
                "specialties": "رصف طرق، سفلتة، خلطات إسفلتية، علامات مرورية",
                "rating": 4.6,
                "description": "مؤسسة متخصصة في تنفيذ أعمال رصف الطرق والسفلتة والخلطات الإسفلتية والعلامات المرورية"
            },
            {
                "id": "ROAD-003",
                "name": "شركة البنية التحتية للطرق",
                "category": "أعمال الطرق",
                "subcategory": "بنية تحتية",
                "contact_person": "م. عبدالله المالكي",
                "phone": "0557123456",
                "email": "abdullah@infrastructure-roads.com",
                "address": "الدمام - حي الفيصلية",
                "classification": "درجة أولى",
                "experience_years": 17,
                "completed_projects": 120,
                "ongoing_projects": 10,
                "min_project_value": 3000000,
                "max_project_value": 150000000,
                "specialties": "بنية تحتية، تصريف مياه، قنوات، عبارات",
                "rating": 4.8,
                "description": "شركة متخصصة في تنفيذ أعمال البنية التحتية للطرق وتصريف المياه والقنوات والعبارات"
            }
        ])
        
        # 8. أعمال الجسور
        subcontractors_data.extend([
            {
                "id": "BRIDGE-001",
                "name": "شركة الجسور العالمية",
                "category": "أعمال الجسور",
                "subcategory": "إنشاء جسور",
                "contact_person": "م. فيصل الدوسري",
                "phone": "0557234567",
                "email": "faisal@global-bridges.com",
                "address": "الرياض - حي الصحافة",
                "classification": "درجة أولى",
                "experience_years": 22,
                "completed_projects": 80,
                "ongoing_projects": 8,
                "min_project_value": 10000000,
                "max_project_value": 500000000,
                "specialties": "إنشاء جسور، جسور معلقة، جسور خرسانية، جسور معدنية",
                "rating": 4.9,
                "description": "شركة متخصصة في تنفيذ أعمال إنشاء الجسور والجسور المعلقة والجسور الخرسانية والجسور المعدنية"
            },
            {
                "id": "BRIDGE-002",
                "name": "مؤسسة الجسور الحديثة",
                "category": "أعمال الجسور",
                "subcategory": "صيانة جسور",
                "contact_person": "م. خالد العمري",
                "phone": "0557345678",
                "email": "khalid@modern-bridges.com",
                "address": "جدة - حي البوادي",
                "classification": "درجة ثانية",
                "experience_years": 14,
                "completed_projects": 60,
                "ongoing_projects": 5,
                "min_project_value": 2000000,
                "max_project_value": 100000000,
                "specialties": "صيانة جسور، ترميم، تقوية، توسعة",
                "rating": 4.7,
                "description": "مؤسسة متخصصة في تنفيذ أعمال صيانة الجسور والترميم والتقوية والتوسعة"
            },
            {
                "id": "BRIDGE-003",
                "name": "شركة الإنشاءات المتخصصة",
                "category": "أعمال الجسور",
                "subcategory": "جسور معقدة",
                "contact_person": "م. سلطان الشهري",
                "phone": "0557456789",
                "email": "sultan@specialized-construction.com",
                "address": "الدمام - حي الروضة",
                "classification": "درجة أولى",
                "experience_years": 25,
                "completed_projects": 90,
                "ongoing_projects": 7,
                "min_project_value": 20000000,
                "max_project_value": 800000000,
                "specialties": "جسور معقدة، تقاطعات متعددة المستويات، أنفاق، منشآت خاصة",
                "rating": 5.0,
                "description": "شركة متخصصة في تنفيذ أعمال الجسور المعقدة والتقاطعات متعددة المستويات والأنفاق والمنشآت الخاصة"
            }
        ])
        
        # 9. أعمال الحفر والردم
        subcontractors_data.extend([
            {
                "id": "EXCAV-001",
                "name": "شركة الحفريات الكبرى",
                "category": "أعمال الحفر والردم",
                "subcategory": "حفر كبير",
                "contact_person": "م. ناصر العتيبي",
                "phone": "0557567890",
                "email": "nasser@major-excavation.com",
                "address": "الرياض - حي العزيزية",
                "classification": "درجة أولى",
                "experience_years": 18,
                "completed_projects": 130,
                "ongoing_projects": 10,
                "min_project_value": 3000000,
                "max_project_value": 150000000,
                "specialties": "حفر كبير، نقل مواد، تسوية، تثبيت تربة",
                "rating": 4.8,
                "description": "شركة متخصصة في تنفيذ أعمال الحفر الكبير ونقل المواد والتسوية وتثبيت التربة"
            },
            {
                "id": "EXCAV-002",
                "name": "مؤسسة الحفر والردم",
                "category": "أعمال الحفر والردم",
                "subcategory": "حفر وردم",
                "contact_person": "م. سعيد القحطاني",
                "phone": "0557678901",
                "email": "saeed@excavation-backfill.com",
                "address": "جدة - حي السلامة",
                "classification": "درجة ثانية",
                "experience_years": 12,
                "completed_projects": 90,
                "ongoing_projects": 6,
                "min_project_value": 500000,
                "max_project_value": 30000000,
                "specialties": "حفر وردم، تسوية مواقع، دك تربة، تصريف مياه",
                "rating": 4.6,
                "description": "مؤسسة متخصصة في تنفيذ أعمال الحفر والردم وتسوية المواقع ودك التربة وتصريف المياه"
            },
            {
                "id": "EXCAV-003",
                "name": "شركة التربة المتخصصة",
                "category": "أعمال الحفر والردم",
                "subcategory": "معالجة تربة",
                "contact_person": "م. فهد الشمري",
                "phone": "0557789012",
                "email": "fahad@specialized-soil.com",
                "address": "الدمام - حي النزهة",
                "classification": "درجة أولى",
                "experience_years": 15,
                "completed_projects": 100,
                "ongoing_projects": 8,
                "min_project_value": 2000000,
                "max_project_value": 100000000,
                "specialties": "معالجة تربة، تثبيت، تحسين خواص، فحوصات",
                "rating": 4.8,
                "description": "شركة متخصصة في تنفيذ أعمال معالجة التربة والتثبيت وتحسين الخواص والفحوصات"
            }
        ])
        
        # 10. أعمال الخرسانة
        subcontractors_data.extend([
            {
                "id": "CONC-001",
                "name": "شركة الخرسانة المتميزة",
                "category": "أعمال الخرسانة",
                "subcategory": "خرسانة جاهزة",
                "contact_person": "م. عبدالرحمن الشهري",
                "phone": "0557890123",
                "email": "abdulrahman@premium-concrete.com",
                "address": "الرياض - حي الربيع",
                "classification": "درجة أولى",
                "experience_years": 20,
                "completed_projects": 200,
                "ongoing_projects": 15,
                "min_project_value": 2000000,
                "max_project_value": 200000000,
                "specialties": "خرسانة جاهزة، خرسانة خاصة، خرسانة مسلحة، خرسانة سابقة الإجهاد",
                "rating": 4.9,
                "description": "شركة متخصصة في تنفيذ أعمال الخرسانة الجاهزة والخرسانة الخاصة والخرسانة المسلحة والخرسانة سابقة الإجهاد"
            },
            {
                "id": "CONC-002",
                "name": "مؤسسة الهياكل الخرسانية",
                "category": "أعمال الخرسانة",
                "subcategory": "هياكل خرسانية",
                "contact_person": "م. ماجد العنزي",
                "phone": "0557901234",
                "email": "majed@concrete-structures.com",
                "address": "جدة - حي الروضة",
                "classification": "درجة ثانية",
                "experience_years": 15,
                "completed_projects": 120,
                "ongoing_projects": 8,
                "min_project_value": 1000000,
                "max_project_value": 80000000,
                "specialties": "هياكل خرسانية، أعمدة، أسقف، جدران",
                "rating": 4.7,
                "description": "مؤسسة متخصصة في تنفيذ أعمال الهياكل الخرسانية والأعمدة والأسقف والجدران"
            },
            {
                "id": "CONC-003",
                "name": "شركة الخرسانة المتخصصة",
                "category": "أعمال الخرسانة",
                "subcategory": "خرسانة خاصة",
                "contact_person": "م. خالد المالكي",
                "phone": "0558012345",
                "email": "khalid@specialized-concrete.com",
                "address": "الدمام - حي الشاطئ",
                "classification": "درجة أولى",
                "experience_years": 18,
                "completed_projects": 150,
                "ongoing_projects": 12,
                "min_project_value": 3000000,
                "max_project_value": 250000000,
                "specialties": "خرسانة خاصة، خرسانة عالية المقاومة، خرسانة مقاومة للكيماويات، خرسانة ذاتية الدمك",
                "rating": 4.9,
                "description": "شركة متخصصة في تنفيذ أعمال الخرسانة الخاصة والخرسانة عالية المقاومة والخرسانة المقاومة للكيماويات والخرسانة ذاتية الدمك"
            }
        ])
        
        # تخزين البيانات في حالة الجلسة
        st.session_state.subcontractors_catalog = pd.DataFrame(subcontractors_data)
    
    def render(self):
        """عرض واجهة كتالوج مقاولي الباطن"""
        
        st.markdown("## كتالوج مقاولي الباطن")
        
        # إنشاء تبويبات لعرض الكتالوج
        tabs = st.tabs([
            "عرض الكتالوج", 
            "إضافة مقاول", 
            "تحليل المقاولين",
            "استيراد/تصدير"
        ])
        
        with tabs[0]:
            self._render_catalog_view_tab()
        
        with tabs[1]:
            self._render_add_subcontractor_tab()
        
        with tabs[2]:
            self._render_analysis_tab()
        
        with tabs[3]:
            self._render_import_export_tab()
    
    def _render_catalog_view_tab(self):
        """عرض تبويب عرض الكتالوج"""
        
        st.markdown("### عرض كتالوج مقاولي الباطن")
        
        # استخراج البيانات
        subcontractors_df = st.session_state.subcontractors_catalog
        
        # إنشاء فلاتر للعرض
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # فلتر حسب الفئة
            categories = ["الكل"] + sorted(subcontractors_df["category"].unique().tolist())
            selected_category = st.selectbox("اختر فئة المقاول", categories)
        
        with col2:
            # فلتر حسب الفئة الفرعية
            if selected_category != "الكل":
                subcategories = ["الكل"] + sorted(subcontractors_df[subcontractors_df["category"] == selected_category]["subcategory"].unique().tolist())
            else:
                subcategories = ["الكل"] + sorted(subcontractors_df["subcategory"].unique().tolist())
            
            selected_subcategory = st.selectbox("اختر التخصص", subcategories)
        
        with col3:
            # فلتر حسب التصنيف
            classifications = ["الكل"] + sorted(subcontractors_df["classification"].unique().tolist())
            selected_classification = st.selectbox("اختر التصنيف", classifications)
        
        # تطبيق الفلاتر
        filtered_df = subcontractors_df.copy()
        
        if selected_category != "الكل":
            filtered_df = filtered_df[filtered_df["category"] == selected_category]
        
        if selected_subcategory != "الكل":
            filtered_df = filtered_df[filtered_df["subcategory"] == selected_subcategory]
        
        if selected_classification != "الكل":
            filtered_df = filtered_df[filtered_df["classification"] == selected_classification]
        
        # عرض البيانات
        if not filtered_df.empty:
            # عرض عدد النتائج
            st.info(f"تم العثور على {len(filtered_df)} مقاول باطن")
            
            # عرض المقاولين في شكل بطاقات
            for i, (_, subcontractor) in enumerate(filtered_df.iterrows()):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    # عرض صورة المقاول (استخدام صورة افتراضية)
                    st.image("https://via.placeholder.com/150", caption=subcontractor["name"])
                
                with col2:
                    # عرض معلومات المقاول
                    st.markdown(f"**{subcontractor['name']}** (الكود: {subcontractor['id']})")
                    st.markdown(f"الفئة: {subcontractor['category']} - {subcontractor['subcategory']}")
                    st.markdown(f"التصنيف: {subcontractor['classification']} | الخبرة: {subcontractor['experience_years']} سنة")
                    st.markdown(f"التقييم: {'⭐' * int(subcontractor['rating'])} ({subcontractor['rating']})")
                    st.markdown(f"المشاريع المنجزة: {subcontractor['completed_projects']} | المشاريع الجارية: {subcontractor['ongoing_projects']}")
                
                # إضافة زر لعرض التفاصيل
                if st.button(f"عرض التفاصيل الكاملة", key=f"details_{subcontractor['id']}"):
                    st.session_state.selected_subcontractor = subcontractor['id']
                    self._show_subcontractor_details(subcontractor)
                
                st.markdown("---")
        else:
            st.warning("لا يوجد مقاولين يطابقون معايير البحث")
    
    def _show_subcontractor_details(self, subcontractor):
        """عرض تفاصيل المقاول"""
        
        st.markdown(f"## تفاصيل مقاول الباطن: {subcontractor['name']}")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # عرض صورة المقاول (استخدام صورة افتراضية)
            st.image("https://via.placeholder.com/300", caption=subcontractor["name"])
        
        with col2:
            # عرض المعلومات الأساسية
            st.markdown("### المعلومات الأساسية")
            st.markdown(f"**الكود:** {subcontractor['id']}")
            st.markdown(f"**الفئة:** {subcontractor['category']} - {subcontractor['subcategory']}")
            st.markdown(f"**التصنيف:** {subcontractor['classification']}")
            st.markdown(f"**سنوات الخبرة:** {subcontractor['experience_years']} سنة")
            st.markdown(f"**التقييم:** {'⭐' * int(subcontractor['rating'])} ({subcontractor['rating']})")
            st.markdown(f"**التخصصات:** {subcontractor['specialties']}")
            st.markdown(f"**الوصف:** {subcontractor['description']}")
        
        # عرض معلومات الاتصال
        st.markdown("### معلومات الاتصال")
        
        contact_col1, contact_col2 = st.columns(2)
        
        with contact_col1:
            st.markdown(f"**الشخص المسؤول:** {subcontractor['contact_person']}")
            st.markdown(f"**الهاتف:** {subcontractor['phone']}")
        
        with contact_col2:
            st.markdown(f"**البريد الإلكتروني:** {subcontractor['email']}")
            st.markdown(f"**العنوان:** {subcontractor['address']}")
        
        # عرض معلومات المشاريع
        st.markdown("### معلومات المشاريع")
        
        projects_col1, projects_col2 = st.columns(2)
        
        with projects_col1:
            st.markdown(f"**المشاريع المنجزة:** {subcontractor['completed_projects']}")
            st.markdown(f"**المشاريع الجارية:** {subcontractor['ongoing_projects']}")
        
        with projects_col2:
            st.markdown(f"**الحد الأدنى لقيمة المشروع:** {subcontractor['min_project_value']:,} ريال")
            st.markdown(f"**الحد الأقصى لقيمة المشروع:** {subcontractor['max_project_value']:,} ريال")
        
        # إضافة زر للتعديل
        if st.button("تعديل بيانات المقاول"):
            st.session_state.edit_subcontractor = subcontractor['id']
            # هنا يمكن إضافة منطق التعديل
    
    def _render_add_subcontractor_tab(self):
        """عرض تبويب إضافة مقاول"""
        
        st.markdown("### إضافة مقاول باطن جديد")
        
        # استخراج البيانات
        subcontractors_df = st.session_state.subcontractors_catalog
        
        # إنشاء نموذج إضافة مقاول
        with st.form("add_subcontractor_form"):
            st.markdown("#### المعلومات الأساسية")
            
            # الصف الأول
            col1, col2 = st.columns(2)
            with col1:
                subcontractor_id = st.text_input("كود المقاول", value=f"SUB-{len(subcontractors_df) + 1:03d}")
                subcontractor_name = st.text_input("اسم المقاول", placeholder="مثال: شركة الأنظمة الكهربائية المتكاملة")
            
            with col2:
                # استخراج الفئات والفئات الفرعية الموجودة
                categories = sorted(subcontractors_df["category"].unique().tolist())
                subcontractor_category = st.selectbox("فئة المقاول", categories)
                
                # استخراج الفئات الفرعية بناءً على الفئة المختارة
                subcategories = sorted(subcontractors_df[subcontractors_df["category"] == subcontractor_category]["subcategory"].unique().tolist())
                subcontractor_subcategory = st.selectbox("التخصص", subcategories)
            
            # الصف الثاني
            col1, col2 = st.columns(2)
            with col1:
                subcontractor_classification = st.selectbox("التصنيف", ["درجة أولى", "درجة ثانية", "درجة ثالثة", "درجة رابعة", "درجة خامسة"])
            with col2:
                subcontractor_experience_years = st.number_input("سنوات الخبرة", min_value=1, max_value=50, step=1)
            
            # معلومات الاتصال
            st.markdown("#### معلومات الاتصال")
            
            col1, col2 = st.columns(2)
            with col1:
                subcontractor_contact_person = st.text_input("الشخص المسؤول", placeholder="مثال: م. خالد العتيبي")
                subcontractor_phone = st.text_input("الهاتف", placeholder="مثال: 0555123456")
            
            with col2:
                subcontractor_email = st.text_input("البريد الإلكتروني", placeholder="مثال: info@company.com")
                subcontractor_address = st.text_input("العنوان", placeholder="مثال: الرياض - حي العليا")
            
            # معلومات المشاريع
            st.markdown("#### معلومات المشاريع")
            
            col1, col2 = st.columns(2)
            with col1:
                subcontractor_completed_projects = st.number_input("عدد المشاريع المنجزة", min_value=0, step=1)
                subcontractor_ongoing_projects = st.number_input("عدد المشاريع الجارية", min_value=0, step=1)
            
            with col2:
                subcontractor_min_project_value = st.number_input("الحد الأدنى لقيمة المشروع (ريال)", min_value=0, step=100000)
                subcontractor_max_project_value = st.number_input("الحد الأقصى لقيمة المشروع (ريال)", min_value=0, step=1000000)
            
            # معلومات إضافية
            st.markdown("#### معلومات إضافية")
            
            subcontractor_specialties = st.text_area("التخصصات", placeholder="مثال: تمديدات كهربائية، محطات توزيع، لوحات توزيع، أنظمة إنارة")
            subcontractor_rating = st.slider("التقييم", min_value=1.0, max_value=5.0, step=0.1, value=4.0)
            subcontractor_description = st.text_area("وصف المقاول", placeholder="أدخل وصفاً تفصيلياً للمقاول")
            
            # زر الإضافة
            submit_button = st.form_submit_button("إضافة المقاول")
            
            if submit_button:
                # التحقق من البيانات
                if not subcontractor_name or not subcontractor_category or not subcontractor_subcategory:
                    st.error("يرجى إدخال المعلومات الأساسية للمقاول")
                else:
                    # إنشاء مقاول جديد
                    new_subcontractor = {
                        "id": subcontractor_id,
                        "name": subcontractor_name,
                        "category": subcontractor_category,
                        "subcategory": subcontractor_subcategory,
                        "contact_person": subcontractor_contact_person,
                        "phone": subcontractor_phone,
                        "email": subcontractor_email,
                        "address": subcontractor_address,
                        "classification": subcontractor_classification,
                        "experience_years": subcontractor_experience_years,
                        "completed_projects": subcontractor_completed_projects,
                        "ongoing_projects": subcontractor_ongoing_projects,
                        "min_project_value": subcontractor_min_project_value,
                        "max_project_value": subcontractor_max_project_value,
                        "specialties": subcontractor_specialties,
                        "rating": subcontractor_rating,
                        "description": subcontractor_description
                    }
                    
                    # إضافة المقاول إلى الكتالوج
                    st.session_state.subcontractors_catalog = pd.concat([
                        st.session_state.subcontractors_catalog,
                        pd.DataFrame([new_subcontractor])
                    ], ignore_index=True)
                    
                    st.success(f"تمت إضافة المقاول {subcontractor_name} بنجاح!")
    
    def _render_analysis_tab(self):
        """عرض تبويب تحليل المقاولين"""
        
        st.markdown("### تحليل مقاولي الباطن")
        
        # استخراج البيانات
        subcontractors_df = st.session_state.subcontractors_catalog
        
        # تحليل توزيع المقاولين حسب الفئة
        st.markdown("#### توزيع المقاولين حسب الفئة")
        
        # حساب عدد المقاولين لكل فئة
        category_counts = subcontractors_df["category"].value_counts().reset_index()
        category_counts.columns = ["الفئة", "عدد المقاولين"]
        
        # عرض الجدول
        st.dataframe(category_counts, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة
        fig = px.bar(
            category_counts,
            x="الفئة",
            y="عدد المقاولين",
            title="توزيع مقاولي الباطن حسب الفئة",
            color="الفئة",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل توزيع المقاولين حسب التصنيف
        st.markdown("#### توزيع المقاولين حسب التصنيف")
        
        # حساب عدد المقاولين لكل تصنيف
        classification_counts = subcontractors_df["classification"].value_counts().reset_index()
        classification_counts.columns = ["التصنيف", "عدد المقاولين"]
        
        # إنشاء رسم بياني دائري
        fig = px.pie(
            classification_counts,
            values="عدد المقاولين",
            names="التصنيف",
            title="توزيع مقاولي الباطن حسب التصنيف",
            color="التصنيف"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل متوسط التقييم حسب الفئة
        st.markdown("#### متوسط التقييم حسب الفئة")
        
        # حساب متوسط التقييم لكل فئة
        category_ratings = subcontractors_df.groupby("category").agg({
            "rating": "mean"
        }).reset_index()
        
        # تغيير أسماء الأعمدة
        category_ratings.columns = ["الفئة", "متوسط التقييم"]
        
        # عرض الجدول
        st.dataframe(category_ratings, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة
        fig = px.bar(
            category_ratings,
            x="الفئة",
            y="متوسط التقييم",
            title="متوسط تقييم مقاولي الباطن حسب الفئة",
            color="الفئة",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل متوسط سنوات الخبرة حسب التصنيف
        st.markdown("#### متوسط سنوات الخبرة حسب التصنيف")
        
        # حساب متوسط سنوات الخبرة لكل تصنيف
        classification_experience = subcontractors_df.groupby("classification").agg({
            "experience_years": "mean"
        }).reset_index()
        
        # تغيير أسماء الأعمدة
        classification_experience.columns = ["التصنيف", "متوسط سنوات الخبرة"]
        
        # عرض الجدول
        st.dataframe(classification_experience, use_container_width=True)
        
        # إنشاء رسم بياني للمقارنة
        fig = px.bar(
            classification_experience,
            x="التصنيف",
            y="متوسط سنوات الخبرة",
            title="متوسط سنوات خبرة مقاولي الباطن حسب التصنيف",
            color="التصنيف",
            text_auto=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # تحليل المقاولين الأعلى تقييماً
        st.markdown("#### المقاولين الأعلى تقييماً")
        
        # استخراج المقاولين الأعلى تقييماً
        top_rated = subcontractors_df.sort_values(by="rating", ascending=False).head(10)
        
        # إنشاء جدول للعرض
        top_rated_display = top_rated[["name", "category", "classification", "rating", "experience_years"]].copy()
        top_rated_display.columns = ["اسم المقاول", "الفئة", "التصنيف", "التقييم", "سنوات الخبرة"]
        
        # عرض الجدول
        st.dataframe(top_rated_display, use_container_width=True)
        
        # تحليل المقاولين الأكثر خبرة
        st.markdown("#### المقاولين الأكثر خبرة")
        
        # استخراج المقاولين الأكثر خبرة
        most_experienced = subcontractors_df.sort_values(by="experience_years", ascending=False).head(10)
        
        # إنشاء جدول للعرض
        most_experienced_display = most_experienced[["name", "category", "classification", "experience_years", "rating"]].copy()
        most_experienced_display.columns = ["اسم المقاول", "الفئة", "التصنيف", "سنوات الخبرة", "التقييم"]
        
        # عرض الجدول
        st.dataframe(most_experienced_display, use_container_width=True)
    
    def _render_import_export_tab(self):
        """عرض تبويب استيراد/تصدير"""
        
        st.markdown("### استيراد وتصدير بيانات مقاولي الباطن")
        
        # استيراد البيانات
        st.markdown("#### استيراد البيانات")
        
        uploaded_file = st.file_uploader("اختر ملف Excel لاستيراد بيانات مقاولي الباطن", type=["xlsx", "xls"])
        
        if uploaded_file is not None:
            try:
                # قراءة الملف
                imported_df = pd.read_excel(uploaded_file)
                
                # عرض البيانات المستوردة
                st.dataframe(imported_df, use_container_width=True)
                
                # زر الاستيراد
                if st.button("استيراد البيانات"):
                    # التحقق من وجود الأعمدة المطلوبة
                    required_columns = ["id", "name", "category", "subcategory", "classification"]
                    
                    if all(col in imported_df.columns for col in required_columns):
                        # دمج البيانات المستوردة مع البيانات الحالية
                        st.session_state.subcontractors_catalog = pd.concat([
                            st.session_state.subcontractors_catalog,
                            imported_df
                        ], ignore_index=True).drop_duplicates(subset=["id"])
                        
                        st.success(f"تم استيراد {len(imported_df)} مقاول باطن بنجاح!")
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
            subcontractors_df = st.session_state.subcontractors_catalog
            
            # تصدير البيانات حسب التنسيق المختار
            if export_format == "Excel":
                # تصدير إلى Excel
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    subcontractors_df.to_excel(writer, index=False, sheet_name="Subcontractors")
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف Excel",
                    data=output.getvalue(),
                    file_name="subcontractors_catalog.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            elif export_format == "CSV":
                # تصدير إلى CSV
                csv_data = subcontractors_df.to_csv(index=False)
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف CSV",
                    data=csv_data,
                    file_name="subcontractors_catalog.csv",
                    mime="text/csv"
                )
            
            else:  # JSON
                # تصدير إلى JSON
                json_data = subcontractors_df.to_json(orient="records", force_ascii=False)
                
                # تحميل الملف
                st.download_button(
                    label="تنزيل ملف JSON",
                    data=json_data,
                    file_name="subcontractors_catalog.json",
                    mime="application/json"
                )
    
    def get_subcontractor_by_id(self, subcontractor_id):
        """الحصول على مقاول بواسطة الكود"""
        
        subcontractors_df = st.session_state.subcontractors_catalog
        subcontractor = subcontractors_df[subcontractors_df["id"] == subcontractor_id]
        
        if not subcontractor.empty:
            return subcontractor.iloc[0].to_dict()
        
        return None
    
    def get_subcontractors_by_category(self, category):
        """الحصول على المقاولين حسب الفئة"""
        
        subcontractors_df = st.session_state.subcontractors_catalog
        subcontractors = subcontractors_df[subcontractors_df["category"] == category]
        
        if not subcontractors.empty:
            return subcontractors.to_dict(orient="records")
        
        return []
    
    def get_top_rated_subcontractors(self, category=None, limit=5):
        """الحصول على المقاولين الأعلى تقييماً"""
        
        subcontractors_df = st.session_state.subcontractors_catalog
        
        if category:
            filtered_df = subcontractors_df[subcontractors_df["category"] == category]
        else:
            filtered_df = subcontractors_df
        
        top_rated = filtered_df.sort_values(by="rating", ascending=False).head(limit)
        
        if not top_rated.empty:
            return top_rated.to_dict(orient="records")
        
        return []
