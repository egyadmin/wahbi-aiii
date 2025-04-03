"""
ملف الإعدادات لنظام إدارة المناقصات
"""

import os
import json
from pathlib import Path

class AppConfig:
    """فئة إعدادات التطبيق"""
    
    def __init__(self):
        """تهيئة الإعدادات"""
        # المسارات الأساسية
        self.app_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.app_dir, "assets")
        self.data_dir = os.path.join(self.app_dir, "data")
        
        # إنشاء المجلدات إذا لم تكن موجودة
        Path(self.assets_dir).mkdir(parents=True, exist_ok=True)
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
        
        # مسارات الأصول
        self.icons_dir = os.path.join(self.assets_dir, "icons")
        self.images_dir = os.path.join(self.assets_dir, "images")
        self.fonts_dir = os.path.join(self.assets_dir, "fonts")
        
        # إنشاء مجلدات الأصول إذا لم تكن موجودة
        Path(self.icons_dir).mkdir(parents=True, exist_ok=True)
        Path(self.images_dir).mkdir(parents=True, exist_ok=True)
        Path(self.fonts_dir).mkdir(parents=True, exist_ok=True)
        
        # مسارات البيانات
        self.database_file = os.path.join(self.data_dir, "database.db")
        self.settings_file = os.path.join(self.data_dir, "settings.json")
        self.charts_dir = os.path.join(self.data_dir, "charts")
        
        # إنشاء مجلد الرسوم البيانية إذا لم يكن موجودًا
        Path(self.charts_dir).mkdir(parents=True, exist_ok=True)
        
        # تحميل الإعدادات
        self.settings = self._load_settings()
    
    def _load_settings(self):
        """تحميل الإعدادات من ملف JSON"""
        default_settings = {
            "app": {
                "name": "نظام إدارة المناقصات",
                "version": "1.0.0",
                "language": "ar",
                "theme": "light",
                "font": "Cairo",
                "font_size": 12
            },
            "database": {
                "type": "sqlite",
                "path": self.database_file
            },
            "ui": {
                "window_width": 1200,
                "window_height": 800,
                "sidebar_width": 250
            },
            "notifications": {
                "enabled": True,
                "email_enabled": True,
                "email_server": "smtp.example.com",
                "email_port": 587,
                "email_username": "",
                "email_password": ""
            },
            "reports": {
                "default_format": "pdf",
                "default_path": os.path.join(self.data_dir, "reports")
            },
            "backup": {
                "auto_backup": True,
                "backup_frequency": "weekly",
                "backup_path": os.path.join(self.data_dir, "backups"),
                "max_backups": 10
            }
        }
        
        # إذا كان ملف الإعدادات موجودًا، قم بتحميله
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                
                # دمج الإعدادات المحملة مع الإعدادات الافتراضية
                self._merge_settings(default_settings, settings)
                return default_settings
            except Exception as e:
                print(f"خطأ في تحميل الإعدادات: {str(e)}")
                return default_settings
        else:
            # إنشاء ملف الإعدادات الافتراضية
            self._save_settings(default_settings)
            return default_settings
    
    def _merge_settings(self, default_settings, loaded_settings):
        """دمج الإعدادات المحملة مع الإعدادات الافتراضية"""
        for key, value in loaded_settings.items():
            if key in default_settings:
                if isinstance(value, dict) and isinstance(default_settings[key], dict):
                    self._merge_settings(default_settings[key], value)
                else:
                    default_settings[key] = value
    
    def _save_settings(self, settings=None):
        """حفظ الإعدادات إلى ملف JSON"""
        if settings is None:
            settings = self.settings
        
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"خطأ في حفظ الإعدادات: {str(e)}")
            return False
    
    def get_setting(self, section, key, default=None):
        """الحصول على قيمة إعداد معين"""
        try:
            return self.settings[section][key]
        except KeyError:
            return default
    
    def set_setting(self, section, key, value):
        """تعيين قيمة إعداد معين"""
        if section not in self.settings:
            self.settings[section] = {}
        
        self.settings[section][key] = value
        self._save_settings()
    
    def get_app_name(self):
        """الحصول على اسم التطبيق"""
        return self.get_setting("app", "name", "نظام إدارة المناقصات")
    
    def get_app_version(self):
        """الحصول على إصدار التطبيق"""
        return self.get_setting("app", "version", "1.0.0")
    
    def get_language(self):
        """الحصول على لغة التطبيق"""
        return self.get_setting("app", "language", "ar")
    
    def set_language(self, language):
        """تعيين لغة التطبيق"""
        self.set_setting("app", "language", language)
    
    def get_theme(self):
        """الحصول على نمط التطبيق"""
        return self.get_setting("app", "theme", "light")
    
    def set_theme(self, theme):
        """تعيين نمط التطبيق"""
        self.set_setting("app", "theme", theme)
    
    def get_font(self):
        """الحصول على خط التطبيق"""
        return self.get_setting("app", "font", "Cairo")
    
    def set_font(self, font):
        """تعيين خط التطبيق"""
        self.set_setting("app", "font", font)
    
    def get_font_size(self):
        """الحصول على حجم خط التطبيق"""
        return self.get_setting("app", "font_size", 12)
    
    def set_font_size(self, font_size):
        """تعيين حجم خط التطبيق"""
        self.set_setting("app", "font_size", font_size)
    
    def get_window_size(self):
        """الحصول على حجم نافذة التطبيق"""
        width = self.get_setting("ui", "window_width", 1200)
        height = self.get_setting("ui", "window_height", 800)
        return (width, height)
    
    def set_window_size(self, width, height):
        """تعيين حجم نافذة التطبيق"""
        self.set_setting("ui", "window_width", width)
        self.set_setting("ui", "window_height", height)
    
    def get_sidebar_width(self):
        """الحصول على عرض الشريط الجانبي"""
        return self.get_setting("ui", "sidebar_width", 250)
    
    def set_sidebar_width(self, width):
        """تعيين عرض الشريط الجانبي"""
        self.set_setting("ui", "sidebar_width", width)
    
    def get_database_config(self):
        """الحصول على إعدادات قاعدة البيانات"""
        return self.settings.get("database", {
            "type": "sqlite",
            "path": self.database_file
        })
    
    def get_notifications_config(self):
        """الحصول على إعدادات الإشعارات"""
        return self.settings.get("notifications", {
            "enabled": True,
            "email_enabled": True,
            "email_server": "smtp.example.com",
            "email_port": 587,
            "email_username": "",
            "email_password": ""
        })
    
    def get_reports_config(self):
        """الحصول على إعدادات التقارير"""
        return self.settings.get("reports", {
            "default_format": "pdf",
            "default_path": os.path.join(self.data_dir, "reports")
        })
    
    def get_backup_config(self):
        """الحصول على إعدادات النسخ الاحتياطي"""
        return self.settings.get("backup", {
            "auto_backup": True,
            "backup_frequency": "weekly",
            "backup_path": os.path.join(self.data_dir, "backups"),
            "max_backups": 10
        })
