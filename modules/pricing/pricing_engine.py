"""
وحدة التسعير المتكامل لنظام إدارة المناقصات - Hybrid Face
"""

import os
import logging
import threading
import datetime
import json
import math
from pathlib import Path

# تهيئة السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('pricing')

class PricingEngine:
    """محرك التسعير المتكامل"""
    
    def __init__(self, config=None, db=None):
        """تهيئة محرك التسعير"""
        self.config = config
        self.db = db
        self.pricing_in_progress = False
        self.current_project = None
        self.pricing_results = {}
        
        # إنشاء مجلد التسعير إذا لم يكن موجوداً
        if config and hasattr(config, 'EXPORTS_PATH'):
            self.exports_path = Path(config.EXPORTS_PATH)
        else:
            self.exports_path = Path('data/exports')
            
        if not self.exports_path.exists():
            self.exports_path.mkdir(parents=True, exist_ok=True)
    
    def calculate_pricing(self, project_id, strategy="comprehensive", callback=None):
        """حساب التسعير للمشروع"""
        if self.pricing_in_progress:
            logger.warning("هناك عملية تسعير جارية بالفعل")
            return False
        
        self.pricing_in_progress = True
        self.current_project = project_id
        self.pricing_results = {
            "project_id": project_id,
            "strategy": strategy,
            "pricing_start_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "status": "جاري التسعير",
            "direct_costs": {},
            "indirect_costs": {},
            "risk_costs": {},
            "summary": {}
        }
        
        # بدء التسعير في خيط منفصل
        thread = threading.Thread(
            target=self._calculate_pricing_thread,
            args=(project_id, strategy, callback)
        )
        thread.daemon = True
        thread.start()
        
        return True
    
    def _calculate_pricing_thread(self, project_id, strategy, callback):
        """خيط حساب التسعير"""
        try:
            # محاكاة جلب بيانات المشروع من قاعدة البيانات
            project_data = self._get_project_data(project_id)
            
            if not project_data:
                logger.error(f"لم يتم العثور على بيانات المشروع: {project_id}")
                self.pricing_results["status"] = "فشل التسعير"
                self.pricing_results["error"] = "لم يتم العثور على بيانات المشروع"
                return
            
            # حساب التكاليف المباشرة
            self._calculate_direct_costs(project_data)
            
            # حساب التكاليف غير المباشرة
            self._calculate_indirect_costs(project_data, strategy)
            
            # حساب تكاليف المخاطر
            self._calculate_risk_costs(project_data, strategy)
            
            # حساب ملخص التسعير
            self._calculate_pricing_summary(strategy)
            
            # تحديث حالة التسعير
            self.pricing_results["status"] = "اكتمل التسعير"
            self.pricing_results["pricing_end_time"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            logger.info(f"اكتمل تسعير المشروع: {project_id}")
            
        except Exception as e:
            logger.error(f"خطأ في تسعير المشروع: {str(e)}")
            self.pricing_results["status"] = "فشل التسعير"
            self.pricing_results["error"] = str(e)
        
        finally:
            self.pricing_in_progress = False
            
            # استدعاء دالة الاستجابة إذا تم توفيرها
            if callback and callable(callback):
                callback(self.pricing_results)
    
    def _get_project_data(self, project_id):
        """الحصول على بيانات المشروع"""
        # في التطبيق الفعلي، سيتم جلب البيانات من قاعدة البيانات
        # هنا نقوم بمحاكاة البيانات للتوضيح
        
        return {
            "id": project_id,
            "name": "مشروع الطرق السريعة",
            "client": "وزارة النقل",
            "items": [
                {"id": 1, "name": "أعمال الحفر", "unit": "م³", "quantity": 1500, "unit_cost": 45},
                {"id": 2, "name": "أعمال الخرسانة", "unit": "م³", "quantity": 750, "unit_cost": 1200},
                {"id": 3, "name": "أعمال الأسفلت", "unit": "م²", "quantity": 5000, "unit_cost": 120},
                {"id": 4, "name": "أعمال الإنارة", "unit": "عدد", "quantity": 50, "unit_cost": 3500}
            ],
            "resources": {
                "materials": [
                    {"id": 1, "name": "أسمنت", "unit": "طن", "quantity": 300, "unit_cost": 950},
                    {"id": 2, "name": "حديد تسليح", "unit": "طن", "quantity": 120, "unit_cost": 3200},
                    {"id": 3, "name": "رمل", "unit": "م³", "quantity": 450, "unit_cost": 75},
                    {"id": 4, "name": "أسفلت", "unit": "طن", "quantity": 200, "unit_cost": 1800}
                ],
                "equipment": [
                    {"id": 1, "name": "حفارة", "unit": "يوم", "quantity": 45, "unit_cost": 1500},
                    {"id": 2, "name": "لودر", "unit": "يوم", "quantity": 30, "unit_cost": 1200},
                    {"id": 3, "name": "شاحنة نقل", "unit": "يوم", "quantity": 60, "unit_cost": 800},
                    {"id": 4, "name": "خلاطة خرسانة", "unit": "يوم", "quantity": 40, "unit_cost": 600}
                ],
                "labor": [
                    {"id": 1, "name": "عمال", "unit": "يوم", "quantity": 1200, "unit_cost": 150},
                    {"id": 2, "name": "فنيون", "unit": "يوم", "quantity": 600, "unit_cost": 300},
                    {"id": 3, "name": "مهندسون", "unit": "يوم", "quantity": 180, "unit_cost": 800}
                ]
            },
            "risks": [
                {"id": 1, "name": "تأخر توريد المواد", "probability": "متوسط", "impact": "عالي", "cost_impact": 0.05},
                {"id": 2, "name": "تغير أسعار المواد", "probability": "عالي", "impact": "عالي", "cost_impact": 0.08},
                {"id": 3, "name": "ظروف جوية غير مواتية", "probability": "منخفض", "impact": "متوسط", "cost_impact": 0.03},
                {"id": 4, "name": "نقص العمالة", "probability": "متوسط", "impact": "متوسط", "cost_impact": 0.04}
            ],
            "project_duration": 180,  # بالأيام
            "location": "المنطقة الشرقية"
        }
    
    def _calculate_direct_costs(self, project_data):
        """حساب التكاليف المباشرة"""
        # حساب تكاليف البنود
        items_cost = 0
        items_details = []
        
        for item in project_data["items"]:
            total_cost = item["quantity"] * item["unit_cost"]
            items_cost += total_cost
            
            items_details.append({
                "id": item["id"],
                "name": item["name"],
                "unit": item["unit"],
                "quantity": item["quantity"],
                "unit_cost": item["unit_cost"],
                "total_cost": total_cost
            })
        
        # حساب تكاليف الموارد
        materials_cost = 0
        equipment_cost = 0
        labor_cost = 0
        
        for material in project_data["resources"]["materials"]:
            materials_cost += material["quantity"] * material["unit_cost"]
        
        for equipment in project_data["resources"]["equipment"]:
            equipment_cost += equipment["quantity"] * equipment["unit_cost"]
        
        for labor in project_data["resources"]["labor"]:
            labor_cost += labor["quantity"] * labor["unit_cost"]
        
        resources_cost = materials_cost + equipment_cost + labor_cost
        
        # تخزين نتائج التكاليف المباشرة
        self.pricing_results["direct_costs"] = {
            "items": {
                "total": items_cost,
                "details": items_details
            },
            "resources": {
                "total": resources_cost,
                "materials": materials_cost,
                "equipment": equipment_cost,
                "labor": labor_cost
            },
            "total_direct_costs": items_cost
        }
    
    def _calculate_indirect_costs(self, project_data, strategy):
        """حساب التكاليف غير المباشرة"""
        direct_costs = self.pricing_results["direct_costs"]["total_direct_costs"]
        
        # تحديد نسب التكاليف غير المباشرة بناءً على استراتيجية التسعير
        if strategy == "comprehensive":
            overhead_rate = 0.15  # 15% نفقات عامة
            profit_rate = 0.10    # 10% ربح
            admin_rate = 0.05     # 5% تكاليف إدارية
        elif strategy == "competitive":
            overhead_rate = 0.12  # 12% نفقات عامة
            profit_rate = 0.07    # 7% ربح
            admin_rate = 0.04     # 4% تكاليف إدارية
        else:  # balanced
            overhead_rate = 0.13  # 13% نفقات عامة
            profit_rate = 0.08    # 8% ربح
            admin_rate = 0.045    # 4.5% تكاليف إدارية
        
        # حساب التكاليف غير المباشرة
        overhead_cost = direct_costs * overhead_rate
        profit_cost = direct_costs * profit_rate
        admin_cost = direct_costs * admin_rate
        
        # تكاليف إضافية
        mobilization_cost = direct_costs * 0.03  # 3% تكاليف التجهيز
        bonds_insurance_cost = direct_costs * 0.02  # 2% تكاليف الضمانات والتأمين
        
        # إجمالي التكاليف غير المباشرة
        total_indirect_costs = overhead_cost + profit_cost + admin_cost + mobilization_cost + bonds_insurance_cost
        
        # تخزين نتائج التكاليف غير المباشرة
        self.pricing_results["indirect_costs"] = {
            "overhead": {
                "rate": overhead_rate,
                "cost": overhead_cost
            },
            "profit": {
                "rate": profit_rate,
                "cost": profit_cost
            },
            "administrative": {
                "rate": admin_rate,
                "cost": admin_cost
            },
            "mobilization": {
                "rate": 0.03,
                "cost": mobilization_cost
            },
            "bonds_insurance": {
                "rate": 0.02,
                "cost": bonds_insurance_cost
            },
            "total_indirect_costs": total_indirect_costs
        }
    
    def _calculate_risk_costs(self, project_data, strategy):
        """حساب تكاليف المخاطر"""
        direct_costs = self.pricing_results["direct_costs"]["total_direct_costs"]
        
        # تحويل احتمالية وتأثير المخاطر إلى قيم رقمية
        probability_map = {
            "منخفض": 0.3,
            "متوسط": 0.5,
            "عالي": 0.7
        }
        
        impact_map = {
            "منخفض": 0.3,
            "متوسط": 0.5,
            "عالي": 0.7
        }
        
        # حساب تكاليف المخاطر
        risk_costs = []
        total_risk_cost = 0
        
        for risk in project_data["risks"]:
            probability = probability_map.get(risk["probability"], 0.5)
            impact = impact_map.get(risk["impact"], 0.5)
            
            # حساب درجة المخاطرة
            risk_score = probability * impact
            
            # حساب تكلفة المخاطرة
            risk_cost = direct_costs * risk["cost_impact"] * risk_score
            
            # تعديل تكلفة المخاطرة بناءً على استراتيجية التسعير
            if strategy == "comprehensive":
                risk_cost_factor = 1.0  # تغطية كاملة للمخاطر
            elif strategy == "competitive":
                risk_cost_factor = 0.7  # تغطية جزئية للمخاطر
            else:  # balanced
                risk_cost_factor = 0.85  # تغطية متوازنة للمخاطر
            
            adjusted_risk_cost = risk_cost * risk_cost_factor
            total_risk_cost += adjusted_risk_cost
            
            risk_costs.append({
                "id": risk["id"],
                "name": risk["name"],
                "probability": risk["probability"],
                "impact": risk["impact"],
                "risk_score": risk_score,
                "cost_impact": risk["cost_impact"],
                "risk_cost": risk_cost,
                "adjusted_risk_cost": adjusted_risk_cost
            })
        
        # تخزين نتائج تكاليف المخاطر
        self.pricing_results["risk_costs"] = {
            "risks": risk_costs,
            "total_risk_cost": total_risk_cost,
            "strategy_factor": 1.0 if strategy == "comprehensive" else (0.7 if strategy == "competitive" else 0.85)
        }
    
    def _calculate_pricing_summary(self, strategy):
        """حساب ملخص التسعير"""
        direct_costs = self.pricing_results["direct_costs"]["total_direct_costs"]
        indirect_costs = self.pricing_results["indirect_costs"]["total_indirect_costs"]
        risk_costs = self.pricing_results["risk_costs"]["total_risk_cost"]
        
        # حساب إجمالي التكاليف
        total_costs = direct_costs + indirect_costs + risk_costs
        
        # حساب ضريبة القيمة المضافة (15%)
        vat = total_costs * 0.15
        
        # حساب السعر النهائي
        final_price = total_costs + vat
        
        # تخزين ملخص التسعير
        self.pricing_results["summary"] = {
            "direct_costs": direct_costs,
            "indirect_costs": indirect_costs,
            "risk_costs": risk_costs,
            "total_costs": total_costs,
            "vat": {
                "rate": 0.15,
                "amount": vat
            },
            "final_price": final_price,
            "strategy": strategy,
            "pricing_notes": self._generate_pricing_notes(strategy)
        }
    
    def _generate_pricing_notes(self, strategy):
        """توليد ملاحظات التسعير"""
        if strategy == "comprehensive":
            return [
                "تم تطبيق استراتيجية التسعير الشاملة التي تغطي جميع التكاليف والمخاطر",
                "تم تضمين هامش ربح مناسب (10%) لضمان ربحية المشروع",
                "تم تغطية جميع المخاطر المحتملة بشكل كامل",
                "يوصى بمراجعة أسعار المواد قبل تقديم العرض النهائي"
            ]
        elif strategy == "competitive":
            return [
                "تم تطبيق استراتيجية التسعير التنافسية لزيادة فرص الفوز بالمناقصة",
                "تم تخفيض هامش الربح (7%) لتقديم سعر تنافسي",
                "تم تغطية المخاطر بشكل جزئي، مما يتطلب إدارة مخاطر فعالة أثناء التنفيذ",
                "يجب مراقبة التكاليف بدقة أثناء تنفيذ المشروع لضمان الربحية"
            ]
        else:  # balanced
            return [
                "تم تطبيق استراتيجية التسعير المتوازنة التي توازن بين الربحية والتنافسية",
                "تم تضمين هامش ربح معقول (8%) يوازن بين الربحية والتنافسية",
                "تم تغطية المخاطر الرئيسية بشكل مناسب",
                "يوصى بمراجعة بنود التكلفة العالية قبل تقديم العرض النهائي"
            ]
    
    def get_pricing_status(self):
        """الحصول على حالة التسعير الحالي"""
        if not self.pricing_in_progress:
            if not self.pricing_results:
                return {"status": "لا يوجد تسعير جارٍ"}
            else:
                return {"status": self.pricing_results.get("status", "غير معروف")}
        
        return {
            "status": "جاري التسعير",
            "project_id": self.current_project,
            "start_time": self.pricing_results.get("pricing_start_time")
        }
    
    def get_pricing_results(self):
        """الحصول على نتائج التسعير"""
        return self.pricing_results
    
    def export_pricing_results(self, output_path=None):
        """تصدير نتائج التسعير إلى ملف JSON"""
        if not self.pricing_results:
            logger.warning("لا توجد نتائج تسعير للتصدير")
            return None
        
        if not output_path:
            # إنشاء اسم ملف افتراضي
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"pricing_results_{timestamp}.json"
            output_path = os.path.join(self.exports_path, filename)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(self.pricing_results, f, ensure_ascii=False, indent=4)
            
            logger.info(f"تم تصدير نتائج التسعير إلى: {output_path}")
            return output_path
        
        except Exception as e:
            logger.error(f"خطأ في تصدير نتائج التسعير: {str(e)}")
            return None
    
    def import_pricing_results(self, input_path):
        """استيراد نتائج التسعير من ملف JSON"""
        if not os.path.exists(input_path):
            logger.error(f"ملف نتائج التسعير غير موجود: {input_path}")
            return False
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                self.pricing_results = json.load(f)
            
            logger.info(f"تم استيراد نتائج التسعير من: {input_path}")
            return True
        
        except Exception as e:
            logger.error(f"خطأ في استيراد نتائج التسعير: {str(e)}")
            return False
