
"""
استراتيجية التسعير المتوازن
"""
import streamlit as st
import pandas as pd

def render_balanced_strategy():
    st.markdown("### التسعير المتوازن")
    
    strategies = [
        "التسعير القياسي",
        "التسعير المتزن",
        "التسعير غير المتزن", 
        "التسعير الموجه للربحية",
        "التسعير بالتجميع",
        "التسعير بالمحتوى المحلي"
    ]
    
    selected_strategy = st.selectbox(
        "اختر استراتيجية التسعير",
        strategies
    )
    
    # قراءة البنود من المشروع الحالي
    if 'current_project' not in st.session_state:
        st.warning("يرجى اختيار مشروع أولاً")
        return
        
    project = st.session_state.current_project
    if not project:
        st.info("لم يتم اختيار مشروع بعد. يرجى إدخال بيانات المشروع أولاً.")
        return
        
    boq_items = project.get('boq_items', [])
    
    if not boq_items:
        st.info("لا توجد بنود مضافة للمشروع بعد. يرجى إضافة البنود أولاً.")
        return

    # عرض تحليل البنود
    st.markdown("#### تحليل بنود المشروع")
    
    for i, item in enumerate(boq_items):
        with st.expander(f"البند {i+1}: {item['description']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("معلومات البند:")
                st.write(f"- الكود: {item['code']}")
                st.write(f"- الوحدة: {item['unit']}")
                st.write(f"- الكمية: {item['quantity']}")
                st.write(f"- سعر الوحدة: {item['unit_price']} ريال")
                
            with col2:
                st.write("تحليل التكاليف:")
                
                # تعديل سعر الوحدة
                new_unit_price = st.number_input(
                    "سعر الوحدة الجديد",
                    min_value=0.0,
                    value=float(item['unit_price']),
                    key=f"unit_price_{selected_strategy}_{i}"
                )
                
                # تعديل الكمية
                new_quantity = st.number_input(
                    "الكمية الجديدة",
                    min_value=0.0,
                    value=float(item['quantity']),
                    key=f"quantity_{selected_strategy}_{i}"
                )
                
                # زر تحديث البند
                if st.button("تحديث البند", key=f"update_{selected_strategy}_{i}"):
                    item['unit_price'] = new_unit_price
                    item['quantity'] = new_quantity
                    item['total_price'] = new_unit_price * new_quantity
                    st.success("تم تحديث البند بنجاح")
                    st.rerun()
                
                # زر حذف البند
                if st.button("حذف البند", key=f"delete_{selected_strategy}_{i}"):
                    st.session_state.current_project['boq_items'].pop(i)
                    st.success("تم حذف البند بنجاح")
                    st.rerun()

def calculate_balanced_price(base_cost, overhead_ratio=0.15, profit_ratio=0.10):
    """حساب السعر المتوازن"""
    overhead = base_cost * overhead_ratio
    profit = base_cost * profit_ratio
    return base_cost + overhead + profit
