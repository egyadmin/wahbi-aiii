"""
مولد الرسوم البيانية لنظام إدارة المناقصات
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import customtkinter as ctk

class ChartGenerator:
    """فئة مولد الرسوم البيانية"""
    
    def __init__(self, theme):
        """تهيئة مولد الرسوم البيانية"""
        self.theme = theme
        
        # تحديد مسار مجلد الرسوم البيانية
        self.charts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "charts")
        
        # إنشاء مجلد الرسوم البيانية إذا لم يكن موجودًا
        os.makedirs(self.charts_dir, exist_ok=True)
        
        # تهيئة نمط الرسوم البيانية
        self._setup_chart_style()
    
    def _setup_chart_style(self):
        """إعداد نمط الرسوم البيانية"""
        # تعيين نمط الرسوم البيانية
        plt.style.use('ggplot')
        
        # تعيين الخط
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans', 'Bitstream Vera Sans', 'sans-serif']
        
        # تعيين حجم الخط
        plt.rcParams['font.size'] = 10
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        
        # تعيين الألوان
        if self.theme.current_theme == "light":
            plt.rcParams['figure.facecolor'] = self.theme.LIGHT_CARD_BG_COLOR
            plt.rcParams['axes.facecolor'] = self.theme.LIGHT_BG_COLOR
            plt.rcParams['axes.edgecolor'] = self.theme.LIGHT_BORDER_COLOR
            plt.rcParams['axes.labelcolor'] = self.theme.LIGHT_FG_COLOR
            plt.rcParams['xtick.color'] = self.theme.LIGHT_FG_COLOR
            plt.rcParams['ytick.color'] = self.theme.LIGHT_FG_COLOR
            plt.rcParams['text.color'] = self.theme.LIGHT_FG_COLOR
            plt.rcParams['grid.color'] = self.theme.LIGHT_BORDER_COLOR
        else:
            plt.rcParams['figure.facecolor'] = self.theme.DARK_CARD_BG_COLOR
            plt.rcParams['axes.facecolor'] = self.theme.DARK_BG_COLOR
            plt.rcParams['axes.edgecolor'] = self.theme.DARK_BORDER_COLOR
            plt.rcParams['axes.labelcolor'] = self.theme.DARK_FG_COLOR
            plt.rcParams['xtick.color'] = self.theme.DARK_FG_COLOR
            plt.rcParams['ytick.color'] = self.theme.DARK_FG_COLOR
            plt.rcParams['text.color'] = self.theme.DARK_FG_COLOR
            plt.rcParams['grid.color'] = self.theme.DARK_BORDER_COLOR
    
    def create_bar_chart(self, data, title, xlabel, ylabel):
        """إنشاء رسم بياني شريطي"""
        # إنشاء الشكل والمحاور
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # رسم الرسم البياني الشريطي
        bars = ax.bar(data['labels'], data['values'], color=self.theme.PRIMARY_COLOR[self.theme.current_theme])
        
        # إضافة القيم فوق الأشرطة
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + 0.1 * max(data['values']),
                    f'{height:,.0f}', ha='center', va='bottom')
        
        # تعيين العنوان والتسميات
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # تعيين حدود المحور y
        ax.set_ylim(0, max(data['values']) * 1.2)
        
        # إضافة الشبكة
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # تضييق الشكل
        fig.tight_layout()
        
        return fig
    
    def create_line_chart(self, data, title, xlabel, ylabel):
        """إنشاء رسم بياني خطي"""
        # إنشاء الشكل والمحاور
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # رسم الرسم البياني الخطي
        line = ax.plot(data['labels'], data['values'], marker='o', linestyle='-', linewidth=2,
                      color=self.theme.PRIMARY_COLOR[self.theme.current_theme],
                      markersize=8, markerfacecolor=self.theme.SECONDARY_COLOR[self.theme.current_theme])
        
        # إضافة القيم فوق النقاط
        for i, value in enumerate(data['values']):
            ax.text(i, value + 0.05 * max(data['values']), f'{value:,.0f}', ha='center', va='bottom')
        
        # تعيين العنوان والتسميات
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # تعيين حدود المحور y
        ax.set_ylim(0, max(data['values']) * 1.2)
        
        # إضافة الشبكة
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # تضييق الشكل
        fig.tight_layout()
        
        return fig
    
    def create_pie_chart(self, data, title):
        """إنشاء رسم بياني دائري"""
        # إنشاء الشكل والمحاور
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # تعيين الألوان
        colors = [
            self.theme.PRIMARY_COLOR[self.theme.current_theme],
            self.theme.SECONDARY_COLOR[self.theme.current_theme],
            self.theme.ACCENT_COLOR[self.theme.current_theme],
            self.theme.WARNING_COLOR[self.theme.current_theme],
            self.theme.SUCCESS_COLOR[self.theme.current_theme]
        ]
        
        # رسم الرسم البياني الدائري
        wedges, texts, autotexts = ax.pie(
            data['values'],
            labels=data['labels'],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            wedgeprops={'edgecolor': 'white', 'linewidth': 1},
            textprops={'color': self.theme.get_color('fg_color')}
        )
        
        # تعيين خصائص النص
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
        
        # تعيين العنوان
        ax.set_title(title)
        
        # جعل الرسم البياني دائريًا
        ax.axis('equal')
        
        # تضييق الشكل
        fig.tight_layout()
        
        return fig
    
    def create_stacked_bar_chart(self, data, title, xlabel, ylabel):
        """إنشاء رسم بياني شريطي متراكم"""
        # إنشاء الشكل والمحاور
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # تعيين الألوان
        colors = [
            self.theme.PRIMARY_COLOR[self.theme.current_theme],
            self.theme.SECONDARY_COLOR[self.theme.current_theme],
            self.theme.ACCENT_COLOR[self.theme.current_theme],
            self.theme.WARNING_COLOR[self.theme.current_theme],
            self.theme.SUCCESS_COLOR[self.theme.current_theme]
        ]
        
        # رسم الرسم البياني الشريطي المتراكم
        bottom = np.zeros(len(data['labels']))
        for i, category in enumerate(data['categories']):
            values = data['values'][i]
            bars = ax.bar(data['labels'], values, bottom=bottom, label=category, color=colors[i % len(colors)])
            bottom += values
        
        # تعيين العنوان والتسميات
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        
        # إضافة وسيلة إيضاح
        ax.legend()
        
        # إضافة الشبكة
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # تضييق الشكل
        fig.tight_layout()
        
        return fig
    
    def create_risk_matrix(self, data, title):
        """إنشاء مصفوفة المخاطر"""
        # إنشاء الشكل والمحاور
        fig, ax = plt.subplots(figsize=(8, 5), dpi=100)
        
        # تعيين الألوان
        colors = {
            'منخفض': self.theme.SUCCESS_COLOR[self.theme.current_theme],
            'متوسط': self.theme.WARNING_COLOR[self.theme.current_theme],
            'عالي': self.theme.ERROR_COLOR[self.theme.current_theme]
        }
        
        # تعيين قيم المحاور
        probability_values = {'منخفض': 1, 'متوسط': 2, 'عالي': 3}
        impact_values = {'منخفض': 1, 'متوسط': 2, 'عالي': 3}
        
        # رسم المصفوفة
        for risk in data['risks']:
            prob = probability_values[risk['probability']]
            impact = impact_values[risk['impact']]
            color = colors[risk['probability']] if prob > impact else colors[risk['impact']]
            ax.scatter(impact, prob, color=color, s=100, alpha=0.7)
            ax.annotate(risk['name'], (impact, prob), xytext=(5, 5), textcoords='offset points')
        
        # تعيين حدود المحاور
        ax.set_xlim(0.5, 3.5)
        ax.set_ylim(0.5, 3.5)
        
        # تعيين تسميات المحاور
        ax.set_xticks([1, 2, 3])
        ax.set_xticklabels(['منخفض', 'متوسط', 'عالي'])
        ax.set_yticks([1, 2, 3])
        ax.set_yticklabels(['منخفض', 'متوسط', 'عالي'])
        
        # تعيين العنوان والتسميات
        ax.set_title(title)
        ax.set_xlabel('التأثير')
        ax.set_ylabel('الاحتمالية')
        
        # إضافة الشبكة
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # إضافة مناطق المخاطر
        # منطقة المخاطر المنخفضة (أخضر)
        ax.add_patch(plt.Rectangle((0.5, 0.5), 1, 1, fill=True, color=self.theme.SUCCESS_COLOR[self.theme.current_theme], alpha=0.1))
        # منطقة المخاطر المتوسطة (أصفر)
        ax.add_patch(plt.Rectangle((1.5, 0.5), 1, 1, fill=True, color=self.theme.WARNING_COLOR[self.theme.current_theme], alpha=0.1))
        ax.add_patch(plt.Rectangle((0.5, 1.5), 1, 1, fill=True, color=self.theme.WARNING_COLOR[self.theme.current_theme], alpha=0.1))
        # منطقة المخاطر العالية (أحمر)
        ax.add_patch(plt.Rectangle((2.5, 0.5), 1, 3, fill=True, color=self.theme.ERROR_COLOR[self.theme.current_theme], alpha=0.1))
        ax.add_patch(plt.Rectangle((0.5, 2.5), 2, 1, fill=True, color=self.theme.ERROR_COLOR[self.theme.current_theme], alpha=0.1))
        ax.add_patch(plt.Rectangle((1.5, 1.5), 1, 1, fill=True, color=self.theme.ERROR_COLOR[self.theme.current_theme], alpha=0.1))
        
        # تضييق الشكل
        fig.tight_layout()
        
        return fig
    
    def embed_chart_in_frame(self, parent, fig):
        """تضمين الرسم البياني في إطار"""
        # إنشاء إطار للرسم البياني
        chart_frame = ctk.CTkFrame(parent, fg_color="transparent")
        
        # تضمين الرسم البياني في الإطار
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        return chart_frame
    
    def save_chart(self, fig, name):
        """حفظ الرسم البياني"""
        # تحديد مسار الملف
        file_path = os.path.join(self.charts_dir, f"{name}.png")
        
        # حفظ الرسم البياني
        fig.savefig(file_path, dpi=100, bbox_inches='tight')
        
        return file_path
