"""
ملف النمط لنظام إدارة المناقصات
"""

import os
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AppTheme:
    """فئة نمط التطبيق"""
    
    # ألوان النمط الفاتح
    LIGHT_BG_COLOR = "#F5F5F5"
    LIGHT_FG_COLOR = "#333333"
    LIGHT_CARD_BG_COLOR = "#FFFFFF"
    LIGHT_SIDEBAR_BG_COLOR = "#2C3E50"
    LIGHT_SIDEBAR_FG_COLOR = "#FFFFFF"
    LIGHT_SIDEBAR_HOVER_COLOR = "#34495E"
    LIGHT_SIDEBAR_ACTIVE_COLOR = "#1ABC9C"
    LIGHT_BUTTON_BG_COLOR = "#2980B9"
    LIGHT_BUTTON_HOVER_COLOR = "#3498DB"
    LIGHT_BUTTON_ACTIVE_COLOR = "#1F618D"
    LIGHT_INPUT_BG_COLOR = "#FFFFFF"
    LIGHT_INPUT_FG_COLOR = "#333333"
    LIGHT_BORDER_COLOR = "#E0E0E0"
    
    # ألوان النمط الداكن
    DARK_BG_COLOR = "#121212"
    DARK_FG_COLOR = "#E0E0E0"
    DARK_CARD_BG_COLOR = "#1E1E1E"
    DARK_SIDEBAR_BG_COLOR = "#1A1A2E"
    DARK_SIDEBAR_FG_COLOR = "#E0E0E0"
    DARK_SIDEBAR_HOVER_COLOR = "#16213E"
    DARK_SIDEBAR_ACTIVE_COLOR = "#0F3460"
    DARK_BUTTON_BG_COLOR = "#0F3460"
    DARK_BUTTON_HOVER_COLOR = "#16213E"
    DARK_BUTTON_ACTIVE_COLOR = "#1A1A2E"
    DARK_INPUT_BG_COLOR = "#2C2C2C"
    DARK_INPUT_FG_COLOR = "#E0E0E0"
    DARK_BORDER_COLOR = "#333333"
    
    # ألوان الأساسية
    PRIMARY_COLOR = {
        "light": "#2980B9",
        "dark": "#0F3460"
    }
    
    SECONDARY_COLOR = {
        "light": "#1ABC9C",
        "dark": "#16213E"
    }
    
    ACCENT_COLOR = {
        "light": "#9B59B6",
        "dark": "#533483"
    }
    
    WARNING_COLOR = {
        "light": "#F39C12",
        "dark": "#E58E26"
    }
    
    ERROR_COLOR = {
        "light": "#E74C3C",
        "dark": "#C0392B"
    }
    
    SUCCESS_COLOR = {
        "light": "#2ECC71",
        "dark": "#27AE60"
    }
    
    def __init__(self, config):
        """تهيئة النمط"""
        self.config = config
        self.current_theme = self.config.get_theme()
        self.font_family = self.config.get_font()
        self.font_size = self.config.get_font_size()
        
        # تهيئة النمط
        self._setup_theme()
    
    def _setup_theme(self):
        """إعداد النمط"""
        # تعيين نمط customtkinter
        ctk.set_appearance_mode(self.current_theme)
        ctk.set_default_color_theme("blue")
        
        # تهيئة الخطوط
        self.fonts = {
            "title": (self.font_family, self.font_size + 8, "bold"),
            "subtitle": (self.font_family, self.font_size + 4, "bold"),
            "heading": (self.font_family, self.font_size + 2, "bold"),
            "body": (self.font_family, self.font_size, "normal"),
            "small": (self.font_family, self.font_size - 2, "normal")
        }
    
    def apply_theme_to_app(self, app):
        """تطبيق النمط على التطبيق"""
        app.configure(fg_color=self.get_color("bg_color"))
    
    def get_color(self, color_name):
        """الحصول على لون معين"""
        if self.current_theme == "light":
            colors = {
                "bg_color": self.LIGHT_BG_COLOR,
                "fg_color": self.LIGHT_FG_COLOR,
                "card_bg_color": self.LIGHT_CARD_BG_COLOR,
                "sidebar_bg_color": self.LIGHT_SIDEBAR_BG_COLOR,
                "sidebar_fg_color": self.LIGHT_SIDEBAR_FG_COLOR,
                "sidebar_hover_color": self.LIGHT_SIDEBAR_HOVER_COLOR,
                "sidebar_active_color": self.LIGHT_SIDEBAR_ACTIVE_COLOR,
                "button_bg_color": self.LIGHT_BUTTON_BG_COLOR,
                "button_hover_color": self.LIGHT_BUTTON_HOVER_COLOR,
                "button_active_color": self.LIGHT_BUTTON_ACTIVE_COLOR,
                "input_bg_color": self.LIGHT_INPUT_BG_COLOR,
                "input_fg_color": self.LIGHT_INPUT_FG_COLOR,
                "border_color": self.LIGHT_BORDER_COLOR,
                "primary_color": self.PRIMARY_COLOR["light"],
                "secondary_color": self.SECONDARY_COLOR["light"],
                "accent_color": self.ACCENT_COLOR["light"],
                "warning_color": self.WARNING_COLOR["light"],
                "error_color": self.ERROR_COLOR["light"],
                "success_color": self.SUCCESS_COLOR["light"]
            }
        else:
            colors = {
                "bg_color": self.DARK_BG_COLOR,
                "fg_color": self.DARK_FG_COLOR,
                "card_bg_color": self.DARK_CARD_BG_COLOR,
                "sidebar_bg_color": self.DARK_SIDEBAR_BG_COLOR,
                "sidebar_fg_color": self.DARK_SIDEBAR_FG_COLOR,
                "sidebar_hover_color": self.DARK_SIDEBAR_HOVER_COLOR,
                "sidebar_active_color": self.DARK_SIDEBAR_ACTIVE_COLOR,
                "button_bg_color": self.DARK_BUTTON_BG_COLOR,
                "button_hover_color": self.DARK_BUTTON_HOVER_COLOR,
                "button_active_color": self.DARK_BUTTON_ACTIVE_COLOR,
                "input_bg_color": self.DARK_INPUT_BG_COLOR,
                "input_fg_color": self.DARK_INPUT_FG_COLOR,
                "border_color": self.DARK_BORDER_COLOR,
                "primary_color": self.PRIMARY_COLOR["dark"],
                "secondary_color": self.SECONDARY_COLOR["dark"],
                "accent_color": self.ACCENT_COLOR["dark"],
                "warning_color": self.WARNING_COLOR["dark"],
                "error_color": self.ERROR_COLOR["dark"],
                "success_color": self.SUCCESS_COLOR["dark"]
            }
        
        return colors.get(color_name, self.LIGHT_BG_COLOR)
    
    def get_font(self, font_type):
        """الحصول على خط معين"""
        return self.fonts.get(font_type, self.fonts["body"])
    
    def toggle_theme(self):
        """تبديل النمط بين الفاتح والداكن"""
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        
        # تحديث النمط في الإعدادات
        self.config.set_theme(self.current_theme)
        
        # تحديث نمط customtkinter
        ctk.set_appearance_mode(self.current_theme)
        
        return self.current_theme
    
    def create_styled_frame(self, parent, **kwargs):
        """إنشاء إطار منسق"""
        default_kwargs = {
            "fg_color": self.get_color("bg_color"),
            "corner_radius": 10,
            "border_width": 0
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkFrame(parent, **default_kwargs)
    
    def create_styled_scrollable_frame(self, parent, **kwargs):
        """إنشاء إطار قابل للتمرير منسق"""
        default_kwargs = {
            "fg_color": self.get_color("bg_color"),
            "corner_radius": 10,
            "border_width": 0
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkScrollableFrame(parent, **default_kwargs)
    
    def create_styled_label(self, parent, text, **kwargs):
        """إنشاء تسمية منسقة"""
        default_kwargs = {
            "text": text,
            "font": self.get_font("body"),
            "text_color": self.get_color("fg_color")
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkLabel(parent, **default_kwargs)
    
    def create_styled_button(self, parent, text, **kwargs):
        """إنشاء زر منسق"""
        default_kwargs = {
            "text": text,
            "font": self.get_font("body"),
            "fg_color": self.get_color("button_bg_color"),
            "hover_color": self.get_color("button_hover_color"),
            "text_color": "white",
            "corner_radius": 8,
            "border_width": 0,
            "height": 36
        }
        
        # إضافة أيقونة إذا تم تحديدها
        if "icon" in kwargs:
            icon_name = kwargs.pop("icon")
            # هنا يمكن إضافة منطق لتحميل الأيقونة
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkButton(parent, **default_kwargs)
    
    def create_styled_entry(self, parent, placeholder_text, **kwargs):
        """إنشاء حقل إدخال منسق"""
        default_kwargs = {
            "placeholder_text": placeholder_text,
            "font": self.get_font("body"),
            "fg_color": self.get_color("input_bg_color"),
            "text_color": self.get_color("input_fg_color"),
            "placeholder_text_color": self.get_color("border_color"),
            "corner_radius": 8,
            "border_width": 1,
            "border_color": self.get_color("border_color"),
            "height": 36
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkEntry(parent, **default_kwargs)
    
    def create_styled_textbox(self, parent, **kwargs):
        """إنشاء مربع نص منسق"""
        default_kwargs = {
            "font": self.get_font("body"),
            "fg_color": self.get_color("input_bg_color"),
            "text_color": self.get_color("input_fg_color"),
            "corner_radius": 8,
            "border_width": 1,
            "border_color": self.get_color("border_color")
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkTextbox(parent, **default_kwargs)
    
    def create_styled_combobox(self, parent, values, **kwargs):
        """إنشاء قائمة منسدلة منسقة"""
        default_kwargs = {
            "values": values,
            "font": self.get_font("body"),
            "fg_color": self.get_color("input_bg_color"),
            "text_color": self.get_color("input_fg_color"),
            "border_color": self.get_color("border_color"),
            "button_color": self.get_color("button_bg_color"),
            "button_hover_color": self.get_color("button_hover_color"),
            "dropdown_fg_color": self.get_color("card_bg_color"),
            "dropdown_text_color": self.get_color("fg_color"),
            "dropdown_hover_color": self.get_color("sidebar_hover_color"),
            "corner_radius": 8,
            "border_width": 1,
            "dropdown_font": self.get_font("body")
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkComboBox(parent, **default_kwargs)
    
    def create_styled_switch(self, parent, text, **kwargs):
        """إنشاء مفتاح تبديل منسق"""
        default_kwargs = {
            "text": text,
            "font": self.get_font("body"),
            "fg_color": self.get_color("border_color"),
            "progress_color": self.get_color("button_bg_color"),
            "button_color": "white",
            "button_hover_color": "white",
            "text_color": self.get_color("fg_color")
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkSwitch(parent, **default_kwargs)
    
    def create_styled_radio_button(self, parent, text, variable, value, **kwargs):
        """إنشاء زر راديو منسق"""
        default_kwargs = {
            "text": text,
            "font": self.get_font("body"),
            "fg_color": self.get_color("button_bg_color"),
            "border_color": self.get_color("border_color"),
            "hover_color": self.get_color("button_hover_color"),
            "text_color": self.get_color("fg_color"),
            "variable": variable,
            "value": value
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkRadioButton(parent, **default_kwargs)
    
    def create_styled_slider(self, parent, **kwargs):
        """إنشاء شريط تمرير منسق"""
        default_kwargs = {
            "fg_color": self.get_color("border_color"),
            "progress_color": self.get_color("button_bg_color"),
            "button_color": self.get_color("button_bg_color"),
            "button_hover_color": self.get_color("button_hover_color")
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkSlider(parent, **default_kwargs)
    
    def create_styled_tabview(self, parent, **kwargs):
        """إنشاء عرض تبويب منسق"""
        default_kwargs = {
            "fg_color": self.get_color("card_bg_color"),
            "segmented_button_fg_color": self.get_color("sidebar_bg_color"),
            "segmented_button_selected_color": self.get_color("button_bg_color"),
            "segmented_button_unselected_color": self.get_color("sidebar_bg_color"),
            "segmented_button_selected_hover_color": self.get_color("button_hover_color"),
            "segmented_button_unselected_hover_color": self.get_color("sidebar_hover_color"),
            "segmented_button_text_color": self.get_color("sidebar_fg_color"),
            "segmented_button_selected_text_color": "white",
            "text_color": self.get_color("fg_color"),
            "corner_radius": 10
        }
        
        # دمج الخصائص المخصصة مع الخصائص الافتراضية
        for key, value in kwargs.items():
            default_kwargs[key] = value
        
        return ctk.CTkTabview(parent, **default_kwargs)
    
    def create_styled_sidebar_button(self, parent, text, icon, command=None):
        """إنشاء زر الشريط الجانبي المنسق"""
        # إنشاء إطار للزر
        button_frame = ctk.CTkFrame(
            parent,
            fg_color="transparent",
            corner_radius=0
        )
        
        # إنشاء الزر
        button = ctk.CTkButton(
            button_frame,
            text=text,
            font=self.get_font("body"),
            fg_color="transparent",
            hover_color=self.get_color("sidebar_hover_color"),
            text_color=self.get_color("sidebar_fg_color"),
            anchor="w",
            corner_radius=0,
            border_width=0,
            height=40,
            command=command
        )
        button.pack(fill="x", padx=0, pady=0)
        
        return button_frame, button
    
    def create_styled_card(self, parent, title):
        """إنشاء بطاقة منسقة"""
        # إنشاء إطار البطاقة
        card = self.create_styled_frame(
            parent,
            fg_color=self.get_color("card_bg_color")
        )
        
        # إنشاء عنوان البطاقة
        title_label = self.create_styled_label(
            card,
            title,
            font=self.get_font("heading")
        )
        title_label.pack(anchor="w", padx=15, pady=(15, 5))
        
        # إنشاء خط فاصل
        separator = ctk.CTkFrame(
            card,
            height=1,
            fg_color=self.get_color("border_color")
        )
        separator.pack(fill="x", padx=15, pady=(5, 0))
        
        # إنشاء إطار المحتوى
        content_frame = self.create_styled_frame(
            card,
            fg_color="transparent"
        )
        content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        return card, content_frame
    
    def create_styled_data_table(self, parent, columns, data):
        """إنشاء جدول بيانات منسق"""
        # إنشاء إطار الجدول
        table_frame = self.create_styled_frame(
            parent,
            fg_color="transparent"
        )
        
        # إنشاء إطار العناوين
        header_frame = self.create_styled_frame(
            table_frame,
            fg_color=self.get_color("sidebar_bg_color")
        )
        header_frame.pack(fill="x", padx=0, pady=(0, 1))
        
        # إنشاء عناوين الأعمدة
        for i, column in enumerate(columns):
            column_label = self.create_styled_label(
                header_frame,
                column,
                font=self.get_font("heading"),
                text_color=self.get_color("sidebar_fg_color")
            )
            column_label.grid(row=0, column=i, sticky="ew", padx=10, pady=10)
            header_frame.grid_columnconfigure(i, weight=1)
        
        # إنشاء إطار البيانات
        data_frame = self.create_styled_scrollable_frame(
            table_frame,
            fg_color="transparent"
        )
        data_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # إنشاء صفوف البيانات
        for i, row in enumerate(data):
            row_frame = self.create_styled_frame(
                data_frame,
                fg_color=self.get_color("card_bg_color") if i % 2 == 0 else self.get_color("bg_color")
            )
            row_frame.pack(fill="x", padx=0, pady=(0, 1))
            
            for j, cell in enumerate(row):
                cell_label = self.create_styled_label(
                    row_frame,
                    cell,
                    font=self.get_font("body")
                )
                cell_label.grid(row=0, column=j, sticky="ew", padx=10, pady=10)
                row_frame.grid_columnconfigure(j, weight=1)
        
        return table_frame, data_frame
    
    def create_styled_message_box(self, title, message, message_type="info"):
        """إنشاء مربع رسالة منسق"""
        # تحديد لون الرسالة بناءً على النوع
        if message_type == "error":
            color = self.get_color("error_color")
        elif message_type == "warning":
            color = self.get_color("warning_color")
        elif message_type == "success":
            color = self.get_color("success_color")
        else:  # info
            color = self.get_color("primary_color")
        
        # إنشاء نافذة الرسالة
        message_window = ctk.CTkToplevel()
        message_window.title(title)
        message_window.geometry("400x200")
        message_window.resizable(False, False)
        message_window.grab_set()  # جعل النافذة المنبثقة مركز الاهتمام
        
        # تطبيق النمط
        message_window.configure(fg_color=self.get_color("bg_color"))
        
        # إنشاء إطار الرسالة
        message_frame = self.create_styled_frame(
            message_window,
            fg_color=self.get_color("card_bg_color")
        )
        message_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # إنشاء عنوان الرسالة
        title_label = self.create_styled_label(
            message_frame,
            title,
            font=self.get_font("heading"),
            text_color=color
        )
        title_label.pack(padx=20, pady=(20, 10))
        
        # إنشاء نص الرسالة
        message_label = self.create_styled_label(
            message_frame,
            message,
            font=self.get_font("body")
        )
        message_label.pack(padx=20, pady=(0, 20))
        
        # إنشاء زر موافق
        ok_button = self.create_styled_button(
            message_frame,
            "موافق",
            fg_color=color,
            hover_color=color,
            command=message_window.destroy
        )
        ok_button.pack(pady=(0, 20))
        
        return message_window
