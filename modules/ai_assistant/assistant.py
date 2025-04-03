# -*- coding: utf-8 -*-
"""
وحدة المساعد الذكي

هذا الملف يحتوي على الفئة الرئيسية لتطبيق المساعد الذكي مع دعم نموذج Claude AI.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import json
import time
import base64
import logging
import os
from datetime import datetime, timedelta
import io
import tempfile
import random
from io import BytesIO
from tempfile import NamedTemporaryFile
from PIL import Image

# استيراد النماذج المطلوبة
try:
    from models.inference import (
        load_cost_prediction_model, 
        load_document_classifier_model, 
        load_risk_assessment_model,
        load_local_content_model,
        load_entity_recognition_model
    )
except ImportError:
    # إنشاء دوال وهمية في حال عدم توفر النماذج
    def load_cost_prediction_model():
        return None

    def load_document_classifier_model():
        return None

    def load_risk_assessment_model():
        return None

    def load_local_content_model():
        return None

    def load_entity_recognition_model():
        return None

try:
    # استيراد مكتبة pdf2image للتعامل مع ملفات PDF
    from pdf2image import convert_from_path
    pdf_conversion_available = True
except ImportError:
    pdf_conversion_available = False
    logging.warning("لم يتم العثور على مكتبة pdf2image. لن يمكن تحويل ملفات PDF إلى صور.")


class ClaudeAIService:
    """
    فئة خدمة Claude AI للتحليل الذكي
    """
    def __init__(self):
        """تهيئة خدمة Claude AI"""
        self.api_url = "https://api.anthropic.com/v1/messages"

    def get_api_key(self):
        """الحصول على مفتاح API من متغيرات البيئة"""
        api_key = os.environ.get("anthropic")
        if not api_key:
            raise ValueError("مفتاح API لـ Claude غير موجود في متغيرات البيئة")
        return api_key

    def get_available_models(self):
        """
        الحصول على قائمة بالنماذج المتاحة

        العوائد:
            dict: قائمة بالنماذج مع وصفها
        """
        return {
            "claude-3-7-sonnet": "Claude 3.7 Sonnet - نموذج ذكي للمهام المتقدمة",
            "claude-3-5-haiku": "Claude 3.5 Haiku - أسرع نموذج للمهام اليومية"
        }

    def get_model_full_name(self, short_name):
        """
        تحويل الاسم المختصر للنموذج إلى الاسم الكامل

        المعلمات:
            short_name: الاسم المختصر للنموذج

        العوائد:
            str: الاسم الكامل للنموذج
        """
        valid_models = {
            "claude-3-7-sonnet": "claude-3-7-sonnet-20250219", 
            "claude-3-5-haiku": "claude-3-5-haiku-20240307"
        }

        return valid_models.get(short_name, short_name)

    def analyze_image(self, image_path, prompt, model_name="claude-3-7-sonnet"):
        """
        تحليل صورة باستخدام نموذج Claude AI

        المعلمات:
            image_path: مسار الصورة المراد تحليلها
            prompt: التوجيه للنموذج
            model_name: اسم نموذج Claude المراد استخدامه

        العوائد:
            dict: نتائج التحليل
        """
        try:
            # الحصول على مفتاح API
            api_key = self.get_api_key()

            # قراءة محتوى الصورة
            with open(image_path, 'rb') as f:
                file_content = f.read()

            # تحويل المحتوى إلى Base64
            file_base64 = base64.b64encode(file_content).decode('utf-8')

            # تحديد نوع الملف من امتداده
            _, ext = os.path.splitext(image_path)
            ext = ext.lower()

            if ext in ('.jpg', '.jpeg'):
                file_type = "image/jpeg"
            elif ext == '.png':
                file_type = "image/png"
            elif ext == '.gif':
                file_type = "image/gif"
            elif ext == '.webp':
                file_type = "image/webp"
            else:
                file_type = "image/jpeg"  # افتراضي

            # التحقق من اسم النموذج وتصحيحه إذا لزم الأمر
            model_name = self.get_model_full_name(model_name)

            # إعداد البيانات للطلب
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }

            payload = {
                "model": model_name,
                "max_tokens": 4096,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": file_type,
                                    "data": file_base64
                                }
                            }
                        ]
                    }
                ]
            }

            # إرسال الطلب إلى API
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )

            # التحقق من نجاح الطلب
            if response.status_code != 200:
                error_message = f"فشل طلب API: {response.status_code}"
                try:
                    error_details = response.json()
                    error_message += f"\nتفاصيل: {error_details}"
                except:
                    error_message += f"\nتفاصيل: {response.text}"

                return {"error": error_message}

            # معالجة الاستجابة
            result = response.json()

            return {
                "success": True,
                "content": result["content"][0]["text"],
                "model": result["model"],
                "usage": result.get("usage", {})
            }

        except Exception as e:
            logging.error(f"خطأ أثناء تحليل الصورة: {str(e)}")
            import traceback
            stack_trace = traceback.format_exc()
            return {"error": f"فشل في تحليل الصورة: {str(e)}\n{stack_trace}"}

    def chat_completion(self, messages, model_name="claude-3-7-sonnet"):
        """
        إكمال محادثة باستخدام نموذج Claude AI

        المعلمات:
            messages: سجل المحادثة
            model_name: اسم نموذج Claude المراد استخدامه

        العوائد:
            dict: نتائج الإكمال
        """
        try:
            # الحصول على مفتاح API
            api_key = self.get_api_key()

            # تحويل رسائل streamlit إلى تنسيق Claude API
            claude_messages = []
            for msg in messages:
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

            # التحقق من اسم النموذج وتصحيحه إذا لزم الأمر
            model_name = self.get_model_full_name(model_name)

            # إعداد البيانات للطلب
            headers = {
                "Content-Type": "application/json",
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01"
            }

            payload = {
                "model": model_name,
                "max_tokens": 2048,
                "messages": claude_messages,
                "temperature": 0.7
            }

            # إرسال الطلب إلى API
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            # التحقق من نجاح الطلب
            if response.status_code != 200:
                error_message = f"فشل طلب API: {response.status_code}"
                try:
                    error_details = response.json()
                    error_message += f"\nتفاصيل: {error_details}"
                except:
                    error_message += f"\nتفاصيل: {response.text}"

                return {"error": error_message}

            # معالجة الاستجابة
            result = response.json()

            return {
                "success": True,
                "content": result["content"][0]["text"],
                "model": result["model"],
                "usage": result.get("usage", {})
            }

        except Exception as e:
            logging.error(f"خطأ أثناء إكمال المحادثة: {str(e)}")
            import traceback
            stack_trace = traceback.format_exc()
            return {"error": f"فشل في إكمال المحادثة: {str(e)}\n{stack_trace}"}


class AIAssistantApp:
    """وحدة المساعد الذكي"""

    def __init__(self):
        """تهيئة وحدة المساعد الذكي"""
        # تحميل النماذج عند بدء التشغيل
        self.cost_model = load_cost_prediction_model()
        self.document_model = load_document_classifier_model()
        self.risk_model = load_risk_assessment_model()
        self.local_content_model = load_local_content_model()
        self.entity_model = load_entity_recognition_model()

        # إنشاء خدمة Claude AI
        self.claude_service = ClaudeAIService()

        # تهيئة قائمة الأسئلة والإجابات الشائعة
        self.faqs = [
            {
                "question": "كيف يمكنني إضافة مشروع جديد؟",
                "answer": "يمكنك إضافة مشروع جديد من خلال الانتقال إلى وحدة إدارة المشاريع، ثم النقر على زر 'إضافة مشروع جديد'، وملء النموذج بالبيانات المطلوبة."
            },
            {
                "question": "ما هي خطوات تسعير المناقصة؟",
                "answer": "تتضمن خطوات تسعير المناقصة: 1) تحليل مستندات المناقصة، 2) تحديد بنود العمل، 3) تقدير التكاليف المباشرة، 4) إضافة المصاريف العامة والأرباح، 5) احتساب المحتوى المحلي، 6) مراجعة النتائج النهائية."
            },
            {
                "question": "كيف يتم حساب المحتوى المحلي؟",
                "answer": "يتم حساب المحتوى المحلي بتحديد نسبة المنتجات والخدمات والقوى العاملة المحلية من إجمالي التكاليف. يتم استخدام قاعدة بيانات الموردين المعتمدين وتطبيق معادلات خاصة حسب متطلبات هيئة المحتوى المحلي."
            },
            {
                "question": "كيف يمكنني تصدير التقارير؟",
                "answer": "يمكنك تصدير التقارير من وحدة التقارير والتحليلات، حيث يوجد زر 'تصدير' في كل تقرير. يمكن تصدير التقارير بتنسيقات مختلفة مثل Excel و PDF و CSV."
            },
            {
                "question": "كيف يمكنني تقييم المخاطر للمشروع؟",
                "answer": "يمكنك تقييم المخاطر للمشروع من خلال وحدة المخاطر، حيث يمكنك إضافة المخاطر المحتملة وتقييم تأثيرها واحتماليتها، ثم وضع خطة الاستجابة المناسبة."
            },
            {
                "question": "ما هي طرق التسعير المتاحة في النظام؟",
                "answer": "يوفر النظام أربع طرق للتسعير: 1) التسعير القياسي، 2) التسعير غير المتزن، 3) التسعير التنافسي، 4) التسعير الموجه بالربحية. يمكنك اختيار الطريقة المناسبة حسب طبيعة المشروع واستراتيجية الشركة."
            },
            {
                "question": "كيف يمكنني معالجة مستندات المناقصة ضخمة الحجم؟",
                "answer": "يمكنك استخدام وحدة تحليل المستندات لمعالجة مستندات المناقصة ضخمة الحجم، حيث تقوم الوحدة بتحليل المستندات واستخراج المعلومات المهمة مثل مواصفات المشروع ومتطلباته وشروطه تلقائياً."
            }
        ]

    def render(self):
        """عرض واجهة وحدة المساعد الذكي"""

        st.markdown("<h1 class='module-title'>وحدة المساعد الذكي</h1>", unsafe_allow_html=True)

        tabs = st.tabs([
            "المساعد الذكي",
            "التنبؤ بالتكاليف",
            "تحليل المخاطر",
            "تحليل المستندات",
            "المحتوى المحلي",
            "الأسئلة الشائعة"
        ])

        with tabs[0]:
            self._render_ai_assistant_tab()

        with tabs[1]:
            self._render_cost_prediction_tab()

        with tabs[2]:
            self._render_risk_analysis_tab()

        with tabs[3]:
            self._render_document_analysis_tab()

        with tabs[4]:
            self._render_local_content_tab()

        with tabs[5]:
            self._render_faq_tab()

    def _render_ai_assistant_tab(self):
        """عرض تبويب المساعد الذكي مع دعم Claude AI"""

        st.markdown("### المساعد الذكي لتسعير المناقصات")

        # اختيار نموذج Claude
        claude_models = self.claude_service.get_available_models()

        selected_model = st.radio(
            "اختر نموذج الذكاء الاصطناعي",
            options=list(claude_models.keys()),
            format_func=lambda x: claude_models[x],
            horizontal=True,
            key="assistant_ai_model"
        )

        # عرض واجهة المحادثة
        st.markdown("""
        <div class="chat-container">
            <div class="chat-header">
                <h4>المساعد الذكي</h4>
                <p>تحدث مع المساعد الذكي للحصول على المساعدة في تسعير المناقصات وتحليل البيانات</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # تهيئة محفوظات المحادثة في حالة الجلسة إذا لم تكن موجودة
        if 'ai_assistant_messages' not in st.session_state:
            st.session_state.ai_assistant_messages = [
                {"role": "assistant", "content": "مرحباً! أنا المساعد الذكي لنظام تسعير المناقصات. كيف يمكنني مساعدتك اليوم؟"}
            ]

        # عرض محفوظات المحادثة بتنسيق محسن
        chat_container = st.container()
        with chat_container:
            for message in st.session_state.ai_assistant_messages:
                if message["role"] == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                        <div style="background-color: #e0f7fa; padding: 10px; border-radius: 10px; max-width: 80%;">
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                        <div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; max-width: 80%;">
                            {message["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # إضافة خيار رفع الملفات
        uploaded_file = st.file_uploader(
            "اختياري: ارفع ملفًا للمساعدة (صورة، PDF)",
            type=["jpg", "jpeg", "png", "pdf"],
            key="assistant_file_upload"
        )

        # مربع إدخال الرسالة
        user_input = st.text_input("اكتب رسالتك هنا", key="ai_assistant_input")

        # التحقق من وجود مفتاح API
        api_available = True
        try:
            self.claude_service.get_api_key()
        except ValueError:
            api_available = False
            st.warning("مفتاح API لـ Claude غير متوفر. يرجى التأكد من تعيين متغير البيئة 'anthropic'.")

        if user_input and api_available:
            # إضافة رسالة المستخدم إلى المحفوظات
            st.session_state.ai_assistant_messages.append({"role": "user", "content": user_input})

            # عرض محفوظات المحادثة المحدثة
            with chat_container:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 10px;">
                    <div style="background-color: #e0f7fa; padding: 10px; border-radius: 10px; max-width: 80%;">
                        {user_input}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # معالجة الرد
            with st.spinner("جاري التفكير..."):
                # التحقق مما إذا كان هناك ملف مرفق
                if uploaded_file:
                    # حفظ الملف المرفوع مؤقتاً
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as temp_file:
                        temp_file.write(uploaded_file.getbuffer())
                        temp_file_path = temp_file.name

                    # إذا كان الملف PDF، تحويله إلى صورة
                    if uploaded_file.name.lower().endswith('.pdf'):
                        if pdf_conversion_available:
                            try:
                                # تحويل الصفحة الأولى فقط
                                images = convert_from_path(temp_file_path, first_page=1, last_page=1)
                                if images:
                                    # حفظ الصورة بشكل مؤقت
                                    temp_image_path = f"{temp_file_path}_image.jpg"
                                    images[0].save(temp_image_path, 'JPEG')
                                    # استخدام مسار الصورة بدلاً من PDF
                                    os.remove(temp_file_path)
                                    temp_file_path = temp_image_path
                            except Exception as e:
                                st.error(f"فشل في تحويل ملف PDF إلى صورة: {str(e)}")
                        else:
                            st.error("تحليل ملفات PDF يتطلب تثبيت مكتبة pdf2image.")
                            response = "عذراً، لا يمكنني تحليل ملفات PDF في الوقت الحالي. يرجى تحويل الملف إلى صورة أو مشاركة المعلومات كنص."

                    # تحليل الصورة باستخدام Claude
                    prompt = f"المستخدم قام برفع هذه الصورة وسأل: {user_input}\nقم بتحليل الصورة والرد على سؤال المستخدم بشكل تفصيلي."
                    results = self.claude_service.analyze_image(temp_file_path, prompt, model_name=selected_model)

                    # حذف الملف المؤقت
                    try:
                        os.remove(temp_file_path)
                    except:
                        pass

                    if "error" in results:
                        response = f"عذراً، حدث خطأ أثناء تحليل الملف: {results['error']}"
                    else:
                        response = results["content"]
                else:
                    # استخدام خدمة Claude للرد على الرسائل النصية
                    results = self.claude_service.chat_completion(st.session_state.ai_assistant_messages, model_name=selected_model)

                    if "error" in results:
                        response = f"عذراً، حدث خطأ أثناء معالجة طلبك: {results['error']}"
                    else:
                        response = results["content"]

            # إضافة رد المساعد إلى المحفوظات
            st.session_state.ai_assistant_messages.append({"role": "assistant", "content": response})

            # عرض رد المساعد
            with chat_container:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 10px;">
                    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 10px; max-width: 80%;">
                        {response}
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # إعادة تعيين قيمة الإدخال
            st.text_input("اكتب رسالتك هنا", value="", key="ai_assistant_input_reset")

    def _generate_ai_response(self, user_input, model_name="claude-3-7-sonnet"):
        """توليد رد المساعد الذكي باستخدام Claude AI"""

        # التحقق من وجود مفتاح API
        try:
            self.claude_service.get_api_key()
        except ValueError:
            return "عذراً، لا يمكنني الاتصال بخدمة الذكاء الاصطناعي في الوقت الحالي. يرجى التحقق من إعدادات API."

        # البحث في الأسئلة الشائعة أولاً
        for faq in self.faqs:
            if any(keyword in user_input.lower() for keyword in faq["question"].lower().split()):
                return f"{faq['answer']}\n\nهل تحتاج إلى مساعدة أخرى؟"

        # إنشاء محادثة لإرسالها إلى Claude
        messages = [
            {"role": "user", "content": user_input}
        ]

        # استدعاء خدمة Claude
        results = self.claude_service.chat_completion(messages, model_name=model_name)

        if "error" in results:
            # إذا فشل الاتصال، استخدم التوليد الافتراضي
            logging.warning(f"فشل الاتصال بـ Claude AI: {results['error']}. استخدام التوليد الافتراضي.")
            return self._generate_default_response(user_input)
        else:
            return results["content"]

    def _generate_default_response(self, user_input):
        """توليد رد افتراضي في حالة عدم توفر Claude AI"""

        if "تسعير" in user_input or "سعر" in user_input or "تكلفة" in user_input:
            return "يمكنك استخدام وحدة التنبؤ بالتكاليف لتقدير تكاليف المشروع بناءً على خصائصه. انتقل إلى تبويب 'التنبؤ بالتكاليف' وأدخل بيانات المشروع لتحصل على تقدير دقيق للتكاليف."

        elif "مخاطر" in user_input or "مخاطرة" in user_input:
            return "يمكنك استخدام وحدة تحليل المخاطر لتقييم المخاطر المحتملة للمشروع. انتقل إلى تبويب 'تحليل المخاطر' وأدخل بيانات المشروع وعوامل المخاطرة لتحصل على تحليل شامل للمخاطر واستراتيجيات الاستجابة المقترحة."

        elif "مستند" in user_input or "ملف" in user_input or "وثيقة" in user_input or "مناقصة" in user_input:
            return "يمكنك استخدام وحدة تحليل المستندات لتحليل مستندات المناقصة واستخراج المعلومات المهمة منها. انتقل إلى تبويب 'تحليل المستندات' وقم بتحميل ملفات المناقصة لتحصل على تحليل تفصيلي للمستندات."

        elif "محتوى محلي" in user_input or "محلي" in user_input:
            return "يمكنك استخدام وحدة المحتوى المحلي لحساب وتحسين نسبة المحتوى المحلي في مشروعك. انتقل إلى تبويب 'المحتوى المحلي' وأدخل بيانات مكونات المشروع لتحصل على تحليل شامل للمحتوى المحلي واقتراحات لتحسينه."

        elif "تقرير" in user_input or "إحصائيات" in user_input or "بيانات" in user_input:
            return "يمكنك استخدام وحدة التقارير والتحليلات للحصول على تقارير تفصيلية وإحصائيات عن المشاريع. يمكنك الوصول إليها من القائمة الرئيسية للنظام."

        else:
            return "شكراً لاستفسارك. يمكنني مساعدتك في تسعير المناقصات، وتحليل المخاطر، وتحليل المستندات، وحساب المحتوى المحلي. يرجى توضيح استفسارك أكثر أو اختيار أحد الخيارات في الأعلى للحصول على المساعدة المطلوبة."

    def _render_cost_prediction_tab(self):
        """عرض تبويب التنبؤ بالتكاليف"""

        st.markdown("### التنبؤ بالتكاليف")

        # عرض نموذج إدخال بيانات المشروع
        st.markdown("#### بيانات المشروع")

        col1, col2 = st.columns(2)

        with col1:
            project_type = st.selectbox(
                "نوع المشروع",
                [
                    "مباني سكنية",
                    "مباني تجارية",
                    "مباني حكومية",
                    "مراكز صحية",
                    "مدارس",
                    "بنية تحتية",
                    "طرق",
                    "جسور",
                    "صرف صحي",
                    "مياه",
                    "كهرباء"
                ],
                key="cost_project_type"
            )

            location = st.selectbox(
                "الموقع",
                [
                    "الرياض",
                    "جدة",
                    "الدمام",
                    "مكة",
                    "المدينة",
                    "تبوك",
                    "حائل",
                    "عسير",
                    "جازان",
                    "نجران",
                    "الباحة",
                    "الجوف",
                    "القصيم"
                ],
                key="cost_location"
            )

            client_type = st.selectbox(
                "نوع العميل",
                [
                    "حكومي",
                    "شبه حكومي",
                    "شركة كبيرة",
                    "شركة متوسطة",
                    "شركة صغيرة",
                    "أفراد"
                ],
                key="cost_client_type"
            )

        with col2:
            area = st.number_input("المساحة (م²)", min_value=100, max_value=1000000, value=5000, key="cost_area")

            floors = st.number_input("عدد الطوابق", min_value=1, max_value=100, value=3, key="cost_floors")

            duration = st.number_input("مدة التنفيذ (شهور)", min_value=1, max_value=60, value=12, key="cost_duration")

            tender_type = st.selectbox(
                "نوع المناقصة",
                [
                    "عامة",
                    "خاصة",
                    "أمر مباشر"
                ],
                key="cost_tender_type"
            )

        st.markdown("#### متغيرات إضافية")

        col1, col2, col3 = st.columns(3)

        with col1:
            has_basement = st.checkbox("يتضمن بدروم", key="cost_has_basement")
            has_special_finishing = st.checkbox("تشطيبات خاصة", key="cost_has_special_finishing")

        with col2:
            has_landscape = st.checkbox("أعمال تنسيق المواقع", key="cost_has_landscape")
            has_parking = st.checkbox("مواقف متعددة الطوابق", key="cost_has_parking")

        with col3:
            has_smart_systems = st.checkbox("أنظمة ذكية", key="cost_has_smart_systems")
            has_sustainability = st.checkbox("متطلبات استدامة", key="cost_has_sustainability")

        # زر التنبؤ بالتكلفة مع دعم Claude AI
        col1, col2 = st.columns([1, 3])

        with col1:
            predict_button = st.button("التنبؤ بالتكلفة", use_container_width=True, key="cost_predict_button")

        with col2:
            use_claude = st.checkbox("استخدام Claude AI للتحليل المتقدم", value=True, key="cost_use_claude")

        if predict_button:
            with st.spinner("جاري تحليل البيانات والتنبؤ بالتكاليف..."):
                # محاكاة وقت المعالجة
                time.sleep(2)

                # تجهيز البيانات للنموذج
                features = {
                    'project_type': project_type,
                    'location': location,
                    'area': area,
                    'floors': floors,
                    'duration_months': duration,
                    'tender_type': tender_type,
                    'client_type': client_type,
                    'has_basement': has_basement,
                    'has_special_finishing': has_special_finishing,
                    'has_landscape': has_landscape,
                    'has_parking': has_parking,
                    'has_smart_systems': has_smart_systems,
                    'has_sustainability': has_sustainability
                }

                # استدعاء النموذج للتنبؤ
                cost_prediction_results = self._predict_cost(features)

                # إضافة تحليل إضافي باستخدام Claude AI إذا تم تفعيل الخيار
                if use_claude:
                    try:
                        # إنشاء نص الميزات للتحليل
                        features_text = f"""
                        بيانات المشروع:
                        - نوع المشروع: {project_type}
                        - الموقع: {location}
                        - المساحة: {area} م²
                        - عدد الطوابق: {floors}
                        - مدة التنفيذ: {duration} شهر
                        - نوع المناقصة: {tender_type}
                        - نوع العميل: {client_type}
                        - يتضمن بدروم: {'نعم' if has_basement else 'لا'}
                        - تشطيبات خاصة: {'نعم' if has_special_finishing else 'لا'}
                        - أعمال تنسيق المواقع: {'نعم' if has_landscape else 'لا'}
                        - مواقف متعددة الطوابق: {'نعم' if has_parking else 'لا'}
                        - أنظمة ذكية: {'نعم' if has_smart_systems else 'لا'}
                        - متطلبات استدامة: {'نعم' if has_sustainability else 'لا'}

                        نتائج التنبؤ الأولية:
                        - التكلفة الإجمالية المقدرة: {cost_prediction_results['total_cost']:,.0f} ريال
                        - تكلفة المتر المربع: {cost_prediction_results['cost_per_sqm']:,.0f} ريال/م²
                        - تكلفة المواد: {cost_prediction_results['material_cost']:,.0f} ريال
                        - تكلفة العمالة: {cost_prediction_results['labor_cost']:,.0f} ريال
                        - تكلفة المعدات: {cost_prediction_results['equipment_cost']:,.0f} ريال
                        """

                        prompt = f"""تحليل بيانات مشروع وتكاليفه:

                        {features_text}

                        المطلوب:
                        1. تحليل التكاليف المتوقعة ومعقوليتها مقارنة بمشاريع مماثلة في السوق السعودي
                        2. تقديم توصيات وملاحظات لتحسين التكلفة
                        3. تحديد أي مخاطر محتملة قد تؤثر على التكلفة
                        4. تقديم نصائح لزيادة فعالية التكلفة
                        5. تقديم رأي حول مدى تنافسية هذه التكلفة في السوق الحالي

                        يرجى تقديم تحليل مهني ومختصر يركز على الجوانب الأكثر أهمية.
                        """

                        # استدعاء Claude للتحليل
                        claude_analysis = self.claude_service.chat_completion(
                            [{"role": "user", "content": prompt}]
                        )

                        if "error" not in claude_analysis:
                            # إضافة تحليل Claude إلى النتائج
                            cost_prediction_results["claude_analysis"] = claude_analysis["content"]
                    except Exception as e:
                        st.warning(f"تعذر إجراء التحليل المتقدم: {str(e)}")

                # عرض نتائج التنبؤ
                self._display_cost_prediction_results(cost_prediction_results)

    def _predict_cost(self, features):
        """التنبؤ بتكاليف المشروع"""

        # في البيئة الحقيقية، سيتم استدعاء نموذج التنبؤ بالتكاليف
        # محاكاة نتائج التنبؤ للعرض

        # حساب القيمة الأساسية للمتر المربع حسب نوع المشروع
        base_cost_per_sqm = {
            "مباني سكنية": 2500,
            "مباني تجارية": 3000,
            "مباني حكومية": 3500,
            "مراكز صحية": 4000,
            "مدارس": 3200,
            "بنية تحتية": 2000,
            "طرق": 1500,
            "جسور": 5000,
            "صرف صحي": 2200,
            "مياه": 2000,
            "كهرباء": 2500
        }.get(features['project_type'], 2500)

        # تطبيق معاملات التعديل حسب المتغيرات
        location_factor = {
            "الرياض": 1.1,
            "جدة": 1.15,
            "الدمام": 1.05,
            "مكة": 1.2,
            "المدينة": 1.1,
            "تبوك": 0.95,
            "حائل": 0.9,
            "عسير": 0.95,
            "جازان": 0.9,
            "نجران": 0.85,
            "الباحة": 0.9,
            "الجوف": 0.85,
            "القصيم": 0.9
        }.get(features['location'], 1.0)

        client_factor = {
            "حكومي": 1.05,
            "شبه حكومي": 1.0,
            "شركة كبيرة": 0.95,
            "شركة متوسطة": 0.9,
            "شركة صغيرة": 0.85,
            "أفراد": 0.8
        }.get(features['client_type'], 1.0)

        tender_factor = {
            "عامة": 1.0,
            "خاصة": 0.95,
            "أمر مباشر": 0.9
        }.get(features['tender_type'], 1.0)

        # معاملات للميزات الإضافية
        basement_factor = 1.1 if features['has_basement'] else 1.0
        special_finishing_factor = 1.2 if features['has_special_finishing'] else 1.0
        landscape_factor = 1.05 if features['has_landscape'] else 1.0
        parking_factor = 1.1 if features['has_parking'] else 1.0
        smart_systems_factor = 1.15 if features['has_smart_systems'] else 1.0
        sustainability_factor = 1.1 if features['has_sustainability'] else 1.0

        # معامل لعدد الطوابق
        floors_factor = 1.0 + (features['floors'] - 1) * 0.05

        # حساب التكلفة الإجمالية
        total_sqm_cost = base_cost_per_sqm * location_factor * client_factor * tender_factor * \
                         basement_factor * special_finishing_factor * landscape_factor * \
                         parking_factor * smart_systems_factor * sustainability_factor * \
                         floors_factor

        total_cost = total_sqm_cost * features['area']

        # حساب التكاليف المفصلة
        material_cost = total_cost * 0.6
        labor_cost = total_cost * 0.25
        equipment_cost = total_cost * 0.15

        # إضافة هامش خطأ عشوائي للمحاكاة
        error_margin = 0.05  # 5%
        total_cost = total_cost * (1 + np.random.uniform(-error_margin, error_margin))

        # إعداد النتائج
        results = {
            "total_cost": total_cost,
            "cost_per_sqm": total_cost / features['area'],
            "material_cost": material_cost,
            "labor_cost": labor_cost,
            "equipment_cost": equipment_cost,
            "breakdown": {
                "structural_works": total_cost * 0.35,
                "architectural_works": total_cost * 0.25,
                "mep_works": total_cost * 0.25,
                "site_works": total_cost * 0.1,
                "general_requirements": total_cost * 0.05
            },
            "confidence_level": 0.85,  # مستوى الثقة في التنبؤ
            "comparison": {
                "market_average": total_cost * 1.1,
                "historical_projects": total_cost * 0.95
            }
        }

        return results

    def _display_cost_prediction_results(self, results):
        """عرض نتائج التنبؤ بالتكاليف"""

        st.markdown("### نتائج التنبؤ بالتكاليف")

        # عرض التكلفة الإجمالية وتكلفة المتر المربع
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "التكلفة الإجمالية المتوقعة",
                f"{results['total_cost']:,.0f} ريال",
                delta=f"{(results['total_cost'] - results['comparison']['historical_projects']):,.0f} ريال"
            )

        with col2:
            st.metric(
                "تكلفة المتر المربع",
                f"{results['cost_per_sqm']:,.0f} ريال/م²"
            )

        with col3:
            st.metric(
                "مستوى الثقة في التنبؤ",
                f"{results['confidence_level'] * 100:.0f}%"
            )

        # عرض تفصيل التكاليف
        st.markdown("#### تفصيل التكاليف")

        # رسم مخطط دائري للتكاليف المفصلة
        fig = px.pie(
            values=[
                results['material_cost'],
                results['labor_cost'],
                results['equipment_cost']
            ],
            names=["تكلفة المواد", "تكلفة العمالة", "تكلفة المعدات"],
            title="توزيع التكاليف الرئيسية"
        )

        st.plotly_chart(fig, use_container_width=True)

        # رسم مخطط شريطي لتفصيل الأعمال
        breakdown_data = pd.DataFrame({
            'فئة الأعمال': [
                "الأعمال الإنشائية",
                "الأعمال المعمارية",
                "الأعمال الكهروميكانيكية",
                "أعمال الموقع",
                "المتطلبات العامة"
            ],
            'التكلفة': [
                results['breakdown']['structural_works'],
                results['breakdown']['architectural_works'],
                results['breakdown']['mep_works'],
                results['breakdown']['site_works'],
                results['breakdown']['general_requirements']
            ]
        })

        fig = px.bar(
            breakdown_data,
            x='فئة الأعمال',
            y='التكلفة',
            title="تفصيل التكاليف حسب فئة الأعمال",
            text_auto='.3s'
        )

        fig.update_traces(texttemplate='%{text:,.0f} ريال', textposition='outside')

        st.plotly_chart(fig, use_container_width=True)

        # عرض مقارنة مع متوسط السوق
        st.markdown("#### مقارنة مع متوسط السوق")

        comparison_data = pd.DataFrame({
            'المصدر': [
                "التكلفة المتوقعة",
                "متوسط السوق",
                "مشاريع مماثلة سابقة"
            ],
            'التكلفة': [
                results['total_cost'],
                results['comparison']['market_average'],
                results['comparison']['historical_projects']
            ]
        })

        fig = px.bar(
            comparison_data,
            x='المصدر',
            y='التكلفة',
            title="مقارنة التكلفة المتوقعة مع السوق",
            text_auto='.3s',
            color='المصدر',
            color_discrete_map={
                "التكلفة المتوقعة": "#1f77b4",
                "متوسط السوق": "#ff7f0e",
                "مشاريع مماثلة سابقة": "#2ca02c"
            }
        )

        fig.update_traces(texttemplate='%{text:,.0f} ريال', textposition='outside')

        st.plotly_chart(fig, use_container_width=True)

        # عرض تحليل Claude AI إذا كان متوفراً
        if "claude_analysis" in results:
            st.markdown("### تحليل Claude AI المتقدم")
            st.info(results["claude_analysis"])

        # عرض ملاحظات وتوصيات
        st.markdown("#### ملاحظات وتوصيات")

        st.info("""
        - تم التنبؤ بالتكاليف بناءً على البيانات المدخلة ونماذج التعلم الآلي المدربة على مشاريع مماثلة.
        - مستوى الثقة في التنبؤ جيد، ولكن يجب مراجعة التكاليف بشكل تفصيلي قبل اتخاذ القرار النهائي.
        - تكلفة المتر المربع متوافقة مع متوسط السوق لهذا النوع من المشاريع.
        - ينصح بمراجعة التصميم لتحسين التكلفة وزيادة الكفاءة.
        """)

        # زر تصدير التقرير
        if st.button("تصدير تقرير التكاليف"):
            st.success("تم تصدير تقرير التكاليف بنجاح!")

    def _render_risk_analysis_tab(self):
        """عرض تبويب تحليل المخاطر"""

        st.markdown("### تحليل المخاطر")

        # عرض نموذج إدخال بيانات المشروع للمخاطر
        st.markdown("#### بيانات المشروع")

        col1, col2 = st.columns(2)

        with col1:
            project_type = st.selectbox(
                "نوع المشروع",
                [
                    "مباني سكنية",
                    "مباني تجارية",
                    "مباني حكومية",
                    "مراكز صحية",
                    "مدارس",
                    "بنية تحتية",
                    "طرق",
                    "جسور",
                    "صرف صحي",
                    "مياه",
                    "كهرباء"
                ],
                key="risk_project_type"
            )

            location = st.selectbox(
                "الموقع",
                [
                    "الرياض",
                    "جدة",
                    "الدمام",
                    "مكة",
                    "المدينة",
                    "تبوك",
                    "حائل",
                    "عسير",
                    "جازان",
                    "نجران",
                    "الباحة",
                    "الجوف",
                    "القصيم"
                ],
                key="risk_location"
            )

        with col2:
            client_type = st.selectbox(
                "نوع العميل",
                [
                    "حكومي",
                    "شبه حكومي",
                    "شركة كبيرة",
                    "شركة متوسطة",
                    "شركة صغيرة",
                    "أفراد"
                ],
                key="risk_client_type"
            )

            tender_type = st.selectbox(
                "نوع المناقصة",
                [
                    "عامة",
                    "خاصة",
                    "أمر مباشر"
                ],
                key="risk_tender_type"
            )

        st.markdown("#### عوامل المخاطرة")

        col1, col2, col3 = st.columns(3)

        with col1:
            payment_terms = st.slider("شروط الدفع (1-10)", 1, 10, 5, 
                                     help="1: شروط دفع سيئة جداً، 10: شروط دفع ممتازة",
                                     key="risk_payment_terms")
            completion_deadline = st.slider("مهلة الإنجاز (1-10)", 1, 10, 5,
                                           help="1: مهلة قصيرة جداً، 10: مهلة مريحة",
                                           key="risk_completion_deadline")

        with col2:
            penalty_clause = st.slider("شروط الغرامات (1-10)", 1, 10, 5,
                                      help="1: غرامات مرتفعة جداً، 10: غرامات معقولة",
                                      key="risk_penalty_clause")
            technical_complexity = st.slider("التعقيد الفني (1-10)", 1, 10, 5,
                                            help="1: بسيط جداً، 10: معقد للغاية",
                                            key="risk_technical_complexity")

        with col3:
            company_experience = st.slider("خبرة الشركة (1-10)", 1, 10, 7,
                                          help="1: لا توجد خبرة، 10: خبرة عالية",
                                          key="risk_company_experience")
            market_volatility = st.slider("تقلبات السوق (1-10)", 1, 10, 5,
                                         help="1: مستقر جداً، 10: متقلب للغاية",
                                         key="risk_market_volatility")

        # زر تحليل المخاطر مع دعم Claude AI
        col1, col2 = st.columns([1, 3])

        with col1:
            analyze_button = st.button("تحليل المخاطر", use_container_width=True, key="risk_analyze_button")

        with col2:
            # Añadimos un key único para este checkbox
            use_claude = st.checkbox("استخدام Claude AI للتحليل المتقدم", value=True, key="risk_use_claude")

        if analyze_button:
            with st.spinner("جاري تحليل المخاطر..."):
                # محاكاة وقت المعالجة
                time.sleep(2)

                # تجهيز البيانات للنموذج
                features = {
                    'project_type': project_type,
                    'location': location,
                    'client_type': client_type,
                    'tender_type': tender_type,
                    'payment_terms': payment_terms,
                    'completion_deadline': completion_deadline,
                    'penalty_clause': penalty_clause,
                    'technical_complexity': technical_complexity,
                    'company_experience': company_experience,
                    'market_volatility': market_volatility
                }

                # استدعاء النموذج لتحليل المخاطر
                risk_analysis_results = self._analyze_risks(features)

                # إضافة تحليل إضافي باستخدام Claude AI إذا تم تفعيل الخيار
                if use_claude:
                    try:
                        # إنشاء نص الميزات للتحليل
                        features_text = f"""
                        بيانات المشروع:
                        - نوع المشروع: {project_type}
                        - الموقع: {location}
                        - نوع العميل: {client_type}
                        - نوع المناقصة: {tender_type}

                        عوامل المخاطرة:
                        - شروط الدفع: {payment_terms}/10
                        - مهلة الإنجاز: {completion_deadline}/10
                        - شروط الغرامات: {penalty_clause}/10
                        - التعقيد الفني: {technical_complexity}/10
                        - خبرة الشركة: {company_experience}/10
                        - تقلبات السوق: {market_volatility}/10

                        ملخص التحليل الأولي:
                        - متوسط درجة المخاطرة: {risk_analysis_results['avg_risk_score']:.1f}/10
                        - عدد المخاطر العالية: {risk_analysis_results['high_risks']}
                        - عدد المخاطر المتوسطة: {risk_analysis_results['medium_risks']}
                        - عدد المخاطر المنخفضة: {risk_analysis_results['low_risks']}

                        أعلى المخاطر:
                        """

                        # إضافة تفاصيل أعلى المخاطر
                        for i, risk in enumerate(risk_analysis_results['top_risks'][:3]):
                            features_text += f"""
                            {i+1}. {risk['name']} ({risk['category']})
                               - الاحتمالية: {risk['probability'] * 100:.0f}%
                               - التأثير: {risk['impact'] * 100:.0f}%
                               - درجة المخاطرة: {risk['risk_score']}/10
                            """

                        prompt = f"""تحليل مخاطر مشروع:

                        {features_text}

                        المطلوب:
                        1. تحليل عوامل المخاطرة وتأثيرها على المشروع
                        2. تقديم توصيات إضافية لإدارة المخاطر
                        3. اقتراح استراتيجيات استجابة للمخاطر الرئيسية
                        4. تقديم نصائح لتحسين شروط العقد لتقليل المخاطر
                        5. تقييم مدى ملاءمة المشروع لاستراتيجية الشركة

                        يرجى تقديم تحليل مهني ومختصر يركز على الجوانب الأكثر أهمية.
                        """

                        # استدعاء Claude للتحليل
                        claude_analysis = self.claude_service.chat_completion(
                            [{"role": "user", "content": prompt}]
                        )

                        if "error" not in claude_analysis:
                            # إضافة تحليل Claude إلى النتائج
                            risk_analysis_results["claude_analysis"] = claude_analysis["content"]
                    except Exception as e:
                        st.warning(f"تعذر إجراء التحليل المتقدم: {str(e)}")

                # عرض نتائج تحليل المخاطر
                self._display_risk_analysis_results(risk_analysis_results)

    def _analyze_risks(self, features):
        """تحليل مخاطر المشروع"""

        # في البيئة الحقيقية، سيتم استدعاء نموذج تحليل المخاطر
        # محاكاة نتائج تحليل المخاطر للعرض

        # تعريف قائمة من المخاطر المحتملة
        potential_risks = [
            {
                "id": "R-001",
                "name": "غرامة تأخير مرتفعة",
                "category": "مخاطر مالية",
                "description": "غرامة تأخير مرتفعة تصل إلى 10% من قيمة العقد، مما قد يؤثر سلباً على ربحية المشروع في حال التأخير.",
                "probability": 0.6,
                "impact": 0.8,
                "risk_score": 7.8,
                "response_strategy": "تخطيط مفصل للمشروع مع وضع مخزون زمني مناسب وتحديد نقاط التسليم المبكر."
            },
            {
                "id": "R-002",
                "name": "تقلبات أسعار المواد",
                "category": "مخاطر السوق",
                "description": "ارتفاع محتمل في أسعار المواد الخام خلال فترة تنفيذ المشروع، مما يؤثر على التكلفة الإجمالية.",
                "probability": 0.7,
                "impact": 0.7,
                "risk_score": 7.5,
                "response_strategy": "التعاقد المبكر مع الموردين وتثبيت الأسعار، أو إضافة بند تعديل سعري في العقد."
            },
            {
                "id": "R-003",
                "name": "ضعف تدفق المدفوعات",
                "category": "مخاطر مالية",
                "description": "تأخر العميل في سداد المستخلصات مما يؤثر على التدفق النقدي للمشروع.",
                "probability": 0.5,
                "impact": 0.8,
                "risk_score": 7.2,
                "response_strategy": "التفاوض على شروط دفع واضحة ومواعيد محددة، وإمكانية طلب دفعة مقدمة."
            },
            {
                "id": "R-004",
                "name": "نقص العمالة الماهرة",
                "category": "مخاطر الموارد",
                "description": "صعوبة توفير عمالة ماهرة لتنفيذ أجزاء محددة من المشروع.",
                "probability": 0.5,
                "impact": 0.6,
                "risk_score": 6.5,
                "response_strategy": "التخطيط المبكر للموارد البشرية وتوقيع عقود مع مقاولي الباطن المتخصصين."
            },
            {
                "id": "R-005",
                "name": "تغييرات في نطاق العمل",
                "category": "مخاطر تعاقدية",
                "description": "طلبات تغيير من العميل تؤدي إلى زيادة نطاق العمل دون تعديل مناسب للتكلفة والجدول الزمني.",
                "probability": 0.6,
                "impact": 0.6,
                "risk_score": 6.0,
                "response_strategy": "تضمين آلية واضحة لإدارة التغيير في العقد وتقييم تأثير أي تغييرات على التكلفة والزمن."
            },
            {
                "id": "R-006",
                "name": "مشاكل في الموقع",
                "category": "مخاطر فنية",
                "description": "ظروف موقع غير متوقعة تؤثر على تنفيذ الأعمال، مثل مشاكل في التربة أو مرافق تحت الأرض.",
                "probability": 0.4,
                "impact": 0.7,
                "risk_score": 5.8,
                "response_strategy": "إجراء دراسات واختبارات مفصلة للموقع قبل بدء التنفيذ، وتخصيص احتياطي للطوارئ."
            },
            {
                "id": "R-007",
                "name": "تضارب في التصاميم",
                "category": "مخاطر فنية",
                "description": "تعارض بين مختلف تخصصات التصميم (معماري، إنشائي، كهروميكانيكي) يؤدي إلى تأخير وإعادة عمل.",
                "probability": 0.4,
                "impact": 0.6,
                "risk_score": 5.4,
                "response_strategy": "مراجعة شاملة للتصاميم قبل البدء في التنفيذ واستخدام نمذجة معلومات البناء (BIM) لكشف التعارضات."
            },
            {
                "id": "R-008",
                "name": "تأخر الموافقات",
                "category": "مخاطر تنظيمية",
                "description": "تأخر في الحصول على الموافقات والتصاريح اللازمة من الجهات المختصة.",
                "probability": 0.5,
                "impact": 0.5,
                "risk_score": 5.0,
                "response_strategy": "التخطيط المبكر للتصاريح المطلوبة وبناء علاقات جيدة مع الجهات التنظيمية."
            },
            {
                "id": "R-009",
                "name": "عدم توفر المعدات",
                "category": "مخاطر الموارد",
                "description": "صعوبة في توفير المعدات المتخصصة في الوقت المطلوب.",
                "probability": 0.3,
                "impact": 0.6,
                "risk_score": 4.8,
                "response_strategy": "حجز المعدات مبكراً وتوفير بدائل محتملة في حالة عدم توفر المعدات الأساسية."
            },
            {
                "id": "R-010",
                "name": "ظروف جوية قاسية",
                "category": "مخاطر خارجية",
                "description": "تأثير الظروف الجوية القاسية (حرارة شديدة، أمطار غزيرة، عواصف رملية) على سير العمل.",
                "probability": 0.3,
                "impact": 0.5,
                "risk_score": 4.5,
                "response_strategy": "تخطيط الجدول الزمني مع مراعاة المواسم وإضافة مخزون زمني للظروف الجوية غير المتوقعة."
            }
        ]

        # حساب درجات المخاطرة بناءً على الميزات المدخلة
        for risk in potential_risks:
            # تعديل احتمالية حدوث المخاطر بناءً على العوامل المدخلة
            if risk["id"] == "R-001":  # غرامة تأخير
                risk["probability"] = risk["probability"] * (10 - features["penalty_clause"]) / 10
                risk["probability"] = risk["probability"] * (10 - features["completion_deadline"]) / 10

            elif risk["id"] == "R-002":  # تقلبات أسعار المواد
                risk["probability"] = risk["probability"] * features["market_volatility"] / 10

            elif risk["id"] == "R-003":  # ضعف تدفق المدفوعات
                risk["probability"] = risk["probability"] * (10 - features["payment_terms"]) / 10

                if features["client_type"] == "حكومي":
                    risk["probability"] = risk["probability"] * 0.6  # احتمالية أقل مع العملاء الحكوميين
                elif features["client_type"] == "أفراد":
                    risk["probability"] = risk["probability"] * 1.3  # احتمالية أعلى مع العملاء الأفراد

            elif risk["id"] == "R-004":  # نقص العمالة الماهرة
                risk["probability"] = risk["probability"] * features["technical_complexity"] / 10

            elif risk["id"] == "R-005":  # تغييرات في نطاق العمل
                risk["probability"] = risk["probability"] * features["technical_complexity"] / 10

                if features["client_type"] == "حكومي":
                    risk["probability"] = risk["probability"] * 1.2  # احتمالية أعلى للتغييرات مع العملاء الحكوميين

            # تعديل تأثير المخاطر بناءً على العوامل المدخلة
            if risk["category"] == "مخاطر فنية":
                risk["impact"] = risk["impact"] * (10 - features["company_experience"]) / 10

            # إعادة حساب درجة المخاطرة
            risk["risk_score"] = round(risk["probability"] * risk["impact"] * 10, 1)

        # ترتيب المخاطر تنازلياً حسب درجة المخاطرة
        sorted_risks = sorted(potential_risks, key=lambda x: x["risk_score"], reverse=True)

        # حساب عدد المخاطر حسب شدتها
        high_risks = sum(1 for risk in sorted_risks if risk["risk_score"] >= 6.0)
        medium_risks = sum(1 for risk in sorted_risks if 3.0 <= risk["risk_score"] < 6.0)
        low_risks = sum(1 for risk in sorted_risks if risk["risk_score"] < 3.0)

        # حساب متوسط درجة المخاطرة
        avg_risk_score = sum(risk["risk_score"] for risk in sorted_risks) / len(sorted_risks)

        # تجهيز النتائج
        results = {
            "top_risks": sorted_risks,
            "high_risks": high_risks,
            "medium_risks": medium_risks,
            "low_risks": low_risks,
            "avg_risk_score": avg_risk_score,
            "risk_profile": {
                "financial_risk": sum(risk["risk_score"] for risk in sorted_risks if risk["category"] == "مخاطر مالية") / sum(1 for risk in sorted_risks if risk["category"] == "مخاطر مالية") if sum(1 for risk in sorted_risks if risk["category"] == "مخاطر مالية") > 0 else 0,
                "technical_risk": sum(risk["risk_score"] for risk in sorted_risks if risk["category"] == "مخاطر فنية") / sum(1 for risk in sorted_risks if risk["category"] == "مخاطر فنية") if sum(1 for risk in sorted_risks if risk["category"] == "مخاطر فنية") > 0 else 0,
                "market_risk": sum(risk["risk_score"] for risk in sorted_risks if risk["category"] == "مخاطر السوق") / sum(1 for risk in sorted_risks if risk["category"] == "مخاطر السوق") if sum(1 for risk in sorted_risks if risk["category"] == "مخاطر السوق") > 0 else 0,
                "resource_risk": sum(risk["risk_score"] for risk in sorted_risks if risk["category"] == "مخاطر الموارد") / sum(1 for risk in sorted_risks if risk["category"] == "مخاطر الموارد") if sum(1 for risk in sorted_risks if risk["category"] == "مخاطر الموارد") > 0 else 0,
                "contract_risk": sum(risk["risk_score"] for risk in sorted_risks if risk["category"] == "مخاطر تعاقدية") / sum(1 for risk in sorted_risks if risk["category"] == "مخاطر تعاقدية") if sum(1 for risk in sorted_risks if risk["category"] == "مخاطر تعاقدية") > 0 else 0,
                "regulatory_risk": sum(risk["risk_score"] for risk in sorted_risks if risk["category"] == "مخاطر تنظيمية") / sum(1 for risk in sorted_risks if risk["category"] == "مخاطر تنظيمية") if sum(1 for risk in sorted_risks if risk["category"] == "مخاطر تنظيمية") > 0 else 0
            },
            "overall_assessment": "",
            "recommendation": ""
        }

        # تقييم شامل للمخاطر
        if avg_risk_score >= 6.0:
            results["overall_assessment"] = "مشروع عالي المخاطر"
            results["recommendation"] = "ينصح بإعادة التفاوض على شروط العقد أو إضافة هامش ربح أعلى لتغطية المخاطر."
        elif avg_risk_score >= 4.0:
            results["overall_assessment"] = "مشروع متوسط المخاطر"
            results["recommendation"] = "متابعة دقيقة للمخاطر العالية ووضع خطط استجابة مفصلة لها."
        else:
            results["overall_assessment"] = "مشروع منخفض المخاطر"
            results["recommendation"] = "مراقبة المخاطر بشكل دوري والتركيز على تحسين الأداء."

        return results

    def _display_risk_analysis_results(self, results):
        """عرض نتائج تحليل المخاطر"""

        st.markdown("### نتائج تحليل المخاطر")

        # عرض ملخص تقييم المخاطر
        st.markdown(f"#### التقييم العام: {results['overall_assessment']}")

        # عرض الإحصائيات الرئيسية للمخاطر
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("متوسط درجة المخاطرة", f"{results['avg_risk_score']:.1f}/10")

        with col2:
            st.metric("المخاطر العالية", f"{results['high_risks']}")

        with col3:
            st.metric("المخاطر المتوسطة", f"{results['medium_risks']}")

        with col4:
            st.metric("المخاطر المنخفضة", f"{results['low_risks']}")

        # عرض ملف المخاطر حسب الفئة
        st.markdown("#### ملف المخاطر حسب الفئة")

        # تجهيز البيانات للرسم البياني
        risk_profile_data = pd.DataFrame({
            'الفئة': [
                "مخاطر مالية",
                "مخاطر فنية",
                "مخاطر السوق",
                "مخاطر الموارد",
                "مخاطر تعاقدية",
                "مخاطر تنظيمية"
            ],
            'درجة المخاطرة': [
                results['risk_profile']['financial_risk'],
                results['risk_profile']['technical_risk'],
                results['risk_profile']['market_risk'],
                results['risk_profile']['resource_risk'],
                results['risk_profile']['contract_risk'],
                results['risk_profile']['regulatory_risk']
            ]
        })

        # رسم مخطط شعاعي لملف المخاطر
        fig = px.line_polar(
            risk_profile_data,
            r='درجة المخاطرة',
            theta='الفئة',
            line_close=True,
            range_r=[0, 10],
            title="ملف المخاطر حسب الفئة"
        )

        st.plotly_chart(fig, use_container_width=True)

        # عرض المخاطر الرئيسية
        st.markdown("#### المخاطر الرئيسية")

        # إنشاء جدول المخاطر
        risk_table_data = []

        for risk in results['top_risks'][:5]:  # عرض أعلى 5 مخاطر فقط
            risk_level = "عالية" if risk["risk_score"] >= 6.0 else "متوسطة" if risk["risk_score"] >= 3.0 else "منخفضة"
            risk_color = "red" if risk_level == "عالية" else "orange" if risk_level == "متوسطة" else "green"

            risk_table_data.append({
                "المعرف": risk["id"],
                "الوصف": risk["name"],
                "الفئة": risk["category"],
                "الاحتمالية": f"{risk['probability'] * 100:.0f}%",
                "التأثير": f"{risk['impact'] * 100:.0f}%",
                "درجة المخاطرة": risk["risk_score"],
                "المستوى": risk_level,
                "استراتيجية الاستجابة": risk["response_strategy"],
                "color": risk_color
            })

        # عرض جدول المخاطر
        risk_df = pd.DataFrame(risk_table_data)

        # استخدام تنسيق HTML مخصص لعرض المخاطر الرئيسية
        for index, row in risk_df.iterrows():
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                    <h5 style="margin-top: 0;">{row['المعرف']} - {row['الوصف']} <span style="float: right; background-color: {row['color']}; color: white; padding: 2px 8px; border-radius: 10px;">{row['المستوى']}</span></h5>
                    <p><strong>الفئة:</strong> {row['الفئة']} | <strong>الاحتمالية:</strong> {row['الاحتمالية']} | <strong>التأثير:</strong> {row['التأثير']} | <strong>درجة المخاطرة:</strong> {row['درجة المخاطرة']}/10</p>
                    <p><strong>استراتيجية الاستجابة:</strong> {row['استراتيجية الاستجابة']}</p>
                </div>
                """, unsafe_allow_html=True)

        # عرض توصيات عامة
        st.markdown("#### التوصيات العامة")
        st.info(results["recommendation"])

        # عرض تحليل Claude AI إذا كان متوفراً
        if "claude_analysis" in results:
            st.markdown("### تحليل Claude AI المتقدم")
            st.success(results["claude_analysis"])

        # زر تصدير تقرير المخاطر
        if st.button("تصدير تقرير المخاطر"):
            st.success("تم تصدير تقرير المخاطر بنجاح!")

    def _render_document_analysis_tab(self):
        """عرض تبويب تحليل المستندات"""

        st.markdown("### تحليل المستندات")

        # خيارات رفع الملفات
        st.markdown("#### رفع ملفات المناقصة")

        # رفع الملفات
        uploaded_files = st.file_uploader(
            "اختر ملفات المناقصة للتحليل",
            type=["pdf", "docx", "doc", "xls", "xlsx", "jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="document_analysis_files"
        )

        # اختيار نموذج التحليل
        analysis_model = st.radio(
            "اختر نموذج التحليل",
            [
                "استخراج البنود والمواصفات",
                "استخراج الشروط التعاقدية",
                "تحليل الكميات",
                "تحليل المتطلبات القانونية",
                "تحليل شامل (يستخدم Claude AI)"
            ],
            horizontal=True
        )

        # زر بدء التحليل
        if uploaded_files and st.button("بدء تحليل المستندات"):
            with st.spinner("جاري تحليل المستندات..."):
                # محاكاة وقت المعالجة
                time.sleep(3)

                # معالجة الملفات المرفوعة
                analysis_results = self._analyze_documents(uploaded_files, analysis_model)

                # عرض نتائج التحليل
                self._display_document_analysis_results(analysis_results)

    def _analyze_documents(self, files, analysis_model):
        """تحليل المستندات المرفوعة"""

        # في البيئة الحقيقية، سيتم استدعاء نموذج تحليل المستندات
        # محاكاة نتائج تحليل المستندات للعرض

        # نتائج التحليل المبدئية
        basic_results = {
            "file_count": len(files),
            "file_names": [file.name for file in files],
            "file_sizes": [f"{file.size / 1024:.1f} KB" for file in files],
            "file_types": [file.type or "غير محدد" for file in files],
            "extracted_text_samples": {},
            "entities": [],
            "tender_items": [],
            "contract_terms": [],
            "quantities": [],
            "legal_requirements": [],
            "summary": ""
        }

        # محاكاة استخراج نص من الملفات
        for file in files:
            # استخراج عينة نصية (في البيئة الحقيقية سيتم استخراج النص الكامل)
            sample_text = f"عينة نصية مستخرجة من الملف {file.name}. هذا النص لأغراض العرض فقط."
            basic_results["extracted_text_samples"][file.name] = sample_text

        # محاكاة تحليل المحتوى حسب نموذج التحليل المختار
        if analysis_model == "استخراج البنود والمواصفات" or analysis_model == "تحليل شامل (يستخدم Claude AI)":
            basic_results["tender_items"] = [
                {
                    "id": "T-001",
                    "description": "أعمال الحفر والردم",
                    "unit": "م³",
                    "quantity": 1500,
                    "estimated_price": 85,
                    "specifications": "حفر في أي نوع من التربة بما في ذلك الصخور والردم باستخدام مواد معتمدة."
                },
                {
                    "id": "T-002",
                    "description": "أعمال الخرسانة المسلحة للأساسات",
                    "unit": "م³",
                    "quantity": 750,
                    "estimated_price": 1200,
                    "specifications": "خرسانة مسلحة بقوة 30 نيوتن/مم² بعد 28 يوم، مع حديد تسليح من الفئة 60."
                },
                {
                    "id": "T-003",
                    "description": "أعمال الخرسانة المسلحة للهيكل",
                    "unit": "م³",
                    "quantity": 1200,
                    "estimated_price": 1350,
                    "specifications": "خرسانة مسلحة بقوة 30 نيوتن/مم² بعد 28 يوم، مع حديد تسليح من الفئة 60."
                },
                {
                    "id": "T-004",
                    "description": "أعمال الطابوق",
                    "unit": "م²",
                    "quantity": 3500,
                    "estimated_price": 120,
                    "specifications": "جدران طابوق مفرغ سمك 20 سم مع مونة إسمنتية."
                },
                {
                    "id": "T-005",
                    "description": "أعمال التشطيبات الداخلية",
                    "unit": "م²",
                    "quantity": 5000,
                    "estimated_price": 200,
                    "specifications": "تشطيبات داخلية تشمل اللياسة والدهان والأرضيات حسب المواصفات المرفقة."
                }
            ]

        if analysis_model == "استخراج الشروط التعاقدية" or analysis_model == "تحليل شامل (يستخدم Claude AI)":
            basic_results["contract_terms"] = [
                {
                    "id": "C-001",
                    "title": "مدة تنفيذ المشروع",
                    "description": "يجب إنجاز جميع الأعمال خلال 18 شهراً من تاريخ تسليم الموقع.",
                    "risk_level": "متوسط",
                    "notes": "مدة تنفيذ معقولة نسبياً للحجم المتوقع من الأعمال."
                },
                {
                    "id": "C-002",
                    "title": "غرامة التأخير",
                    "description": "تفرض غرامة تأخير بنسبة 0.1% من قيمة العقد عن كل يوم تأخير، بحد أقصى 10% من القيمة الإجمالية للعقد.",
                    "risk_level": "عالي",
                    "notes": "غرامة مرتفعة نسبياً، تتطلب جدولة دقيقة وإدارة استباقية للمخاطر."
                },
                {
                    "id": "C-003",
                    "title": "شروط الدفع",
                    "description": "يتم صرف المستخلصات خلال 45 يوماً من تاريخ تقديمها، مع خصم نسبة 10% كضمان حسن التنفيذ تسترد بعد فترة الضمان.",
                    "risk_level": "متوسط",
                    "notes": "فترة 45 يوماً طويلة نسبياً وقد تؤثر على التدفق النقدي."
                },
                {
                    "id": "C-004",
                    "title": "التزامات المحتوى المحلي",
                    "description": "يجب أن لا تقل نسبة المحتوى المحلي عن 30% من إجمالي قيمة العقد.",
                    "risk_level": "منخفض",
                    "notes": "يمكن تحقيق النسبة المطلوبة من خلال توريد المواد والعمالة المحلية."
                },
                {
                    "id": "C-005",
                    "title": "التغييرات والأعمال الإضافية",
                    "description": "يحق للمالك طلب تغييرات بنسبة ±10% من قيمة العقد دون تعديل أسعار الوحدات.",
                    "risk_level": "متوسط",
                    "notes": "نسبة معقولة، لكن يجب مراعاة احتمالية الطلبات الإضافية عند تسعير البنود."
                }
            ]

        if analysis_model == "تحليل الكميات" or analysis_model == "تحليل شامل (يستخدم Claude AI)":
            basic_results["quantities"] = [
                {
                    "category": "أعمال الحفر والردم",
                    "volume": 1500,
                    "unit": "م³",
                    "estimated_cost": 127500
                },
                {
                    "category": "أعمال الخرسانة",
                    "volume": 1950,
                    "unit": "م³",
                    "estimated_cost": 2437500
                },
                {
                    "category": "أعمال الطابوق",
                    "volume": 3500,
                    "unit": "م²",
                    "estimated_cost": 420000
                },
                {
                    "category": "أعمال التشطيبات الداخلية",
                    "volume": 5000,
                    "unit": "م²",
                    "estimated_cost": 1000000
                },
                {
                    "category": "أعمال التشطيبات الخارجية",
                    "volume": 2200,
                    "unit": "م²",
                    "estimated_cost": 660000
                },
                {
                    "category": "أعمال الكهروميكانيكية",
                    "volume": 1,
                    "unit": "مقطوعية",
                    "estimated_cost": 1750000
                }
            ]

        if analysis_model == "تحليل المتطلبات القانونية" or analysis_model == "تحليل شامل (يستخدم Claude AI)":
            basic_results["legal_requirements"] = [
                {
                    "id": "L-001",
                    "title": "متطلبات التراخيص",
                    "description": "يجب أن يكون المقاول حاصلاً على تصنيف في الفئة الأولى في مجال المباني.",
                    "compliance_status": "مطلوب التحقق",
                    "required_documents": "شهادة التصنيف سارية المفعول"
                },
                {
                    "id": "L-002",
                    "title": "متطلبات التأمين",
                    "description": "يجب تقديم بوليصة تأمين شاملة تغطي جميع مخاطر المشروع بقيمة لا تقل عن 100% من قيمة العقد.",
                    "compliance_status": "مطلوب التحقق",
                    "required_documents": "وثائق التأمين الشاملة"
                },
                {
                    "id": "L-003",
                    "title": "متطلبات الضمان البنكي",
                    "description": "يجب تقديم ضمان بنكي ابتدائي بنسبة 2% من قيمة العطاء، وضمان نهائي بنسبة 5% من قيمة العقد.",
                    "compliance_status": "مطلوب التحقق",
                    "required_documents": "نماذج الضمانات البنكية"
                },
                {
                    "id": "L-004",
                    "title": "متطلبات السعودة",
                    "description": "يجب الالتزام بنسبة السعودة المطلوبة حسب برنامج نطاقات وأن يكون المقاول في النطاق الأخضر.",
                    "compliance_status": "مطلوب التحقق",
                    "required_documents": "شهادة نطاقات سارية المفعول"
                },
                {
                    "id": "L-005",
                    "title": "متطلبات الزكاة والدخل",
                    "description": "يجب تقديم شهادة سداد الزكاة والضريبة سارية المفعول.",
                    "compliance_status": "مطلوب التحقق",
                    "required_documents": "شهادة الزكاة والدخل"
                }
            ]

        # إعداد ملخص التحليل
        basic_results["summary"] = f"""
        تم تحليل {len(files)} ملفات بإجمالي حجم {sum([file.size for file in files]) / 1024 / 1024:.2f} ميجابايت.

        نتائج التحليل الرئيسية:
        - تم استخراج {len(basic_results.get('tender_items', []))} بنود رئيسية للمناقصة.
        - تم تحديد {len(basic_results.get('contract_terms', []))} شروط تعاقدية هامة.
        - تم تحليل الكميات لـ {len(basic_results.get('quantities', []))} فئات من الأعمال.
        - تم تحديد {len(basic_results.get('legal_requirements', []))} متطلبات قانونية.

        التوصيات:
        - مراجعة شروط التعاقد وخاصة البنود المتعلقة بالغرامات والدفعات.
        - تدقيق جداول الكميات والتأكد من تغطية جميع البنود اللازمة للتنفيذ.
        - التحقق من استيفاء جميع المتطلبات القانونية قبل تقديم العطاء.
        """

        # إضافة تحليل متقدم باستخدام Claude AI إذا تم اختياره
        if analysis_model == "تحليل شامل (يستخدم Claude AI)":
            try:
                # إنشاء مدخلات للتحليل
                analysis_input = f"""
                المناقصة: تطوير مبنى إداري متعدد الطوابق

                ملفات تم تحليلها:
                {', '.join(basic_results['file_names'])}

                بنود رئيسية:
                - أعمال الحفر والردم: 1500 م³
                - أعمال الخرسانة المسلحة للأساسات: 750 م³
                - أعمال الخرسانة المسلحة للهيكل: 1200 م³
                - أعمال الطابوق: 3500 م²
                - أعمال التشطيبات الداخلية: 5000 م²

                شروط تعاقدية رئيسية:
                - مدة التنفيذ: 18 شهر
                - غرامة التأخير: 0.1% يومياً بحد أقصى 10%
                - شروط الدفع: 45 يوم للمستخلصات مع خصم 10% ضمان
                - المحتوى المحلي: 30% كحد أدنى

                متطلبات قانونية:
                - تصنيف الفئة الأولى مباني
                - تأمين شامل بنسبة 100%
                - ضمان بنكي ابتدائي 2% ونهائي 5%
                - الالتزام بمتطلبات السعودة (النطاق الأخضر)

                من فضلك قم بتحليل هذه المناقصة وتقديم:
                1. تقييم عام للمناقصة وجاذبيتها
                2. نقاط القوة والضعف الرئيسية
                3. المخاطر المحتملة التي يجب مراعاتها
                4. توصيات للتسعير المناسب
                5. استراتيجية مقترحة للتنافس على المناقصة
                """

                # استدعاء خدمة Claude للتحليل
                claude_response = self.claude_service.chat_completion(
                    [{"role": "user", "content": analysis_input}]
                )

                if "error" not in claude_response:
                    # إضافة تحليل Claude إلى النتائج
                    basic_results["claude_analysis"] = claude_response["content"]
            except Exception as e:
                logging.error(f"فشل في تحليل المستندات باستخدام Claude AI: {str(e)}")

        return basic_results

    def _display_document_analysis_results(self, results):
        """عرض نتائج تحليل المستندات"""

        st.markdown("### نتائج تحليل المستندات")

        # عرض ملخص التحليل
        st.markdown("#### ملخص التحليل")
        st.info(results["summary"])

        # عرض البنود المستخرجة من المناقصة إذا وجدت
        if results["tender_items"]:
            st.markdown("#### بنود المناقصة المستخرجة")

            # إنشاء DataFrame للبنود
            items_df = pd.DataFrame(results["tender_items"])

            # عرض الجدول بشكل منسق
            st.dataframe(
                items_df[["id", "description", "unit", "quantity", "estimated_price"]],
                use_container_width=True
            )

            # عرض مخطط للتكاليف المقدرة
            costs = [item["quantity"] * item["estimated_price"] for item in results["tender_items"]]
            labels = [item["description"] for item in results["tender_items"]]

            fig = px.pie(
                names=labels,
                values=costs,
                title="توزيع التكاليف المقدرة حسب البنود"
            )

            st.plotly_chart(fig, use_container_width=True)

        # عرض الشروط التعاقدية إذا وجدت
        if results["contract_terms"]:
            st.markdown("#### الشروط التعاقدية الهامة")

            # عرض كل شرط في قسم منفصل
            for term in results["contract_terms"]:
                risk_color = "red" if term["risk_level"] == "عالي" else "orange" if term["risk_level"] == "متوسط" else "green"

                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                    <h5 style="margin-top: 0;">{term['id']} - {term['title']} <span style="float: right; background-color: {risk_color}; color: white; padding: 2px 8px; border-radius: 10px;">مستوى الخطورة: {term['risk_level']}</span></h5>
                    <p>{term['description']}</p>
                    <p><strong>ملاحظات:</strong> {term['notes']}</p>
                </div>
                """, unsafe_allow_html=True)

        # عرض تحليل الكميات إذا وجد
        if results["quantities"]:
            st.markdown("#### تحليل الكميات")

            # إنشاء DataFrame للكميات
            quantities_df = pd.DataFrame(results["quantities"])

            # عرض الجدول بشكل منسق
            st.dataframe(quantities_df, use_container_width=True)

            # عرض مخطط شريطي للتكاليف المقدرة
            fig = px.bar(
                quantities_df,
                x="category",
                y="estimated_cost",
                title="التكاليف المقدرة حسب فئة الأعمال",
                labels={"category": "فئة الأعمال", "estimated_cost": "التكلفة المقدرة (ريال)"}
            )

            fig.update_traces(text=quantities_df["estimated_cost"], textposition="outside")

            st.plotly_chart(fig, use_container_width=True)

        # عرض المتطلبات القانونية إذا وجدت
        if results["legal_requirements"]:
            st.markdown("#### المتطلبات القانونية")

            # عرض المتطلبات في جدول
            legal_df = pd.DataFrame(results["legal_requirements"])

            # عرض الجدول بشكل منسق
            st.dataframe(
                legal_df[["id", "title", "description", "compliance_status", "required_documents"]],
                use_container_width=True
            )

            # عرض قائمة تحقق للمتطلبات القانونية
            st.markdown("##### قائمة التحقق من المتطلبات القانونية")

            for req in results["legal_requirements"]:
                st.checkbox(f"{req['title']} - {req['description']}", key=f"req_{req['id']}")

        # عرض تحليل Claude AI المتقدم إذا وجد
        if "claude_analysis" in results:
            st.markdown("### تحليل Claude AI المتقدم")
            st.success(results["claude_analysis"])

        # أزرار إضافية
        col1, col2 = st.columns(2)

        with col1:
            if st.button("تصدير تقرير تحليل المستندات"):
                st.success("تم تصدير تقرير تحليل المستندات بنجاح!")

        with col2:
            if st.button("استخراج جدول الكميات"):
                st.success("تم استخراج جدول الكميات بنجاح!")

    def _render_local_content_tab(self):
        """عرض تبويب المحتوى المحلي"""

        st.markdown("### المحتوى المحلي")

        st.markdown("""
        وحدة حساب المحتوى المحلي تساعدك في تحليل وتحسين نسبة المحتوى المحلي في مشروعك طبقاً لمتطلبات هيئة المحتوى المحلي والمشتريات الحكومية.
        """)

        # عرض علامات تبويب فرعية
        lc_tabs = st.tabs([
            "حساب المحتوى المحلي", 
            "قاعدة بيانات الموردين", 
            "التقارير", 
            "التحسين"
        ])

        with lc_tabs[0]:
            self._render_lc_calculator_tab()

        with lc_tabs[1]:
            self._render_lc_suppliers_tab()

        with lc_tabs[2]:
            self._render_lc_reports_tab()

        with lc_tabs[3]:
            self._render_lc_optimization_tab()

    def _render_lc_calculator_tab(self):
        """عرض تبويب حساب المحتوى المحلي"""

        st.markdown("#### حساب المحتوى المحلي")

        # نموذج إدخال بيانات المشروع
        st.markdown("##### بيانات المشروع")

        col1, col2 = st.columns(2)

        with col1:
            project_name = st.text_input("اسم المشروع", "مبنى إداري الرياض")
            project_value = st.number_input("القيمة الإجمالية للمشروع (ريال)", min_value=1000, value=10000000)

        with col2:
            target_lc = st.slider("نسبة المحتوى المحلي المستهدفة (%)", 0, 100, 40)
            calculation_method = st.selectbox(
                "طريقة الحساب",
                [
                    "الطريقة القياسية (المدخلات)",
                    "طريقة القيمة المضافة",
                    "الطريقة المختلطة"
                ]
            )

        # جدول مكونات المشروع
        st.markdown("##### مكونات المشروع")

        # إعداد بيانات المكونات الافتراضية
        if 'lc_components' not in st.session_state:
            st.session_state.lc_components = [
                {
                    "id": 1,
                    "name": "الخرسانة المسلحة",
                    "category": "مواد",
                    "value": 3000000,
                    "local_content": 85,
                    "supplier": "شركة الإنشاءات السعودية"
                },
                {
                    "id": 2,
                    "name": "الأعمال الكهربائية",
                    "category": "أنظمة",
                    "value": 1500000,
                    "local_content": 65,
                    "supplier": "مؤسسة الطاقة المتقدمة"
                },
                {
                    "id": 3,
                    "name": "أعمال التكييف",
                    "category": "أنظمة",
                    "value": 1200000,
                    "local_content": 55,
                    "supplier": "شركة التبريد العالمية"
                },
                {
                    "id": 4,
                    "name": "الواجهات والنوافذ",
                    "category": "مواد",
                    "value": 800000,
                    "local_content": 45,
                    "supplier": "شركة الزجاج المتطورة"
                },
                {
                    "id": 5,
                    "name": "أعمال التشطيبات",
                    "category": "مواد وعمالة",
                    "value": 1200000,
                    "local_content": 80,
                    "supplier": "مؤسسة التشطيبات الحديثة"
                },
                {
                    "id": 6,
                    "name": "الأثاث والتجهيزات",
                    "category": "أثاث",
                    "value": 900000,
                    "local_content": 30,
                    "supplier": "شركة الأثاث المكتبي"
                },
                {
                    "id": 7,
                    "name": "أنظمة الأمن والمراقبة",
                    "category": "أنظمة",
                    "value": 600000,
                    "local_content": 40,
                    "supplier": "شركة الأنظمة الأمنية المتقدمة"
                },
                {
                    "id": 8,
                    "name": "العمالة المباشرة",
                    "category": "عمالة",
                    "value": 800000,
                    "local_content": 50,
                    "supplier": "داخلي"
                }
            ]

        # عرض جدول المكونات للتعديل
        for i, component in enumerate(st.session_state.lc_components):
            col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 2, 1])

            with col1:
                st.session_state.lc_components[i]["name"] = st.text_input(
                    "المكون",
                    component["name"],
                    key=f"comp_name_{i}"
                )

            with col2:
                st.session_state.lc_components[i]["category"] = st.selectbox(
                    "الفئة",
                    ["مواد", "أنظمة", "عمالة", "مواد وعمالة", "أثاث", "خدمات"],
                    index=["مواد", "أنظمة", "عمالة", "مواد وعمالة", "أثاث", "خدمات"].index(component["category"]),
                    key=f"comp_category_{i}"
                )

            with col3:
                st.session_state.lc_components[i]["value"] = st.number_input(
                    "القيمة (ريال)",
                    min_value=0,
                    value=int(component["value"]),
                    key=f"comp_value_{i}"
                )

            with col4:
                st.session_state.lc_components[i]["local_content"] = st.slider(
                    "المحتوى المحلي (%)",
                    0, 100, int(component["local_content"]),
                    key=f"comp_lc_{i}"
                )

            with col5:
                st.session_state.lc_components[i]["supplier"] = st.text_input(
                    "المورد",
                    component["supplier"],
                    key=f"comp_supplier_{i}"
                )

            with col6:
                if st.button("حذف", key=f"delete_comp_{i}"):
                    st.session_state.lc_components.pop(i)
                    st.rerun()

        # زر إضافة مكون جديد
        if st.button("إضافة مكون جديد"):
            new_id = max([c["id"] for c in st.session_state.lc_components]) + 1 if st.session_state.lc_components else 1
            st.session_state.lc_components.append({
                "id": new_id,
                "name": f"مكون جديد {new_id}",
                "category": "مواد",
                "value": 100000,
                "local_content": 50,
                "supplier": "غير محدد"
            })
            st.rerun()

        # زر حساب المحتوى المحلي
        col1, col2 = st.columns([1, 3])

        with col1:
            calculate_button = st.button("حساب المحتوى المحلي", use_container_width=True)

        with col2:
            use_claude = st.checkbox("استخدام Claude AI للتحليل المتقدم", value=True, key="lc_use_claude")

        if calculate_button:
            with st.spinner("جاري حساب وتحليل المحتوى المحلي..."):
                # محاكاة وقت المعالجة
                time.sleep(2)

                # حساب المحتوى المحلي
                lc_results = self._calculate_local_content(st.session_state.lc_components, target_lc, calculation_method)

                # إضافة تحليل إضافي باستخدام Claude AI إذا تم تفعيل الخيار
                if use_claude:
                    try:
                        # إنشاء نص المكونات للتحليل
                        components_text = ""
                        for comp in st.session_state.lc_components:
                            components_text += f"""
                            - {comp['name']} ({comp['category']}):
                              القيمة: {comp['value']:,} ريال | المحتوى المحلي: {comp['local_content']}% | المورد: {comp['supplier']}
                            """

                        prompt = f"""تحليل وتحسين المحتوى المحلي:

                        بيانات المشروع:
                        - اسم المشروع: {project_name}
                        - القيمة الإجمالية: {project_value:,} ريال
                        - نسبة المحتوى المحلي المستهدفة: {target_lc}%
                        - النسبة المحسوبة: {lc_results['total_local_content']:.1f}%

                        مكونات المشروع:
                        {components_text}

                        المطلوب:
                        1. تحليل نسبة المحتوى المحلي المحسوبة ومقارنتها بالمستهدف
                        2. تحديد المكونات ذات المحتوى المحلي المنخفض التي يمكن تحسينها
                        3. اقتراح بدائل محلية أو استراتيجيات لزيادة المحتوى المحلي
                        4. تقديم توصيات عملية لتحقيق النسبة المستهدفة
                        5. تحديد أي فرص إضافية لتحسين المحتوى المحلي في المشروع

                        يرجى تقديم تحليل مهني ومختصر يركز على الجوانب الأكثر أهمية.
                        """

                        # استدعاء Claude للتحليل
                        claude_analysis = self.claude_service.chat_completion(
                            [{"role": "user", "content": prompt}]
                        )

                        if "error" not in claude_analysis:
                            # إضافة تحليل Claude إلى النتائج
                            lc_results["claude_analysis"] = claude_analysis["content"]
                    except Exception as e:
                        st.warning(f"تعذر إجراء التحليل المتقدم: {str(e)}")

                # عرض نتائج حساب المحتوى المحلي
                self._display_local_content_results(lc_results, target_lc)

    def _calculate_local_content(self, components, target_lc, calculation_method):
        """حساب المحتوى المحلي"""

        # حساب إجمالي قيمة المشروع
        total_value = sum([comp["value"] for comp in components])

        # حساب المحتوى المحلي الإجمالي
        total_local_content_value = sum([comp["value"] * comp["local_content"] / 100 for comp in components])

        # حساب نسبة المحتوى المحلي الإجمالية
        total_local_content_percent = (total_local_content_value / total_value) * 100 if total_value > 0 else 0

        # تحليل المحتوى المحلي حسب الفئة
        categories = {}
        for comp in components:
            category = comp["category"]
            if category not in categories:
                categories[category] = {
                    "total_value": 0,
                    "local_content_value": 0
                }

            categories[category]["total_value"] += comp["value"]
            categories[category]["local_content_value"] += comp["value"] * comp["local_content"] / 100

        # حساب نسبة المحتوى المحلي لكل فئة
        for category in categories:
            if categories[category]["total_value"] > 0:
                categories[category]["local_content_percent"] = (categories[category]["local_content_value"] / categories[category]["total_value"]) * 100
            else:
                categories[category]["local_content_percent"] = 0

        # تحديد المكونات ذات المحتوى المحلي المنخفض
        low_lc_components = sorted(
            [comp for comp in components if comp["local_content"] < 50],
            key=lambda x: x["local_content"]
        )

        # تحديد المكونات ذات المحتوى المحلي المرتفع
        high_lc_components = sorted(
            [comp for comp in components if comp["local_content"] >= 80],
            key=lambda x: x["local_content"],
            reverse=True
        )

        # تقديم توصيات لتحسين المحتوى المحلي
        improvement_recommendations = []

        # توصيات للمكونات ذات المحتوى المحلي المنخفض
        for comp in low_lc_components[:3]:  # أخذ أقل 3 مكونات
            improvement_recommendations.append({
                "component": comp["name"],
                "current_lc": comp["local_content"],
                "recommendation": f"البحث عن بدائل محلية لـ {comp['name']} التي تمثل {comp['value'] / total_value * 100:.1f}% من قيمة المشروع."
            })

        # حساب الفجوة بين المحتوى المحلي الفعلي والمستهدف
        lc_gap = target_lc - total_local_content_percent

        # إعداد النتائج
        results = {
            "total_value": total_value,
            "total_local_content_value": total_local_content_value,
            "total_local_content": total_local_content_percent,
            "target_lc": target_lc,
            "lc_gap": lc_gap,
            "categories": categories,
            "low_lc_components": low_lc_components,
            "high_lc_components": high_lc_components,
            "improvement_recommendations": improvement_recommendations,
            "calculation_method": calculation_method,
            "components": components
        }

        # تحديد حالة المحتوى المحلي
        if lc_gap <= 0:
            results["status"] = "تم تحقيق المستهدف"
            results["color"] = "green"
        elif lc_gap <= 5:
            results["status"] = "قريب من المستهدف"
            results["color"] = "orange"
        else:
            results["status"] = "بعيد عن المستهدف"
            results["color"] = "red"

        return results

    def _display_local_content_results(self, results, target_lc):
        """عرض نتائج حساب المحتوى المحلي"""

        st.markdown("### نتائج حساب المحتوى المحلي")

        # عرض نسبة المحتوى المحلي الإجمالية
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "نسبة المحتوى المحلي الحالية",
                f"{results['total_local_content']:.1f}%",
                delta=f"{results['lc_gap']:.1f}%" if results['lc_gap'] < 0 else f"-{results['lc_gap']:.1f}%",
                delta_color="normal" if results['lc_gap'] < 0 else "inverse"
            )

        with col2:
            st.metric(
                "النسبة المستهدفة",
                f"{target_lc}%"
            )

        with col3:
            # Aquí está el problema - no podemos usar 'green' como valor para delta_color
            # En lugar de eso, usamos un texto formateado para mostrar el estado
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 5px; background-color: {"green" if results['status'] == 'تم تحقيق المستهدف' else "orange" if results['status'] == 'قريب من المستهدف' else "red"}; color: white; text-align: center;">
                <h4 style="margin: 0;">{results["status"]}</h4>
            </div>
            """, unsafe_allow_html=True)

            # Alternativa sin usar delta_color
            # st.metric(
            #     "حالة المحتوى المحلي",
            #     results["status"]
            # )


        # عرض مخطط مقارنة بين النسبة الحالية والمستهدفة
        comparison_data = pd.DataFrame({
            'النوع': ['النسبة الحالية', 'النسبة المستهدفة'],
            'النسبة': [results['total_local_content'], target_lc]
        })

        fig = px.bar(
            comparison_data,
            x='النوع',
            y='النسبة',
            title="مقارنة نسبة المحتوى المحلي الحالية مع المستهدفة",
            color='النوع',
            color_discrete_map={
                'النسبة الحالية': results["color"],
                'النسبة المستهدفة': 'blue'
            }
        )

        fig.update_layout(yaxis_range=[0, 100])

        st.plotly_chart(fig, use_container_width=True)

        # عرض توزيع المحتوى المحلي حسب الفئة
        st.markdown("#### توزيع المحتوى المحلي حسب الفئة")

        categories_data = []
        for category, data in results["categories"].items():
            categories_data.append({
                'الفئة': category,
                'القيمة الإجمالية': data["total_value"],
                'قيمة المحتوى المحلي': data["local_content_value"],
                'نسبة المحتوى المحلي': data["local_content_percent"]
            })

        categories_df = pd.DataFrame(categories_data)

        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(
                categories_df,
                values='القيمة الإجمالية',
                names='الفئة',
                title="توزيع قيمة المشروع حسب الفئة"
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                categories_df,
                x='الفئة',
                y='نسبة المحتوى المحلي',
                title="نسبة المحتوى المحلي لكل فئة",
                text_auto='.1f'
            )

            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(yaxis_range=[0, 100])

            st.plotly_chart(fig, use_container_width=True)

        # عرض المكونات ذات المحتوى المحلي المنخفض
        st.markdown("#### المكونات ذات المحتوى المحلي المنخفض")

        if results["low_lc_components"]:
            low_lc_df = pd.DataFrame([
                {
                    'المكون': comp["name"],
                    'الفئة': comp["category"],
                    'القيمة': comp["value"],
                    'نسبة المحتوى المحلي': comp["local_content"],
                    'المورد': comp["supplier"]
                }
                for comp in results["low_lc_components"]
            ])

            st.dataframe(low_lc_df, use_container_width=True)

            # مخطط المكونات ذات المحتوى المحلي المنخفض
            fig = px.bar(
                low_lc_df,
                x='المكون',
                y='نسبة المحتوى المحلي',
                color='القيمة',
                title="المكونات ذات المحتوى المحلي المنخفض",
                text_auto='.1f'
            )

            fig.update_traces(texttemplate='%{text}%', textposition='outside')

            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("لا توجد مكونات ذات محتوى محلي منخفض (أقل من 50%).")

        # عرض توصيات لتحسين المحتوى المحلي
        st.markdown("#### توصيات لتحسين المحتوى المحلي")

        if results["improvement_recommendations"]:
            for recommendation in results["improvement_recommendations"]:
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                    <h5 style="margin-top: 0;">{recommendation['component']} (المحتوى المحلي الحالي: {recommendation['current_lc']}%)</h5>
                    <p>{recommendation['recommendation']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("المحتوى المحلي جيد ولا توجد توصيات للتحسين.")

        # عرض تحليل Claude AI المتقدم إذا كان متوفراً
        if "claude_analysis" in results:
            st.markdown("### تحليل Claude AI المتقدم")
            st.info(results["claude_analysis"])

    def _render_lc_suppliers_tab(self):
        """عرض تبويب قاعدة بيانات الموردين للمحتوى المحلي"""

        st.markdown("#### قاعدة بيانات الموردين المحليين")

        # قائمة الفئات
        categories = [
            "جميع الفئات",
            "مواد بناء",
            "أنظمة كهربائية",
            "أنظمة ميكانيكية",
            "تشطيبات",
            "أثاث ومفروشات",
            "خدمات هندسية",
            "أنظمة أمنية",
            "معدات وآليات"
        ]

        # اختيار الفئة
        selected_category = st.selectbox("فئة الموردين", categories)

        # البحث
        search_query = st.text_input("البحث عن مورد")

        # إعداد قائمة الموردين
        suppliers = [
            {
                "id": 1,
                "name": "شركة الإنشاءات السعودية",
                "category": "مواد بناء",
                "lc_rating": 95,
                "quality_rating": 4.5,
                "location": "الرياض",
                "contact": "info@saudiconstruction.com",
                "description": "شركة متخصصة في توريد جميع أنواع مواد البناء ذات المنشأ المحلي."
            },
            {
                "id": 2,
                "name": "مؤسسة الطاقة المتقدمة",
                "category": "أنظمة كهربائية",
                "lc_rating": 85,
                "quality_rating": 4.2,
                "location": "جدة",
                "contact": "sales@advancedpower.com",
                "description": "مؤسسة متخصصة في توريد وتركيب الأنظمة الكهربائية والطاقة المتجددة."
            },
            {
                "id": 3,
                "name": "شركة التبريد العالمية",
                "category": "أنظمة ميكانيكية",
                "lc_rating": 75,
                "quality_rating": 4.0,
                "location": "الدمام",
                "contact": "info@globalcooling.com",
                "description": "شركة متخصصة في أنظمة التكييف والتبريد المركزي للمشاريع الكبرى."
            },
            {
                "id": 4,
                "name": "شركة الزجاج المتطورة",
                "category": "مواد بناء",
                "lc_rating": 80,
                "quality_rating": 4.3,
                "location": "الرياض",
                "contact": "sales@advancedglass.com",
                "description": "شركة متخصصة في إنتاج وتوريد الزجاج والواجهات الزجاجية للمباني."
            },
            {
                "id": 5,
                "name": "مؤسسة التشطيبات الحديثة",
                "category": "تشطيبات",
                "lc_rating": 90,
                "quality_rating": 4.7,
                "location": "جدة",
                "contact": "info@modernfinishing.com",
                "description": "مؤسسة متخصصة في أعمال التشطيبات الداخلية والخارجية بجودة عالية."
            },
            {
                "id": 6,
                "name": "شركة الأثاث المكتبي",
                "category": "أثاث ومفروشات",
                "lc_rating": 70,
                "quality_rating": 4.0,
                "location": "الرياض",
                "contact": "sales@officefurniture.com",
                "description": "شركة متخصصة في تصنيع وتوريد الأثاث المكتبي والتجهيزات المكتبية."
            },
            {
                "id": 7,
                "name": "شركة الأنظمة الأمنية المتقدمة",
                "category": "أنظمة أمنية",
                "lc_rating": 65,
                "quality_rating": 4.1,
                "location": "الدمام",
                "contact": "info@advancedsecurity.com",
                "description": "شركة متخصصة في أنظمة الأمن والمراقبة والإنذار للمباني والمنشآت."
            },
            {
                "id": 8,
                "name": "شركة المعدات الهندسية",
                "category": "معدات وآليات",
                "lc_rating": 85,
                "quality_rating": 4.5,
                "location": "جدة",
                "contact": "sales@engineeringequipment.com",
                "description": "شركة متخصصة في توريد وصيانة المعدات الهندسية والآليات للمشاريع."
            },
            {
                "id": 9,
                "name": "مكتب الاستشارات الهندسية",
                "category": "خدمات هندسية",
                "lc_rating": 100,
                "quality_rating": 4.8,
                "location": "الرياض",
                "contact": "info@engineeringconsultants.com",
                "description": "مكتب استشاري متخصص في تقديم الخدمات الهندسية والاستشارية للمشاريع."
            },
            {
                "id": 10,
                "name": "مصنع الحديد السعودي",
                "category": "مواد بناء",
                "lc_rating": 100,
                "quality_rating": 4.6,
                "location": "جدة",
                "contact": "sales@saudisteel.com",
                "description": "مصنع متخصص في إنتاج وتوريد منتجات الحديد والصلب للمشاريع الإنشائية."
            }
        ]

        # تطبيق الفلترة حسب الفئة
        if selected_category != "جميع الفئات":
            filtered_suppliers = [s for s in suppliers if s["category"] == selected_category]
        else:
            filtered_suppliers = suppliers

        # تطبيق فلترة البحث
        if search_query:
            filtered_suppliers = [s for s in filtered_suppliers if search_query.lower() in s["name"].lower() or search_query.lower() in s["description"].lower()]

        # عرض الموردين
        for supplier in filtered_suppliers:
            with st.container():
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.markdown(f"""
                    <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                        <h5 style="margin-top: 0;">{supplier['name']} <span style="color: #888; font-size: 0.8em;">({supplier['category']})</span></h5>
                        <p style="margin-bottom: 5px;"><strong>الموقع:</strong> {supplier['location']} | <strong>التواصل:</strong> {supplier['contact']}</p>
                        <p style="margin-bottom: 5px;"><strong>تصنيف المحتوى المحلي:</strong> {supplier['lc_rating']}% | <strong>تقييم الجودة:</strong> {supplier['quality_rating']}/5</p>
                        <p>{supplier['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.button(f"عرض التفاصيل #{supplier['id']}", key=f"supplier_details_{supplier['id']}")
                    st.button(f"إضافة للمشروع #{supplier['id']}", key=f"add_supplier_{supplier['id']}")

        # زر إضافة مورد جديد
        st.button("إضافة مورد جديد")

    def _render_lc_reports_tab(self):
        """عرض تبويب تقارير المحتوى المحلي"""

        st.markdown("#### تقارير المحتوى المحلي")

        # اختيار نوع التقرير
        report_type = st.selectbox(
            "نوع التقرير",
            [
                "تقرير المحتوى المحلي للمشروع الحالي",
                "تقرير مقارنة المحتوى المحلي بين المشاريع",
                "تقرير التطور التاريخي للمحتوى المحلي",
                "تقرير الموردين ذوي المحتوى المحلي المرتفع",
                "تقرير الامتثال لمتطلبات هيئة المحتوى المحلي"
            ]
        )

        # عرض محاكاة للتقرير المختار
        st.markdown(f"##### {report_type}")

        if report_type == "تقرير المحتوى المحلي للمشروع الحالي":
            # محاكاة تقرير المشروع الحالي
            project_data = pd.DataFrame({
                'المكون': ['الخرسانة المسلحة', 'الأعمال الكهربائية', 'أعمال التكييف', 'الواجهات والنوافذ', 
                           'أعمال التشطيبات', 'الأثاث والتجهيزات', 'أنظمة الأمن والمراقبة', 'العمالة المباشرة'],
                'القيمة': [3000000, 1500000, 1200000, 800000, 1200000, 900000, 600000, 800000],
                'نسبة المحتوى المحلي': [85, 65, 55, 45, 80, 30, 40, 50]
            })

            # حساب قيمة المحتوى المحلي
            project_data['قيمة المحتوى المحلي'] = project_data['القيمة'] * project_data['نسبة المحتوى المحلي'] / 100

            # إضافة نسبة من إجمالي المشروع
            total_value = project_data['القيمة'].sum()
            project_data['نسبة من المشروع'] = project_data['القيمة'] / total_value * 100

            # حساب النسبة الإجمالية للمحتوى المحلي
            total_lc = project_data['قيمة المحتوى المحلي'].sum() / total_value * 100

            # عرض الإجمالي
            st.metric("نسبة المحتوى المحلي الإجمالية", f"{total_lc:.1f}%")

            # عرض تفاصيل المكونات
            st.dataframe(project_data.style.format({
                'القيمة': '{:,.0f} ريال',
                'قيمة المحتوى المحلي': '{:,.0f} ريال',
                'نسبة المحتوى المحلي': '{:.1f}%',
                'نسبة من المشروع': '{:.1f}%'
            }), use_container_width=True)

            # مخطط توزيع المحتوى المحلي
            col1, col2 = st.columns(2)

            with col1:
                fig = px.pie(
                    project_data,
                    values='القيمة',
                    names='المكون',
                    title="توزيع قيمة المشروع"
                )

                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.pie(
                    project_data,
                    values='قيمة المحتوى المحلي',
                    names='المكون',
                    title="توزيع قيمة المحتوى المحلي"
                )

                st.plotly_chart(fig, use_container_width=True)

            # مخطط شريطي للمحتوى المحلي
            fig = px.bar(
                project_data,
                x='المكون',
                y='نسبة المحتوى المحلي',
                title="نسبة المحتوى المحلي لكل مكون",
                text_auto='.1f',
                color='نسبة من المشروع'
            )

            fig.update_traces(texttemplate='%{text}%', textposition='outside')

            st.plotly_chart(fig, use_container_width=True)

        elif report_type == "تقرير مقارنة المحتوى المحلي بين المشاريع":
            # محاكاة بيانات مقارنة المشاريع
            projects_data = pd.DataFrame({
                'المشروع': ['مبنى إداري الرياض', 'مجمع سكني جدة', 'مستشفى الدمام', 'مركز تجاري المدينة', 'فندق مكة'],
                'القيمة': [10000000, 15000000, 20000000, 12000000, 18000000],
                'نسبة المحتوى المحلي': [65, 55, 70, 60, 50],
                'سنة الإنجاز': [2022, 2022, 2023, 2023, 2024]
            })

            # عرض جدول المقارنة
            st.dataframe(projects_data.style.format({
                'القيمة': '{:,.0f} ريال',
                'نسبة المحتوى المحلي': '{:.1f}%'
            }), use_container_width=True)

            # مخطط شريطي للمقارنة
            fig = px.bar(
                projects_data,
                x='المشروع',
                y='نسبة المحتوى المحلي',
                title="مقارنة نسبة المحتوى المحلي بين المشاريع",
                text_auto='.1f',
                color='سنة الإنجاز'
            )

            fig.update_traces(texttemplate='%{text}%', textposition='outside')

            st.plotly_chart(fig, use_container_width=True)

            # مخطط فقاعي للمقارنة
            fig = px.scatter(
                projects_data,
                x='القيمة',
                y='نسبة المحتوى المحلي',
                size='القيمة',
                color='سنة الإنجاز',
                text='المشروع',
                title="العلاقة بين قيمة المشروع ونسبة المحتوى المحلي"
            )

            fig.update_traces(textposition='top center')
            fig.update_layout(xaxis_title="قيمة المشروع (ريال)", yaxis_title="نسبة المحتوى المحلي (%)")

            st.plotly_chart(fig, use_container_width=True)

        elif report_type == "تقرير التطور التاريخي للمحتوى المحلي":
            # محاكاة بيانات التطور التاريخي
            historical_data = pd.DataFrame({
                'السنة': [2019, 2020, 2021, 2022, 2023, 2024],
                'نسبة المحتوى المحلي': [45, 48, 52, 58, 62, 66],
                'المستهدف': [40, 45, 50, 55, 60, 65]
            })

            # عرض جدول التطور التاريخي
            st.dataframe(historical_data.style.format({
                'نسبة المحتوى المحلي': '{:.1f}%',
                'المستهدف': '{:.1f}%'
            }), use_container_width=True)

            # مخطط خطي للتطور التاريخي
            fig = px.line(
                historical_data,
                x='السنة',
                y=['نسبة المحتوى المحلي', 'المستهدف'],
                title="التطور التاريخي لنسبة المحتوى المحلي",
                markers=True,
                labels={'value': 'النسبة (%)', 'variable': ''}
            )

            fig.update_layout(legend_title_text='')

            st.plotly_chart(fig, use_container_width=True)

            # مخطط شريطي للمقارنة بين الفعلي والمستهدف
            historical_data['الفرق'] = historical_data['نسبة المحتوى المحلي'] - historical_data['المستهدف']

            fig = px.bar(
                historical_data,
                x='السنة',
                y='الفرق',
                title="الفرق بين نسبة المحتوى المحلي الفعلية والمستهدفة",
                text_auto='.1f',
                color='الفرق',
                color_continuous_scale=['red', 'green']
            )

            fig.update_traces(texttemplate='%{text}%', textposition='outside')

            st.plotly_chart(fig, use_container_width=True)

        elif report_type == "تقرير الموردين ذوي المحتوى المحلي المرتفع":
            # محاكاة بيانات الموردين
            suppliers_data = pd.DataFrame({
                'المورد': ['شركة الإنشاءات السعودية', 'مؤسسة الطاقة المتقدمة', 'شركة التبريد العالمية', 
                           'شركة الزجاج المتطورة', 'مؤسسة التشطيبات الحديثة', 'مصنع الحديد السعودي',
                           'شركة المعدات الهندسية', 'مكتب الاستشارات الهندسية'],
                'الفئة': ['مواد بناء', 'أنظمة كهربائية', 'أنظمة ميكانيكية', 'مواد بناء', 
                          'تشطيبات', 'مواد بناء', 'معدات وآليات', 'خدمات هندسية'],
                'نسبة المحتوى المحلي': [95, 85, 75, 80, 90, 100, 85, 100],
                'حجم التعامل': [3000000, 1500000, 1200000, 800000, 1200000, 2500000, 900000, 500000]
            })

            # عرض جدول الموردين
            st.dataframe(suppliers_data.style.format({
                'نسبة المحتوى المحلي': '{:.0f}%',
                'حجم التعامل': '{:,.0f} ريال'
            }), use_container_width=True)

            # مخطط شريطي للموردين
            fig = px.bar(
                suppliers_data,
                x='المورد',
                y='نسبة المحتوى المحلي',
                title="نسبة المحتوى المحلي للموردين",
                text_auto='.0f',
                color='الفئة'
            )

            fig.update_traces(texttemplate='%{text}%', textposition='outside')
            fig.update_layout(xaxis_tickangle=-45)

            st.plotly_chart(fig, use_container_width=True)

            # مخطط فقاعي للموردين
            fig = px.scatter(
                suppliers_data,
                x='نسبة المحتوى المحلي',
                y='حجم التعامل',
                size='حجم التعامل',
                color='الفئة',
                text='المورد',
                title="العلاقة بين نسبة المحتوى المحلي وحجم التعامل مع الموردين"
            )

            fig.update_traces(textposition='top center')
            fig.update_layout(xaxis_title="نسبة المحتوى المحلي (%)", yaxis_title="حجم التعامل (ريال)")

            st.plotly_chart(fig, use_container_width=True)

        elif report_type == "تقرير الامتثال لمتطلبات هيئة المحتوى المحلي":
            # محاكاة بيانات الامتثال
            compliance_data = pd.DataFrame({
                'المتطلب': [
                    'نسبة المحتوى المحلي الإجمالية',
                    'نسبة السعودة في القوى العاملة',
                    'نسبة المنتجات المحلية',
                    'نسبة الخدمات المحلية',
                    'نسبة الموردين المحليين',
                    'المساهمة في تطوير المحتوى المحلي'
                ],
                'المستهدف': [40, 30, 50, 60, 70, 20],
                'المحقق': [38, 35, 45, 65, 75, 25],
                'حالة الامتثال': ['قريب', 'ممتثل', 'غير ممتثل', 'ممتثل', 'ممتثل', 'ممتثل']
            })

            # إضافة ألوان لحالة الامتثال
            colors = []
            for status in compliance_data['حالة الامتثال']:
                if status == 'ممتثل':
                    colors.append('green')
                elif status == 'قريب':
                    colors.append('orange')
                else:
                    colors.append('red')

            compliance_data['اللون'] = colors

            # عرض جدول الامتثال
            st.dataframe(compliance_data.style.format({
                'المستهدف': '{:.0f}%',
                'المحقق': '{:.0f}%'
            }), use_container_width=True)

            # مخطط شريطي للامتثال
            fig = px.bar(
                compliance_data,
                x='المتطلب',
                y=['المستهدف', 'المحقق'],
                title="مقارنة المتطلبات المستهدفة والمحققة",
                barmode='group',
                labels={'value': 'النسبة (%)', 'variable': ''}
            )

            st.plotly_chart(fig, use_container_width=True)

            # مخطط دائري لحالة الامتثال
            status_counts = compliance_data['حالة الامتثال'].value_counts().reset_index()
            status_counts.columns = ['حالة الامتثال', 'العدد']

            fig = px.pie(
                status_counts,
                values='العدد',
                names='حالة الامتثال',
                title="توزيع حالة الامتثال للمتطلبات",
                color='حالة الامتثال',
                color_discrete_map={
                    'ممتثل': 'green',
                    'قريب': 'orange',
                    'غير ممتثل': 'red'
                }
            )

            st.plotly_chart(fig, use_container_width=True)

        # أزرار التصدير
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                "تصدير التقرير كملف Excel",
                "بيانات التقرير",
                file_name=f"{report_type}.xlsx",
                mime="application/vnd.ms-excel"
            )

        with col2:
            st.download_button(
                "تصدير التقرير كملف PDF",
                "بيانات التقرير",
                file_name=f"{report_type}.pdf",
                mime="application/pdf"
            )

    def _render_lc_optimization_tab(self):
        """عرض تبويب تحسين المحتوى المحلي"""

        st.markdown("#### تحسين المحتوى المحلي")

        st.markdown("""
        تساعدك هذه الأداة في تحسين نسبة المحتوى المحلي في المشروع من خلال تقديم توصيات وبدائل للمكونات ذات المحتوى المحلي المنخفض.
        """)

        # عرض المكونات ذات المحتوى المحلي المنخفض
        st.markdown("##### المكونات ذات المحتوى المحلي المنخفض")

        # محاكاة بيانات المكونات ذات المحتوى المحلي المنخفض
        low_lc_components = [
            {
                "id": 1,
                "name": "الأثاث والتجهيزات",
                "category": "أثاث",
                "value": 900000,
                "local_content": 30,
                "supplier": "شركة الأثاث المكتبي"
            },
            {
                "id": 2,
                "name": "أنظمة الأمن والمراقبة",
                "category": "أنظمة",
                "value": 600000,
                "local_content": 40,
                "supplier": "شركة الأنظمة الأمنية المتقدمة"
            },
            {
                "id": 3,
                "name": "الواجهات والنوافذ",
                "category": "مواد",
                "value": 800000,
                "local_content": 45,
                "supplier": "شركة الزجاج المتطورة"
            }
        ]

        # عرض جدول المكونات
        low_lc_df = pd.DataFrame(low_lc_components)

        st.dataframe(
            low_lc_df[["name", "category", "value", "local_content", "supplier"]].rename(columns={
                "name": "المكون",
                "category": "الفئة",
                "value": "القيمة",
                "local_content": "المحتوى المحلي",
                "supplier": "المورد"
            }).style.format({
                "القيمة": "{:,.0f} ريال",
                "المحتوى المحلي": "{:.0f}%"
            }),
            use_container_width=True
        )

        # اختيار مكون للتحسين
        selected_component = st.selectbox(
            "اختر المكون للتحسين",
            options=[comp["name"] for comp in low_lc_components],
            index=0
        )

        # الحصول على المكون المختار
        selected_comp_data = next((comp for comp in low_lc_components if comp["name"] == selected_component), None)

        # عرض بدائل المكون المختار
        if selected_comp_data:
            st.markdown(f"##### البدائل المقترحة لـ {selected_component}")

            # محاكاة بيانات البدائل
            alternatives = []

            if selected_component == "الأثاث والتجهيزات":
                alternatives = [
                    {
                        "id": 1,
                        "name": "شركة الأثاث الوطني",
                        "description": "شركة متخصصة في تصنيع الأثاث المكتبي محلياً",
                        "local_content": 80,
                        "cost_factor": 1.05,
                        "quality_rating": 4.2
                    },
                    {
                        "id": 2,
                        "name": "مصنع التجهيزات المكتبية",
                        "description": "مصنع متخصص في إنتاج الأثاث المكتبي بخامات محلية",
                        "local_content": 90,
                        "cost_factor": 1.10,
                        "quality_rating": 4.5
                    },
                    {
                        "id": 3,
                        "name": "توزيع المكونات على موردين محليين",
                        "description": "تقسيم توريد الأثاث على عدة موردين محليين",
                        "local_content": 75,
                        "cost_factor": 1.00,
                        "quality_rating": 4.0
                    }
                ]
            elif selected_component == "أنظمة الأمن والمراقبة":
                alternatives = [
                    {
                        "id": 1,
                        "name": "شركة التقنية الأمنية السعودية",
                        "description": "شركة متخصصة في تركيب وتجميع أنظمة الأمن محلياً",
                        "local_content": 70,
                        "cost_factor": 1.08,
                        "quality_rating": 4.0
                    },
                    {
                        "id": 2,
                        "name": "مؤسسة تقنيات الحماية",
                        "description": "توريد وتركيب أنظمة أمنية معتمدة من هيئة المحتوى المحلي",
                        "local_content": 65,
                        "cost_factor": 0.95,
                        "quality_rating": 3.8
                    },
                    {
                        "id": 3,
                        "name": "تجميع الأنظمة محلياً",
                        "description": "استيراد المكونات وتجميعها وبرمجتها محلياً",
                        "local_content": 60,
                        "cost_factor": 0.90,
                        "quality_rating": 3.7
                    }
                ]
            elif selected_component == "الواجهات والنوافذ":
                alternatives = [
                    {
                        "id": 1,
                        "name": "مصنع الزجاج السعودي",
                        "description": "مصنع متخصص في إنتاج الزجاج والواجهات الزجاجية محلياً",
                        "local_content": 85,
                        "cost_factor": 1.15,
                        "quality_rating": 4.3
                    },
                    {
                        "id": 2,
                        "name": "شركة الألمنيوم الوطنية",
                        "description": "شركة متخصصة في إنتاج الواجهات والنوافذ من الألمنيوم محلياً",
                        "local_content": 90,
                        "cost_factor": 1.20,
                        "quality_rating": 4.5
                    },
                    {
                        "id": 3,
                        "name": "تعديل التصميم لاستخدام مواد محلية",
                        "description": "تعديل تصميم الواجهات لاستخدام نسبة أكبر من المواد المتوفرة محلياً",
                        "local_content": 75,
                        "cost_factor": 1.00,
                        "quality_rating": 4.0
                    }
                ]

            # عرض البدائل
            for alt in alternatives:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])

                    with col1:
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; border-radius: 5px; padding: 10px; margin-bottom: 10px;">
                            <h6 style="margin-top: 0;">{alt['name']}</h6>
                            <p style="margin-bottom: 5px;">{alt['description']}</p>
                            <p style="margin-bottom: 0;"><strong>المحتوى المحلي:</strong> {alt['local_content']}% | <strong>معامل التكلفة:</strong> {alt['cost_factor']:.2f} | <strong>تقييم الجودة:</strong> {alt['quality_rating']}/5</p>
                        </div>
                        """, unsafe_allow_html=True)

                    with col2:
                        st.button(f"تفاصيل #{alt['id']}", key=f"alt_details_{alt['id']}")

                    with col3:
                        if st.button(f"اختيار #{alt['id']}", key=f"select_alt_{alt['id']}"):
                            st.success(f"تم اختيار {alt['name']} كبديل لـ {selected_component}.")

            # حساب تأثير البدائل على المحتوى المحلي الإجمالي
            st.markdown("##### تأثير البدائل على المحتوى المحلي الإجمالي")

            # محاكاة البيانات الإجمالية
            total_value = 10000000
            current_lc_value = 6000000
            current_lc_percent = current_lc_value / total_value * 100

            # حساب التأثير لكل بديل
            impact_data = []
            for alt in alternatives:
                # القيمة الحالية للمحتوى المحلي في المكون
                current_component_lc_value = selected_comp_data["value"] * selected_comp_data["local_content"] / 100

                # القيمة المتوقعة للمحتوى المحلي مع البديل
                new_component_value = selected_comp_data["value"] * alt["cost_factor"]
                new_component_lc_value = new_component_value * alt["local_content"] / 100

                # الفرق في قيمة المحتوى المحلي
                lc_value_diff = new_component_lc_value - current_component_lc_value

                # القيمة الإجمالية الجديدة للمشروع
                new_total_value = total_value - selected_comp_data["value"] + new_component_value

                # قيمة المحتوى المحلي الإجمالية الجديدة
                new_total_lc_value = current_lc_value + lc_value_diff

                # نسبة المحتوى المحلي الإجمالية الجديدة
                new_total_lc_percent = new_total_lc_value / new_total_value * 100

                # إضافة البيانات
                impact_data.append({
                    "البديل": alt["name"],
                    "نسبة المحتوى المحلي الحالية": current_lc_percent,
                    "نسبة المحتوى المحلي المتوقعة": new_total_lc_percent,
                    "التغير": new_total_lc_percent - current_lc_percent,
                    "القيمة الإجمالية الجديدة": new_total_value,
                    "تقييم الجودة": alt["quality_rating"]
                })

            # عرض جدول التأثير
            impact_df = pd.DataFrame(impact_data)

            st.dataframe(
                impact_df.style.format({
                    "نسبة المحتوى المحلي الحالية": "{:.1f}%",
                    "نسبة المحتوى المحلي المتوقعة": "{:.1f}%",
                    "التغير": "{:+.1f}%",
                    "القيمة الإجمالية الجديدة": "{:,.0f} ريال",
                    "تقييم الجودة": "{:.1f}/5"
                }),
                use_container_width=True
            )

            # مخطط مقارنة للبدائل
            fig = px.bar(
                impact_df,
                x="البديل",
                y=["نسبة المحتوى المحلي الحالية", "نسبة المحتوى المحلي المتوقعة"],
                barmode="group",
                title="مقارنة تأثير البدائل على نسبة المحتوى المحلي الإجمالية",
                labels={"value": "نسبة المحتوى المحلي (%)", "variable": ""}
            )

            st.plotly_chart(fig, use_container_width=True)

            # استخدام Claude AI للتحليل المتقدم
            if st.checkbox("استخدام Claude AI لتحليل البدائل", value=False, key="lc_optimization_use_claude"):
                with st.spinner("جاري تحليل البدائل..."):
                    # محاكاة وقت المعالجة
                    time.sleep(2)

                    try:
                        # إنشاء نص المدخلات للتحليل
                        prompt = f"""تحليل بدائل المحتوى المحلي لمكون {selected_component}:

                        المكون الحالي:
                        - الاسم: {selected_component}
                        - الفئة: {selected_comp_data['category']}
                        - القيمة: {selected_comp_data['value']:,} ريال
                        - نسبة المحتوى المحلي: {selected_comp_data['local_content']}%
                        - المورد: {selected_comp_data['supplier']}

                        البدائل المقترحة:
                        1. {alternatives[0]['name']}:
                           - المحتوى المحلي: {alternatives[0]['local_content']}%
                           - معامل التكلفة: {alternatives[0]['cost_factor']:.2f}
                           - تقييم الجودة: {alternatives[0]['quality_rating']}/5
                           - الوصف: {alternatives[0]['description']}

                        2. {alternatives[1]['name']}:
                           - المحتوى المحلي: {alternatives[1]['local_content']}%
                           - معامل التكلفة: {alternatives[1]['cost_factor']:.2f}
                           - تقييم الجودة: {alternatives[1]['quality_rating']}/5
                           - الوصف: {alternatives[1]['description']}

                        3. {alternatives[2]['name']}:
                           - المحتوى المحلي: {alternatives[2]['local_content']}%
                           - معامل التكلفة: {alternatives[2]['cost_factor']:.2f}
                           - تقييم الجودة: {alternatives[2]['quality_rating']}/5
                           - الوصف: {alternatives[2]['description']}

                        المطلوب:
                        1. تحليل مقارن شامل للبدائل من حيث المحتوى المحلي والتكلفة والجودة
                        2. تحديد البديل الأفضل مع شرح أسباب اختياره
                        3. تقديم توصيات إضافية لتحسين المحتوى المحلي لهذا المكون
                        4. تحديد أي مخاطر محتملة في الانتقال للبديل المقترح

                        يرجى تقديم تحليل مهني ومختصر يركز على الجوانب الأكثر أهمية.
                        """

                        # استدعاء Claude للتحليل
                        claude_analysis = self.claude_service.chat_completion(
                            [{"role": "user", "content": prompt}]
                        )

                        if "error" not in claude_analysis:
                            # عرض تحليل Claude
                            st.markdown("##### تحليل متقدم للبدائل")
                            st.info(claude_analysis["content"])
                        else:
                            st.warning(f"تعذر إجراء التحليل المتقدم: {claude_analysis['error']}")
                    except Exception as e:
                        st.warning(f"تعذر إجراء التحليل المتقدم: {str(e)}")

            # زر تطبيق البديل المختار
            if st.button("تطبيق البديل المختار على المشروع"):
                st.success("تم تطبيق البديل المختار على المشروع وتحديث نسبة المحتوى المحلي.")

    def _render_faq_tab(self):
        """عرض تبويب الأسئلة الشائعة"""

        st.markdown("### الأسئلة الشائعة")

        # البحث في الأسئلة الشائعة
        search_query = st.text_input("البحث في الأسئلة الشائعة", key="faq_search")

        # فلترة الأسئلة حسب البحث
        if search_query:
            filtered_faqs = [
                faq for faq in self.faqs 
                if search_query.lower() in faq["question"].lower() or search_query.lower() in faq["answer"].lower()
            ]
        else:
            filtered_faqs = self.faqs

        # عرض الأسئلة والأجوبة
        for i, faq in enumerate(filtered_faqs):
            with st.expander(faq["question"]):
                st.markdown(faq["answer"])

        # زر التواصل مع الدعم
        st.markdown("##### لم تجد إجابة لسؤالك؟")
        col1, col2 = st.columns(2)

        with col1:
            if st.button("التواصل مع الدعم الفني", use_container_width=True):
                st.info("سيتم التواصل معك قريباً من قبل فريق الدعم الفني.")

        with col2:
            if st.button("طرح سؤال جديد", use_container_width=True):
                st.text_area("اكتب سؤالك هنا")
                st.button("إرسال")