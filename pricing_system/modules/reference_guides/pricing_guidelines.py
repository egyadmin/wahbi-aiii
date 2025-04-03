
import streamlit as st
import pandas as pd
from pathlib import Path

class PricingGuidelines:
    def __init__(self):
        self.guides_path = Path("attached_assets")
        
    def render(self):
        st.markdown("""
            <style>
                .guide-title {
                    color: #1f77b4;
                    font-size: 1.8rem;
                    text-align: center;
                    margin-bottom: 2rem;
                }
                .guide-section {
                    background-color: #f8f9fa;
                    padding: 1rem;
                    border-radius: 0.5rem;
                    margin-bottom: 1rem;
                }
                .guide-section h3 {
                    color: #2c3e50;
                    margin-bottom: 1rem;
                }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<h1 class="guide-title">الدليل المرجعي للتسعير</h1>', unsafe_allow_html=True)
        
        # القسم الأول: دليل تحليل الأسعار
        with st.expander("دليل تحليل أسعار بنود الإنشاءات", expanded=True):
            st.markdown("""
            ### محتويات الدليل:
            1. المبادئ الأساسية لتحليل الأسعار
            2. طرق حساب تكاليف المواد
            3. معايير تقدير تكاليف العمالة
            4. حساب تكاليف المعدات
            5. المصروفات غير المباشرة
            6. هوامش الربح المقترحة
            """)
            
            # زر تحميل الدليل
            try:
                with open(self.guides_path / "دليل تحليل أسعار بنود الإنشاءات.pdf", "rb") as pdf_file:
                    st.download_button(
                        label="تحميل الدليل الكامل (PDF)",
                        data=pdf_file,
                        file_name="pricing_analysis_guide.pdf",
                        mime="application/pdf"
                    )
            except FileNotFoundError:
                st.warning("ملف الدليل غير متوفر حالياً")

        # القسم الثاني: معدلات الأداء
        with st.expander("معدلات الأداء القياسية"):
            try:
                rates_df = pd.read_excel(self.guides_path / "معدلات استهلاك الخامات واداء العمالة والمعدات.xlsx")
                st.dataframe(rates_df)
            except Exception:
                st.error("لم يتم العثور على ملف المعدلات")

        # القسم الثالث: النصائح والإرشادات
        with st.expander("نصائح وإرشادات التسعير"):
            st.markdown("""
            ### أفضل الممارسات في التسعير:
            
            #### 1. تحليل السوق
            - دراسة أسعار السوق الحالية
            - تحليل المنافسين
            - مراقبة اتجاهات الأسعار
            
            #### 2. تقييم المخاطر
            - تحديد المخاطر المحتملة
            - تقدير تأثيرها على التكلفة
            - وضع احتياطيات مناسبة
            
            #### 3. حساب التكاليف
            - تحديد التكاليف المباشرة بدقة
            - تضمين جميع التكاليف غير المباشرة
            - مراعاة التضخم والتغيرات المحتملة
            
            #### 4. تحديد هامش الربح
            - تحليل هوامش الربح التاريخية
            - مراعاة ظروف السوق
            - تحديد الحد الأدنى المقبول
            """)
