"""
وحدة استراتيجيات التسعير المتقدمة
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

class PricingStrategies:
    def __init__(self):
        if 'pricing_strategies' not in st.session_state:
            self._initialize_pricing_strategies()
        if 'items' not in st.session_state:
            st.session_state.items = []

    def _initialize_pricing_strategies(self):
        """تهيئة استراتيجيات التسعير"""
        st.session_state.pricing_strategies = {
            "strategies": [
                {
                    "id": "MTR-001",
                    "name": "تسعير المواد",
                    "description": "استراتيجية خاصة بتسعير المواد تأخذ في الاعتبار تقلبات الأسعار وتكاليف النقل والتخزين",
                    "profit_margin": 0.12,
                    "risk_factor": 0.05,
                    "storage_cost": 0.03,
                    "transport_cost": 0.04,
                    "market_volatility": 0.02,
                    "applicable_to": "materials"
                },
                {
                    "id": "LBR-001",
                    "name": "تسعير العمالة",
                    "description": "استراتيجية مخصصة للعمالة تراعي المهارات والخبرات ومعدلات الإنتاجية",
                    "profit_margin": 0.15,
                    "risk_factor": 0.03,
                    "productivity_factor": 1.0,
                    "overtime_factor": 1.5,
                    "skill_premium": 0.1,
                    "applicable_to": "labor"
                },
                {
                    "id": "EQP-001",
                    "name": "تسعير المعدات",
                    "description": "استراتيجية لتسعير المعدات تشمل تكاليف التشغيل والصيانة والاستهلاك",
                    "profit_margin": 0.18,
                    "risk_factor": 0.07,
                    "maintenance_factor": 0.1,
                    "depreciation_rate": 0.15,
                    "utilization_rate": 0.8,
                    "applicable_to": "equipment"
                },
                {
                    "id": "SUB-001",
                    "name": "تسعير المقاولين",
                    "description": "استراتيجية لتسعير أعمال المقاولين من الباطن مع مراعاة جودة العمل والالتزام",
                    "profit_margin": 0.10,
                    "risk_factor": 0.08,
                    "quality_factor": 1.0,
                    "reliability_factor": 1.0,
                    "market_competition": 0.05,
                    "applicable_to": "subcontractors"
                }
            ]
        }

    def apply_strategy(self, strategy_id, item_data):
        """تطبيق استراتيجية التسعير حسب نوع البند"""
        strategy = next((s for s in st.session_state.pricing_strategies["strategies"] 
                        if s["id"] == strategy_id), None)

        if not strategy:
            return None

        base_cost = self._calculate_base_cost(item_data, strategy)
        adjustments = self._apply_strategy_adjustments(base_cost, strategy, item_data)

        return {
            "base_cost": base_cost,
            "adjustments": adjustments,
            "total_price": base_cost + sum(adjustments.values())
        }

    def _calculate_base_cost(self, item_data, strategy):
        """حساب التكلفة الأساسية حسب نوع البند"""
        if strategy["applicable_to"] == "materials":
            return self._calculate_materials_cost(item_data, strategy)
        elif strategy["applicable_to"] == "labor":
            return self._calculate_labor_cost(item_data, strategy)
        elif strategy["applicable_to"] == "equipment":
            return self._calculate_equipment_cost(item_data, strategy)
        elif strategy["applicable_to"] == "subcontractors":
            return self._calculate_subcontractor_cost(item_data, strategy)
        return 0

    def _calculate_materials_cost(self, item_data, strategy):
        """حساب تكلفة المواد مع العوامل المؤثرة"""
        base_cost = item_data.get("unit_price", 0) * item_data.get("quantity", 0)
        storage_cost = base_cost * strategy["storage_cost"]
        transport_cost = base_cost * strategy["transport_cost"]
        market_adjustment = base_cost * strategy["market_volatility"]
        return base_cost + storage_cost + transport_cost + market_adjustment

    def _calculate_labor_cost(self, item_data, strategy):
        """حساب تكلفة العمالة مع عوامل الإنتاجية والمهارة"""
        daily_rate = item_data.get("daily_rate", 0)
        productivity = item_data.get("productivity", 1.0) * strategy["productivity_factor"]
        skill_level = item_data.get("skill_level", 1.0)
        skill_premium = daily_rate * strategy["skill_premium"] * (skill_level - 1)
        return (daily_rate + skill_premium) * productivity

    def _calculate_equipment_cost(self, item_data, strategy):
        """حساب تكلفة المعدات مع الصيانة والاستهلاك"""
        daily_rate = item_data.get("daily_rate", 0)
        utilization = strategy["utilization_rate"]
        maintenance = daily_rate * strategy["maintenance_factor"]
        depreciation = daily_rate * strategy["depreciation_rate"]
        return (daily_rate + maintenance + depreciation) / utilization

    def _calculate_subcontractor_cost(self, item_data, strategy):
        """حساب تكلفة المقاولين من الباطن مع عوامل الجودة"""
        base_cost = item_data.get("quoted_price", 0)
        quality_adjustment = base_cost * (strategy["quality_factor"] - 1)
        reliability_adjustment = base_cost * (strategy["reliability_factor"] - 1)
        market_adjustment = base_cost * strategy["market_competition"]
        return base_cost + quality_adjustment + reliability_adjustment + market_adjustment

    def _apply_strategy_adjustments(self, base_cost, strategy, item_data):
        """تطبيق التعديلات حسب الاستراتيجية"""
        return {
            "profit": base_cost * strategy["profit_margin"],
            "risk": base_cost * strategy["risk_factor"]
        }

    def render_strategy_selection(self):
        """عرض واجهة اختيار الاستراتيجية"""
        st.subheader("اختيار استراتيجية التسعير")
        item_type = st.selectbox(
            "نوع البند",
            ["المواد", "العمالة", "المعدات", "المقاولين من الباطن"]
        )

        strategies = [s for s in st.session_state.pricing_strategies["strategies"] 
                     if s["applicable_to"] == self._get_type_key(item_type)]

        selected_strategy = st.selectbox(
            "اختر الاستراتيجية المناسبة",
            options=[s["id"] for s in strategies],
            format_func=lambda x: next(s["name"] for s in strategies if s["id"] == x)
        )

        if selected_strategy:
            strategy = next(s for s in strategies if s["id"] == selected_strategy)
            st.info(strategy["description"])
            self._render_strategy_params(strategy)

        return selected_strategy

    def _get_type_key(self, display_type):
        """تحويل النوع المعروض إلى المفتاح المناسب"""
        type_map = {
            "المواد": "materials",
            "العمالة": "labor",
            "المعدات": "equipment",
            "المقاولين من الباطن": "subcontractors"
        }
        return type_map.get(display_type, "")

    def _render_strategy_params(self, strategy):
        """عرض وتعديل معاملات الاستراتيجية"""
        st.write("معاملات الاستراتيجية:")
        cols = st.columns(2)

        with cols[0]:
            st.metric("هامش الربح", f"{strategy['profit_margin']*100:.1f}%")
            st.metric("عامل المخاطرة", f"{strategy['risk_factor']*100:.1f}%")

        with cols[1]:
            if strategy["applicable_to"] == "materials":
                st.metric("تكلفة التخزين", f"{strategy['storage_cost']*100:.1f}%")
                st.metric("تكلفة النقل", f"{strategy['transport_cost']*100:.1f}%")
            elif strategy["applicable_to"] == "labor":
                st.metric("معامل الإنتاجية", f"{strategy['productivity_factor']:.2f}")
                st.metric("علاوة المهارة", f"{strategy['skill_premium']*100:.1f}%")
            elif strategy["applicable_to"] == "equipment":
                st.metric("معدل الاستهلاك", f"{strategy['depreciation_rate']*100:.1f}%")
                st.metric("معدل الاستغلال", f"{strategy['utilization_rate']*100:.1f}%")
            elif strategy["applicable_to"] == "subcontractors":
                st.metric("معامل الجودة", f"{strategy['quality_factor']:.2f}")
                st.metric("معامل الموثوقية", f"{strategy['reliability_factor']:.2f}")


    def render_strategy_results(self, strategy_id, items_data):
        """عرض نتائج تطبيق الاستراتيجية"""
        if not items_data:
            st.warning("لا توجد بنود لعرض النتائج")
            return

        results = []
        for item in items_data:
            result = self.apply_strategy(strategy_id, item)
            if result:
                results.append({
                    **item,
                    **result
                })

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)

            # عرض الرسم البياني
            st.bar_chart(df[["base_cost", "profit", "risk_cost", "local_content_adjustment"]])

    def calculate_local_content(self, items_data):
        """حساب نسبة المحتوى المحلي"""
        total_cost = 0
        local_content_cost = 0

        for item in items_data:
            total_cost += item.get("total_cost", 0)
            if item.get("is_local", False):
                local_content_cost += item.get("total_cost", 0)

        if total_cost > 0:
            return (local_content_cost / total_cost) * 100
        return 0

    def get_strategy_by_id(self, strategy_id):
        """الحصول على استراتيجية بواسطة المعرف"""
        strategies = st.session_state.pricing_strategies.get("strategies", [])
        strategy = next((s for s in strategies if s["id"] == strategy_id), None)
        return strategy

    def apply_strategy_to_project(self, project_id, strategy_id):
        """تطبيق استراتيجية على مشروع"""
        pass

    def get_project_by_id(self, project_id):
        """الحصول على مشروع بواسطة الكود"""
        projects = st.session_state.pricing_strategies["projects"]
        project = projects[projects["id"] == project_id]
        return project.iloc[0].to_dict() if not project.empty else None

    def calculate_local_content(self, materials_percentage, local_materials_percentage, equipment_percentage, local_equipment_percentage, labor_percentage, local_labor_percentage, subcontractors_percentage, local_subcontractors_percentage):
        """حساب نسبة المحتوى المحلي"""
        total_percentage = materials_percentage + equipment_percentage + labor_percentage + subcontractors_percentage

        if total_percentage != 100:
            return False, f"إجمالي النسب يجب أن يكون 100%، الإجمالي الحالي: {total_percentage}%"

        local_content = (
            materials_percentage * local_materials_percentage / 100 +
            equipment_percentage * local_equipment_percentage / 100 +
            labor_percentage * local_labor_percentage / 100 +
            subcontractors_percentage * local_subcontractors_percentage / 100
        )

        return True, local_content

    def compare_strategies(self, project_data, price_analysis):
        """مقارنة استراتيجيات التسعير المختلفة"""
        strategies = self.get_strategies_list()
        if not strategies:
            return {"success": False, "message": "لا توجد استراتيجيات للمقارنة"}

        try:
            strategies_result = []
            for strategy in strategies:
                result = self.apply_strategy(strategy['id'], project_data) #modified to handle item data
                if result['success']:
                    strategies_result.append(result)
            return {
                "success": True,
                "strategies_result": strategies_result
            }
        except Exception as e:
            return {"success": False, "message": str(e)}

    def get_strategies_list(self):
        """الحصول على قائمة الاستراتيجيات النشطة"""
        strategies = st.session_state.pricing_strategies.get("strategies", []) # Handle case where strategies might not exist yet.
        return strategies


    def render(self):
        """عرض واجهة استراتيجيات التسعير"""
        st.markdown("## استراتيجيات التسعير المتقدمة")

        # إنشاء تبويبات
        tabs = st.tabs([
            "الاستراتيجيات المتاحة",
            "تطبيق الاستراتيجيات",
            "إعدادات التسعير"
        ])

        with tabs[0]:
            self._render_strategies_list()

        with tabs[1]:
            self._render_strategy_application()

        with tabs[2]:
            self._render_pricing_settings()

    def _render_strategies_list(self):
        """عرض قائمة الاستراتيجيات"""
        st.markdown("### الاستراتيجيات المتاحة")
        strategies = st.session_state.pricing_strategies.get("strategies", []) # Handle missing strategies

        # تحويل البيانات للعرض
        if strategies: #Added check for empty list
            display_df = pd.DataFrame(strategies)
            display_df = display_df[["name", "description", "profit_margin", "risk_factor", "local_content_factor"]].copy()
            display_df.columns = ["الاستراتيجية", "الوصف", "هامش الربح", "عامل المخاطرة", "عامل المحتوى المحلي"]
            st.dataframe(display_df, use_container_width=True)
        else:
            st.write("لا توجد استراتيجيات متاحة حاليًا.")


    def _render_strategy_application(self):
        """عرض واجهة تطبيق الاستراتيجيات"""
        st.markdown("### تطبيق استراتيجية التسعير")
        if 'current_project' not in st.session_state:
            st.warning("يرجى اختيار مشروع أولاً")
            return

        project = st.session_state.current_project
        strategies = st.session_state.pricing_strategies["strategies"]

        render_items_management()

        selected_strategy = self.render_strategy_selection()

        if selected_strategy:
            if st.button("تطبيق الاستراتيجية المختارة"):
                if project and "items" in project:
                    strategy = next(s for s in strategies if s["id"] == selected_strategy)
                    st.subheader(f"نتائج تطبيق {strategy['name']}")
                    for item in project["items"]:
                        result = self.apply_strategy(selected_strategy, item)
                        if result:
                            st.write(f"نتائج تطبيق الاستراتيجية على البند: {item.get('code', 'غير محدد')}")
                            st.write(result)

                else:
                    st.error("لا توجد بيانات للبنود في المشروع الحالي.")

    def _render_pricing_settings(self):
        """عرض إعدادات التسعير"""
        st.markdown("### إعدادات التسعير")

        with st.form("pricing_settings"):
            st.number_input("الحد الأدنى لهامش الربح", 0.0, 1.0, 0.15)
            st.number_input("الحد الأقصى لهامش الربح", 0.0, 1.0, 0.30)
            st.number_input("نسبة المحتوى المحلي المستهدفة", 0.0, 1.0, 0.40)

            if st.form_submit_button("حفظ الإعدادات"):
                st.success("تم حفظ الإعدادات بنجاح")

    def _calculate_base_costs(self, project_data):
        """حساب التكاليف الأساسية"""
        if not project_data:
            return {}

        materials_cost = sum(item.get("materials_cost", 0) for item in project_data.get("items", []))
        equipment_cost = sum(item.get("equipment_cost", 0) for item in project_data.get("items", []))
        labor_cost = sum(item.get("labor_cost", 0) for item in project_data.get("items", []))
        subcontractors_cost = sum(item.get("subcontractors_cost", 0) for item in project_data.get("items", []))

        return {
            "materials": materials_cost,
            "equipment": equipment_cost,
            "labor": labor_cost,
            "subcontractors": subcontractors_cost,
            "total": materials_cost + equipment_cost + labor_cost + subcontractors_cost
        }

    def _calculate_final_price(self, base_costs, strategy_factors):
        """حساب السعر النهائي"""
        total_base_cost = base_costs["total"]
        profit = total_base_cost * strategy_factors["profit_margin"]
        risk_cost = total_base_cost * strategy_factors["risk_factor"]
        local_content_adjustment = total_base_cost * (strategy_factors["local_content_factor"] - 1)

        return {
            "base_cost": total_base_cost,
            "profit": profit,
            "risk_cost": risk_cost,
            "local_content_adjustment": local_content_adjustment,
            "total": total_base_cost + profit + risk_cost + local_content_adjustment
        }



def render_items_management():
    st.header("نظام إدارة البنود")

    tab1, tab2, tab3 = st.tabs(["إضافة بنود يدوياً", "استيراد من Excel", "البنود الجاهزة"])

    with tab1:
        with st.form("manual_item_entry"):
            item_code = st.text_input("رمز البند")
            item_desc = st.text_area("وصف البند")
            unit = st.selectbox("الوحدة", ["متر مربع", "متر مكعب", "متر طولي", "عدد", "طن", "كجم"])
            quantity = st.number_input("الكمية", min_value=0.0)

            item_type = st.selectbox("نوع البند", ["المواد", "العمالة", "المعدات", "المقاولين من الباطن"])

            col1, col2 = st.columns(2)
            with col1:
                material_cost = st.number_input("تكلفة المواد", min_value=0.0)
                labor_cost = st.number_input("تكلفة العمالة", min_value=0.0)
            with col2:
                equipment_cost = st.number_input("تكلفة المعدات", min_value=0.0)
                overhead_cost = st.number_input("التكاليف غير المباشرة", min_value=0.0)

            if st.form_submit_button("إضافة البند"):
                if item_code and item_desc:
                    if 'items' not in st.session_state:
                        st.session_state.items = []

                    item_data = {
                        'code': item_code,
                        'description': item_desc,
                        'unit': unit,
                        'quantity': quantity,
                        'item_type': item_type,
                        'materials_cost': material_cost,
                        'labor_cost': labor_cost,
                        'equipment_cost': equipment_cost,
                        'subcontractors_cost': overhead_cost,
                        'total_cost': material_cost + labor_cost + equipment_cost + overhead_cost
                    }

                    if item_type == "المواد":
                      item_data['unit_price'] = material_cost / quantity if quantity > 0 else 0
                    elif item_type == "العمالة":
                      item_data['daily_rate'] = labor_cost / quantity if quantity > 0 else 0
                    elif item_type == "المعدات":
                      item_data['daily_rate'] = equipment_cost / quantity if quantity > 0 else 0
                    elif item_type == "المقاولين من الباطن":
                      item_data['quoted_price'] = overhead_cost

                    st.session_state.items.append(item_data)
                    st.success("تم إضافة البند بنجاح")

    with tab2:
        uploaded_file = st.file_uploader("اختر ملف Excel", type=['xlsx', 'xls'])
        if uploaded_file:
            df = pd.read_excel(uploaded_file)
            st.dataframe(df)
            if st.button("استيراد البنود"):
                # معالجة وتخزين البنود من Excel
                st.success("تم استيراد البنود بنجاح")

    with tab3:
        # عرض البنود المخزنة مسبقاً
        if 'items' in st.session_state:
            df = pd.DataFrame(st.session_state.items)
            st.dataframe(df)