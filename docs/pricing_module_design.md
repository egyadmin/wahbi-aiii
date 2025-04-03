# تصميم وحدة التسعير المتكاملة وتحليل الأسعار

## هيكل قاعدة البيانات

### جدول فئات البنود (pricing_categories)
```sql
CREATE TABLE pricing_categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### جدول وحدات القياس (measurement_units)
```sql
CREATE TABLE measurement_units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    symbol TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### جدول بنود التسعير الأساسية (pricing_items_base)
```sql
CREATE TABLE pricing_items_base (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    category_id INTEGER,
    unit_id INTEGER,
    base_price REAL NOT NULL,
    last_updated_date TEXT,
    price_source TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES pricing_categories (id),
    FOREIGN KEY (unit_id) REFERENCES measurement_units (id)
);
```

### جدول تاريخ أسعار البنود (pricing_items_history)
```sql
CREATE TABLE pricing_items_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_item_id INTEGER,
    price REAL NOT NULL,
    price_date TEXT NOT NULL,
    price_source TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (base_item_id) REFERENCES pricing_items_base (id)
);
```

### جدول بنود التسعير للمشاريع (project_pricing_items)
```sql
CREATE TABLE project_pricing_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    base_item_id INTEGER,
    item_number TEXT NOT NULL,
    description TEXT NOT NULL,
    unit_id INTEGER,
    quantity REAL NOT NULL,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    direct_cost REAL,
    indirect_cost REAL,
    profit_margin REAL,
    risk_factor REAL,
    notes TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id),
    FOREIGN KEY (base_item_id) REFERENCES pricing_items_base (id),
    FOREIGN KEY (unit_id) REFERENCES measurement_units (id),
    FOREIGN KEY (created_by) REFERENCES users (id)
);
```

### جدول مكونات بنود التسعير (pricing_item_components)
```sql
CREATE TABLE pricing_item_components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pricing_item_id INTEGER,
    component_type TEXT NOT NULL, -- 'material', 'labor', 'equipment', 'subcontractor', 'other'
    component_name TEXT NOT NULL,
    unit_id INTEGER,
    quantity REAL NOT NULL,
    unit_price REAL NOT NULL,
    total_price REAL NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pricing_item_id) REFERENCES project_pricing_items (id),
    FOREIGN KEY (unit_id) REFERENCES measurement_units (id)
);
```

### جدول عوامل التعديل (adjustment_factors)
```sql
CREATE TABLE adjustment_factors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    factor_type TEXT NOT NULL, -- 'inflation', 'location', 'risk', 'market', 'other'
    value REAL NOT NULL,
    start_date TEXT,
    end_date TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### جدول نماذج التسعير (pricing_templates)
```sql
CREATE TABLE pricing_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_by INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users (id)
);
```

### جدول بنود نماذج التسعير (pricing_template_items)
```sql
CREATE TABLE pricing_template_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_id INTEGER,
    base_item_id INTEGER,
    item_number TEXT NOT NULL,
    description TEXT NOT NULL,
    unit_id INTEGER,
    unit_price REAL NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (template_id) REFERENCES pricing_templates (id),
    FOREIGN KEY (base_item_id) REFERENCES pricing_items_base (id),
    FOREIGN KEY (unit_id) REFERENCES measurement_units (id)
);
```

### جدول تنبؤات الأسعار (price_forecasts)
```sql
CREATE TABLE price_forecasts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    base_item_id INTEGER,
    forecast_date TEXT NOT NULL,
    forecast_price REAL NOT NULL,
    forecast_model TEXT,
    confidence_level REAL,
    scenario TEXT, -- 'optimistic', 'baseline', 'pessimistic'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (base_item_id) REFERENCES pricing_items_base (id)
);
```

## هيكل الكلاسات

### 1. مدير التسعير (PricingManager)
```python
class PricingManager:
    """فئة مدير التسعير الرئيسية"""
    
    def __init__(self, db_connector, config):
        """تهيئة مدير التسعير"""
        self.db = db_connector
        self.config = config
        self.item_manager = PricingItemManager(db_connector)
        self.cost_calculator = CostCalculator(db_connector)
        self.price_analyzer = PriceAnalyzer(db_connector)
        self.price_forecaster = PriceForecaster(db_connector)
        self.report_generator = PricingReportGenerator(db_connector)
    
    def initialize_database(self):
        """تهيئة قاعدة البيانات للتسعير"""
        # إنشاء الجداول إذا لم تكن موجودة
        pass
    
    def load_default_data(self):
        """تحميل البيانات الافتراضية"""
        # تحميل الفئات ووحدات القياس الافتراضية
        pass
    
    def get_project_pricing_summary(self, project_id):
        """الحصول على ملخص التسعير للمشروع"""
        pass
    
    def import_pricing_data(self, file_path, import_type):
        """استيراد بيانات التسعير من ملف خارجي"""
        pass
    
    def export_pricing_data(self, project_id, export_type, file_path):
        """تصدير بيانات التسعير إلى ملف خارجي"""
        pass
```

### 2. مدير بنود التسعير (PricingItemManager)
```python
class PricingItemManager:
    """فئة إدارة بنود التسعير"""
    
    def __init__(self, db_connector):
        """تهيئة مدير بنود التسعير"""
        self.db = db_connector
    
    def get_all_base_items(self, filters=None):
        """الحصول على جميع البنود الأساسية"""
        pass
    
    def get_base_item_by_id(self, item_id):
        """الحصول على بند أساسي بواسطة المعرف"""
        pass
    
    def add_base_item(self, item_data):
        """إضافة بند أساسي جديد"""
        pass
    
    def update_base_item(self, item_id, item_data):
        """تحديث بند أساسي"""
        pass
    
    def delete_base_item(self, item_id):
        """حذف بند أساسي"""
        pass
    
    def get_project_items(self, project_id):
        """الحصول على بنود المشروع"""
        pass
    
    def add_project_item(self, project_id, item_data):
        """إضافة بند للمشروع"""
        pass
    
    def update_project_item(self, item_id, item_data):
        """تحديث بند المشروع"""
        pass
    
    def delete_project_item(self, item_id):
        """حذف بند المشروع"""
        pass
    
    def get_item_components(self, item_id):
        """الحصول على مكونات البند"""
        pass
    
    def add_item_component(self, item_id, component_data):
        """إضافة مكون للبند"""
        pass
    
    def update_item_component(self, component_id, component_data):
        """تحديث مكون البند"""
        pass
    
    def delete_item_component(self, component_id):
        """حذف مكون البند"""
        pass
    
    def get_categories(self):
        """الحصول على فئات البنود"""
        pass
    
    def get_measurement_units(self):
        """الحصول على وحدات القياس"""
        pass
    
    def get_templates(self):
        """الحصول على نماذج التسعير"""
        pass
    
    def get_template_items(self, template_id):
        """الحصول على بنود النموذج"""
        pass
    
    def apply_template_to_project(self, project_id, template_id):
        """تطبيق نموذج على مشروع"""
        pass
```

### 3. حاسبة التكاليف (CostCalculator)
```python
class CostCalculator:
    """فئة حساب التكاليف"""
    
    def __init__(self, db_connector):
        """تهيئة حاسبة التكاليف"""
        self.db = db_connector
    
    def calculate_direct_costs(self, project_id):
        """حساب التكاليف المباشرة"""
        pass
    
    def calculate_indirect_costs(self, project_id, indirect_cost_percentage):
        """حساب التكاليف غير المباشرة"""
        pass
    
    def calculate_profit_margin(self, project_id, profit_percentage):
        """حساب هامش الربح"""
        pass
    
    def calculate_risk_contingency(self, project_id, risk_factors):
        """حساب احتياطي المخاطر"""
        pass
    
    def calculate_taxes_and_fees(self, project_id, tax_rates):
        """حساب الضرائب والرسوم"""
        pass
    
    def calculate_total_cost(self, project_id):
        """حساب التكلفة الإجمالية"""
        pass
    
    def calculate_unit_rates(self, project_id):
        """حساب معدلات الوحدات"""
        pass
    
    def apply_adjustment_factors(self, project_id, factors):
        """تطبيق عوامل التعديل"""
        pass
    
    def calculate_cost_breakdown(self, project_id):
        """حساب تفصيل التكاليف"""
        pass
```

### 4. محلل الأسعار (PriceAnalyzer)
```python
class PriceAnalyzer:
    """فئة تحليل الأسعار"""
    
    def __init__(self, db_connector):
        """تهيئة محلل الأسعار"""
        self.db = db_connector
    
    def get_price_history(self, item_id):
        """الحصول على تاريخ الأسعار"""
        pass
    
    def analyze_price_trends(self, item_id, start_date, end_date):
        """تحليل اتجاهات الأسعار"""
        pass
    
    def compare_prices(self, items, date=None):
        """مقارنة الأسعار"""
        pass
    
    def calculate_price_volatility(self, item_id, period):
        """حساب تقلب الأسعار"""
        pass
    
    def perform_sensitivity_analysis(self, project_id, variable_items, ranges):
        """إجراء تحليل الحساسية"""
        pass
    
    def analyze_price_correlations(self, items):
        """تحليل ارتباطات الأسعار"""
        pass
    
    def compare_with_market_prices(self, items):
        """مقارنة مع أسعار السوق"""
        pass
    
    def analyze_cost_drivers(self, project_id):
        """تحليل محركات التكلفة"""
        pass
    
    def generate_price_analysis_charts(self, analysis_type, params):
        """إنشاء رسوم بيانية لتحليل الأسعار"""
        pass
```

### 5. متنبئ الأسعار (PriceForecaster)
```python
class PriceForecaster:
    """فئة التنبؤ بالأسعار"""
    
    def __init__(self, db_connector):
        """تهيئة متنبئ الأسعار"""
        self.db = db_connector
    
    def forecast_price(self, item_id, forecast_date, model_type='arima'):
        """التنبؤ بالسعر"""
        pass
    
    def generate_price_scenarios(self, item_id, forecast_date):
        """إنشاء سيناريوهات الأسعار"""
        pass
    
    def calculate_inflation_impact(self, project_id, inflation_rate, duration):
        """حساب تأثير التضخم"""
        pass
    
    def forecast_project_costs(self, project_id, forecast_date):
        """التنبؤ بتكاليف المشروع"""
        pass
    
    def evaluate_forecast_accuracy(self, item_id):
        """تقييم دقة التنبؤ"""
        pass
    
    def generate_forecast_charts(self, item_id, forecast_date):
        """إنشاء رسوم بيانية للتنبؤ"""
        pass
```

### 6. مولد تقارير التسعير (PricingReportGenerator)
```python
class PricingReportGenerator:
    """فئة إنشاء تقارير التسعير"""
    
    def __init__(self, db_connector):
        """تهيئة مولد تقارير التسعير"""
        self.db = db_connector
    
    def generate_cost_summary_report(self, project_id):
        """إنشاء تقرير ملخص التكاليف"""
        pass
    
    def generate_detailed_items_report(self, project_id):
        """إنشاء تقرير تفصيلي للبنود"""
        pass
    
    def generate_price_comparison_report(self, items, parameters):
        """إنشاء تقرير مقارنة الأسعار"""
        pass
    
    def generate_sensitivity_analysis_report(self, project_id, parameters):
        """إنشاء تقرير تحليل الحساسية"""
        pass
    
    def generate_price_forecast_report(self, items, forecast_date):
        """إنشاء تقرير التنبؤ بالأسعار"""
        pass
    
    def generate_price_risk_report(self, project_id):
        """إنشاء تقرير مخاطر الأسعار"""
        pass
    
    def export_report_to_pdf(self, report_data, file_path):
        """تصدير التقرير إلى PDF"""
        pass
    
    def export_report_to_excel(self, report_data, file_path):
        """تصدير التقرير إلى Excel"""
        pass
```

## تصميم واجهة المستخدم

### 1. الشاشة الرئيسية لوحدة التسعير

```
+--------------------------------------------------+
|                  وحدة التسعير                    |
+--------------------------------------------------+
|                                                  |
|  +----------------+  +----------------------+    |
|  | المناقصات      |  | إحصائيات التسعير     |    |
|  | الحالية        |  |                      |    |
|  |                |  |                      |    |
|  |                |  |                      |    |
|  |                |  |                      |    |
|  +----------------+  +----------------------+    |
|                                                  |
|  +----------------+  +----------------------+    |
|  | الوصول         |  | آخر التحديثات        |    |
|  | السريع         |  |                      |    |
|  |                |  |                      |    |
|  |                |  |                      |    |
|  |                |  |                      |    |
|  +----------------+  +----------------------+    |
|                                                  |
+--------------------------------------------------+
```

### 2. شاشة إدارة بنود التسعير

```
+--------------------------------------------------+
|                إدارة بنود التسعير                |
+--------------------------------------------------+
| بحث: [                    ] [تصفية▼] [تصدير]     |
+--------------------------------------------------+
| # | الكود | الوصف | الوحدة | الكمية | السعر | المجموع |
+--------------------------------------------------+
| 1 |       |       |        |        |      |        |
| 2 |       |       |        |        |      |        |
| 3 |       |       |        |        |      |        |
| 4 |       |       |        |        |      |        |
| 5 |       |       |        |        |      |        |
+--------------------------------------------------+
| [إضافة بند] [حذف المحدد] [استيراد من Excel]      |
+--------------------------------------------------+
| المجموع الكلي:                                   |
+--------------------------------------------------+
```

### 3. شاشة تفاصيل البند

```
+--------------------------------------------------+
|                  تفاصيل البند                    |
+--------------------------------------------------+
| الكود: [        ]  الوصف: [                    ] |
| الفئة: [        ▼] الوحدة: [                  ▼] |
+--------------------------------------------------+
| مكونات البند:                                    |
+--------------------------------------------------+
| النوع | الوصف | الوحدة | الكمية | السعر | المجموع |
+--------------------------------------------------+
| مواد |      |        |        |      |        |
| عمالة |      |        |        |      |        |
| معدات |      |        |        |      |        |
| أخرى |      |        |        |      |        |
+--------------------------------------------------+
| [إضافة مكون] [حذف المحدد]                        |
+--------------------------------------------------+
| التكلفة المباشرة:                                |
| التكلفة غير المباشرة:                            |
| هامش الربح:                                      |
| احتياطي المخاطر:                                 |
| السعر النهائي:                                   |
+--------------------------------------------------+
| [حفظ] [إلغاء]                                    |
+--------------------------------------------------+
```

### 4. شاشة تحليل الأسعار

```
+--------------------------------------------------+
|                 تحليل الأسعار                    |
+--------------------------------------------------+
| [اختيار البند▼] [الفترة الزمنية▼] [تحليل]       |
+--------------------------------------------------+
|                                                  |
|                                                  |
|                                                  |
|              (رسم بياني للأسعار)                 |
|                                                  |
|                                                  |
|                                                  |
+--------------------------------------------------+
| إحصائيات:                                        |
| - متوسط السعر:                                   |
| - أعلى سعر:                                      |
| - أدنى سعر:                                      |
| - معدل التغير:                                   |
| - التقلب:                                        |
+--------------------------------------------------+
| [مقارنة مع بنود أخرى] [تصدير التحليل]            |
+--------------------------------------------------+
```

### 5. شاشة التنبؤ بالأسعار

```
+--------------------------------------------------+
|                التنبؤ بالأسعار                   |
+--------------------------------------------------+
| [اختيار البند▼] [تاريخ التنبؤ] [نموذج التنبؤ▼]   |
+--------------------------------------------------+
|                                                  |
|                                                  |
|                                                  |
|            (رسم بياني للتنبؤ بالأسعار)           |
|                                                  |
|                                                  |
|                                                  |
+--------------------------------------------------+
| السيناريوهات:                                    |
| - متفائل:                                        |
| - متوسط:                                         |
| - متشائم:                                        |
+--------------------------------------------------+
| عوامل التأثير:                                   |
| - التضخم:                                        |
| - تغيرات السوق:                                  |
| - العوامل الموسمية:                              |
+--------------------------------------------------+
| [تطبيق على المشروع] [تصدير التنبؤ]               |
+--------------------------------------------------+
```

### 6. شاشة تحليل الحساسية

```
+--------------------------------------------------+
|                تحليل الحساسية                    |
+--------------------------------------------------+
| المشروع: [                                     ▼] |
+--------------------------------------------------+
| المتغيرات:                                       |
| [✓] أسعار المواد الخام (±20%)                    |
| [✓] تكلفة العمالة (±15%)                         |
| [✓] تكلفة المعدات (±10%)                         |
| [ ] المصاريف العامة (±5%)                        |
+--------------------------------------------------+
|                                                  |
|                                                  |
|            (رسم بياني لتحليل الحساسية)           |
|                                                  |
|                                                  |
|                                                  |
+--------------------------------------------------+
| النتائج:                                         |
| - أكثر العوامل تأثيراً:                          |
| - نطاق التغير المتوقع:                           |
| - توصيات:                                        |
+--------------------------------------------------+
| [تحديث التحليل] [تصدير النتائج]                  |
+--------------------------------------------------+
```

### 7. شاشة التقارير

```
+--------------------------------------------------+
|                   التقارير                       |
+--------------------------------------------------+
| [نوع التقرير▼] [المشروع▼] [إنشاء تقرير]          |
+--------------------------------------------------+
| التقارير المتاحة:                                |
|                                                  |
| ○ ملخص التكاليف                                  |
| ○ تفصيل البنود                                   |
| ○ مقارنة الأسعار                                 |
| ○ تحليل الحساسية                                 |
| ○ التنبؤ بالأسعار                                |
| ○ مخاطر الأسعار                                  |
|                                                  |
+--------------------------------------------------+
| خيارات التقرير:                                  |
|                                                  |
| [✓] تضمين الرسوم البيانية                        |
| [✓] تضمين التوصيات                               |
| [ ] تضمين البيانات التفصيلية                     |
|                                                  |
+--------------------------------------------------+
| [PDF] [Excel] [طباعة]                            |
+--------------------------------------------------+
```

## تكامل النظام

### 1. تكامل مع وحدة تحليل المستندات
- استخراج بنود التسعير من وثائق المناقصة
- تحديد الكميات والمواصفات من المستندات
- مقارنة البنود المستخرجة مع قاعدة البيانات

### 2. تكامل مع وحدة تحليل المخاطر
- تحديد المخاطر المرتبطة بالتسعير
- تقييم تأثير المخاطر على التكاليف
- تحديد احتياطي المخاطر المناسب

### 3. تكامل مع وحدة إدارة المشاريع
- متابعة التكاليف الفعلية مقابل المخططة
- تحديث التنبؤات بناءً على بيانات المشروع الفعلية
- تحليل انحرافات التكاليف

### 4. تكامل مع وحدة التقارير
- إنشاء تقارير متكاملة تشمل بيانات التسعير
- دمج تحليلات التسعير في تقارير المشروع
- توفير لوحات معلومات متكاملة

## خطة التنفيذ التفصيلية

### المرحلة 1: إعداد البنية التحتية (3 أيام)
- تصميم وإنشاء جداول قاعدة البيانات
- إعداد هيكل الملفات والمجلدات
- تهيئة البيئة التطويرية

### المرحلة 2: تنفيذ الوظائف الأساسية (5 أيام)
- تنفيذ فئة مدير التسعير
- تنفيذ فئة مدير بنود التسعير
- تنفيذ فئة حاسبة التكاليف
- إنشاء واجهات المستخدم الأساسية

### المرحلة 3: تنفيذ وظائف التحليل (7 أيام)
- تنفيذ فئة محلل الأسعار
- تنفيذ فئة متنبئ الأسعار
- إنشاء الرسوم البيانية والتحليلات
- تنفيذ واجهات المستخدم للتحليل

### المرحلة 4: تنفيذ التقارير والتكامل (5 أيام)
- تنفيذ فئة مولد تقارير التسعير
- تكامل مع الوحدات الأخرى
- إنشاء واجهات المستخدم للتقارير
- اختبار التكامل

### المرحلة 5: الاختبار والتحسين (3 أيام)
- اختبار جميع الوظائف
- تحسين الأداء
- إصلاح الأخطاء
- تحسين واجهة المستخدم

### المرحلة 6: التوثيق والتسليم (2 أيام)
- إعداد وثائق المستخدم
- إعداد وثائق المطور
- تجهيز النسخة النهائية
- تسليم النظام
