"""
مولد الأيقونات لنظام إدارة المناقصات
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

class IconGenerator:
    """فئة مولد الأيقونات"""
    
    def __init__(self):
        """تهيئة مولد الأيقونات"""
        # تحديد مسار مجلد الأيقونات
        self.icons_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "icons")
        
        # إنشاء مجلد الأيقونات إذا لم يكن موجودًا
        os.makedirs(self.icons_dir, exist_ok=True)
        
        # تحديد حجم الأيقونة الافتراضي
        self.icon_size = (64, 64)
        
        # تحديد الألوان الافتراضية
        self.colors = {
            "primary": "#2980B9",
            "secondary": "#1ABC9C",
            "accent": "#9B59B6",
            "warning": "#F39C12",
            "error": "#E74C3C",
            "success": "#2ECC71",
            "white": "#FFFFFF",
            "black": "#333333",
            "gray": "#95A5A6"
        }
    
    def generate_icon(self, name, color=None, background_color=None, size=None):
        """توليد أيقونة"""
        # تحديد الألوان
        if color is None:
            color = self.colors["primary"]
        
        if background_color is None:
            background_color = self.colors["white"]
        
        # تحديد الحجم
        if size is None:
            size = self.icon_size
        
        # إنشاء صورة جديدة
        icon = Image.new("RGBA", size, background_color)
        draw = ImageDraw.Draw(icon)
        
        # رسم الأيقونة بناءً على الاسم
        if name == "dashboard":
            self._draw_dashboard_icon(draw, size, color)
        elif name == "projects":
            self._draw_projects_icon(draw, size, color)
        elif name == "documents":
            self._draw_documents_icon(draw, size, color)
        elif name == "pricing":
            self._draw_pricing_icon(draw, size, color)
        elif name == "resources":
            self._draw_resources_icon(draw, size, color)
        elif name == "risk":
            self._draw_risk_icon(draw, size, color)
        elif name == "reports":
            self._draw_reports_icon(draw, size, color)
        elif name == "ai":
            self._draw_ai_icon(draw, size, color)
        elif name == "settings":
            self._draw_settings_icon(draw, size, color)
        elif name == "logout":
            self._draw_logout_icon(draw, size, color)
        elif name == "search":
            self._draw_search_icon(draw, size, color)
        elif name == "add":
            self._draw_add_icon(draw, size, color)
        elif name == "upload":
            self._draw_upload_icon(draw, size, color)
        elif name == "import":
            self._draw_import_icon(draw, size, color)
        elif name == "export":
            self._draw_export_icon(draw, size, color)
        elif name == "save":
            self._draw_save_icon(draw, size, color)
        else:
            # أيقونة افتراضية
            self._draw_default_icon(draw, size, color)
        
        # حفظ الأيقونة
        icon_path = os.path.join(self.icons_dir, f"{name}.png")
        icon.save(icon_path)
        
        return icon_path
    
    def _draw_dashboard_icon(self, draw, size, color):
        """رسم أيقونة لوحة التحكم"""
        width, height = size
        padding = width // 8
        
        # رسم المربعات الأربعة
        box_size = (width - 3 * padding) // 2
        
        # المربع العلوي الأيسر
        draw.rectangle(
            [(padding, padding), (padding + box_size, padding + box_size)],
            fill=color
        )
        
        # المربع العلوي الأيمن
        draw.rectangle(
            [(2 * padding + box_size, padding), (2 * padding + 2 * box_size, padding + box_size)],
            fill=color
        )
        
        # المربع السفلي الأيسر
        draw.rectangle(
            [(padding, 2 * padding + box_size), (padding + box_size, 2 * padding + 2 * box_size)],
            fill=color
        )
        
        # المربع السفلي الأيمن
        draw.rectangle(
            [(2 * padding + box_size, 2 * padding + box_size), (2 * padding + 2 * box_size, 2 * padding + 2 * box_size)],
            fill=color
        )
    
    def _draw_projects_icon(self, draw, size, color):
        """رسم أيقونة المشاريع"""
        width, height = size
        padding = width // 8
        
        # رسم مجلد
        folder_points = [
            (padding, height // 3),
            (width // 3, height // 3),
            (width // 2, padding),
            (width - padding, padding),
            (width - padding, height - padding),
            (padding, height - padding)
        ]
        draw.polygon(folder_points, fill=color)
    
    def _draw_documents_icon(self, draw, size, color):
        """رسم أيقونة المستندات"""
        width, height = size
        padding = width // 8
        
        # رسم ورقة
        draw.rectangle(
            [(padding, padding), (width - padding, height - padding)],
            fill=color
        )
        
        # رسم خطوط النص
        line_padding = height // 8
        line_height = height // 20
        for i in range(4):
            y = padding + line_padding + i * (line_height + line_padding)
            draw.rectangle(
                [(padding * 2, y), (width - padding * 2, y + line_height)],
                fill=self.colors["white"]
            )
    
    def _draw_pricing_icon(self, draw, size, color):
        """رسم أيقونة التسعير"""
        width, height = size
        padding = width // 8
        
        # رسم علامة الدولار
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 3
        
        # رسم دائرة
        draw.ellipse(
            [(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)],
            fill=color
        )
        
        # رسم علامة الدولار
        line_width = radius // 4
        draw.rectangle(
            [(center_x - line_width // 2, center_y - radius * 2 // 3), (center_x + line_width // 2, center_y + radius * 2 // 3)],
            fill=self.colors["white"]
        )
        draw.rectangle(
            [(center_x - radius * 2 // 3, center_y - line_width // 2), (center_x + radius * 2 // 3, center_y + line_width // 2)],
            fill=self.colors["white"]
        )
    
    def _draw_resources_icon(self, draw, size, color):
        """رسم أيقونة الموارد"""
        width, height = size
        padding = width // 8
        
        # رسم ثلاثة أشخاص
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 10
        
        # الشخص الأول (في الوسط)
        head_center_y = center_y - radius * 2
        draw.ellipse(
            [(center_x - radius, head_center_y - radius), (center_x + radius, head_center_y + radius)],
            fill=color
        )
        draw.polygon(
            [
                (center_x, head_center_y + radius),
                (center_x - radius * 2, center_y + radius * 3),
                (center_x + radius * 2, center_y + radius * 3)
            ],
            fill=color
        )
        
        # الشخص الثاني (على اليسار)
        left_center_x = center_x - radius * 4
        head_center_y = center_y - radius * 2
        draw.ellipse(
            [(left_center_x - radius, head_center_y - radius), (left_center_x + radius, head_center_y + radius)],
            fill=color
        )
        draw.polygon(
            [
                (left_center_x, head_center_y + radius),
                (left_center_x - radius * 2, center_y + radius * 3),
                (left_center_x + radius * 2, center_y + radius * 3)
            ],
            fill=color
        )
        
        # الشخص الثالث (على اليمين)
        right_center_x = center_x + radius * 4
        head_center_y = center_y - radius * 2
        draw.ellipse(
            [(right_center_x - radius, head_center_y - radius), (right_center_x + radius, head_center_y + radius)],
            fill=color
        )
        draw.polygon(
            [
                (right_center_x, head_center_y + radius),
                (right_center_x - radius * 2, center_y + radius * 3),
                (right_center_x + radius * 2, center_y + radius * 3)
            ],
            fill=color
        )
    
    def _draw_risk_icon(self, draw, size, color):
        """رسم أيقونة المخاطر"""
        width, height = size
        padding = width // 8
        
        # رسم علامة تحذير (مثلث)
        draw.polygon(
            [
                (width // 2, padding),
                (padding, height - padding),
                (width - padding, height - padding)
            ],
            fill=color
        )
        
        # رسم علامة التعجب
        exclamation_width = width // 10
        exclamation_height = height // 3
        center_x = width // 2
        center_y = height // 2
        
        # الجزء العلوي من علامة التعجب
        draw.rectangle(
            [
                (center_x - exclamation_width // 2, center_y - exclamation_height),
                (center_x + exclamation_width // 2, center_y)
            ],
            fill=self.colors["white"]
        )
        
        # النقطة السفلية من علامة التعجب
        dot_radius = exclamation_width
        draw.ellipse(
            [
                (center_x - dot_radius // 2, center_y + exclamation_height // 4),
                (center_x + dot_radius // 2, center_y + exclamation_height // 4 + dot_radius)
            ],
            fill=self.colors["white"]
        )
    
    def _draw_reports_icon(self, draw, size, color):
        """رسم أيقونة التقارير"""
        width, height = size
        padding = width // 8
        
        # رسم ورقة
        draw.rectangle(
            [(padding, padding), (width - padding, height - padding)],
            fill=color
        )
        
        # رسم رسم بياني
        chart_padding = width // 6
        chart_width = width - 2 * chart_padding
        chart_height = height // 2
        chart_bottom = height - chart_padding
        
        # رسم الأعمدة
        bar_width = chart_width // 5
        bar_spacing = bar_width // 2
        
        for i in range(4):
            bar_height = (i + 1) * chart_height // 4
            bar_x = chart_padding + i * (bar_width + bar_spacing)
            bar_y = chart_bottom - bar_height
            
            draw.rectangle(
                [(bar_x, bar_y), (bar_x + bar_width, chart_bottom)],
                fill=self.colors["white"]
            )
    
    def _draw_ai_icon(self, draw, size, color):
        """رسم أيقونة الذكاء الاصطناعي"""
        width, height = size
        padding = width // 8
        
        # رسم دماغ (مجرد تمثيل مبسط)
        center_x = width // 2
        center_y = height // 2
        brain_width = width - 2 * padding
        brain_height = height - 2 * padding
        
        # رسم الجزء الخارجي من الدماغ
        draw.ellipse(
            [(center_x - brain_width // 2, center_y - brain_height // 2), (center_x + brain_width // 2, center_y + brain_height // 2)],
            fill=color
        )
        
        # رسم خطوط الدماغ
        line_width = brain_width // 10
        line_spacing = brain_width // 8
        
        for i in range(-2, 3):
            y = center_y + i * line_spacing
            draw.line(
                [(center_x - brain_width // 3, y), (center_x + brain_width // 3, y)],
                fill=self.colors["white"],
                width=line_width
            )
    
    def _draw_settings_icon(self, draw, size, color):
        """رسم أيقونة الإعدادات"""
        width, height = size
        padding = width // 8
        
        # رسم ترس
        center_x = width // 2
        center_y = height // 2
        outer_radius = min(width, height) // 2 - padding
        inner_radius = outer_radius * 2 // 3
        
        # رسم الدائرة الداخلية
        draw.ellipse(
            [(center_x - inner_radius, center_y - inner_radius), (center_x + inner_radius, center_y + inner_radius)],
            fill=color
        )
        
        # رسم الأسنان
        num_teeth = 8
        tooth_width = outer_radius - inner_radius
        
        for i in range(num_teeth):
            angle = 2 * math.pi * i / num_teeth
            tooth_center_x = center_x + (inner_radius + tooth_width // 2) * math.cos(angle)
            tooth_center_y = center_y + (inner_radius + tooth_width // 2) * math.sin(angle)
            
            draw.ellipse(
                [
                    (tooth_center_x - tooth_width // 2, tooth_center_y - tooth_width // 2),
                    (tooth_center_x + tooth_width // 2, tooth_center_y + tooth_width // 2)
                ],
                fill=color
            )
    
    def _draw_logout_icon(self, draw, size, color):
        """رسم أيقونة تسجيل الخروج"""
        width, height = size
        padding = width // 8
        
        # رسم سهم الخروج
        arrow_width = width - 2 * padding
        arrow_height = height - 2 * padding
        
        # رسم المستطيل الرئيسي
        draw.rectangle(
            [(padding, padding), (width // 2, height - padding)],
            fill=color
        )
        
        # رسم السهم
        arrow_points = [
            (width // 2, height // 3),
            (width - padding, height // 2),
            (width // 2, height * 2 // 3),
            (width // 2, height // 2 + height // 8),
            (width // 2 + width // 4, height // 2 + height // 8),
            (width // 2 + width // 4, height // 2 - height // 8),
            (width // 2, height // 2 - height // 8)
        ]
        draw.polygon(arrow_points, fill=color)
    
    def _draw_search_icon(self, draw, size, color):
        """رسم أيقونة البحث"""
        width, height = size
        padding = width // 8
        
        # رسم دائرة البحث
        center_x = width // 2 - padding
        center_y = height // 2 - padding
        radius = min(width, height) // 3
        
        draw.ellipse(
            [(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)],
            outline=color,
            width=radius // 3
        )
        
        # رسم مقبض البحث
        handle_width = radius // 3
        handle_length = radius
        handle_angle = math.pi / 4  # 45 درجة
        
        handle_start_x = center_x + radius * math.cos(handle_angle)
        handle_start_y = center_y + radius * math.sin(handle_angle)
        handle_end_x = handle_start_x + handle_length * math.cos(handle_angle)
        handle_end_y = handle_start_y + handle_length * math.sin(handle_angle)
        
        draw.line(
            [(handle_start_x, handle_start_y), (handle_end_x, handle_end_y)],
            fill=color,
            width=handle_width
        )
    
    def _draw_add_icon(self, draw, size, color):
        """رسم أيقونة الإضافة"""
        width, height = size
        padding = width // 8
        
        # رسم علامة الزائد
        center_x = width // 2
        center_y = height // 2
        line_length = min(width, height) - 2 * padding
        line_width = line_length // 5
        
        # الخط الأفقي
        draw.rectangle(
            [
                (center_x - line_length // 2, center_y - line_width // 2),
                (center_x + line_length // 2, center_y + line_width // 2)
            ],
            fill=color
        )
        
        # الخط الرأسي
        draw.rectangle(
            [
                (center_x - line_width // 2, center_y - line_length // 2),
                (center_x + line_width // 2, center_y + line_length // 2)
            ],
            fill=color
        )
    
    def _draw_upload_icon(self, draw, size, color):
        """رسم أيقونة التحميل"""
        width, height = size
        padding = width // 8
        
        # رسم سهم لأعلى
        center_x = width // 2
        arrow_width = width // 3
        arrow_height = height // 2
        
        # رسم السهم
        arrow_points = [
            (center_x, padding),
            (center_x + arrow_width, padding + arrow_height),
            (center_x + arrow_width // 2, padding + arrow_height),
            (center_x + arrow_width // 2, height - padding),
            (center_x - arrow_width // 2, height - padding),
            (center_x - arrow_width // 2, padding + arrow_height),
            (center_x - arrow_width, padding + arrow_height)
        ]
        draw.polygon(arrow_points, fill=color)
    
    def _draw_import_icon(self, draw, size, color):
        """رسم أيقونة الاستيراد"""
        width, height = size
        padding = width // 8
        
        # رسم سهم للداخل
        center_y = height // 2
        arrow_width = width // 2
        arrow_height = height // 3
        
        # رسم المستطيل
        draw.rectangle(
            [(width - padding - arrow_width // 2, padding), (width - padding, height - padding)],
            fill=color
        )
        
        # رسم السهم
        arrow_points = [
            (padding, center_y),
            (padding + arrow_width, center_y - arrow_height // 2),
            (padding + arrow_width, center_y - arrow_height // 4),
            (width - padding - arrow_width // 2, center_y - arrow_height // 4),
            (width - padding - arrow_width // 2, center_y + arrow_height // 4),
            (padding + arrow_width, center_y + arrow_height // 4),
            (padding + arrow_width, center_y + arrow_height // 2)
        ]
        draw.polygon(arrow_points, fill=color)
    
    def _draw_export_icon(self, draw, size, color):
        """رسم أيقونة التصدير"""
        width, height = size
        padding = width // 8
        
        # رسم سهم للخارج
        center_y = height // 2
        arrow_width = width // 2
        arrow_height = height // 3
        
        # رسم المستطيل
        draw.rectangle(
            [(padding, padding), (padding + arrow_width // 2, height - padding)],
            fill=color
        )
        
        # رسم السهم
        arrow_points = [
            (width - padding, center_y),
            (width - padding - arrow_width, center_y - arrow_height // 2),
            (width - padding - arrow_width, center_y - arrow_height // 4),
            (padding + arrow_width // 2, center_y - arrow_height // 4),
            (padding + arrow_width // 2, center_y + arrow_height // 4),
            (width - padding - arrow_width, center_y + arrow_height // 4),
            (width - padding - arrow_width, center_y + arrow_height // 2)
        ]
        draw.polygon(arrow_points, fill=color)
    
    def _draw_save_icon(self, draw, size, color):
        """رسم أيقونة الحفظ"""
        width, height = size
        padding = width // 8
        
        # رسم أيقونة القرص
        draw.rectangle(
            [(padding, padding), (width - padding, height - padding)],
            fill=color
        )
        
        # رسم الشريط العلوي
        draw.rectangle(
            [(padding * 2, padding * 2), (width - padding * 2, padding * 4)],
            fill=self.colors["white"]
        )
        
        # رسم المستطيل الداخلي
        draw.rectangle(
            [(width // 3, height // 2), (width * 2 // 3, height - padding * 2)],
            fill=self.colors["white"]
        )
    
    def _draw_default_icon(self, draw, size, color):
        """رسم أيقونة افتراضية"""
        width, height = size
        padding = width // 8
        
        # رسم دائرة
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 2 - padding
        
        draw.ellipse(
            [(center_x - radius, center_y - radius), (center_x + radius, center_y + radius)],
            fill=color
        )
    
    def generate_default_icons(self):
        """توليد الأيقونات الافتراضية"""
        icons = [
            "dashboard",
            "projects",
            "documents",
            "pricing",
            "resources",
            "risk",
            "reports",
            "ai",
            "settings",
            "logout",
            "search",
            "add",
            "upload",
            "import",
            "export",
            "save"
        ]
        
        for icon in icons:
            self.generate_icon(icon)
