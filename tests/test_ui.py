"""
وحدة اختبار واجهة المستخدم لنظام إدارة المناقصات - Hybrid Face
"""

import os
import sys
import logging
import unittest
import tkinter as tk
import customtkinter as ctk
from pathlib import Path

# تهيئة السجل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_ui')

# إضافة المسار الرئيسي للتطبيق إلى مسار البحث
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# استيراد الوحدات المطلوبة للاختبار
from styling.theme import AppTheme
from styling.icons import IconGenerator
from styling.charts import ChartGenerator
from config import AppConfig

class TestUIComponents(unittest.TestCase):
    """اختبار مكونات واجهة المستخدم"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        self.root = ctk.CTk()
        self.root.withdraw()  # إخفاء النافذة أثناء الاختبار
        self.theme = AppTheme()
    
    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        self.root.destroy()
    
    def test_styled_frame(self):
        """اختبار الإطار المنسق"""
        frame = self.theme.create_styled_frame(self.root)
        self.assertIsNotNone(frame)
        self.assertEqual(frame.cget("fg_color"), self.theme.get_color("card_bg_color"))
        self.assertEqual(frame.cget("corner_radius"), self.theme.get_size("border_radius"))
    
    def test_styled_button(self):
        """اختبار الزر المنسق"""
        button = self.theme.create_styled_button(self.root, "زر اختبار")
        self.assertIsNotNone(button)
        self.assertEqual(button.cget("text"), "زر اختبار")
        self.assertEqual(button.cget("fg_color"), self.theme.get_color("button_bg_color"))
        self.assertEqual(button.cget("text_color"), self.theme.get_color("button_fg_color"))
    
    def test_styled_label(self):
        """اختبار التسمية المنسقة"""
        label = self.theme.create_styled_label(self.root, "تسمية اختبار")
        self.assertIsNotNone(label)
        self.assertEqual(label.cget("text"), "تسمية اختبار")
        self.assertEqual(label.cget("text_color"), self.theme.get_color("fg_color"))
    
    def test_styled_entry(self):
        """اختبار حقل الإدخال المنسق"""
        entry = self.theme.create_styled_entry(self.root, "نص توضيحي")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.cget("placeholder_text"), "نص توضيحي")
        self.assertEqual(entry.cget("fg_color"), self.theme.get_color("input_bg_color"))
        self.assertEqual(entry.cget("text_color"), self.theme.get_color("input_fg_color"))
    
    def test_styled_combobox(self):
        """اختبار القائمة المنسدلة المنسقة"""
        values = ["الخيار الأول", "الخيار الثاني", "الخيار الثالث"]
        combobox = self.theme.create_styled_combobox(self.root, values)
        self.assertIsNotNone(combobox)
        self.assertEqual(combobox.cget("values"), values)
        self.assertEqual(combobox.cget("fg_color"), self.theme.get_color("input_bg_color"))
        self.assertEqual(combobox.cget("text_color"), self.theme.get_color("input_fg_color"))
    
    def test_styled_checkbox(self):
        """اختبار خانة الاختيار المنسقة"""
        checkbox = self.theme.create_styled_checkbox(self.root, "خانة اختبار")
        self.assertIsNotNone(checkbox)
        self.assertEqual(checkbox.cget("text"), "خانة اختبار")
        self.assertEqual(checkbox.cget("fg_color"), self.theme.get_color("button_bg_color"))
        self.assertEqual(checkbox.cget("text_color"), self.theme.get_color("fg_color"))
    
    def test_styled_radio_button(self):
        """اختبار زر الراديو المنسق"""
        var = ctk.StringVar(value="1")
        radio_button = self.theme.create_styled_radio_button(self.root, "زر راديو اختبار", var, "1")
        self.assertIsNotNone(radio_button)
        self.assertEqual(radio_button.cget("text"), "زر راديو اختبار")
        self.assertEqual(radio_button.cget("fg_color"), self.theme.get_color("button_bg_color"))
        self.assertEqual(radio_button.cget("text_color"), self.theme.get_color("fg_color"))
    
    def test_styled_switch(self):
        """اختبار مفتاح التبديل المنسق"""
        switch = self.theme.create_styled_switch(self.root, "مفتاح اختبار")
        self.assertIsNotNone(switch)
        self.assertEqual(switch.cget("text"), "مفتاح اختبار")
        self.assertEqual(switch.cget("progress_color"), self.theme.get_color("button_bg_color"))
        self.assertEqual(switch.cget("text_color"), self.theme.get_color("fg_color"))
    
    def test_styled_slider(self):
        """اختبار شريط التمرير المنسق"""
        slider = self.theme.create_styled_slider(self.root)
        self.assertIsNotNone(slider)
        self.assertEqual(slider.cget("fg_color"), self.theme.get_color("input_border_color"))
        self.assertEqual(slider.cget("progress_color"), self.theme.get_color("button_bg_color"))
    
    def test_styled_progressbar(self):
        """اختبار شريط التقدم المنسق"""
        progressbar = self.theme.create_styled_progressbar(self.root)
        self.assertIsNotNone(progressbar)
        self.assertEqual(progressbar.cget("fg_color"), self.theme.get_color("input_border_color"))
        self.assertEqual(progressbar.cget("progress_color"), self.theme.get_color("button_bg_color"))
    
    def test_styled_tabview(self):
        """اختبار عرض التبويب المنسق"""
        tabview = self.theme.create_styled_tabview(self.root)
        self.assertIsNotNone(tabview)
        self.assertEqual(tabview.cget("fg_color"), self.theme.get_color("card_bg_color"))
    
    def test_styled_scrollable_frame(self):
        """اختبار الإطار القابل للتمرير المنسق"""
        scrollable_frame = self.theme.create_styled_scrollable_frame(self.root)
        self.assertIsNotNone(scrollable_frame)
        self.assertEqual(scrollable_frame.cget("fg_color"), "transparent")
    
    def test_styled_textbox(self):
        """اختبار مربع النص المنسق"""
        textbox = self.theme.create_styled_textbox(self.root)
        self.assertIsNotNone(textbox)
        self.assertEqual(textbox.cget("fg_color"), self.theme.get_color("input_bg_color"))
        self.assertEqual(textbox.cget("text_color"), self.theme.get_color("input_fg_color"))
    
    def test_styled_card(self):
        """اختبار البطاقة المنسقة"""
        card, content_frame = self.theme.create_styled_card(self.root, "بطاقة اختبار")
        self.assertIsNotNone(card)
        self.assertIsNotNone(content_frame)
        self.assertEqual(card.cget("fg_color"), self.theme.get_color("card_bg_color"))
    
    def test_styled_data_table(self):
        """اختبار جدول البيانات المنسق"""
        columns = ["العمود الأول", "العمود الثاني", "العمود الثالث"]
        data = [
            ["بيانات 1-1", "بيانات 1-2", "بيانات 1-3"],
            ["بيانات 2-1", "بيانات 2-2", "بيانات 2-3"]
        ]
        table_frame, data_frame = self.theme.create_styled_data_table(self.root, columns, data)
        self.assertIsNotNone(table_frame)
        self.assertIsNotNone(data_frame)
        self.assertEqual(table_frame.cget("fg_color"), self.theme.get_color("card_bg_color"))
    
    def test_theme_switching(self):
        """اختبار تبديل النمط"""
        # تعيين النمط الفاتح
        self.theme.set_theme("light")
        light_bg_color = self.theme.get_color("bg_color")
        
        # تعيين النمط الداكن
        self.theme.set_theme("dark")
        dark_bg_color = self.theme.get_color("bg_color")
        
        # التحقق من اختلاف الألوان
        self.assertNotEqual(light_bg_color, dark_bg_color)
    
    def test_language_switching(self):
        """اختبار تبديل اللغة"""
        # تعيين اللغة العربية
        self.theme.set_language("ar")
        ar_font = self.theme.get_font("body")
        
        # تعيين اللغة الإنجليزية
        self.theme.set_language("en")
        en_font = self.theme.get_font("body")
        
        # التحقق من اختلاف الخطوط
        self.assertNotEqual(ar_font[0], en_font[0])


class TestUILayout(unittest.TestCase):
    """اختبار تخطيط واجهة المستخدم"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        self.root = ctk.CTk()
        self.root.withdraw()  # إخفاء النافذة أثناء الاختبار
        self.theme = AppTheme()
        
        # إنشاء الإطار الرئيسي
        self.main_frame = self.theme.create_styled_frame(self.root)
        self.main_frame.pack(fill="both", expand=True)
        
        # إنشاء الشريط الجانبي
        self.sidebar_frame = self.theme.create_styled_frame(
            self.main_frame,
            fg_color=self.theme.get_color("sidebar_bg_color")
        )
        self.sidebar_frame.pack(side="left", fill="y", padx=0, pady=0)
        
        # إنشاء إطار المحتوى
        self.content_frame = self.theme.create_styled_frame(
            self.main_frame,
            fg_color=self.theme.get_color("bg_color")
        )
        self.content_frame.pack(side="right", fill="both", expand=True, padx=0, pady=0)
    
    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        self.root.destroy()
    
    def test_sidebar_layout(self):
        """اختبار تخطيط الشريط الجانبي"""
        # إنشاء شعار التطبيق
        logo_label = self.theme.create_styled_label(
            self.sidebar_frame,
            "نظام إدارة المناقصات",
            font=self.theme.get_font("title"),
            text_color=self.theme.get_color("sidebar_fg_color")
        )
        logo_label.pack(padx=20, pady=20)
        
        # إنشاء أزرار الشريط الجانبي
        sidebar_buttons = []
        button_texts = [
            "لوحة التحكم", "المشاريع", "المستندات", "التسعير",
            "الموارد", "المخاطر", "التقارير", "الذكاء الاصطناعي"
        ]
        
        for text in button_texts:
            button_frame, button = self.theme.create_styled_sidebar_button(
                self.sidebar_frame,
                text
            )
            button_frame.pack(fill="x", padx=0, pady=2)
            sidebar_buttons.append(button)
        
        # التحقق من إنشاء الأزرار
        self.assertEqual(len(sidebar_buttons), len(button_texts))
        for i, button in enumerate(sidebar_buttons):
            self.assertEqual(button.cget("text"), button_texts[i])
    
    def test_content_layout(self):
        """اختبار تخطيط المحتوى"""
        # إنشاء شريط العنوان
        header_frame = self.theme.create_styled_frame(
            self.content_frame,
            fg_color=self.theme.get_color("card_bg_color")
        )
        header_frame.pack(fill="x", padx=20, pady=20)
        
        # إنشاء عنوان الصفحة
        page_title = self.theme.create_styled_label(
            header_frame,
            "لوحة التحكم",
            font=self.theme.get_font("title")
        )
        page_title.pack(side="left", padx=20, pady=20)
        
        # إنشاء زر البحث
        search_button = self.theme.create_styled_button(
            header_frame,
            "بحث"
        )
        search_button.pack(side="right", padx=20, pady=20)
        
        # إنشاء إطار البطاقات
        cards_frame = self.theme.create_styled_frame(
            self.content_frame,
            fg_color="transparent"
        )
        cards_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # إنشاء بطاقات
        cards = []
        card_titles = [
            "المشاريع النشطة", "المناقصات الجديدة", "المخاطر العالية", "التقارير المعلقة"
        ]
        
        for i, title in enumerate(card_titles):
            card, card_content = self.theme.create_styled_card(
                cards_frame,
                title
            )
            card.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="nsew")
            cards.append(card)
        
        # التحقق من إنشاء البطاقات
        self.assertEqual(len(cards), len(card_titles))
        
        # تهيئة أوزان الصفوف والأعمدة
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        cards_frame.grid_rowconfigure(0, weight=1)
        cards_frame.grid_rowconfigure(1, weight=1)
    
    def test_responsive_layout(self):
        """اختبار التخطيط المتجاوب"""
        # تغيير حجم النافذة
        self.root.geometry("800x600")
        self.root.update()
        
        # التحقق من أن الإطار الرئيسي يملأ النافذة
        self.assertEqual(self.main_frame.winfo_width(), 800)
        self.assertEqual(self.main_frame.winfo_height(), 600)
        
        # تغيير حجم النافذة مرة أخرى
        self.root.geometry("1024x768")
        self.root.update()
        
        # التحقق من أن الإطار الرئيسي يملأ النافذة
        self.assertEqual(self.main_frame.winfo_width(), 1024)
        self.assertEqual(self.main_frame.winfo_height(), 768)


class TestUIArabicSupport(unittest.TestCase):
    """اختبار دعم اللغة العربية في واجهة المستخدم"""
    
    def setUp(self):
        """إعداد بيئة الاختبار"""
        self.root = ctk.CTk()
        self.root.withdraw()  # إخفاء النافذة أثناء الاختبار
        self.theme = AppTheme()
        self.theme.set_language("ar")  # تعيين اللغة العربية
    
    def tearDown(self):
        """تنظيف بيئة الاختبار"""
        self.root.destroy()
    
    def test_arabic_text_display(self):
        """اختبار عرض النص العربي"""
        # إنشاء تسمية بنص عربي
        arabic_text = "هذا نص عربي للاختبار"
        label = self.theme.create_styled_label(self.root, arabic_text)
        self.assertEqual(label.cget("text"), arabic_text)
        
        # إنشاء زر بنص عربي
        button = self.theme.create_styled_button(self.root, "زر باللغة العربية")
        self.assertEqual(button.cget("text"), "زر باللغة العربية")
        
        # إنشاء حقل إدخال بنص توضيحي عربي
        entry = self.theme.create_styled_entry(self.root, "أدخل النص هنا")
        self.assertEqual(entry.cget("placeholder_text"), "أدخل النص هنا")
    
    def test_arabic_font(self):
        """اختبار الخط العربي"""
        # التحقق من استخدام خط يدعم العربية
        ar_font = self.theme.get_font("body")
        self.assertEqual(ar_font[0], "Cairo")
    
    def test_rtl_support(self):
        """اختبار دعم الكتابة من اليمين إلى اليسار"""
        # إنشاء إطار
        frame = self.theme.create_styled_frame(self.root)
        frame.pack(fill="both", expand=True)
        
        # إنشاء تسمية بنص عربي
        label = self.theme.create_styled_label(frame, "نص عربي من اليمين إلى اليسار")
        label.pack(anchor="e", padx=20, pady=20)  # محاذاة إلى اليمين
        
        # التحقق من المحاذاة
        self.assertEqual(label.cget("anchor"), "w")  # w تعني غرب (يسار)، لكن النص سيظهر من اليمين إلى اليسار


def run_ui_tests():
    """تشغيل اختبارات واجهة المستخدم"""
    # إنشاء مجلد الاختبارات
    test_dir = Path('test_results')
    test_dir.mkdir(exist_ok=True)
    
    # إنشاء ملف لنتائج الاختبارات
    test_results_file = test_dir / 'ui_test_results.txt'
    
    # تشغيل الاختبارات وحفظ النتائج
    with open(test_results_file, 'w', encoding='utf-8') as f:
        runner = unittest.TextTestRunner(stream=f, verbosity=2)
        suite = unittest.TestSuite()
        
        # إضافة اختبارات مكونات واجهة المستخدم
        suite.addTest(unittest.makeSuite(TestUIComponents))
        
        # إضافة اختبارات تخطيط واجهة المستخدم
        suite.addTest(unittest.makeSuite(TestUILayout))
        
        # إضافة اختبارات دعم اللغة العربية
        suite.addTest(unittest.makeSuite(TestUIArabicSupport))
        
        # تشغيل الاختبارات
        result = runner.run(suite)
        
        # كتابة ملخص النتائج
        f.write("\n\n=== ملخص نتائج اختبارات واجهة المستخدم ===\n")
        f.write(f"عدد الاختبارات: {result.testsRun}\n")
        f.write(f"عدد النجاحات: {result.testsRun - len(result.failures) - len(result.errors)}\n")
        f.write(f"عدد الإخفاقات: {len(result.failures)}\n")
        f.write(f"عدد الأخطاء: {len(result.errors)}\n")
    
    # طباعة ملخص النتائج
    logger.info(f"تم تشغيل {result.testsRun} اختبار لواجهة المستخدم")
    logger.info(f"النجاحات: {result.testsRun - len(result.failures) - len(result.errors)}")
    logger.info(f"الإخفاقات: {len(result.failures)}")
    logger.info(f"الأخطاء: {len(result.errors)}")
    logger.info(f"تم حفظ نتائج الاختبارات في: {test_results_file}")
    
    return result


if __name__ == "__main__":
    run_ui_tests()
