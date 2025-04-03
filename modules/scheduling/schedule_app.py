
import streamlit as st
import pandas as pd
import plotly.figure_factory as ff
from datetime import datetime, timedelta
import plotly.express as px
import numpy as np
import io
import openpyxl

class ScheduleApp:
    def __init__(self):
        if 'saved_pricing' not in st.session_state:
            st.session_state.saved_pricing = []
        if 'uploaded_files' not in st.session_state:
            st.session_state.uploaded_files = {}

    def run(self):
        st.title("الجدول الزمني للمشروع")

        # إضافة تبويب للملفات
        tabs = st.tabs(["جدول الكميات", "ملفات المشروع"])

        with tabs[0]:
            self._handle_boq_tab()

        with tabs[1]:
            self._handle_project_files()

    def _handle_project_files(self):
        st.subheader("إدارة ملفات المشروع")
        
        # رفع الملفات
        uploaded_file = st.file_uploader(
            "قم برفع ملفات المشروع",
            type=['xls', 'xlsx', 'xml', 'xer', 'pmxml', 'mpp', 'vsdx'],
            help="يمكنك رفع ملفات من برامج مثل Primavera P6, Microsoft Project, Power BI, Visio"
        )

        if uploaded_file:
            try:
                # قراءة وتحليل الملف
                if uploaded_file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(uploaded_file)
                    st.session_state.uploaded_files[uploaded_file.name] = {
                        'data': df,
                        'type': 'excel',
                        'upload_time': datetime.now()
                    }
                    
                    # عرض معلومات الملف
                    st.success(f"تم استيراد الملف: {uploaded_file.name}")
                    st.write("معلومات الملف:")
                    st.write(f"- عدد الأنشطة: {len(df)}")
                    st.write(f"- الأعمدة: {', '.join(df.columns)}")
                    
                    # عرض البيانات في جدول
                    st.dataframe(df, use_container_width=True)
                    
                    # إنشاء مخطط جانت تفاعلي
                    if 'Start' in df.columns and 'Finish' in df.columns:
                        self._create_interactive_gantt(df)
                    
                else:
                    st.info(f"تم استلام الملف {uploaded_file.name}. سيتم إضافة دعم لهذا النوع من الملفات قريباً.")

            except Exception as e:
                st.error(f"حدث خطأ أثناء معالجة الملف: {str(e)}")

        # عرض الملفات المحفوظة
        if st.session_state.uploaded_files:
            st.subheader("الملفات المحفوظة")
            for filename, file_info in st.session_state.uploaded_files.items():
                with st.expander(filename):
                    st.write(f"نوع الملف: {file_info['type']}")
                    st.write(f"تاريخ الرفع: {file_info['upload_time']}")
                    if file_info['type'] == 'excel':
                        st.dataframe(file_info['data'], use_container_width=True)

    def _create_interactive_gantt(self, df):
        st.subheader("مخطط جانت التفاعلي")
        
        # تحضير البيانات للمخطط
        df['Start'] = pd.to_datetime(df['Start'])
        df['Finish'] = pd.to_datetime(df['Finish'])
        
        fig = ff.create_gantt(
            df,
            colors={
                'Task': '#2196F3',
                'Complete': '#4CAF50'
            },
            index_col='Resource',
            show_colorbar=True,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True
        )
        
        fig.update_layout(
            title="مخطط جانت للمشروع",
            xaxis_title="التاريخ",
            yaxis_title="الأنشطة",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _handle_boq_tab(self):
        # نفس الكود السابق لمعالجة جدول الكميات
        source_type = st.radio("اختر مصدر جدول الكميات:", 
                             ["جدول كميات محفوظ", "رفع جدول كميات جديد"],
                             key="boq_source")

        if source_type == "جدول كميات محفوظ":
            self._handle_saved_boq()
        else:
            self._handle_new_boq()

    def _handle_saved_boq(self):
        if not st.session_state.saved_pricing:
            st.warning("لا توجد جداول كميات محفوظة.")
            return

        projects = [(p['project_name'], i) for i, p in enumerate(st.session_state.saved_pricing)]
        selected_project_name = st.selectbox("اختر المشروع", [p[0] for p in projects])
        project_index = next(p[1] for p in projects if p[0] == selected_project_name)
        project = st.session_state.saved_pricing[project_index]
        
        self._display_project_schedule(project)

    def _handle_new_boq(self):
        uploaded_file = st.file_uploader("قم برفع ملف Excel لجدول الكميات", type=['xlsx', 'xls'])
        if uploaded_file:
            try:
                df = pd.read_excel(uploaded_file)
                project = self._create_project_from_boq(df)
                self._display_project_schedule(project)
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {str(e)}")

    def _create_project_from_boq(self, df):
        return {
            'project_name': 'مشروع جديد',
            'items': [row.to_dict() for _, row in df.iterrows()],
            'total_price': df.get('الإجمالي', df.get('total_price', 0)).sum(),
            'project_duration': 180
        }

    def _display_project_schedule(self, project):
        if not project:
            return

        st.subheader("تفاصيل المشروع")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"اسم المشروع: {project['project_name']}")
            st.write(f"إجمالي القيمة: {project['total_price']:,.2f} ريال")
        with col2:
            project['project_duration'] = st.number_input(
                "مدة المشروع (بالأيام)", 
                min_value=30, 
                max_value=1800, 
                value=project.get('project_duration', 180)
            )

        self._generate_and_display_schedule(project)

    def _generate_and_display_schedule(self, project):
        if 'schedule_items' not in project:
            self._initialize_schedule_items(project)

        st.subheader("تحرير الجدول الزمني")
        edited_df = self._edit_schedule(project['schedule_items'])
        project['schedule_items'] = edited_df.to_dict('records')

        self._display_gantt_chart(project['schedule_items'])
        self._display_progress_report(project['schedule_items'])

    def _initialize_schedule_items(self, project):
        project['schedule_items'] = []
        for item in project['items']:
            relative_duration = int((item['total_price'] / project['total_price']) * project['project_duration'])
            schedule_item = {
                'Task': item.get('description', ''),
                'Start': datetime.now().strftime('%Y-%m-%d'),
                'Finish': (datetime.now() + timedelta(days=relative_duration)).strftime('%Y-%m-%d'),
                'Duration': relative_duration,
                'Dependencies': '',
                'Progress': 0,
                'Resource': ''
            }
            project['schedule_items'].append(schedule_item)

    def _edit_schedule(self, schedule_items):
        return st.data_editor(
            pd.DataFrame(schedule_items),
            column_config={
                "Task": "البند",
                "Start": st.column_config.DateColumn("تاريخ البداية"),
                "Finish": st.column_config.DateColumn("تاريخ النهاية"),
                "Duration": "المدة (أيام)",
                "Dependencies": "الاعتماديات",
                "Progress": st.column_config.NumberColumn("نسبة الإنجاز %", min_value=0, max_value=100),
                "Resource": "الموارد"
            },
            use_container_width=True,
            hide_index=True
        )

    def _display_gantt_chart(self, schedule_items):
        st.subheader("مخطط جانت")
        df = pd.DataFrame(schedule_items)
        fig = ff.create_gantt(
            df,
            colors={
                'Complete': 'rgb(0, 255, 100)',
                'Incomplete': 'rgb(160, 160, 160)'
            },
            index_col='Resource',
            show_colorbar=True,
            group_tasks=True,
            showgrid_x=True,
            showgrid_y=True
        )
        
        fig.update_layout(
            title="مخطط جانت للمشروع",
            xaxis_title="التاريخ",
            yaxis_title="البنود",
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)

    def _display_progress_report(self, schedule_items):
        st.subheader("تقرير تقدم المشروع")
        df = pd.DataFrame(schedule_items)
        avg_progress = df['Progress'].mean()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("متوسط نسبة الإنجاز", f"{avg_progress:.1f}%")
        with col2:
            completed_tasks = len(df[df['Progress'] == 100])
            st.metric("البنود المكتملة", f"{completed_tasks} من {len(df)}")
        with col3:
            not_started = len(df[df['Progress'] == 0])
            st.metric("البنود غير المبدوءة", not_started)
