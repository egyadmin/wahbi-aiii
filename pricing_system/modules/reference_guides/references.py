
import streamlit as st
import docx
import pandas as pd
from pathlib import Path
import os
from datetime import datetime

class ReferenceGuides:
    def __init__(self):
        self.guides_path = Path("attached_assets")
        
    def render(self):
        st.title("المراجع والأدلة الإرشادية")
        
        # Add completion button at the top
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✅ إنهاء التسعير وحفظ البيانات", key="complete_pricing_btn", type="primary"):
                try:
                    if 'current_project' in st.session_state and 'boq_items' in st.session_state.current_project:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        total_price = sum(item['total_price'] for item in st.session_state.current_project['boq_items'])
                        
                        # Calculate local content if available
                        local_content = 0
                        if hasattr(st.session_state, 'local_content'):
                            local_content = (
                                st.session_state.local_content.get('materials_local', 0.4) * 40 +
                                st.session_state.local_content.get('equipment_local', 0.3) * 20 +
                                st.session_state.local_content.get('labor_local', 0.8) * 30 +
                                st.session_state.local_content.get('subcontractors_local', 0.5) * 10
                            )
                        
                        pricing_data = {
                            'timestamp': timestamp,
                            'project_name': st.session_state.current_project.get('name', 'مشروع جديد'),
                            'total_price': total_price,
                            'items': st.session_state.current_project['boq_items'],
                            'local_content': local_content
                        }
                        
                        if 'saved_pricing' not in st.session_state:
                            st.session_state.saved_pricing = []
                        
                        st.session_state.saved_pricing.append(pricing_data)
                        st.success("✅ تم حفظ وإنهاء التسعير بنجاح!")
                        
                        # Export to Excel
                        try:
                            export_path = "data/exports"
                            os.makedirs(export_path, exist_ok=True)
                            excel_file = f"{export_path}/final_pricing_{timestamp}.xlsx"
                            
                            df = pd.DataFrame(st.session_state.current_project['boq_items'])
                            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                                df.to_excel(writer, index=False, sheet_name='التسعير النهائي')
                                worksheet = writer.sheets['التسعير النهائي']
                                worksheet['A1'] = f"اسم المشروع: {pricing_data['project_name']}"
                                worksheet['A2'] = f"التاريخ: {timestamp}"
                                worksheet['A3'] = f"إجمالي السعر: {total_price:,.2f} ريال"
                                worksheet['A4'] = f"نسبة المحتوى المحلي: {local_content:.1f}%"
                            
                            st.success("📊 تم تصدير ملف Excel للتسعير النهائي")
                        except Exception as e:
                            st.warning(f"لم يتم تصدير ملف Excel: {str(e)}")
                    else:
                        st.warning("لا توجد بيانات تسعير لحفظها")
                except Exception as e:
                    st.error(f"حدث خطأ أثناء حفظ التسعير: {str(e)}")
        
        st.markdown("---")
        
        # عرض الدليل
        with st.expander("دليل تحليل أسعار بنود الإنشاءات", expanded=True):
            try:
                doc = docx.Document(self.guides_path / "دليل تحليل أسعار بنود الإنشاءات.docx")
                for paragraph in doc.paragraphs:
                    st.write(paragraph.text)
            except Exception:
                st.error("لم يتم العثور على ملف الدليل")
            
            # إضافة رابط لتحميل الدليل
            with open(self.guides_path / "دليل تحليل أسعار بنود الإنشاءات.pdf", "rb") as pdf_file:
                st.download_button(
                    label="تحميل الدليل (PDF)",
                    data=pdf_file,
                    file_name="دليل_تحليل_أسعار_بنود_الإنشاءات.pdf",
                    mime="application/pdf"
                )
        
        # عرض جداول المعدلات
        with st.expander("معدلات الأداء والاستهلاك"):
            try:
                rates_df = pd.read_excel(self.guides_path / "معدلات استهلاك الخامات واداء العمالة والمعدات.xlsx")
                st.dataframe(rates_df)
            except Exception:
                st.error("لم يتم العثور على ملف المعدلات")
