import streamlit as st
import pandas as pd
from pricing_system.modules.stages.project_entry import render_project_entry
from pricing_system.modules.pricing_strategies import balanced_pricing
from pricing_system.modules.indirect_support import overheads
from pricing_system.modules.analysis.smart_price_analysis import SmartPriceAnalysis
from pricing_system.modules.analysis.market_analysis import MarketAnalysis

import openpyxl

from pricing_system.modules.risk_analysis.risk_analyzer import RiskAnalyzer
from pricing_system.modules.reference_guides.pricing_guidelines import PricingGuidelines
import os
from datetime import datetime
import pdfkit

class ReferenceGuides:
    def render(self):
        st.title("المراجع والأدلة")
        st.markdown("## دليل تحليل أسعار بنود الإنشاءات")
        st.markdown("**المرجع الأول:** [رابط للمرجع الأول](link_to_reference_1)")
        st.markdown("**المرجع الثاني:** [رابط للمرجع الثاني](link_to_reference_2)")


class IntegratedApp:
    def __init__(self):
        from config_manager import ConfigManager
        config_manager = ConfigManager()
        config_manager.set_page_config_if_needed(
            page_title="نظام التسعير المتكامل",
            page_icon="💰",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        if 'pricing_stage' not in st.session_state:
            st.session_state.pricing_stage = 1

        if 'current_project' not in st.session_state:
            st.session_state.current_project = {
                'name': '',
                'code': '',
                'boq_items': [],
                'indirect_costs': {
                    'overhead': 0.15,
                    'profit': 0.10,
                    'risk': 0.05
                }
            }
        elif 'boq_items' not in st.session_state.current_project:
            st.session_state.current_project['boq_items'] = []

        self.smart_analysis = SmartPriceAnalysis()
        self.market_analysis = MarketAnalysis()
        self.risk_analyzer = RiskAnalyzer()
        self.reference_guides = ReferenceGuides()

    def run(self):
        st.markdown("""
            <style>
                .main-title {
                    color: #1f77b4;
                    font-size: 2rem;
                    text-align: center;
                    margin-bottom: 2rem;
                }
                .sidebar-title {
                    font-size: 1.2rem;
                    font-weight: bold;
                    margin-bottom: 1rem;
                }
                .stage-number {
                    background-color: #1f77b4;
                    color: white;
                    padding: 0.2rem 0.5rem;
                    border-radius: 50%;
                    margin-right: 0.5rem;
                }
            </style>
        """, unsafe_allow_html=True)

        st.markdown('<h1 class="main-title">نظام التسعير المتكامل</h1>', unsafe_allow_html=True)
        st.sidebar.markdown('<div class="sidebar-title">مراحل التسعير</div>', unsafe_allow_html=True)

        self._render_sidebar_stages()

        if st.session_state.pricing_stage == 1:
            self._render_project_entry()
        elif st.session_state.pricing_stage == 2:
            self._render_boq_items()
        elif st.session_state.pricing_stage == 3:
            self._render_price_analysis()
        elif st.session_state.pricing_stage == 4:
            self._render_risk_analysis()
        elif st.session_state.pricing_stage == 5:
            self._render_pricing_strategies()
        elif st.session_state.pricing_stage == 6:
            self._render_local_content()
        elif st.session_state.pricing_stage == 7:
            self._render_final_boq()
        elif st.session_state.pricing_stage == 8:
            self._render_reference_guides()

        self._render_navigation()

    def _render_sidebar_stages(self):
        st.sidebar.markdown("### مراحل التسعير")
        stages = [
            "بيانات المشروع",
            "جدول الكميات",
            "تحليل الأسعار",
            "تحليل المخاطر",
            "استراتيجيات التسعير",
            "المحتوى المحلي",
            "الجدول النهائي",
            "المراجع والأدلة"
        ]
        for i, stage in enumerate(stages, 1):
            if st.session_state.pricing_stage > i:
                status = "✓"
            elif st.session_state.pricing_stage == i:
                status = "🔄"
            else:
                status = ""
            st.sidebar.markdown(f"{i}. {stage} {status}")

    def _render_project_entry(self):
        st.title("بيانات المشروع")

        if 'current_project' not in st.session_state:
            st.session_state.current_project = {}
            st.session_state.show_entry_form = True

        if st.session_state.get('show_entry_form', True):
            st.subheader("إدخال بيانات المشروع")
            with st.form("project_entry_form"):
                col1, col2 = st.columns(2)

                with col1:
                    name = st.text_input("اسم المشروع")
                    code = st.text_input("رقم المشروع")
                    location = st.text_input("الموقع")

                with col2:
                    start_date = st.date_input("تاريخ البدء")
                    duration = st.number_input("مدة المشروع (يوم)", min_value=1, value=180)
                    budget = st.number_input("الميزانية (ريال)", min_value=0.0, step=1000.0)

                description = st.text_area("وصف المشروع")

                if st.form_submit_button("حفظ البيانات"):
                    st.session_state.current_project.update({
                        'name': name,
                        'code': code,
                        'location': location,
                        'start_date': start_date,
                        'duration': duration,
                        'budget': budget,
                        'description': description
                    })
                    st.session_state.show_entry_form = False
                    st.success("تم حفظ بيانات المشروع بنجاح!")
                    st.rerun()

        else:
            st.subheader("بيانات المشروع المحفوظة")
            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"**اسم المشروع:** {st.session_state.current_project.get('name', '')}")
                st.markdown(f"**رقم المشروع:** {st.session_state.current_project.get('code', '')}")
                st.markdown(f"**الموقع:** {st.session_state.current_project.get('location', '')}")

            with col2:
                st.markdown(f"**تاريخ البدء:** {st.session_state.current_project.get('start_date', '')}")
                st.markdown(f"**مدة المشروع:** {st.session_state.current_project.get('duration', '')} يوم")
                st.markdown(f"**الميزانية:** {st.session_state.current_project.get('budget', '')} ريال")

            st.markdown(f"**الوصف:** {st.session_state.current_project.get('description', '')}")

            if st.button("تعديل البيانات"):
                st.session_state.show_entry_form = True
                st.rerun()

    def _render_boq_items(self):
        st.title("جدول الكميات")
        tabs = st.tabs(["إدخال البنود", "استيراد/تصدير جدول الكميات", "تحليل البنود"])

        with tabs[0]:
            st.subheader("إضافة بند جديد")
            st.markdown("### إضافة بند جديد")
            new_item_type = st.selectbox("نوع البند", ["عمالة", "معدات", "مواد"])

            col1, col2, col3 = st.columns(3)
            with col1:
                item_name = st.text_input("اسم البند")
            with col2:
                item_quantity = st.number_input("الكمية", min_value=0.0, step=0.1)
            with col3:
                item_price = st.number_input("السعر", min_value=0.0, step=0.1)

            if st.button("إضافة البند"):
                new_item = {
                    "type": new_item_type,
                    "name": item_name,
                    "quantity": item_quantity,
                    "price": item_price,
                    "total": item_quantity * item_price
                }

                if new_item_type == "عمالة":
                    if 'labor' not in st.session_state.current_project:
                        st.session_state.current_project['labor'] = []
                    st.session_state.current_project['labor'].append(new_item)
                elif new_item_type == "معدات":
                    if 'equipment' not in st.session_state.current_project:
                        st.session_state.current_project['equipment'] = []
                    st.session_state.current_project['equipment'].append(new_item)
                else:
                    if 'materials' not in st.session_state.current_project:
                        st.session_state.current_project['materials'] = []
                    st.session_state.current_project['materials'].append(new_item)

                st.success(f"تم إضافة {item_name} بنجاح")
                st.rerun()


        with st.form("boq_item_form"):
            col1, col2 = st.columns(2)

            with col1:
                item_code = st.text_input("كود البند")
                item_desc = st.text_area("وصف البند")
                quantity = st.number_input("الكمية", min_value=0.0)

            with col2:
                unit = st.selectbox("الوحدة", ["متر مربع", "متر مكعب", "متر طولي", "عدد", "طن", "كجم"])
                unit_price = st.number_input("سعر الوحدة", min_value=0.0)

            if st.form_submit_button("إضافة البند"):
                if not item_code or not item_desc or quantity <= 0 or unit_price <= 0:
                    st.error("يرجى إدخال جميع البيانات المطلوبة")
                else:
                    new_item = {
                        'code': item_code,
                        'description': item_desc,
                        'unit': unit,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total_price': quantity * unit_price
                    }
                    st.session_state.current_project['boq_items'].append(new_item)
                    st.success("تم إضافة البند بنجاح")
                    st.rerun()

        with tabs[1]:
            st.subheader("استيراد/تصدير جدول الكميات")

            uploaded_file = st.file_uploader("رفع ملف جدول كميات", type=['xlsx', 'xls'], key="boq_upload")
            if uploaded_file:
                try:
                    df = pd.read_excel(uploaded_file)
                    st.write("معاينة البيانات:")
                    st.dataframe(df)

                    if st.button("تأكيد استيراد البيانات", key="confirm_import"):
                        for _, row in df.iterrows():
                            new_item = {
                                'code': str(row.get('كود البند', '')),
                                'description': str(row.get('وصف البند', '')),
                                'unit': str(row.get('الوحدة', '')),
                                'quantity': float(row.get('الكمية', 0)),
                                'unit_price': float(row.get('سعر الوحدة', 0)),
                                'total_price': float(row.get('السعر الإجمالي', 0))
                            }
                            st.session_state.current_project['boq_items'].append(new_item)
                        st.success("تم استيراد البيانات بنجاح")
                        st.rerun()
                except Exception as e:
                    st.error(f"حدث خطأ أثناء استيراد الملف: {str(e)}")

            st.divider()

            if st.session_state.current_project.get('boq_items'):
                if st.button("تصدير جدول الكميات الحالي", key="export_current_boq"):
                    try:
                        df = pd.DataFrame(st.session_state.current_project['boq_items'])
                        # Rename columns to Arabic
                        df = df.rename(columns={
                            'code': 'كود البند',
                            'description': 'وصف البند',
                            'unit': 'الوحدة',
                            'quantity': 'الكمية',
                            'unit_price': 'سعر الوحدة',
                            'total_price': 'السعر الإجمالي'
                        })

                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        excel_file = f"data/exports/boq_{timestamp}.xlsx"
                        os.makedirs("data/exports", exist_ok=True)
                        df.to_excel(excel_file, index=False)

                        with open(excel_file, 'rb') as f:
                            st.download_button(
                                label="تحميل الملف",
                                data=f,
                                file_name=f"boq_{timestamp}.xlsx",
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key="download_boq"
                            )
                    except Exception as e:
                        st.error(f"حدث خطأ أثناء تصدير الملف: {str(e)}")

        with tabs[2]:
            st.subheader("تحليل البنود")
            if st.session_state.current_project.get('boq_items'):
                df = pd.DataFrame(st.session_state.current_project['boq_items'])

                categories = ["أعمال ترابية", "أعمال خرسانية", "أعمال حديد", "أعمال بناء", "أعمال تشطيبات"]
                selected_category = st.selectbox("اختر فئة البند", categories)

                if 'category' in df.columns:
                    category_items = df[df['category'] == selected_category]
                    if not category_items.empty:
                        st.write("### البنود المتاحة في هذه الفئة:")
                        for _, item in category_items.iterrows():
                            st.write(f"- {item['description']}")
                    else:
                        st.info("لا توجد بنود في هذه الفئة")

                total_cost = df['total_price'].sum()
                st.metric("إجمالي التكاليف", f"{total_cost:,.2f} ريال")

                st.subheader("توزيع التكاليف حسب الوحدات")
                unit_costs = df.groupby('unit')['total_price'].sum()
                st.bar_chart(unit_costs)

                st.subheader("البنود الأعلى تكلفة")
                top_items = df.nlargest(5, 'total_price')[['code', 'description', 'total_price']]
                st.dataframe(top_items)

                st.subheader("تحليل تفصيلي للبند")
                selected_item = st.selectbox("اختر بند للتحليل", df['code'].tolist())
                if selected_item:
                    item = df[df['code'] == selected_item].iloc[0]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**الوصف:**", item['description'])
                        st.write("**الكمية:**", item['quantity'])
                    with col2:
                        st.write("**سعر الوحدة:**", f"{item['unit_price']:,.2f} ريال")
                        st.write("**الإجمالي:**", f"{item['total_price']:,.2f} ريال")
            else:
                st.warning("لا توجد بنود للتحليل. الرجاء إضافة بنود أولاً.")

        if st.session_state.current_project['boq_items']:
            st.markdown("### البنود المضافة")

            for idx, item in enumerate(st.session_state.current_project['boq_items']):
                st.markdown(f"### البند {idx+1}: {item['description'][:50]}...")
                col1, col2, col3 = st.columns([2,2,1])

                with col1:
                    st.text_input("كود البند", value=item['code'], key=f"code_{idx}")
                    st.text_area("وصف البند", value=item['description'], key=f"desc_{idx}")

                if st.checkbox(f"عرض تحليل مكونات البند {idx+1}", key=f"show_analysis_{idx}"):
                    with st.expander("تحليل مكونات البند"):
                            # المواد
                            st.subheader("المواد")
                            materials_container = st.container()
                            with materials_container:
                                if 'materials' not in st.session_state:
                                    st.session_state.materials = []
                                materials = st.session_state.materials

                                for i in range(len(materials)):
                                    cols = st.columns([3, 2, 2, 1])
                                    with cols[0]:
                                        materials[i]['name'] = st.selectbox(f"المادة {i+1}", ["اسمنت", "رمل", "حصى", "حديد"], key=f"mat_{idx}_{i}", index = 0 if materials[i]['name'] == "" else ["اسمنت", "رمل", "حصى", "حديد"].index(materials[i]['name']))
                                    with cols[1]:
                                        unit_col1, unit_col2 = st.columns(2)
                                        with unit_col1:
                                            materials[i]['unit'] = st.selectbox(
                                                "وحدة القياس",
                                                ["متر مربع", "متر مكعب", "متر طولي", "رول", "بوكس", "كجم", "طن", "عدد", "لتر"],
                                                key=f"mat_unit_{idx}_{i}"
                                            )
                                        with unit_col2:
                                            try:
                                                current_qty = float(materials[i]['quantity'])
                                            except (ValueError, TypeError):
                                                current_qty = 0.0
                                            materials[i]['quantity'] = st.number_input(
                                                "الكمية",
                                                min_value=0.0,
                                                value=current_qty,
                                                key=f"mat_qty_{idx}_{i}"
                                            )
                                    with cols[2]:
                                        try:
                                            current_price = float(materials[i]['price'])
                                        except (ValueError, TypeError):
                                            current_price = 0.0
                                        materials[i]['price'] = st.number_input("السعر", min_value=0.0, value=current_price, key=f"mat_price_{idx}_{i}")
                                    with cols[3]:
                                        materials[i]['total'] = materials[i]['quantity'] * materials[i]['price']
                                        st.text(f"{materials[i]['total']:.2f}")
                                        if st.button("🗑️ حذف", key=f"delete_mat_{idx}_{i}"):
                                            if len(materials) > i:
                                                materials.pop(i)
                                                st.rerun()

                                if st.button("➕ إضافة مادة جديدة", key=f"add_mat_{idx}"):
                                    materials.append({
                                        "name": "",
                                        "quantity": 0,
                                        "price": 0,
                                        "total": 0
                                    })
                                    st.rerun()

                                # العمالة
                                st.subheader("العمالة")
                                with st.container():
                                    labor_container = st.container()
                                    with labor_container:
                                        if 'labor' not in st.session_state:
                                            st.session_state.labor = []
                                        labor = st.session_state.labor

                                        for i in range(len(labor)):
                                            cols = st.columns([3, 2, 2, 1])
                                            with cols[0]:
                                                labor[i]['name'] = st.selectbox(f"العامل {i+1}", ["نجار", "حداد", "عامل", "فني"], key=f"labor_{idx}_{i}")
                                            with cols[1]:
                                                labor[i]['quantity'] = st.number_input("العدد", min_value=0, value=labor[i].get('quantity', 0), key=f"labor_qty_{idx}_{i}")
                                            with cols[2]:
                                                current_price = float(labor[i].get('price', 0.0))
                                                labor[i]['price'] = st.number_input("الأجر اليومي", min_value=0.0, value=current_price, key=f"labor_price_{idx}_{i}")
                                            with cols[3]:
                                                labor[i]['total'] = labor[i]['quantity'] * labor[i]['price']
                                                st.text(f"{labor[i]['total']:.2f}")
                                                if st.button("🗑️ حذف", key=f"delete_labor_{idx}_{i}"):
                                                    if len(labor) > i:
                                                        labor.pop(i)
                                                        st.rerun()

                                        if st.button("➕ إضافة عامل جديد", key=f"add_labor_{idx}"):
                                            labor.append({
                                                "name": "",
                                                "quantity": 0,
                                                "price": 0,
                                                "total": 0
                                            })
                                            st.rerun()

                                    # المعدات
                                    st.subheader("المعدات")
                                    equipment_container = st.container()
                                    with equipment_container:
                                        if 'equipment' not in st.session_state:
                                            st.session_state.equipment = []
                                        equipment = st.session_state.equipment

                                        for i in range(len(equipment)):
                                            cols = st.columns([3, 2, 2, 1])
                                            with cols[0]:
                                                equipment[i]['name'] = st.selectbox(f"المعدة {i+1}", ["خلاطة", "هزاز", "ونش", "مضخة"], key=f"equip_{idx}_{i}")
                                            with cols[1]:
                                                equipment[i]['quantity'] = st.number_input("العدد", min_value=0, value=int(equipment[i].get('quantity', 0)), key=f"equip_qty_{idx}_{i}")
                                            with cols[2]:
                                                current_price = float(equipment[i].get('price', 0.0))
                                                equipment[i]['price'] = st.number_input("السعر اليومي", min_value=0.0, value=current_price, key=f"equip_price_{idx}_{i}")
                                            with cols[3]:
                                                equipment[i]['total'] = equipment[i]['quantity'] * equipment[i]['price']
                                                st.text(f"{equipment[i]['total']:.2f}")
                                                if st.button("🗑️ حذف", key=f"delete_equip_{idx}_{i}"):
                                                    if len(equipment) > i:
                                                        equipment.pop(i)
                                                        st.rerun()

                                        if st.button("➕ إضافة معدة جديدة", key=f"add_equip_{idx}"):
                                            equipment.append({
                                                "name": "",
                                                "quantity": 0,
                                                "price": 0,
                                                "total": 0
                                            })
                                            st.rerun()
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("➕ إضافة بند جديد", key=f"add_item_{idx}"):
                                    if 'materials' not in st.session_state:
                                        st.session_state.materials = []
                                    st.session_state.materials.append({
                                        "name": "",
                                        "quantity": 0,
                                        "price": 0,
                                        "total": 0
                                    })
                                    st.rerun()
                            with col2:
                                if st.button("❌ حذف البند", key=f"delete_item_{idx}"):
                                    if len(st.session_state.materials) > 0:
                                        st.session_state.materials.pop()
                                        st.rerun()

                            total_materials = sum(m["total"] for m in materials)
                            total_labor = sum(l["total"] for l in labor)
                            total_equipment = sum(e["total"] for e in equipment)
                            total_cost = total_materials + total_labor + total_equipment

                            st.markdown("---")
                            st.subheader("ملخص التكاليف والحاسبة")

                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("تكلفة المواد", f"{total_materials:.2f}")
                            with col2:
                                st.metric("تكلفة العمالة", f"{total_labor:.2f}")
                            with col3:
                                st.metric("تكلفة المعدات", f"{total_equipment:.2f}")
                            with col4:
                                st.metric("التكلفة الإجمالية", f"{total_cost:.2f}")

                            st.markdown("### الحاسبة")
                            calc_col1, calc_col2, calc_col3 = st.columns([2,1,2])

                            with calc_col1:
                                num1 = st.number_input("الرقم الأول", value=0.0, format="%.2f")
                                num2 = st.number_input("الرقم الثاني", value=0.0, format="%.2f")

                            with calc_col2:
                                operation = st.selectbox("العملية", ['+', '-', '×', '÷'])

                            with calc_col3:
                                if operation == '+':
                                    result = num1 + num2
                                elif operation == '-':
                                    result = num1 - num2
                                elif operation == '×':
                                    result = num1 * num2
                                elif operation == '÷':
                                    result = num1 / num2 if num2 != 0 else 0

                                st.metric("النتيجة", f"{result:.2f}")

                            unit_cost = total_cost / quantity if quantity > 0 else 0
                            st.success(f"تكلفة الوحدة: {unit_cost:.2f}")

                            if st.button("تطبيق السعر", key=f"apply_price_{idx}"):
                                item['unit_price'] = unit_cost
                                item['total_price'] = unit_cost * quantity
                                st.success("تم تحديث سعر البند")
                                st.rerun()

                with col2:
                    units_list = ["م3", "م2", "متر طولي", "عدد", "متر مربع", "طن", "كجم"]
                    try:
                        default_index = units_list.index(item['unit'])
                    except ValueError:
                        default_index = 0
                    unit = st.selectbox("الوحدة", units_list, key=f"unit_{idx}", index=default_index)
                    quantity = st.number_input("الكمية", value=float(item['quantity']), key=f"quantity_{idx}")


                with col3:
                    unit_price = st.number_input("سعر الوحدة", value=float(item['unit_price']), key=f"price_{idx}")
                    if st.button("تحديث البند", key=f"update_{idx}"):
                        st.session_state.current_project['boq_items'][idx].update({
                            'code': st.session_state[f"code_{idx}"],
                            'description': st.session_state[f"desc_{idx}"],
                            'unit': st.session_state[f"unit_{idx}"],
                            'quantity': st.session_state[f"quantity_{idx}"],
                            'unit_price': st.session_state[f"price_{idx}"],
                            'total_price': st.session_state[f"quantity_{idx}"] * st.session_state[f"price_{idx}"]
                        })
                        st.success("تم تحديث البند بنجاح")
                        st.rerun()

                    if st.button("حذف البند", key=f"delete_{idx}"):
                        st.session_state.current_project['boq_items'].pop(idx)
                        st.success("تم حذف البند بنجاح")
                        st.rerun()

            df = pd.DataFrame(st.session_state.current_project['boq_items'])
            column_names = {
                'code': 'كود البند',
                'description': 'وصف البند',
                'unit': 'الوحدة',
                'quantity': 'الكمية',
                'unit_price': 'سعر الوحدة',
                'total_price': 'السعر الإجمالي'
            }
            df = df.rename(columns=column_names)
            st.markdown("### ملخص البنود")
            st.dataframe(df, use_container_width=True)

    def _render_price_analysis(self):
        st.title("تحليل الأسعار")
        tabs = st.tabs(["تحليل البنود", "تحليل التكاليف", "تحليل السوق", "التحليل الذكي"])

        with tabs[0]:
            if 'current_project' in st.session_state and 'boq_items' in st.session_state.current_project:
                df = pd.DataFrame(st.session_state.current_project['boq_items'])
                if not df.empty:
                    # تغيير أسماء الأعمدة إلى العربية
                    df = df.rename(columns={
                        'code': 'كود البند',
                        'description': 'وصف البند',
                        'unit': 'الوحدة',
                        'quantity': 'الكمية',
                        'unit_price': 'سعر الوحدة',
                        'total_price': 'السعر الإجمالي'
                    })
                    st.dataframe(df)

                    selected_item = st.selectbox("اختر بند للتحليل", df['كود البند'].tolist())
                    if selected_item:
                        item = df[df['كود البند'] == selected_item].iloc[0]
                        st.write("### تفاصيل البند")
                        st.write(f"الوصف: {item['وصف البند']}")
                        st.write(f"الكمية: {item['الكمية']}")
                        st.write(f"سعر الوحدة: {item['سعر الوحدة']}")
                        st.write(f"الإجمالي: {item['السعر الإجمالي']}")
                else:
                    st.warning("لا توجد بنود مضافة بعد")
            else:
                st.warning("الرجاء إضافة بنود للمشروع أولاً")

        with tabs[1]:
            self._render_cost_analysis()
        with tabs[2]:
            self.market_analysis.render()
        with tabs[3]:
            self.smart_analysis.render()

    def _render_cost_analysis(self):
        if not st.session_state.current_project['boq_items']:
            st.warning("لا توجد بنود لتحليلها")
            return

        total_direct_cost = sum(item['total_price'] for item in st.session_state.current_project['boq_items'])
        indirect_costs = st.session_state.current_project['indirect_costs']

        st.markdown("### ملخص التكاليف")
        col1, col2 = st.columns(2)

        with col1:
            st.metric("إجمالي التكاليف المباشرة", f"{total_direct_cost:,.2f} ريال")
            st.metric("المصاريف العامة", f"{total_direct_cost * indirect_costs['overhead']:,.2f} ريال")
            st.metric("هامش الربح", f"{total_direct_cost * indirect_costs['profit']:,.2f} ريال")

        with col2:
            st.metric("احتياطي المخاطر", f"{total_direct_cost * indirect_costs['risk']:,.2f} ريال")
            total_cost = total_direct_cost * (1 + sum(indirect_costs.values()))
            st.metric("إجمالي التكلفة", f"{total_cost:,.2f} ريال")

    def _render_risk_analysis(self):
        st.title("تحليل المخاطر")
        self.risk_analyzer.render()

    def _render_pricing_strategies(self):
        st.title("استراتيجيات التسعير")
        balanced_pricing.render_balanced_strategy()

    def _render_local_content(self):
        st.title("المحتوى المحلي")
        st.subheader("نسب المكونات المحلية")

        col1, col2 = st.columns(2)
        with col1:
            materials_percentage = st.number_input("نسبة المواد المحلية (%)", 0, 100, 40)
            equipment_percentage = st.number_input("نسبة المعدات المحلية (%)", 0, 100, 30)

        with col2:
            labor_percentage = st.number_input("نسبة العمالة المحلية (%)", 0, 100, 80)
            subcontractors_percentage = st.number_input("نسبة المقاولين المحليين (%)", 0, 100, 50)

        total_local_content = (
            materials_percentage * 0.4 +
            equipment_percentage * 0.2 +
            labor_percentage * 0.3 +
            subcontractors_percentage * 0.1
        )

        st.markdown("### نتيجة تحليل المحتوى المحلي")
        st.metric("نسبة المحتوى المحلي الإجمالية", f"{total_local_content:.1f}%")

        if st.checkbox("عرض التحليل التفصيلي"):
            data = {
                'المكون': ['المواد', 'المعدات', 'العمالة', 'المقاولين'],
                'النسبة المحلية': [materials_percentage, equipment_percentage, 
                                  labor_percentage, subcontractors_percentage]
            }
            df = pd.DataFrame(data)
            st.bar_chart(df.set_index('المكون'))

    def _render_final_boq(self):
        st.title("جدول الكميات النهائي")

        if not st.session_state.current_project['boq_items']:
            st.warning("لا توجد بنود في جدول الكميات")
            return

        # Create fresh DataFrame with numeric values
        df = pd.DataFrame(st.session_state.current_project['boq_items'])

        # Convert quantity and prices to float
        df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
        df['unit_price'] = pd.to_numeric(df['unit_price'], errors='coerce')

        # Calculate total price
        df['total_price'] = df['quantity'] * df['unit_price']

        # Calculate grand total
        total = df['total_price'].sum()

        # Format numbers for display
        df['quantity'] = df['quantity'].apply(lambda x: '{:.2f}'.format(x))
        df['unit_price'] = df['unit_price'].apply(lambda x: '{:.2f}'.format(x))
        df['total_price'] = df['total_price'].apply(lambda x: '{:.2f}'.format(x))

        # Rename columns to Arabic
        # Get local content percentage if available
        local_content = 0
        if hasattr(st.session_state, 'local_content'):
            materials_percentage = st.session_state.local_content.get('materials_local', 0.4) * 100
            equipment_percentage = st.session_state.local_content.get('equipment_local', 0.3) * 100
            labor_percentage = st.session_state.local_content.get('labor_local', 0.8) * 100
            subcontractors_percentage = st.session_state.local_content.get('subcontractors_local', 0.5) * 100

            local_content = (
                materials_percentage * 0.4 +
                equipment_percentage * 0.2 +
                labor_percentage * 0.3 +
                subcontractors_percentage * 0.1
            )

        # Add local content column
        df['نسبة المحتوى المحلي'] = local_content

        df = df.rename(columns={
            'code': 'الكود',
            'description': 'الوصف',
            'unit': 'الوحدة',
            'quantity': 'الكمية',
            'unit_price': 'سعر الوحدة',
            'total_price': 'السعر الإجمالي'
        })

        # Add total row to display dataframe
        total_row = pd.DataFrame([{
            'الكود': 'الإجمالي',
            'الوصف': '',
            'الوحدة': '',
            'الكمية': '',
            'سعر الوحدة': '',
            'السعر الإجمالي': f"{total:,.2f}"
        }])

        # Combine original dataframe with total row
        df_with_total = pd.concat([df, total_row], ignore_index=True)

        st.dataframe(
            df_with_total,
            use_container_width=True,
            hide_index=True,
            column_config={
                "الكود": st.column_config.TextColumn("الكود", width="small", help="كود البند"),
                "الوصف": st.column_config.TextColumn("الوصف", width="medium", help="وصف البند"),
                "الوحدة": st.column_config.TextColumn("الوحدة", width="small", help="وحدة القياس"),
                "الكمية": st.column_config.NumberColumn("الكمية", width="small", help="كمية البند", format="%.2f"),
                "سعر الوحدة": st.column_config.NumberColumn("سعر الوحدة", width="small", help="سعر الوحدة", format="%.2f"),
                "السعر الإجمالي": st.column_config.NumberColumn("السعر الإجمالي", width="small", help="السعر الإجمالي", format="%.2f"),
                "نسبة المحتوى المحلي": st.column_config.NumberColumn("نسبة المحتوى المحلي", width="small", help="نسبة المحتوى المحلي", format="%.1f%%")
            }
        )
        st.metric("إجمالي جدول الكميات", f"{total:,.2f} ريال")

        # Show saved pricing history with export option
        if st.button("عرض التسعيرات المحفوظة", key="show_saved_pricing"):
            if 'saved_pricing' in st.session_state and st.session_state.saved_pricing:
                st.subheader("التسعيرات المحفوظة")

                # Create selection for saved pricing
                pricing_options = [f"{p['project_name']} - {p['timestamp']}" for p in st.session_state.saved_pricing]
                selected_pricing = st.selectbox("اختر التسعير", pricing_options, key="pricing_select")

                if selected_pricing:
                    selected_idx = pricing_options.index(selected_pricing)
                    pricing = st.session_state.saved_pricing[selected_idx]

                    st.write(f"إجمالي السعر: {pricing['total_price']:,.2f} ريال")
                    st.write(f"نسبة المحتوى المحلي: {pricing['local_content']:.1f}%")
                    df = pd.DataFrame(pricing['items'])
                    st.dataframe(df)

                    # Export selected pricing to Excel
                    if st.button("تصدير التسعير المحدد إلى Excel", key="export_selected_pricing"):
                        try:
                            export_path = "data/exports"
                            os.makedirs(export_path, exist_ok=True)
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            excel_file = f"{export_path}/saved_pricing_{timestamp}.xlsx"

                            # Create Excel writer
                            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                                df.to_excel(writer, index=False, sheet_name='التسعير المحفوظ')
                                worksheet = writer.sheets['التسعير المحفوظ']

                                # Add summary information
                                worksheet['A1'] = f"اسم المشروع: {pricing['project_name']}"
                                worksheet['A2'] = f"التاريخ: {pricing['timestamp']}"
                                worksheet['A3'] = f"إجمالي السعر: {pricing['total_price']:,.2f} ريال"
                                worksheet['A4'] = f"نسبة المحتوى المحلي: {pricing['local_content']:.1f}%"

                            # Provide download button
                            with open(excel_file, 'rb') as f:
                                excel_data = f.read()
                                st.download_button(
                                    label="تحميل ملف Excel",
                                    data=excel_data,
                                    file_name=f"saved_pricing_{timestamp}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            st.success("تم تصدير التسعير المحدد بنجاح!")
                        except Exception as e:
                            st.error(f"حدث خطأ أثناء التصدير: {str(e)}")
            else:
                st.info("لا توجد تسعيرات محفوظة")

        col1, col2, col3, col4 = st.columns(4)

        # Add save button
        with col1:
            if st.button("💾 حفظ التسعير", key="save_pricing_btn"):
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    pricing_data = {
                        'timestamp': timestamp,
                        'project_name': st.session_state.current_project.get('name', 'مشروع جديد'),
                        'total_price': total,
                        'items': df.to_dict('records'),
                        'local_content': local_content
                    }

                    # Save to session state database
                    if 'saved_pricing' not in st.session_state:
                        st.session_state.saved_pricing = []

                    # Check for duplicates before saving
                    is_duplicate = False
                    for saved_pricing in st.session_state.saved_pricing:
                        if (saved_pricing['project_name'] == pricing_data['project_name'] and 
                            saved_pricing['total_price'] == pricing_data['total_price'] and
                            saved_pricing['timestamp'] == pricing_data['timestamp']):
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        st.session_state.saved_pricing.append(pricing_data)
                        st.success("تم حفظ التسعير بنجاح!")
                    else:
                        st.warning("هذا التسعير موجود بالفعل!")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء الحفظ: {str(e)}")

        # Export button
        with col2:
            st.empty()  # Placeholder for future functionality

        with col3:
            if st.button("تصدير إلى Excel"):
                try:
                    export_path = "data/exports"
                    os.makedirs(export_path, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    excel_file = f"{export_path}/boq_{timestamp}.xlsx"

                    # Add a total row
                    total_row = pd.DataFrame([{
                        'الكود': 'الإجمالي',
                        'الوصف': '',
                        'الوحدة': '',
                        'الكمية': '',
                        'سعر الوحدة': '',
                        'السعر الإجمالي': f"{total:,.2f}"
                    }])

                    # Combine original dataframe with total row
                    df_with_total = pd.concat([df, total_row], ignore_index=True)

                    # Write to Excel with styling
                    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                        df_with_total.to_excel(writer, index=False, sheet_name='جدول الكميات')
                        worksheet = writer.sheets['جدول الكميات']
                        # Style the total row
                        for col in range(1, worksheet.max_column + 1):
                            cell = worksheet.cell(row=len(df_with_total), column=col)
                            cell.font = openpyxl.styles.Font(bold=True)

                    with open(excel_file, 'rb') as f:
                        excel_data = f.read()
                    st.download_button(
                        label="تحميل ملف Excel",
                        data=excel_data,
                        file_name=f"boq_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                    st.success("تم تصدير الملف بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء التصدير: {str(e)}")

        with col2:
            if st.button("تصدير إلى PDF"):
                try:
                    export_path = "data/exports"
                    os.makedirs(export_path, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    pdf_file = f"{export_path}/boq_{timestamp}.pdf"

                    # Create HTML with Arabic support and styling
                    html = f"""
                    <html dir="rtl">
                    <head><meta charset="UTF-8">
                        <style>
                            body {{ font-family: Arial, sans-serif; }}
                            table {{ border-collapse: collapse; width: 100%; direction: rtl; }}
                            th, td {{ border: 1px solid black; padding: 8px; text-align: center; }}
                            th {{ background-color: #f2f2f2; }}
                        </style>
                    </head>
                    <body>
                        <h2>جدول الكميات</h2>
                        {df.to_html(index=False)}
                        <p>إجمالي جدول الكميات: {total:,.2f} ريال</p>
                    </body>
                    </html>
                    """

                    # Configure PDF options
                    options = {
                        'page-size': 'A4',
                        'margin-top': '1.0in',
                        'margin-right': '0.75in',
                        'margin-bottom': '1.0in',
                        'margin-left': '0.75in',
                        'encoding': 'UTF-8',
                        'enable-local-file-access': None
                    }

                    # Generate PDF
                    pdfkit.from_string(html, pdf_file, options=options)

                    # Provide download button
                    with open(pdf_file, 'rb') as f:
                        pdf_data = f.read()
                    st.download_button(
                        label="تحميل ملف PDF",
                        data=pdf_data,
                        file_name=f"boq_{timestamp}.pdf",
                        mime="application/pdf"
                    )
                    st.success("تم تصدير الملف بنجاح!")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء التصدير: {str(e)}")


    def _render_navigation(self):
        can_proceed = self._validate_current_stage()
        st.markdown("---")
        st.markdown("""
            <style>
            .nav-button {
                width: 120px;
                height: 40px;
                margin: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        nav_col1, nav_col2, nav_col3 = st.columns([2, 4, 2])

        with nav_col1:
            if st.session_state.pricing_stage > 1:
                st.button("⮕ السابق", key="prev_button", help="العودة للمرحلة السابقة", on_click=lambda: setattr(st.session_state, 'pricing_stage', st.session_state.pricing_stage - 1))

        with nav_col2:
            st.markdown(f"<h4 style='text-align: center;'>المرحلة {st.session_state.pricing_stage} من 8</h4>", unsafe_allow_html=True)

        with nav_col3:
            if st.session_state.pricing_stage < 8:
                st.button("التالي ⬅️", key="next_button", help="الانتقال للمرحلة التالية", disabled=not can_proceed, on_click=lambda: setattr(st.session_state, 'pricing_stage', st.session_state.pricing_stage + 1))

        progress = (st.session_state.pricing_stage - 1) / 7
        st.progress(progress, text=f"اكتمال {int(progress * 100)}% من مراحل التسعير")

        progress = (st.session_state.pricing_stage - 1) / 7
        st.progress(progress, text=f"اكتمال {int(progress * 100)}% من مراحل التسعير")

    def _validate_current_stage(self):
        if st.session_state.pricing_stage == 1:
            return True
        elif st.session_state.pricing_stage == 2:
            return len(st.session_state.current_project.get('boq_items', [])) > 0
        elif st.session_state.pricing_stage == 3:
            return True
        elif st.session_state.pricing_stage == 4:
            return True
        return True

    def _render_reference_guides(self):
        self.reference_guides.render()