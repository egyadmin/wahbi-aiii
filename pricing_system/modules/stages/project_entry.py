
import streamlit as st
from datetime import datetime

def render_project_entry():
    """عرض نموذج إدخال بيانات المشروع"""
    st.header("إدخال تفاصيل المشروع")
    project_data = {}

    # التأكد من وجود حالة المشروع في session_state
    if 'current_project' not in st.session_state:
        st.session_state.current_project = {}

    # نموذج إدخال البيانات
    with st.form("project_entry_form", clear_on_submit=False):
        col1, col2 = st.columns(2)

        with col1:
            project_name = st.text_input(
                "اسم المشروع", 
                value=st.session_state.current_project.get('name', ''),
                key="project_name"
            )
            project_code = st.text_input(
                "رقم المشروع/المناقصة",
                value=st.session_state.current_project.get('code', ''),
                key="project_code"
            )
            location = st.text_input(
                "الموقع",
                value=st.session_state.current_project.get('location', ''),
                key="location"
            )
            
        with col2:
            start_date = st.date_input(
                "تاريخ البدء",
                value=st.session_state.current_project.get('start_date', datetime.now().date())
            )
            duration = st.number_input(
                "مدة المشروع (بالأيام)",
                min_value=1,
                value=st.session_state.current_project.get('duration', 180)
            )
            estimated_budget = st.number_input(
                "الميزانية التقديرية",
                min_value=0.0,
                value=st.session_state.current_project.get('budget', 0.0),
                format="%f"
            )

        project_description = st.text_area(
            "وصف المشروع",
            value=st.session_state.current_project.get('description', ''),
            height=100
        )

        submitted = st.form_submit_button("حفظ البيانات")
        
        if submitted:
            if not project_name or not project_code:
                st.error("يجب إدخال اسم المشروع ورقمه")
            else:
                # تحديث بيانات المشروع في session_state
                st.session_state.current_project.update({
                    'name': project_name,
                    'code': project_code,
                    'location': location,
                    'start_date': start_date,
                    'duration': duration,
                    'budget': estimated_budget,
                    'description': project_description,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                project_data = {
                    'name': project_name,
                    'code': project_code,
                    'location': location,
                    'start_date': start_date,
                    'duration': duration,
                    'budget': estimated_budget,
                    'description': project_description
                }
                st.success("تم حفظ بيانات المشروع بنجاح")
                return project_data

    return False
