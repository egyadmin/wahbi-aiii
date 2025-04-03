import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# إضافة مسار الوحدات الجديدة
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'pricing_system'))

# استيراد الوحدات الجديدة
from modules.catalogs.equipment_catalog import EquipmentCatalog
from modules.catalogs.materials_catalog import MaterialsCatalog
from modules.catalogs.labor_catalog import LaborCatalog
from modules.catalogs.subcontractors_catalog import SubcontractorsCatalog
from modules.analysis.smart_price_analysis import SmartPriceAnalysis
from pricing_system.modules.indirect_support.overheads import IndirectSupportManagement
from modules.pricing_strategies.pricing_strategies import PricingStrategies

class IntegrationFramework:
    """
    إطار التكامل بين النظام الجديد والنظام القديم
    يربط بين وحدات PricingApp و ResourcesApp مع الوحدات الجديدة
    """
    
    def __init__(self):
        """
        تهيئة إطار التكامل وإنشاء مثيلات من جميع الوحدات
        """
        # تهيئة حالة الجلسة إذا لم تكن موجودة
        if 'integration_initialized' not in st.session_state:
            st.session_state.integration_initialized = True
            
            # تهيئة وحدات الكتالوج
            st.session_state.equipment_catalog = EquipmentCatalog()
            st.session_state.materials_catalog = MaterialsCatalog()
            st.session_state.labor_catalog = LaborCatalog()
            st.session_state.subcontractors_catalog = SubcontractorsCatalog()
            
            # تهيئة وحدات التحليل والتسعير
            st.session_state.smart_price_analysis = SmartPriceAnalysis()
            st.session_state.indirect_support = IndirectSupportManagement()
            if 'pricing_strategies' not in st.session_state or not isinstance(st.session_state.pricing_strategies, PricingStrategies):
                st.session_state.pricing_strategies = PricingStrategies()
            
            # تهيئة بيانات المشروع
            st.session_state.project_data = {
                'name': '',
                'location': '',
                'client': '',
                'start_date': None,
                'end_date': None,
                'budget': 0.0,
                'boq_items': [],
                'resources': [],
                'pricing_strategy': 'standard',
                'indirect_costs': {},
                'profit_margin': 0.15,
                'local_content_target': 0.40,  # هدف المحتوى المحلي (رؤية 2030)
            }
            
            # تهيئة بيانات التحليل
            st.session_state.analysis_results = {
                'direct_costs': 0.0,
                'indirect_costs': 0.0,
                'total_costs': 0.0,
                'profit': 0.0,
                'total_price': 0.0,
                'local_content_percentage': 0.0,
            }
    
    def connect_pricing_app(self, pricing_app):
        """
        ربط وحدة PricingApp مع إطار التكامل
        
        Args:
            pricing_app: مثيل من فئة PricingApp
        """
        self.pricing_app = pricing_app
        
        # إضافة الوظائف الجديدة إلى PricingApp
        pricing_app._render_bill_of_quantities_tab_original = pricing_app._render_bill_of_quantities_tab
        pricing_app._render_bill_of_quantities_tab = self._enhanced_render_bill_of_quantities_tab
        
        pricing_app._render_cost_analysis_tab_original = pricing_app._render_cost_analysis_tab
        pricing_app._render_cost_analysis_tab = self._enhanced_render_cost_analysis_tab
        
        pricing_app._render_pricing_scenarios_tab_original = pricing_app._render_pricing_scenarios_tab
        pricing_app._render_pricing_scenarios_tab = self._enhanced_render_pricing_scenarios_tab
        
        # إضافة علامات تبويب جديدة
        pricing_app.tabs.extend([
            "كتالوجات الموارد",
            "الإدارات المساندة",
            "المحتوى المحلي"
        ])
        
        # إضافة دوال العرض للعلامات الجديدة
        pricing_app._render_resource_catalogs_tab = self._render_resource_catalogs_tab
        pricing_app._render_indirect_support_tab = self._render_indirect_support_tab
        pricing_app._render_local_content_tab = self._render_local_content_tab
        
        # تحديث دالة العرض الرئيسية
        pricing_app_render_original = pricing_app.render
        
        def enhanced_render():
            """
            دالة العرض المحسنة لـ PricingApp
            """
            st.sidebar.title("نظام التسعير الذكي")
            selected_tab = st.sidebar.radio("اختر القسم:", pricing_app.tabs)
            
            if selected_tab == "جدول الكميات":
                pricing_app._render_bill_of_quantities_tab()
            elif selected_tab == "تحليل التكاليف":
                pricing_app._render_cost_analysis_tab()
            elif selected_tab == "سيناريوهات التسعير":
                pricing_app._render_pricing_scenarios_tab()
            elif selected_tab == "التحليل التنافسي":
                pricing_app._render_competitive_analysis_tab()
            elif selected_tab == "التقارير":
                pricing_app._render_reports_tab()
            elif selected_tab == "كتالوجات الموارد":
                pricing_app._render_resource_catalogs_tab()
            elif selected_tab == "الإدارات المساندة":
                pricing_app._render_indirect_support_tab()
            elif selected_tab == "المحتوى المحلي":
                pricing_app._render_local_content_tab()
        
        pricing_app.render = enhanced_render
    
    def connect_resources_app(self, resources_app):
        """
        ربط وحدة ResourcesApp مع إطار التكامل
        
        Args:
            resources_app: مثيل من فئة ResourcesApp
        """
        self.resources_app = resources_app
        
        # إضافة الوظائف الجديدة إلى ResourcesApp
        resources_app_render_original = resources_app.render
        
        def enhanced_resources_render():
            """
            دالة العرض المحسنة لـ ResourcesApp
            """
            st.sidebar.title("إدارة الموارد")
            
            # استدعاء دالة العرض الأصلية
            resources_app_render_original()
            
            # إضافة زر للوصول إلى كتالوجات الموارد
            if st.sidebar.button("عرض كتالوجات الموارد", key="resources_catalogs_btn"):
                st.session_state.current_view = "resource_catalogs"
                self._render_resource_catalogs_tab()
        
        resources_app.render = enhanced_resources_render
        
        # ربط كتالوجات الموارد مع ResourcesApp
        resources_app.equipment_catalog = st.session_state.equipment_catalog
        resources_app.materials_catalog = st.session_state.materials_catalog
        resources_app.labor_catalog = st.session_state.labor_catalog
        resources_app.subcontractors_catalog = st.session_state.subcontractors_catalog
    
    def _enhanced_render_bill_of_quantities_tab(self):
        """
        النسخة المحسنة من دالة عرض علامة تبويب جدول الكميات
        تدمج الوظائف الجديدة مع الوظائف الموجودة
        """
        st.header("جدول الكميات (BOQ)")
        
        # استدعاء الدالة الأصلية
        self.pricing_app._render_bill_of_quantities_tab_original()
        
        # إضافة وظائف جديدة
        st.subheader("استيراد جدول الكميات من Excel")
        
        uploaded_file = st.file_uploader("اختر ملف Excel", type=["xlsx", "xls"], key="boq_uploader")
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.success(f"تم استيراد {len(df)} بند بنجاح")
                st.dataframe(df)
                
                if st.button("إضافة البنود إلى المشروع", key="add_imported_items"):
                    # إضافة البنود المستوردة إلى بيانات المشروع
                    for _, row in df.iterrows():
                        item = {
                            'item_code': row.get('كود البند', ''),
                            'description': row.get('وصف البند', ''),
                            'unit': row.get('الوحدة', ''),
                            'quantity': float(row.get('الكمية', 0)),
                            'unit_price': float(row.get('سعر الوحدة', 0)),
                            'total_price': float(row.get('الإجمالي', 0)),
                        }
                        st.session_state.project_data['boq_items'].append(item)
                    
                    st.success("تم إضافة البنود إلى المشروع بنجاح")
                    
                    # تحليل البنود باستخدام وحدة التحليل الذكي
                    st.session_state.smart_price_analysis.analyze_boq_items(st.session_state.project_data['boq_items'])
            
            except Exception as e:
                st.error(f"حدث خطأ أثناء استيراد الملف: {str(e)}")
        
        # إضافة قسم التحليل الذكي للبنود
        st.subheader("التحليل الذكي للبنود")
        
        if len(st.session_state.project_data['boq_items']) > 0:
            selected_item_index = st.selectbox(
                "اختر البند للتحليل",
                range(len(st.session_state.project_data['boq_items'])),
                format_func=lambda i: f"{st.session_state.project_data['boq_items'][i]['item_code']} - {st.session_state.project_data['boq_items'][i]['description']}"
            )
            
            selected_item = st.session_state.project_data['boq_items'][selected_item_index]
            
            # عرض تحليل البند
            analysis_result = st.session_state.smart_price_analysis.get_item_analysis(selected_item_index)
            
            if analysis_result:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**تحليل تكاليف البند:**")
                    st.write(f"- تكلفة المواد: {analysis_result['materials_cost']} ريال")
                    st.write(f"- تكلفة المعدات: {analysis_result['equipment_cost']} ريال")
                    st.write(f"- تكلفة العمالة: {analysis_result['labor_cost']} ريال")
                    st.write(f"- تكاليف غير مباشرة: {analysis_result['indirect_cost']} ريال")
                    st.write(f"- هامش الربح: {analysis_result['profit_margin']} ريال")
                    st.write(f"- **إجمالي سعر البند: {analysis_result['total_price']} ريال**")
                
                with col2:
                    # رسم بياني دائري لتوزيع التكاليف
                    fig = px.pie(
                        values=[
                            analysis_result['materials_cost'],
                            analysis_result['equipment_cost'],
                            analysis_result['labor_cost'],
                            analysis_result['indirect_cost'],
                            analysis_result['profit_margin']
                        ],
                        names=['المواد', 'المعدات', 'العمالة', 'تكاليف غير مباشرة', 'هامش الربح'],
                        title="توزيع تكاليف البند"
                    )
                    st.plotly_chart(fig)
            
            # تحرير مكونات البند
            st.subheader("تحرير مكونات البند")
            
            tab1, tab2, tab3, tab4 = st.tabs(["المواد", "المعدات", "العمالة", "مقاولي الباطن"])
            
            with tab1:
                st.write("**المواد المستخدمة في البند:**")
                
                # عرض المواد الحالية
                if 'materials' in analysis_result:
                    for i, material in enumerate(analysis_result['materials']):
                        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                        with col1:
                            st.text(material['name'])
                        with col2:
                            st.text(f"الكمية: {material['quantity']} {material['unit']}")
                        with col3:
                            st.text(f"السعر: {material['price']} ريال/{material['unit']}")
                        with col4:
                            st.text(f"الإجمالي: {material['total']} ريال")
                        with col5:
                            if st.button("حذف", key=f"del_mat_{i}"):
                                analysis_result['materials'].pop(i)
                                st.session_state.smart_price_analysis.update_item_analysis(selected_item_index, analysis_result)
                                st.experimental_rerun()
                
                # إضافة مواد جديدة
                st.subheader("إضافة مادة جديدة")
                
                # عرض قائمة المواد من الكتالوج
                catalog_materials = st.session_state.materials_catalog.get_materials_list()
                selected_material = st.selectbox("اختر المادة من الكتالوج", catalog_materials, key="mat_select")
                
                material_details = st.session_state.materials_catalog.get_material_details(selected_material)
                
                quantity = st.number_input("الكمية", min_value=0.0, step=0.1, key="mat_quantity")
                
                if st.button("إضافة المادة", key="add_material_btn"):
                    if 'materials' not in analysis_result:
                        analysis_result['materials'] = []
                    
                    new_material = {
                        'name': selected_material,
                        'quantity': quantity,
                        'unit': material_details['unit'],
                        'price': material_details['price'],
                        'total': quantity * material_details['price'],
                        'is_local': material_details['is_local']
                    }
                    
                    analysis_result['materials'].append(new_material)
                    st.session_state.smart_price_analysis.update_item_analysis(selected_item_index, analysis_result)
                    st.success(f"تمت إضافة {selected_material} بنجاح")
                    st.experimental_rerun()
            
            with tab2:
                st.write("**المعدات المستخدمة في البند:**")
                
                # عرض المعدات الحالية
                if 'equipment' in analysis_result:
                    for i, equipment in enumerate(analysis_result['equipment']):
                        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                        with col1:
                            st.text(equipment['name'])
                        with col2:
                            st.text(f"المدة: {equipment['duration']} {equipment['duration_unit']}")
                        with col3:
                            st.text(f"السعر: {equipment['price']} ريال/{equipment['duration_unit']}")
                        with col4:
                            st.text(f"الإجمالي: {equipment['total']} ريال")
                        with col5:
                            if st.button("حذف", key=f"del_equip_{i}"):
                                analysis_result['equipment'].pop(i)
                                st.session_state.smart_price_analysis.update_item_analysis(selected_item_index, analysis_result)
                                st.experimental_rerun()
                
                # إضافة معدات جديدة
                st.subheader("إضافة معدة جديدة")
                
                # عرض قائمة المعدات من الكتالوج
                catalog_equipment = st.session_state.equipment_catalog.get_equipment_list()
                selected_equipment = st.selectbox("اختر المعدة من الكتالوج", catalog_equipment, key="equip_select")
                
                equipment_details = st.session_state.equipment_catalog.get_equipment_details(selected_equipment)
                
                duration = st.number_input("المدة", min_value=0.0, step=0.5, key="equip_duration")
                duration_unit = st.selectbox("وحدة المدة", ["ساعة", "يوم", "أسبوع", "شهر"], key="equip_duration_unit")
                
                if st.button("إضافة المعدة", key="add_equipment_btn"):
                    if 'equipment' not in analysis_result:
                        analysis_result['equipment'] = []
                    
                    # تحويل السعر حسب وحدة المدة
                    price_per_unit = equipment_details['price_per_hour']
                    if duration_unit == "يوم":
                        price_per_unit = equipment_details['price_per_day']
                    elif duration_unit == "أسبوع":
                        price_per_unit = equipment_details['price_per_week']
                    elif duration_unit == "شهر":
                        price_per_unit = equipment_details['price_per_month']
                    
                    new_equipment = {
                        'name': selected_equipment,
                        'duration': duration,
                        'duration_unit': duration_unit,
                        'price': price_per_unit,
                        'total': duration * price_per_unit,
                        'is_local': equipment_details['is_local']
                    }
                    
                    analysis_result['equipment'].append(new_equipment)
                    st.session_state.smart_price_analysis.update_item_analysis(selected_item_index, analysis_result)
                    st.success(f"تمت إضافة {selected_equipment} بنجاح")
                    st.experimental_rerun()
            
            with tab3:
                st.write("**العمالة المستخدمة في البند:**")
                
                # عرض العمالة الحالية
                if 'labor' in analysis_result:
                    for i, labor in enumerate(analysis_result['labor']):
                        col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])
                        with col1:
                            st.text(labor['name'])
                        with col2:
                            st.text(f"المدة: {labor['duration']} {labor['duration_unit']}")
                        with col3:
                            st.text(f"السعر: {labor['price']} ريال/{labor['duration_unit']}")
                        with col4:
                            st.text(f"الإجمالي: {labor['total']} ريال")
                        with col5:
                            if st.button("حذف", key=f"del_labor_{i}"):
                                analysis_result['labor'].pop(i)
                                st.session_state.smart_price_analysis.update_item_analysis(selected_item_index, analysis_result)
                                st.experimental_rerun()
                
                # إضافة عمالة جديدة
                st.subheader("إضافة عمالة جديدة")
                
                # عرض قائمة العمالة من الكتالوج
                catalog_labor = st.session_state.labor_catalog.get_labor_list()
                selected_labor = st.selectbox("اختر العمالة من الكتالوج", catalog_labor, key="labor_select")
                
                labor_details = st.session_state.labor_catalog.get_labor_details(selected_labor)
                
                duration = st.number_input("المدة", min_value=0.0, step=0.5, key="labor_duration")
                duration_unit = st.selectbox("وحدة المدة", ["ساعة", "يوم", "أسبوع", "شهر"], key="labor_duration_unit")
                
                if st.button("إضافة العمالة", key="add_labor_btn"):
                    if 'labor' not in analysis_result:
                        analysis_result['labor'] = []
                    
                    # تحويل السعر حسب وحدة المدة
                    price_per_unit = labor_details['price_per_hour']
                    if duration_unit == "يوم":
                        price_per_unit = labor_details['price_per_day']
                    elif duration_unit == "أسبوع":
                        price_per_unit = labor_details['price_per_week']
                    elif duration_unit == "شهر":
                        price_per_unit = labor_details['price_per_month']
                    
                    new_labor = {
                        'name': selected_labor,
                        'duration': duration,
                        'duration_unit': duration_unit,
                        'price': price_per_unit,
                        'total': duration * price_per_unit,
                        'is_local': labor_details['is_local']
                    }
                    
                    analysis_result['labor'].append(new_labor)
                    st.session_state.smart_price_analysis.update_item_analysis(selected_item_index, analysis_result)
                    st.success(f"تمت إضافة {selected_labor} بنجاح")
                    st.experimental_rerun()
            
            with tab4:
                st.write("**مقاولي الباطن المستخدمين في البند:**")
                
                # عرض مقاولي الباطن الحاليين
                if 'subcontractors' in analysis_result:
                    for i, subcontractor in enumerate(analysis_result['subcontractors']):
                        col1, col2, col3, col4 = st.columns([3, 3, 3, 1])
                        with col1:
                            st.text(subcontractor['name'])
                        with col2:
                            st.text(f"نوع العمل: {subcontractor['work_type']}")
                        with col3:
                            st.text(f"الإجمالي: {subcontractor['total']} ريال")
                        with col4:
                            if st.button("حذف", key=f"del_sub_{i}"):
                                analysis_result['subcontractors'].pop(i)
                                st.session_state.smart_price_analysis.update_item_analysis(selected_item_index, analysis_result)
                                st.experimental_rerun()
                
                # إضافة مقاول باطن جديد
                st.subheader("إضافة مقاول باطن جديد")
                
                # عرض قائمة مقاولي الباطن من الكتالوج
                catalog_subcontractors = st.session_state.subcontractors_catalog.get_subcontractors_list()
                selected_subcontractor = st.selectbox("اختر مقاول الباطن من الكتالوج", catalog_subcontractors, key="sub_select")
                
                subcontractor_details = st.session_state.subcontractors_catalog.get_subcontractor_details(selected_subcontractor)
                
                work_description = st.text_area("وصف العمل", key="sub_work_desc")
                total_price = st.number_input("السعر الإجمالي", min_value=0.0, step=1000.0, key="sub_price")
                
                if st.button("إضافة مقاول الباطن", key="add_sub_btn"):
                    if 'subcontractors' not in analysis_result:
                        analysis_result['subcontractors'] = []
                    
                    new_subcontractor = {
                        'name': selected_subcontractor,
                        'work_type': subcontractor_details['specialization'],
                        'work_description': work_description,
                        'total': total_price,
                        'is_local': subcontractor_details['is_local']
                    }
                    
                    analysis_result['subcontractors'].append(new_subcontractor)
                    st.session_state.smart_price_analysis.update_item_analysis(selected_item_index, analysis_result)
                    st.success(f"تمت إضافة {selected_subcontractor} بنجاح")
                    st.experimental_rerun()
    
    def _enhanced_render_cost_analysis_tab(self):
        """
        النسخة المحسنة من دالة عرض علامة تبويب تحليل التكاليف
        تدمج الوظائف الجديدة مع الوظائف الموجودة
        """
        st.header("تحليل التكاليف")
        
        # استدعاء الدالة الأصلية
        self.pricing_app._render_cost_analysis_tab_original()
        
        # إضافة وظائف جديدة
        st.subheader("التحليل الذكي للتكاليف")
        
        # تحليل التكاليف الإجمالية للمشروع
        if len(st.session_state.project_data['boq_items']) > 0:
            # تحليل التكاليف حسب النوع
            cost_analysis = st.session_state.smart_price_analysis.get_project_cost_analysis()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**تحليل التكاليف الإجمالية للمشروع:**")
                st.write(f"- تكلفة المواد: {cost_analysis['total_materials_cost']} ريال")
                st.write(f"- تكلفة المعدات: {cost_analysis['total_equipment_cost']} ريال")
                st.write(f"- تكلفة العمالة: {cost_analysis['total_labor_cost']} ريال")
                st.write(f"- تكلفة مقاولي الباطن: {cost_analysis['total_subcontractors_cost']} ريال")
                st.write(f"- التكاليف غير المباشرة: {cost_analysis['total_indirect_cost']} ريال")
                st.write(f"- هامش الربح: {cost_analysis['total_profit_margin']} ريال")
                st.write(f"- **إجمالي تكلفة المشروع: {cost_analysis['total_project_cost']} ريال**")
                st.write(f"- **إجمالي سعر المشروع: {cost_analysis['total_project_price']} ريال**")
            
            with col2:
                # رسم بياني دائري لتوزيع التكاليف
                fig = px.pie(
                    values=[
                        cost_analysis['total_materials_cost'],
                        cost_analysis['total_equipment_cost'],
                        cost_analysis['total_labor_cost'],
                        cost_analysis['total_subcontractors_cost'],
                        cost_analysis['total_indirect_cost'],
                        cost_analysis['total_profit_margin']
                    ],
                    names=['المواد', 'المعدات', 'العمالة', 'مقاولي الباطن', 'تكاليف غير مباشرة', 'هامش الربح'],
                    title="توزيع تكاليف المشروع"
                )
                st.plotly_chart(fig)
            
            # تحليل التكاليف حسب البنود
            st.subheader("تحليل التكاليف حسب البنود")
            
            items_df = pd.DataFrame([
                {
                    'البند': item['item_code'] + ' - ' + item['description'],
                    'التكلفة المباشرة': analysis['direct_cost'],
                    'التكلفة غير المباشرة': analysis['indirect_cost'],
                    'هامش الربح': analysis['profit_margin'],
                    'إجمالي السعر': analysis['total_price']
                }
                for item, analysis in zip(
                    st.session_state.project_data['boq_items'],
                    st.session_state.smart_price_analysis.get_all_items_analysis()
                )
            ])
            
            st.dataframe(items_df)
            
            # رسم بياني شريطي للتكاليف حسب البنود
            fig = px.bar(
                items_df,
                x='البند',
                y=['التكلفة المباشرة', 'التكلفة غير المباشرة', 'هامش الربح'],
                title="توزيع التكاليف حسب البنود",
                barmode='stack'
            )
            st.plotly_chart(fig)
            
            # تحليل المواد الأكثر تكلفة
            st.subheader("المواد الأكثر تكلفة في المشروع")
            
            top_materials = st.session_state.smart_price_analysis.get_top_materials(limit=10)
            
            if top_materials:
                materials_df = pd.DataFrame(top_materials)
                
                fig = px.bar(
                    materials_df,
                    x='name',
                    y='total_cost',
                    title="المواد الأكثر تكلفة في المشروع",
                    labels={'name': 'المادة', 'total_cost': 'التكلفة الإجمالية (ريال)'}
                )
                st.plotly_chart(fig)
            
            # تحليل المعدات الأكثر تكلفة
            st.subheader("المعدات الأكثر تكلفة في المشروع")
            
            top_equipment = st.session_state.smart_price_analysis.get_top_equipment(limit=10)
            
            if top_equipment:
                equipment_df = pd.DataFrame(top_equipment)
                
                fig = px.bar(
                    equipment_df,
                    x='name',
                    y='total_cost',
                    title="المعدات الأكثر تكلفة في المشروع",
                    labels={'name': 'المعدة', 'total_cost': 'التكلفة الإجمالية (ريال)'}
                )
                st.plotly_chart(fig)
    
    def _enhanced_render_pricing_scenarios_tab(self):
        """
        النسخة المحسنة من دالة عرض علامة تبويب سيناريوهات التسعير
        تدمج الوظائف الجديدة مع الوظائف الموجودة
        """
        st.header("سيناريوهات التسعير")
        
        # استدعاء الدالة الأصلية
        self.pricing_app._render_pricing_scenarios_tab_original()
        
        # إضافة وظائف جديدة
        st.subheader("استراتيجيات التسعير المتقدمة")
        
        # عرض استراتيجيات التسعير المتاحة
        strategy_options = [
            "التسعير القياسي",
            "التسعير المتزن",
            "التسعير غير المتزن",
            "التسعير الموجه للربحية",
            "التسعير بالتجميع",
            "التسعير بالمحتوى المحلي"
        ]
        
        selected_strategy = st.selectbox(
            "اختر استراتيجية التسعير",
            strategy_options,
            key="pricing_strategy_select"
        )
        
        # عرض وصف الاستراتيجية المختارة
        strategy_descriptions = {
            "التسعير القياسي": "تعتمد على تحديد سعر كل بند بناءً على تكلفته الفعلية مضافاً إليها نسبة ربح ثابتة.",
            "التسعير المتزن": "تعتمد على توزيع هامش الربح بشكل متوازن على جميع بنود المشروع مع مراعاة المخاطر.",
            "التسعير غير المتزن": "تعتمد على زيادة أسعار البنود المبكرة في المشروع وتخفيض أسعار البنود المتأخرة.",
            "التسعير الموجه للربحية": "تعتمد على زيادة أسعار البنود ذات التكلفة المنخفضة والكميات الكبيرة.",
            "التسعير بالتجميع": "تعتمد على تجميع البنود المتشابهة وتسعيرها كمجموعة واحدة.",
            "التسعير بالمحتوى المحلي": "تعتمد على زيادة نسبة المحتوى المحلي في المشروع لتحقيق متطلبات الجهات المالكة."
        }
        
        st.info(strategy_descriptions[selected_strategy])
        
        # تطبيق الاستراتيجية المختارة
        if st.button("تطبيق الاستراتيجية", key="apply_strategy_btn"):
            strategy_map = {
                "التسعير القياسي": "standard",
                "التسعير المتزن": "balanced",
                "التسعير غير المتزن": "unbalanced",
                "التسعير الموجه للربحية": "profit_oriented",
                "التسعير بالتجميع": "bundling",
                "التسعير بالمحتوى المحلي": "local_content"
            }
            
            strategy_key = strategy_map[selected_strategy]
            
            # تطبيق الاستراتيجية على المشروع
            result = st.session_state.pricing_strategies.apply_strategy(
                strategy_key,
                st.session_state.project_data,
                st.session_state.smart_price_analysis
            )
            
            if result['success']:
                st.success(f"تم تطبيق استراتيجية {selected_strategy} بنجاح")
                
                # عرض نتائج تطبيق الاستراتيجية
                st.subheader("نتائج تطبيق الاستراتيجية")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**ملخص النتائج:**")
                    st.write(f"- إجمالي التكلفة: {result['total_cost']} ريال")
                    st.write(f"- إجمالي السعر: {result['total_price']} ريال")
                    st.write(f"- هامش الربح: {result['profit_margin']} ريال")
                    st.write(f"- نسبة الربح: {result['profit_percentage']:.2f}%")
                    
                    if 'local_content_percentage' in result:
                        st.write(f"- نسبة المحتوى المحلي: {result['local_content_percentage']:.2f}%")
                
                with col2:
                    # رسم بياني للمقارنة بين التكلفة والسعر
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=['التكلفة', 'السعر'],
                        y=[result['total_cost'], result['total_price']],
                        marker_color=['#1f77b4', '#2ca02c']
                    ))
                    
                    fig.update_layout(
                        title="مقارنة بين التكلفة والسعر",
                        xaxis_title="",
                        yaxis_title="القيمة (ريال)"
                    )
                    
                    st.plotly_chart(fig)
                
                # عرض تفاصيل البنود بعد تطبيق الاستراتيجية
                st.subheader("تفاصيل البنود بعد تطبيق الاستراتيجية")
                
                items_df = pd.DataFrame([
                    {
                        'البند': item['item_code'] + ' - ' + item['description'],
                        'التكلفة': item_result['cost'],
                        'السعر': item_result['price'],
                        'هامش الربح': item_result['profit'],
                        'نسبة الربح': f"{item_result['profit_percentage']:.2f}%"
                    }
                    for item, item_result in zip(
                        st.session_state.project_data['boq_items'],
                        result['items_result']
                    )
                ])
                
                st.dataframe(items_df)
                
                # رسم بياني شريطي للمقارنة بين التكلفة والسعر لكل بند
                fig = px.bar(
                    items_df,
                    x='البند',
                    y=['التكلفة', 'السعر'],
                    title="مقارنة بين التكلفة والسعر لكل بند",
                    barmode='group'
                )
                st.plotly_chart(fig)
            else:
                st.error(f"حدث خطأ أثناء تطبيق الاستراتيجية: {result['message']}")
        
        # مقارنة استراتيجيات التسعير
        st.subheader("مقارنة استراتيجيات التسعير")
        
        if st.button("مقارنة جميع الاستراتيجيات", key="compare_strategies_btn"):
            comparison_result = st.session_state.pricing_strategies.compare_strategies(
                st.session_state.project_data,
                st.session_state.smart_price_analysis
            )
            
            if comparison_result['success']:
                st.success("تمت مقارنة استراتيجيات التسعير بنجاح")
                
                # عرض نتائج المقارنة
                comparison_df = pd.DataFrame([
                    {
                        'الاستراتيجية': strategy_options[i],
                        'إجمالي التكلفة': result['total_cost'],
                        'إجمالي السعر': result['total_price'],
                        'هامش الربح': result['profit_margin'],
                        'نسبة الربح': f"{result['profit_percentage']:.2f}%",
                        'نسبة المحتوى المحلي': f"{result.get('local_content_percentage', 0):.2f}%"
                    }
                    for i, result in enumerate(comparison_result['strategies_result'])
                ])
                
                st.dataframe(comparison_df)
                
                # رسم بياني للمقارنة بين الاستراتيجيات
                fig = px.bar(
                    comparison_df,
                    x='الاستراتيجية',
                    y=['إجمالي التكلفة', 'إجمالي السعر', 'هامش الربح'],
                    title="مقارنة بين استراتيجيات التسعير",
                    barmode='group'
                )
                st.plotly_chart(fig)
                
                # رسم بياني لنسبة الربح
                profit_df = pd.DataFrame([
                    {
                        'الاستراتيجية': strategy_options[i],
                        'نسبة الربح': result['profit_percentage']
                    }
                    for i, result in enumerate(comparison_result['strategies_result'])
                ])
                
                fig = px.bar(
                    profit_df,
                    x='الاستراتيجية',
                    y='نسبة الربح',
                    title="مقارنة نسبة الربح بين استراتيجيات التسعير"
                )
                st.plotly_chart(fig)
                
                # رسم بياني لنسبة المحتوى المحلي
                local_content_df = pd.DataFrame([
                    {
                        'الاستراتيجية': strategy_options[i],
                        'نسبة المحتوى المحلي': result.get('local_content_percentage', 0)
                    }
                    for i, result in enumerate(comparison_result['strategies_result'])
                ])
                
                fig = px.bar(
                    local_content_df,
                    x='الاستراتيجية',
                    y='نسبة المحتوى المحلي',
                    title="مقارنة نسبة المحتوى المحلي بين استراتيجيات التسعير"
                )
                st.plotly_chart(fig)
            else:
                st.error(f"حدث خطأ أثناء مقارنة الاستراتيجيات: {comparison_result['message']}")
    
    def _render_resource_catalogs_tab(self):
        """
        دالة عرض علامة تبويب كتالوجات الموارد
        """
        st.header("كتالوجات الموارد")
        
        tab1, tab2, tab3, tab4 = st.tabs(["المعدات", "المواد", "العمالة", "مقاولي الباطن"])
        
        with tab1:
            st.subheader("كتالوج المعدات")
            
            # عرض قائمة المعدات
            equipment_list = st.session_state.equipment_catalog.get_equipment_list()
            
            if equipment_list:
                equipment_df = pd.DataFrame([
                    {
                        'المعدة': equipment,
                        'النوع': st.session_state.equipment_catalog.get_equipment_details(equipment)['type'],
                        'سعر الساعة': st.session_state.equipment_catalog.get_equipment_details(equipment)['price_per_hour'],
                        'سعر اليوم': st.session_state.equipment_catalog.get_equipment_details(equipment)['price_per_day'],
                        'سعر الأسبوع': st.session_state.equipment_catalog.get_equipment_details(equipment)['price_per_week'],
                        'سعر الشهر': st.session_state.equipment_catalog.get_equipment_details(equipment)['price_per_month'],
                        'محلي': "نعم" if st.session_state.equipment_catalog.get_equipment_details(equipment)['is_local'] else "لا"
                    }
                    for equipment in equipment_list
                ])
                
                st.dataframe(equipment_df)
            else:
                st.info("لا توجد معدات في الكتالوج")
            
            # إضافة معدة جديدة
            st.subheader("إضافة معدة جديدة")
            
            with st.form("add_equipment_form"):
                equipment_name = st.text_input("اسم المعدة")
                equipment_type = st.selectbox(
                    "نوع المعدة",
                    [
                        "حفار", "لودر", "بلدوزر", "جريدر", "دكاك", "شاحنة", "خلاطة خرسانة",
                        "رافعة", "مولد كهرباء", "مضخة مياه", "كسارة", "معدة أخرى"
                    ]
                )
                equipment_description = st.text_area("وصف المعدة")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    price_per_hour = st.number_input("سعر الساعة (ريال)", min_value=0.0, step=10.0)
                    price_per_day = st.number_input("سعر اليوم (ريال)", min_value=0.0, step=100.0)
                
                with col2:
                    price_per_week = st.number_input("سعر الأسبوع (ريال)", min_value=0.0, step=500.0)
                    price_per_month = st.number_input("سعر الشهر (ريال)", min_value=0.0, step=1000.0)
                
                is_local = st.checkbox("معدة محلية")
                
                submit_button = st.form_submit_button("إضافة المعدة")
                
                if submit_button:
                    if equipment_name:
                        equipment_details = {
                            'name': equipment_name,
                            'type': equipment_type,
                            'description': equipment_description,
                            'price_per_hour': price_per_hour,
                            'price_per_day': price_per_day,
                            'price_per_week': price_per_week,
                            'price_per_month': price_per_month,
                            'is_local': is_local
                        }
                        
                        st.session_state.equipment_catalog.add_equipment(equipment_name, equipment_details)
                        st.success(f"تمت إضافة {equipment_name} بنجاح")
                        st.experimental_rerun()
                    else:
                        st.error("يرجى إدخال اسم المعدة")
            
            # استيراد كتالوج المعدات من Excel
            st.subheader("استيراد كتالوج المعدات من Excel")
            
            uploaded_file = st.file_uploader("اختر ملف Excel", type=["xlsx", "xls"], key="equipment_catalog_uploader")
            if uploaded_file is not None:
                if st.button("استيراد الكتالوج", key="import_equipment_catalog_btn"):
                    try:
                        result = st.session_state.equipment_catalog.import_from_excel(uploaded_file)
                        st.success(f"تم استيراد {result['count']} معدة بنجاح")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء استيراد الكتالوج: {str(e)}")
        
        with tab2:
            st.subheader("كتالوج المواد")
            
            # عرض قائمة المواد
            materials_list = st.session_state.materials_catalog.get_materials_list()
            
            if materials_list:
                materials_df = pd.DataFrame([
                    {
                        'المادة': material,
                        'الوصف': st.session_state.materials_catalog.get_material_details(material)['description'],
                        'الوحدة': st.session_state.materials_catalog.get_material_details(material)['unit'],
                        'السعر': st.session_state.materials_catalog.get_material_details(material)['price'],
                        'محلي': "نعم" if st.session_state.materials_catalog.get_material_details(material)['is_local'] else "لا"
                    }
                    for material in materials_list
                ])
                
                st.dataframe(materials_df)
            else:
                st.info("لا توجد مواد في الكتالوج")
            
            # إضافة مادة جديدة
            st.subheader("إضافة مادة جديدة")
            
            with st.form("add_material_form"):
                material_name = st.text_input("اسم المادة")
                material_description = st.text_area("وصف المادة")
                material_unit = st.selectbox(
                    "وحدة القياس",
                    ["م3", "م2", "م.ط", "طن", "كجم", "لتر", "قطعة", "حزمة", "وحدة"]
                )
                material_price = st.number_input("السعر (ريال)", min_value=0.0, step=1.0)
                is_local = st.checkbox("مادة محلية")
                
                submit_button = st.form_submit_button("إضافة المادة")
                
                if submit_button:
                    if material_name:
                        material_details = {
                            'name': material_name,
                            'description': material_description,
                            'unit': material_unit,
                            'price': material_price,
                            'is_local': is_local
                        }
                        
                        st.session_state.materials_catalog.add_material(material_name, material_details)
                        st.success(f"تمت إضافة {material_name} بنجاح")
                        st.experimental_rerun()
                    else:
                        st.error("يرجى إدخال اسم المادة")
            
            # استيراد كتالوج المواد من Excel
            st.subheader("استيراد كتالوج المواد من Excel")
            
            uploaded_file = st.file_uploader("اختر ملف Excel", type=["xlsx", "xls"], key="materials_catalog_uploader")
            if uploaded_file is not None:
                if st.button("استيراد الكتالوج", key="import_materials_catalog_btn"):
                    try:
                        result = st.session_state.materials_catalog.import_from_excel(uploaded_file)
                        st.success(f"تم استيراد {result['count']} مادة بنجاح")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء استيراد الكتالوج: {str(e)}")
        
        with tab3:
            st.subheader("كتالوج العمالة")
            
            # عرض قائمة العمالة
            labor_list = st.session_state.labor_catalog.get_labor_list()
            
            if labor_list:
                labor_df = pd.DataFrame([
                    {
                        'العمالة': labor,
                        'النوع': st.session_state.labor_catalog.get_labor_details(labor)['type'],
                        'سعر الساعة': st.session_state.labor_catalog.get_labor_details(labor)['price_per_hour'],
                        'سعر اليوم': st.session_state.labor_catalog.get_labor_details(labor)['price_per_day'],
                        'سعر الأسبوع': st.session_state.labor_catalog.get_labor_details(labor)['price_per_week'],
                        'سعر الشهر': st.session_state.labor_catalog.get_labor_details(labor)['price_per_month'],
                        'محلي': "نعم" if st.session_state.labor_catalog.get_labor_details(labor)['is_local'] else "لا"
                    }
                    for labor in labor_list
                ])
                
                st.dataframe(labor_df)
            else:
                st.info("لا توجد عمالة في الكتالوج")
            
            # إضافة عمالة جديدة
            st.subheader("إضافة عمالة جديدة")
            
            with st.form("add_labor_form"):
                labor_name = st.text_input("اسم العمالة")
                labor_type = st.selectbox(
                    "نوع العمالة",
                    [
                        "مهندس مدني", "مهندس معماري", "مهندس ميكانيكي", "مهندس كهربائي",
                        "مساح", "مراقب", "فني", "عامل", "سائق", "حداد", "نجار", "عامل بناء",
                        "كهربائي", "سباك", "دهان", "لحام", "عمالة أخرى"
                    ]
                )
                labor_description = st.text_area("وصف العمالة")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    price_per_hour = st.number_input("سعر الساعة (ريال)", min_value=0.0, step=5.0, key="labor_hour_price")
                    price_per_day = st.number_input("سعر اليوم (ريال)", min_value=0.0, step=50.0, key="labor_day_price")
                
                with col2:
                    price_per_week = st.number_input("سعر الأسبوع (ريال)", min_value=0.0, step=200.0, key="labor_week_price")
                    price_per_month = st.number_input("سعر الشهر (ريال)", min_value=0.0, step=500.0, key="labor_month_price")
                
                is_local = st.checkbox("عمالة محلية")
                
                submit_button = st.form_submit_button("إضافة العمالة")
                
                if submit_button:
                    if labor_name:
                        labor_details = {
                            'name': labor_name,
                            'type': labor_type,
                            'description': labor_description,
                            'price_per_hour': price_per_hour,
                            'price_per_day': price_per_day,
                            'price_per_week': price_per_week,
                            'price_per_month': price_per_month,
                            'is_local': is_local
                        }
                        
                        st.session_state.labor_catalog.add_labor(labor_name, labor_details)
                        st.success(f"تمت إضافة {labor_name} بنجاح")
                        st.experimental_rerun()
                    else:
                        st.error("يرجى إدخال اسم العمالة")
            
            # استيراد كتالوج العمالة من Excel
            st.subheader("استيراد كتالوج العمالة من Excel")
            
            uploaded_file = st.file_uploader("اختر ملف Excel", type=["xlsx", "xls"], key="labor_catalog_uploader")
            if uploaded_file is not None:
                if st.button("استيراد الكتالوج", key="import_labor_catalog_btn"):
                    try:
                        result = st.session_state.labor_catalog.import_from_excel(uploaded_file)
                        st.success(f"تم استيراد {result['count']} عمالة بنجاح")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء استيراد الكتالوج: {str(e)}")
        
        with tab4:
            st.subheader("كتالوج مقاولي الباطن")
            
            # عرض قائمة مقاولي الباطن
            subcontractors_list = st.session_state.subcontractors_catalog.get_subcontractors_list()
            
            if subcontractors_list:
                subcontractors_df = pd.DataFrame([
                    {
                        'مقاول الباطن': subcontractor,
                        'التخصص': st.session_state.subcontractors_catalog.get_subcontractor_details(subcontractor)['specialization'],
                        'الوصف': st.session_state.subcontractors_catalog.get_subcontractor_details(subcontractor)['description'],
                        'معلومات الاتصال': st.session_state.subcontractors_catalog.get_subcontractor_details(subcontractor)['contact_info'],
                        'محلي': "نعم" if st.session_state.subcontractors_catalog.get_subcontractor_details(subcontractor)['is_local'] else "لا"
                    }
                    for subcontractor in subcontractors_list
                ])
                
                st.dataframe(subcontractors_df)
            else:
                st.info("لا يوجد مقاولي باطن في الكتالوج")
            
            # إضافة مقاول باطن جديد
            st.subheader("إضافة مقاول باطن جديد")
            
            with st.form("add_subcontractor_form"):
                subcontractor_name = st.text_input("اسم مقاول الباطن")
                subcontractor_specialization = st.selectbox(
                    "التخصص",
                    [
                        "أعمال كهربائية", "أعمال ميكانيكية", "أعمال سباكة", "أعمال تكييف",
                        "أعمال ITC", "أعمال CCTV", "أنظمة التحكم في الوصول", "شبكات الري",
                        "أعمال الحفر", "أعمال الخرسانة", "أعمال التشطيبات", "أعمال الأسفلت",
                        "أعمال العزل", "أعمال الألمنيوم والزجاج", "تخصص آخر"
                    ]
                )
                subcontractor_description = st.text_area("وصف مقاول الباطن")
                subcontractor_contact_info = st.text_input("معلومات الاتصال")
                is_local = st.checkbox("مقاول باطن محلي")
                
                submit_button = st.form_submit_button("إضافة مقاول الباطن")
                
                if submit_button:
                    if subcontractor_name:
                        subcontractor_details = {
                            'name': subcontractor_name,
                            'specialization': subcontractor_specialization,
                            'description': subcontractor_description,
                            'contact_info': subcontractor_contact_info,
                            'is_local': is_local
                        }
                        
                        st.session_state.subcontractors_catalog.add_subcontractor(subcontractor_name, subcontractor_details)
                        st.success(f"تمت إضافة {subcontractor_name} بنجاح")
                        st.experimental_rerun()
                    else:
                        st.error("يرجى إدخال اسم مقاول الباطن")
            
            # استيراد كتالوج مقاولي الباطن من Excel
            st.subheader("استيراد كتالوج مقاولي الباطن من Excel")
            
            uploaded_file = st.file_uploader("اختر ملف Excel", type=["xlsx", "xls"], key="subcontractors_catalog_uploader")
            if uploaded_file is not None:
                if st.button("استيراد الكتالوج", key="import_subcontractors_catalog_btn"):
                    try:
                        result = st.session_state.subcontractors_catalog.import_from_excel(uploaded_file)
                        st.success(f"تم استيراد {result['count']} مقاول باطن بنجاح")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء استيراد الكتالوج: {str(e)}")
    
    def _render_indirect_support_tab(self):
        """
        دالة عرض علامة تبويب الإدارات المساندة
        """
        st.header("إدارة الإدارات المساندة")
        
        # عرض قائمة الإدارات المساندة
        indirect_departments = st.session_state.indirect_support.get_departments()
        
        if indirect_departments:
            departments_df = pd.DataFrame([
                {
                    'الإدارة': department,
                    'التكلفة الشهرية': st.session_state.indirect_support.get_department_details(department)['monthly_cost'],
                    'عدد الموظفين': st.session_state.indirect_support.get_department_details(department)['employees_count'],
                    'نسبة التخصيص': f"{st.session_state.indirect_support.get_department_details(department)['allocation_percentage']:.2f}%"
                }
                for department in indirect_departments
            ])
            
            st.dataframe(departments_df)
            
            # رسم بياني لتوزيع التكاليف حسب الإدارات
            fig = px.pie(
                departments_df,
                values='التكلفة الشهرية',
                names='الإدارة',
                title="توزيع التكاليف حسب الإدارات المساندة"
            )
            st.plotly_chart(fig)
        else:
            st.info("لا توجد إدارات مساندة")
        
        # إضافة إدارة مساندة جديدة
        st.subheader("إضافة إدارة مساندة جديدة")
        
        with st.form("add_department_form"):
            department_name = st.text_input("اسم الإدارة")
            department_description = st.text_area("وصف الإدارة")
            monthly_cost = st.number_input("التكلفة الشهرية (ريال)", min_value=0.0, step=1000.0)
            employees_count = st.number_input("عدد الموظفين", min_value=0, step=1)
            allocation_percentage = st.slider("نسبة التخصيص للمشروع (%)", min_value=0.0, max_value=100.0, step=5.0)
            
            submit_button = st.form_submit_button("إضافة الإدارة")
            
            if submit_button:
                if department_name:
                    department_details = {
                        'name': department_name,
                        'description': department_description,
                        'monthly_cost': monthly_cost,
                        'employees_count': employees_count,
                        'allocation_percentage': allocation_percentage
                    }
                    
                    st.session_state.indirect_support.add_department(department_name, department_details)
                    st.success(f"تمت إضافة {department_name} بنجاح")
                    st.experimental_rerun()
                else:
                    st.error("يرجى إدخال اسم الإدارة")
        
        # تحليل تكاليف الإدارات المساندة
        st.subheader("تحليل تكاليف الإدارات المساندة")
        
        if indirect_departments:
            # حساب إجمالي تكاليف الإدارات المساندة
            total_monthly_cost = st.session_state.indirect_support.get_total_monthly_cost()
            total_allocated_cost = st.session_state.indirect_support.get_total_allocated_cost()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**إجمالي التكلفة الشهرية للإدارات المساندة:** {total_monthly_cost} ريال")
                st.write(f"**إجمالي التكلفة المخصصة للمشروع:** {total_allocated_cost} ريال")
            
            with col2:
                # رسم بياني للمقارنة بين التكلفة الكلية والتكلفة المخصصة
                fig = go.Figure()
                
                fig.add_trace(go.Bar(
                    x=['التكلفة الشهرية الكلية', 'التكلفة المخصصة للمشروع'],
                    y=[total_monthly_cost, total_allocated_cost],
                    marker_color=['#1f77b4', '#2ca02c']
                ))
                
                fig.update_layout(
                    title="مقارنة بين التكلفة الكلية والتكلفة المخصصة",
                    xaxis_title="",
                    yaxis_title="القيمة (ريال)"
                )
                
                st.plotly_chart(fig)
            
            # توزيع التكاليف المخصصة على بنود المشروع
            st.subheader("توزيع التكاليف المخصصة على بنود المشروع")
            
            distribution_method = st.selectbox(
                "اختر طريقة توزيع التكاليف",
                ["بالتساوي", "حسب قيمة البند", "حسب مدة البند"]
            )
            
            if st.button("توزيع التكاليف", key="distribute_costs_btn"):
                if len(st.session_state.project_data['boq_items']) > 0:
                    distribution_result = st.session_state.indirect_support.distribute_costs(
                        st.session_state.project_data['boq_items'],
                        distribution_method
                    )
                    
                    if distribution_result['success']:
                        st.success("تم توزيع التكاليف بنجاح")
                        
                        # عرض نتائج التوزيع
                        distribution_df = pd.DataFrame([
                            {
                                'البند': item['item_code'] + ' - ' + item['description'],
                                'التكلفة المباشرة': item['direct_cost'] if 'direct_cost' in item else 0,
                                'التكلفة غير المباشرة المخصصة': cost,
                                'إجمالي التكلفة': (item['direct_cost'] if 'direct_cost' in item else 0) + cost
                            }
                            for item, cost in zip(
                                st.session_state.project_data['boq_items'],
                                distribution_result['distributed_costs']
                            )
                        ])
                        
                        st.dataframe(distribution_df)
                        
                        # رسم بياني لتوزيع التكاليف غير المباشرة
                        fig = px.bar(
                            distribution_df,
                            x='البند',
                            y=['التكلفة المباشرة', 'التكلفة غير المباشرة المخصصة'],
                            title="توزيع التكاليف على بنود المشروع",
                            barmode='stack'
                        )
                        st.plotly_chart(fig)
                    else:
                        st.error(f"حدث خطأ أثناء توزيع التكاليف: {distribution_result['message']}")
                else:
                    st.error("لا توجد بنود في المشروع")
        else:
            st.warning("يرجى إضافة إدارات مساندة أولاً")
    
    def _render_local_content_tab(self):
        """
        دالة عرض علامة تبويب المحتوى المحلي
        """
        st.header("تحليل المحتوى المحلي")
        
        # عرض معلومات المحتوى المحلي
        st.write("""
        يهدف تحليل المحتوى المحلي إلى قياس مدى مساهمة المشروع في تحقيق أهداف رؤية 2030 للمملكة العربية السعودية
        من خلال زيادة نسبة المحتوى المحلي في المشاريع والمناقصات.
        """)
        
        # تحديد هدف المحتوى المحلي
        st.subheader("هدف المحتوى المحلي")
        
        local_content_target = st.slider(
            "نسبة المحتوى المحلي المستهدفة (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(st.session_state.project_data['local_content_target'] * 100),
            step=5.0,
            key="local_content_target_slider"
        )
        
        st.session_state.project_data['local_content_target'] = local_content_target / 100
        
        # تحليل المحتوى المحلي الحالي
        st.subheader("تحليل المحتوى المحلي الحالي")
        
        if len(st.session_state.project_data['boq_items']) > 0:
            # حساب نسبة المحتوى المحلي
            local_content_analysis = st.session_state.pricing_strategies.analyze_local_content(
                st.session_state.project_data,
                st.session_state.smart_price_analysis
            )
            
            if local_content_analysis['success']:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**نسبة المحتوى المحلي الحالية:** {local_content_analysis['local_content_percentage']:.2f}%")
                    st.write(f"**النسبة المستهدفة:** {local_content_target:.2f}%")
                    
                    if local_content_analysis['local_content_percentage'] >= local_content_target:
                        st.success("تم تحقيق هدف المحتوى المحلي")
                    else:
                        st.warning(f"لم يتم تحقيق هدف المحتوى المحلي، الفارق: {local_content_target - local_content_analysis['local_content_percentage']:.2f}%")
                
                with col2:
                    # رسم بياني للمقارنة بين النسبة الحالية والنسبة المستهدفة
                    fig = go.Figure()
                    
                    fig.add_trace(go.Bar(
                        x=['النسبة الحالية', 'النسبة المستهدفة'],
                        y=[local_content_analysis['local_content_percentage'], local_content_target],
                        marker_color=['#1f77b4', '#2ca02c']
                    ))
                    
                    fig.update_layout(
                        title="مقارنة بين نسبة المحتوى المحلي الحالية والمستهدفة",
                        xaxis_title="",
                        yaxis_title="النسبة (%)"
                    )
                    
                    st.plotly_chart(fig)
                
                # تحليل المحتوى المحلي حسب نوع الموارد
                st.subheader("تحليل المحتوى المحلي حسب نوع الموارد")
                
                resources_local_content = local_content_analysis['resources_local_content']
                
                resources_df = pd.DataFrame([
                    {
                        'نوع المورد': resource_type,
                        'التكلفة الإجمالية': resources_local_content[resource_type]['total_cost'],
                        'تكلفة الموارد المحلية': resources_local_content[resource_type]['local_cost'],
                        'نسبة المحتوى المحلي': f"{resources_local_content[resource_type]['percentage']:.2f}%"
                    }
                    for resource_type in resources_local_content
                ])
                
                st.dataframe(resources_df)
                
                # رسم بياني لنسبة المحتوى المحلي حسب نوع الموارد
                fig = px.bar(
                    resources_df,
                    x='نوع المورد',
                    y=['التكلفة الإجمالية', 'تكلفة الموارد المحلية'],
                    title="تحليل المحتوى المحلي حسب نوع الموارد",
                    barmode='group'
                )
                st.plotly_chart(fig)
                
                # رسم بياني لنسبة المحتوى المحلي حسب نوع الموارد
                percentages = [resources_local_content[resource_type]['percentage'] for resource_type in resources_local_content]
                resource_types = list(resources_local_content.keys())
                
                fig = px.bar(
                    x=resource_types,
                    y=percentages,
                    title="نسبة المحتوى المحلي حسب نوع الموارد",
                    labels={'x': 'نوع المورد', 'y': 'نسبة المحتوى المحلي (%)'}
                )
                st.plotly_chart(fig)
                
                # توصيات لتحسين نسبة المحتوى المحلي
                st.subheader("توصيات لتحسين نسبة المحتوى المحلي")
                
                if local_content_analysis['local_content_percentage'] < local_content_target:
                    recommendations = local_content_analysis['recommendations']
                    
                    for i, recommendation in enumerate(recommendations):
                        st.write(f"{i+1}. {recommendation}")
                    
                    # تطبيق استراتيجية المحتوى المحلي
                    st.subheader("تطبيق استراتيجية المحتوى المحلي")
                    
                    if st.button("تطبيق استراتيجية المحتوى المحلي", key="apply_local_content_strategy_btn"):
                        result = st.session_state.pricing_strategies.apply_strategy(
                            'local_content',
                            st.session_state.project_data,
                            st.session_state.smart_price_analysis
                        )
                        
                        if result['success']:
                            st.success("تم تطبيق استراتيجية المحتوى المحلي بنجاح")
                            
                            # عرض نتائج تطبيق الاستراتيجية
                            st.write(f"**نسبة المحتوى المحلي بعد تطبيق الاستراتيجية:** {result['local_content_percentage']:.2f}%")
                            
                            if result['local_content_percentage'] >= local_content_target:
                                st.success("تم تحقيق هدف المحتوى المحلي بنجاح")
                            else:
                                st.warning(f"لم يتم تحقيق هدف المحتوى المحلي بالكامل، الفارق: {local_content_target - result['local_content_percentage']:.2f}%")
                        else:
                            st.error(f"حدث خطأ أثناء تطبيق الاستراتيجية: {result['message']}")
                else:
                    st.success("تم تحقيق هدف المحتوى المحلي بالفعل")
            else:
                st.error(f"حدث خطأ أثناء تحليل المحتوى المحلي: {local_content_analysis['message']}")
        else:
            st.warning("لا توجد بنود في المشروع")
from pricing_system.modules.analysis.market_analysis import MarketAnalysis
from pricing_system.modules.analysis.smart_price_analysis import SmartPriceAnalysis
from modules.risk_analysis.risk_analyzer import RiskAnalyzer

class IntegratedPricingSystem:
    def __init__(self):
        self.market_analysis = MarketAnalysis()
        self.smart_analysis = SmartPriceAnalysis()
        self.risk_analyzer = RiskAnalyzer()
        
        if 'integrated_data' not in st.session_state:
            self._initialize_integrated_data()
    
    def _initialize_integrated_data(self):
        st.session_state.integrated_data = {
            'market_trends': {},
            'risk_analysis': {},
            'price_analysis': {},
            'local_content': {}
        }
    
    def render(self):
        st.title("نظام التسعير المتكامل")
        
        tabs = st.tabs([
            "تحليل السوق",
            "تحليل المخاطر",
            "التحليل الذكي للأسعار",
            "المحتوى المحلي"
        ])
        
        with tabs[0]:
            self.market_analysis.render()
        
        with tabs[1]:
            self.risk_analyzer.render_risk_analysis(st.session_state.project_data)
        
        with tabs[2]:
            self.smart_analysis.render()
        
        with tabs[3]:
            self._render_local_content()
    
    def _render_local_content(self):
        st.header("تحليل المحتوى المحلي")
        # إضافة تحليل المحتوى المحلي هنا
