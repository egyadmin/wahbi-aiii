"""
محلل الأسعار لنظام إدارة المناقصات
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from scipy import stats
import logging

logger = logging.getLogger('tender_system.pricing.analyzer')

class PriceAnalyzer:
    """فئة تحليل الأسعار"""
    
    def __init__(self, db_connector):
        """تهيئة محلل الأسعار"""
        self.db = db_connector
        self.charts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "charts")
        
        # إنشاء مجلد الرسوم البيانية إذا لم يكن موجودًا
        os.makedirs(self.charts_dir, exist_ok=True)
    
    def get_price_history(self, item_id, start_date=None, end_date=None):
        """الحصول على تاريخ الأسعار لبند معين
        
        المعلمات:
            item_id (int): معرف البند
            start_date (str, optional): تاريخ البداية بتنسيق 'YYYY-MM-DD'
            end_date (str, optional): تاريخ النهاية بتنسيق 'YYYY-MM-DD'
            
        العائد:
            pandas.DataFrame: إطار بيانات يحتوي على تاريخ الأسعار
        """
        try:
            query = """
                SELECT 
                    pih.id,
                    pih.price,
                    pih.price_date,
                    pih.price_source,
                    pih.notes,
                    pib.code,
                    pib.name,
                    mu.name as unit_name,
                    mu.symbol as unit_symbol
                FROM 
                    pricing_items_history pih
                JOIN 
                    pricing_items_base pib ON pih.base_item_id = pib.id
                LEFT JOIN 
                    measurement_units mu ON pib.unit_id = mu.id
                WHERE 
                    pih.base_item_id = ?
            """
            
            params = [item_id]
            
            if start_date:
                query += " AND pih.price_date >= ?"
                params.append(start_date)
            
            if end_date:
                query += " AND pih.price_date <= ?"
                params.append(end_date)
            
            query += " ORDER BY pih.price_date ASC"
            
            results = self.db.fetch_all(query, params)
            
            if not results:
                logger.warning(f"لا توجد بيانات تاريخية للسعر للبند رقم {item_id}")
                return pd.DataFrame()
            
            # تحويل النتائج إلى إطار بيانات
            df = pd.DataFrame(results, columns=[
                'id', 'price', 'price_date', 'price_source', 'notes', 
                'code', 'name', 'unit_name', 'unit_symbol'
            ])
            
            # تحويل تاريخ السعر إلى نوع datetime
            df['price_date'] = pd.to_datetime(df['price_date'])
            
            return df
            
        except Exception as e:
            logger.error(f"خطأ في الحصول على تاريخ الأسعار: {str(e)}")
            return pd.DataFrame()
    
    def analyze_price_trends(self, item_id, start_date=None, end_date=None):
        """تحليل اتجاهات الأسعار
        
        المعلمات:
            item_id (int): معرف البند
            start_date (str, optional): تاريخ البداية بتنسيق 'YYYY-MM-DD'
            end_date (str, optional): تاريخ النهاية بتنسيق 'YYYY-MM-DD'
            
        العائد:
            dict: قاموس يحتوي على نتائج تحليل اتجاهات الأسعار
        """
        try:
            # الحصول على تاريخ الأسعار
            df = self.get_price_history(item_id, start_date, end_date)
            
            if df.empty:
                return {
                    'status': 'error',
                    'message': 'لا توجد بيانات كافية لتحليل اتجاهات الأسعار'
                }
            
            # حساب الإحصاءات الأساسية
            stats_data = {
                'min_price': df['price'].min(),
                'max_price': df['price'].max(),
                'avg_price': df['price'].mean(),
                'median_price': df['price'].median(),
                'std_dev': df['price'].std(),
                'price_range': df['price'].max() - df['price'].min(),
                'count': len(df),
                'start_date': df['price_date'].min().strftime('%Y-%m-%d'),
                'end_date': df['price_date'].max().strftime('%Y-%m-%d'),
                'duration_days': (df['price_date'].max() - df['price_date'].min()).days,
                'item_name': df['name'].iloc[0],
                'item_code': df['code'].iloc[0],
                'unit': df['unit_symbol'].iloc[0] if not pd.isna(df['unit_symbol'].iloc[0]) else ''
            }
            
            # حساب التغير المطلق والنسبي
            if len(df) >= 2:
                first_price = df['price'].iloc[0]
                last_price = df['price'].iloc[-1]
                
                stats_data['absolute_change'] = last_price - first_price
                stats_data['percentage_change'] = ((last_price - first_price) / first_price) * 100
                
                # حساب معدل التغير السنوي
                years = stats_data['duration_days'] / 365.0
                if years > 0:
                    stats_data['annual_change_rate'] = (((last_price / first_price) ** (1 / years)) - 1) * 100
                else:
                    stats_data['annual_change_rate'] = 0
            else:
                stats_data['absolute_change'] = 0
                stats_data['percentage_change'] = 0
                stats_data['annual_change_rate'] = 0
            
            # تحليل الاتجاه باستخدام الانحدار الخطي
            if len(df) >= 3:
                # إنشاء متغير مستقل (الأيام منذ أول تاريخ)
                df['days'] = (df['price_date'] - df['price_date'].min()).dt.days
                
                # حساب الانحدار الخطي
                slope, intercept, r_value, p_value, std_err = stats.linregress(df['days'], df['price'])
                
                stats_data['trend_slope'] = slope
                stats_data['trend_intercept'] = intercept
                stats_data['trend_r_squared'] = r_value ** 2
                stats_data['trend_p_value'] = p_value
                stats_data['trend_std_err'] = std_err
                
                # تحديد اتجاه السعر
                if p_value < 0.05:  # إذا كان الاتجاه ذو دلالة إحصائية
                    if slope > 0:
                        stats_data['trend_direction'] = 'upward'
                        stats_data['trend_description'] = 'اتجاه تصاعدي'
                    elif slope < 0:
                        stats_data['trend_direction'] = 'downward'
                        stats_data['trend_description'] = 'اتجاه تنازلي'
                    else:
                        stats_data['trend_direction'] = 'stable'
                        stats_data['trend_description'] = 'مستقر'
                else:
                    stats_data['trend_direction'] = 'no_significant_trend'
                    stats_data['trend_description'] = 'لا يوجد اتجاه واضح'
                
                # حساب التقلب (معامل الاختلاف)
                stats_data['volatility'] = (df['price'].std() / df['price'].mean()) * 100
                
                # تصنيف التقلب
                if stats_data['volatility'] < 5:
                    stats_data['volatility_level'] = 'low'
                    stats_data['volatility_description'] = 'منخفض'
                elif stats_data['volatility'] < 15:
                    stats_data['volatility_level'] = 'medium'
                    stats_data['volatility_description'] = 'متوسط'
                else:
                    stats_data['volatility_level'] = 'high'
                    stats_data['volatility_description'] = 'مرتفع'
            else:
                stats_data['trend_direction'] = 'insufficient_data'
                stats_data['trend_description'] = 'بيانات غير كافية'
                stats_data['volatility'] = 0
                stats_data['volatility_level'] = 'unknown'
                stats_data['volatility_description'] = 'غير معروف'
            
            # إنشاء رسم بياني للاتجاه
            chart_path = self._create_trend_chart(df, stats_data, item_id)
            stats_data['chart_path'] = chart_path
            
            return {
                'status': 'success',
                'data': stats_data
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل اتجاهات الأسعار: {str(e)}")
            return {
                'status': 'error',
                'message': f'حدث خطأ أثناء تحليل اتجاهات الأسعار: {str(e)}'
            }
    
    def _create_trend_chart(self, df, stats_data, item_id):
        """إنشاء رسم بياني للاتجاه
        
        المعلمات:
            df (pandas.DataFrame): إطار البيانات
            stats_data (dict): بيانات الإحصاءات
            item_id (int): معرف البند
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني جديد
            plt.figure(figsize=(10, 6))
            
            # رسم نقاط البيانات
            plt.scatter(df['price_date'], df['price'], color='blue', alpha=0.6, label='أسعار فعلية')
            
            # رسم خط الاتجاه إذا كان هناك بيانات كافية
            if len(df) >= 3 and 'trend_slope' in stats_data:
                # إنشاء خط الاتجاه
                x_trend = pd.date_range(start=df['price_date'].min(), end=df['price_date'].max(), periods=100)
                days_trend = [(date - df['price_date'].min()).days for date in x_trend]
                y_trend = stats_data['trend_slope'] * np.array(days_trend) + stats_data['trend_intercept']
                
                # رسم خط الاتجاه
                plt.plot(x_trend, y_trend, color='red', linestyle='--', label='خط الاتجاه')
            
            # رسم خط متوسط السعر
            plt.axhline(y=stats_data['avg_price'], color='green', linestyle='-', alpha=0.5, label='متوسط السعر')
            
            # إضافة عنوان ومحاور
            plt.title(f"تحليل اتجاه السعر - {stats_data['item_name']} ({stats_data['item_code']})")
            plt.xlabel('التاريخ')
            plt.ylabel(f"السعر ({stats_data['unit']})")
            
            # إضافة شبكة
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # إضافة وسيلة إيضاح
            plt.legend()
            
            # تنسيق التاريخ على المحور السيني
            plt.gcf().autofmt_xdate()
            
            # إضافة معلومات إحصائية
            info_text = (
                f"التغير: {stats_data['percentage_change']:.2f}%\n"
                f"التقلب: {stats_data['volatility']:.2f}%\n"
            )
            
            if 'trend_r_squared' in stats_data:
                info_text += f"R²: {stats_data['trend_r_squared']:.3f}"
            
            plt.annotate(info_text, xy=(0.02, 0.95), xycoords='axes fraction', 
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
            
            # حفظ الرسم البياني
            chart_filename = f"price_trend_{item_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني للاتجاه: {str(e)}")
            return None
    
    def compare_prices(self, items, date=None):
        """مقارنة الأسعار بين عدة بنود
        
        المعلمات:
            items (list): قائمة بمعرفات البنود
            date (str, optional): تاريخ المقارنة بتنسيق 'YYYY-MM-DD'
            
        العائد:
            dict: قاموس يحتوي على نتائج مقارنة الأسعار
        """
        try:
            if not items:
                return {
                    'status': 'error',
                    'message': 'لم يتم تحديد أي بنود للمقارنة'
                }
            
            comparison_data = []
            
            for item_id in items:
                # الحصول على معلومات البند الأساسية
                item_query = """
                    SELECT 
                        id, code, name, description, 
                        (SELECT name FROM measurement_units WHERE id = unit_id) as unit_name,
                        (SELECT symbol FROM measurement_units WHERE id = unit_id) as unit_symbol,
                        base_price, last_updated_date
                    FROM 
                        pricing_items_base
                    WHERE 
                        id = ?
                """
                
                item_result = self.db.fetch_one(item_query, [item_id])
                
                if not item_result:
                    logger.warning(f"البند رقم {item_id} غير موجود")
                    continue
                
                item_data = {
                    'id': item_result[0],
                    'code': item_result[1],
                    'name': item_result[2],
                    'description': item_result[3],
                    'unit_name': item_result[4],
                    'unit_symbol': item_result[5],
                    'base_price': item_result[6],
                    'last_updated_date': item_result[7]
                }
                
                # إذا تم تحديد تاريخ، نبحث عن السعر في ذلك التاريخ
                if date:
                    price_query = """
                        SELECT price, price_date, price_source
                        FROM pricing_items_history
                        WHERE base_item_id = ?
                        AND price_date <= ?
                        ORDER BY price_date DESC
                        LIMIT 1
                    """
                    
                    price_result = self.db.fetch_one(price_query, [item_id, date])
                    
                    if price_result:
                        item_data['price'] = price_result[0]
                        item_data['price_date'] = price_result[1]
                        item_data['price_source'] = price_result[2]
                    else:
                        # إذا لم يتم العثور على سعر في التاريخ المحدد، نستخدم السعر الأساسي
                        item_data['price'] = item_data['base_price']
                        item_data['price_date'] = item_data['last_updated_date']
                        item_data['price_source'] = 'base_price'
                else:
                    # إذا لم يتم تحديد تاريخ، نستخدم أحدث سعر
                    price_query = """
                        SELECT price, price_date, price_source
                        FROM pricing_items_history
                        WHERE base_item_id = ?
                        ORDER BY price_date DESC
                        LIMIT 1
                    """
                    
                    price_result = self.db.fetch_one(price_query, [item_id])
                    
                    if price_result:
                        item_data['price'] = price_result[0]
                        item_data['price_date'] = price_result[1]
                        item_data['price_source'] = price_result[2]
                    else:
                        # إذا لم يتم العثور على سعر، نستخدم السعر الأساسي
                        item_data['price'] = item_data['base_price']
                        item_data['price_date'] = item_data['last_updated_date']
                        item_data['price_source'] = 'base_price'
                
                comparison_data.append(item_data)
            
            if not comparison_data:
                return {
                    'status': 'error',
                    'message': 'لم يتم العثور على أي بنود للمقارنة'
                }
            
            # إنشاء رسم بياني للمقارنة
            chart_path = self._create_comparison_chart(comparison_data, date)
            
            return {
                'status': 'success',
                'data': {
                    'items': comparison_data,
                    'comparison_date': date if date else 'latest',
                    'chart_path': chart_path
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في مقارنة الأسعار: {str(e)}")
            return {
                'status': 'error',
                'message': f'حدث خطأ أثناء مقارنة الأسعار: {str(e)}'
            }
    
    def _create_comparison_chart(self, comparison_data, date=None):
        """إنشاء رسم بياني للمقارنة
        
        المعلمات:
            comparison_data (list): بيانات المقارنة
            date (str, optional): تاريخ المقارنة
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني جديد
            plt.figure(figsize=(12, 6))
            
            # إعداد البيانات للرسم
            names = [f"{item['code']} - {item['name']}" for item in comparison_data]
            prices = [item['price'] for item in comparison_data]
            
            # رسم الأعمدة
            bars = plt.bar(names, prices, color='skyblue', edgecolor='navy')
            
            # إضافة القيم فوق الأعمدة
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.2f}', ha='center', va='bottom')
            
            # إضافة عنوان ومحاور
            title = "مقارنة الأسعار"
            if date:
                title += f" (بتاريخ {date})"
            
            plt.title(title)
            plt.xlabel('البنود')
            plt.ylabel('السعر')
            
            # تدوير تسميات المحور السيني لتجنب التداخل
            plt.xticks(rotation=45, ha='right')
            
            # إضافة شبكة
            plt.grid(True, linestyle='--', alpha=0.7, axis='y')
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"price_comparison_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني للمقارنة: {str(e)}")
            return None
    
    def calculate_price_volatility(self, item_id, period='1y'):
        """حساب تقلب الأسعار
        
        المعلمات:
            item_id (int): معرف البند
            period (str): الفترة الزمنية ('1m', '3m', '6m', '1y', '2y', '5y', 'all')
            
        العائد:
            dict: قاموس يحتوي على نتائج حساب تقلب الأسعار
        """
        try:
            # تحديد تاريخ البداية بناءً على الفترة
            end_date = datetime.now().strftime('%Y-%m-%d')
            
            if period == '1m':
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            elif period == '3m':
                start_date = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')
            elif period == '6m':
                start_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
            elif period == '1y':
                start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
            elif period == '2y':
                start_date = (datetime.now() - timedelta(days=730)).strftime('%Y-%m-%d')
            elif period == '5y':
                start_date = (datetime.now() - timedelta(days=1825)).strftime('%Y-%m-%d')
            else:  # 'all'
                start_date = None
            
            # الحصول على تاريخ الأسعار
            df = self.get_price_history(item_id, start_date, end_date)
            
            if df.empty or len(df) < 2:
                return {
                    'status': 'error',
                    'message': 'لا توجد بيانات كافية لحساب تقلب الأسعار'
                }
            
            # حساب التقلب (معامل الاختلاف)
            mean_price = df['price'].mean()
            std_dev = df['price'].std()
            volatility = (std_dev / mean_price) * 100
            
            # حساب التغيرات النسبية
            df['price_shift'] = df['price'].shift(1)
            df = df.dropna()
            
            if not df.empty:
                df['price_change_pct'] = ((df['price'] - df['price_shift']) / df['price_shift']) * 100
                
                # حساب إحصاءات التغيرات
                max_increase = df['price_change_pct'].max()
                max_decrease = df['price_change_pct'].min()
                avg_change = df['price_change_pct'].mean()
                median_change = df['price_change_pct'].median()
                
                # حساب عدد التغيرات الإيجابية والسلبية
                positive_changes = (df['price_change_pct'] > 0).sum()
                negative_changes = (df['price_change_pct'] < 0).sum()
                no_changes = (df['price_change_pct'] == 0).sum()
                
                # تصنيف التقلب
                if volatility < 5:
                    volatility_level = 'low'
                    volatility_description = 'منخفض'
                elif volatility < 15:
                    volatility_level = 'medium'
                    volatility_description = 'متوسط'
                else:
                    volatility_level = 'high'
                    volatility_description = 'مرتفع'
                
                # إنشاء رسم بياني للتقلب
                chart_path = self._create_volatility_chart(df, item_id, period)
                
                return {
                    'status': 'success',
                    'data': {
                        'item_id': item_id,
                        'item_name': df['name'].iloc[0],
                        'item_code': df['code'].iloc[0],
                        'period': period,
                        'start_date': df['price_date'].min().strftime('%Y-%m-%d'),
                        'end_date': df['price_date'].max().strftime('%Y-%m-%d'),
                        'data_points': len(df),
                        'mean_price': mean_price,
                        'std_dev': std_dev,
                        'volatility': volatility,
                        'volatility_level': volatility_level,
                        'volatility_description': volatility_description,
                        'max_increase': max_increase,
                        'max_decrease': max_decrease,
                        'avg_change': avg_change,
                        'median_change': median_change,
                        'positive_changes': positive_changes,
                        'negative_changes': negative_changes,
                        'no_changes': no_changes,
                        'chart_path': chart_path
                    }
                }
            else:
                return {
                    'status': 'error',
                    'message': 'لا توجد بيانات كافية لحساب تقلب الأسعار بعد معالجة البيانات'
                }
            
        except Exception as e:
            logger.error(f"خطأ في حساب تقلب الأسعار: {str(e)}")
            return {
                'status': 'error',
                'message': f'حدث خطأ أثناء حساب تقلب الأسعار: {str(e)}'
            }
    
    def _create_volatility_chart(self, df, item_id, period):
        """إنشاء رسم بياني للتقلب
        
        المعلمات:
            df (pandas.DataFrame): إطار البيانات
            item_id (int): معرف البند
            period (str): الفترة الزمنية
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني بمحورين
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})
            
            # الرسم البياني العلوي: سعر البند عبر الزمن
            ax1.plot(df['price_date'], df['price'], 'b-', linewidth=2)
            ax1.set_title(f"سعر البند عبر الزمن - {df['name'].iloc[0]} ({df['code'].iloc[0]})")
            ax1.set_xlabel('التاريخ')
            ax1.set_ylabel('السعر')
            ax1.grid(True, linestyle='--', alpha=0.7)
            
            # إضافة نطاق الانحراف المعياري
            mean_price = df['price'].mean()
            std_dev = df['price'].std()
            
            ax1.axhline(y=mean_price, color='g', linestyle='-', alpha=0.8, label='متوسط السعر')
            ax1.axhline(y=mean_price + std_dev, color='r', linestyle='--', alpha=0.5, label='انحراف معياري +1')
            ax1.axhline(y=mean_price - std_dev, color='r', linestyle='--', alpha=0.5, label='انحراف معياري -1')
            
            ax1.fill_between(df['price_date'], mean_price - std_dev, mean_price + std_dev, color='gray', alpha=0.2)
            ax1.legend()
            
            # الرسم البياني السفلي: التغيرات النسبية
            ax2.bar(df['price_date'], df['price_change_pct'], color='skyblue', edgecolor='navy', alpha=0.7)
            ax2.set_title('التغيرات النسبية في السعر (%)')
            ax2.set_xlabel('التاريخ')
            ax2.set_ylabel('التغير النسبي (%)')
            ax2.grid(True, linestyle='--', alpha=0.7)
            
            # إضافة خط الصفر
            ax2.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            
            # تنسيق التاريخ على المحور السيني
            fig.autofmt_xdate()
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"price_volatility_{item_id}_{period}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني للتقلب: {str(e)}")
            return None
    
    def perform_sensitivity_analysis(self, project_id, variable_items, ranges):
        """إجراء تحليل الحساسية
        
        المعلمات:
            project_id (int): معرف المشروع
            variable_items (list): قائمة بمعرفات البنود المتغيرة
            ranges (dict): نطاقات التغيير لكل بند
            
        العائد:
            dict: قاموس يحتوي على نتائج تحليل الحساسية
        """
        try:
            # الحصول على بنود المشروع
            query = """
                SELECT 
                    id, item_number, description, quantity, unit_price, total_price
                FROM 
                    project_pricing_items
                WHERE 
                    project_id = ?
            """
            
            results = self.db.fetch_all(query, [project_id])
            
            if not results:
                return {
                    'status': 'error',
                    'message': 'لا توجد بنود للمشروع المحدد'
                }
            
            # تحويل النتائج إلى إطار بيانات
            project_items = pd.DataFrame(results, columns=[
                'id', 'item_number', 'description', 'quantity', 'unit_price', 'total_price'
            ])
            
            # حساب إجمالي المشروع الأصلي
            original_total = project_items['total_price'].sum()
            
            # تحضير بيانات تحليل الحساسية
            sensitivity_data = []
            
            for item_id in variable_items:
                if item_id not in project_items['id'].values:
                    logger.warning(f"البند رقم {item_id} غير موجود في المشروع")
                    continue
                
                # الحصول على معلومات البند
                item_info = project_items[project_items['id'] == item_id].iloc[0]
                
                # الحصول على نطاق التغيير للبند
                if str(item_id) in ranges:
                    item_range = ranges[str(item_id)]
                else:
                    # استخدام نطاق افتراضي إذا لم يتم تحديد نطاق
                    item_range = {'min': -20, 'max': 20, 'step': 10}
                
                # إنشاء قائمة بنسب التغيير
                change_percentages = list(range(
                    item_range['min'], 
                    item_range['max'] + item_range['step'], 
                    item_range['step']
                ))
                
                item_sensitivity = {
                    'item_id': item_id,
                    'item_number': item_info['item_number'],
                    'description': item_info['description'],
                    'original_price': item_info['unit_price'],
                    'original_total': item_info['total_price'],
                    'changes': []
                }
                
                # حساب تأثير كل نسبة تغيير
                for percentage in change_percentages:
                    # حساب السعر الجديد
                    new_price = item_info['unit_price'] * (1 + percentage / 100)
                    new_total = new_price * item_info['quantity']
                    
                    # حساب إجمالي المشروع الجديد
                    project_total = original_total - item_info['total_price'] + new_total
                    
                    # حساب التغير في إجمالي المشروع
                    project_change = ((project_total - original_total) / original_total) * 100
                    
                    item_sensitivity['changes'].append({
                        'percentage': percentage,
                        'new_price': new_price,
                        'new_total': new_total,
                        'project_total': project_total,
                        'project_change': project_change
                    })
                
                sensitivity_data.append(item_sensitivity)
            
            if not sensitivity_data:
                return {
                    'status': 'error',
                    'message': 'لا توجد بنود صالحة لتحليل الحساسية'
                }
            
            # إنشاء رسم بياني لتحليل الحساسية
            chart_path = self._create_sensitivity_chart(sensitivity_data, original_total, project_id)
            
            return {
                'status': 'success',
                'data': {
                    'project_id': project_id,
                    'original_total': original_total,
                    'sensitivity_data': sensitivity_data,
                    'chart_path': chart_path
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في إجراء تحليل الحساسية: {str(e)}")
            return {
                'status': 'error',
                'message': f'حدث خطأ أثناء إجراء تحليل الحساسية: {str(e)}'
            }
    
    def _create_sensitivity_chart(self, sensitivity_data, original_total, project_id):
        """إنشاء رسم بياني لتحليل الحساسية
        
        المعلمات:
            sensitivity_data (list): بيانات تحليل الحساسية
            original_total (float): إجمالي المشروع الأصلي
            project_id (int): معرف المشروع
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني جديد
            plt.figure(figsize=(12, 8))
            
            # رسم خطوط الحساسية لكل بند
            for item in sensitivity_data:
                percentages = [change['percentage'] for change in item['changes']]
                project_changes = [change['project_change'] for change in item['changes']]
                
                plt.plot(percentages, project_changes, marker='o', linewidth=2, 
                        label=f"{item['item_number']} - {item['description'][:30]}...")
            
            # إضافة عنوان ومحاور
            plt.title(f"تحليل الحساسية للمشروع رقم {project_id}")
            plt.xlabel('نسبة التغيير في سعر البند (%)')
            plt.ylabel('نسبة التغيير في إجمالي المشروع (%)')
            
            # إضافة خط الصفر
            plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
            plt.axvline(x=0, color='k', linestyle='-', alpha=0.3)
            
            # إضافة شبكة
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # إضافة وسيلة إيضاح
            plt.legend(loc='best')
            
            # إضافة معلومات إضافية
            info_text = f"إجمالي المشروع الأصلي: {original_total:,.2f}"
            plt.annotate(info_text, xy=(0.02, 0.02), xycoords='axes fraction', 
                        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"sensitivity_analysis_{project_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لتحليل الحساسية: {str(e)}")
            return None
    
    def analyze_price_correlations(self, items):
        """تحليل ارتباطات الأسعار بين عدة بنود
        
        المعلمات:
            items (list): قائمة بمعرفات البنود
            
        العائد:
            dict: قاموس يحتوي على نتائج تحليل الارتباطات
        """
        try:
            if not items or len(items) < 2:
                return {
                    'status': 'error',
                    'message': 'يجب تحديد بندين على الأقل لتحليل الارتباطات'
                }
            
            # جمع بيانات الأسعار لجميع البنود
            all_prices = {}
            item_names = {}
            
            for item_id in items:
                # الحصول على تاريخ الأسعار
                df = self.get_price_history(item_id)
                
                if df.empty:
                    logger.warning(f"لا توجد بيانات تاريخية للسعر للبند رقم {item_id}")
                    continue
                
                # تخزين بيانات الأسعار
                all_prices[item_id] = df[['price_date', 'price']].copy()
                item_names[item_id] = f"{df['code'].iloc[0]} - {df['name'].iloc[0]}"
            
            if len(all_prices) < 2:
                return {
                    'status': 'error',
                    'message': 'لا توجد بيانات كافية لتحليل الارتباطات'
                }
            
            # إنشاء إطار بيانات موحد بتواريخ مشتركة
            # أولاً، نجمع جميع التواريخ الفريدة
            all_dates = set()
            for item_id, df in all_prices.items():
                all_dates.update(df['price_date'].dt.strftime('%Y-%m-%d').tolist())
            
            # إنشاء إطار بيانات جديد بجميع التواريخ
            unified_df = pd.DataFrame({'price_date': sorted(list(all_dates))})
            unified_df['price_date'] = pd.to_datetime(unified_df['price_date'])
            
            # إضافة أسعار كل بند
            for item_id, df in all_prices.items():
                # تحويل إطار البيانات إلى سلسلة زمنية مفهرسة بالتاريخ
                price_series = df.set_index('price_date')['price']
                
                # إعادة فهرسة السلسلة الزمنية لتتوافق مع التواريخ الموحدة
                unified_df[f'price_{item_id}'] = unified_df['price_date'].map(
                    lambda x: price_series.get(x, None)
                )
            
            # ملء القيم المفقودة باستخدام الاستيفاء الخطي
            price_columns = [col for col in unified_df.columns if col.startswith('price_')]
            unified_df[price_columns] = unified_df[price_columns].interpolate(method='linear')
            
            # حذف الصفوف التي لا تزال تحتوي على قيم مفقودة
            unified_df = unified_df.dropna()
            
            if len(unified_df) < 3:
                return {
                    'status': 'error',
                    'message': 'لا توجد بيانات كافية بعد معالجة التواريخ المشتركة'
                }
            
            # حساب مصفوفة الارتباط
            correlation_matrix = unified_df[price_columns].corr()
            
            # تحويل مصفوفة الارتباط إلى تنسيق أكثر قابلية للقراءة
            correlation_data = []
            
            for i, item1_id in enumerate(items):
                if f'price_{item1_id}' not in correlation_matrix.columns:
                    continue
                    
                for j, item2_id in enumerate(items):
                    if f'price_{item2_id}' not in correlation_matrix.columns or i >= j:
                        continue
                    
                    correlation = correlation_matrix.loc[f'price_{item1_id}', f'price_{item2_id}']
                    
                    # تحديد قوة واتجاه الارتباط
                    if abs(correlation) < 0.3:
                        strength = 'weak'
                        strength_description = 'ضعيف'
                    elif abs(correlation) < 0.7:
                        strength = 'moderate'
                        strength_description = 'متوسط'
                    else:
                        strength = 'strong'
                        strength_description = 'قوي'
                    
                    if correlation > 0:
                        direction = 'positive'
                        direction_description = 'طردي'
                    else:
                        direction = 'negative'
                        direction_description = 'عكسي'
                    
                    correlation_data.append({
                        'item1_id': item1_id,
                        'item1_name': item_names.get(item1_id, f'البند {item1_id}'),
                        'item2_id': item2_id,
                        'item2_name': item_names.get(item2_id, f'البند {item2_id}'),
                        'correlation': correlation,
                        'strength': strength,
                        'strength_description': strength_description,
                        'direction': direction,
                        'direction_description': direction_description
                    })
            
            if not correlation_data:
                return {
                    'status': 'error',
                    'message': 'لم يتم العثور على ارتباطات بين البنود المحددة'
                }
            
            # إنشاء رسم بياني للارتباطات
            chart_path = self._create_correlation_chart(correlation_matrix, item_names)
            
            # إنشاء رسم بياني لتطور الأسعار
            trends_chart_path = self._create_price_trends_chart(unified_df, price_columns, item_names)
            
            return {
                'status': 'success',
                'data': {
                    'correlation_data': correlation_data,
                    'chart_path': chart_path,
                    'trends_chart_path': trends_chart_path
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل ارتباطات الأسعار: {str(e)}")
            return {
                'status': 'error',
                'message': f'حدث خطأ أثناء تحليل ارتباطات الأسعار: {str(e)}'
            }
    
    def _create_correlation_chart(self, correlation_matrix, item_names):
        """إنشاء رسم بياني لمصفوفة الارتباط
        
        المعلمات:
            correlation_matrix (pandas.DataFrame): مصفوفة الارتباط
            item_names (dict): قاموس بأسماء البنود
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني جديد
            plt.figure(figsize=(10, 8))
            
            # إنشاء خريطة حرارية للارتباطات
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
            cmap = sns.diverging_palette(230, 20, as_cmap=True)
            
            # تعديل تسميات المحاور
            labels = [item_names.get(int(col.split('_')[1]), col) for col in correlation_matrix.columns]
            
            # رسم الخريطة الحرارية
            sns.heatmap(correlation_matrix, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                        square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True,
                        xticklabels=labels, yticklabels=labels)
            
            # إضافة عنوان
            plt.title('مصفوفة ارتباط الأسعار بين البنود')
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"price_correlation_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لمصفوفة الارتباط: {str(e)}")
            return None
    
    def _create_price_trends_chart(self, unified_df, price_columns, item_names):
        """إنشاء رسم بياني لتطور الأسعار
        
        المعلمات:
            unified_df (pandas.DataFrame): إطار البيانات الموحد
            price_columns (list): أسماء أعمدة الأسعار
            item_names (dict): قاموس بأسماء البنود
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني جديد
            plt.figure(figsize=(12, 6))
            
            # رسم تطور الأسعار لكل بند
            for col in price_columns:
                item_id = int(col.split('_')[1])
                item_name = item_names.get(item_id, f'البند {item_id}')
                
                # تطبيع الأسعار للمقارنة (القيمة الأولى = 100)
                first_price = unified_df[col].iloc[0]
                normalized_prices = (unified_df[col] / first_price) * 100
                
                plt.plot(unified_df['price_date'], normalized_prices, linewidth=2, label=item_name)
            
            # إضافة عنوان ومحاور
            plt.title('تطور الأسعار النسبية للبنود (القيمة الأولى = 100)')
            plt.xlabel('التاريخ')
            plt.ylabel('السعر النسبي')
            
            # إضافة شبكة
            plt.grid(True, linestyle='--', alpha=0.7)
            
            # إضافة وسيلة إيضاح
            plt.legend(loc='best')
            
            # تنسيق التاريخ على المحور السيني
            plt.gcf().autofmt_xdate()
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"price_trends_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لتطور الأسعار: {str(e)}")
            return None
    
    def compare_with_market_prices(self, items):
        """مقارنة أسعار البنود مع أسعار السوق
        
        المعلمات:
            items (list): قائمة بمعرفات البنود
            
        العائد:
            dict: قاموس يحتوي على نتائج المقارنة
        """
        try:
            if not items:
                return {
                    'status': 'error',
                    'message': 'لم يتم تحديد أي بنود للمقارنة'
                }
            
            comparison_data = []
            
            for item_id in items:
                # الحصول على معلومات البند الأساسية
                item_query = """
                    SELECT 
                        id, code, name, description, 
                        (SELECT name FROM measurement_units WHERE id = unit_id) as unit_name,
                        (SELECT symbol FROM measurement_units WHERE id = unit_id) as unit_symbol,
                        base_price, last_updated_date
                    FROM 
                        pricing_items_base
                    WHERE 
                        id = ?
                """
                
                item_result = self.db.fetch_one(item_query, [item_id])
                
                if not item_result:
                    logger.warning(f"البند رقم {item_id} غير موجود")
                    continue
                
                item_data = {
                    'id': item_result[0],
                    'code': item_result[1],
                    'name': item_result[2],
                    'description': item_result[3],
                    'unit_name': item_result[4],
                    'unit_symbol': item_result[5],
                    'base_price': item_result[6],
                    'last_updated_date': item_result[7]
                }
                
                # الحصول على أحدث سعر للبند
                price_query = """
                    SELECT price, price_date, price_source
                    FROM pricing_items_history
                    WHERE base_item_id = ?
                    ORDER BY price_date DESC
                    LIMIT 1
                """
                
                price_result = self.db.fetch_one(price_query, [item_id])
                
                if price_result:
                    item_data['current_price'] = price_result[0]
                    item_data['price_date'] = price_result[1]
                    item_data['price_source'] = price_result[2]
                else:
                    # إذا لم يتم العثور على سعر، نستخدم السعر الأساسي
                    item_data['current_price'] = item_data['base_price']
                    item_data['price_date'] = item_data['last_updated_date']
                    item_data['price_source'] = 'base_price'
                
                # الحصول على متوسط سعر السوق (من مصادر مختلفة)
                market_query = """
                    SELECT AVG(price) as avg_price
                    FROM pricing_items_history
                    WHERE base_item_id = ? AND price_source != 'internal'
                    AND price_date >= date('now', '-6 months')
                """
                
                market_result = self.db.fetch_one(market_query, [item_id])
                
                if market_result and market_result[0]:
                    item_data['market_price'] = market_result[0]
                    
                    # حساب الفرق بين السعر الحالي وسعر السوق
                    item_data['price_difference'] = item_data['current_price'] - item_data['market_price']
                    item_data['price_difference_percentage'] = (item_data['price_difference'] / item_data['market_price']) * 100
                    
                    # تحديد حالة السعر
                    if abs(item_data['price_difference_percentage']) < 5:
                        item_data['price_status'] = 'competitive'
                        item_data['price_status_description'] = 'تنافسي'
                    elif item_data['price_difference_percentage'] < 0:
                        item_data['price_status'] = 'below_market'
                        item_data['price_status_description'] = 'أقل من السوق'
                    else:
                        item_data['price_status'] = 'above_market'
                        item_data['price_status_description'] = 'أعلى من السوق'
                else:
                    # إذا لم يتم العثور على سعر سوق، نستخدم متوسط الأسعار الداخلية
                    internal_query = """
                        SELECT AVG(price) as avg_price
                        FROM pricing_items_history
                        WHERE base_item_id = ?
                        AND price_date >= date('now', '-6 months')
                    """
                    
                    internal_result = self.db.fetch_one(internal_query, [item_id])
                    
                    if internal_result and internal_result[0]:
                        item_data['market_price'] = internal_result[0]
                        item_data['price_difference'] = item_data['current_price'] - item_data['market_price']
                        item_data['price_difference_percentage'] = (item_data['price_difference'] / item_data['market_price']) * 100
                        
                        # تحديد حالة السعر
                        if abs(item_data['price_difference_percentage']) < 5:
                            item_data['price_status'] = 'competitive'
                            item_data['price_status_description'] = 'تنافسي'
                        elif item_data['price_difference_percentage'] < 0:
                            item_data['price_status'] = 'below_average'
                            item_data['price_status_description'] = 'أقل من المتوسط'
                        else:
                            item_data['price_status'] = 'above_average'
                            item_data['price_status_description'] = 'أعلى من المتوسط'
                    else:
                        item_data['market_price'] = None
                        item_data['price_difference'] = None
                        item_data['price_difference_percentage'] = None
                        item_data['price_status'] = 'unknown'
                        item_data['price_status_description'] = 'غير معروف'
                
                comparison_data.append(item_data)
            
            if not comparison_data:
                return {
                    'status': 'error',
                    'message': 'لم يتم العثور على أي بنود للمقارنة'
                }
            
            # إنشاء رسم بياني للمقارنة
            chart_path = self._create_market_comparison_chart(comparison_data)
            
            return {
                'status': 'success',
                'data': {
                    'items': comparison_data,
                    'chart_path': chart_path
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في مقارنة الأسعار مع أسعار السوق: {str(e)}")
            return {
                'status': 'error',
                'message': f'حدث خطأ أثناء مقارنة الأسعار مع أسعار السوق: {str(e)}'
            }
    
    def _create_market_comparison_chart(self, comparison_data):
        """إنشاء رسم بياني لمقارنة الأسعار مع أسعار السوق
        
        المعلمات:
            comparison_data (list): بيانات المقارنة
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # تصفية البنود التي لها أسعار سوق
            valid_items = [item for item in comparison_data if item.get('market_price') is not None]
            
            if not valid_items:
                return None
            
            # إنشاء رسم بياني جديد
            plt.figure(figsize=(12, 6))
            
            # إعداد البيانات للرسم
            names = [f"{item['code']} - {item['name'][:20]}..." for item in valid_items]
            current_prices = [item['current_price'] for item in valid_items]
            market_prices = [item['market_price'] for item in valid_items]
            
            # إنشاء مواقع الأعمدة
            x = np.arange(len(names))
            width = 0.35
            
            # رسم الأعمدة
            plt.bar(x - width/2, current_prices, width, label='السعر الحالي', color='skyblue')
            plt.bar(x + width/2, market_prices, width, label='سعر السوق', color='lightgreen')
            
            # إضافة تسميات وعنوان
            plt.xlabel('البنود')
            plt.ylabel('السعر')
            plt.title('مقارنة الأسعار الحالية مع أسعار السوق')
            plt.xticks(x, names, rotation=45, ha='right')
            plt.legend()
            
            # إضافة شبكة
            plt.grid(True, linestyle='--', alpha=0.7, axis='y')
            
            # إضافة قيم الفروق النسبية
            for i, item in enumerate(valid_items):
                if 'price_difference_percentage' in item and item['price_difference_percentage'] is not None:
                    percentage = item['price_difference_percentage']
                    color = 'green' if percentage < 0 else 'red' if percentage > 0 else 'black'
                    plt.annotate(f"{percentage:.1f}%", 
                                xy=(x[i], max(current_prices[i], market_prices[i]) * 1.05),
                                ha='center', va='bottom', color=color,
                                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"market_comparison_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لمقارنة الأسعار مع أسعار السوق: {str(e)}")
            return None
    
    def analyze_cost_drivers(self, project_id):
        """تحليل محركات التكلفة للمشروع
        
        المعلمات:
            project_id (int): معرف المشروع
            
        العائد:
            dict: قاموس يحتوي على نتائج تحليل محركات التكلفة
        """
        try:
            # الحصول على بنود المشروع
            query = """
                SELECT 
                    id, item_number, description, quantity, unit_price, total_price,
                    (SELECT name FROM pricing_categories WHERE id = 
                        (SELECT category_id FROM pricing_items_base WHERE id = base_item_id)
                    ) as category_name
                FROM 
                    project_pricing_items
                WHERE 
                    project_id = ?
            """
            
            results = self.db.fetch_all(query, [project_id])
            
            if not results:
                return {
                    'status': 'error',
                    'message': 'لا توجد بنود للمشروع المحدد'
                }
            
            # تحويل النتائج إلى إطار بيانات
            df = pd.DataFrame(results, columns=[
                'id', 'item_number', 'description', 'quantity', 'unit_price', 
                'total_price', 'category_name'
            ])
            
            # معالجة القيم المفقودة في عمود الفئة
            df['category_name'] = df['category_name'].fillna('أخرى')
            
            # حساب إجمالي المشروع
            project_total = df['total_price'].sum()
            
            # تحليل البنود حسب الفئة
            category_analysis = df.groupby('category_name').agg({
                'total_price': 'sum'
            }).reset_index()
            
            # إضافة النسبة المئوية
            category_analysis['percentage'] = (category_analysis['total_price'] / project_total) * 100
            
            # ترتيب الفئات حسب التكلفة
            category_analysis = category_analysis.sort_values('total_price', ascending=False)
            
            # تحليل البنود الأعلى تكلفة
            top_items = df.sort_values('total_price', ascending=False).head(10)
            top_items['percentage'] = (top_items['total_price'] / project_total) * 100
            
            # حساب تركيز التكلفة (نسبة باريتو)
            df_sorted = df.sort_values('total_price', ascending=False)
            df_sorted['cumulative_cost'] = df_sorted['total_price'].cumsum()
            df_sorted['cumulative_percentage'] = (df_sorted['cumulative_cost'] / project_total) * 100
            
            # تحديد عدد البنود التي تشكل 80% من التكلفة
            items_80_percent = len(df_sorted[df_sorted['cumulative_percentage'] <= 80])
            if items_80_percent == 0:
                items_80_percent = 1
            
            pareto_ratio = items_80_percent / len(df)
            
            # إنشاء رسوم بيانية
            category_chart_path = self._create_category_chart(category_analysis)
            top_items_chart_path = self._create_top_items_chart(top_items)
            pareto_chart_path = self._create_pareto_chart(df_sorted)
            
            return {
                'status': 'success',
                'data': {
                    'project_id': project_id,
                    'project_total': project_total,
                    'category_analysis': category_analysis.to_dict('records'),
                    'top_items': top_items.to_dict('records'),
                    'pareto_ratio': pareto_ratio,
                    'items_80_percent': items_80_percent,
                    'total_items': len(df),
                    'category_chart_path': category_chart_path,
                    'top_items_chart_path': top_items_chart_path,
                    'pareto_chart_path': pareto_chart_path
                }
            }
            
        except Exception as e:
            logger.error(f"خطأ في تحليل محركات التكلفة: {str(e)}")
            return {
                'status': 'error',
                'message': f'حدث خطأ أثناء تحليل محركات التكلفة: {str(e)}'
            }
    
    def _create_category_chart(self, category_analysis):
        """إنشاء رسم بياني للتكاليف حسب الفئة
        
        المعلمات:
            category_analysis (pandas.DataFrame): تحليل الفئات
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني جديد
            plt.figure(figsize=(10, 6))
            
            # رسم مخطط دائري
            plt.pie(
                category_analysis['total_price'],
                labels=category_analysis['category_name'],
                autopct='%1.1f%%',
                startangle=90,
                shadow=False,
                wedgeprops={'edgecolor': 'white', 'linewidth': 1}
            )
            
            # إضافة عنوان
            plt.title('توزيع التكاليف حسب الفئة')
            
            # جعل الرسم البياني دائريًا
            plt.axis('equal')
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"cost_category_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني للتكاليف حسب الفئة: {str(e)}")
            return None
    
    def _create_top_items_chart(self, top_items):
        """إنشاء رسم بياني للبنود الأعلى تكلفة
        
        المعلمات:
            top_items (pandas.DataFrame): البنود الأعلى تكلفة
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني جديد
            plt.figure(figsize=(12, 6))
            
            # إعداد البيانات للرسم
            items = [f"{row['item_number']} - {row['description'][:20]}..." for _, row in top_items.iterrows()]
            costs = top_items['total_price'].tolist()
            
            # رسم الأعمدة
            bars = plt.barh(items, costs, color='skyblue', edgecolor='navy')
            
            # إضافة القيم على الأعمدة
            for i, bar in enumerate(bars):
                width = bar.get_width()
                plt.text(width * 1.01, bar.get_y() + bar.get_height()/2,
                        f'{width:,.0f} ({top_items["percentage"].iloc[i]:.1f}%)',
                        va='center')
            
            # إضافة عنوان ومحاور
            plt.title('البنود الأعلى تكلفة')
            plt.xlabel('التكلفة')
            plt.ylabel('البنود')
            
            # إضافة شبكة
            plt.grid(True, linestyle='--', alpha=0.7, axis='x')
            
            # ضبط التخطيط
            plt.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"top_cost_items_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني للبنود الأعلى تكلفة: {str(e)}")
            return None
    
    def _create_pareto_chart(self, df_sorted):
        """إنشاء رسم بياني لتحليل باريتو
        
        المعلمات:
            df_sorted (pandas.DataFrame): إطار البيانات المرتب
            
        العائد:
            str: مسار ملف الرسم البياني
        """
        try:
            # إنشاء رسم بياني جديد
            fig, ax1 = plt.subplots(figsize=(12, 6))
            
            # إعداد البيانات للرسم
            x = range(1, len(df_sorted) + 1)
            y1 = df_sorted['total_price'].tolist()
            y2 = df_sorted['cumulative_percentage'].tolist()
            
            # رسم الأعمدة (التكلفة)
            ax1.bar(x, y1, color='skyblue', alpha=0.7)
            ax1.set_xlabel('عدد البنود')
            ax1.set_ylabel('التكلفة', color='navy')
            ax1.tick_params(axis='y', labelcolor='navy')
            
            # إنشاء محور ثانوي
            ax2 = ax1.twinx()
            
            # رسم الخط (النسبة التراكمية)
            ax2.plot(x, y2, 'r-', linewidth=2, marker='o', markersize=4)
            ax2.set_ylabel('النسبة التراكمية (%)', color='red')
            ax2.tick_params(axis='y', labelcolor='red')
            
            # إضافة خط 80%
            ax2.axhline(y=80, color='green', linestyle='--', alpha=0.7)
            
            # إضافة عنوان
            plt.title('تحليل باريتو للتكاليف')
            
            # إضافة شبكة
            ax1.grid(True, linestyle='--', alpha=0.7)
            
            # ضبط التخطيط
            fig.tight_layout()
            
            # حفظ الرسم البياني
            chart_filename = f"pareto_analysis_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            chart_path = os.path.join(self.charts_dir, chart_filename)
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            return chart_path
            
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسم بياني لتحليل باريتو: {str(e)}")
            return None
    
    def generate_price_analysis_charts(self, analysis_type, params):
        """إنشاء رسوم بيانية لتحليل الأسعار
        
        المعلمات:
            analysis_type (str): نوع التحليل
            params (dict): معلمات التحليل
            
        العائد:
            dict: قاموس يحتوي على مسارات الرسوم البيانية
        """
        try:
            if analysis_type == 'trend':
                # تحليل اتجاه السعر
                if 'item_id' not in params:
                    return {
                        'status': 'error',
                        'message': 'لم يتم تحديد معرف البند'
                    }
                
                result = self.analyze_price_trends(
                    params['item_id'],
                    params.get('start_date'),
                    params.get('end_date')
                )
                
                if result['status'] == 'success':
                    return {
                        'status': 'success',
                        'charts': [result['data']['chart_path']]
                    }
                else:
                    return result
                
            elif analysis_type == 'comparison':
                # مقارنة الأسعار
                if 'items' not in params:
                    return {
                        'status': 'error',
                        'message': 'لم يتم تحديد البنود للمقارنة'
                    }
                
                result = self.compare_prices(
                    params['items'],
                    params.get('date')
                )
                
                if result['status'] == 'success':
                    return {
                        'status': 'success',
                        'charts': [result['data']['chart_path']]
                    }
                else:
                    return result
                
            elif analysis_type == 'volatility':
                # تحليل تقلب الأسعار
                if 'item_id' not in params:
                    return {
                        'status': 'error',
                        'message': 'لم يتم تحديد معرف البند'
                    }
                
                result = self.calculate_price_volatility(
                    params['item_id'],
                    params.get('period', '1y')
                )
                
                if result['status'] == 'success':
                    return {
                        'status': 'success',
                        'charts': [result['data']['chart_path']]
                    }
                else:
                    return result
                
            elif analysis_type == 'sensitivity':
                # تحليل الحساسية
                if 'project_id' not in params or 'variable_items' not in params:
                    return {
                        'status': 'error',
                        'message': 'لم يتم تحديد معرف المشروع أو البنود المتغيرة'
                    }
                
                result = self.perform_sensitivity_analysis(
                    params['project_id'],
                    params['variable_items'],
                    params.get('ranges', {})
                )
                
                if result['status'] == 'success':
                    return {
                        'status': 'success',
                        'charts': [result['data']['chart_path']]
                    }
                else:
                    return result
                
            elif analysis_type == 'correlation':
                # تحليل الارتباطات
                if 'items' not in params:
                    return {
                        'status': 'error',
                        'message': 'لم يتم تحديد البنود للتحليل'
                    }
                
                result = self.analyze_price_correlations(params['items'])
                
                if result['status'] == 'success':
                    return {
                        'status': 'success',
                        'charts': [result['data']['chart_path'], result['data']['trends_chart_path']]
                    }
                else:
                    return result
                
            elif analysis_type == 'market_comparison':
                # مقارنة مع أسعار السوق
                if 'items' not in params:
                    return {
                        'status': 'error',
                        'message': 'لم يتم تحديد البنود للمقارنة'
                    }
                
                result = self.compare_with_market_prices(params['items'])
                
                if result['status'] == 'success':
                    return {
                        'status': 'success',
                        'charts': [result['data']['chart_path']]
                    }
                else:
                    return result
                
            elif analysis_type == 'cost_drivers':
                # تحليل محركات التكلفة
                if 'project_id' not in params:
                    return {
                        'status': 'error',
                        'message': 'لم يتم تحديد معرف المشروع'
                    }
                
                result = self.analyze_cost_drivers(params['project_id'])
                
                if result['status'] == 'success':
                    return {
                        'status': 'success',
                        'charts': [
                            result['data']['category_chart_path'],
                            result['data']['top_items_chart_path'],
                            result['data']['pareto_chart_path']
                        ]
                    }
                else:
                    return result
                
            else:
                return {
                    'status': 'error',
                    'message': f'نوع التحليل غير معروف: {analysis_type}'
                }
                
        except Exception as e:
            logger.error(f"خطأ في إنشاء رسوم بيانية لتحليل الأسعار: {str(e)}")
            return {
                'status': 'error',
                'message': f'حدث خطأ أثناء إنشاء رسوم بيانية لتحليل الأسعار: {str(e)}'
            }
