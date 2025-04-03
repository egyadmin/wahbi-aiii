from pathlib import Path
import streamlit as st
import pandas as pd
from datetime import datetime
from pricing_system.modules.analysis import smart_price_analysis as analysis_utils
from pricing_system.modules.catalogs import materials_catalog, equipment_catalog
from pricing_system.modules.indirect_support import overheads
from pricing_system.modules.pricing_strategies import balanced_pricing, profit_oriented

class PricingApp:
    """وحدة التسعير"""
    def __init__(self):
        """تهيئة وحدة التسعير"""
        if 'project_data' not in st.session_state:
            st.session_state.project_data = {}

        if 'bill_of_quantities' not in st.session_state:
            st.session_state.bill_of_quantities = []

        # Maintain existing session state for indirect costs and risks if available.
        if 'indirect_costs' not in st.session_state:
            st.session_state.indirect_costs = {
                'overhead': 0.10,    # نسبة المصاريف العمومية والإدارية
                'profit': 0.15,      # نسبة الربح
                'contingency': 0.05,  # نسبة الطوارئ
                'bonds': 0.02,        # نسبة الضمانات
                'insurance': 0.03     # نسبة التأمين
            }

        if 'risks' not in st.session_state:
            st.session_state.risks = []


    def run(self):
        """تشغيل وحدة التسعير"""
        st.title("وحدة التسعير")

        # اختيار المشروع
        self._select_project()

        tabs = st.tabs([
            "جدول الكميات",
            "تحليل التكاليف",
            "سيناريوهات التسعير",
            "المحتوى المحلي"
        ])

        with tabs[0]:
            self._render_bill_of_quantities_tab()
        with tabs[1]:
            self._render_cost_analysis_tab()
        with tabs[2]:
            self._render_pricing_scenarios_tab()
        with tabs[3]:
            self._render_local_content_tab()

    def _select_project(self):
        """اختيار المشروع"""
        st.sidebar.markdown("### اختيار المشروع")

        # جلب المشاريع من قاعدة البيانات
        projects = self._get_projects_from_db()

        if projects:
            project_names = [p['name'] for p in projects]
            selected_project = st.sidebar.selectbox(
                "اختر المشروع",
                project_names
            )

            # تحديث بيانات المشروع المحدد
            project = next((p for p in projects if p['name'] == selected_project), None)
            if project:
                st.session_state.current_project = project
                st.session_state.bill_of_quantities = project.get('boq_items', [])
        else:
            st.sidebar.warning("لا توجد مشاريع متاحة")

    def _get_projects_from_db(self):
        """جلب المشاريع من قاعدة البيانات"""
        # هنا يتم جلب المشاريع من قاعدة البيانات
        # هذه بيانات تجريبية للتوضيح
        return [
            {
                'id': 1,
                'name': 'مشروع تطوير الطريق',
                'client': 'وزارة النقل',
                'boq_items': [
                    {
                        'code': 'A-001',
                        'description': 'أعمال الحفر',
                        'unit': 'م3',
                        'quantity': 1000,
                        'unit_price': 50,
                        'total_price': 50000
                    }
                ]
            }
        ]

    def _render_bill_of_quantities_tab(self):
        """عرض تبويب جدول الكميات"""
        st.markdown("### جدول الكميات")

        # عرض البنود الحالية
        if st.session_state.bill_of_quantities:
            df = pd.DataFrame(st.session_state.bill_of_quantities)
            st.dataframe(df, use_container_width=True)

        # إضافة بند جديد
        st.markdown("### إضافة بند جديد")

        col1, col2 = st.columns(2)
        with col1:
            code = st.text_input("كود البند")
            description = st.text_area("وصف البند")

        with col2:
            unit = st.selectbox("الوحدة", ["م3", "م2", "متر طولي", "عدد"])
            quantity = st.number_input("الكمية", min_value=0.0)
            unit_price = st.number_input("سعر الوحدة", min_value=0.0)

        if st.button("إضافة البند"):
            if code and description and quantity > 0 and unit_price > 0:
                new_item = {
                    'code': code,
                    'description': description,
                    'unit': unit,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': quantity * unit_price
                }
                st.session_state.bill_of_quantities.append(new_item)
                st.success("تم إضافة البند بنجاح")
                st.rerun()


    def _render_cost_analysis_tab(self):
        st.markdown("### تحليل التكاليف")

        if len(st.session_state.bill_of_quantities) > 0:
            # تحليل التكاليف حسب الفئة
            category_costs = {}
            total_cost = 0

            for item in st.session_state.bill_of_quantities:
                category = item.get('category', 'غير مصنف') # Handle missing category gracefully
                cost = item['total_price']

                if category in category_costs:
                    category_costs[category] += cost
                else:
                    category_costs[category] = cost

                total_cost += cost

            # عرض إجمالي التكاليف
            st.metric("إجمالي التكاليف", f"{total_cost:,.2f} ريال")

            # عرض التكاليف حسب الفئة
            st.markdown("#### التكاليف حسب الفئة")
            for category, cost in category_costs.items():
                percentage = (cost / total_cost) * 100
                st.write(f"- {category}: {cost:,.2f} ريال ({percentage:.1f}%)")
        else:
            st.warning("لا توجد بنود في جدول الكميات")

    def _render_pricing_scenarios_tab(self):
        st.markdown("### سيناريوهات التسعير")
        balanced_pricing.render_balanced_strategy()

    def _render_local_content_tab(self):
        st.markdown("### المحتوى المحلي")
        overheads.render_local_content_ui()