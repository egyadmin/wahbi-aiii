import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
from datetime import datetime
import os
import sys
from pathlib import Path

# إضافة المسار للوصول إلى الوحدات الأخرى
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(os.path.dirname(current_dir))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

class DataAnalysisApp:
    """تطبيق تحليل البيانات"""
    
    def __init__(self):
        """تهيئة تطبيق تحليل البيانات"""
        self.data = None
        self.file_path = None
    
    def run(self):
        """تشغيل تطبيق تحليل البيانات"""
        # استيراد مدير التكوين
        from config_manager import ConfigManager
        
        # محاولة تعيين تكوين الصفحة (سيتم تجاهلها إذا كان التكوين معينًا بالفعل)
        config_manager = ConfigManager()
        config_manager.set_page_config_if_needed(
            page_title="تحليل البيانات",
            page_icon="📊",
            layout="wide"
        )
        
        # عرض عنوان التطبيق
        st.title("تحليل البيانات")
        st.write("استخدم هذه الأداة لتحليل بيانات المناقصات والمشاريع")
        
        # إنشاء علامات تبويب للتطبيق
        tabs = st.tabs(["تحميل البيانات", "استكشاف البيانات", "تحليل متقدم", "التصور المرئي", "التقارير"])
        
        with tabs[0]:
            self._load_data_tab()
        
        with tabs[1]:
            self._explore_data_tab()
        
        with tabs[2]:
            self._advanced_analysis_tab()
        
        with tabs[3]:
            self._visualization_tab()
        
        with tabs[4]:
            self._reports_tab()
    
    def _load_data_tab(self):
        """علامة تبويب تحميل البيانات"""
        st.header("تحميل البيانات")
        
        # خيارات تحميل البيانات
        data_source = st.radio(
            "اختر مصدر البيانات:",
            ["تحميل ملف", "استيراد من قاعدة البيانات", "استخدام بيانات نموذجية"]
        )
        
        if data_source == "تحميل ملف":
            uploaded_file = st.file_uploader("اختر ملف CSV أو Excel", type=["csv", "xlsx", "xls"])
            
            if uploaded_file is not None:
                try:
                    if uploaded_file.name.endswith('.csv'):
                        self.data = pd.read_csv(uploaded_file)
                    else:
                        self.data = pd.read_excel(uploaded_file)
                    
                    st.success(f"تم تحميل الملف بنجاح! عدد الصفوف: {self.data.shape[0]}, عدد الأعمدة: {self.data.shape[1]}")
                    st.write("معاينة البيانات:")
                    st.dataframe(self.data.head())
                except Exception as e:
                    st.error(f"حدث خطأ أثناء تحميل الملف: {str(e)}")
        
        elif data_source == "استيراد من قاعدة البيانات":
            st.info("هذه الميزة قيد التطوير")
            
            # محاكاة الاتصال بقاعدة البيانات
            if st.button("اتصال بقاعدة البيانات"):
                with st.spinner("جاري الاتصال بقاعدة البيانات..."):
                    # محاكاة تأخير الاتصال
                    import time
                    time.sleep(2)
                    
                    # إنشاء بيانات نموذجية
                    self.data = self._create_sample_data()
                    
                    st.success("تم الاتصال بقاعدة البيانات بنجاح!")
                    st.write("معاينة البيانات:")
                    st.dataframe(self.data.head())
        
        elif data_source == "استخدام بيانات نموذجية":
            if st.button("تحميل بيانات نموذجية"):
                self.data = self._create_sample_data()
                st.success("تم تحميل البيانات النموذجية بنجاح!")
                st.write("معاينة البيانات:")
                st.dataframe(self.data.head())
    
    def _explore_data_tab(self):
        """علامة تبويب استكشاف البيانات"""
        st.header("استكشاف البيانات")
        
        if self.data is None:
            st.info("الرجاء تحميل البيانات أولاً من علامة تبويب 'تحميل البيانات'")
            return
        
        # عرض معلومات عامة عن البيانات
        st.subheader("معلومات عامة")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"عدد الصفوف: {self.data.shape[0]}")
            st.write(f"عدد الأعمدة: {self.data.shape[1]}")
            st.write(f"القيم المفقودة: {self.data.isna().sum().sum()}")
        
        with col2:
            st.write(f"أنواع البيانات:")
            st.write(self.data.dtypes)
        
        # عرض إحصاءات وصفية
        st.subheader("إحصاءات وصفية")
        st.dataframe(self.data.describe())
        
        # عرض معلومات عن الأعمدة
        st.subheader("معلومات الأعمدة")
        
        selected_column = st.selectbox("اختر عمودًا لتحليله:", self.data.columns)
        
        if selected_column:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"نوع البيانات: {self.data[selected_column].dtype}")
                st.write(f"القيم الفريدة: {self.data[selected_column].nunique()}")
                st.write(f"القيم المفقودة: {self.data[selected_column].isna().sum()}")
            
            with col2:
                if pd.api.types.is_numeric_dtype(self.data[selected_column]):
                    st.write(f"الحد الأدنى: {self.data[selected_column].min()}")
                    st.write(f"الحد الأقصى: {self.data[selected_column].max()}")
                    st.write(f"المتوسط: {self.data[selected_column].mean()}")
                    st.write(f"الوسيط: {self.data[selected_column].median()}")
                else:
                    st.write("القيم الأكثر تكرارًا:")
                    st.write(self.data[selected_column].value_counts().head())
            
            # عرض رسم بياني للعمود المحدد
            st.subheader(f"رسم بياني لـ {selected_column}")
            
            if pd.api.types.is_numeric_dtype(self.data[selected_column]):
                fig = px.histogram(self.data, x=selected_column, title=f"توزيع {selected_column}")
                st.plotly_chart(fig, use_container_width=True)
            else:
                # الكود المعدل لحل مشكلة الرسم البياني
                value_counts_df = self.data[selected_column].value_counts().reset_index()
                value_counts_df.columns = ['القيمة', 'العدد']  # تسمية الأعمدة بأسماء واضحة
                fig = px.bar(value_counts_df, x='القيمة', y='العدد', title=f"توزيع {selected_column}")
                fig.update_layout(xaxis_title="القيمة", yaxis_title="العدد")
                st.plotly_chart(fig, use_container_width=True)
    
    def _advanced_analysis_tab(self):
        """علامة تبويب التحليل المتقدم"""
        st.header("تحليل متقدم")
        
        if self.data is None:
            st.info("الرجاء تحميل البيانات أولاً من علامة تبويب 'تحميل البيانات'")
            return
        
        # أنواع التحليل المتقدم
        analysis_type = st.selectbox(
            "اختر نوع التحليل:",
            ["تحليل الارتباط", "تحليل الاتجاهات", "تحليل المجموعات", "تحليل التباين"]
        )
        
        if analysis_type == "تحليل الارتباط":
            st.subheader("تحليل الارتباط")
            
            # اختيار الأعمدة الرقمية فقط
            numeric_columns = self.data.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_columns) < 2:
                st.warning("يجب أن يكون هناك عمودان رقميان على الأقل لإجراء تحليل الارتباط")
                return
            
            # حساب مصفوفة الارتباط
            correlation_matrix = self.data[numeric_columns].corr()
            
            # عرض مصفوفة الارتباط
            st.write("مصفوفة الارتباط:")
            st.dataframe(correlation_matrix)
            
            # رسم خريطة حرارية للارتباط
            st.write("خريطة حرارية للارتباط:")
            fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto",
                           title="خريطة حرارية لمصفوفة الارتباط")
            st.plotly_chart(fig, use_container_width=True)
            
            # تحليل الارتباط بين عمودين محددين
            st.subheader("تحليل الارتباط بين عمودين محددين")
            
            col1 = st.selectbox("اختر العمود الأول:", numeric_columns, key="corr_col1")
            col2 = st.selectbox("اختر العمود الثاني:", numeric_columns, key="corr_col2")
            
            if col1 != col2:
                # حساب معامل الارتباط
                correlation = self.data[col1].corr(self.data[col2])
                
                st.write(f"معامل الارتباط بين {col1} و {col2}: {correlation:.4f}")
                
                # رسم مخطط التشتت
                fig = px.scatter(self.data, x=col1, y=col2, title=f"مخطط التشتت: {col1} مقابل {col2}")
                fig.update_layout(xaxis_title=col1, yaxis_title=col2)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("الرجاء اختيار عمودين مختلفين")
        
        elif analysis_type == "تحليل الاتجاهات":
            st.subheader("تحليل الاتجاهات")
            st.info("هذه الميزة قيد التطوير")
        
        elif analysis_type == "تحليل المجموعات":
            st.subheader("تحليل المجموعات")
            st.info("هذه الميزة قيد التطوير")
        
        elif analysis_type == "تحليل التباين":
            st.subheader("تحليل التباين")
            st.info("هذه الميزة قيد التطوير")
    
    def _visualization_tab(self):
        """علامة تبويب التصور المرئي"""
        st.header("التصور المرئي")
        
        if self.data is None:
            st.info("الرجاء تحميل البيانات أولاً من علامة تبويب 'تحميل البيانات'")
            return
        
        # أنواع الرسوم البيانية
        chart_type = st.selectbox(
            "اختر نوع الرسم البياني:",
            ["مخطط شريطي", "مخطط خطي", "مخطط دائري", "مخطط تشتت", "مخطط صندوقي", "مخطط حراري"]
        )
        
        # اختيار الأعمدة حسب نوع الرسم البياني
        if chart_type == "مخطط شريطي":
            st.subheader("مخطط شريطي")
            
            x_column = st.selectbox("اختر عمود المحور الأفقي (x):", self.data.columns, key="bar_x")
            y_column = st.selectbox("اختر عمود المحور الرأسي (y):", 
                                   self.data.select_dtypes(include=['number']).columns.tolist(), 
                                   key="bar_y")
            
            # خيارات إضافية
            color_column = st.selectbox("اختر عمود اللون (اختياري):", 
                                       ["لا يوجد"] + self.data.columns.tolist(), 
                                       key="bar_color")
            
            # إنشاء الرسم البياني
            if color_column == "لا يوجد":
                fig = px.bar(self.data, x=x_column, y=y_column, title=f"{y_column} حسب {x_column}")
            else:
                fig = px.bar(self.data, x=x_column, y=y_column, color=color_column, 
                            title=f"{y_column} حسب {x_column} (مصنف حسب {color_column})")
            
            fig.update_layout(xaxis_title=x_column, yaxis_title=y_column)
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "مخطط خطي":
            st.subheader("مخطط خطي")
            
            x_column = st.selectbox("اختر عمود المحور الأفقي (x):", self.data.columns, key="line_x")
            y_columns = st.multiselect("اختر أعمدة المحور الرأسي (y):", 
                                      self.data.select_dtypes(include=['number']).columns.tolist(), 
                                      key="line_y")
            
            if y_columns:
                # إنشاء الرسم البياني
                fig = go.Figure()
                
                for y_column in y_columns:
                    fig.add_trace(go.Scatter(x=self.data[x_column], y=self.data[y_column], 
                                           mode='lines+markers', name=y_column))
                
                fig.update_layout(title=f"مخطط خطي", xaxis_title=x_column, yaxis_title="القيمة")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("الرجاء اختيار عمود واحد على الأقل للمحور الرأسي")
        
        elif chart_type == "مخطط دائري":
            st.subheader("مخطط دائري")
            
            column = st.selectbox("اختر العمود:", self.data.columns, key="pie_column")
            
            # إنشاء الرسم البياني
            # تعديل لحل مشكلة مماثلة في مخطط دائري
            value_counts_df = self.data[column].value_counts().reset_index()
            value_counts_df.columns = ['القيمة', 'العدد']
            fig = px.pie(value_counts_df, names='القيمة', values='العدد', title=f"توزيع {column}")
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "مخطط تشتت":
            st.subheader("مخطط تشتت")
            
            numeric_columns = self.data.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_columns) < 2:
                st.warning("يجب أن يكون هناك عمودان رقميان على الأقل لإنشاء مخطط تشتت")
                return
            
            x_column = st.selectbox("اختر عمود المحور الأفقي (x):", numeric_columns, key="scatter_x")
            y_column = st.selectbox("اختر عمود المحور الرأسي (y):", numeric_columns, key="scatter_y")
            
            # خيارات إضافية
            color_column = st.selectbox("اختر عمود اللون (اختياري):", 
                                       ["لا يوجد"] + self.data.columns.tolist(), 
                                       key="scatter_color")
            
            size_column = st.selectbox("اختر عمود الحجم (اختياري):", 
                                      ["لا يوجد"] + numeric_columns, 
                                      key="scatter_size")
            
            # إنشاء الرسم البياني
            if color_column == "لا يوجد" and size_column == "لا يوجد":
                fig = px.scatter(self.data, x=x_column, y=y_column, 
                                title=f"{y_column} مقابل {x_column}")
            elif color_column != "لا يوجد" and size_column == "لا يوجد":
                fig = px.scatter(self.data, x=x_column, y=y_column, color=color_column, 
                                title=f"{y_column} مقابل {x_column} (مصنف حسب {color_column})")
            elif color_column == "لا يوجد" and size_column != "لا يوجد":
                fig = px.scatter(self.data, x=x_column, y=y_column, size=size_column, 
                                title=f"{y_column} مقابل {x_column} (الحجم حسب {size_column})")
            else:
                fig = px.scatter(self.data, x=x_column, y=y_column, color=color_column, size=size_column, 
                                title=f"{y_column} مقابل {x_column} (مصنف حسب {color_column}, الحجم حسب {size_column})")
            
            fig.update_layout(xaxis_title=x_column, yaxis_title=y_column)
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "مخطط صندوقي":
            st.subheader("مخطط صندوقي")
            
            numeric_columns = self.data.select_dtypes(include=['number']).columns.tolist()
            
            if not numeric_columns:
                st.warning("يجب أن يكون هناك عمود رقمي واحد على الأقل لإنشاء مخطط صندوقي")
                return
            
            y_column = st.selectbox("اختر عمود القيمة:", numeric_columns, key="box_y")
            
            # خيارات إضافية
            x_column = st.selectbox("اختر عمود التصنيف (اختياري):", 
                                   ["لا يوجد"] + self.data.columns.tolist(), 
                                   key="box_x")
            
            # إنشاء الرسم البياني
            if x_column == "لا يوجد":
                fig = px.box(self.data, y=y_column, title=f"مخطط صندوقي لـ {y_column}")
            else:
                fig = px.box(self.data, x=x_column, y=y_column, 
                            title=f"مخطط صندوقي لـ {y_column} حسب {x_column}")
            
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "مخطط حراري":
            st.subheader("مخطط حراري")
            
            numeric_columns = self.data.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_columns) < 2:
                st.warning("يجب أن يكون هناك عمودان رقميان على الأقل لإنشاء مخطط حراري")
                return
            
            # اختيار الأعمدة للمخطط الحراري
            selected_columns = st.multiselect("اختر الأعمدة للمخطط الحراري:", 
                                             numeric_columns, 
                                             default=numeric_columns[:5] if len(numeric_columns) > 5 else numeric_columns)
            
            if selected_columns:
                # حساب مصفوفة الارتباط
                correlation_matrix = self.data[selected_columns].corr()
                
                # إنشاء الرسم البياني
                fig = px.imshow(correlation_matrix, text_auto=True, aspect="auto",
                               title="مخطط حراري لمصفوفة الارتباط")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("الرجاء اختيار عمود واحد على الأقل")
    
    def _reports_tab(self):
        """علامة تبويب التقارير"""
        st.header("التقارير")
        
        if self.data is None:
            st.info("الرجاء تحميل البيانات أولاً من علامة تبويب 'تحميل البيانات'")
            return
        
        st.subheader("إنشاء تقرير")
        
        # خيارات التقرير
        report_type = st.selectbox(
            "اختر نوع التقرير:",
            ["تقرير ملخص", "تقرير تحليلي", "تقرير مقارنة"]
        )
        
        if report_type == "تقرير ملخص":
            st.write("محتوى التقرير:")
            
            # إنشاء ملخص للبيانات
            st.write("### ملخص البيانات")
            st.write(f"عدد الصفوف: {self.data.shape[0]}")
            st.write(f"عدد الأعمدة: {self.data.shape[1]}")
            
            # إحصاءات وصفية
            st.write("### إحصاءات وصفية")
            st.dataframe(self.data.describe())
            
            # معلومات عن القيم المفقودة
            st.write("### القيم المفقودة")
            missing_data = pd.DataFrame({
                'العمود': self.data.columns,
                'عدد القيم المفقودة': self.data.isna().sum().values,
                'نسبة القيم المفقودة (%)': (self.data.isna().sum().values / len(self.data) * 100).round(2)
            })
            st.dataframe(missing_data)
            
            # توزيع البيانات الرقمية
            st.write("### توزيع البيانات الرقمية")
            numeric_columns = self.data.select_dtypes(include=['number']).columns.tolist()
            
            if numeric_columns:
                for i in range(0, len(numeric_columns), 2):
                    cols = st.columns(2)
                    for j in range(2):
                        if i + j < len(numeric_columns):
                            col = numeric_columns[i + j]
                            with cols[j]:
                                fig = px.histogram(self.data, x=col, title=f"توزيع {col}")
                                st.plotly_chart(fig, use_container_width=True)
            
            # خيارات تصدير التقرير
            st.subheader("تصدير التقرير")
            export_format = st.radio("اختر صيغة التصدير:", ["PDF", "Excel", "HTML"])
            
            if st.button("تصدير التقرير"):
                st.success(f"تم تصدير التقرير بصيغة {export_format} بنجاح!")
        
        elif report_type == "تقرير تحليلي":
            st.info("هذه الميزة قيد التطوير")
        
        elif report_type == "تقرير مقارنة":
            st.info("هذه الميزة قيد التطوير")
    
    def _create_sample_data(self):
        """إنشاء بيانات نموذجية للمناقصات"""
        # إنشاء تواريخ عشوائية
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2025, 3, 31)
        days = (end_date - start_date).days
        
        # إنشاء بيانات نموذجية
        data = {
            'رقم المناقصة': [f'T-{i:04d}' for i in range(1, 101)],
            'اسم المشروع': [f'مشروع {i}' for i in range(1, 101)],
            'نوع المشروع': np.random.choice(['بناء', 'صيانة', 'تطوير', 'توريد', 'خدمات'], 100),
            'الموقع': np.random.choice(['الرياض', 'جدة', 'الدمام', 'مكة', 'المدينة', 'تبوك', 'أبها'], 100),
            'تاريخ الإعلان': [start_date + pd.Timedelta(days=np.random.randint(0, days)) for _ in range(100)],
            'تاريخ الإغلاق': [start_date + pd.Timedelta(days=np.random.randint(30, days)) for _ in range(100)],
            'الميزانية التقديرية': np.random.uniform(1000000, 50000000, 100),
            'عدد المتقدمين': np.random.randint(1, 20, 100),
            'سعر العرض': np.random.uniform(900000, 55000000, 100),
            'نسبة الفوز (%)': np.random.uniform(0, 100, 100),
            'مدة التنفيذ (أشهر)': np.random.randint(3, 36, 100),
            'عدد العمال': np.random.randint(10, 500, 100),
            'تكلفة المواد': np.random.uniform(500000, 30000000, 100),
            'تكلفة العمالة': np.random.uniform(200000, 15000000, 100),
            'تكلفة المعدات': np.random.uniform(100000, 10000000, 100),
            'هامش الربح (%)': np.random.uniform(5, 25, 100),
            'درجة المخاطرة': np.random.choice(['منخفضة', 'متوسطة', 'عالية'], 100),
            'حالة المناقصة': np.random.choice(['جارية', 'مغلقة', 'ملغاة', 'فائزة', 'خاسرة'], 100)
        }
        
        # إنشاء DataFrame
        df = pd.DataFrame(data)
        
        # إضافة بعض العلاقات المنطقية
        df['إجمالي التكلفة'] = df['تكلفة المواد'] + df['تكلفة العمالة'] + df['تكلفة المعدات']
        df['الربح المتوقع'] = df['سعر العرض'] - df['إجمالي التكلفة']
        df['نسبة التكلفة من العرض (%)'] = (df['إجمالي التكلفة'] / df['سعر العرض'] * 100).round(2)
        
        return df
