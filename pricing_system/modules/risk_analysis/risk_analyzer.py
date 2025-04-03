import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

class RiskAnalyzer:
    def __init__(self):
        self.risk_categories = [
            "مخاطر السوق",
            "مخاطر التنفيذ",
            "مخاطر العقود",
            "مخاطر التمويل",
            "مخاطر الموارد"
        ]

        self.impact_levels = {
            "منخفض": 1,
            "متوسط": 2,
            "عالي": 3,
            "حرج": 4
        }

        self.probability_levels = {
            "نادر": 1,
            "محتمل": 2,
            "مرجح": 3,
            "شبه مؤكد": 4
        }

    def render(self):
        """عرض واجهة تحليل المخاطر"""
        st.markdown("### تحليل المخاطر")

        # إضافة مخاطر جديدة
        with st.form("add_risk_form"):
            col1, col2 = st.columns(2)

            with col1:
                category = st.selectbox("فئة المخاطر", self.risk_categories)
                description = st.text_area("وصف المخاطر")
                probability = st.selectbox("احتمالية الحدوث", list(self.probability_levels.keys()))

            with col2:
                impact = st.selectbox("مستوى التأثير", list(self.impact_levels.keys()))
                response = st.text_area("استراتيجية الاستجابة")
                responsible = st.text_input("المسؤول")

            if st.form_submit_button("إضافة المخاطر"):
                if not description or not response:
                    st.error("يرجى إدخال جميع البيانات المطلوبة")
                else:
                    if 'project_risks' not in st.session_state:
                        st.session_state.project_risks = []

                    risk = {
                        'category': category,
                        'description': description,
                        'probability': probability,
                        'impact': impact,
                        'response': response,
                        'responsible': responsible,
                        'risk_score': self.probability_levels[probability] * self.impact_levels[impact]
                    }

                    st.session_state.project_risks.append(risk)
                    st.success("تم إضافة المخاطر بنجاح")
                    st.rerun()

        # عرض المخاطر المضافة
        if 'project_risks' in st.session_state and st.session_state.project_risks:
            st.markdown("### المخاطر المحددة")
            risks_df = pd.DataFrame(st.session_state.project_risks)
            # تعيين أسماء الأعمدة بالعربية
            column_names = {
                'category': 'فئة المخاطر',
                'description': 'وصف المخاطر',
                'probability': 'احتمالية الحدوث',
                'impact': 'مستوى التأثير',
                'response': 'استراتيجية الاستجابة',
                'responsible': 'المسؤول',
                'risk_score': 'درجة الخطورة'
            }
            risks_df = risks_df.rename(columns=column_names)
            st.dataframe(risks_df)

            # عرض مصفوفة المخاطر
            self._render_risk_matrix(risks_df)

    def _render_risk_matrix(self, risks_df):
        """عرض مصفوفة المخاطر"""
        st.markdown("### مصفوفة المخاطر")

        matrix_data = np.zeros((4, 4))
        for _, risk in risks_df.iterrows():
            prob_idx = self.probability_levels[risk['احتمالية الحدوث']] - 1
            impact_idx = self.impact_levels[risk['مستوى التأثير']] - 1
            matrix_data[prob_idx, impact_idx] += 1

        fig = px.imshow(
            matrix_data,
            labels=dict(x="التأثير", y="الاحتمالية"),
            x=list(self.impact_levels.keys()),
            y=list(self.probability_levels.keys())
        )
        st.plotly_chart(fig)